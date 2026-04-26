param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("init", "up", "down", "restart", "ps", "logs", "dags")]
    [string]$Action
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

if (-not (Test-Path ".env")) {
    Write-Host "[info] .env not found. Creating from .env.example"
    Copy-Item ".env.example" ".env"
}

if (-not (Select-String -Path ".env" -Pattern "^COMPOSE_PROJECT_NAME=" -Quiet)) {
    $envRaw = Get-Content -Raw ".env"
    Set-Content ".env" ("COMPOSE_PROJECT_NAME=docker_airflow`r`n" + $envRaw)
}

foreach ($dir in @("dags", "logs", "plugins", "config")) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
    }
}

switch ($Action) {
    "init" {
        docker compose run --rm airflow-init
        Write-Host "[ok] Airflow initialized"
    }
    "up" {
        docker compose up -d postgres redis
        docker compose run --rm airflow-init
        docker compose up -d airflow-webserver airflow-scheduler airflow-triggerer airflow-worker
        Write-Host "[ok] Airflow services are starting"
    }
    "down" {
        docker compose down
        Write-Host "[ok] Stack stopped"
    }
    "restart" {
        docker compose down
        docker compose up -d postgres redis
        docker compose run --rm airflow-init
        docker compose up -d airflow-webserver airflow-scheduler airflow-triggerer airflow-worker
        Write-Host "[ok] Stack restarted"
    }
    "ps" {
        docker compose ps
    }
    "logs" {
        docker compose logs -f --tail 100
    }
    "dags" {
        docker compose run --rm airflow-cli airflow dags list
    }
}
