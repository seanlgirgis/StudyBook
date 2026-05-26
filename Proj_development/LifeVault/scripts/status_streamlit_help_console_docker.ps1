param(
    [switch]$Logs,
    [int]$Tail = 50
)

$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = (Resolve-Path (Join-Path $scriptDir "..")).Path
$composeFile = Join-Path $projectRoot "docker\streamlit_dashboard\docker-compose.yml"

try {
    Push-Location $projectRoot
    docker compose -f $composeFile ps
    if ($LASTEXITCODE -ne 0) { throw "docker compose ps failed" }

    if ($Logs) {
        docker compose -f $composeFile logs --tail $Tail
        if ($LASTEXITCODE -ne 0) { throw "docker compose logs failed" }
    }

    Pop-Location
    exit 0
}
catch {
    try { Pop-Location } catch {}
    Write-Error "Failed to get Streamlit Help Console docker status: $_"
    exit 1
}
