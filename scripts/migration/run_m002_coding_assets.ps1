[CmdletBinding()]
param(
    [switch]$Execute,
    [switch]$DeleteSource,
    [switch]$WhatIfOnly,
    [string]$StudyBookRoot = 'D:\StudyBook',
    [string]$WorkspaceRoot = 'D:\Workspace',
    [string]$BackupRoot = 'C:\Users\shareuser\migration_backups',
    [int]$RollbackRetentionDays = 7
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if ($DeleteSource -and -not $Execute) {
    throw '-DeleteSource requires -Execute.'
}

if ($WhatIfOnly) {
    $Execute = $false
    $DeleteSource = $false
}

$runTs = Get-Date -Format 'yyyyMMdd_HHmmss'
$codingRoot = Join-Path $StudyBookRoot 'coding_challenges'
$metaRoot = Join-Path $codingRoot '_migration_meta'
$runMeta = Join-Path $metaRoot ("run_" + $runTs)

$null = New-Item -ItemType Directory -Path $runMeta -Force

$moveMap = New-Object System.Collections.Generic.List[object]
$conflicts = New-Object System.Collections.Generic.List[string]

function New-RelPath {
    param([string]$Base, [string]$Full)
    $uriBase = New-Object System.Uri((Resolve-Path -LiteralPath $Base).Path + [IO.Path]::DirectorySeparatorChar)
    $uriFull = New-Object System.Uri((Resolve-Path -LiteralPath $Full).Path)
    [System.Uri]::UnescapeDataString($uriBase.MakeRelativeUri($uriFull).ToString()).Replace('/', '\\')
}

function Get-FileHashSafe {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { return '' }
    (Get-FileHash -Algorithm SHA256 -LiteralPath $Path).Hash
}

function Ensure-Parent {
    param([string]$Path)
    $parent = Split-Path -Parent $Path
    if ($parent) { $null = New-Item -ItemType Directory -Path $parent -Force }
}

function Resolve-ConflictTarget {
    param([string]$TargetPath)
    $dir = Split-Path -Parent $TargetPath
    $name = [IO.Path]::GetFileNameWithoutExtension($TargetPath)
    $ext = [IO.Path]::GetExtension($TargetPath)
    for ($i = 1; $i -le 500; $i++) {
        $candidate = Join-Path $dir ("{0}__dup{1:D3}{2}" -f $name, $i, $ext)
        if (-not (Test-Path -LiteralPath $candidate)) {
            return $candidate
        }
    }
    throw "Could not resolve conflict target for $TargetPath"
}

function Copy-WithMap {
    param(
        [string]$Group,
        [string]$SourcePath,
        [string]$TargetPath,
        [string]$Note = ''
    )

    if (-not (Test-Path -LiteralPath $SourcePath -PathType Leaf)) {
        $moveMap.Add([pscustomobject]@{ Group=$Group; Source=$SourcePath; Target=$TargetPath; Status='missing_source'; Note=$Note })
        return
    }

    $finalTarget = $TargetPath
    $status = 'copied'

    if (Test-Path -LiteralPath $finalTarget -PathType Leaf) {
        $srcHash = Get-FileHashSafe -Path $SourcePath
        $dstHash = Get-FileHashSafe -Path $finalTarget
        if ($srcHash -eq $dstHash) {
            $status = 'duplicate_existing'
        } else {
            $finalTarget = Resolve-ConflictTarget -TargetPath $finalTarget
            $status = 'conflict_renamed'
            $conflicts.Add("Conflict: $SourcePath -> $TargetPath ; resolved to $finalTarget")
        }
    }

    if ($Execute -and ($status -ne 'duplicate_existing')) {
        Ensure-Parent -Path $finalTarget
        Copy-Item -LiteralPath $SourcePath -Destination $finalTarget -Force
    }

    $moveMap.Add([pscustomobject]@{
        Group = $Group
        Source = $SourcePath
        Target = $finalTarget
        Status = $status
        Note = $Note
    })
}

function Add-GroupFiles {
    param(
        [string]$Group,
        [string]$SourceBase,
        [string]$TargetBase,
        [scriptblock]$Transform
    )

    if (-not (Test-Path -LiteralPath $SourceBase)) {
        $moveMap.Add([pscustomobject]@{ Group=$Group; Source=$SourceBase; Target=$TargetBase; Status='missing_group_source'; Note='' })
        return
    }

    $files = Get-ChildItem -LiteralPath $SourceBase -Recurse -File
    foreach ($file in $files) {
        $rel = New-RelPath -Base $SourceBase -Full $file.FullName
        $targetRel = if ($Transform) { & $Transform $file $rel } else { $rel }
        if ([string]::IsNullOrWhiteSpace($targetRel)) {
            $moveMap.Add([pscustomobject]@{ Group=$Group; Source=$file.FullName; Target=''; Status='skipped'; Note='transform returned empty' })
            continue
        }
        $target = Join-Path $TargetBase $targetRel
        Copy-WithMap -Group $Group -SourcePath $file.FullName -TargetPath $target
    }
}

function Get-Inventory {
    param([string]$Root, [string]$Label)
    if (-not (Test-Path -LiteralPath $Root)) { return @() }
    $files = Get-ChildItem -LiteralPath $Root -Recurse -File
    $rows = foreach ($f in $files) {
        [pscustomobject]@{
            label = $Label
            root = $Root
            path = $f.FullName
            rel = New-RelPath -Base $Root -Full $f.FullName
            size = $f.Length
            sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $f.FullName).Hash
            last_write_utc = $f.LastWriteTimeUtc.ToString('o')
        }
    }
    return $rows
}

