# env_setter.ps1
$projectRoot = $PSScriptRoot
$venvPath = Join-Path $projectRoot ".venv"
$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"

if (Test-Path $activateScript) {
    & $activateScript
    Write-Host "Virtual environment activated: $venvPath" -ForegroundColor Green
    Write-Host "Python executable: $(Get-Command python).Path" -ForegroundColor Cyan
}
else {
    Write-Host "Activation script not found! Check the path:" $activateScript -ForegroundColor Red
}

$kbInboxPath = Join-Path $projectRoot "KB\00_Inbox"
if (-not (Test-Path $kbInboxPath)) {
    New-Item -Path $kbInboxPath -ItemType Directory -Force | Out-Null
    Write-Host "Created KB Inbox Path: $kbInboxPath" -ForegroundColor Yellow
}

$env:KB_INBOX_PATH = $kbInboxPath
$global:kbInboxPath = $kbInboxPath
Write-Host "KB Inbox Path set: $env:KB_INBOX_PATH" -ForegroundColor Green
