[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$snapshotRoot = Join-Path -Path $PSScriptRoot -ChildPath "snapshots"
$snapshotDir = Join-Path -Path $snapshotRoot -ChildPath $timestamp

if (-not (Test-Path -LiteralPath $snapshotRoot)) {
    New-Item -ItemType Directory -Path $snapshotRoot | Out-Null
}
New-Item -ItemType Directory -Path $snapshotDir | Out-Null

$filesToCopy = @(
    "AGENTS.md",
    "PROJECT_STATE.md",
    "TASK_BOARD.md",
    "HANDOFF.md",
    "DAILY_LOG.md",
    "DECISIONS.md",
    "KNOWN_ISSUES.md",
    "CHANGELOG.md"
)

foreach ($file in $filesToCopy) {
    $sourcePath = Join-Path -Path $repoRoot -ChildPath $file
    if (Test-Path -LiteralPath $sourcePath) {
        $destinationPath = Join-Path -Path $snapshotDir -ChildPath $file
        Copy-Item -LiteralPath $sourcePath -Destination $destinationPath -Force
    }
}

Write-Output $snapshotDir
