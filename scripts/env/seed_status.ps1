param(
    [string]$SeedPath = "config/secrets/.local/studybook.secret.seed.dpapi.json",
    [switch]$AsJson
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$projectRoot = [System.IO.Path]::GetFullPath((Join-Path -Path $PSScriptRoot -ChildPath "..\.."))
$coreScript = Join-Path -Path $projectRoot -ChildPath "scripts\env\env_core.ps1"
if (-not (Test-Path -LiteralPath $coreScript)) {
    throw "Missing env core script: $coreScript"
}
. $coreScript

$seedPathResolved = Resolve-StudyBookPath -ProjectRoot $projectRoot -PathValue $SeedPath
$seedExists = Test-Path -LiteralPath $seedPathResolved
$envPassphrasePresent = -not [string]::IsNullOrWhiteSpace($env:STUDYBOOK_SECRET_PASSPHRASE)

$seedDecryptable = $false
$seedMetadata = $null
$seedError = $null

if ($seedExists) {
    try {
        $raw = Get-Content -LiteralPath $seedPathResolved -Raw -Encoding UTF8
        if (-not [string]::IsNullOrWhiteSpace($raw)) {
            $seedMetadata = $raw | ConvertFrom-Json -AsHashtable
        }
    }
    catch {
        $seedError = "Seed metadata parse failed: $($_.Exception.Message)"
    }

    try {
        $seedSecure = Unprotect-StudyBookSecretSeed -SeedPath $seedPathResolved
        if ($seedSecure) {
            $seedDecryptable = $true
        }
        elseif (-not $seedError) {
            $seedError = "Seed file found but decrypt returned null."
        }
    }
    catch {
        $seedError = "Seed decrypt failed: $($_.Exception.Message)"
    }
}

$effectiveSource = if ($envPassphrasePresent) {
    "env_var"
}
elseif ($seedDecryptable) {
    "seed_file"
}
else {
    "prompt_or_missing"
}

$canRunNonInteractive = $envPassphrasePresent -or $seedDecryptable

$fileInfo = $null
if ($seedExists) {
    $item = Get-Item -LiteralPath $seedPathResolved
    $fileInfo = [ordered]@{
        length_bytes = [int64]$item.Length
        last_write_utc = $item.LastWriteTimeUtc.ToString("o")
    }
}

$result = [ordered]@{
    ok = $canRunNonInteractive
    project_root = $projectRoot
    seed_path = $seedPathResolved
    seed_exists = $seedExists
    seed_decryptable = $seedDecryptable
    env_passphrase_present = $envPassphrasePresent
    effective_source = $effectiveSource
    can_run_noninteractive = $canRunNonInteractive
    seed_metadata = if ($seedMetadata) {
        [ordered]@{
            version = $seedMetadata.version
            algorithm = $seedMetadata.algorithm
            created_utc = $seedMetadata.created_utc
        }
    }
    else {
        $null
    }
    file_info = $fileInfo
    error = $seedError
}

if ($AsJson) {
    $result | ConvertTo-Json -Depth 6
}
else {
    Write-Host "--- StudyBook Seed Status ---" -ForegroundColor Yellow
    Write-Host "Seed Path: $($result.seed_path)" -ForegroundColor Gray
    Write-Host "Seed Exists: $($result.seed_exists)" -ForegroundColor Gray
    Write-Host "Seed Decryptable: $($result.seed_decryptable)" -ForegroundColor Gray
    Write-Host "Env Passphrase Present: $($result.env_passphrase_present)" -ForegroundColor Gray
    Write-Host "Effective Source: $($result.effective_source)" -ForegroundColor Cyan
    Write-Host "Can Run NonInteractive: $($result.can_run_noninteractive)" -ForegroundColor Green
    if ($result.seed_metadata) {
        Write-Host "Seed Algorithm: $($result.seed_metadata.algorithm)" -ForegroundColor Gray
        Write-Host "Seed Created UTC: $($result.seed_metadata.created_utc)" -ForegroundColor Gray
    }
    if ($result.error) {
        Write-Warning $result.error
    }
}
