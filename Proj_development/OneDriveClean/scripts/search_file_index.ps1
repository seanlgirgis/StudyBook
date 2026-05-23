param([Parameter(Mandatory=$true)][string]$Query)
$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptDir "..")
$env:PYTHONPATH = (Join-Path $repoRoot "src")
$code = @"
from onedriveclean.db import connect_db, ensure_tables, search_files
rows = search_files(connect_db(), r'$Query')
for r in rows:
    print(f"[{r['batch_name']}] {r['filename']} | {r['project']} | {r['category']} | {r['staged_path']} | status={r['copy_status']}")
print(f"matches={len(rows)}")
"@
python -c $code
