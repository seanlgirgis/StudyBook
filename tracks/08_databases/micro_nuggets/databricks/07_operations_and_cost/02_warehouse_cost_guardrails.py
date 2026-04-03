from __future__ import annotations

import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent))
from _db_connect import get_creds

print("\n-- Phase 2 · 07-02 Warehouse Cost Guardrails --")

creds = get_creds()
host = (creds.get("DATABRICKS_HOST") or "").rstrip("/")
token = creds.get("DATABRICKS_TOKEN") or ""

if not host or not token:
    raise SystemExit("Missing DATABRICKS_HOST or DATABRICKS_TOKEN")
if not host.startswith("http"):
    host = f"https://{host}"

url = f"{host}/api/2.0/sql/warehouses"
headers = {"Authorization": f"Bearer {token}"}

try:
    resp = requests.get(url, headers=headers, timeout=15)
    if not resp.ok:
        print(f"  API unavailable: HTTP {resp.status_code}")
        print(f"  Body: {resp.text[:240]}")
        raise SystemExit(0)

    payload = resp.json() if resp.content else {}
    warehouses = payload.get("warehouses", []) if isinstance(payload, dict) else []

    print(f"  Warehouses found: {len(warehouses)}")
    for w in warehouses[:20]:
        name = w.get("name")
        size = w.get("cluster_size")
        auto_stop = w.get("auto_stop_mins")
        spot = w.get("enable_photon")
        guard = "OK" if (auto_stop is not None and int(auto_stop) <= 20) else "CHECK"
        print(f"  - {name} | size={size} | auto_stop={auto_stop} | photon={spot} | {guard}")

    print("\nGuardrail suggestion:")
    print("  - Set auto_stop_mins <= 20 for ad-hoc/dev warehouses.")
    print("  - Separate BI and ETL workloads into different warehouses.")
    print("  - Review large cluster sizes without clear concurrency need.")

except requests.RequestException as exc:
    print(f"  Network/API error: {exc}")

print()
