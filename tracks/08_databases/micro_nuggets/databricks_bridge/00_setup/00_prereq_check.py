"""
NUGGET 00-00 (Bridge) -- Prerequisite Check
============================================
Verify your environment before running any other bridge nugget.

Checks:
  1. Python version (>= 3.8)
  2. Required packages (databricks-sql-connector, requests)
  3. Credential resolution with source identification
  4. Live REST probe (no SQL Warehouse needed)
  5. SQL connection probe (starts warehouse if stopped)

Why this matters:
  Databricks uses HTTPS to a SQL Warehouse -- not a native TCP port.
  A working REST token does NOT guarantee the SQL Warehouse is running.
  This check validates both the auth layer and the compute layer.

Usage:
    python 00_prereq_check.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

# ── Standard two-line path bootstrap used by every bridge nugget ─────────────
sys.path.insert(0, str(Path(__file__).parent.parent))
from _db_bridge_connect import get_creds, get_workspace_info, get_connection, LAB_CATALOG, LAB_SCHEMA

DIVIDER = "-" * 60

print()
print("=" * 60)
print("  Databricks Bridge -- Prerequisite Check")
print("=" * 60)

# ─────────────────────────────────────────────────────────────────────────────
# 1. Python version
#    Databricks SQL Connector requires >= 3.8.
#    The connector communicates over HTTPS using the Thrift protocol,
#    which is used by Hive/Impala too -- this is why the connection string
#    looks different from psycopg2 (PostgreSQL) or snowflake-connector.
# ─────────────────────────────────────────────────────────────────────────────
print()
print("  [1] Python version")
py_ok = sys.version_info >= (3, 8)
mark = "OK" if py_ok else "FAIL"
print(f"      [{mark}] Python {sys.version.split()[0]}  (requires >= 3.8)")
if not py_ok:
    print("      Fix: upgrade to Python 3.8+  https://python.org/downloads")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Required packages
#    databricks-sql-connector  -- Python DB-API 2.0 client for Databricks SQL
#    requests                  -- HTTP client used for REST API probes
# ─────────────────────────────────────────────────────────────────────────────
print()
print("  [2] Required packages")
pkg_ok = True
for pip_name, import_name in [
    ("databricks-sql-connector", "databricks.sql"),
    ("requests", "requests"),
]:
    try:
        import importlib
        mod = importlib.import_module(import_name)
        version = getattr(mod, "__version__", None)
        if version is None:
            # Try parent module for version (e.g., databricks has __version__)
            parent = importlib.import_module(import_name.split(".")[0])
            version = getattr(parent, "__version__", "unknown")
        print(f"      [OK] {pip_name} {version}")
    except ImportError:
        print(f"      [FAIL] {pip_name} -- NOT INSTALLED")
        print(f"             Fix: pip install {pip_name}")
        pkg_ok = False

# ─────────────────────────────────────────────────────────────────────────────
# 3. Credential resolution
#    Databricks needs:
#      DATABRICKS_HOST      -- workspace URL  e.g. https://dbc-xxxx.cloud.databricks.com
#      DATABRICKS_TOKEN     -- Personal Access Token (PAT), starts with "dapi"
#      DATABRICKS_HTTP_PATH -- SQL Warehouse path  e.g. /sql/1.0/warehouses/<id>
#
#    The HTTP path can be auto-discovered from the REST API if not set.
#    PostgreSQL equivalent: host + port + password + ssl_mode
# ─────────────────────────────────────────────────────────────────────────────
print()
print("  [3] Credential resolution")
creds = get_creds()
host  = creds.get("DATABRICKS_HOST")
token = creds.get("DATABRICKS_TOKEN")
http_path = creds.get("DATABRICKS_HTTP_PATH")

source = "unknown"
if os.getenv("DATABRICKS_HOST"):
    source = "environment_variables"
elif token:
    project_root = Path(__file__).resolve().parent.parent.parent.parent.parent
    enc_file = project_root / "config" / "secrets" / "shared.secrets.enc.json"
    source = "encrypted_secrets" if enc_file.exists() else "env_file (.env.local)"

print(f"      Host:      {host or 'MISSING'}")
if token:
    masked = token[:4] + "***" + f"  ({len(token)} chars)"
    print(f"      Token:     {masked}")
else:
    print("      Token:     MISSING")

if http_path:
    print(f"      HTTP Path: {http_path}")
else:
    print("      HTTP Path: not set  (will attempt auto-discovery)")

print(f"      Source:    {source}")

if not host or not token:
    print()
    print("  [FAIL] Missing credentials. Fix options:")
    print("    1. Set environment variables:")
    print("       $env:DATABRICKS_HOST='https://dbc-xxxx.cloud.databricks.com'")
    print("       $env:DATABRICKS_TOKEN='dapi...'")
    print("    2. Add to _infra/env/.env.local (gitignored):")
    print("       DATABRICKS_HOST=https://dbc-xxxx.cloud.databricks.com")
    print("       DATABRICKS_TOKEN=dapi...")
    sys.exit(1)

# ─────────────────────────────────────────────────────────────────────────────
# 4. Live REST probe
#    Validates the token and workspace reachability WITHOUT starting compute.
#    /api/2.0/current-user/me returns user metadata.
#    Falls back to /api/2.0/clusters/list if the first endpoint is blocked.
#
#    PostgreSQL equivalent: pg_isready -h host -p port
# ─────────────────────────────────────────────────────────────────────────────
print()
print("  [4] Live REST probe")
try:
    info = get_workspace_info()
    if info:
        print("      [OK] REST probe successful")
        if "userName" in info:
            print(f"           User:   {info.get('userName', 'unknown')}")
            print(f"           Active: {info.get('active', 'unknown')}")
        else:
            print(f"           Probe:  {info.get('_probe', 'unknown')}")
            print(f"           Active: {info.get('workspace_reachable', 'unknown')}")
    else:
        print("      [FAIL] REST probe returned no data")
        print("             Check token validity and workspace URL")
        sys.exit(1)
except Exception as exc:
    print(f"      [FAIL] REST probe failed: {exc}")
    sys.exit(1)

# ─────────────────────────────────────────────────────────────────────────────
# 5. SQL connection probe
#    Opens an actual SQL Warehouse connection and runs SELECT 1.
#    This MAY start a stopped warehouse (cold start can take 30-90 seconds).
#
#    PostgreSQL equivalent: psql -c "SELECT 1"
# ─────────────────────────────────────────────────────────────────────────────
print()
print("  [5] SQL connection probe  (may start warehouse if stopped...)")
try:
    conn = get_connection(_bootstrap=True)
    with conn.cursor() as cur:
        cur.execute("SELECT 1 AS probe")
        row = cur.fetchone()
    conn.close()
    if row and row[0] == 1:
        print("      [OK] SQL Warehouse connection successful")
        print(f"           Target: {LAB_CATALOG}.{LAB_SCHEMA}")
    else:
        print("      [FAIL] Unexpected result from SELECT 1")
        sys.exit(1)
except Exception as exc:
    print(f"      [FAIL] SQL connection failed: {exc}")
    print()
    print("      Common causes:")
    print("        - SQL Warehouse is stopped and auto-resume is disabled")
    print("        - HTTP path is wrong (check SQL Warehouses > Connection Details)")
    print("        - Token lacks USE CATALOG / USE SCHEMA permissions")
    sys.exit(1)

print()
print(DIVIDER)
print("  All prerequisites met. Run 01_seed_lab.py next.")
print(DIVIDER)
print()
