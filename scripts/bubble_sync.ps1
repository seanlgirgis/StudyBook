[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Runs from the current directory. Expect to be inside a StudyBubble container
# (folder containing bubbles.ini), but bubbles will report a clear error if not.
if (-not (Get-Command bubbles -ErrorAction SilentlyContinue)) {
    throw "'bubbles' command not found. Run: cd D:\Workarea\StudyBook; .\env_setter.ps1"
}

Write-Host 'Running: bubbles sync-layout' -ForegroundColor Yellow
bubbles sync-layout
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host 'Running: bubbles build' -ForegroundColor Yellow
bubbles build
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host 'bubble_sync complete.' -ForegroundColor Green
