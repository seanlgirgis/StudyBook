"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 00-00 · Bootstrap — Lab Ground Setup                                 ║
║  Run this ONCE before any other nugget.                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Creates the dedicated lab database and schema that every nugget writes into.
Safe to rerun — all statements use IF NOT EXISTS so nothing is overwritten.

WHY THIS IS NEEDED
──────────────────
Snowflake trial accounts start empty — no databases exist yet (the warehouse
COMPUTE_WH is the only pre-created object).  If you connect without a valid
database, CURRENT_DATABASE() returns NULL and any USE DATABASE command that
references your credentials value fails.

This script is the answer: it creates a clean, isolated workspace called
NUGGET_LAB that every nugget can trust to exist.

WHAT IT CREATES
───────────────
  DATABASE  NUGGET_LAB           ← isolated study workspace
  SCHEMA    NUGGET_LAB.PUBLIC    ← default schema for all nugget objects

DESIGN PRINCIPLES
─────────────────
  - Prefix "NUGGET_" keeps lab objects easy to identify and bulk-drop later.
  - Everything lives in one DB so the reset script (99_reset_lab.py)
    can nuke it cleanly without touching anything else in the account.
  - ACCOUNTADMIN role can create databases — which matches the role your
    trial account defaults to.

AFTER RUNNING THIS
──────────────────
  All subsequent nuggets connect with:
      database = NUGGET_LAB
      schema   = PUBLIC
  _sf_connect.LAB_DB and LAB_SCHEMA constants provide these values.
  You do NOT need to change your encrypted secrets or .env.local.

USAGE
─────
    python 00_bootstrap.py

EXPECTED OUTPUT
───────────────
    ════════════════════════════════════════════
      Snowflake Nuggets — Lab Bootstrap
    ════════════════════════════════════════════

    ── Account info ─────────────────────────────
      Account  : QU00939
      User     : SEANLGIRGIS
      Role     : ACCOUNTADMIN
      Warehouse: COMPUTE_WH  (state: STARTED)

    ── Creating lab objects ──────────────────────
      [✓] DATABASE  NUGGET_LAB       — created
      [✓] SCHEMA    NUGGET_LAB.PUBLIC — created

    ── Smoke test ────────────────────────────────
      [✓] USE DATABASE NUGGET_LAB    — ok
      [✓] USE SCHEMA   PUBLIC        — ok
      [✓] SELECT 1                   — ok

    ════════════════════════════════════════════
      Bootstrap complete.  You are ready.

      Lab database : NUGGET_LAB
      Lab schema   : PUBLIC

      Next step: run 00_prereq_check.py
                 then work through the nuggets in order.
    ════════════════════════════════════════════
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _sf_connect import get_connection, LAB_DB, LAB_SCHEMA

# ── connect WITHOUT specifying a database — avoids the "db doesn't exist" trap
# We pass database=None and schema=None so Snowflake connects at account level.
# ACCOUNTADMIN can then CREATE DATABASE freely.
conn = get_connection(_bootstrap=True)

print()
print("════════════════════════════════════════════")
print("  Snowflake Nuggets — Lab Bootstrap")
print("════════════════════════════════════════════")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Show account context — always good to confirm you're on the right account
# ─────────────────────────────────────────────────────────────────────────────
print("\n── Account info ─────────────────────────────")
with conn.cursor() as cur:
    cur.execute("""
        SELECT CURRENT_ACCOUNT(),
               CURRENT_USER(),
               CURRENT_ROLE(),
               CURRENT_WAREHOUSE()
    """)
    acct, user, role, wh = cur.fetchone()

    # Check warehouse state
    cur.execute("SHOW WAREHOUSES LIKE %s", (wh or "COMPUTE_WH",))
    wh_rows = cur.fetchall()
    wh_cols  = [d[0] for d in cur.description]
    state_idx = wh_cols.index("state")
    wh_state  = wh_rows[0][state_idx] if wh_rows else "UNKNOWN"

print(f"  Account  : {acct}")
print(f"  User     : {user}")
print(f"  Role     : {role}")
print(f"  Warehouse: {wh}  (state: {wh_state})")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Create lab database and schema
#
#    DATA_RETENTION_TIME_IN_DAYS = 1
#      Trial accounts have limited storage — keep time travel short.
#      (Production accounts can use up to 90 days for PERMANENT tables.)
#
#    Why a dedicated database rather than using an existing one?
#      - Clean isolation: nuggets never collide with real project data.
#      - Easy teardown: DROP DATABASE NUGGET_LAB CASCADE removes everything.
#      - Predictable: every learner gets the same environment regardless of
#        what else is in their account.
# ─────────────────────────────────────────────────────────────────────────────
print("\n── Creating lab objects ──────────────────────")

steps = []   # (label, sql, description)

steps.append((
    f"DATABASE  {LAB_DB}",
    f"""
        CREATE DATABASE IF NOT EXISTS {LAB_DB}
        DATA_RETENTION_TIME_IN_DAYS = 1
        COMMENT = 'Snowflake micro-nuggets study lab — safe to drop when done'
    """,
    "created",
))

steps.append((
    f"SCHEMA    {LAB_DB}.{LAB_SCHEMA}",
    f"""
        CREATE SCHEMA IF NOT EXISTS {LAB_DB}.{LAB_SCHEMA}
        COMMENT = 'Default schema for all nugget objects'
    """,
    "created",
))

with conn.cursor() as cur:
    for label, sql, desc in steps:
        try:
            cur.execute(sql)
            print(f"  [✓] {label:<35} — {desc}")
        except Exception as exc:
            print(f"  [✗] {label:<35} — FAILED: {exc}")
            conn.close()
            sys.exit(1)

# ─────────────────────────────────────────────────────────────────────────────
# 3. Smoke test — switch into the lab and run a trivial query
#    This is the same test every nugget will implicitly run at startup.
# ─────────────────────────────────────────────────────────────────────────────
print("\n── Smoke test ────────────────────────────────")
smoke_ok = True
with conn.cursor() as cur:
    tests = [
        (f"USE DATABASE {LAB_DB}",   f"USE DATABASE {LAB_DB}"),
        (f"USE SCHEMA   {LAB_SCHEMA}", f"USE SCHEMA   {LAB_SCHEMA}"),
        ("SELECT 1",                  "SELECT 1"),
    ]
    for label, sql in tests:
        try:
            cur.execute(sql)
            print(f"  [✓] {label:<35} — ok")
        except Exception as exc:
            print(f"  [✗] {label:<35} — {exc}")
            smoke_ok = False

conn.close()

# ─────────────────────────────────────────────────────────────────────────────
# 4. Summary
# ─────────────────────────────────────────────────────────────────────────────
print()
print("════════════════════════════════════════════")
if smoke_ok:
    print("  Bootstrap complete.  You are ready.\n")
    print(f"  Lab database : {LAB_DB}")
    print(f"  Lab schema   : {LAB_SCHEMA}\n")
    print("  Next step: run 00_prereq_check.py")
    print("             then work through the nuggets in order.")
else:
    print("  Bootstrap encountered errors — see above.")
    print("  Fix the issues then rerun this script.")
print("════════════════════════════════════════════")
print()

sys.exit(0 if smoke_ok else 1)
