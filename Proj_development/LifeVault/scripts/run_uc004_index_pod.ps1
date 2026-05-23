param(
  [Parameter(Mandatory = $true)]
  [string]$PodPath,
  [Parameter(Mandatory = $true)]
  [string]$DbPath,
  [switch]$DryRun,
  [switch]$Approved,
  [switch]$RealDbConfirm
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Resolve-Path (Join-Path $scriptDir "..")
$srcPath = Join-Path $projectRoot "src"

if ($env:PYTHONPATH) {
  $env:PYTHONPATH = "$srcPath;$($env:PYTHONPATH)"
} else {
  $env:PYTHONPATH = $srcPath
}

$args = @("-m", "lifevault.uc004_cli", "--pod-path", $PodPath, "--db-path", $DbPath)
if ($DryRun) { $args += "--dry-run" }
if ($Approved) { $args += "--approved" }
if ($RealDbConfirm) { $args += "--real-db-confirm" }

python @args
