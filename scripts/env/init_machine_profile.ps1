param(
    [string]$MachineName
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$projectRoot = [System.IO.Path]::GetFullPath((Join-Path -Path $PSScriptRoot -ChildPath "..\.."))
$coreScript = Join-Path -Path $projectRoot -ChildPath "scripts\env\env_core.ps1"
. $coreScript

if ([string]::IsNullOrWhiteSpace($MachineName)) {
    $MachineName = $env:COMPUTERNAME
}
$normalized = ConvertTo-NormalizedMachineName -Name $MachineName

$targetPath = Join-Path -Path $projectRoot -ChildPath "config\machines\$normalized.psd1"
if (Test-Path -LiteralPath $targetPath) {
    Write-Host "Machine profile already exists: $targetPath" -ForegroundColor Yellow
    exit 0
}

$templatePath = Join-Path -Path $projectRoot -ChildPath "config\machines\_template.psd1"
if (-not (Test-Path -LiteralPath $templatePath)) {
    throw "Template file not found: $templatePath"
}

$template = Get-Content -LiteralPath $templatePath -Raw -Encoding UTF8
$content = $template.Replace("replace-me", $MachineName)
Set-Content -LiteralPath $targetPath -Value $content -Encoding UTF8

Write-Host "Created machine profile: $targetPath" -ForegroundColor Green
