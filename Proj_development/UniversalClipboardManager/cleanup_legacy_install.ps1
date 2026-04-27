# cleanup_legacy_install.ps1
# Detects and removes older/conflicting installations of Universal Clipboard Manager

Write-Host "Checking for legacy installations..." -ForegroundColor Cyan
$projectRootPattern = [regex]::Escape($PSScriptRoot)

# 1. Identify Running Processes
$processes = Get-WmiObject Win32_Process | Where-Object { $_.CommandLine -match "clipboard_app.py" }

if ($processes) {
    foreach ($proc in $processes) {
        $cmd = $proc.CommandLine
        $pid_ = $proc.ProcessId
        
        # Check if this is the "official" one (running from this project) or a rogue one
        if ($cmd -match $projectRootPattern) {
            Write-Host "Found likely CURRENT process (PID: $pid_): $cmd" -ForegroundColor Green
            # We can choose to leave it or kill it. Let's kill it to ensure restart.
            Stop-Process -Id $pid_ -Force
            Write-Host "Stopped current process to ensure clean restart." -ForegroundColor Yellow
        } else {
            Write-Host "Found SUSPICIOUS legacy process (PID: $pid_): $cmd" -ForegroundColor Red
            Stop-Process -Id $pid_ -Force
            Write-Host "Terminated legacy process." -ForegroundColor Red
        }
    }
} else {
    Write-Host "No running instances found." -ForegroundColor Gray
}

# 2. Check Startup Folder for anomalies
$StartupFolder = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
$shortcuts = Get-ChildItem -Path $StartupFolder -Filter "*.lnk"

foreach ($lnkFile in $shortcuts) {
    $shell = New-Object -ComObject WScript.Shell
    $shortcut = $shell.CreateShortcut($lnkFile.FullName)
    
    # Check if target involves clipboard_app.py
    if ($shortcut.Arguments -match "clipboard_app.py" -or $shortcut.TargetPath -match "clipboard_app.py") {
        if ($lnkFile.Name -eq "UniversalClipboardManager.lnk") {
            Write-Host "Found valid official shortcut: $($lnkFile.Name)" -ForegroundColor Green
        } else {
            Write-Host "Found LEGACY/DUPLICATE shortcut: $($lnkFile.Name) -> $($shortcut.TargetPath)" -ForegroundColor Red
            Remove-Item $lnkFile.FullName -Force
            Write-Host "Removed legacy shortcut." -ForegroundColor Red
        }
    }
}

Write-Host "Cleanup check complete." -ForegroundColor Cyan
Write-Host "You can run '.\install_startup.ps1' again if you need to restore the official startup item." -ForegroundColor Magenta
