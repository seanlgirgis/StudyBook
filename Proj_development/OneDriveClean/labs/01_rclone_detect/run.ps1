$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $scriptDir "..\..\scripts\_lab_common.ps1")
$ctx = Get-LabContext -ScriptDir $scriptDir -LabName "01_rclone_detect"
if (-not (Get-Command rclone -ErrorAction SilentlyContinue)) { throw "rclone not found on PATH" }
rclone version | Set-Content -Encoding UTF8 (Join-Path $ctx.RunDir "rclone_version.txt")
Write-Host "rclone detect complete: $($ctx.RunDir)"
