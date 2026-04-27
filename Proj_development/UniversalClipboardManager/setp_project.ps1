param (
    [string]$ProjectName = "UniversalClipboardManager",
    [string]$InstallRoot = "C:\scripts"
)

# --- Define Paths ---
$sourceDir = $PSScriptRoot
$projectDir = Join-Path -Path $InstallRoot -ChildPath $ProjectName
$venvPath = Join-Path -Path $projectDir -ChildPath ".venv"
$pythonExecutable = "python"
$venvPythonExecutable = Join-Path -Path $venvPath -ChildPath "Scripts\python.exe"
$pipExecutable = Join-Path -Path $venvPath -ChildPath "Scripts\pip.exe"
$requirementsFile = Join-Path -Path $sourceDir -ChildPath "requirements.txt"

$filesToCopy = @(
    "clipboard_app.py",
    "clipboard_data.json",
    "env_setter.ps1",
    "launch_clipboard.bat",
    "run_app.bat",
    "install_startup.ps1",
    "cleanup_legacy_install.ps1",
    "requirements.txt"
)

# --- Check for existing directory and create if not found ---
if (-not (Test-Path $projectDir)) {
    Write-Host "Creating project directory: $projectDir"
    New-Item -Path $projectDir -ItemType Directory -Force | Out-Null
}
else {
    Write-Host "Project directory already exists: $projectDir"
}

# --- Copy project runtime files into install directory ---
Write-Host "Copying project files to $projectDir..."
foreach ($file in $filesToCopy) {
    $src = Join-Path $sourceDir $file
    if (Test-Path $src) {
        Copy-Item -Path $src -Destination $projectDir -Force
    }
}
Write-Host "Project files synchronized."

# --- Create virtual environment using the specified Python version ---
if (-not (Test-Path $venvPath)) {
    Write-Host "Creating virtual environment in project directory ($venvPath)..."
    & $pythonExecutable -m venv $venvPath
    Write-Host "Virtual environment created."
}
else {
    Write-Host "Virtual environment already exists."
}

# --- Install required packages ---
Write-Host "Installing required packages..."
if (Test-Path $requirementsFile) {
    & $pipExecutable install -r $requirementsFile
}
else {
    & $pipExecutable install pyperclip pynput PyQt6
}
Write-Host "Installation completed. The project is ready!"

# --- Instructions for the user ---
Write-Host "Project setup complete!"
Write-Host "Install directory: $projectDir"
Write-Host "Run the app with: $projectDir\\launch_clipboard.bat"
Write-Host "Configure auto-start with: $projectDir\\install_startup.ps1"
