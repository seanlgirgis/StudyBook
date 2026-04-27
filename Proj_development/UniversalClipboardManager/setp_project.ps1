param (
    [string]$ProjectName = "UniversalClipboardManager"
)

# --- Define Paths ---
$pythonBaseDir = "C:\pyver\py312"
$baseDir = $PSScriptRoot
$projectDir = $PSScriptRoot
$venvPath = "C:\py_venv\commonEnv"
$pythonExecutable = Join-Path -Path $pythonBaseDir -ChildPath "python.exe"
$venvPythonExecutable = Join-Path -Path $venvPath -ChildPath "Scripts\python.exe"
$pipExecutable = Join-Path -Path $venvPath -ChildPath "Scripts\pip.exe"

# --- Check for existing directory and create if not found ---
if (-not (Test-Path $projectDir)) {
    Write-Host "Creating project directory: $projectDir"
    New-Item -Path $projectDir -ItemType Directory | Out-Null
}
else {
    Write-Host "Project directory already exists: $projectDir"
}

# --- Create virtual environment using the specified Python version ---
if (-not (Test-Path $venvPath)) {
    Write-Host "Creating virtual environment using Python at $pythonBaseDir..."
    & $pythonExecutable -m venv $venvPath
    Write-Host "Virtual environment created."
}
else {
    Write-Host "Virtual environment already exists."
}

# --- Install required packages ---
Write-Host "Installing required packages..."
& $pipExecutable install pyperclip pynput PyQt6
Write-Host "Installation completed. The project is ready!"

# --- Instructions for the user ---
Write-Host "Project setup complete!"
Write-Host "1. Copy your clipboard_app.py and clipboard_data.json files to $projectDir"
Write-Host "2. Create a batch file to run the app at startup. Example: start_app.bat"
Write-Host "   @echo off"
Write-Host "   start /b $venvPythonExecutable $projectDir\clipboard_app.py"
Write-Host "3. Place the batch file in the Windows Startup folder."