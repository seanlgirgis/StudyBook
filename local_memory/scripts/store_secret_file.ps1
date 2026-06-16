[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$SourcePath,
    [Parameter(Mandatory = $true)][string]$Id,
    [string]$Purpose
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

. (Join-Path -Path $PSScriptRoot -ChildPath '_vault_common.ps1')

if (-not (Test-Path -LiteralPath $SourcePath -PathType Leaf)) {
    throw "Source file not found: $SourcePath"
}

$secretId = ConvertTo-SecretId -RawId $Id
$purposeText = if ([string]::IsNullOrWhiteSpace($Purpose)) { $secretId } else { $Purpose.Trim() }
$fileName = [System.IO.Path]::GetFileName($SourcePath)
$destDir = Join-Path -Path $script:VaultFilesRoot -ChildPath $secretId
$destPath = Join-Path -Path $destDir -ChildPath $fileName

Ensure-VaultDirectories
if (-not (Test-Path -LiteralPath $destDir)) {
    New-Item -ItemType Directory -Path $destDir -Force | Out-Null
}

Copy-Item -LiteralPath $SourcePath -Destination $destPath -Force

$storage = "secrets\files\$secretId\$fileName"
$retrieve = "Start-Process `"$destPath`""
Update-SecretRegistryRow -Id $secretId -Type 'file' -Purpose $purposeText -Storage $storage -Retrieve $retrieve

Write-Host "Stored secret file: $secretId" -ForegroundColor Green
Write-Host "Path: $destPath" -ForegroundColor Gray
Write-Host "Registry updated: $script:RegistryPath" -ForegroundColor Gray
Write-Host "Run gitqall.ps1 (with V: mounted) to mirror git-ignored files to encrypted E: backup." -ForegroundColor Gray