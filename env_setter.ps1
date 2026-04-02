param(
    [string]$Machine,
    [switch]$SkipVenvActivation,
    [switch]$NonInteractive
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Path $PSCommandPath -Parent
$coreScript = Join-Path -Path $projectRoot -ChildPath "scripts\env\env_core.ps1"
if (-not (Test-Path -LiteralPath $coreScript)) {
    throw "Missing core environment script: $coreScript"
}

. $coreScript

$result = Invoke-StudyBookEnvBootstrap `
    -ProjectRoot $projectRoot `
    -MachineName $Machine `
    -SkipVenvActivation:$SkipVenvActivation `
    -NonInteractive:$NonInteractive

Write-Host "--- StudyBook Environment ---" -ForegroundColor Yellow
Write-Host "Machine: $($result.Machine)" -ForegroundColor Green
Write-Host "Project Root: $($result.ProjectRoot)" -ForegroundColor Gray
Write-Host "Venv Path: $($result.VenvPath)" -ForegroundColor Gray
Write-Host "Python: $($result.PythonPath)" -ForegroundColor Cyan
Write-Host "Secrets Loaded: $($result.SecretsLoaded)" -ForegroundColor DarkCyan
