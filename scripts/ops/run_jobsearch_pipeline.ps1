param(
    [string]$IntakeFile,
    [string]$Uuid,
    [string]$Method = 'LinkedIn',
    [string]$Version = 'v1',
    [string]$Model = 'grok-3',
    [switch]$NoMove,
    [string]$Machine
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($IntakeFile) -and [string]::IsNullOrWhiteSpace($Uuid)) {
    throw 'Provide either -IntakeFile or -Uuid.'
}

$scriptRoot = Split-Path -Path $PSCommandPath -Parent
$openScript = Join-Path -Path $scriptRoot -ChildPath 'open_jobsearch.ps1'
if (-not (Test-Path -LiteralPath $openScript)) {
    throw "Missing launcher: $openScript"
}

# Dot-source to keep env activation + cwd in this process.
. $openScript -Machine $Machine

$python = (Get-Command python -ErrorAction SilentlyContinue)
if (-not $python) {
    throw 'Python is not available after JobSearch environment activation.'
}

$cmd = @('scripts/10_auto_pipeline.py')
if (-not [string]::IsNullOrWhiteSpace($IntakeFile)) {
    $cmd += $IntakeFile
}
if (-not [string]::IsNullOrWhiteSpace($Uuid)) {
    $cmd += @('--uuid', $Uuid)
}
$cmd += @('--method', $Method, '--version', $Version, '--model', $Model)
if ($NoMove) {
    $cmd += '--no-move'
}

Write-Host "Running: python $($cmd -join ' ')" -ForegroundColor Cyan
& python @cmd
$exitCode = $LASTEXITCODE
if ($exitCode -ne 0) {
    throw "JobSearch pipeline failed with exit code $exitCode"
}

Write-Host 'JobSearch pipeline completed successfully.' -ForegroundColor Green
