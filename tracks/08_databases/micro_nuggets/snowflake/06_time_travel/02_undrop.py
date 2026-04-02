"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 06-02 · UNDROP — Restore Dropped Objects                             ║
║  DROP TABLE is not permanent — until the retention window closes.            ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Shows that DROP TABLE / DROP SCHEMA / DROP DATABASE do not immediately
destroy data in Snowflake. UNDROP restores the object and all its data
as long as the Time Travel window is still open.

CONCEPTS
────────
UNDROP in Snowflake:
  When you DROP a table (or schema, or database), Snowflake marks it
  "deleted" but keeps the underlying micro-partition data alive for the
  Time Travel retention window.

  UNDROP TABLE   my_table;
  UNDROP SCHEMA  my_schema;
  UNDROP DATABASE my_db;

  Constraints:
  - Works only within DATA_RETENTION_TIME_IN_DAYS of the DROP.
  - If a NEW object with the same name was created after the DROP,
    UNDROP will fail — you must DROP or rename the new object first.
  - UNDROP restores the table at the same path (db.schema.table).
  - All data, column definitions, and constraints are restored.
  - Clustering keys and column comments are also restored.

What about TRUNCATE vs DROP?
  TRUNCATE: empties the table, table definition stays → just restore from
            Time Travel AT (OFFSET => -n) (covered in nugget 06-01).
  DROP:     removes the table object → use UNDROP.

UNDROP scope:
  TABLE    → single table
  SCHEMA   → schema + ALL tables inside it (!)
  DATABASE → database + ALL schemas + ALL tables inside it (!!)
  This makes UNDROP very powerful for disaster recovery.

Name conflict after UNDROP:
  Scenario: you dropped orders_v1, created orders_v2, then try UNDROP orders_v1.
  Both would have the name "orders" — conflict.
  Resolution:
    ALTER TABLE orders RENAME TO orders_v2_current;   -- rename new one
    UNDROP TABLE orders;                               -- restores orders_v1

SHOW TABLES HISTORY:
  Shows both current AND recently dropped tables:
    SHOW TABLES HISTORY;
    SHOW TABLES HISTORY LIKE 'NUGGET%';
  Dropped tables appear with a "dropped_on" column.
  Useful for discovering what was dropped and when.

Fail-Safe (beyond Time Travel):
  After the Time Travel window expires, data enters a 7-day Fail-Safe period.
  During Fail-Safe: only Snowflake support can recover the data (not you).
  After Fail-Safe: permanently gone.
  Always set DATA_RETENTION_TIME_IN_DAYS > 0 on important tables.

USAGE
─────
    python 02_undrop.py

EXPECTED OUTPUT
───────────────
    ── UNDROP — Restore Dropped Objects ─────────

      Created NUGGET_PRODUCTS with 5 rows.

      ── Step 1: DROP the table ─────────────────────────
        DROP TABLE NUGGET_PRODUCTS ...
        Confirm — does NUGGET_PRODUCTS exist?  NO (it is dropped)

      ── Step 2: SHOW TABLES HISTORY ─────────────────────
        name                kind    dropped_on
        ------------------- ------- -------------------------
        NUGGET_PRODUCTS      TABLE   2024-01-17 10:30:12.000
        (shows dropped tables within retention window)

      ── Step 3: UNDROP ──────────────────────────────────
        UNDROP TABLE NUGGET_PRODUCTS ...
        Confirm — does NUGGET_PRODUCTS exist?  YES (restored!)
        Row count after UNDROP: 5  ← all data is back

      ── Step 4: UNDROP a schema (demo) ──────────────────
        Created NUGGET_TEMP_SCHEMA with table NUGGET_TEMP_TABLE (3 rows)
        Dropped NUGGET_TEMP_SCHEMA ...
        UNDROP SCHEMA NUGGET_TEMP_SCHEMA ...
        Table in restored schema: NUGGET_TEMP_TABLE (3 rows) ← schema + contents restored

      Key insight: DROP is reversible within the retention window.
                   Set DATA_RETENTION_TIME_IN_DAYS on important tables.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _sf_connect import get_connection

conn = get_connection(autocommit=True)

print("\n── UNDROP — Restore Dropped Objects ─────────")


def table_exists(cur, name: str) -> bool:
    cur.execute(f"SHOW TABLES LIKE '{name}'")
    return bool(cur.fetchone())


def schema_exists(cur, name: str) -> bool:
    cur.execute(f"SHOW SCHEMAS LIKE '{name}'")
    return bool(cur.fetchone())


