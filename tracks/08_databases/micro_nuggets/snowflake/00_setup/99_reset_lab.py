"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 00-99 · Reset Lab                                                    ║
║  Run at the VERY END after all nuggets — or between reruns of any nugget.    ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Drops every object the nuggets create, in safe dependency order.
Safe to run multiple times — all statements use IF EXISTS.

TWO MODES
─────────
  python 99_reset_lab.py             → drops all NUGGET_* objects (keeps database)
  python 99_reset_lab.py --nuke      → drops the entire NUGGET_LAB database
                                        (everything gone in one shot — run at the
                                         absolute end when you are fully done)
  python 99_reset_lab.py --dry-run   → prints what would be dropped, does nothing

WHEN TO USE EACH MODE
─────────────────────
  Between nugget reruns:
      python 99_reset_lab.py
      → tables/streams/tasks/stages/formats are dropped
      → NUGGET_LAB database and PUBLIC schema survive
      → run 00_bootstrap.py is NOT needed again after this

  When completely done with the study lab:
      python 99_reset_lab.py --nuke
      → DROP DATABASE NUGGET_LAB CASCADE removes everything at once
      → run 00_bootstrap.py again if you ever want to restart from scratch

CONVENTION
──────────
All objects created by these nuggets are prefixed with  NUGGET_
This makes them trivial to identify and bulk-clean.

DROP ORDER — why it matters
────────────────────────────
  TASK       references a STREAM      → drop TASK first
  STREAM     references a TABLE       → drop STREAM before TABLE
  CLONE      references a parent      → parent can be dropped independently
  STAGE      may be referenced by PIPE→ drop PIPE before STAGE
  FILE FORMAT is independent          → drop any time

  General rule: drop CONSUMERS before PRODUCERS.

OBJECTS COVERED (by folder)
────────────────────────────
  07_streams_and_tasks : NUGGET_CDC_TASK, NUGGET_HEARTBEAT_TASK,
                          NUGGET_ORDERS_STREAM,
                          NUGGET_ORDERS_CLEAN, NUGGET_TASK_LOG
  05_semi_structured   : NUGGET_EVENTS
  03_dml_basics        : NUGGET_ORDERS, NUGGET_ORDERS_STAGING
  02_ddl_basics        : NUGGET_PRODUCTS_CLONE, NUGGET_PRODUCTS,
                          NUGGET_EMPLOYEES, NUGGET_SCHEMA
  04_loading_data      : NUGGET_INTERNAL_STAGE, NUGGET_EXTERNAL_STAGE_PUBLIC,
                          NUGGET_CSV_FORMAT, NUGGET_JSON_FORMAT,
                          NUGGET_PARQUET_FORMAT

EXPECTED OUTPUT (normal run)
─────────────────────────────
    ── Reset Lab ────────────────────────────────────
      [OK]  DROP TASK        IF EXISTS NUGGET_CDC_TASK
      [OK]  DROP TASK        IF EXISTS NUGGET_HEARTBEAT_TASK
      [OK]  DROP STREAM      IF EXISTS NUGGET_ORDERS_STREAM
      [OK]  DROP TABLE       IF EXISTS NUGGET_ORDERS_CLEAN
      [OK]  DROP TABLE       IF EXISTS NUGGET_TASK_LOG
      [OK]  DROP TABLE       IF EXISTS NUGGET_EVENTS
      [OK]  DROP TABLE       IF EXISTS NUGGET_ORDERS_STAGING
      [OK]  DROP TABLE       IF EXISTS NUGGET_ORDERS
      [OK]  DROP TABLE       IF EXISTS NUGGET_PRODUCTS_CLONE
      [OK]  DROP TABLE       IF EXISTS NUGGET_PRODUCTS
      [OK]  DROP TABLE       IF EXISTS NUGGET_EMPLOYEES
      [OK]  DROP SCHEMA      IF EXISTS NUGGET_SCHEMA
      [OK]  DROP STAGE       IF EXISTS NUGGET_INTERNAL_STAGE
      [OK]  DROP STAGE       IF EXISTS NUGGET_EXTERNAL_STAGE_PUBLIC
      [OK]  DROP FILE FORMAT IF EXISTS NUGGET_CSV_FORMAT
      [OK]  DROP FILE FORMAT IF EXISTS NUGGET_JSON_FORMAT
      [OK]  DROP FILE FORMAT IF EXISTS NUGGET_PARQUET_FORMAT

      16/16 objects processed.
      NUGGET_LAB database preserved. Run with --nuke to drop it too.
      Done. Lab is clean.

EXPECTED OUTPUT (--nuke)
─────────────────────────
    ── Reset Lab (NUKE MODE) ────────────────────────
      WARNING: This will DROP DATABASE NUGGET_LAB CASCADE.
               ALL tables, schemas, and objects inside will be destroyed.
               This cannot be undone (no Time Travel on a dropped database
               once the retention window closes).
      Confirm? [yes/no]: yes
      [OK]  DROP DATABASE IF EXISTS NUGGET_LAB
      Database NUGGET_LAB is gone. Run 00_bootstrap.py to start fresh.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _sf_connect import get_connection, LAB_DB

DRY_RUN = "--dry-run" in sys.argv
NUKE    = "--nuke"    in sys.argv

