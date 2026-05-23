param(
  [Parameter(Mandatory = $true)]
  [string]$ProposalPath,
  [switch]$Approved,
  [string]$OutputRoot,
  [string]$ApprovedPodName
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

$args = @("-m", "lifevault.uc003_cli", "--proposal-path", $ProposalPath)
if ($Approved) { $args += "--approved" }
if ($OutputRoot) { $args += @("--output-root", $OutputRoot) }
if ($ApprovedPodName) { $args += @("--approved-pod-name", $ApprovedPodName) }

python @args