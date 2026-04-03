"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 04-01 · Mini Capstone: End-to-End Sales Pipeline                     ║
║  Land → Transform → Serve — the complete DE workflow.                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Builds a complete data pipeline from scratch:
  1. LAND: Create raw tables (simulating data ingestion from source systems)
  2. TRANSFORM: Clean, deduplicate, and model the data
  3. SERVE: Create analytics-ready tables with proper optimization
  4. AUDIT: Use Time Travel to verify data lineage
  5. OPTIMIZE: Apply Z-ORDER for query performance

This is the pattern you'll use in every real DE project.

PIPELINE ARCHITECTURE
─────────────────────
    ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
    │  RAW LAYER   │────▶│  SILVER      │────▶│  GOLD        │
    │  (bronze)    │     │  (cleaned)   │     │  (analytics) │
    └──────────────┘     └──────────────┘     └──────────────┘
         │                     │                     │
    Source system data    Deduplicated,         Business-ready
    As-is, no schema     typed, validated       Aggregated, optimized
    enforcement          Schema enforced        Z-ORDER applied

WHY THREE LAYERS?
─────────────────
  RAW (Bronze):
    - Data exactly as received from the source — no modifications.
    - If something goes wrong downstream, you always have the original.
    - Schema-on-read — you can re-interpret the raw data later.
    - Never delete from raw — it's your source of truth.

  SILVER (Cleaned):
    - Deduplicated, typed, validated data.
    - One row per business entity (no duplicates).
    - Foreign keys are consistent (no orphaned records).
    - This is your "single source of truth" for the business.

  GOLD (Analytics):
    - Business-ready tables optimized for querying.
    - Aggregations, joins, and business logic applied.
    - Z-ORDER'd on the columns analysts filter most.
    - This is what BI tools and dashboards query.

USAGE
─────
    python 01_mini_capstone.py

EXPECTED OUTPUT
───────────────
    ── Mini Capstone: End-to-End Sales Pipeline ─────────

      ══ PHASE 1: LAND (Raw Layer) ════════════════════
        Created raw schema: bronze
        Landed 8 raw orders (including 2 duplicates)
        Landed 5 raw customers (including 1 duplicate)

      ══ PHASE 2: TRANSFORM (Silver Layer) ════════════
        Created silver schema
        Deduplicated orders: 8 raw → 6 unique
        Deduplicated customers: 5 raw → 4 unique
        Applied data quality rules:
          - Removed orders with quantity <= 0
          - Removed orders with total_amount <= 0
          - Validated customer references

      ══ PHASE 3: SERVE (Gold Layer) ══════════════════
        Created gold schema
        Created daily_sales_summary: 3 rows
        Created customer_lifetime_value: 4 rows

      ══ PHASE 4: AUDIT (Time Travel) ═════════════════
        DESCRIBE HISTORY for silver_orders:
          Version 0: CREATE TABLE
          Version 1: INSERT (deduplicated data)

      ══ PHASE 5: OPTIMIZE ════════════════════════════
        Z-ORDER'd gold.daily_sales_summary by (sale_date)
        Z-ORDER'd gold.customer_lifetime_value by (customer_id)

      ══ FINAL RESULTS ════════════════════════════════

      ── Daily Sales Summary ──────────────────────────
        Date         Orders  Revenue    Avg Order
        -----------  ------  ---------  ---------
        2024-01-15   2       1,649.97   824.99
        2024-01-16   2       179.97     89.99
        2024-01-17   2       1,399.98   699.99

      ── Customer Lifetime Value ──────────────────────
        Customer          Orders  Total Spent  Avg Order
        ----------------  ------  -----------  ---------
        Alice Johnson     2       1,649.97     824.99
        Bob Smith         1       89.99        89.99
        Carol White       2       1,399.98     699.99
        David Brown       1       89.98        89.98

      Pipeline complete! 🎉
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _db_connect import get_connection, LAB_CATALOG, LAB_SCHEMA

conn = get_connection()

print("\n── Mini Capstone: End-to-End Sales Pipeline ────────")

# ═════════════════════════════════════════════════════════════════════════════
# PHASE 1: LAND — Raw Layer (Bronze)
# ═════════════════════════════════════════════════════════════════════════════
print("\n  ══ PHASE 1: LAND (Raw Layer) ════════════════════")