function Invoke-SecretScan {
    param([string]$ScanRoot)

    $patterns = @(
        '(?i)AKIA[0-9A-Z]{16}',
        '(?i)ASIA[0-9A-Z]{16}',
        '(?i)-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----',
        '(?i)xox[baprs]-[0-9A-Za-z-]{10,}',
        '(?i)ghp_[0-9A-Za-z]{20,}',
        '(?i)AIza[0-9A-Za-z_-]{35}',
        '(?i)dapi[0-9a-f]{20,}',
        '(?i)mongodb\+srv:\/\/\S+'
    )

    $extensions = @('.md','.txt','.py','.ps1','.ipynb','.json','.yaml','.yml','.env')
    if (-not (Test-Path -LiteralPath $ScanRoot)) { return @() }

    $hits = New-Object System.Collections.Generic.List[object]
    $files = Get-ChildItem -LiteralPath $ScanRoot -Recurse -File | Where-Object { $extensions -contains $_.Extension.ToLower() -or $_.Name -like '*.env*' }

    foreach ($file in $files) {
        try {
            $content = Get-Content -LiteralPath $file.FullName -Raw -ErrorAction Stop
        } catch {
            continue
        }

        foreach ($p in $patterns) {
            $m = [regex]::Match($content, $p)
            if ($m.Success) {
                $hits.Add([pscustomobject]@{
                    file = $file.FullName
                    pattern = $p
                    match_preview = $m.Value.Substring(0, [Math]::Min(40, $m.Value.Length))
                })
            }
        }
    }

    return $hits
}

# Target folders
$targets = @(
    'leetcode\\by_topic',
    'leetcode\\active',
    'leetcode\\reviews',
    'leetcode\\tracker',
    'guides\\data_structures',
    'guides\\algorithms',
    'guides\\patterns',
    'guides\\advanced\\recursion_and_backtracking',
    'guides\\advanced\\dynamic_programming',
    'guides\\advanced\\trees_and_graphs',
    'guides\\advanced\\theory',
    'python\\fundamentals',
    'python\\data_libraries\\pandas',
    'python\\data_libraries\\numpy',
    'python\\data_libraries\\_misc',
    'study_plans\\daily',
    'study_plans\\templates',
    'study_plans\\instructions',
    'study_plans\\_archive\\change_reports',
    '_archive\\workspace_legacy'
)

