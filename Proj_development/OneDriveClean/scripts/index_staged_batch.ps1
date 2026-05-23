param([Parameter(Mandatory=$true)][string]$BatchName)
$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptDir "..")
$env:PYTHONPATH = (Join-Path $repoRoot "src")
$code = @"
from pathlib import Path
from onedriveclean.config import load_config
from onedriveclean.db import connect_db, ensure_tables, read_manifest_csv, upsert_batch, upsert_files_from_manifest
cfg = load_config(Path(r'$repoRoot'))
batch = r'$BatchName'
manifest = cfg.lab_path('staging_dir') / batch / '_manifest.csv'
if not manifest.exists():
    raise SystemExit(f"Manifest not found: {manifest}")
rows = read_manifest_csv(manifest)
conn = connect_db()
ensure_tables(conn)
batch_row = {'batch_name': batch, 'source_name': rows[0].get('source_name','') if rows else '', 'project': rows[0].get('project','') if rows else '', 'category': rows[0].get('category','') if rows else '', 'suggested_clean_remote_path': rows[0].get('suggested_clean_remote_path','') if rows else '', 'notes': None}
upsert_batch(conn, batch_row)
count = upsert_files_from_manifest(conn, rows)
print(f'indexed_files={count}')
"@
python -c $code
