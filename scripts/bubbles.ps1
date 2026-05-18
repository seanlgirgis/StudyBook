Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$runner = Join-Path $repoRoot "Study_bubbles\tools\studybubble.py"

if (-not (Test-Path $runner)) {
    throw "StudyBubble runner not found: $runner"
}

& python $runner @args
exit $LASTEXITCODE