foreach ($t in $targets) {
    if ($Execute) { $null = New-Item -ItemType Directory -Path (Join-Path $codingRoot $t) -Force }
}

# Inventories before
$sourceRoots = @(
    (Join-Path $WorkspaceRoot 'PracticeHistory\\LeetCode'),
    (Join-Path $WorkspaceRoot 'newStudy'),
    (Join-Path $WorkspaceRoot 'Basics\\DSA'),
    (Join-Path $WorkspaceRoot 'Basics\\Advanced_DSA'),
    (Join-Path $WorkspaceRoot 'Basics\\Language\\Python'),
    (Join-Path $WorkspaceRoot 'Basics\\Python_Data'),
    (Join-Path $WorkspaceRoot 'StudyPlans'),
    (Join-Path $WorkspaceRoot 'archive'),
    (Join-Path $WorkspaceRoot 'leetcode_tracker.xlsx'),
    (Join-Path $WorkspaceRoot 'WORKSPACE_PROTOCOL.md'),
    (Join-Path $WorkspaceRoot 'TRACKER.md'),
    (Join-Path $WorkspaceRoot 'WORKFLOW.md')
)

$preInventory = New-Object System.Collections.Generic.List[object]
foreach ($root in $sourceRoots) {
    if (Test-Path -LiteralPath $root -PathType Leaf) {
        $preInventory.Add([pscustomobject]@{
            label = 'source_file'
            root = $root
            path = $root
            rel = [IO.Path]::GetFileName($root)
            size = (Get-Item -LiteralPath $root).Length
            sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $root).Hash
            last_write_utc = (Get-Item -LiteralPath $root).LastWriteTimeUtc.ToString('o')
        })
    } elseif (Test-Path -LiteralPath $root -PathType Container) {
        foreach ($row in (Get-Inventory -Root $root -Label 'source_dir')) { $preInventory.Add($row) }
    }
}
$preInventory | ConvertTo-Json -Depth 5 | Set-Content -Path (Join-Path $runMeta 'pre_migration_inventory.json')

# Group A: LeetCode by topic
$topicMap = @{
    'Arrays' = 'arrays'
    'BinarySearch' = 'binary_search'
    'BitManipulation' = 'bit_manipulation'
    'DP' = 'dynamic_programming'
    'Graphs' = 'graphs'
    'Hashing' = 'hashing'
    'Heaps' = 'heaps'
    'Intervals' = 'intervals'
    'LinkedList' = 'linked_list'
    'Mixed' = 'mixed'
    'SlidingWindow' = 'sliding_window'
    'Stack' = 'stack'
    'Trees' = 'trees'
    'TwoPointers' = 'two_pointers'
}
$srcA = Join-Path $WorkspaceRoot 'PracticeHistory\\LeetCode'
if (Test-Path -LiteralPath $srcA) {
    $topicDirs = Get-ChildItem -LiteralPath $srcA -Directory
    foreach ($dir in $topicDirs) {
        $mapped = if ($topicMap.ContainsKey($dir.Name)) { $topicMap[$dir.Name] } else { $dir.Name.ToLower() }
        Add-GroupFiles -Group 'A_leetcode_by_topic' -SourceBase $dir.FullName -TargetBase (Join-Path $codingRoot ("leetcode\\by_topic\\$mapped")) -Transform { param($f,$rel) $rel }
    }
}

# Group B: active newStudy as-is
Add-GroupFiles -Group 'B_leetcode_active' -SourceBase (Join-Path $WorkspaceRoot 'newStudy') -TargetBase (Join-Path $codingRoot 'leetcode\\active') -Transform { param($f,$rel) $rel }