# ─────────────────────────────────────────────────────────────────────────────
# NUKE MODE: drop the entire database in one shot.
# Requires interactive confirmation so it can never run accidentally.
# ─────────────────────────────────────────────────────────────────────────────
if NUKE:
    print(f"\n── Reset Lab (NUKE MODE) ────────────────────────")
    print(f"  WARNING: This will DROP DATABASE {LAB_DB} CASCADE.")
    print(f"           ALL tables, schemas, and objects inside will be destroyed.")
    print(f"           This cannot be undone once the retention window closes.")
    answer = input("\n  Confirm? [yes/no]: ").strip().lower()
    if answer != "yes":
        print("  Aborted.\n")
        sys.exit(0)

    conn = get_connection(_bootstrap=True)   # connect without a database
    with conn.cursor() as cur:
        try:
            cur.execute(f"DROP DATABASE IF EXISTS {LAB_DB}")
            print(f"\n  [OK]  DROP DATABASE {LAB_DB}")
        except Exception as exc:
            print(f"\n  [ERR] DROP DATABASE {LAB_DB}  — {exc}")
    conn.close()
    print(f"\n  Database {LAB_DB} is gone.")
    print(f"  Run 00_bootstrap.py to start fresh.\n")
    sys.exit(0)

# ─────────────────────────────────────────────────────────────────────────────
# Drop statements — ORDER IS IMPORTANT (consumers before producers).
#
# Tier 1 — Tasks (reference streams → must go first)
# Tier 2 — Streams (reference tables → go before tables)
# Tier 3 — Tables (no dependents after tasks/streams are gone)
# Tier 4 — Schemas (must be empty first)
# Tier 5 — Stages and File Formats (independent)
# ─────────────────────────────────────────────────────────────────────────────
DROP_STATEMENTS = [

    # ── Tier 1: Tasks (nugget 07) ─────────────────────────────────────────
    # Drop tasks before streams — a task body may reference a stream.
    # Suspended tasks can still be dropped.
    "DROP TASK        IF EXISTS NUGGET_CDC_TASK",
    "DROP TASK        IF EXISTS NUGGET_HEARTBEAT_TASK",

    # ── Tier 2: Streams (nugget 07) ───────────────────────────────────────
    # Streams reference source tables — drop before dropping source tables.
    "DROP STREAM      IF EXISTS NUGGET_ORDERS_STREAM",

    # ── Tier 3: Tables ────────────────────────────────────────────────────
    # nugget 07 — task and pipeline targets
    "DROP TABLE       IF EXISTS NUGGET_ORDERS_CLEAN",
    "DROP TABLE       IF EXISTS NUGGET_TASK_LOG",

    # nugget 05 — semi-structured
    "DROP TABLE       IF EXISTS NUGGET_EVENTS",

    # nugget 03 — dml basics
    "DROP TABLE       IF EXISTS NUGGET_ORDERS_STAGING",
    "DROP TABLE       IF EXISTS NUGGET_ORDERS",

    # nugget 02 — ddl basics (clone before original — both can be dropped
    # independently, but drop clone first as good hygiene)
    "DROP TABLE       IF EXISTS NUGGET_PRODUCTS_CLONE",
    "DROP TABLE       IF EXISTS NUGGET_PRODUCTS",
    "DROP TABLE       IF EXISTS NUGGET_EMPLOYEES",

    # ── Tier 4: Schemas (nugget 02) ───────────────────────────────────────
    # Only NUGGET_SCHEMA is a custom schema — PUBLIC stays (it's the lab default).
    # Drop schema after all tables inside it are gone.
    "DROP SCHEMA      IF EXISTS NUGGET_SCHEMA",

    # ── Tier 5: Stages (nugget 04) ────────────────────────────────────────
    "DROP STAGE       IF EXISTS NUGGET_INTERNAL_STAGE",
    "DROP STAGE       IF EXISTS NUGGET_EXTERNAL_STAGE_PUBLIC",

    # ── Tier 5: File Formats (nugget 04) ──────────────────────────────────
    # File formats have no dependents at runtime — safe to drop any time.
    "DROP FILE FORMAT IF EXISTS NUGGET_CSV_FORMAT",
    "DROP FILE FORMAT IF EXISTS NUGGET_JSON_FORMAT",
    "DROP FILE FORMAT IF EXISTS NUGGET_PARQUET_FORMAT",
]

# ─────────────────────────────────────────────────────────────────────────────
# Execute
# ─────────────────────────────────────────────────────────────────────────────
conn = get_connection()
label = "(DRY RUN) " if DRY_RUN else ""
print(f"\n── Reset Lab {label}────────────────────────────────")

ok_count  = 0
err_count = 0

with conn.cursor() as cur:
    for stmt in DROP_STATEMENTS:
        display = " ".join(stmt.split())   # collapse extra whitespace for readability
        if DRY_RUN:
            print(f"  [DRY] {display}")
            ok_count += 1
        else:
            try:
                cur.execute(stmt)
                print(f"  [OK]  {display}")
                ok_count += 1
            except Exception as exc:
                print(f"  [ERR] {display}  — {exc}")
                err_count += 1

conn.close()

total = len(DROP_STATEMENTS)
print(f"\n  {ok_count}/{total} objects processed." + (f"  {err_count} error(s)." if err_count else ""))

if DRY_RUN:
    print(f"  (dry run — nothing was dropped)\n")
else:
    print(f"  {LAB_DB} database preserved. Run with --nuke to drop it too.")
    print(f"  Done. Lab is clean.\n")
