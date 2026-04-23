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

$scriptsDir = Join-Path -Path $projectRoot -ChildPath "scripts"
[Environment]::SetEnvironmentVariable("STUDYBOOK_SCRIPTS_DIR", $scriptsDir, "Process")
$pathValue = [Environment]::GetEnvironmentVariable("Path", "Process")
$pathEntries = @($pathValue -split ";" | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
$alreadyPresent = $false
foreach ($entry in $pathEntries) {
    if ($entry.TrimEnd("\") -ieq $scriptsDir.TrimEnd("\")) {
        $alreadyPresent = $true
        break
    }
}
if (-not $alreadyPresent) {
    $newPath = if ([string]::IsNullOrWhiteSpace($pathValue)) { $scriptsDir } else { "$scriptsDir;$pathValue" }
    [Environment]::SetEnvironmentVariable("Path", $newPath, "Process")
}

Write-Host "--- StudyBook Environment ---" -ForegroundColor Yellow
Write-Host "Machine: $($result.Machine)" -ForegroundColor Green
Write-Host "Project Root: $($result.ProjectRoot)" -ForegroundColor Gray
Write-Host "Venv Path: $($result.VenvPath)" -ForegroundColor Gray
Write-Host "Python: $($result.PythonPath)" -ForegroundColor Cyan
Write-Host "Secrets Loaded: $($result.SecretsLoaded)" -ForegroundColor DarkCyan
Write-Host "Scripts On PATH: $scriptsDir" -ForegroundColor DarkGray