# Group C: reviews
$srcC = Join-Path $WorkspaceRoot 'Basics\\DSA'
if (Test-Path -LiteralPath $srcC) {
    Get-ChildItem -LiteralPath $srcC -File -Filter 'LC*_review.md' | ForEach-Object {
        Copy-WithMap -Group 'C_leetcode_reviews' -SourcePath $_.FullName -TargetPath (Join-Path $codingRoot ("leetcode\\reviews\\" + $_.Name))
    }
}

# Group D: guides by explicit mapping
$dsaMap = @{
    'arrays_master_guide.ipynb' = 'guides\\data_structures\\arrays.ipynb'
    'linked_list_master_guide.ipynb' = 'guides\\data_structures\\linked_lists.ipynb'
    'stack_master_guide.ipynb' = 'guides\\data_structures\\stacks.ipynb'
    'hashmap_master_guide.ipynb' = 'guides\\data_structures\\hashmaps.ipynb'
    'heap_master_guide.ipynb' = 'guides\\data_structures\\heaps.ipynb'
    'deque_master_guide.ipynb' = 'guides\\data_structures\\deques.ipynb'
    'multidimensional_tensors_master_guide.ipynb' = 'guides\\data_structures\\tensors.ipynb'
    'binary_search_master_guide.ipynb' = 'guides\\algorithms\\binary_search.ipynb'
    'sorting_master_guide.ipynb' = 'guides\\algorithms\\sorting.ipynb'
    'sliding_window_master_guide.ipynb' = 'guides\\algorithms\\sliding_window.ipynb'
    'two_pointer_master_guide.ipynb' = 'guides\\algorithms\\two_pointers.ipynb'
    'prefix_sum_master_guide.ipynb' = 'guides\\algorithms\\prefix_sum.ipynb'
    'monotonic_stack_master_guide.ipynb' = 'guides\\patterns\\monotonic_stack.ipynb'
    'monotonic_deque_master_guide.ipynb' = 'guides\\patterns\\monotonic_deque.ipynb'
    'bit_operations_master_guide.ipynb' = 'guides\\patterns\\bit_operations.ipynb'
    'intervals_master_guide.ipynb' = 'guides\\patterns\\intervals.ipynb'
    'string_master_guide.ipynb' = 'guides\\patterns\\strings.ipynb'
}
$advMap = @{
    'backtracking_master_guide.ipynb' = 'guides\\advanced\\recursion_and_backtracking\\backtracking.ipynb'
    'recursion_guide.ipynb' = 'guides\\advanced\\recursion_and_backtracking\\recursion.ipynb'
    'greedy_master_guide.ipynb' = 'guides\\advanced\\recursion_and_backtracking\\greedy.ipynb'
    'dp_1d_master_guide.ipynb' = 'guides\\advanced\\dynamic_programming\\dp_1d.ipynb'
    'dp_2d_master_guide.ipynb' = 'guides\\advanced\\dynamic_programming\\dp_2d.ipynb'
    'dp_trees_master_guide.ipynb' = 'guides\\advanced\\dynamic_programming\\dp_trees.ipynb'
    'string_dp_master_guide.ipynb' = 'guides\\advanced\\dynamic_programming\\dp_string.ipynb'
    'knapsack_master_guide.ipynb' = 'guides\\advanced\\dynamic_programming\\dp_knapsack.ipynb'
    'binary_tree_master_guide.ipynb' = 'guides\\advanced\\trees_and_graphs\\binary_trees.ipynb'
    'bst_master_guide.ipynb' = 'guides\\advanced\\trees_and_graphs\\bst.ipynb'
    'segment_tree_master_guide.ipynb' = 'guides\\advanced\\trees_and_graphs\\segment_trees.ipynb'
    'union_find_master_guide.ipynb' = 'guides\\advanced\\trees_and_graphs\\union_find.ipynb'
    'trie_master_guide.ipynb' = 'guides\\advanced\\trees_and_graphs\\tries.ipynb'
    'topological_sort_master_guide.ipynb' = 'guides\\advanced\\trees_and_graphs\\topological_sort.ipynb'
    'graphs_bfs_master_guide.ipynb' = 'guides\\advanced\\trees_and_graphs\\bfs.ipynb'
    'graphs_dfs_master_guide.ipynb' = 'guides\\advanced\\trees_and_graphs\\dfs.ipynb'
    'oop_patterns_guide.ipynb' = 'guides\\advanced\\theory\\oop_patterns.ipynb'
    'complexity_reference_guide.ipynb' = 'guides\\advanced\\theory\\complexity_analysis.ipynb'
    'math_number_theory_master_guide.ipynb' = 'guides\\advanced\\theory\\math_number_theory.ipynb'
}

