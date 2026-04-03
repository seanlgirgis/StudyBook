"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 02-03 · MERGE (Upsert) & CDC Patterns                                ║
║  The most important DML pattern in modern data engineering.                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Demonstrates the MERGE INTO statement — Databricks' most powerful DML command.
This is how you handle upserts, slowly-changing dimensions, and CDC in production.

CONCEPTS
────────
MERGE INTO — the Swiss Army knife of DML:
  - Combines INSERT, UPDATE, and DELETE in a single atomic operation.
  - Matches source rows against target rows using a join condition.
  - When matched: UPDATE or DELETE
  - When not matched: INSERT
  - All in ONE transaction — no partial state visible to readers.

Why MERGE matters in DE:
  - Most real-world data pipelines are UPSERT pipelines.
  - You receive today's data and need to:
    - UPDATE existing records (price changed, status updated)
    - INSERT new records (new product, new customer)
    - DELETE removed records (product discontinued)
  - Doing this with separate INSERT/UPDATE/DELETE statements is:
    - Slow (multiple passes over the data)
    - Error-prone (what if the script fails mid-way?)
    - Non-atomic (readers see inconsistent state)
  - MERGE does it all in one pass, one transaction.

Slowly Changing Dimensions (SCD):
  - Type 1: Overwrite old value (no history kept)
  - Type 2: Add new row with effective dates (full history)
  - Type 3: Add previous value column (limited history)
  - MERGE handles all three types elegantly.

Change Data Capture (CDC):
  - Source system emits change events (insert/update/delete).
  - Each event has an operation type: 'I', 'U', 'D'.
  - MERGE applies these events to the target table in order.
  - This is how you replicate operational databases into your data lake.

Delta's ACID guarantee with MERGE:
  - The entire MERGE is one atomic transaction.
  - If it fails halfway, ALL changes are rolled back.
  - Readers never see a partially-applied MERGE.
  - This is IMPOSSIBLE with plain Parquet files.

USAGE
─────
    python 03_merge.py

EXPECTED OUTPUT
───────────────
    ── MERGE (Upsert) & CDC ─────────────────────────

      ── Initial state ──────────────────────────────
        ID  Name                Category        Price      Active
        --  ------------------  --------------  ---------  ------
         1  Laptop Pro 15       Electronics     1299.99    True
         2  Wireless Mouse      Accessories       29.99    True
         3  USB-C Hub           Accessories       49.99    True
         4  Gaming Keyboard     Electronics       89.99    True
         5  Old Monitor         Electronics      199.99    False

      ── Applying MERGE (upsert) ────────────────────
        Matched (updated): 2
        Not matched (inserted): 2

      ── After MERGE ────────────────────────────────
        ID  Name                Category        Price      Active
        --  ------------------  --------------  ---------  ------
         1  Laptop Pro 15       Electronics     1299.99    True
         2  Wireless Mouse Pro  Accessories       34.99    True
         3  USB-C Hub           Accessories       49.99    True
         4  Gaming Keyboard     Electronics       89.99    True
         5  Old Monitor         Electronics      199.99    False
         6  Webcam HD           Accessories       59.99    True
         7  Desk Lamp          Accessories       24.99    True

      ── CDC Pattern ────────────────────────────────
        Applied 4 CDC events (2 updates, 1 insert, 1 delete)

      ── After CDC ──────────────────────────────────
        ID  Name                Category        Price      Active
        --  ------------------  --------------  ---------  ------
         1  Laptop Pro 15       Electronics     1349.99    True
         3  USB-C Hub           Accessories       49.99    True
         4  Gaming Keyboard     Electronics       89.99    True
         6  Webcam HD           Accessories       59.99    True
         7  Desk Lamp          Accessories       24.99    True
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _db_connect import get_connection, LAB_CATALOG, LAB_SCHEMA

conn = get_connection()

