<#
.SYNOPSIS
POC 04f Integration Script

.DESCRIPTION
- Mirrors extracted files into local 04f folder
- Verifies folder structure
- Loads environment and installs dependencies
- Runs pytest with explicit failure if no tests found
- Optional Docker / docker-compose build & run

.PARAMETER ExtractedRoot
Path to extracted 04f files.

.PARAMETER TargetRoot
Local 04f destination path.

.PARAMETER EnvSetter
Path to env_setter.ps1

.PARAMETER BackupExisting
Optional backup of existing target folder.

.PARAMETER RunDocker
Build and run Docker container.

.PARAMETER RunCompose
Run docker-compose.

.PARAMETER All
Runs mirror, env, pip, pytest, and Docker build/run in one shot.
#>

param(
    [string]$ExtractedRoot = "D:\Workarea\StudyBook\demos\rag\pocs\04f",
    [string]$TargetRoot = "D:\Workarea\StudyBook\demos\rag\pocs\04f",
    [string]$EnvSetter = "D:\Workarea\StudyBook\env_setter.ps1",
    [switch]$BackupExisting,
    [switch]$RunDocker,
    [switch]$RunCompose,
    [switch]$All
)

$ErrorActionPreference = "Stop"

if ($All) {
    $RunDocker = $true
}

Write-Host "[1/7] Preparing target folder..."
if ($BackupExisting -and (Test-Path $TargetRoot)) {
    $parent = Split-Path $TargetRoot -Parent
    $name = Split-Path $TargetRoot -Leaf
    $stamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $backup = Join-Path $parent ("{0}_backup_{1}" -f $name, $stamp)
    Rename-Item -Path $TargetRoot -NewName (Split-Path $backup -Leaf)
    Write-Host "Backed up existing folder to: $backup"
}

if (-not (Test-Path $ExtractedRoot)) {
    throw "Extracted source path not found: $ExtractedRoot"
}

if (-not (Test-Path $TargetRoot)) {
    New-Item -ItemType Directory -Path $TargetRoot | Out-Null
}

Write-Host "[2/7] Mirroring extracted files into target..."
robocopy $ExtractedRoot $TargetRoot /E /MIR | Out-Null

Write-Host "[3/7] Verifying file tree..."
Push-Location $TargetRoot
try {
    tree /F
}
finally {
    Pop-Location
}

Write-Host "[4/7] Loading environment and installing dependencies..."
. $EnvSetter
$reqPath = Join-Path $TargetRoot "src\requirements.txt"
if (Test-Path $reqPath) {
    pip install -r $reqPath
}
else {
    Write-Warning "requirements.txt not found at $reqPath"
}

Write-Host "[5/7] Running tests..."
$pytestOutput = pytest (Join-Path $TargetRoot "tests") --tb=short 2>&1
$pytestText = $pytestOutput | Out-String
Write-Host $pytestText

if ($pytestText -match "collected 0 items") {
    throw "Pytest discovered 0 tests. Ensure test files/functions use test_* naming conventions."
}

if ($LASTEXITCODE -ne 0) {
    throw "Pytest failed with exit code $LASTEXITCODE"
}

Write-Host "[6/7] Starting local API smoke run (10 seconds)..."
$srcPath = Join-Path $TargetRoot "src"
$uvicornArgs = "app:app --host 0.0.0.0 --port 8000"
$apiProc = Start-Process -FilePath "uvicorn" -ArgumentList $uvicornArgs -WorkingDirectory $srcPath -WindowStyle Hidden -PassThru
Start-Sleep -Seconds 10
if (-not $apiProc.HasExited) {
    Stop-Process -Id $apiProc.Id -Force
}
Write-Host "Local API smoke run complete."

if ($RunDocker -and $RunCompose) {
    throw "Use only one of -RunDocker or -RunCompose."
}

if ($RunDocker) {
    Write-Host "[7/7] Building/running Docker image..."
    docker build -t poc_04f_service (Join-Path $TargetRoot "src")
    docker run --rm -p 8000:8000 poc_04f_service
}
elseif ($RunCompose) {
    Write-Host "[7/7] Starting docker-compose..."
    docker-compose -f (Join-Path $TargetRoot "docker-compose.yaml") up
}
else {
    Write-Host "[7/7] Docker steps skipped. Use -RunDocker, -RunCompose, or -All."
}

Write-Host "Done."

