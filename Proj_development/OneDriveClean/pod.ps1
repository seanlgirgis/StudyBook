param(
  [Parameter(Mandatory=$true, Position=0)]
  [string]$SourcePath
)

$ErrorActionPreference = "Stop"
& (Join-Path $PSScriptRoot "scripts\start_pod_intake.ps1") -SourcePath $SourcePath