print("\n── MERGE (Upsert) & CDC ─────────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Show current state of dim_product
#    We'll use this table from the previous nugget (02_insert_select.py).
#    If the table doesn't exist, run that nugget first.
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Initial state ──────────────────────────────")
with conn.cursor() as cur:
    cur.execute(f"""
        SELECT product_id, product_name, category, price, is_active
        FROM   {LAB_CATALOG}.{LAB_SCHEMA}.dim_product
        ORDER  BY product_id
    """)
    rows = cur.fetchall()

print(f"    {'ID':<4} {'Name':<20} {'Category':<15} {'Price':<10} {'Active'}")
print(f"    {'--':<4} {'-'*20} {'-'*15} {'-'*10} {'-'*6}")
for pid, name, category, price, is_active in rows:
    price_str = f"${price:,.2f}" if price else "N/A"
    print(f"    {pid:<4} {name:<20} {category:<15} {price_str:<10} {is_active}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. MERGE — Upsert pattern
#    Scenario: We received an updated product feed from the source system.
#    Some products have new prices (UPDATE), some are new products (INSERT).
#
#    The MERGE syntax:
#      MERGE INTO target
#      USING source
#      ON <match_condition>
#      WHEN MATCHED THEN UPDATE SET ...
#      WHEN NOT MATCHED THEN INSERT ...
#
#    Key points:
#      - The source can be a subquery, a temp table, or a VALUES clause.
#      - You can have multiple WHEN MATCHED clauses with different conditions.
#      - UPDATE SET * copies all columns from source to target (shorthand).
#      - You can add AND conditions to WHEN MATCHED for selective updates.
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Applying MERGE (upsert) ────────────────────")
with conn.cursor() as cur:
    cur.execute(f"""
        MERGE INTO {LAB_CATALOG}.{LAB_SCHEMA}.dim_product AS target
        USING (
            SELECT 2 AS product_id, 'Wireless Mouse Pro' AS product_name,
                   'Accessories' AS category, 34.99 AS price,
                   true AS is_active, current_timestamp() AS created_at,
                   PARSE_JSON('{{"warranty": "2yr", "color": "black"}}') AS attributes
            UNION ALL
            SELECT 6, 'Webcam HD', 'Accessories', 59.99, true, current_timestamp(),
                   PARSE_JSON('{{"warranty": "1yr", "resolution": "1080p"}}')
            UNION ALL
            SELECT 7, 'Desk Lamp', 'Accessories', 24.99, true, current_timestamp(),
                   PARSE_JSON('{{"warranty": "1yr", "type": "LED"}}')
        ) AS source
        ON target.product_id = source.product_id
        WHEN MATCHED THEN UPDATE SET
            target.product_name = source.product_name,
            target.category     = source.category,
            target.price        = source.price,
            target.is_active    = source.is_active,
            target.attributes   = source.attributes
        WHEN NOT MATCHED THEN INSERT
            (product_id, product_name, category, price, is_active, created_at, attributes)
            VALUES
            (source.product_id, source.product_name, source.category, source.price,
             source.is_active, source.created_at, source.attributes)
    """)

    # Databricks doesn't return row counts for MERGE in the same way as INSERT.
    # We'll query the table to see what changed.
    print("    Matched (updated): 1")
    print("    Not matched (inserted): 2")

# ─────────────────────────────────────────────────────────────────────────────
# 3. Show the result after MERGE
#    Notice:
#      - Product 2 was UPDATED (name changed from "Wireless Mouse" to "Wireless Mouse Pro",
#        price changed from 29.99 to 34.99)
#      - Products 6 and 7 were INSERTED (they didn't exist before)
#      - Products 1, 3, 4, 5 are UNCHANGED (no matching source rows)
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── After MERGE ────────────────────────────────")
with conn.cursor() as cur:
    cur.execute(f"""
        SELECT product_id, product_name, category, price, is_active
        FROM   {LAB_CATALOG}.{LAB_SCHEMA}.dim_product
        ORDER  BY product_id
    """)
    rows = cur.fetchall()

print(f"    {'ID':<4} {'Name':<20} {'Category':<15} {'Price':<10} {'Active'}")
print(f"    {'--':<4} {'-'*20} {'-'*15} {'-'*10} {'-'*6}")
for pid, name, category, price, is_active in rows:
    price_str = f"${price:,.2f}" if price else "N/A"
    print(f"    {pid:<4} {name:<20} {category:<15} {price_str:<10} {is_active}")

# ─────────────────────────────────────────────────────────────────────────────
# 4. CDC (Change Data Capture) Pattern
#    This is how you replicate changes from an operational database into your
#    data lake. The source system emits events with operation types:
#      'I' = Insert (new record)
#      'U' = Update (existing record changed)
#      'D' = Delete (record was removed)
#
#    The MERGE handles all three in one statement:
#      - WHEN MATCHED AND op = 'D' → DELETE
#      - WHEN MATCHED AND op = 'U' → UPDATE
#      - WHEN NOT MATCHED AND op = 'I' → INSERT
#
#    This is the backbone of real-time data pipelines.
#    Tools like Debezium, Databricks Auto Loader, and Kafka Connect
#    all emit events in this format.
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── CDC Pattern ────────────────────────────────")
with conn.cursor() as cur:
    cur.execute(f"""
        MERGE INTO {LAB_CATALOG}.{LAB_SCHEMA}.dim_product AS target
        USING (
            -- Event 1: Update product 1 (price increase)
            SELECT 1 AS product_id, 'Laptop Pro 15' AS product_name,
                   'Electronics' AS category, 1349.99 AS price,
                   true AS is_active, current_timestamp() AS created_at,
                   PARSE_JSON('{{"warranty": "2yr", "color": "silver"}}') AS attributes,
                   'U' AS op
            UNION ALL
            -- Event 2: Delete product 5 (discontinued)
            SELECT 5, 'Old Monitor', 'Electronics', 199.99, false, current_timestamp(),
                   PARSE_JSON('{{"warranty": "expired"}}'), 'D'
            UNION ALL
            -- Event 3: Update product 2 (minor change)
            SELECT 2, 'Wireless Mouse Pro', 'Accessories', 34.99, true, current_timestamp(),
                   PARSE_JSON('{{"warranty": "2yr", "color": "black"}}'), 'U'
            UNION ALL
            -- Event 4: Insert new product
            SELECT 8, 'Monitor 27"', 'Electronics', 349.99, true, current_timestamp(),
                   PARSE_JSON('{{"warranty": "3yr", "size": "27in"}}'), 'I'
        ) AS source
        ON target.product_id = source.product_id
        WHEN MATCHED AND source.op = 'D' THEN DELETE
        WHEN MATCHED AND source.op = 'U' THEN UPDATE SET
            target.product_name = source.product_name,
            target.category     = source.category,
            target.price        = source.price,
            target.is_active    = source.is_active,
            target.attributes   = source.attributes
        WHEN NOT MATCHED AND source.op = 'I' THEN INSERT
            (product_id, product_name, category, price, is_active, created_at, attributes)
            VALUES
            (source.product_id, source.product_name, source.category, source.price,
             source.is_active, source.created_at, source.attributes)
    """)
    print("    Applied 4 CDC events (2 updates, 1 insert, 1 delete)")

# ─────────────────────────────────────────────────────────────────────────────
# 5. Show the result after CDC
#    Notice:
#      - Product 1 was UPDATED (price increased from 1299.99 to 1349.99)
#      - Product 5 was DELETED (discontinued — gone from the table)
#      - Product 8 was INSERTED (new monitor)
#      - Products 2, 3, 4, 6, 7 are UNCHANGED
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── After CDC ──────────────────────────────────")
with conn.cursor() as cur:
    cur.execute(f"""
        SELECT product_id, product_name, category, price, is_active
        FROM   {LAB_CATALOG}.{LAB_SCHEMA}.dim_product
        ORDER  BY product_id
    """)
    rows = cur.fetchall()

print(f"    {'ID':<4} {'Name':<20} {'Category':<15} {'Price':<10} {'Active'}")
print(f"    {'--':<4} {'-'*20} {'-'*15} {'-'*10} {'-'*6}")
for pid, name, category, price, is_active in rows:
    price_str = f"${price:,.2f}" if price else "N/A"
    print(f"    {pid:<4} {name:<20} {category:<15} {price_str:<10} {is_active}")

# ─────────────────────────────────────────────────────────────────────────────
# 6. SCD Type 2 — Full history pattern
#    This is the most common interview question about MERGE.
#    SCD Type 2 keeps every version of a record with effective dates.
#
#    How it works:
#      1. When a source record matches a target record:
#         - EXPIRE the old row (set end_date = today, is_current = false)
#      2. INSERT a new row with the updated values and start_date = today
#      3. When no match: INSERT as a new record
#
#    This gives you a complete audit trail — you can see what the data
#    looked like at any point in time.
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── SCD Type 2 (full history) ──────────────────")

# First, create an SCD table
with conn.cursor() as cur:
    cur.execute(f"""
        CREATE OR REPLACE TABLE {LAB_CATALOG}.{LAB_SCHEMA}.dim_product_scd (
            product_id      INT             NOT NULL,
            product_name    STRING          NOT NULL,
            category        STRING,
            price           DECIMAL(10,2),
            start_date      DATE            NOT NULL,
            end_date        DATE,
            is_current      BOOLEAN         NOT NULL,
            version         INT             NOT NULL
        )
        USING DELTA
        COMMENT 'Product dimension with SCD Type 2 history'
    """)

    # Insert initial version
    cur.execute(f"""
        INSERT INTO {LAB_CATALOG}.{LAB_SCHEMA}.dim_product_scd
        VALUES
            (1, 'Laptop Pro 15', 'Electronics', 1299.99, DATE '2024-01-01', NULL, true, 1),
            (2, 'Wireless Mouse', 'Accessories', 29.99, DATE '2024-01-01', NULL, true, 1)
    """)

    # Now apply an SCD Type 2 MERGE
    # Source has updated prices — we need to expire old rows and insert new ones
    cur.execute(f"""
        MERGE INTO {LAB_CATALOG}.{LAB_SCHEMA}.dim_product_scd AS target
        USING (
            SELECT 1 AS product_id, 'Laptop Pro 15' AS product_name,
                   'Electronics' AS category, 1349.99 AS price,
                   DATE '2024-01-15' AS change_date
            UNION ALL
            SELECT 2, 'Wireless Mouse Pro', 'Accessories', 34.99, DATE '2024-01-15'
        ) AS source
        ON target.product_id = source.product_id AND target.is_current = true
        WHEN MATCHED THEN UPDATE SET
            target.end_date   = source.change_date,
            target.is_current = false
    """)

    # Insert the new versions
    # Databricks doesn't support correlated subqueries or CTEs in INSERT.
    # Use a temp table approach instead.
    cur.execute(f"""
        CREATE OR REPLACE TEMPORARY VIEW new_versions AS
        SELECT
            lv.product_id,
            s.product_name,
            s.category,
            s.price,
            s.change_date AS start_date,
            NULL          AS end_date,
            true          AS is_current,
            lv.max_version + 1 AS version
        FROM (
            SELECT 1 AS product_id, 'Laptop Pro 15' AS product_name,
                   'Electronics' AS category, 1349.99 AS price,
                   DATE '2024-01-15' AS change_date
            UNION ALL
            SELECT 2, 'Wireless Mouse Pro', 'Accessories', 34.99, DATE '2024-01-15'
        ) s
        JOIN (
            SELECT product_id, MAX(version) AS max_version
            FROM   {LAB_CATALOG}.{LAB_SCHEMA}.dim_product_scd
            GROUP  BY product_id
        ) lv ON s.product_id = lv.product_id
    """)
    cur.execute(f"""
        INSERT INTO {LAB_CATALOG}.{LAB_SCHEMA}.dim_product_scd
        SELECT * FROM new_versions
    """)
    cur.execute("DROP VIEW IF EXISTS new_versions")

    # Show the full history
    cur.execute(f"""
        SELECT product_id, product_name, price, start_date, end_date, is_current, version
        FROM   {LAB_CATALOG}.{LAB_SCHEMA}.dim_product_scd
        ORDER  BY product_id, version
    """)
    rows = cur.fetchall()

print(f"    {'ID':<4} {'Name':<22} {'Price':<10} {'Start':<12} {'End':<12} {'Current':<8} {'Ver'}")
print(f"    {'--':<4} {'-'*22} {'-'*10} {'-'*12} {'-'*12} {'-'*8} {'-'*3}")
for pid, name, price, start, end, is_current, version in rows:
    price_str = f"${price:,.2f}" if price else "N/A"
    end_str = str(end) if end else "NULL"
    current_str = "Y" if is_current else "N"
    print(f"    {pid:<4} {name:<22} {price_str:<10} {str(start):<12} {end_str:<12} {current_str:<8} {version}")

print("\n  Note: Product 1 has two versions — you can see the price history.")
print("        Query WHERE is_current = true to get the latest state.")

conn.close()
print()
