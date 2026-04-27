# env_setter.ps1
$venvPath = "c:\py_venv\commonEnv"
$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"

if (Test-Path $activateScript) {
    & $activateScript
    Write-Host "Virtual environment activated: $venvPath" -ForegroundColor Green
    Write-Host "Python executable: $(Get-Command python).Path" -ForegroundColor Cyan
}
else {
    Write-Host "Activation script not found! Check the path:" $activateScript -ForegroundColor Red
}

$kbInboxPath = "C:\pyproj\KB\00_Inbox"
if (Test-Path $kbInboxPath) {
    $env:KB_INBOX_PATH = $kbInboxPath
    $global:kbInboxPath = $kbInboxPath
    Write-Host "KB Inbox Path set: $env:KB_INBOX_PATH" -ForegroundColor Green
}
else {
    Write-Host "KB Inbox Path not found: $kbInboxPath" -ForegroundColor Yellow
}