with conn.cursor() as cur:

    # ─────────────────────────────────────────────────────────────────────────
    # 0. Seed: create NUGGET_PRODUCTS with data
    # ─────────────────────────────────────────────────────────────────────────
    cur.execute("""
        CREATE OR REPLACE TABLE NUGGET_PRODUCTS (
            product_id   NUMBER,
            product_name VARCHAR(200),
            price        FLOAT
        )
        DATA_RETENTION_TIME_IN_DAYS = 1
    """)
    cur.execute("""
        INSERT INTO NUGGET_PRODUCTS VALUES
            (1, 'Widget Alpha',  29.99),
            (2, 'Widget Beta',   49.99),
            (3, 'Gadget Pro',    99.99),
            (4, 'Gadget Lite',   59.99),
            (5, 'Super Gadget', 199.99)
    """)
    cur.execute("SELECT COUNT(*) FROM NUGGET_PRODUCTS")
    print(f"\n  Created NUGGET_PRODUCTS with {cur.fetchone()[0]} rows.")

    # ─────────────────────────────────────────────────────────────────────────
    # 1. DROP the table — simulates an accident
    # ─────────────────────────────────────────────────────────────────────────
    print("\n  ── Step 1: DROP the table ─────────────────────────")
    print("    DROP TABLE NUGGET_PRODUCTS ...")
    cur.execute("DROP TABLE NUGGET_PRODUCTS")

    exists = table_exists(cur, "NUGGET_PRODUCTS")
    print(f"    Confirm — does NUGGET_PRODUCTS exist?  {'YES' if exists else 'NO (it is dropped)'}")

    # ─────────────────────────────────────────────────────────────────────────
    # 2. SHOW TABLES HISTORY — see the dropped table in history
    #    The HISTORY keyword includes objects dropped within the retention window.
    # ─────────────────────────────────────────────────────────────────────────
    print("\n  ── Step 2: SHOW TABLES HISTORY ─────────────────────")
    cur.execute("SHOW TABLES HISTORY LIKE 'NUGGET_PRODUCTS'")
    hist_rows = cur.fetchall()
    hist_cols = [d[0] for d in cur.description]

    name_idx    = hist_cols.index("name")
    kind_idx    = hist_cols.index("kind")
    dropped_idx = hist_cols.index("dropped_on") if "dropped_on" in hist_cols else None

    print(f"    {'name':<22}  {'kind':<8}  dropped_on")
    print(f"    {'─'*22}  {'─'*8}  {'─'*25}")
    for row in hist_rows:
        dropped = str(row[dropped_idx])[:25] if dropped_idx is not None else "N/A"
        print(f"    {row[name_idx]:<22}  {row[kind_idx]:<8}  {dropped}")

    if not hist_rows:
        print("    (no dropped tables found — they may expire from history quickly)")

    # ─────────────────────────────────────────────────────────────────────────
    # 3. UNDROP — restore the table
    # ─────────────────────────────────────────────────────────────────────────
    print("\n  ── Step 3: UNDROP ──────────────────────────────────")
    print("    UNDROP TABLE NUGGET_PRODUCTS ...")
    try:
        cur.execute("UNDROP TABLE NUGGET_PRODUCTS")
        exists = table_exists(cur, "NUGGET_PRODUCTS")
        print(f"    Confirm — does NUGGET_PRODUCTS exist?  {'YES (restored!)' if exists else 'NO — UNDROP failed'}")

        if exists:
            cur.execute("SELECT COUNT(*) FROM NUGGET_PRODUCTS")
            count = cur.fetchone()[0]
            print(f"    Row count after UNDROP: {count}  ← all data is back")
    except Exception as exc:
        print(f"    UNDROP failed: {exc}")

    # ─────────────────────────────────────────────────────────────────────────
    # 4. UNDROP SCHEMA — restores the schema AND everything inside it
    #    Creating a temp schema to demonstrate schema-level UNDROP.
    # ─────────────────────────────────────────────────────────────────────────
    print("\n  ── Step 4: UNDROP a schema ─────────────────────────")
    try:
        # Create a temp schema with a table
        cur.execute("""
            CREATE OR REPLACE SCHEMA NUGGET_TEMP_SCHEMA
            DATA_RETENTION_TIME_IN_DAYS = 1
        """)
        cur.execute("USE SCHEMA NUGGET_TEMP_SCHEMA")
        cur.execute("""
            CREATE TABLE NUGGET_TEMP_TABLE (id NUMBER, val VARCHAR(50))
            DATA_RETENTION_TIME_IN_DAYS = 1
        """)
        cur.execute("INSERT INTO NUGGET_TEMP_TABLE VALUES (1,'a'),(2,'b'),(3,'c')")
        print("    Created NUGGET_TEMP_SCHEMA with table NUGGET_TEMP_TABLE (3 rows)")

        # Drop the entire schema
        cur.execute("USE SCHEMA PUBLIC")
        cur.execute("DROP SCHEMA NUGGET_TEMP_SCHEMA")
        print("    Dropped NUGGET_TEMP_SCHEMA ...")

        # Undrop it
        cur.execute("UNDROP SCHEMA NUGGET_TEMP_SCHEMA")
        print("    UNDROP SCHEMA NUGGET_TEMP_SCHEMA ...")

        # Verify the table inside it came back too
        cur.execute("SELECT COUNT(*) FROM NUGGET_TEMP_SCHEMA.NUGGET_TEMP_TABLE")
        count = cur.fetchone()[0]
        print(f"    Table in restored schema: NUGGET_TEMP_TABLE ({count} rows) ← schema + contents restored")

        # Clean up temp schema
        cur.execute("DROP SCHEMA IF EXISTS NUGGET_TEMP_SCHEMA")

    except Exception as exc:
        print(f"    Schema UNDROP demo: {exc}")

conn.close()
print("\n  Key insight: DROP is reversible within the retention window.")
print("               Set DATA_RETENTION_TIME_IN_DAYS on important tables.\n")
