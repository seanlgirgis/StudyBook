param(
  [string]$DbPath = "D:\AI_Lab\LifeVault\db\lifevault.sqlite",
  [string]$Query,
  [string]$PodId,
  [string]$Sensitivity,
  [string]$ReviewDecision,
  [switch]$DuplicatesOnly,
  [switch]$ListPods,
  [int]$Limit = 50
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

$args = @("-m", "lifevault.uc005_cli", "--db-path", $DbPath, "--limit", "$Limit")
if ($Query) { $args += @("--query", $Query) }
if ($PodId) { $args += @("--pod-id", $PodId) }
if ($Sensitivity) { $args += @("--sensitivity", $Sensitivity) }
if ($ReviewDecision) { $args += @("--review-decision", $ReviewDecision) }
if ($DuplicatesOnly) { $args += "--duplicates-only" }
if ($ListPods) { $args += "--list-pods" }

python @args