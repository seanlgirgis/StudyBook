$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $scriptDir "..\..\scripts\_lab_common.ps1")
$ctx = Get-LabContext -ScriptDir $scriptDir -LabName "06_local_inventory_scan"
$env:PYTHONPATH = (Join-Path $ctx.RepoRoot "src")
$fake = Join-Path $ctx.RunDir "fake_batch"
New-Item -ItemType Directory -Force -Path (Join-Path $fake "docs"), (Join-Path $fake "photos") | Out-Null
Set-Content -Encoding UTF8 (Join-Path $fake "docs\readme.txt") "hello"
Set-Content -Encoding UTF8 (Join-Path $fake "photos\pic.jpg") "img"
$code = @"
import csv
from pathlib import Path
from onedriveclean.inventory_local import scan_folder
root = Path(r'$fake')
out = Path(r'$($ctx.RunDir)\\file_inventory.csv')
rows = scan_folder(root)
with out.open('w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); [w.writerow(r) for r in rows]
print(len(rows))
"@
python -c $code
