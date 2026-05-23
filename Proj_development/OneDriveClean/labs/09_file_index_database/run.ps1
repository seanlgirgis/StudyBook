$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptDir "..\\..")
$env:PYTHONPATH = (Join-Path $repoRoot "src")

$tempRoot = Join-Path $env:TEMP "odc_lab09"
if (Test-Path $tempRoot) { Remove-Item -Recurse -Force $tempRoot }
New-Item -ItemType Directory -Force -Path $tempRoot | Out-Null
$stage = Join-Path $tempRoot "stage"
New-Item -ItemType Directory -Force -Path $stage | Out-Null
@"
source_name,source_path,staged_path,filename,extension,size_bytes,modified_time,batch_name,project,category,suggested_clean_remote_path
fake_source,C:\\fake\\a.pdf,C:\\fake_stage\\a.pdf,a.pdf,.pdf,123,2026-05-22T10:00:00,batch_009_fake,BOA_LTIMindtree,career_onboarding,FileStore/10_Career/BOA_LTIMindtree/2026_Onboarding
"@ | Set-Content -Encoding UTF8 (Join-Path $stage "_manifest.csv")
$code = @"
from pathlib import Path
from onedriveclean.db import connect_db, ensure_tables, read_manifest_csv, upsert_batch, upsert_files_from_manifest
p = Path(r'$tempRoot') / 'lab09.sqlite'
conn = connect_db(p)
ensure_tables(conn)
rows = read_manifest_csv(Path(r'$stage') / '_manifest.csv')
upsert_batch(conn, {'batch_name':'batch_009_fake','source_name':'fake_source','project':'BOA_LTIMindtree','category':'career_onboarding','suggested_clean_remote_path':'FileStore/10_Career/BOA_LTIMindtree/2026_Onboarding','notes':None})
print(upsert_files_from_manifest(conn, rows))
"@
python -c $code
