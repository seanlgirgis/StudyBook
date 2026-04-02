[CmdletBinding()]
param(
    [string]$TargetHost = 'localhost',
    [string]$EnvFile = 'D:\StudyBook\_infra\env\.env.local',
    [switch]$AsJson
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$scripts = @(
    'Run-CoreDockerProofs.ps1',
    'Run-StreamingDockerProofs.ps1',
    'Run-PipelineDockerProofs.ps1',
    'Run-ObservabilityDockerProofs.ps1'
)

$allResults = @()
$hasFailure = $false

foreach ($scriptName in $scripts) {
    $scriptPath = Join-Path -Path $PSScriptRoot -ChildPath $scriptName
    if (-not (Test-Path -LiteralPath $scriptPath)) {
        $allResults += [PSCustomObject]@{
            Group = $scriptName
            Error = 'Script missing'
            Success = $false
        }
        $hasFailure = $true
        continue
    }

    $json = & $scriptPath -TargetHost $TargetHost -EnvFile $EnvFile -AsJson
    $exitCode = $LASTEXITCODE

    $parsed = $null
    try {
        $parsed = $json | ConvertFrom-Json
    } catch {
        $parsed = @([PSCustomObject]@{ Name = $scriptName; Success = $false; Detail = 'Could not parse JSON output.' })
    }

    if ($parsed -isnot [System.Array]) {
        $parsed = @($parsed)
    }

    foreach ($item in $parsed) {
        if (-not ($item.PSObject.Properties.Name -contains 'Group')) {
            $item | Add-Member -NotePropertyName Group -NotePropertyValue $scriptName
        }
        $allResults += $item
    }

    if ($exitCode -ne 0) {
        $hasFailure = $true
    }
}

if ($AsJson) {
    $allResults | ConvertTo-Json -Depth 6
} else {
    $allResults | Sort-Object Group, Name | Format-Table Group, Name, Method, Success, LatencyMs -AutoSize
}

if ($hasFailure) {
    exit 1
}

