"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 02-02 · INSERT & SELECT                                              ║
║  Loading data and querying Delta tables.                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Inserts data into Delta tables using multiple patterns and runs
SELECT queries to verify the data landed correctly.

CONCEPTS
────────
INSERT INTO ... VALUES:
  - The simplest way to load data — one row at a time or multi-row.
  - Fine for small batches, terrible for bulk loads.
  - Each INSERT is a separate Delta transaction (overhead adds up).
  - Use for: dimension tables, config tables, small reference data.

INSERT INTO ... SELECT:
  - Load data from another table or query result.
  - The standard ETL pattern — transform then insert.
  - Single Delta transaction for the entire batch (atomic).
  - Use for: fact tables, bulk dimension loads, pipeline outputs.

SELECT * vs SELECT <columns>:
  - SELECT * is fine for exploration — NEVER in production code.
  - SELECT <columns> is explicit — schema changes won't break your query.
  - Delta supports schema evolution — new columns can appear over time.
  - Production queries should always name their columns.

WHERE clause basics:
  - Filters rows before they're returned (reduces I/O via partition pruning).
  - Delta uses Z-ORDER and partitioning to skip irrelevant data files.
  - A well-placed WHERE can reduce a 1TB scan to 10GB.

ORDER BY:
  - Sorts the result set in the client (not in storage).
  - Delta tables are NOT physically sorted unless you OPTIMIZE + ZORDER.
  - ORDER BY on large result sets is expensive — use LIMIT with it.

Delta's ACID guarantee:
  - Every INSERT is atomic — either all rows land or none do.
  - Concurrent writers don't corrupt the table (unlike plain Parquet).
  - Readers always see a consistent snapshot (no dirty reads).

USAGE
─────
    python 02_insert_select.py

EXPECTED OUTPUT
───────────────
    ── INSERT & SELECT ──────────────────────────────

      Current catalog: nugget_lab
      Current schema:  default

      ── Inserting products ─────────────────────────
        Inserted 5 rows into dim_product

      ── All products ───────────────────────────────
        ID  Name                Category        Price      Active
        --  ------------------  --------------  ---------  ------
         1  Laptop Pro 15       Electronics     1299.99    True
         2  Wireless Mouse      Accessories       29.99    True
         3  USB-C Hub           Accessories       49.99    True
         4  Gaming Keyboard     Electronics       89.99    True
         5  Old Monitor         Electronics      199.99    False

      ── Active products only ───────────────────────
        Found 4 active products

      ── Products by category ───────────────────────
        Category       Count  Avg Price
        -------------  -----  ---------
        Accessories        2      39.99
        Electronics        2     694.99

      ── Inserting sales ────────────────────────────
        Inserted 8 rows into fact_sales

      ── Total sales by product ─────────────────────
        Product             Total Qty  Total Revenue
        ------------------  ---------  -------------
        Laptop Pro 15              15       18749.85
        Wireless Mouse             50        1499.50
        USB-C Hub                  30        1499.70
        Gaming Keyboard            20        1799.80
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _db_connect import get_connection, LAB_CATALOG, LAB_SCHEMA

conn = get_connection()

