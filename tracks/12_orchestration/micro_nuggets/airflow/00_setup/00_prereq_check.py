"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 00-00 · Prerequisite Check                                           ║
║  Verify your environment before running any other nugget.                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Checks everything you need is in place:
  1. Python version (>= 3.8)
  2. Required packages (requests, apache-airflow-client)
  3. Credentials resolved (host, port, user, password)
  4. Live Airflow API reachability test
  5. Scheduler health check

USAGE
─────
    python 00_prereq_check.py

EXPECTED OUTPUT
───────────────
    -- Airflow Prerequisite Check ---------------------

      [OK] Python 3.12.x  (requires >= 3.8)
      [OK] requests 2.x.x
      [OK] apache-airflow-client (optional)

      Credentials resolved:
        Host:     localhost
        Port:     8082
        User:     airflow
        Source:   defaults

      Testing live connection...
      [OK] Connected!  Airflow 2.8.0

      Scheduler status: healthy

      All prerequisites met. Ready to run nuggets!
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _airflow_connect import get_creds, get_creds_source, check_airflow_reachable, get_airflow_session

print("\n-- Airflow Prerequisite Check ---------------------")

strict = os.getenv("AIRFLOW_NUGGETS_STRICT", "").strip().lower() in {"1", "true", "yes"}

# 1. Python version
py_ok = sys.version_info >= (3, 8)
status = "OK" if py_ok else "FAIL"
print(f"\n  [{status}] Python {sys.version.split()[0]}  (requires >= 3.8)")
if not py_ok:
    print("      Fix: upgrade to Python 3.8+")
    sys.exit(1)

# 2. Package checks
packages = [
    ("requests", "requests", None),
    ("apache-airflow-client", "airflow_client", "optional — needed for typed SDK access"),
]

all_pkgs_ok = True
for pkg_name, import_name, note in packages:
    try:
        mod = __import__(import_name)
        version = getattr(mod, "__version__", "installed")
        tag = "OK" if not note else "OK"
        print(f"  [{tag}] {pkg_name} {version}" + (f"  ({note})" if note else ""))
    except ImportError:
        if note and "optional" in note:
            print(f"  [--] {pkg_name} — not installed  ({note})")
        else:
            print(f"  [FAIL] {pkg_name} — NOT INSTALLED")
            print(f"      Fix: pip install {pkg_name}")
            all_pkgs_ok = False

if not all_pkgs_ok:
    sys.exit(1)

# 3. Credential check
creds = get_creds()
host = creds.get("AIRFLOW_HOST", "localhost")
port = creds.get("AIRFLOW_PORT", "8082")
user = creds.get("AIRFLOW_USER", "airflow")
source = get_creds_source()

print("\n  Credentials resolved:")
print(f"    Host:     {host}")
print(f"    Port:     {port}")
print(f"    User:     {user}")
print(f"    Source:   {source}")

# 4. Live connection test
print("\n  Testing live connection...")
reachable = False
version_or_err = ""
for attempt in range(1, 5):
    reachable, version_or_err = check_airflow_reachable(timeout=8)
    if reachable:
        break
    if attempt < 4:
        time.sleep(3)

if not reachable:
    tag = "FAIL" if strict else "SKIP"
    print(f"  [{tag}] Cannot reach Airflow at http://{host}:{port}")
    print(f"         Error: {version_or_err}")
    print()
    print("  Common causes:")
    print("    - Pipeline Docker stack not running")
    print("      Fix: pwsh D:\\StudyBook\\_infra\\scripts\\infra_up.ps1 -Group pipeline")
    print("    - Wrong port (check .env.local: AIRFLOW_PORT)")
    print("    - Container still starting — wait 30s and retry")
    if strict:
        sys.exit(1)
    print("  [SKIP] Setup checks skipped because Airflow API is not reachable yet.")
    sys.exit(0)

print(f"  [OK] Connected!  Airflow {version_or_err}")

# 5. Scheduler health check
try:
    session, base_url = get_airflow_session()
    resp = session.get(f"{base_url}/api/v1/health", timeout=8)
    if resp.status_code == 200:
        health = resp.json()
        sched = health.get("scheduler", {}).get("status", "unknown")
        meta = health.get("metadatabase", {}).get("status", "unknown")
        sched_ok = sched == "healthy"
        meta_ok = meta == "healthy"
        print(f"  {'[OK]' if sched_ok else '[WARN]'} Scheduler status: {sched}")
        print(f"  {'[OK]' if meta_ok else '[WARN]'} Metadatabase status: {meta}")
        if not sched_ok:
            print("      Note: scheduler may still be starting up (wait ~60s)")
    else:
        print(f"  [WARN] Health endpoint returned HTTP {resp.status_code}")
except Exception as e:
    print(f"  [WARN] Health check skipped: {e}")

print("\n  All prerequisites met. Ready to run nuggets!")
print()
