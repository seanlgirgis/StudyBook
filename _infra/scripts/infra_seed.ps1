param(
    [ValidateSet("all", "core", "tech")]
    [string]$Target = "all",
    [string]$Python = "python"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptRoot = Split-Path -Parent $PSCommandPath
$infraRoot = Split-Path -Parent $scriptRoot
$seedsDir = Join-Path $infraRoot "seeds"

$seedMap = @{
    core = @(Join-Path $seedsDir "seed_core.py")
    tech = @(Join-Path $seedsDir "seed_tech_telemetry.py")
    all  = @(
        (Join-Path $seedsDir "seed_core.py"),
        (Join-Path $seedsDir "seed_tech_telemetry.py")
    )
}

$targets = $seedMap[$Target]
foreach ($seedScript in $targets) {
    if (-not (Test-Path $seedScript)) {
        throw "Seed script missing: $seedScript"
    }

    Write-Host "Running seed script: $seedScript" -ForegroundColor Cyan
    & $Python $seedScript
    if ($LASTEXITCODE -ne 0) {
        throw "Seed script failed: $seedScript"
    }
}

Write-Host "Seed target '$Target' completed successfully." -ForegroundColor Green
