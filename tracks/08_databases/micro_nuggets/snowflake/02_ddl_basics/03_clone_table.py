"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 02-03 · Zero-Copy Clone                                              ║
║  One of Snowflake's most powerful and unique features.                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Demonstrates zero-copy cloning of a table, shows that the clone is
independent of the source, and inspects storage metrics to understand
how copy-on-write works.

CONCEPTS
────────
What is Zero-Copy Clone?
  CREATE TABLE my_clone CLONE my_source;

  - Instantly creates a copy of a table (or schema, or database).
  - "Zero-copy" means NO DATA IS DUPLICATED at creation time.
  - Snowflake uses micro-partition metadata pointers — the clone shares
    the same underlying immutable micro-partitions as the source.
  - Storage cost = ZERO until data in one diverges from the other.
  - Speed = instant, regardless of table size (TB-scale clones in seconds!).

How copy-on-write works:
  ┌──────────────┐         ┌──────────────┐
  │   SOURCE     │         │   CLONE      │
  │  partition A ├─ shared ─┤  partition A │  ← same physical data
  │  partition B ├─ shared ─┤  partition B │
  └──────────────┘         └──────────────┘

  After you UPDATE rows in the clone, Snowflake writes a NEW micro-partition
  for just the changed rows. Old partitions remain shared. Only new/changed
  data is billed to the clone.

Real DE use cases:
  1. Sandbox production data instantly
       CREATE DATABASE DEV_DB CLONE PROD_DB;   ← full DB clone!
  2. Branch before a risky transform
       CREATE TABLE orders_backup CLONE orders;
       -- run your risky UPDATE/DELETE
       -- if it goes wrong: DROP TABLE orders; ALTER TABLE orders_backup RENAME TO orders;
  3. dbt model testing against a cloned schema
  4. Provide analysts a personal sandbox with no storage cost
  5. Blue/green deployment: clone prod, run migration on clone, swap names

Clone scope — you can clone:
  - TABLE   → CREATE TABLE clone CLONE source
  - SCHEMA  → CREATE SCHEMA clone CLONE source  (all tables inside!)
  - DATABASE → CREATE DATABASE clone CLONE source (everything inside!)

AT / BEFORE clause (time travel clone):
  - Clone a table AS IT WAS at a past point in time:
      CREATE TABLE orders_jan CLONE orders AT (TIMESTAMP => '2024-01-31'::TIMESTAMP);
  - This is covered in depth in nugget 06_time_travel.

TABLE_STORAGE_METRICS view:
  - Shows per-table byte counts: ACTIVE_BYTES, TIME_TRAVEL_BYTES, FAIL_SAFE_BYTES
  - CLONE_GROUP_ID: tables that share physical partitions have the same ID
  - After a clone, both source and clone share a CLONE_GROUP_ID
  - As data diverges, ACTIVE_BYTES grows only for the changed side

USAGE
─────
    python 03_clone_table.py

EXPECTED OUTPUT
───────────────
    ── Zero-Copy Clone ──────────────────────────

      Seeded NUGGET_PRODUCTS with 10 rows.

      Cloning NUGGET_PRODUCTS → NUGGET_PRODUCTS_CLONE ... done (instant!)

      Source rows : 10
      Clone rows  : 10   ← identical at clone time

      Mutating clone: DELETE 3 rows from clone only ...

      After mutation:
        Clone rows  : 7
        Source rows : 10  ← source completely unaffected

      ── Storage metrics ──────────────────────────────────
        TABLE                          ACTIVE_BYTES  CLONE_GROUP_ID
        ------------------------------ ------------- --------------
        NUGGET_PRODUCTS                        81920 <id>
        NUGGET_PRODUCTS_CLONE                      0 <id>
        (clone shows 0 own bytes — still sharing source partitions)

      Key insight: clone storage cost = 0 until data diverges.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _sf_connect import get_connection

conn = get_connection()

print("\n── Zero-Copy Clone ──────────────────────────")

