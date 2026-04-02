param(
    [ValidateSet("all", "core", "streaming", "pipeline", "observability")]
    [string]$Group = "all",
    [switch]$RemoveVolumes
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptRoot = Split-Path -Parent $PSCommandPath
$infraRoot = Split-Path -Parent $scriptRoot
$dockerDir = Join-Path $infraRoot "docker"
$envDir = Join-Path $infraRoot "env"

$envLocal = Join-Path $envDir ".env.local"
$envExample = Join-Path $envDir ".env.example"

if (Test-Path $envLocal) {
    $envFile = $envLocal
} elseif (Test-Path $envExample) {
    $envFile = $envExample
} else {
    throw "No env file found. Expected $envLocal or $envExample."
}

$composeMap = @{
    all = Join-Path $dockerDir "docker-compose.yml"
    core = Join-Path $dockerDir "core.yml"
    streaming = Join-Path $dockerDir "streaming.yml"
    pipeline = Join-Path $dockerDir "pipeline.yml"
    observability = Join-Path $dockerDir "observability.yml"
}

$composeFile = $composeMap[$Group]
if (-not (Test-Path $composeFile)) {
    throw "Compose file not found: $composeFile"
}

$args = @("compose", "-f", $composeFile, "--env-file", $envFile, "down")
if ($RemoveVolumes) {
    $args += "-v"
}

Write-Host "Stopping infra group '$Group' using $composeFile" -ForegroundColor Cyan
& docker @args
if ($LASTEXITCODE -ne 0) {
    throw "docker compose down failed for group '$Group'."
}

Write-Host "Infra group '$Group' stopped successfully." -ForegroundColor Green