$srcDSA = Join-Path $WorkspaceRoot 'Basics\\DSA'
if (Test-Path -LiteralPath $srcDSA) {
    Get-ChildItem -LiteralPath $srcDSA -File -Filter '*.ipynb' | ForEach-Object {
        if ($dsaMap.ContainsKey($_.Name)) {
            Copy-WithMap -Group 'D_guides' -SourcePath $_.FullName -TargetPath (Join-Path $codingRoot $dsaMap[$_.Name])
        } else {
            Copy-WithMap -Group 'D_guides' -SourcePath $_.FullName -TargetPath (Join-Path $codingRoot ("_archive\\workspace_legacy\\guides_unmapped\\" + $_.Name)) -Note 'unmapped_dsa_guide'
        }
    }
}

$srcADV = Join-Path $WorkspaceRoot 'Basics\\Advanced_DSA'
if (Test-Path -LiteralPath $srcADV) {
    Get-ChildItem -LiteralPath $srcADV -File -Filter '*.ipynb' | ForEach-Object {
        if ($advMap.ContainsKey($_.Name)) {
            Copy-WithMap -Group 'D_guides' -SourcePath $_.FullName -TargetPath (Join-Path $codingRoot $advMap[$_.Name])
        } else {
            Copy-WithMap -Group 'D_guides' -SourcePath $_.FullName -TargetPath (Join-Path $codingRoot ("_archive\\workspace_legacy\\advanced_guides_unmapped\\" + $_.Name)) -Note 'unmapped_advanced_guide'
        }
    }
}

# Group E: python fundamentals + data libraries
Add-GroupFiles -Group 'E_python_fundamentals' -SourceBase (Join-Path $WorkspaceRoot 'Basics\\Language\\Python') -TargetBase (Join-Path $codingRoot 'python\\fundamentals') -Transform { param($f,$rel) $rel }

$srcPyData = Join-Path $WorkspaceRoot 'Basics\\Python_Data'
if (Test-Path -LiteralPath $srcPyData) {
    Get-ChildItem -LiteralPath $srcPyData -Recurse -File | ForEach-Object {
        $n = $_.Name.ToLower()
        $sub = if ($n -like 'pandas*') { 'pandas' } elseif ($n -like 'numpy*') { 'numpy' } else { '_misc' }
        Copy-WithMap -Group 'E_python_data' -SourcePath $_.FullName -TargetPath (Join-Path $codingRoot ("python\\data_libraries\\$sub\\" + $_.Name))
    }
}

# Group F: study plans
$srcSP = Join-Path $WorkspaceRoot 'StudyPlans'
if (Test-Path -LiteralPath $srcSP) {
    Add-GroupFiles -Group 'F_study_plans' -SourceBase (Join-Path $srcSP 'daily') -TargetBase (Join-Path $codingRoot 'study_plans\\daily') -Transform { param($f,$rel) $rel }
    Add-GroupFiles -Group 'F_study_plans' -SourceBase (Join-Path $srcSP 'templates') -TargetBase (Join-Path $codingRoot 'study_plans\\templates') -Transform { param($f,$rel) $rel }
    Add-GroupFiles -Group 'F_study_plans' -SourceBase (Join-Path $srcSP 'instructions') -TargetBase (Join-Path $codingRoot 'study_plans\\instructions') -Transform { param($f,$rel) $rel }
    Add-GroupFiles -Group 'F_study_plans' -SourceBase (Join-Path $srcSP 'change_reports') -TargetBase (Join-Path $codingRoot 'study_plans\\_archive\\change_reports') -Transform { param($f,$rel) $rel }
}

