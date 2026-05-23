$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $scriptDir "..\..\scripts\_lab_common.ps1")
$ctx = Get-LabContext -ScriptDir $scriptDir -LabName "04_two_onedrives_inventory"
$d = [string]$ctx.Remotes.dirty_remote
$c = [string]$ctx.Remotes.clean_remote
$excludeArgs = Get-RcloneExcludeArgs -RemotesConfig $ctx.Remotes
rclone about "${d}:" @excludeArgs | Set-Content -Encoding UTF8 (Join-Path $ctx.RunDir "dirty_about.txt")
rclone about "${c}:" @excludeArgs | Set-Content -Encoding UTF8 (Join-Path $ctx.RunDir "clean_about.txt")
rclone lsd "${d}:" @excludeArgs | Set-Content -Encoding UTF8 (Join-Path $ctx.RunDir "dirty_top_folders.txt")
rclone lsd "${c}:" @excludeArgs | Set-Content -Encoding UTF8 (Join-Path $ctx.RunDir "clean_top_folders.txt")
