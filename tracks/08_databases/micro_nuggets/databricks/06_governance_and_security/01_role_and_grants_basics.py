from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _db_connect import LAB_CATALOG, get_connection

print("\n-- Phase 2 · 06-01 Role and Grants Basics --")

conn = get_connection()
with conn.cursor() as cur:
    cur.execute(f"USE CATALOG {LAB_CATALOG}")
    cur.execute("CREATE SCHEMA IF NOT EXISTS phase2_security")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phase2_security.sales_secure (
          id INT,
          region STRING,
          amount DECIMAL(12,2)
        ) USING DELTA
    """)

    cur.execute("SELECT current_user()")
    me = cur.fetchone()[0]
    print(f"  Current user: {me}")

    try:
        cur.execute("CREATE ROLE IF NOT EXISTS phase2_analyst")
        cur.execute(f"GRANT USAGE ON CATALOG {LAB_CATALOG} TO `phase2_analyst`")
        cur.execute("GRANT USAGE ON SCHEMA phase2_security TO `phase2_analyst`")
        cur.execute("GRANT SELECT ON TABLE phase2_security.sales_secure TO `phase2_analyst`")
        print("  [OK] Role + grants executed.")
    except Exception as exc:
        print("  [INFO] Role/grant DDL was blocked in this workspace.")
        print(f"  Reason: {str(exc)[:220]}")
        print("  This is common on restricted/community setups.")

conn.close()
print("\nDone. Nugget goal: understand minimum least-privilege grant shape.\n")
