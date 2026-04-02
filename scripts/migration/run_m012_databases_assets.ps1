[CmdletBinding()]
param(
    [switch]$Execute,
    [switch]$WhatIfOnly,
    [string]$StudyBookRoot = 'D:\StudyBook',
    [string]$WorkspaceRoot = 'D:\Workspace'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if ($WhatIfOnly) { $Execute = $false }

$runTs = Get-Date -Format 'yyyyMMdd_HHmmss'
$sourceDbRoot = Join-Path $WorkspaceRoot 'Basics\Databases'
$sourcePromptsRoot = Join-Path $sourceDbRoot 'prompts'
$targetTrackRoot = Join-Path $StudyBookRoot 'tracks\08_databases'
$targetLegacyPrompts = Join-Path $StudyBookRoot '_prompts\legacy\databases'
$metaRoot = Join-Path $targetTrackRoot '_migration_meta'
$runMeta = Join-Path $metaRoot ("run_" + $runTs)

$null = New-Item -ItemType Directory -Path $runMeta -Force

$moveMap = New-Object System.Collections.Generic.List[object]
$targetTouched = New-Object System.Collections.Generic.List[string]

function Hash-File {
    param([string]$Path)
    (Get-FileHash -Algorithm SHA256 -LiteralPath $Path).Hash
}

function RelPath {
    param([string]$Base,[string]$Full)
    $uBase = New-Object System.Uri((Resolve-Path -LiteralPath $Base).Path + [IO.Path]::DirectorySeparatorChar)
    $uFull = New-Object System.Uri((Resolve-Path -LiteralPath $Full).Path)
    [System.Uri]::UnescapeDataString($uBase.MakeRelativeUri($uFull).ToString()).Replace('/','\\')
}

function EnsureParent {
    param([string]$Path)
    $p = Split-Path -Parent $Path
    if ($p) { $null = New-Item -ItemType Directory -Path $p -Force }
}

function AddMove {
    param([string]$Group,[string]$Source,[string]$Target,[string]$Status,[string]$Note='')
    $moveMap.Add([pscustomobject]@{Group=$Group;Source=$Source;Target=$Target;Status=$Status;Note=$Note})
    if ($Status -eq 'copied') { $targetTouched.Add($Target) }
}

function Sanitize-TextContent {
    param([string]$Content)

    $changed = $false
    $sanitized = $Content

    $old = $sanitized
    $sanitized = [regex]::Replace($sanitized, '(?i)(mongodb\+srv:\/\/)([^:\s\/]+):([^@\s\/]+)@', '$1<user>:<password>@')
    if ($sanitized -ne $old) { $changed = $true }

    $patterns = @(
        '(?i)AKIA[0-9A-Z]{16}',
        '(?i)ASIA[0-9A-Z]{16}',
        '(?i)-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----',
        '(?i)xox[baprs]-[0-9A-Za-z-]{10,}',
        '(?i)ghp_[0-9A-Za-z]{20,}',
        '(?i)AIza[0-9A-Za-z_-]{35}',
        '(?i)dapi[0-9a-f]{20,}'
    )

    foreach ($p in $patterns) {
        $old = $sanitized
        $sanitized = [regex]::Replace($sanitized, $p, '<redacted_secret>')
        if ($sanitized -ne $old) { $changed = $true }
    }

    return [pscustomobject]@{ content = $sanitized; changed = $changed }
}

function Scan-FilesForSecrets {
    param([string[]]$Paths)

    $patterns = @(
        '(?i)AKIA[0-9A-Z]{16}',
        '(?i)ASIA[0-9A-Z]{16}',
        '(?i)-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----',
        '(?i)xox[baprs]-[0-9A-Za-z-]{10,}',
        '(?i)ghp_[0-9A-Za-z]{20,}',
        '(?i)AIza[0-9A-Za-z_-]{35}',
        '(?i)dapi[0-9a-f]{20,}',
        '(?i)mongodb\+srv:\/\/[^:\/\s<]+:[^@\s<]+@'
    )

    $hits = New-Object System.Collections.Generic.List[object]
    foreach ($path in $Paths) {
        if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { continue }
        try { $content = Get-Content -LiteralPath $path -Raw -ErrorAction Stop } catch { continue }
        foreach ($pat in $patterns) {
            $m = [regex]::Match($content, $pat)
            if ($m.Success) {
                $hits.Add([pscustomobject]@{file=$path;pattern=$pat;preview=$m.Value.Substring(0,[Math]::Min(40,$m.Value.Length))})
            }
        }
    }

    return $hits
}

if (-not (Test-Path -LiteralPath $sourceDbRoot)) {
    throw "Source not found: $sourceDbRoot"
}

if ($Execute) {
    $dirs = @(
        $targetTrackRoot,
        (Join-Path $targetTrackRoot 'r1'),
        (Join-Path $targetTrackRoot 'r2\sql_telemetry_mastery\exercises'),
        $targetLegacyPrompts
    )
    foreach ($d in $dirs) { $null = New-Item -ItemType Directory -Path $d -Force }
}

# Inventory source files in scope
$sourceFiles = New-Object System.Collections.Generic.List[object]

$ipynbFiles = Get-ChildItem -LiteralPath $sourceDbRoot -Recurse -File -Filter '*.ipynb' |
    Where-Object { $_.FullName -notmatch '\\.ipynb_checkpoints\\' }
foreach ($f in $ipynbFiles) {
    $sourceFiles.Add([pscustomobject]@{path=$f.FullName;size=$f.Length;sha256=(Hash-File $f.FullName);type='ipynb'})
}

$promptFiles = @()
if (Test-Path -LiteralPath $sourcePromptsRoot) {
    $promptFiles = Get-ChildItem -LiteralPath $sourcePromptsRoot -Recurse -File
    foreach ($f in $promptFiles) {
        $sourceFiles.Add([pscustomobject]@{path=$f.FullName;size=$f.Length;sha256=(Hash-File $f.FullName);type='prompt'})
    }
}

$sourceFiles | ConvertTo-Json -Depth 4 | Set-Content -Path (Join-Path $runMeta 'pre_migration_inventory.json')

# Copy notebooks
foreach ($f in $ipynbFiles) {
    $rel = RelPath -Base $sourceDbRoot -Full $f.FullName
    $target = ''
    if ($rel -like 'SQL\\TelemetryMastery\\exercises\\*') {
        $tail = $rel.Substring('SQL\\TelemetryMastery\\exercises\\'.Length)
        $target = Join-Path $targetTrackRoot ("r2\\sql_telemetry_mastery\\exercises\\" + $tail)
    } else {
        $target = Join-Path $targetTrackRoot ("r1\\" + $f.Name)
    }

    if ($Execute) {
        EnsureParent -Path $target
        Copy-Item -LiteralPath $f.FullName -Destination $target -Force
    }
    AddMove -Group 'ipynb' -Source $f.FullName -Target $target -Status 'copied'
}

# Copy prompts preserving tree and sanitize sensitive literals
foreach ($f in $promptFiles) {
    $rel = RelPath -Base $sourcePromptsRoot -Full $f.FullName
    $target = Join-Path $targetLegacyPrompts $rel
    $note = ''

    if ($Execute) {
        EnsureParent -Path $target
        $content = Get-Content -LiteralPath $f.FullName -Raw
        $sanitize = Sanitize-TextContent -Content $content
        if ($sanitize.changed) { $note = 'sanitized_secret_literal' }
        Set-Content -Path $target -Value $sanitize.content
    }
    AddMove -Group 'prompt' -Source $f.FullName -Target $target -Status 'copied' -Note $note
}

$moveMap | Export-Csv -Path (Join-Path $runMeta 'move_map.csv') -NoTypeInformation -Encoding UTF8

# Post inventory and security scan on touched targets
$post = New-Object System.Collections.Generic.List[object]
foreach ($t in ($targetTouched | Sort-Object -Unique)) {
    if (Test-Path -LiteralPath $t -PathType Leaf) {
        $i = Get-Item -LiteralPath $t
        $post.Add([pscustomobject]@{path=$t;size=$i.Length;sha256=(Hash-File $t)})
    }
}
$post | ConvertTo-Json -Depth 4 | Set-Content -Path (Join-Path $runMeta 'post_migration_inventory.json')

$secretHits = @()
if ($Execute) {
    $secretHits = @(Scan-FilesForSecrets -Paths ($targetTouched | Sort-Object -Unique))
}
$secretHits | ConvertTo-Json -Depth 5 | Set-Content -Path (Join-Path $runMeta 'secret_scan_hits.json')

if ($Execute -and $secretHits.Count -gt 0) {
    throw "Target secret scan gate failed with $($secretHits.Count) high-confidence hit(s). See secret_scan_hits.json"
}

$summary = [pscustomobject]@{
    ok = $true
    execute = [bool]$Execute
    source_ipynb_count = $ipynbFiles.Count
    source_prompt_count = $promptFiles.Count
    move_map_entries = $moveMap.Count
    secret_hits = $secretHits.Count
    run_meta = $runMeta
    target_tracks = $targetTrackRoot
    target_legacy_prompts = $targetLegacyPrompts
}

$summary | ConvertTo-Json -Depth 4 | Set-Content -Path (Join-Path $runMeta 'summary.json')
$summary | ConvertTo-Json -Depth 4
