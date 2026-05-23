param(
  [string]$TempRoot
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Resolve-Path (Join-Path $scriptDir "..")
$srcPath = Join-Path $projectRoot "src"

if ($env:PYTHONPATH) {
  $env:PYTHONPATH = "$srcPath;$($env:PYTHONPATH)"
} else {
  $env:PYTHONPATH = $srcPath
}

function Resolve-SmokeRoot {
  param([string]$OverrideRoot)
  if ($OverrideRoot) { return $OverrideRoot }

  $dTemp = "D:\temp"
  try {
    if (-not (Test-Path $dTemp)) {
      New-Item -ItemType Directory -Force -Path $dTemp | Out-Null
    }
    if (Test-Path $dTemp) {
      return (Join-Path $dTemp "lifevault_init_db_smoke")
    }
  } catch {}

  return (Join-Path $env:TEMP "lifevault_init_db_smoke")
}

$base = Resolve-SmokeRoot -OverrideRoot $TempRoot
New-Item -ItemType Directory -Force -Path $base | Out-Null
$dbPath = Join-Path $base "temp_lifevault.sqlite"
if (Test-Path $dbPath) { Remove-Item -Force $dbPath }

Write-Host "Init DB smoke root: $base"

python -m lifevault.migrate --db-path "$dbPath" --apply 0001_lifevault_core_schema
if ($LASTEXITCODE -ne 0) { throw "Migration apply failed" }

python -m lifevault.migrate --db-path "$dbPath" --validate
if ($LASTEXITCODE -ne 0) { throw "Schema validation failed" }

Write-Host "Temp DB initialized: $dbPath"
Write-Host "Migration applied and validated: 0001_lifevault_core_schema"