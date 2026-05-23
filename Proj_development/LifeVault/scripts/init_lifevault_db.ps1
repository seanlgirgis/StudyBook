param()

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Resolve-Path (Join-Path $scriptDir "..")
$srcPath = Join-Path $projectRoot "src"

if ($env:PYTHONPATH) {
  $env:PYTHONPATH = "$srcPath;$($env:PYTHONPATH)"
} else {
  $env:PYTHONPATH = $srcPath
}

$dbPath = "D:\AI_Lab\LifeVault\db\lifevault.sqlite"
$dbDir = Split-Path -Parent $dbPath

if (-not (Test-Path $dbDir)) {
  New-Item -ItemType Directory -Force -Path $dbDir | Out-Null
}

if (Test-Path $dbPath) {
  throw "Refusing to overwrite existing DB: $dbPath"
}

python -m lifevault.migrate --db-path "$dbPath" --apply 0001_lifevault_core_schema --real-db-confirm
if ($LASTEXITCODE -ne 0) { throw "Migration apply failed" }

python -m lifevault.migrate --db-path "$dbPath" --validate --real-db-confirm
if ($LASTEXITCODE -ne 0) { throw "Schema validation failed" }

Write-Host "LifeVault DB initialized: $dbPath"
Write-Host "Migration applied: 0001_lifevault_core_schema"
