param(
  [Parameter(Mandatory=$true)][string]$SourcePath,
  [Parameter(Mandatory=$true)][string]$PodName,
  [Parameter(Mandatory=$true)][string]$Project,
  [Parameter(Mandatory=$true)][string]$Category,
  [Parameter(Mandatory=$true)][string]$EventName,
  [Parameter(Mandatory=$true)][string]$SuggestedVaultPath
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptDir "..")
$env:PYTHONPATH = (Join-Path $repoRoot "src")

$code = @"
import csv, json, re, shutil
from datetime import datetime
from pathlib import Path
from onedriveclean.config import load_config

source = Path(r'$SourcePath')
if not source.exists() or not source.is_dir():
    raise SystemExit(f"SourcePath must exist as directory: {source}")

pod_name = r'$PodName'
project = r'$Project'
category = r'$Category'
event_name = r'$EventName'
suggested_vault_path = r'$SuggestedVaultPath'

cfg = load_config(Path(r'$repoRoot'))
pods_root = cfg.lab_path('pods_dir')
pods_root.mkdir(parents=True, exist_ok=True)

safe_name = re.sub(r'[^a-z0-9]+', '_', pod_name.lower()).strip('_') or 'pod'
pod_id = f"pod_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_name}"
pod_dir = pods_root / pod_id
orig = pod_dir / 'original_copies'
reports = pod_dir / 'reports'
orig.mkdir(parents=True, exist_ok=True)
reports.mkdir(parents=True, exist_ok=True)

manifest = pod_dir / '_pod_manifest.csv'
profile = pod_dir / '_pod_profile.json'
review = pod_dir / '_review.csv'
notes = pod_dir / '_notes.md'

rows = []
for p in sorted(x for x in source.rglob('*') if x.is_file()):
    rel = p.relative_to(source)
    dst = orig / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(p, dst)
    st = p.stat()
    rows.append({
        'pod_id': pod_id,
        'pod_name': pod_name,
        'source_path': str(source),
        'source_file_path': str(p),
        'pod_file_path': str(dst),
        'filename': p.name,
        'extension': p.suffix.lower(),
        'size_bytes': int(st.st_size),
        'modified_time': datetime.fromtimestamp(st.st_mtime).isoformat(timespec='seconds'),
        'project': project,
        'category': category,
        'event_name': event_name,
        'suggested_vault_path': suggested_vault_path,
        'text_extraction_status': 'not_extracted',
    })

fields = ['pod_id','pod_name','source_path','source_file_path','pod_file_path','filename','extension','size_bytes','modified_time','project','category','event_name','suggested_vault_path','text_extraction_status']
with manifest.open('w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for r in rows:
        w.writerow(r)

pod_profile = {
    'pod_id': pod_id,
    'pod_name': pod_name,
    'source_path': str(source),
    'project': project,
    'category': category,
    'event_name': event_name,
    'suggested_vault_path': suggested_vault_path,
    'created_at': datetime.now().isoformat(timespec='seconds'),
    'status': 'onboarded_needs_review',
    'notes': ''
}
profile.write_text(json.dumps(pod_profile, indent=2) + '\n', encoding='utf-8')
review.write_text('filename,decision,notes\n', encoding='utf-8')
notes.write_text('# Pod Notes\n\n', encoding='utf-8')
print(pod_id)
"@

python -c $code
