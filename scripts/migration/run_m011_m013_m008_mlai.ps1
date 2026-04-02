[CmdletBinding()]
param(
    [switch]$Execute,
    [switch]$DeleteMlAiSource,
    [switch]$WhatIfOnly,
    [string]$StudyBookRoot = 'D:\StudyBook',
    [string]$WorkspaceRoot = 'D:\Workspace',
    [string]$BackupRoot = 'C:\Users\shareuser\migration_backups'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if ($DeleteMlAiSource -and -not $Execute) {
    throw '-DeleteMlAiSource requires -Execute.'
}
if ($WhatIfOnly) {
    $Execute = $false
    $DeleteMlAiSource = $false
}

$runTs = Get-Date -Format 'yyyyMMdd_HHmmss'
$runId = "run_$runTs"

$srcTech = Join-Path $WorkspaceRoot 'Technologies'
$srcTechPrompts = Join-Path $srcTech 'prompts'
$srcInterview = Join-Path $WorkspaceRoot 'Basics\DE_Interview'
$srcMlAi = Join-Path $WorkspaceRoot 'ML_AI'

$tracksRoot = Join-Path $StudyBookRoot 'tracks'
$interviewRoot = Join-Path $StudyBookRoot 'interview'
$legacyTechPrompts = Join-Path $StudyBookRoot '_prompts\legacy\technologies'
$canonicalTechPrompts = Join-Path $StudyBookRoot '_prompts\tracks\technologies'
$mlAiTarget = Join-Path $StudyBookRoot 'tracks\22_ml_platform\ml_ai_pack'

$metaRoot = Join-Path $StudyBookRoot 'temp\migration_meta'
$runMeta = Join-Path $metaRoot $runId
$null = New-Item -ItemType Directory -Path $runMeta -Force

$moveMap = New-Object System.Collections.Generic.List[object]
$targetTouched = New-Object System.Collections.Generic.List[string]
$conflicts = New-Object System.Collections.Generic.List[string]

function Ensure-Dir([string]$Path) { $null = New-Item -ItemType Directory -Path $Path -Force }

function Hash-File([string]$Path) { (Get-FileHash -Algorithm SHA256 -LiteralPath $Path).Hash }

function Rel-Path([string]$Base, [string]$Full) {
    $b = New-Object System.Uri((Resolve-Path -LiteralPath $Base).Path + [IO.Path]::DirectorySeparatorChar)
    $f = New-Object System.Uri((Resolve-Path -LiteralPath $Full).Path)
    [System.Uri]::UnescapeDataString($b.MakeRelativeUri($f).ToString()).Replace('/','\\')
}

function Resolve-Conflict([string]$Target) {
    $dir = Split-Path -Parent $Target
    $name = [IO.Path]::GetFileNameWithoutExtension($Target)
    $ext = [IO.Path]::GetExtension($Target)
    for ($i=1; $i -le 500; $i++) {
        $cand = Join-Path $dir ("{0}__dup{1:D3}{2}" -f $name,$i,$ext)
        if (-not (Test-Path -LiteralPath $cand)) { return $cand }
    }
    throw "Unable to resolve conflict for $Target"
}

function Add-Move([string]$Group,[string]$Source,[string]$Target,[string]$Status,[string]$Note='') {
    $moveMap.Add([pscustomobject]@{group=$Group;source=$Source;target=$Target;status=$Status;note=$Note})
    if ($Status -eq 'copied' -and $Target) { $targetTouched.Add($Target) }
}

function Copy-Mapped([string]$Group,[string]$Source,[string]$Target,[string]$Note='') {
    if (-not (Test-Path -LiteralPath $Source -PathType Leaf)) {
        Add-Move -Group $Group -Source $Source -Target $Target -Status 'missing_source' -Note $Note
        return
    }

    $final = $Target
    $status = 'copied'
    if (Test-Path -LiteralPath $final -PathType Leaf) {
        $srcHash = Hash-File $Source
        $dstHash = Hash-File $final
        if ($srcHash -eq $dstHash) {
            $status = 'duplicate_existing'
        } else {
            $final = Resolve-Conflict $final
            $status = 'conflict_renamed'
            $conflicts.Add("$Source -> $Target resolved to $final")
        }
    }

    if ($Execute -and ($status -ne 'duplicate_existing')) {
        Ensure-Dir (Split-Path -Parent $final)
        Copy-Item -LiteralPath $Source -Destination $final -Force
    }

    Add-Move -Group $Group -Source $Source -Target $final -Status $status -Note $Note
}

function Get-TechTrack([string]$NameNoExt) {
    $n = $NameNoExt.ToLower()

    if ($n -like '*interview_sim*') { return 'interview' }

    if ($n -match '^(kafka_|streaming_|lambda_kappa)') { return '10_streaming' }
    if ($n -match '^(spark_|batch_pipeline_)') { return '11_batch_processing' }
    if ($n -match '^airflow_') { return '12_orchestration' }
    if ($n -match '^(mlflow_|databricks_|feature_store_|vertex_sagemaker_|unity_catalog|lakehouse_)') { return '22_ml_platform' }
    if ($n -match '^(splunk_|great_expectations)') { return '29_observability' }
    return '30_system_design'
}

function Get-TechRound([string]$NameNoExt) {
    $n = $NameNoExt.ToLower()
    if ($n -in @(
        'lambda_kappa_architecture','streaming_pipeline_end2end','batch_pipeline_end2end',
        'platform_decision_matrix','modern_de_stack_2026','system_design_streaming','system_design_batch'
    )) { return 'r3' }

    if ($n -match '(_intro$|_intro_recreated$|_guide$)') { return 'r1' }

    return 'r2'
}

function Sanitize-Text([string]$Content) {
    $out = $Content
    $changed = $false

    $old = $out
    $out = [regex]::Replace($out, '(?i)(mongodb\+srv:\/\/)([^:\s\/]+):([^@\s\/]+)@', '$1<user>:<password>@')
    if ($out -ne $old) { $changed = $true }

    foreach ($pat in @('(?i)AKIA[0-9A-Z]{16}','(?i)ASIA[0-9A-Z]{16}','(?i)ghp_[0-9A-Za-z]{20,}','(?i)dapi[0-9a-f]{20,}','(?i)AIza[0-9A-Za-z_-]{35}')) {
        $old = $out
        $out = [regex]::Replace($out, $pat, '<redacted_secret>')
        if ($out -ne $old) { $changed = $true }
    }

    [pscustomobject]@{content=$out;changed=$changed}
}

function Scan-Secrets([string[]]$Paths) {
    $patterns = @(
        '(?i)AKIA[0-9A-Z]{16}','(?i)ASIA[0-9A-Z]{16}','(?i)-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----',
        '(?i)xox[baprs]-[0-9A-Za-z-]{10,}','(?i)ghp_[0-9A-Za-z]{20,}','(?i)AIza[0-9A-Za-z_-]{35}',
        '(?i)dapi[0-9a-f]{20,}','(?i)mongodb\+srv:\/\/[^:\/\s<]+:[^@\s<]+@'
    )
    $hits = New-Object System.Collections.Generic.List[object]
    foreach ($p in $Paths | Sort-Object -Unique) {
        if (-not (Test-Path -LiteralPath $p -PathType Leaf)) { continue }
        try { $c = Get-Content -LiteralPath $p -Raw -ErrorAction Stop } catch { continue }
        foreach ($pat in $patterns) {
            $m = [regex]::Match($c, $pat)
            if ($m.Success) {
                $hits.Add([pscustomobject]@{file=$p;pattern=$pat;preview=$m.Value.Substring(0,[Math]::Min(40,$m.Value.Length))})
            }
        }
    }
    return $hits
}

# Prepare target dirs
if ($Execute) {
    foreach ($d in @(
        (Join-Path $tracksRoot '10_streaming\r1'),(Join-Path $tracksRoot '10_streaming\r2'),(Join-Path $tracksRoot '10_streaming\r3'),
        (Join-Path $tracksRoot '11_batch_processing\r1'),(Join-Path $tracksRoot '11_batch_processing\r2'),(Join-Path $tracksRoot '11_batch_processing\r3'),
        (Join-Path $tracksRoot '12_orchestration\r1'),(Join-Path $tracksRoot '12_orchestration\r2'),
        (Join-Path $tracksRoot '22_ml_platform\r1'),(Join-Path $tracksRoot '22_ml_platform\r2'),
        (Join-Path $tracksRoot '29_observability\r1'),(Join-Path $tracksRoot '29_observability\r2'),
        (Join-Path $tracksRoot '30_system_design\r2'),(Join-Path $tracksRoot '30_system_design\r3'),
        $interviewRoot,$legacyTechPrompts,(Join-Path $canonicalTechPrompts 'r1'),(Join-Path $canonicalTechPrompts 'r2'),(Join-Path $canonicalTechPrompts 'r3'),
        $mlAiTarget
    )) { Ensure-Dir $d }
}

# Source inventory
$sourceInventory = New-Object System.Collections.Generic.List[object]
$techNotebooks = @()
if (Test-Path -LiteralPath $srcTech) {
    $techNotebooks = Get-ChildItem -LiteralPath $srcTech -Recurse -File -Filter '*.ipynb' | Where-Object { $_.FullName -notmatch '\\.ipynb_checkpoints\\' }
}
$techPromptFiles = @()
if (Test-Path -LiteralPath $srcTechPrompts) {
    $techPromptFiles = Get-ChildItem -LiteralPath $srcTechPrompts -Recurse -File | Where-Object { $_.FullName -match '\\R[123]\\' }
}
$deInterviewFiles = @()
if (Test-Path -LiteralPath $srcInterview) {
    $deInterviewFiles = Get-ChildItem -LiteralPath $srcInterview -Recurse -File -Filter '*.ipynb'
}
$mlAiFiles = @()
if (Test-Path -LiteralPath $srcMlAi) {
    $mlAiFiles = Get-ChildItem -LiteralPath $srcMlAi -Recurse -File
}

foreach ($f in ($techNotebooks + $techPromptFiles + $deInterviewFiles + $mlAiFiles)) {
    $sourceInventory.Add([pscustomobject]@{path=$f.FullName;size=$f.Length;sha256=(Hash-File $f.FullName)})
}
$sourceInventory | ConvertTo-Json -Depth 4 | Set-Content -Path (Join-Path $runMeta 'pre_migration_inventory.json')

# M-011 technologies notebooks
foreach ($f in $techNotebooks) {
    $nameNoExt = [IO.Path]::GetFileNameWithoutExtension($f.Name)
    $track = Get-TechTrack $nameNoExt
    if ($track -eq 'interview') {
        $target = Join-Path $interviewRoot $f.Name
        Copy-Mapped -Group 'M-011_technologies_notebooks' -Source $f.FullName -Target $target
        continue
    }
    $round = Get-TechRound $nameNoExt
    $target = Join-Path $tracksRoot ("$track\\$round\\" + $f.Name)
    Copy-Mapped -Group 'M-011_technologies_notebooks' -Source $f.FullName -Target $target
}

# M-013 legacy prompt migration (R1/R2/R3 only)
foreach ($f in $techPromptFiles) {
    $rel = Rel-Path $srcTechPrompts $f.FullName
    $legacyTarget = Join-Path $legacyTechPrompts $rel

    if ($Execute) {
        Ensure-Dir (Split-Path -Parent $legacyTarget)
        $raw = Get-Content -LiteralPath $f.FullName -Raw
        $san = Sanitize-Text $raw
        Set-Content -Path $legacyTarget -Value $san.content
    }
    Copy-Mapped -Group 'M-013_legacy_prompts' -Source $f.FullName -Target $legacyTarget
}

# M-013 canonical prompt derivation from migrated legacy
foreach ($f in $techPromptFiles) {
    $rel = Rel-Path $srcTechPrompts $f.FullName
    $legacyTarget = Join-Path $legacyTechPrompts $rel

    $round = ''
    if ($rel -like 'R1\\*') { $round = 'r1' }
    elseif ($rel -like 'R2\\*') { $round = 'r2' }
    elseif ($rel -like 'R3\\*') { $round = 'r3' }
    else { continue }

    $leaf = [IO.Path]::GetFileName($rel)
    $canonTarget = Join-Path $canonicalTechPrompts ("$round\\" + $leaf)

    if ($Execute -and (Test-Path -LiteralPath $legacyTarget -PathType Leaf)) {
        Ensure-Dir (Split-Path -Parent $canonTarget)
        $raw = Get-Content -LiteralPath $legacyTarget -Raw
        $header = "# Canonical Derived Prompt`r`n`r`n> Source legacy: $legacyTarget`r`n`r`n"
        Set-Content -Path $canonTarget -Value ($header + $raw)
    }
    Add-Move -Group 'M-013_canonical_derived_prompts' -Source $legacyTarget -Target $canonTarget -Status 'copied'
}

# M-008 DE interview
foreach ($f in $deInterviewFiles) {
    $target = Join-Path $interviewRoot ("de_interview_" + $f.Name)
    Copy-Mapped -Group 'M-008_de_interview' -Source $f.FullName -Target $target
}

# ML_AI pack
foreach ($f in $mlAiFiles) {
    $rel = Rel-Path $srcMlAi $f.FullName
    $target = Join-Path $mlAiTarget $rel
    Copy-Mapped -Group 'ML_AI_pack' -Source $f.FullName -Target $target
}

# Post-scan and artifacts
$secretHits = @()
if ($Execute) { $secretHits = @(Scan-Secrets ($targetTouched | Sort-Object -Unique)) }
$secretHits | ConvertTo-Json -Depth 5 | Set-Content -Path (Join-Path $runMeta 'secret_scan_hits.json')
if ($Execute -and $secretHits.Count -gt 0) {
    throw "Target secret scan failed with $($secretHits.Count) hit(s). See secret_scan_hits.json"
}

$moveMap | Export-Csv -Path (Join-Path $runMeta 'move_map.csv') -NoTypeInformation -Encoding UTF8
if ($conflicts.Count -eq 0) {
    '# Conflicts Report`n`nNo conflicts.' | Set-Content -Path (Join-Path $runMeta 'conflicts_report.md')
} else {
    @('# Conflicts Report','',$conflicts) | Set-Content -Path (Join-Path $runMeta 'conflicts_report.md')
}

$postInventory = New-Object System.Collections.Generic.List[object]
foreach ($t in ($targetTouched | Sort-Object -Unique)) {
    if (Test-Path -LiteralPath $t -PathType Leaf) {
        $it = Get-Item -LiteralPath $t
        $postInventory.Add([pscustomobject]@{path=$t;size=$it.Length;sha256=(Hash-File $t)})
    }
}
$postInventory | ConvertTo-Json -Depth 4 | Set-Content -Path (Join-Path $runMeta 'post_migration_inventory.json')

# Optional ML_AI source deletion after successful migration
$mlAiDeleted = $false
if ($Execute -and $DeleteMlAiSource) {
    $backupPath = Join-Path $BackupRoot ("ml_ai_backup_" + $runTs)
    Ensure-Dir $backupPath
    if (Test-Path -LiteralPath $srcMlAi) {
        Copy-Item -LiteralPath $srcMlAi -Destination (Join-Path $backupPath 'ML_AI') -Recurse -Force
        Remove-Item -LiteralPath $srcMlAi -Recurse -Force
        $mlAiDeleted = $true
    }
}

$summary = [pscustomobject]@{
    ok = $true
    execute = [bool]$Execute
    delete_ml_ai_source = [bool]$DeleteMlAiSource
    run_id = $runId
    source_tech_notebooks = $techNotebooks.Count
    source_tech_prompts_r123 = $techPromptFiles.Count
    source_de_interview_notebooks = $deInterviewFiles.Count
    source_ml_ai_files = $mlAiFiles.Count
    move_map_entries = $moveMap.Count
    conflicts = $conflicts.Count
    secret_hits = $secretHits.Count
    ml_ai_source_deleted = $mlAiDeleted
    run_meta = $runMeta
}
$summary | ConvertTo-Json -Depth 4 | Set-Content -Path (Join-Path $runMeta 'summary.json')
$summary | ConvertTo-Json -Depth 4