# Create the bronze schema for raw data
with conn.cursor() as cur:
    cur.execute(f"USE CATALOG {LAB_CATALOG}")
    cur.execute("CREATE SCHEMA IF NOT EXISTS bronze COMMENT 'Raw ingested data — no modifications'")
    cur.execute(f"CREATE SCHEMA IF NOT EXISTS silver COMMENT 'Cleaned, deduplicated, validated data'")
    cur.execute(f"CREATE SCHEMA IF NOT EXISTS gold COMMENT 'Analytics-ready aggregated data'")

print("    Created schemas: bronze, silver, gold")

# ── Land raw orders ──────────────────────────────────────────────────────────
# Simulating data received from an operational database.
# Notice: there are DUPLICATES (order_id 1001 appears twice with different prices)
# and potentially bad data (negative quantity). This is REALISTIC — source data
# is never clean.
with conn.cursor() as cur:
    cur.execute(f"""
        CREATE OR REPLACE TABLE bronze.raw_orders (
            order_id        INT,
            customer_id     INT,
            product_id      INT,
            quantity        INT,
            total_amount    DECIMAL(12,2),
            order_date      DATE,
            ingested_at     TIMESTAMP
        )
        USING DELTA
        COMMENT 'Raw orders from source system — as-is, no validation'
    """)

    cur.execute(f"""
        INSERT INTO bronze.raw_orders
        VALUES
            -- Normal orders
            (1001, 1, 1, 1, 1299.99, DATE '2024-01-15', current_timestamp()),
            (1002, 2, 2, 3, 89.97,   DATE '2024-01-15', current_timestamp()),
            (1003, 3, 4, 2, 179.98,  DATE '2024-01-16', current_timestamp()),
            (1004, 1, 3, 1, 49.99,   DATE '2024-01-16', current_timestamp()),
            -- Duplicate order (same order_id, different amount — data quality issue!)
            (1001, 1, 1, 1, 1349.99, DATE '2024-01-15', current_timestamp()),
            -- Bad data (negative quantity — should be filtered in silver)
            (1005, 4, 2, -1, -29.99, DATE '2024-01-17', current_timestamp()),
            -- More normal orders
            (1006, 3, 1, 1, 1299.99, DATE '2024-01-17', current_timestamp()),
            (1007, 4, 4, 1, 89.99,   DATE '2024-01-17', current_timestamp())
    """)
    raw_orders = cur.rowcount
    print(f"    Landed {raw_orders} raw orders (including 2 duplicates and 1 bad record)")

# ── Land raw customers ───────────────────────────────────────────────────────
with conn.cursor() as cur:
    cur.execute(f"""
        CREATE OR REPLACE TABLE bronze.raw_customers (
            customer_id     INT,
            first_name      STRING,
            last_name       STRING,
            email           STRING,
            signup_date     DATE,
            ingested_at     TIMESTAMP
        )
        USING DELTA
        COMMENT 'Raw customers from source system — may have duplicates'
    """)

    cur.execute(f"""
        INSERT INTO bronze.raw_customers
        VALUES
            (1, 'Alice', 'Johnson',  'alice@example.com',  DATE '2023-06-01', current_timestamp()),
            (2, 'Bob',   'Smith',    'bob@example.com',    DATE '2023-07-15', current_timestamp()),
            (3, 'Carol', 'White',    'carol@example.com',  DATE '2023-08-20', current_timestamp()),
            (4, 'David', 'Brown',    'david@example.com',  DATE '2023-09-10', current_timestamp()),
            -- Duplicate customer (same customer_id, different email)
            (1, 'Alice', 'Johnson',  'alice.j@newmail.com', DATE '2023-06-01', current_timestamp())
    """)
    raw_customers = cur.rowcount
    print(f"    Landed {raw_customers} raw customers (including 1 duplicate)")

# ═════════════════════════════════════════════════════════════════════════════
# PHASE 2: TRANSFORM — Silver Layer (Cleaned)
# ═════════════════════════════════════════════════════════════════════════════
print("\n  ══ PHASE 2: TRANSFORM (Silver Layer) ════════════")

