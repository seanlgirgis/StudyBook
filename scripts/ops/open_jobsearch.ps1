param(
    [string]$Machine,
    [switch]$NoActivate,
    [switch]$NoCd
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Path $PSCommandPath -Parent
$projectRoot = (Resolve-Path (Join-Path -Path $scriptDir -ChildPath '..\..')).Path
$coreScript = Join-Path -Path $projectRoot -ChildPath 'scripts\env\env_core.ps1'
if (-not (Test-Path -LiteralPath $coreScript)) {
    throw "Missing core environment script: $coreScript"
}
. $coreScript

# Load machine config and env vars, but do NOT activate StudyBook venv.
$null = Invoke-StudyBookEnvBootstrap -ProjectRoot $projectRoot -MachineName $Machine -SkipVenvActivation -NonInteractive

$jobsearchRootRaw = $env:STUDYBOOK_JOBSEARCH_ROOT
if ([string]::IsNullOrWhiteSpace($jobsearchRootRaw)) {
    $jobsearchRootRaw = 'C:\jobsearch'
}
$jobsearchRoot = [System.IO.Path]::GetFullPath($jobsearchRootRaw)

if (-not (Test-Path -LiteralPath $jobsearchRoot)) {
    throw "JobSearch root not found: $jobsearchRoot`nSet STUDYBOOK_JOBSEARCH_ROOT in config/machines/<machine>.psd1 or <machine>.local.psd1"
}

$jobsearchEnv = Join-Path -Path $jobsearchRoot -ChildPath 'env_setter.ps1'
if (-not (Test-Path -LiteralPath $jobsearchEnv)) {
    throw "JobSearch env_setter not found: $jobsearchEnv"
}

if (-not $NoCd) {
    Set-Location -LiteralPath $jobsearchRoot
}

if (-not $NoActivate) {
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
    . $jobsearchEnv
}

Write-Host '--- JobSearch Launch ---' -ForegroundColor Yellow
Write-Host "JobSearch Root: $jobsearchRoot" -ForegroundColor Gray
Write-Host "Activated: $([bool](-not $NoActivate))" -ForegroundColor Gray
Write-Host "Current Dir: $(Get-Location)" -ForegroundColor Gray

[PSCustomObject]@{
    JobSearchRoot = $jobsearchRoot
    Activated = [bool](-not $NoActivate)
    CurrentDirectory = (Get-Location).Path
}
