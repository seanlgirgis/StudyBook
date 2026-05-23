$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $scriptDir "..\..\scripts\_lab_common.ps1")
$ctx = Get-LabContext -ScriptDir $scriptDir -LabName "03_onedrive_clean_connection"
$remote = [string]$ctx.Remotes.clean_remote
$excludeArgs = Get-RcloneExcludeArgs -RemotesConfig $ctx.Remotes
rclone about "${remote}:" @excludeArgs | Set-Content -Encoding UTF8 (Join-Path $ctx.RunDir "clean_about.txt")
rclone lsd "${remote}:" @excludeArgs | Set-Content -Encoding UTF8 (Join-Path $ctx.RunDir "clean_lsd.txt")
