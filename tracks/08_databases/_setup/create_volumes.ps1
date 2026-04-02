# create_volumes.ps1
# Creates all bind-mount volume directories on D drive
# Run from: D:\Workspace\Basics\Databases\_setup\
# Run once before first docker compose up

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$setupDir = Split-Path $MyInvocation.MyCommand.Path -Parent

Write-Host ""
Write-Host "Creating volume directories..." -ForegroundColor Cyan
Write-Host "Location: $setupDir\volumes\" -ForegroundColor Cyan
Write-Host ""

$dirs = @(
    "volumes\postgres",
    "volumes\postgres_init",
    "volumes\redis",
    "volumes\cassandra\data",
    "volumes\cassandra\commitlog",
    "volumes\neo4j\data",
    "volumes\neo4j\logs",
    "volumes\neo4j\import",
    "volumes\neo4j\plugins",
    "volumes\influxdb\data",
    "volumes\influxdb\config",
    "volumes\elasticsearch\data",
    "volumes\kibana"
)

foreach ($d in $dirs) {
    $full = Join-Path $setupDir $d
    if (-not (Test-Path $full)) {
        New-Item -ItemType Directory -Force -Path $full | Out-Null
        Write-Host "  [+] $d" -ForegroundColor Green
    } else {
        Write-Host "  [=] $d (exists)" -ForegroundColor DarkGray
    }
}

Write-Host ""
Write-Host "Done. Now run:" -ForegroundColor White
Write-Host "  docker compose up -d" -ForegroundColor Yellow
Write-Host ""
