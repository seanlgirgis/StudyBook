param(
    [Parameter(Mandatory = $true)][string]$PodId,
    [Parameter(Mandatory = $true)][string]$VaultRoot,
    [string]$DbPath = "D:\AI_Lab\LifeVault\db\lifevault.sqlite",
    [switch]$DryRun,
    [switch]$ApprovedVerify,
    [switch]$RealDbConfirm
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = (Resolve-Path (Join-Path $scriptDir "..")).Path
$srcPath = Join-Path $projectRoot "src"
if ($env:PYTHONPATH) { $env:PYTHONPATH = "$srcPath;$env:PYTHONPATH" } else { $env:PYTHONPATH = $srcPath }

$args = @("-m", "lifevault.uc008_cli", "--db-path", $DbPath, "--pod-id", $PodId, "--vault-root", $VaultRoot)
if ($DryRun) { $args += "--dry-run" }
if ($ApprovedVerify) { $args += "--approved-verify" }
if ($RealDbConfirm) { $args += "--real-db-confirm" }

python @args
exit $LASTEXITCODE
