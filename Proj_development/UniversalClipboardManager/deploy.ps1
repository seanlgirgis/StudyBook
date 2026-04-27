# deploy.ps1
# Deploys the Universal Clipboard Manager to C:\scripts\UniversalClipboardManager

$SourceDir = $PSScriptRoot
$TargetDir = "C:\scripts\UniversalClipboardManager"
$FilesToCopy = @(
    "clipboard_app.py",
    "clipboard_data.json",
    "settings.json",
    "env_setter.ps1",
    "launch_clipboard.bat",
    "run_app.bat",
    "install_startup.ps1",
    "cleanup_legacy_install.ps1",
    "requirements.txt"
)

Write-Host "Deploying Universal Clipboard Manager..." -ForegroundColor Cyan
Write-Host "Source: $SourceDir"
Write-Host "Destination: $TargetDir"

# 1. Create Target Directory
if (-not (Test-Path -Path $TargetDir)) {
    New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
    Write-Host "Created directory: $TargetDir" -ForegroundColor Green
}
else {
    Write-Host "Directory exists: $TargetDir" -ForegroundColor Yellow
}

# 2. Copy Application Files
foreach ($file in $FilesToCopy) {
    $sourcePath = Join-Path $SourceDir $file
    if (Test-Path $sourcePath) {
        Copy-Item -Path $sourcePath -Destination $TargetDir -Force
    }
}
Write-Host "Copied application files." -ForegroundColor Green

# 3. Handle Data File (Preserve existing data in target if present, else copy from source, else init)
$TargetDataFile = "$TargetDir\clipboard_data.json"
$SourceDataFile = "$SourceDir\clipboard_data.json"

if (Test-Path $SourceDataFile) {
    Copy-Item -Path $SourceDataFile -Destination $TargetDir -Force
    Write-Host "Copied clipboard_data.json from source." -ForegroundColor Green
}
elseif (-not (Test-Path $TargetDataFile)) {
    # Initialize empty data file if neither source nor target has it
    Set-Content -Path $TargetDataFile -Value "[]"
    Write-Host "Created new clipboard_data.json." -ForegroundColor Green
}

Write-Host "Deployment Complete!" -ForegroundColor Cyan
Write-Host "You can now run install_startup.ps1 to configure auto-start." -ForegroundColor Magenta
