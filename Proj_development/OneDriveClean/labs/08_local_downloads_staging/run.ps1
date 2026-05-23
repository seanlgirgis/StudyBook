param(
  [Parameter(Mandatory = $true)]
  [string]$BatchName
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptDir "..\..")
$env:PYTHONPATH = (Join-Path $repoRoot "src")

$code = @"
import csv, fnmatch, shutil
from datetime import datetime
from pathlib import Path
from onedriveclean.config import load_config

batch_name = r'$BatchName'
cfg = load_config(Path(r'$repoRoot'))
b = cfg.staging_batches.get('batches', {}).get(batch_name)
if not b:
    raise SystemExit(f"Batch not found: {batch_name}")
source_name = b.get('source_name')
source = Path(cfg.local_sources.get('sources', {}).get(source_name, {}).get('path', ''))
if not source.exists():
    raise SystemExit(f"Source path not found: {source}")
stage_dir = cfg.lab_path('staging_dir') / batch_name
stage_dir.mkdir(parents=True, exist_ok=True)
manifest = stage_dir / '_manifest.csv'
includes = b.get('include_globs', ['*'])
excludes = b.get('exclude_globs', [])
project = b.get('project', '')
category = b.get('category', '')
suggested = b.get('suggested_clean_remote_path', '')
rows = []
for p in sorted(x for x in source.rglob('*') if x.is_file()):
    rel = p.relative_to(source)
    rel_s = str(rel).replace('\\\\', '/')
    if not any(fnmatch.fnmatch(p.name, pat) or fnmatch.fnmatch(rel_s, pat) for pat in includes):
        continue
    if any(fnmatch.fnmatch(rel_s, pat) for pat in excludes):
        continue
    dst = stage_dir / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(p, dst)
    st = p.stat()
    rows.append({'source_name':source_name,'source_path':str(p),'staged_path':str(dst),'filename':p.name,'extension':p.suffix.lower(),'size_bytes':int(st.st_size),'modified_time':datetime.fromtimestamp(st.st_mtime).isoformat(timespec='seconds'),'batch_name':batch_name,'project':project,'category':category,'suggested_clean_remote_path':suggested})
fields=['source_name','source_path','staged_path','filename','extension','size_bytes','modified_time','batch_name','project','category','suggested_clean_remote_path']
with manifest.open('w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); [w.writerow(r) for r in rows]
print(f'staged_files={len(rows)}')
print(f'manifest={manifest}')
"@
python -c $code