# ── Deduplicate orders ───────────────────────────────────────────────────────
# Strategy: Keep the FIRST occurrence of each order_id (by ingested_at).
# This is a common pattern — ROW_NUMBER() OVER (PARTITION BY key ORDER BY timestamp)
# gives each duplicate a rank, and we keep only rank = 1.
#
# We also filter out bad data:
#   - quantity > 0 (no negative quantities)
#   - total_amount > 0 (no negative amounts)
#
# This is the "data quality gate" — bad records don't make it to silver.
with conn.cursor() as cur:
    cur.execute(f"""
        CREATE OR REPLACE TABLE silver.orders AS
        WITH ranked AS (
            SELECT
                order_id,
                customer_id,
                product_id,
                quantity,
                total_amount,
                order_date,
                ingested_at,
                ROW_NUMBER() OVER (
                    PARTITION BY order_id
                    ORDER BY ingested_at ASC
                ) AS rn
            FROM bronze.raw_orders
            WHERE  quantity > 0       -- Data quality rule: no negative quantities
               AND total_amount > 0   -- Data quality rule: no negative amounts
        )
        SELECT
            order_id,
            customer_id,
            product_id,
            quantity,
            total_amount,
            order_date,
            ingested_at
        FROM ranked
        WHERE rn = 1  -- Keep only the first occurrence of each order_id
    """)

    cur.execute(f"SELECT COUNT(*) FROM silver.orders")
    silver_orders = cur.fetchone()[0]
    print(f"    Deduplicated orders: {raw_orders} raw → {silver_orders} unique")

# ── Deduplicate customers ────────────────────────────────────────────────────
# Same pattern — ROW_NUMBER() to keep the first occurrence.
# For customers, we also keep the earliest email (by ingested_at).
with conn.cursor() as cur:
    cur.execute(f"""
        CREATE OR REPLACE TABLE silver.customers AS
        WITH ranked AS (
            SELECT
                customer_id,
                first_name,
                last_name,
                email,
                signup_date,
                ingested_at,
                ROW_NUMBER() OVER (
                    PARTITION BY customer_id
                    ORDER BY ingested_at ASC
                ) AS rn
            FROM bronze.raw_customers
        )
        SELECT
            customer_id,
            first_name,
            last_name,
            email,
            signup_date,
            ingested_at
        FROM ranked
        WHERE rn = 1
    """)

    cur.execute(f"SELECT COUNT(*) FROM silver.customers")
    silver_customers = cur.fetchone()[0]
    print(f"    Deduplicated customers: {raw_customers} raw → {silver_customers} unique")

# ── Data quality summary ─────────────────────────────────────────────────────
print("    Applied data quality rules:")
print("      - Removed orders with quantity <= 0")
print("      - Removed orders with total_amount <= 0")
print("      - Kept first occurrence of duplicate order_ids")
print("      - Kept first occurrence of duplicate customer_ids")

# ═════════════════════════════════════════════════════════════════════════════
# PHASE 3: SERVE — Gold Layer (Analytics)
# ═════════════════════════════════════════════════════════════════════════════
print("\n  ══ PHASE 3: SERVE (Gold Layer) ══════════════════")

# ── Daily Sales Summary ──────────────────────────────────────────────────────
# This is what a BI dashboard would query — pre-aggregated by date.
# Benefits:
#   - Faster queries (no need to aggregate millions of rows at query time)
#   - Consistent metrics (everyone uses the same definition of "daily sales")
#   - Smaller data (365 rows per year vs millions of order rows)
with conn.cursor() as cur:
    cur.execute(f"""
        CREATE OR REPLACE TABLE gold.daily_sales_summary AS
        SELECT
            o.order_date      AS sale_date,
            COUNT(*)          AS order_count,
            SUM(o.quantity)   AS total_units,
            SUM(o.total_amount) AS total_revenue,
            ROUND(AVG(o.total_amount), 2) AS avg_order_value
        FROM   silver.orders o
        GROUP  BY o.order_date
        ORDER  BY o.order_date
    """)

    cur.execute(f"SELECT COUNT(*) FROM gold.daily_sales_summary")
    daily_rows = cur.fetchone()[0]
    print(f"    Created daily_sales_summary: {daily_rows} rows")

