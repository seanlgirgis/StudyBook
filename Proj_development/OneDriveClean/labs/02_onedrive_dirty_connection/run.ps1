$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $scriptDir "..\..\scripts\_lab_common.ps1")
$ctx = Get-LabContext -ScriptDir $scriptDir -LabName "02_onedrive_dirty_connection"
$remote = [string]$ctx.Remotes.dirty_remote
$excludeArgs = Get-RcloneExcludeArgs -RemotesConfig $ctx.Remotes
rclone about "${remote}:" @excludeArgs | Set-Content -Encoding UTF8 (Join-Path $ctx.RunDir "dirty_about.txt")
rclone lsd "${remote}:" @excludeArgs | Set-Content -Encoding UTF8 (Join-Path $ctx.RunDir "dirty_lsd.txt")
