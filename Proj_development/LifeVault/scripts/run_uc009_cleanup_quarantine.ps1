param(
    [Parameter(Mandatory = $true)][string]$PodId,
    [Parameter(Mandatory = $true)][string]$QuarantineRoot,
    [string]$DbPath = "D:\AI_Lab\LifeVault\db\lifevault.sqlite",
    [switch]$DryRun,
    [switch]$ApprovedCleanup,
    [switch]$RealDbConfirm,
    [switch]$IncludeSensitive
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = (Resolve-Path (Join-Path $scriptDir "..")).Path
$srcPath = Join-Path $projectRoot "src"
if ($env:PYTHONPATH) { $env:PYTHONPATH = "$srcPath;$env:PYTHONPATH" } else { $env:PYTHONPATH = $srcPath }

$args = @("-m", "lifevault.uc009_cli", "--db-path", $DbPath, "--pod-id", $PodId, "--quarantine-root", $QuarantineRoot)
if ($DryRun) { $args += "--dry-run" }
if ($ApprovedCleanup) { $args += "--approved-cleanup" }
if ($RealDbConfirm) { $args += "--real-db-confirm" }
if ($IncludeSensitive) { $args += "--include-sensitive" }

python @args
exit $LASTEXITCODE