print("\n── INSERT & SELECT ──────────────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Confirm we're in the right catalog/schema
# ─────────────────────────────────────────────────────────────────────────────
with conn.cursor() as cur:
    cur.execute("SELECT CURRENT_CATALOG(), CURRENT_SCHEMA()")
    current_catalog, current_schema = cur.fetchone()

print(f"\n  Current catalog: {current_catalog}")
print(f"  Current schema:  {current_schema}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Insert data into dim_product using multi-row VALUES
#    Multi-row INSERT is more efficient than individual INSERTs.
#    Each VALUES clause is a single Delta transaction.
#
#    Note: We use PARSE_JSON() to create VARIANT values from JSON strings.
#    This is how you load semi-structured data into a VARIANT column.
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Inserting products ─────────────────────────")
with conn.cursor() as cur:
    cur.execute(f"""
        INSERT INTO {LAB_CATALOG}.{LAB_SCHEMA}.dim_product
        (product_id, product_name, category, price, is_active, created_at, attributes)
        VALUES
            (1, 'Laptop Pro 15',    'Electronics', 1299.99, true,  current_timestamp(), PARSE_JSON('{{"warranty": "2yr", "color": "silver"}}')),
            (2, 'Wireless Mouse',   'Accessories',   29.99, true,  current_timestamp(), PARSE_JSON('{{"warranty": "1yr", "color": "black"}}')),
            (3, 'USB-C Hub',        'Accessories',   49.99, true,  current_timestamp(), PARSE_JSON('{{"warranty": "1yr", "ports": 7}}')),
            (4, 'Gaming Keyboard',  'Electronics',   89.99, true,  current_timestamp(), PARSE_JSON('{{"warranty": "2yr", "switches": "mechanical"}}')),
            (5, 'Old Monitor',      'Electronics',  199.99, false, current_timestamp(), PARSE_JSON('{{"warranty": "expired", "size": "24in"}}'))
    """)
    # cur.rowcount returns the number of affected rows (INSERTed in this case).
    # Note: Not all drivers support rowcount — Databricks SQL Connector does.
    inserted = cur.rowcount
    print(f"    Inserted {inserted} rows into dim_product")

# ─────────────────────────────────────────────────────────────────────────────
# 3. SELECT all products
#    SELECT * is fine for exploration — but name columns in production code.
#    Notice we ORDER BY product_id — Delta tables have NO inherent order.
#    Without ORDER BY, rows come back in whatever order the files were read.
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── All products ───────────────────────────────")
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
    # price comes back as Decimal — format to 2 decimal places
    price_str = f"${price:,.2f}" if price else "N/A"
    print(f"    {pid:<4} {name:<20} {category:<15} {price_str:<10} {is_active}")

# ─────────────────────────────────────────────────────────────────────────────
# 4. SELECT with WHERE filter
#    This is the most common query pattern in DE work.
#    Filter early, filter often — push WHERE clauses as close to the source as possible.
#    Delta's optimizer will use partition pruning and Z-ORDER to skip irrelevant files.
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Active products only ───────────────────────")
with conn.cursor() as cur:
    cur.execute(f"""
        SELECT COUNT(*) AS active_count
        FROM   {LAB_CATALOG}.{LAB_SCHEMA}.dim_product
        WHERE  is_active = true
    """)
    active_count = cur.fetchone()[0]
    print(f"    Found {active_count} active products")

# ─────────────────────────────────────────────────────────────────────────────
# 5. Aggregation with GROUP BY
#    Standard SQL aggregation — works identically on Delta as on any RDBMS.
#    The difference: Delta can push aggregations down to the file level
#    using statistics in the transaction log (min/max values per file).
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Products by category ───────────────────────")
with conn.cursor() as cur:
    cur.execute(f"""
        SELECT
            category,
            COUNT(*)          AS product_count,
            ROUND(AVG(price), 2) AS avg_price
        FROM   {LAB_CATALOG}.{LAB_SCHEMA}.dim_product
        WHERE  is_active = true
        GROUP  BY category
        ORDER  BY product_count DESC
    """)
    rows = cur.fetchall()

print(f"    {'Category':<15} {'Count':<6} {'Avg Price'}")
print(f"    {'-'*15} {'-'*6} {'-'*10}")
for category, count, avg_price in rows:
    print(f"    {category:<15} {count:<6} ${avg_price:,.2f}")

# ─────────────────────────────────────────────────────────────────────────────
# 6. Insert data into fact_sales using INSERT ... SELECT
#    This is the standard ETL pattern — generate data from a query and insert.
#    In real pipelines, the SELECT would read from a staging table or external source.
#    Here we use a cross join to generate synthetic sales data.
#
#    Note: We use sequence() and explode() to generate rows — a common
#    Databricks pattern for data generation and testing.
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Inserting sales ────────────────────────────")
with conn.cursor() as cur:
    cur.execute(f"""
        INSERT INTO {LAB_CATALOG}.{LAB_SCHEMA}.fact_sales
        (sale_id, product_id, customer_id, sale_date, quantity, total_amount, channel)
        SELECT
            ROW_NUMBER() OVER (ORDER BY p.product_id, d.date_val) AS sale_id,
            p.product_id,
            (p.product_id * 100 + FLOOR(RAND() * 50)) AS customer_id,
            d.date_val,
            CASE p.product_id
                WHEN 1 THEN FLOOR(UNIFORM(1, 5, RANDOM()))   -- laptops: 1-5
                WHEN 2 THEN FLOOR(UNIFORM(5, 20, RANDOM()))  -- mice: 5-20
                WHEN 3 THEN FLOOR(UNIFORM(3, 15, RANDOM()))  -- hubs: 3-15
                WHEN 4 THEN FLOOR(UNIFORM(2, 10, RANDOM()))  -- keyboards: 2-10
                ELSE 1
            END AS quantity,
            CASE p.product_id
                WHEN 1 THEN FLOOR(UNIFORM(1, 5, RANDOM())) * 1299.99
                WHEN 2 THEN FLOOR(UNIFORM(5, 20, RANDOM())) * 29.99
                WHEN 3 THEN FLOOR(UNIFORM(3, 15, RANDOM())) * 49.99
                WHEN 4 THEN FLOOR(UNIFORM(2, 10, RANDOM())) * 89.99
                ELSE 199.99
            END AS total_amount,
            CASE FLOOR(UNIFORM(0, 3, RANDOM()))
                WHEN 0 THEN 'online'
                WHEN 1 THEN 'retail'
                ELSE 'wholesale'
            END AS channel
        FROM   {LAB_CATALOG}.{LAB_SCHEMA}.dim_product p
        CROSS  JOIN (SELECT DATE '2024-01-01' AS date_val UNION ALL
                     SELECT DATE '2024-01-02' UNION ALL
                     SELECT DATE '2024-01-03' UNION ALL
                     SELECT DATE '2024-01-04') d
        WHERE  p.is_active = true
    """)
    inserted = cur.rowcount
    print(f"    Inserted {inserted} rows into fact_sales")

# ─────────────────────────────────────────────────────────────────────────────
# 7. JOIN query — total sales by product
#    This is the classic fact-to-dimension JOIN.
#    In a real pipeline, this would be a dbt model or a Spark SQL transformation.
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Total sales by product ─────────────────────")
with conn.cursor() as cur:
    cur.execute(f"""
        SELECT
            p.product_name,
            SUM(f.quantity)     AS total_qty,
            SUM(f.total_amount) AS total_revenue
        FROM   {LAB_CATALOG}.{LAB_SCHEMA}.fact_sales f
        JOIN   {LAB_CATALOG}.{LAB_SCHEMA}.dim_product p
               ON f.product_id = p.product_id
        GROUP  BY p.product_name
        ORDER  BY total_revenue DESC
    """)
    rows = cur.fetchall()

print(f"    {'Product':<20} {'Total Qty':<10} {'Total Revenue'}")
print(f"    {'-'*20} {'-'*10} {'-'*13}")
for name, qty, revenue in rows:
    print(f"    {name:<20} {qty:<10} ${revenue:,.2f}")

conn.close()
print()
