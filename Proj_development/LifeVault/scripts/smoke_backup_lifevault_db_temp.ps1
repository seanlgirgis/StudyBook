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
      return (Join-Path $dTemp "lifevault_backup_smoke")
    }
  } catch {}
  return (Join-Path $env:TEMP "lifevault_backup_smoke")
}

$base = Resolve-SmokeRoot -OverrideRoot $TempRoot
$dbDir = Join-Path $base "db"
$bkDir = Join-Path $base "db_backups"
$dbPath = Join-Path $dbDir "temp_lifevault.sqlite"

New-Item -ItemType Directory -Force -Path $base,$dbDir,$bkDir | Out-Null
if (Test-Path $dbPath) { Remove-Item -Force $dbPath }

Write-Host "Backup smoke temp root: $base"

python -m lifevault.migrate --db-path "$dbPath" --apply 0001_lifevault_core_schema
if ($LASTEXITCODE -ne 0) { throw "Temp DB migration apply failed" }

$timestamp = (Get-Date).ToUniversalTime().ToString("yyyyMMdd_HHmmss")
$backupPath = Join-Path $bkDir "lifevault_${timestamp}.sqlite"
$checksumPath = "$backupPath.sha256"

@"
import hashlib
import sqlite3
import sys
from pathlib import Path

from lifevault.schema_v0 import validate_schema_v0

source = Path(sys.argv[1])
backup = Path(sys.argv[2])
checksum = Path(sys.argv[3])

with sqlite3.connect(source) as src_conn:
    with sqlite3.connect(backup) as dst_conn:
        src_conn.backup(dst_conn)

with sqlite3.connect(backup) as verify_conn:
    verify_conn.execute("SELECT 1").fetchone()
    v = validate_schema_v0(verify_conn)
    if not v["ok"]:
        raise SystemExit(f"Backup schema validation failed: {v}")

h = hashlib.sha256()
with backup.open("rb") as f:
    for chunk in iter(lambda: f.read(1024 * 1024), b""):
        h.update(chunk)
checksum.write_text(f"{h.hexdigest()}  {backup.name}\n", encoding="utf-8")

print(str(backup))
print(str(checksum))
"@ | python - "$dbPath" "$backupPath" "$checksumPath"
if ($LASTEXITCODE -ne 0) { throw "Temp backup failed" }

Write-Host "Temp backup created: $backupPath"
Write-Host "Temp checksum file: $checksumPath"