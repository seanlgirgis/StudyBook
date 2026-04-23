param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$envSetter = Join-Path $repoRoot "env_setter.ps1"
$generator = Join-Path $repoRoot "scripts\generate_audio.py"

if (-not (Test-Path $envSetter)) {
    Write-Error "Could not find env_setter.ps1 at $envSetter"
    exit 1
}
if (-not (Test-Path $generator)) {
    Write-Error "Could not find audio generator script at $generator"
    exit 1
}

. $envSetter

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

$defaultArgs = @(
    "--format", "mp3",
    "--chunk-chars", "1800",
    "--max-completion-tokens", "4000",
    "--instructions", "Read verbatim and do not summarize. Use a calm, natural interview pace. Keep pacing consistent from start to finish and do not speed up near the end. For dialogue, make speaker turns clear with subtle tone shifts only."
)

python $generator @defaultArgs @Args
exit $LASTEXITCODE
