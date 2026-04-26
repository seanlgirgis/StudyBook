$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

if (-not (Test-Path ".env")) {
    throw ".env not found. Copy .env.example to .env first."
}

Write-Host "[check] compose services"
$psOutput = docker compose ps --format json | Out-String
if (-not $psOutput.Trim()) {
    throw "No compose services found. Run ./scripts/manage.ps1 up"
}

Write-Host "[check] web health endpoint"
$healthOk = $false
for ($i = 0; $i -lt 20; $i++) {
    try {
        $resp = Invoke-WebRequest -Uri "http://localhost:8088/health" -UseBasicParsing -TimeoutSec 5
        if ($resp.StatusCode -eq 200) {
            $healthOk = $true
            break
        }
    }
    catch {
        Start-Sleep -Seconds 3
    }
}
if (-not $healthOk) {
    throw "Airflow webserver health endpoint did not become ready on http://localhost:8088/health"
}

Write-Host "[check] DAG list includes sample DAG"
$dagList = docker compose run --rm airflow-cli airflow dags list | Out-String
if ($dagList -notmatch "studybook_docker_hello") {
    throw "Sample DAG studybook_docker_hello not found."
}

Write-Host "[ok] Smoke test passed"