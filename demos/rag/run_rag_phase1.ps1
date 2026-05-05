<#
.SYNOPSIS
Automates Phase 1 RAG local setup: Docker build, container run, endpoint test, and log verification.

.DESCRIPTION
- Copies src, data, outputs folders into container
- Builds Docker image
- Runs container
- Tests /health, /ping, and /ask endpoints
- Displays latest logs from outputs/ask_logs.json
- Runs in-container pytest

#>

# Config
$dockerImageName = "poc_04g_rag"
$dockerContainerName = "poc_04g_rag_run"
$localPort = 8000
$baseDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$askLog = Join-Path $baseDir "outputs\ask_logs.json"

# Step 0: Ensure outputs folder exists
$outputsDir = Join-Path $baseDir "outputs"
if (-Not (Test-Path $outputsDir)) { New-Item -ItemType Directory -Path $outputsDir | Out-Null }

# Step 1: Build Docker image
Write-Host "`nBuilding Docker image..." -ForegroundColor Cyan
docker build -t $dockerImageName $baseDir

# Step 2: Stop and remove any existing container with the same name
$existing = docker ps -a --filter "name=$dockerContainerName" --format "{{.ID}}"
if ($existing) {
    Write-Host "`nStopping and removing existing container..." -ForegroundColor Yellow
    docker stop $dockerContainerName | Out-Null
    docker rm $dockerContainerName | Out-Null
}

# Step 3: Run Docker container
Write-Host "`nStarting Docker container..." -ForegroundColor Cyan
docker run --name $dockerContainerName -d -p $localPort:8000 $dockerImageName

Start-Sleep -Seconds 5  # Wait a moment for container to initialize

# Step 4: Test deterministic endpoints
Write-Host "`nTesting /health endpoint..." -ForegroundColor Green
Invoke-RestMethod http://localhost:$localPort/health | ConvertTo-Json

Write-Host "`nTesting /ping endpoint..." -ForegroundColor Green
Invoke-RestMethod http://localhost:$localPort/ping | ConvertTo-Json

# Step 5: Test /ask endpoint with a sample query
$sampleQuery = "AC repair"
Write-Host "`nTesting /ask endpoint with query: '$sampleQuery'" -ForegroundColor Green
$response = Invoke-RestMethod "http://localhost:$localPort/ask?query=$($sampleQuery -replace ' ','%20')"
$response | ConvertTo-Json

# Step 6: Show last 5 lines of ask_logs.json
if (Test-Path $askLog) {
    Write-Host "`nLast 5 log entries from ask_logs.json:" -ForegroundColor Cyan
    Get-Content $askLog -Tail 5
} else {
    Write-Host "`nNo ask_logs.json found yet." -ForegroundColor Yellow
}

# Step 7: Run in-container pytest
Write-Host "`nRunning in-container pytest..." -ForegroundColor Cyan
docker exec -it $dockerContainerName pytest tests/

Write-Host "`nPhase 1 RAG automation complete!" -ForegroundColor Magenta