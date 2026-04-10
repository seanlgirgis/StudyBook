param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$envSetter = Join-Path $repoRoot "env_setter.ps1"

if (-not (Test-Path $envSetter)) {
    Write-Error "Could not find env_setter.ps1 at $envSetter"
    exit 1
}

. $envSetter

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

python @Args
exit $LASTEXITCODE
