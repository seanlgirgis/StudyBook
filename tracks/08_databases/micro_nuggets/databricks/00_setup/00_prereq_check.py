"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 00-00 · Prerequisite Check                                           ║
║  Verify your environment before running any other nugget.                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Checks everything you need is in place:
  1. Python version (≥ 3.8)
  2. Required packages installed (databricks-sql-connector, requests)
  3. Credentials resolved (host + token)
  4. Live connection test (ping the workspace)

WHY THIS MATTERS
────────────────
Databricks uses a different connector than traditional databases.
Instead of a native binary driver, it uses a Python SQL connector that
communicates over HTTPS to a SQL Warehouse endpoint.

This means:
  - No native port to open — everything goes through port 443 (HTTPS)
  - Authentication is via Personal Access Token (PAT), not password
  - The SQL Warehouse is the compute engine (like Snowflake's warehouse)

CREDENTIAL RESOLUTION ORDER
────────────────────────────
  1. Environment variables  DATABRICKS_HOST, DATABRICKS_TOKEN
     → Set by env_setter.ps1 from encrypted secrets
  2. Encrypted secrets file  config/secrets/asuspc.secrets.enc.json
     → Decrypted via StudyBook seed-backed DPAPI system
  3. .env.local file  _infra/env/.env.local
     → Local override (gitignored)

USAGE
─────
    python 00_prereq_check.py

EXPECTED OUTPUT
───────────────
    ── Databricks Prerequisite Check ──────────────────────

      [✓] Python 3.12.4
      [✓] databricks-sql-connector 4.0.5
      [✓] requests 2.32.3

      Credentials resolved:
        Host:   https://dbc-xxxx.cloud.databricks.com
        Token:  dapi*** (present, 20 chars)
        Source: encrypted_secrets

      Testing live connection...
      [✓] Connected!
        User:     john.doe@company.com
        Active:   True
        Workspace: dbc-xxxx.cloud.databricks.com

      All prerequisites met. Ready to run nuggets!
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

# ── Path setup — same two lines at the top of every nugget ───────────────────
sys.path.insert(0, str(Path(__file__).parent.parent))
from _db_connect import get_creds, get_workspace_info

print("\n── Databricks Prerequisite Check ──────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Python version check
#    Databricks SQL Connector requires Python ≥ 3.8.
#    The connector uses pure Python (no C extensions) for the protocol layer,
#    but depends on cryptography (C bindings) for TLS.
# ─────────────────────────────────────────────────────────────────────────────
py_ok = sys.version_info >= (3, 8)
status = "✓" if py_ok else "✗"
print(f"\n  [{status}] Python {sys.version.split()[0]}  (requires ≥ 3.8)")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Package checks
#    databricks-sql-connector — the official Python client
#      - Implements the Databricks SQL protocol over HTTPS
#      - Uses Thrift for serialization (like Hive/Impala JDBC/ODBC)
#      - Supports Python DB-API 2.0 interface (connect, cursor, execute, fetch)
#
#    requests — used for REST API calls (workspace info, cluster management)
#      - Not needed for SQL queries, but used for admin/diagnostic calls
# ─────────────────────────────────────────────────────────────────────────────
for pkg_name, import_name in [
    ("databricks-sql-connector", "databricks.sql"),
    ("requests", "requests"),
]:
    try:
        mod = __import__(import_name.replace("-", "_"))
        version = getattr(mod, "__version__", "unknown")
        print(f"  [✓] {pkg_name} {version}")
    except ImportError:
        print(f"  [✗] {pkg_name} — NOT INSTALLED")
        print(f"      Fix: pip install {pkg_name}")

# ─────────────────────────────────────────────────────────────────────────────
# 3. Credential check
#    Databricks needs TWO things:
#      DATABRICKS_HOST — your workspace URL (e.g. https://dbc-xxxx.cloud.databricks.com)
#      DATABRICKS_TOKEN — a Personal Access Token (PAT)
#
#    What is a PAT?
#      - A long-lived token (starts with "dapi") that authenticates API calls
#      - Created in: User Settings → Developer → Access Tokens → Generate New Token
#      - Unlike passwords, PATs don't expire unless you manually revoke them
#      - Scope: inherits all permissions of the user who created it
#      - Best practice: create a dedicated service account for automation
#
#    Optional: DATABRICKS_HTTP_PATH
#      - The HTTP path to your SQL Warehouse
#      - Format: /sql/1.0/warehouses/<warehouse_id>
#      - Found in: SQL Warehouses → Connection Details → JDBC/ODBC tab
#      - If omitted, defaults to serverless compute path
# ─────────────────────────────────────────────────────────────────────────────
creds = get_creds()
host  = creds.get("DATABRICKS_HOST")
token = creds.get("DATABRICKS_TOKEN")

# Determine which source provided the credentials
source = "unknown"
if os.getenv("DATABRICKS_HOST"):
    source = "environment_variables"
elif token:
    # Try to determine if it came from encrypted secrets
    project_root = Path(__file__).resolve().parent.parent.parent.parent.parent
    if (project_root / "config" / "secrets" / "asuspc.secrets.enc.json").exists():
        source = "encrypted_secrets"
    else:
        source = "env_file"

print("\n  Credentials resolved:")
print(f"    Host:   {host or 'MISSING'}")
if token:
    # Show first 4 chars + length — never expose the full token
    masked = token[:4] + "***" + f" ({len(token)} chars)"
    print(f"    Token:  {masked}")
else:
    print(f"    Token:  MISSING")
print(f"    Source: {source}")

if not host or not token:
    print("\n  [✗] Missing credentials!")
    print("  Fix options:")
    print("    1. Set DATABRICKS_HOST and DATABRICKS_TOKEN as environment variables")
    print("    2. Add them to your encrypted secrets:")
    print("       .\\scripts\\env\\set_secret.ps1 -Machine asuspc -PromptSecretKey DATABRICKS_HOST")
    print("       .\\scripts\\env\\set_secret.ps1 -Machine asuspc -PromptSecretKey DATABRICKS_TOKEN")
    print("    3. Add to _infra/env/.env.local (gitignored):")
    print("       DATABRICKS_HOST=https://dbc-xxxx.cloud.databricks.com")
    print("       DATABRICKS_TOKEN=dapi...")
    sys.exit(1)

# ─────────────────────────────────────────────────────────────────────────────
# 4. Live connection test
#    We use the REST API /api/2.0/current-user/me endpoint because:
#      - It's the fastest way to verify auth works (no SQL overhead)
#      - Returns user metadata: userName, displayName, active status
#      - Works even if no SQL Warehouse is running (pure REST, no compute)
#
#    This is different from the SQL connection — it proves the token is valid
#    and the workspace is reachable, but doesn't test SQL execution.
# ─────────────────────────────────────────────────────────────────────────────
print("\n  Testing live connection...")
try:
    info = get_workspace_info()
    if info:
        print("  [✓] Connected!")
        print(f"    User:     {info.get('userName', 'unknown')}")
        print(f"    Active:   {info.get('active', 'unknown')}")
        print(f"    Probe:    {info.get('_probe', 'current-user/me')}")
        # Extract workspace host from the resolved host
        workspace_host = host.replace("https://", "") if host else "unknown"
        print(f"    Workspace: {workspace_host}")
        print("\n  All prerequisites met. Ready to run nuggets!")
    else:
        print("  [✗] Connection returned no data")
        # Try to diagnose why
        import requests
        test_url = f"{host}/api/2.0/current-user/me"
        test_headers = {"Authorization": f"Bearer {token}"}
        try:
            resp = requests.get(test_url, headers=test_headers, timeout=10)
            print(f"\n  Diagnostic: HTTP {resp.status_code}")
            print(f"  Response: {resp.text[:300]}")
            if resp.status_code == 401:
                print("  → Token is invalid or expired. Regenerate in User Settings.")
            elif resp.status_code == 403:
                print("  → Token lacks permission for /api/2.0/current-user/me.")
            elif resp.status_code == 404:
                print("  → /current-user/me is not enabled on this workspace edition/config.")
                print("    This does NOT necessarily mean host/token are wrong.")
                print("    Use clusters/list fallback probe to confirm auth.")
        except requests.RequestException as e:
            print(f"\n  Diagnostic: Network error — {e}")
            print("  → Check firewall/proxy settings. Can you reach the workspace in a browser?")
        sys.exit(1)
except Exception as e:
    print(f"  [✗] Connection failed: {e}")
    print("\n  Common causes:")
    print("    - Invalid or expired token → regenerate in User Settings")
    print("    - Network/firewall blocking port 443")
    print("    - Workspace URL is incorrect")
    sys.exit(1)

print()
