param([Parameter(Mandatory=$true)][string]$PodId)
$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptDir "..")
$env:PYTHONPATH = (Join-Path $repoRoot "src")
$code = @"
import csv, hashlib, re
from pathlib import Path
from onedriveclean.config import load_config
cfg = load_config(Path(r'$repoRoot'))
pod_dir = cfg.lab_path('pods_dir') / r'$PodId'
orig = pod_dir / 'original_copies'
rep = pod_dir / 'reports'
rep.mkdir(parents=True, exist_ok=True)
out = rep / 'duplicate_candidates.csv'
if not orig.exists():
    raise SystemExit('pod original_copies missing')

def norm_name(n):
    base = Path(n).stem.lower()
    base = re.sub(r'[^a-z0-9]+', '_', base).strip('_')
    return base + Path(n).suffix.lower()

rows = []
for p in sorted(x for x in orig.rglob('*') if x.is_file()):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    st = p.stat()
    rows.append({'relative_path':str(p.relative_to(orig)),'filename':p.name,'normalized_filename':norm_name(p.name),'size_bytes':int(st.st_size),'sha256':h.hexdigest()})

by_name, by_size, by_hash = {}, {}, {}
for r in rows:
    by_name.setdefault(r['normalized_filename'], []).append(r)
    by_size.setdefault(r['size_bytes'], []).append(r)
    by_hash.setdefault(r['sha256'], []).append(r)

with out.open('w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['pod_id','relative_path','filename','normalized_filename','size_bytes','sha256','same_normalized_filename_group','same_size_group','same_sha256_group'])
    w.writeheader()
    for r in rows:
        w.writerow({'pod_id':r'$PodId','relative_path':r['relative_path'],'filename':r['filename'],'normalized_filename':r['normalized_filename'],'size_bytes':r['size_bytes'],'sha256':r['sha256'],'same_normalized_filename_group':len(by_name[r['normalized_filename']])>1,'same_size_group':len(by_size[r['size_bytes']])>1,'same_sha256_group':len(by_hash[r['sha256']])>1})
print(out)
"@
python -c $code