with conn.cursor() as cur:

    # ─────────────────────────────────────────────────────────────────────────
    # 1. Ensure NUGGET_PRODUCTS exists and has data to clone.
    #    TABLE(GENERATOR(ROWCOUNT => n)) — Snowflake's built-in row generator.
    #    SEQ4()    — sequential integer (0, 1, 2 …) per row in the generator.
    #    UNIFORM(a, b, RANDOM()) — uniformly random number in [a, b].
    # ─────────────────────────────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS NUGGET_PRODUCTS (
            product_id   NUMBER AUTOINCREMENT PRIMARY KEY,
            product_name VARCHAR(200) NOT NULL,
            category     VARCHAR(100),
            price        FLOAT
        )
    """)

    # Truncate so re-runs are clean; then seed 10 rows
    cur.execute("TRUNCATE TABLE NUGGET_PRODUCTS")
    cur.execute("""
        INSERT INTO NUGGET_PRODUCTS (product_name, category, price)
        SELECT
            'Product-' || (SEQ4() + 1),
            CASE MOD(SEQ4(), 3)
                WHEN 0 THEN 'Electronics'
                WHEN 1 THEN 'Clothing'
                ELSE        'Food'
            END,
            ROUND(UNIFORM(5.0, 500.0, RANDOM()), 2)
        FROM TABLE(GENERATOR(ROWCOUNT => 10))
    """)

    cur.execute("SELECT COUNT(*) FROM NUGGET_PRODUCTS")
    src_count = cur.fetchone()[0]
    print(f"\n  Seeded NUGGET_PRODUCTS with {src_count} rows.")

    # ─────────────────────────────────────────────────────────────────────────
    # 2. Zero-copy clone — a single DDL statement.
    #    CREATE OR REPLACE makes this script idempotent.
    #    This completes in milliseconds regardless of data volume.
    # ─────────────────────────────────────────────────────────────────────────
    print("\n  Cloning NUGGET_PRODUCTS → NUGGET_PRODUCTS_CLONE ... ", end="", flush=True)
    cur.execute("""
        CREATE OR REPLACE TABLE NUGGET_PRODUCTS_CLONE
        CLONE NUGGET_PRODUCTS
    """)
    print("done (instant!)")

    cur.execute("SELECT COUNT(*) FROM NUGGET_PRODUCTS_CLONE")
    clone_count = cur.fetchone()[0]
    print(f"\n  Source rows : {src_count}")
    print(f"  Clone rows  : {clone_count}   ← identical at clone time")

    # ─────────────────────────────────────────────────────────────────────────
    # 3. Mutate the clone — the source must remain completely unchanged.
    #    This is the copy-on-write trigger: Snowflake writes new micro-partitions
    #    for deleted rows, keeping source partitions untouched.
    # ─────────────────────────────────────────────────────────────────────────
    print("\n  Mutating clone: DELETE 3 rows from clone only ...")
    cur.execute("""
        DELETE FROM NUGGET_PRODUCTS_CLONE
        WHERE product_id IN (
            SELECT product_id FROM NUGGET_PRODUCTS_CLONE
            ORDER BY product_id
            LIMIT 3
        )
    """)

    cur.execute("SELECT COUNT(*) FROM NUGGET_PRODUCTS_CLONE")
    clone_after = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM NUGGET_PRODUCTS")
    src_after = cur.fetchone()[0]

    print(f"\n  After mutation:")
    print(f"    Clone rows  : {clone_after}")
    print(f"    Source rows : {src_after}  ← source completely unaffected")

    # ─────────────────────────────────────────────────────────────────────────
    # 4. Storage metrics
    #    TABLE_STORAGE_METRICS is in INFORMATION_SCHEMA.
    #    ACTIVE_BYTES      — bytes for currently live data
    #    TIME_TRAVEL_BYTES — bytes held for time-travel (deleted/updated rows)
    #    CLONE_GROUP_ID    — tables sharing this ID share physical micro-partitions
    #
    #    Right after cloning:
    #      source ACTIVE_BYTES = some value
    #      clone  ACTIVE_BYTES = 0  (sharing source partitions, paying nothing)
    #    After the DELETE on clone:
    #      clone gains TIME_TRAVEL_BYTES for the 3 deleted rows
    #      but ACTIVE_BYTES may still be 0 until Snowflake recalculates
    # ─────────────────────────────────────────────────────────────────────────
    cur.execute("""
        SELECT table_name,
               active_bytes,
               time_travel_bytes,
               clone_group_id
        FROM   information_schema.table_storage_metrics
        WHERE  table_name IN ('NUGGET_PRODUCTS', 'NUGGET_PRODUCTS_CLONE')
        ORDER  BY table_name
    """)
    storage_rows = cur.fetchall()

print("\n  ── Storage metrics ──────────────────────────────────")
print(f"    {'TABLE':<30} {'ACTIVE_BYTES':>13}  CLONE_GROUP_ID")
print(f"    {'-'*30} {'-'*13}  {'─'*14}")
for tname, active, tt, clone_gid in storage_rows:
    print(f"    {tname:<30} {active:>13,}  {clone_gid or 'N/A'}")
print("    (clone shows 0 own bytes — still sharing source partitions)")

conn.close()
print("\n  Key insight: clone storage cost = 0 until data diverges.")
print("  Run 99_reset_lab.py to drop NUGGET_PRODUCTS_CLONE.\n")
