param(
  [Parameter(Mandatory = $true)]
  [string]$SourcePath,
  [string]$Story,
  [string]$OutputRoot,
  [int]$MaxPreviewFiles = 200
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

$args = @("-m", "lifevault.uc001_cli", "--source-path", $SourcePath, "--max-preview-files", "$MaxPreviewFiles")
if ($Story) { $args += @("--story", $Story) }
if ($OutputRoot) { $args += @("--output-root", $OutputRoot) }

python @args
