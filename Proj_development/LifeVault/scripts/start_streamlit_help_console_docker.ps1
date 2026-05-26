param()

$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = (Resolve-Path (Join-Path $scriptDir "..")).Path
$composeFile = Join-Path $projectRoot "docker\streamlit_dashboard\docker-compose.yml"

try {
    Push-Location $projectRoot
    docker compose -f $composeFile up -d --build
    if ($LASTEXITCODE -ne 0) { throw "docker compose up failed" }

    Write-Host "LifeVault Help Console URL: http://localhost:8501"
    docker compose -f $composeFile ps
    if ($LASTEXITCODE -ne 0) { throw "docker compose ps failed" }

    Pop-Location
    exit 0
}
catch {
    try { Pop-Location } catch {}
    Write-Error "Failed to start Streamlit Help Console docker stack: $_"
    exit 1
}
