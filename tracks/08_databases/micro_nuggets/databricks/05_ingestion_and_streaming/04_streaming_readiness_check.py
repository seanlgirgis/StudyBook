from __future__ import annotations

import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent))
from _db_connect import get_creds

print("\n-- Phase 2 · 05-04 Streaming Readiness Check --")

creds = get_creds()
host = (creds.get("DATABRICKS_HOST") or "").rstrip("/")
token = creds.get("DATABRICKS_TOKEN") or ""

if not host or not token:
    raise SystemExit("Missing DATABRICKS_HOST or DATABRICKS_TOKEN.")

if not host.startswith("http"):
    host = f"https://{host}"

headers = {"Authorization": f"Bearer {token}"}
checks = [
    ("Workspace reachability", f"{host}/api/2.0/clusters/list"),
    ("SQL warehouse API", f"{host}/api/2.0/sql/warehouses"),
    ("Jobs API", f"{host}/api/2.1/jobs/list"),
]

ok = 0
for label, url in checks:
    try:
        r = requests.get(url, headers=headers, timeout=12)
        good = r.status_code in (200, 201)
        if good:
            ok += 1
        print(f"  [{'OK' if good else 'NO'}] {label:<22} HTTP {r.status_code}")
    except requests.RequestException as exc:
        print(f"  [NO] {label:<22} network error: {exc}")

print("\nInterpretation:")
print("  - If clusters/list is 200, auth+workspace are healthy.")
print("  - If SQL warehouse API is 200, SQL/BI path is available.")
print("  - If jobs API is 200, workflow orchestration APIs are available.")
print(f"\nSummary: {ok}/{len(checks)} readiness checks passed.\n")
