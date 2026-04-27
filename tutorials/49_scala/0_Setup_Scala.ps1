# Check for Administrator privileges
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Warning "Please run this script as Administrator to ensure successful installation."
    Break
}

Write-Host "Installing Scala..."
choco install scala -y

Write-Host "Installing sbt (Scala Build Tool)..."
choco install sbt -y

Write-Host "Installation complete. Please RESTART your terminal/PowerShell to refresh environment variables."
Write-Host "Verify installation with: scala -version; sbt -version"
