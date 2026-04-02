"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 00-99 · Reset Lab                                                    ║
║  Drops all demo objects so any nugget can be re-run cleanly.                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
A cleanup script that removes every object the nuggets create.
Run it whenever you want a fresh start — e.g. before re-running a nugget
you already ran, or to leave your Snowflake account tidy.

Safe to run multiple times. Every statement uses IF EXISTS so nothing
errors if the object is already gone.

Does NOT drop your database or schema — only nugget-prefixed objects.

CONVENTION
──────────
All objects created by these nuggets are prefixed with  NUGGET_
This makes them easy to identify and bulk-clean.

In real project work, teams often use a similar convention:
    raw_         — raw landing tables
    stg_         — staging / cleaned
    fct_ / dim_  — fact and dimension tables (dbt convention)

DROP ORDER MATTERS
──────────────────
Objects have dependencies:
  - A TASK references a STREAM         → drop TASK first
  - A STREAM references a TABLE        → drop STREAM before TABLE
  - A CLONE references the parent      → parent can be dropped independently
  - A STAGE may be referenced by PIPES → drop PIPE before STAGE
  - FILE FORMAT can be dropped any time (not referenced at runtime)

In general: drop consumers before producers.

USAGE
─────
    python 99_reset_lab.py            # actually drops objects
    python 99_reset_lab.py --dry-run  # only prints what would be dropped

EXPECTED OUTPUT (normal run)
─────────────────────────────
    ── Reset Lab ────────────────────────────────
      [OK]  DROP TASK    IF EXISTS NUGGET_CDC_TASK
      [OK]  DROP STREAM  IF EXISTS NUGGET_ORDERS_STREAM
      [OK]  DROP TABLE   IF EXISTS NUGGET_EVENTS
      [OK]  DROP TABLE   IF EXISTS NUGGET_ORDERS_STAGING
      [OK]  DROP TABLE   IF EXISTS NUGGET_ORDERS
      [OK]  DROP TABLE   IF EXISTS NUGGET_PRODUCTS_CLONE
      [OK]  DROP TABLE   IF EXISTS NUGGET_PRODUCTS
      [OK]  DROP TABLE   IF EXISTS NUGGET_EMPLOYEES
      [OK]  DROP SCHEMA  IF EXISTS NUGGET_SCHEMA
      [OK]  DROP STAGE   IF EXISTS NUGGET_INTERNAL_STAGE
      [OK]  DROP FILE FORMAT IF EXISTS NUGGET_CSV_FORMAT

    Done. Lab is clean.

EXPECTED OUTPUT (dry run)
──────────────────────────
    ── Reset Lab (DRY RUN) ───────────────────────
      [DRY] DROP TASK    IF EXISTS NUGGET_CDC_TASK
      [DRY] DROP STREAM  IF EXISTS NUGGET_ORDERS_STREAM
      ...
    Done (dry run — nothing was dropped).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _sf_connect import get_connection

DRY_RUN = "--dry-run" in sys.argv

# ─────────────────────────────────────────────────────────────────────────────
# Drop statements — ORDER IS IMPORTANT (consumers before producers).
#
# Object types and why they exist:
#   TASK       — scheduled SQL job (nugget 07) — may reference a STREAM
#   STREAM     — CDC change log on a table (nugget 07)
#   TABLE      — the core storage object
#   SCHEMA     — container for tables; drop after all tables inside are gone
#   STAGE      — pointer to file storage (internal or S3/Azure/GCS) (nugget 04)
#   FILE FORMAT — reusable format spec for CSV/JSON/PARQUET (nugget 04)
# ─────────────────────────────────────────────────────────────────────────────
DROP_STATEMENTS = [
    # ── nugget 07: streams & tasks ────────────────
    "DROP TASK        IF EXISTS NUGGET_CDC_TASK",
    "DROP STREAM      IF EXISTS NUGGET_ORDERS_STREAM",

    # ── nugget 05: semi-structured ────────────────
    "DROP TABLE       IF EXISTS NUGGET_EVENTS",

    # ── nugget 03: dml basics ─────────────────────
    "DROP TABLE       IF EXISTS NUGGET_ORDERS_STAGING",
    "DROP TABLE       IF EXISTS NUGGET_ORDERS",

    # ── nugget 02: ddl basics ─────────────────────
    "DROP TABLE       IF EXISTS NUGGET_PRODUCTS_CLONE",
    "DROP TABLE       IF EXISTS NUGGET_PRODUCTS",
    "DROP TABLE       IF EXISTS NUGGET_EMPLOYEES",
    "DROP SCHEMA      IF EXISTS NUGGET_SCHEMA",

    # ── nugget 04: loading data ───────────────────
    "DROP STAGE       IF EXISTS NUGGET_INTERNAL_STAGE",
    "DROP FILE FORMAT IF EXISTS NUGGET_CSV_FORMAT",
]

conn = get_connection()
label = "(DRY RUN) " if DRY_RUN else ""
print(f"\n── Reset Lab {label}────────────────────────────")

with conn.cursor() as cur:
    for stmt in DROP_STATEMENTS:
        display = " ".join(stmt.split())   # collapse extra whitespace
        if DRY_RUN:
            print(f"  [DRY] {display}")
        else:
            try:
                cur.execute(stmt)
                print(f"  [OK]  {display}")
            except Exception as exc:
                # Print but continue — best-effort cleanup
                print(f"  [ERR] {display}  — {exc}")

conn.close()

if DRY_RUN:
    print("\n  Done (dry run — nothing was dropped).\n")
else:
    print("\n  Done. Lab is clean.\n")