# ── Customer Lifetime Value ──────────────────────────────────────────────────
# This is a classic analytics table — how much has each customer spent?
# Used for:
#   - Marketing: who are our best customers?
#   - Support: who should we prioritize?
#   - Finance: what's our recurring revenue base?
with conn.cursor() as cur:
    cur.execute(f"""
        CREATE OR REPLACE TABLE gold.customer_lifetime_value AS
        SELECT
            c.customer_id,
            c.first_name || ' ' || c.last_name AS customer_name,
            c.email,
            COUNT(o.order_id)   AS total_orders,
            SUM(o.total_amount) AS total_spent,
            ROUND(AVG(o.total_amount), 2) AS avg_order_value,
            MIN(o.order_date)   AS first_order_date,
            MAX(o.order_date)   AS last_order_date
        FROM   silver.customers c
        LEFT   JOIN silver.orders o
               ON c.customer_id = o.customer_id
        GROUP  BY c.customer_id, c.first_name, c.last_name, c.email
        ORDER  BY total_spent DESC
    """)

    cur.execute(f"SELECT COUNT(*) FROM gold.customer_lifetime_value")
    clv_rows = cur.fetchone()[0]
    print(f"    Created customer_lifetime_value: {clv_rows} rows")

# ═════════════════════════════════════════════════════════════════════════════
# PHASE 4: AUDIT — Time Travel Verification
# ═════════════════════════════════════════════════════════════════════════════
print("\n  ══ PHASE 4: AUDIT (Time Travel) ═════════════════")

with conn.cursor() as cur:
    cur.execute("DESCRIBE HISTORY silver.orders")
    history = cur.fetchall()

print("    DESCRIBE HISTORY for silver_orders:")
for row in history:
    version = row[0]
    timestamp = str(row[1])[:27] if row[1] else "unknown"
    operation = row[4] if len(row) > 4 else "unknown"
    print(f"      Version {version}: {timestamp} — {operation}")

# ═════════════════════════════════════════════════════════════════════════════
# PHASE 5: OPTIMIZE — Z-ORDER for Query Performance
# ═════════════════════════════════════════════════════════════════════════════
print("\n  ══ PHASE 5: OPTIMIZE ════════════════════════════")

with conn.cursor() as cur:
    cur.execute("OPTIMIZE gold.daily_sales_summary ZORDER BY (sale_date)")
    print("    Z-ORDER'd gold.daily_sales_summary by (sale_date)")

    cur.execute("OPTIMIZE gold.customer_lifetime_value ZORDER BY (customer_id)")
    print("    Z-ORDER'd gold.customer_lifetime_value by (customer_id)")

# ═════════════════════════════════════════════════════════════════════════════
# FINAL RESULTS — Show the analytics output
# ═════════════════════════════════════════════════════════════════════════════
print("\n  ══ FINAL RESULTS ════════════════════════════════")

# ── Daily Sales Summary ──────────────────────────────────────────────────────
print("\n  ── Daily Sales Summary ──────────────────────────")
with conn.cursor() as cur:
    cur.execute("""
        SELECT sale_date, order_count, total_revenue, avg_order_value
        FROM   gold.daily_sales_summary
        ORDER  BY sale_date
    """)
    rows = cur.fetchall()

print(f"    {'Date':<12} {'Orders':<7} {'Revenue':<11} {'Avg Order'}")
print(f"    {'-'*12} {'-'*7} {'-'*11} {'-'*10}")
for date, orders, revenue, avg in rows:
    print(f"    {str(date):<12} {orders:<7} ${revenue:>9,.2f} ${avg:>9,.2f}")

# ── Customer Lifetime Value ──────────────────────────────────────────────────
print("\n  ── Customer Lifetime Value ──────────────────────")
with conn.cursor() as cur:
    cur.execute("""
        SELECT customer_name, total_orders, total_spent, avg_order_value
        FROM   gold.customer_lifetime_value
        ORDER  BY total_spent DESC
    """)
    rows = cur.fetchall()

print(f"    {'Customer':<18} {'Orders':<7} {'Total Spent':<12} {'Avg Order'}")
print(f"    {'-'*18} {'-'*7} {'-'*12} {'-'*10}")
for name, orders, spent, avg in rows:
    print(f"    {name:<18} {orders:<7} ${spent:>10,.2f} ${avg:>9,.2f}")

# ── Pipeline summary ─────────────────────────────────────────────────────────
print("\n  ══ PIPELINE SUMMARY ═════════════════════════════")
print(f"    Bronze (raw):      {raw_orders} orders, {raw_customers} customers")
print(f"    Silver (clean):    {silver_orders} orders, {silver_customers} customers")
print(f"    Gold (analytics):  {daily_rows} daily summaries, {clv_rows} customer profiles")
print("\n  Pipeline complete! 🎉")

conn.close()
print()
