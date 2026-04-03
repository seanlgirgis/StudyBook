"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 00-00 · Prerequisite Check                                           ║
║  Verify your environment before running any other nugget.                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Checks everything you need is in place:
  1. Python version (≥ 3.8)
  2. Required packages installed (psycopg2)
  3. Credentials resolved (host, port, user, password, db)
  4. Live connection test (SELECT version())

USAGE
─────
    python 00_prereq_check.py

EXPECTED OUTPUT
───────────────
    ── PostgreSQL Prerequisite Check ────────────────────

      [✓] Python 3.12.9  (requires ≥ 3.8)
      [✓] psycopg2 2.9.9

      Credentials resolved:
        Host:     localhost
        Port:     5432
        User:     de_admin
        DB:       de_telemetry
        Source:   env_file

      Testing live connection...
      [✓] Connected!
        PostgreSQL 16.x

      All prerequisites met. Ready to run nuggets!
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _pg_connect import get_creds, get_creds_source, get_connection

print("\n── PostgreSQL Prerequisite Check ────────────────────")

# 1. Python version
py_ok = sys.version_info >= (3, 8)
status = "✓" if py_ok else "✗"
print(f"\n  [{status}] Python {sys.version.split()[0]}  (requires ≥ 3.8)")

# 2. Package check
try:
    import psycopg2
    version = getattr(psycopg2, "__version__", "unknown")
    print(f"  [✓] psycopg2 {version}")
except ImportError:
    print(f"  [✗] psycopg2 — NOT INSTALLED")
    print(f"      Fix: pip install psycopg2-binary")
    sys.exit(1)

# 3. Credential check
creds = get_creds()
host = creds.get("POSTGRES_HOST")
port = creds.get("POSTGRES_PORT")
user = creds.get("POSTGRES_USER")
dbname = creds.get("POSTGRES_DB")

source = "defaults"
if os.getenv("POSTGRES_HOST"):
    source = "environment_variables"
else:
    source = get_creds_source()

print("\n  Credentials resolved:")
print(f"    Host:     {host}")
print(f"    Port:     {port}")
print(f"    User:     {user}")
print(f"    DB:       {dbname}")
print(f"    Source:   {source}")

# 4. Live connection test
print("\n  Testing live connection...")
try:
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT version()")
        pg_version = cur.fetchone()[0]
    conn.close()
    print(f"  [✓] Connected!")
    # Show just "PostgreSQL 16.x" not the full build string
    short_ver = pg_version.split("(")[0].strip()
    print(f"    {short_ver}")
    print("\n  All prerequisites met. Ready to run nuggets!")
except Exception as e:
    print(f"  [✗] Connection failed: {e}")
    print("\n  Common causes:")
    print("    - PostgreSQL Docker container not running")
    print("      Fix: cd D:\\StudyBook && .\\_infra\\scripts\\infra_up.ps1")
    print("    - Wrong credentials in _infra/env/.env.local")
    print("    - Firewall blocking port 5432")
    sys.exit(1)

print()