# Group G: root support + archive
$rootMap = @{
    'leetcode_tracker.xlsx' = 'leetcode\\tracker\\leetcode_tracker.xlsx'
    'WORKSPACE_PROTOCOL.md' = '_archive\\workspace_legacy\\WORKSPACE_PROTOCOL.md'
    'TRACKER.md' = '_archive\\workspace_legacy\\TRACKER.md'
    'WORKFLOW.md' = '_archive\\workspace_legacy\\WORKFLOW.md'
}
foreach ($k in $rootMap.Keys) {
    Copy-WithMap -Group 'G_support_files' -SourcePath (Join-Path $WorkspaceRoot $k) -TargetPath (Join-Path $codingRoot $rootMap[$k])
}
Add-GroupFiles -Group 'G_archive' -SourceBase (Join-Path $WorkspaceRoot 'archive') -TargetBase (Join-Path $codingRoot '_archive\\workspace_legacy\\deprecated_utils') -Transform { param($f,$rel) $rel }

# Write move map and conflicts
$moveCsv = Join-Path $runMeta 'move_map.csv'
$moveMap | Export-Csv -Path $moveCsv -NoTypeInformation -Encoding UTF8
$confPath = Join-Path $runMeta 'conflicts_report.md'
if ($conflicts.Count -eq 0) {
    "# Conflicts Report`n`nNo conflicts detected." | Set-Content -Path $confPath
} else {
    @("# Conflicts Report","",$conflicts) | Set-Content -Path $confPath
}

# Post inventory
$postInventory = Get-Inventory -Root $codingRoot -Label 'target'
$postInventory | ConvertTo-Json -Depth 5 | Set-Content -Path (Join-Path $runMeta 'post_migration_inventory.json')

# Secret scan gate
$scanHits = @(Invoke-SecretScan -ScanRoot $codingRoot)
$scanPath = Join-Path $runMeta 'secret_scan_hits.json'
$scanHits | ConvertTo-Json -Depth 5 | Set-Content -Path $scanPath

if ($scanHits.Count -gt 0 -and $DeleteSource) {
    throw "Secret scan found $($scanHits.Count) hits. Aborting source deletion. Review $scanPath"
}

# Generate INDEX and manifests
$indexPath = Join-Path $codingRoot 'INDEX.md'
$coveragePath = Join-Path $codingRoot 'leetcode\\TOPIC_COVERAGE.md'
$roadmapPath = Join-Path $codingRoot 'ROADMAP_INPUT_MANIFEST.md'

