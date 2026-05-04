param(
    [string]$ExtractedRoot = "D:\Workarea\StudyBook\demos\rag\pocs\04f",
    [string]$TargetRoot = "D:\Workarea\StudyBook\demos\rag\pocs\04f",
    [switch]$RunDocker,
    [switch]$RunCompose
)

$ErrorActionPreference = "Stop"

function Ensure-Path([string]$Path) {
    if (-not (Test-Path $Path)) {
        throw "Required path missing: $Path"
    }
}

function Write-Section([string]$Text) {
    Write-Host "`n=== $Text ==="
}

Write-Section "1) Mirror files"
Ensure-Path $ExtractedRoot
if (-not (Test-Path $TargetRoot)) {
    New-Item -ItemType Directory -Path $TargetRoot | Out-Null
}
robocopy $ExtractedRoot $TargetRoot /E /MIR | Out-Null

$required = @(
    (Join-Path $TargetRoot "src"),
    (Join-Path $TargetRoot "tests"),
    (Join-Path $TargetRoot "docs"),
    (Join-Path $TargetRoot "outputs"),
    (Join-Path $TargetRoot "docker-compose.yaml")
)
foreach ($p in $required) { Ensure-Path $p }
Write-Host "Mirror complete and required structure confirmed."

Write-Section "2) Verify structure (tree /F)"
Push-Location $TargetRoot
try {
    cmd /c tree /F
}
finally {
    Pop-Location
}

Write-Section "3) Load environment"
. "D:\Workarea\StudyBook\env_setter.ps1"
Write-Host "Environment loaded. Host dependency installation intentionally skipped (Docker-first mode)."

Write-Section "4) Build Docker image"
$dockerfilePath = Join-Path $TargetRoot "src\Dockerfile"
Ensure-Path $dockerfilePath

# Build context is target root so Dockerfile can COPY src/ correctly.
$rootReq = Join-Path $TargetRoot "requirements.txt"
$srcReq = Join-Path $TargetRoot "src\requirements.txt"
$createdTempReq = $false
if (-not (Test-Path $rootReq) -and (Test-Path $srcReq)) {
    Copy-Item -Path $srcReq -Destination $rootReq -Force
    $createdTempReq = $true
}
try {
    docker build -f $dockerfilePath -t poc_04f_service $TargetRoot
}
finally {
    if ($createdTempReq -and (Test-Path $rootReq)) {
        Remove-Item -Path $rootReq -Force
    }
}

if (-not $RunDocker -and -not $RunCompose) {
    Write-Host "No runtime flag provided; defaulting to -RunDocker for full execution."
    $RunDocker = $true
}

if ($RunDocker -and $RunCompose) {
    throw "Choose only one runtime mode: -RunDocker or -RunCompose"
}

$logsHost = Join-Path $TargetRoot "outputs\logs"
if (-not (Test-Path $logsHost)) { New-Item -ItemType Directory -Path $logsHost | Out-Null }

$containerName = "poc_04f_service_run"

if ($RunDocker) {
    Write-Section "5) Run Docker container (detached)"
    cmd /c "docker rm -f $containerName >nul 2>&1"
    $runCmd = "python -m pip install --quiet uvicorn fastapi pytest > /app/logs/pip_runtime_install.log 2>&1 && uvicorn src.app:app --host 0.0.0.0 --port 8000"
    docker run -d --name $containerName -p 8000:8000 -v "${logsHost}:/app/logs" -v "${TargetRoot}:/workspace" poc_04f_service sh -lc $runCmd | Out-Null
}

if ($RunCompose) {
    Write-Section "5) Run docker-compose"
    Ensure-Path (Join-Path $TargetRoot "docker-compose.yaml")
    Push-Location $TargetRoot
    try {
        docker-compose up -d
    }
    finally {
        Pop-Location
    }

    $composeContainer = docker ps --filter "publish=8000" --format "{{.Names}}" | Select-Object -First 1
    if (-not $composeContainer) {
        throw "Could not determine running compose container exposing port 8000."
    }
    $containerName = $composeContainer
}

Write-Section "6) Run tests inside Docker"
$testLog = Join-Path $logsHost "test_results.log"
$testCmd = "python -m pip install --quiet pytest > /app/logs/pip_pytest_install.log 2>&1 && pytest /workspace/tests --tb=short > /app/logs/test_results.log 2>&1"
docker exec $containerName sh -lc $testCmd

$testText = Get-Content -Raw $testLog
if ($testText -match "collected 0 items") {
    throw "Pytest discovered 0 tests inside container. See $testLog"
}
if ($testText -match "=+ FAILURES =+" -or $testText -match " failed") {
    throw "Pytest reported failures inside container. See $testLog"
}
Write-Host "Containerized tests executed."

Write-Section "7) Smoke test API"
$smokeLog = Join-Path $logsHost "smoke_test.log"
$smokePy = @'
import json
import time
import urllib.request

paths = ["http://127.0.0.1:8000/health", "http://127.0.0.1:8000/ping"]
result = {"ok": True, "checks": [], "startup_wait_seconds": 0}
startup_deadline = time.time() + 30

for url in paths:
    passed = False
    last_error = None
    while time.time() < startup_deadline:
        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                body = response.read().decode("utf-8", "replace")
                parsed = json.loads(body)
                is_ok = response.status == 200 and isinstance(parsed, dict) and parsed.get("ok") is True
                if is_ok:
                    result["checks"].append({"url": url, "status": response.status, "body": parsed, "pass": True})
                    passed = True
                    break
                last_error = f"Unexpected payload/status: status={response.status}, body={parsed}"
        except Exception as exc:
            last_error = str(exc)
        time.sleep(1)

    if not passed:
        result["checks"].append({"url": url, "error": last_error or "unknown error", "pass": False})
        result["ok"] = False

result["startup_wait_seconds"] = int(max(0, 30 - max(0, startup_deadline - time.time())))

print(json.dumps(result, indent=2))
raise SystemExit(0 if result["ok"] and len(result["checks"]) == len(paths) else 1)
'@
$tmpSmoke = Join-Path $TargetRoot "outputs\logs\smoke_test_tmp.py"
$smokePy | Set-Content -Encoding UTF8 $tmpSmoke
docker cp $tmpSmoke "${containerName}:/tmp/smoke_test.py" | Out-Null
$smokeOut = docker exec $containerName python /tmp/smoke_test.py
$smokeExit = $LASTEXITCODE
$smokeOut | Set-Content -Encoding UTF8 $smokeLog
Remove-Item -Force $tmpSmoke
if ($smokeExit -ne 0) {
    throw "Smoke test failed. See $smokeLog"
}
Write-Host "Smoke test completed."

Write-Section "8) Confirm success"
$imageInfo = docker images poc_04f_service --format "{{.Repository}}:{{.Tag}} {{.ID}} {{.Size}}" | Select-Object -First 1
$containerId = docker ps --filter "name=$containerName" --format "{{.ID}}" | Select-Object -First 1
$ports = docker port $containerName

Write-Host "Image: $imageInfo"
Write-Host "Container: $containerName ($containerId)"
Write-Host "Ports:`n$ports"

Ensure-Path $testLog
Ensure-Path $smokeLog
Write-Host "Test results log: $testLog"
Write-Host "Smoke test log:   $smokeLog"
Write-Host "Integration run complete."
