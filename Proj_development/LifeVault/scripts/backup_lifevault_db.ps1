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

$sourceDb = "D:\AI_Lab\LifeVault\db\lifevault.sqlite"
$backupDir = "D:\AI_Lab\LifeVault\db_backups"

if (-not (Test-Path $sourceDb)) {
  throw "Source DB not found: $sourceDb"
}

if (-not (Test-Path $backupDir)) {
  New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
}

$timestamp = (Get-Date).ToUniversalTime().ToString("yyyyMMdd_HHmmss")
$backupPath = Join-Path $backupDir "lifevault_${timestamp}.sqlite"
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
"@ | python - "$sourceDb" "$backupPath" "$checksumPath"
if ($LASTEXITCODE -ne 0) { throw "Backup operation failed" }

Write-Host "Backup created: $backupPath"
Write-Host "Checksum file: $checksumPath"