if ($Execute) {
    $topicStats = @()
    $topicRoot = Join-Path $codingRoot 'leetcode\\by_topic'
    if (Test-Path -LiteralPath $topicRoot) {
        $topicStats = Get-ChildItem -LiteralPath $topicRoot -Directory | ForEach-Object {
            [pscustomobject]@{ topic=$_.Name; file_count=(Get-ChildItem -LiteralPath $_.FullName -Recurse -File | Measure-Object).Count }
        } | Sort-Object topic
    }

    @(
        '# Coding Challenges Index',
        '',
        '- `leetcode/by_topic`: curated categorized solutions',
        '- `leetcode/active`: daily notebook workspace from `newStudy`',
        '- `leetcode/reviews`: LC review markdown files',
        '- `guides`: concept notebooks',
        '- `python`: Python fundamentals and data library notes',
        '- `study_plans`: migrated planning assets',
        '- `_migration_meta`: machine-readable migration artifacts',
        ''
    ) | Set-Content -Path $indexPath

    $coverageLines = New-Object System.Collections.Generic.List[string]
    $coverageLines.Add('# LeetCode Topic Coverage')
    $coverageLines.Add('')
    $coverageLines.Add('| Topic | File Count |')
    $coverageLines.Add('|---|---:|')
    foreach ($r in $topicStats) {
        $coverageLines.Add("| $($r.topic) | $($r.file_count) |")
    }
    $coverageLines | Set-Content -Path $coveragePath

    @(
        '# Roadmap Input Manifest',
        '',
        "- Generated at: $(Get-Date -Format o)",
        "- Migration run id: run_$runTs",
        "- Source root: $WorkspaceRoot",
        "- Target root: $codingRoot",
        "- Move map: _migration_meta\\run_$runTs\\move_map.csv",
        "- Conflicts report: _migration_meta\\run_$runTs\\conflicts_report.md",
        "- Secret scan: _migration_meta\\run_$runTs\\secret_scan_hits.json",
        "- Pre inventory: _migration_meta\\run_$runTs\\pre_migration_inventory.json",
        "- Post inventory: _migration_meta\\run_$runTs\\post_migration_inventory.json",
        ''
    ) | Set-Content -Path $roadmapPath
}

# Optional source deletion and backup
$deletedCount = 0
$backupPath = ''
if ($Execute -and $DeleteSource) {
    $backupPath = Join-Path $BackupRoot ("m002_backup_" + $runTs)
    $null = New-Item -ItemType Directory -Path $backupPath -Force

    $toBackup = @(
        'PracticeHistory\\LeetCode',
        'newStudy',
        'Basics\\DSA',
        'Basics\\Advanced_DSA',
        'Basics\\Language\\Python',
        'Basics\\Python_Data',
        'StudyPlans',
        'archive'
    )

    foreach ($rel in $toBackup) {
        $src = Join-Path $WorkspaceRoot $rel
        if (Test-Path -LiteralPath $src) {
            $dst = Join-Path $backupPath $rel
            $null = New-Item -ItemType Directory -Path (Split-Path -Parent $dst) -Force
            Copy-Item -LiteralPath $src -Destination $dst -Recurse -Force
        }
    }

    foreach ($k in $rootMap.Keys) {
        $src = Join-Path $WorkspaceRoot $k
        if (Test-Path -LiteralPath $src) {
            Copy-Item -LiteralPath $src -Destination (Join-Path $backupPath $k) -Force
        }
    }

    # Delete source roots
    foreach ($rel in $toBackup) {
        $src = Join-Path $WorkspaceRoot $rel
        if (Test-Path -LiteralPath $src) {
            Remove-Item -LiteralPath $src -Recurse -Force
            $deletedCount++
        }
    }
    foreach ($k in $rootMap.Keys) {
        $src = Join-Path $WorkspaceRoot $k
        if (Test-Path -LiteralPath $src) {
            Remove-Item -LiteralPath $src -Force
            $deletedCount++
        }
    }

    # prune old backups
    if (Test-Path -LiteralPath $BackupRoot) {
        $cutoff = (Get-Date).AddDays(-1 * $RollbackRetentionDays)
        Get-ChildItem -LiteralPath $BackupRoot -Directory | Where-Object { $_.LastWriteTime -lt $cutoff } | ForEach-Object {
            Remove-Item -LiteralPath $_.FullName -Recurse -Force
        }
    }
}

$summary = [pscustomobject]@{
    ok = $true
    execute = [bool]$Execute
    delete_source = [bool]$DeleteSource
    coding_root = $codingRoot
    run_meta = $runMeta
    move_map_entries = $moveMap.Count
    conflicts = $conflicts.Count
    secret_hits = $scanHits.Count
    deleted_source_entries = $deletedCount
    backup_path = $backupPath
}

$summary | ConvertTo-Json -Depth 4 | Set-Content -Path (Join-Path $runMeta 'summary.json')
$summary | ConvertTo-Json -Depth 4


