param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("list", "unpause", "trigger", "state")]
    [string]$Action
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$dagId = "studybook_docker_hello"

switch ($Action) {
    "list" {
        docker compose run --rm airflow-cli airflow dags list
    }
    "unpause" {
        docker compose run --rm airflow-cli airflow dags unpause $dagId
    }
    "trigger" {
        docker compose run --rm airflow-cli airflow dags trigger $dagId
    }
    "state" {
        docker compose run --rm airflow-cli airflow dags state $dagId (Get-Date -Format "yyyy-MM-dd")
    }
}