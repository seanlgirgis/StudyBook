param(
    [Parameter(Mandatory = $true)]
    [string]$Title,
    [string]$Status = "Proposed",
    [string]$TaskId = "TB-UNSET",
    [string]$DecisionId = "DEC-UNSET",
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function ConvertTo-AdrSlug {
    param(
        [Parameter(Mandatory = $true)]
        [string]$InputValue
    )

    $slug = $InputValue.Trim().ToLowerInvariant()
    $slug = $slug -replace "[^a-z0-9\s-]", ""
    $slug = $slug -replace "\s+", "-"
    $slug = $slug.Trim("-")
    if ([string]::IsNullOrWhiteSpace($slug)) {
        throw "Unable to derive slug from title."
    }
    return $slug
}

$projectRoot = [System.IO.Path]::GetFullPath((Join-Path -Path $PSScriptRoot -ChildPath "..\.."))
$adrDir = Join-Path -Path $projectRoot -ChildPath "docs\adr"
$indexPath = Join-Path -Path $adrDir -ChildPath "ADR-INDEX.md"

if (-not (Test-Path -LiteralPath $adrDir)) {
    throw "ADR directory not found: $adrDir"
}
if (-not (Test-Path -LiteralPath $indexPath)) {
    throw "ADR index not found: $indexPath"
}

$existing = Get-ChildItem -Path $adrDir -Filter "ADR-*.md" -File |
    Where-Object { $_.Name -match "^ADR-(\d{4})-" } |
    ForEach-Object { [int]$matches[1] }

$nextNumber = if ($existing.Count -gt 0) { [int](($existing | Measure-Object -Maximum).Maximum) + 1 } else { 1 }
$numberText = "{0:D4}" -f $nextNumber
$slug = ConvertTo-AdrSlug -InputValue $Title
$fileName = "ADR-$numberText-$slug.md"
$filePath = Join-Path -Path $adrDir -ChildPath $fileName
$dateText = (Get-Date).ToString("yyyy-MM-dd")

$content = @"
# ADR-${numberText}: $Title

## Status
- $Status

## Date
- $dateText

## Decision Makers
- Project owner
- Code agent execution layer

## Context
- TODO

## Decision
- TODO

## Consequences
- Positive:
- Negative:
- Neutral:

## Alternatives Considered
- TODO

## Supersedes
- none

## Superseded By
- none

## Links
- Task: $TaskId
- Decision Log: agents/shared/decision_log.md
- Related Decision ID: $DecisionId
"@

if ($DryRun) {
    Write-Host "Dry run only. Proposed ADR file: $filePath" -ForegroundColor Yellow
    exit 0
}

Set-Content -LiteralPath $filePath -Value $content -Encoding UTF8
Write-Host "Created ADR file: $filePath" -ForegroundColor Green

$indexLine = "| [ADR-$numberText]($fileName) | $Title | $Status | $dateText | $TaskId | $DecisionId |"
Add-Content -LiteralPath $indexPath -Value "`r`n$indexLine" -Encoding UTF8
Write-Host "Appended ADR index entry to: $indexPath" -ForegroundColor Green
