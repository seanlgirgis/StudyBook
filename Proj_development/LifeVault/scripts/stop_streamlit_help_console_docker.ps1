param(
    [switch]$Down
)

$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = (Resolve-Path (Join-Path $scriptDir "..")).Path
$composeFile = Join-Path $projectRoot "docker\streamlit_dashboard\docker-compose.yml"

try {
    Push-Location $projectRoot
    if ($Down) {
        Write-Host "Stopping and removing containers for Streamlit Help Console (docker compose down)."
        docker compose -f $composeFile down
    }
    else {
        Write-Host "Stopping Streamlit Help Console containers (docker compose stop)."
        docker compose -f $composeFile stop
    }

    if ($LASTEXITCODE -ne 0) { throw "docker compose stop/down failed" }
    Pop-Location
    exit 0
}
catch {
    try { Pop-Location } catch {}
    Write-Error "Failed to stop Streamlit Help Console docker stack: $_"
    exit 1
}
