param(
  [Parameter(Mandatory=$true)][string]$SiteKey,
  [string]$Machine = "asuspc",
  [switch]$ShowInfo
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$cmd = @("-SiteKey", $SiteKey, "-Machine", $Machine)
if ($ShowInfo) { $cmd += "-ShowInfo" }

& .\scripts\env\copy_site_password.ps1 @cmd
