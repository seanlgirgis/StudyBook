param(
    [ValidateSet("up", "down", "logs", "restart")]
    [string]$Action = "up"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$ComposeFile = Join-Path $Root "docker\index_ui\docker-compose.yml"

if (-not (Test-Path -LiteralPath $ComposeFile)) {
    throw "Compose file not found at $ComposeFile"
}

switch ($Action) {
    "up" {
        docker compose -f $ComposeFile up -d --build
        if ($LASTEXITCODE -ne 0) {
            throw "Docker compose up failed with exit code $LASTEXITCODE."
        }
        Write-Host "Index UI running at http://localhost:8501" -ForegroundColor Green
    }
    "down" {
        docker compose -f $ComposeFile down
        if ($LASTEXITCODE -ne 0) {
            throw "Docker compose down failed with exit code $LASTEXITCODE."
        }
    }
    "logs" {
        docker compose -f $ComposeFile logs -f --tail 100
        if ($LASTEXITCODE -ne 0) {
            throw "Docker compose logs failed with exit code $LASTEXITCODE."
        }
    }
    "restart" {
        docker compose -f $ComposeFile down
        if ($LASTEXITCODE -ne 0) {
            throw "Docker compose down failed with exit code $LASTEXITCODE."
        }
        docker compose -f $ComposeFile up -d --build
        if ($LASTEXITCODE -ne 0) {
            throw "Docker compose up failed with exit code $LASTEXITCODE."
        }
        Write-Host "Index UI running at http://localhost:8501" -ForegroundColor Green
    }
}
