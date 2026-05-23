param([Parameter(Mandatory=$true)][string]$PodId)
$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptDir "..")
$env:PYTHONPATH = (Join-Path $repoRoot "src")
$code = @"
import json
from pathlib import Path
from onedriveclean.config import load_config
from onedriveclean.db import connect_db, ensure_tables, read_manifest_csv, upsert_pod, upsert_files_from_manifest
cfg = load_config(Path(r'$repoRoot'))
pod_dir = cfg.lab_path('pods_dir') / r'$PodId'
profile_path = pod_dir / '_pod_profile.json'
manifest_path = pod_dir / '_pod_manifest.csv'
if not profile_path.exists() or not manifest_path.exists():
    raise SystemExit('pod profile or manifest missing')
profile = json.loads(profile_path.read_text(encoding='utf-8'))
rows = read_manifest_csv(manifest_path)
conn = connect_db()
ensure_tables(conn)
upsert_pod(conn, profile)
print(upsert_files_from_manifest(conn, rows))
"@
python -c $code
