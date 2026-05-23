param([switch]$NoPrompt)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $scriptDir "..\..\scripts\_lab_common.ps1")
$ctx = Get-LabContext -ScriptDir $scriptDir -LabName "05_copy_one_tiny_folder"
$src = "{0}:{1}" -f [string]$ctx.Remotes.dirty_remote, [string]$ctx.Remotes.safe_test_remote_path
$dest = Join-Path $ctx.RunDir "copied_data"
New-Item -ItemType Directory -Force -Path $dest | Out-Null
Write-Host "Source: $src"
Write-Host "Destination: $dest"
if (-not $NoPrompt) { if ((Read-Host "Proceed with copy? (yes/no)") -ne "yes") { throw "Aborted" } }
rclone copy $src $dest --progress --log-file (Join-Path $ctx.RunDir "copy.log")
