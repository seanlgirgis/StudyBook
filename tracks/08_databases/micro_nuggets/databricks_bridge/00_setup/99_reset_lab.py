"""
NUGGET 00-99 (Bridge) -- Reset Lab
====================================
Drop all bridge_lab tables (NOT the catalog or schema) so 01_seed_lab.py
can recreate them from scratch.

Safety rules:
  - Only drops objects in nugget_lab.bridge_lab
  - Does NOT touch nugget_lab.default (baseline databricks/ nuggets)
  - Does NOT drop the nugget_lab catalog
  - Requires explicit confirmation flag to run (--confirm)

Usage:
    python 99_reset_lab.py --confirm

Why safe reset matters:
  An idempotent reset lets you:
    1. Reproduce a known-good baseline after a failed experiment
    2. Test your seed script end-to-end
    3. Practice Time Travel demos fresh (clean version history)
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _db_bridge_connect import get_connection, LAB_CATALOG, LAB_SCHEMA

BRIDGE_TABLES = [
    "events_stream",
    "sales_orders",
    "products",
    "customers",
    # DE-pattern and capstone tables created by other nuggets
    "orders_staging",
    "customers_scd2",
    "products_dedupe",
    "incremental_control",
    "late_events_target",
    "data_quality_results",
    "bronze_events",
    "silver_events",
    "gold_daily_summary",
]


def main():
    if "--confirm" not in sys.argv:
        print()
        print("  Reset requires explicit confirmation.")
        print("  Usage: python 99_reset_lab.py --confirm")
        print(f"  This will DROP all tables in {LAB_CATALOG}.{LAB_SCHEMA}")
        sys.exit(0)

    print()
    print("=" * 60)
    print("  Databricks Bridge -- Reset Lab")
    print(f"  Target: {LAB_CATALOG}.{LAB_SCHEMA}")
    print("=" * 60)
    print()

    conn = get_connection()
    dropped = []
    skipped = []

    with conn.cursor() as cur:
        for table in BRIDGE_TABLES:
            fqn = f"{LAB_CATALOG}.{LAB_SCHEMA}.{table}"
            try:
                cur.execute(f"DROP TABLE IF EXISTS {fqn}")
                dropped.append(table)
                print(f"  [DROPPED] {table}")
            except Exception as exc:
                msg = str(exc).splitlines()[0][:60]
                skipped.append((table, msg))
                print(f"  [SKIP]    {table}  =>  {msg}")

    conn.close()

    print()
    print("-" * 60)
    print(f"  Dropped: {len(dropped)}  |  Skipped: {len(skipped)}")
    print("  Run 01_seed_lab.py to recreate tables.")
    print("-" * 60)
    print()


if __name__ == "__main__":
    main()
