# install_startup.ps1
# Configures Universal Clipboard Manager to start automatically with Windows

$TargetDir = $PSScriptRoot
$AppWrapper = "$TargetDir\launch_clipboard.bat"
$ShortcutName = "UniversalClipboardManager.lnk"
$StartupFolder = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
$ShortcutPath = Join-Path $StartupFolder $ShortcutName

Write-Host "Configuring Startup..." -ForegroundColor Cyan

# 1. Verify Checks
if (-not (Test-Path $TargetDir)) {
    Write-Error "Deployment directory not found at $TargetDir. Run deploy.ps1 first."
    exit 1
}
if (-not (Test-Path $AppWrapper)) {
    Write-Error "Wrapper script not found at $AppWrapper."
    exit 1
}

# 2. Create Shortcut
try {
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
    
    $Shortcut.TargetPath = $AppWrapper
    $Shortcut.WindowStyle = 7 # Minimized (to hide the brief flash of the bat file)
    $Shortcut.WorkingDirectory = $TargetDir
    $Shortcut.Description = "Universal Clipboard Manager - Auto Start"
    
    $Shortcut.Save()
    
    Write-Host "Startup shortcut created successfully!" -ForegroundColor Green
    Write-Host "Path: $ShortcutPath"
    Write-Host "Target: $AppWrapper"
    Write-Host "Working Dir: $TargetDir"
}
catch {
    Write-Error "Failed to create shortcut: $_"
}

Write-Host "Installation Complete! The app will start automatically on next login." -ForegroundColor Cyan
