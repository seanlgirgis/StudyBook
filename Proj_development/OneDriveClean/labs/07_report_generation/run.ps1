$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $scriptDir "..\..\scripts\_lab_common.ps1")
$ctx = Get-LabContext -ScriptDir $scriptDir -LabName "07_report_generation"
$env:PYTHONPATH = (Join-Path $ctx.RepoRoot "src")
$inv = Join-Path $ctx.LabRunsRoot "06_local_inventory_scan\file_inventory.csv"
if (-not (Test-Path $inv)) { throw "Run lab 06 first" }
$code = @"
import csv
from collections import Counter, defaultdict
from pathlib import Path
rows = list(csv.DictReader(open(r'$inv', encoding='utf-8')))
out = Path(r'$($ctx.RunDir)'); out.mkdir(parents=True, exist_ok=True)
ext=Counter((r.get('extension') or '').lower() for r in rows)
with open(out/'extension_summary.csv','w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['extension','file_count']); w.writeheader(); [w.writerow({'extension':k,'file_count':v}) for k,v in sorted(ext.items())]
folders=defaultdict(int)
for r in rows: folders[str(Path(r.get('relative_path','')).parent)] += int(r.get('size_bytes',0) or 0)
with open(out/'folder_summary.csv','w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['folder','total_size_bytes']); w.writeheader(); [w.writerow({'folder':k,'total_size_bytes':v}) for k,v in sorted(folders.items())]
with open(out/'large_files.csv','w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['relative_path','size_bytes']); w.writeheader(); [w.writerow({'relative_path':r['relative_path'],'size_bytes':r['size_bytes']}) for r in rows if int(r.get('size_bytes',0) or 0) >= 100]
by=defaultdict(list)
for r in rows: by[(r.get('filename') or '').lower()].append(r)
with open(out/'same_filename_candidates.csv','w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['filename_key','filename','relative_path','size_bytes']); w.writeheader(); [w.writerow({'filename_key':k,'filename':i['filename'],'relative_path':i['relative_path'],'size_bytes':i['size_bytes']}) for k,g in sorted(by.items()) if len(g)>1 for i in sorted(g,key=lambda x:x['relative_path'])]
print('ok')
"@
python -c $code
