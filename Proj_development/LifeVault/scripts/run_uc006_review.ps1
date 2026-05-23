param(
    [Parameter(Mandatory = $true)][string]$PodId,
    [string]$DbPath = "D:\AI_Lab\LifeVault\db\lifevault.sqlite",
    [switch]$ListItems,
    [switch]$ListDuplicates,
    [switch]$PublishReadiness,
    [string]$PodRelativePath,
    [string]$Decision,
    [string]$ApprovedForVaultPublish,
    [switch]$ApprovedUpdate,
    [switch]$RealDbConfirm,
    [int]$Limit = 500
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = (Resolve-Path (Join-Path $scriptDir "..")).Path
$srcPath = Join-Path $projectRoot "src"
if ($env:PYTHONPATH) {
    $env:PYTHONPATH = "$srcPath;$env:PYTHONPATH"
} else {
    $env:PYTHONPATH = $srcPath
}

$args = @("-m", "lifevault.uc006_cli", "--db-path", $DbPath, "--pod-id", $PodId, "--limit", "$Limit")
if ($ListItems) { $args += "--list-items" }
if ($ListDuplicates) { $args += "--list-duplicates" }
if ($PublishReadiness) { $args += "--publish-readiness" }
if ($PodRelativePath) { $args += @("--pod-relative-path", $PodRelativePath) }
if ($Decision) { $args += @("--decision", $Decision) }
if ($ApprovedForVaultPublish) { $args += @("--approved-for-vault-publish", $ApprovedForVaultPublish) }
if ($ApprovedUpdate) { $args += "--approved-update" }
if ($RealDbConfirm) { $args += "--real-db-confirm" }

python @args
exit $LASTEXITCODE
