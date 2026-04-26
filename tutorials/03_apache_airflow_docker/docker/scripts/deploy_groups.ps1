param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("init", "up", "down", "ps")]
    [string]$Action
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
}
if (-not (Select-String -Path ".env" -Pattern "^COMPOSE_PROJECT_NAME=" -Quiet)) {
    $envRaw = Get-Content -Raw ".env"
    Set-Content ".env" ("COMPOSE_PROJECT_NAME=docker_airflow`r`n" + $envRaw)
}

foreach ($dir in @("dags", "logs", "plugins", "config")) {
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir | Out-Null }
}

$files = @("--project-directory", ".", "-f", "compose_groups/00_infra.yml", "-f", "compose_groups/10_airflow.yml")

switch ($Action) {
    "init" {
        docker compose @files run --rm airflow-init
    }
    "up" {
        docker compose @files up -d postgres redis
        docker compose @files run --rm airflow-init
        docker compose @files up -d airflow-webserver airflow-scheduler airflow-triggerer airflow-worker
    }
    "down" {
        docker compose @files down
    }
    "ps" {
        docker compose @files ps
    }
}
