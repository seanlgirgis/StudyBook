param(
    [string]$SeedPath = "config/secrets/.local/studybook.secret.seed.dpapi.json",
    [switch]$Force
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
if (-not (Test-Path -LiteralPath $seedPathResolved)) {
    Write-Host "Seed file not found: $seedPathResolved" -ForegroundColor Yellow
    exit 0
}

if (-not $Force) {
    $confirm = Read-Host "Delete seed file at $seedPathResolved ? [y/N]"
    if ($confirm.Trim().ToLowerInvariant() -notin @('y','yes')) {
        Write-Host "Delete cancelled." -ForegroundColor Yellow
        exit 0
    }
}

Remove-Item -LiteralPath $seedPathResolved -Force
Write-Host "Removed seed file: $seedPathResolved" -ForegroundColor Green
