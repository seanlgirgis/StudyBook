"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 03-02 · OPTIMIZE & Z-ORDER                                           ║
║  Physical data layout optimization for query performance.                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Demonstrates Delta Lake's OPTIMIZE and Z-ORDER commands — how to make
your queries faster by organizing data files intelligently.

CONCEPTS
────────
The small files problem:
  - Every INSERT, UPDATE, DELETE, or MERGE creates new data files.
  - Over time, your table accumulates thousands of tiny files.
  - Reading 10,000 small files is MUCH slower than reading 10 large files.
  - This is the #1 cause of slow Delta queries in production.

OPTIMIZE — file compaction:
  - Rewrites many small files into fewer large files.
  - Default target file size: 128 MB (optimal for Spark/Databricks).
  - Does NOT change the table's logical content — only physical layout.
  - Creates a NEW commit in the Delta log (readers see the optimized table).
  - Old small files are kept for Time Travel until VACUUM removes them.
  - Run OPTIMIZE regularly in production (daily or weekly).

  Syntax:
    OPTIMIZE table_name
    OPTIMIZE table_name WHERE date >= '2024-01-01'  -- partition-level

Z-ORDER — multi-dimensional data skipping:
  - Co-locates related data in the same files based on column values.
  - Creates a Z-order curve mapping multi-dimensional values to 1D space.
  - When you filter on Z-ORDER columns, Delta can skip entire files.
  - Think of it as an automatic index — but for columnar files.

  Syntax:
    OPTIMIZE table_name ZORDER BY (col1, col2)

  Example:
    If you frequently filter by (product_id, sale_date):
    OPTIMIZE fact_sales ZORDER BY (product_id, sale_date)

    After Z-ORDER, a query filtering product_id = 5 will only read
    files that contain product_id = 5 — not the entire table.

Data skipping — how Delta uses Z-ORDER:
  - Delta collects min/max statistics for every column in every file.
  - When you run WHERE product_id = 5, Delta checks each file's stats.
  - If a file's product_id range doesn't include 5, Delta skips it entirely.
  - Z-ORDER makes these statistics more selective → more files skipped.

When to use Z-ORDER:
  - Columns used frequently in WHERE clauses.
  - Columns with high cardinality (many distinct values).
  - Don't Z-ORDER on low-cardinality columns (boolean, country) — use PARTITION BY instead.
  - Max 3-4 columns — more columns dilute the benefit.

PARTITION BY vs Z-ORDER:
  - PARTITION BY: good for low-cardinality columns (date, country, category).
    Creates separate directories per partition value.
    Too many partitions = too many directories = slow listing.
  - Z-ORDER: good for high-cardinality columns (product_id, customer_id).
    No directory structure change — just reorganizes data within files.
    Can combine multiple columns in one Z-ORDER.

  Rule of thumb:
    - Partition by date (if queries filter by date range).
    - Z-ORDER by the columns you filter on most often.

USAGE
─────
    python 02_optimize.py

EXPECTED OUTPUT
───────────────
    ── OPTIMIZE & Z-ORDER ─────────────────────────────

      ── Table stats before OPTIMIZE ──────────────────
        Table: nugget_lab.default.fact_sales
        Row count: 800
        File count: ~1 (small table — OPTIMIZE has minimal effect)

      ── Running OPTIMIZE ─────────────────────────────
        OPTIMIZE complete.

      ── Running Z-ORDER BY (product_id, sale_date) ───
        Z-ORDER complete.

      ── Data skipping demonstration ──────────────────
        Query: SELECT * WHERE product_id = 2
        Files scanned: 1 (out of 1 total)
        Rows returned: 200

        Note: On a small table, data skipping is minimal.
        On a 1TB table with billions of rows, Z-ORDER can reduce
        scanned data by 90-99%.

      ── DESCRIBE DETAIL ──────────────────────────────
        Table format: delta
        Location: abfss://...
        Size in bytes: 45678
        Num files: 1
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _db_connect import get_connection, LAB_CATALOG, LAB_SCHEMA

conn = get_connection()

print("\n── OPTIMIZE & Z-ORDER ─────────────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Check current table stats
#    DESCRIBE DETAIL returns table-level metadata: format, size, file count.
#    This is how you measure the impact of OPTIMIZE.
# ─────────────────────────────────────────────────────────────────────────────
table_name = f"{LAB_CATALOG}.{LAB_SCHEMA}.fact_sales"

print(f"\n  ── Table stats before OPTIMIZE ─────────────────")
print(f"    Table: {table_name}")

with conn.cursor() as cur:
    # Get row count
    cur.execute(f"SELECT COUNT(*) FROM {table_name}")
    row_count = cur.fetchone()[0]
    print(f"    Row count: {row_count:,}")

    # Get file count via DESCRIBE DETAIL
    cur.execute(f"DESCRIBE DETAIL {table_name}")
    detail = {row[0]: row[1] for row in cur.fetchall()}
    num_files = detail.get("numFiles", "unknown")
    size_bytes = detail.get("sizeInBytes", "unknown")
    print(f"    File count: {num_files}")
    if isinstance(size_bytes, int):
        size_str = f"{size_bytes / 1024:.1f} KB" if size_bytes < 1_000_000 else f"{size_bytes / 1_000_000:.1f} MB"
        print(f"    Size: {size_str}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. OPTIMIZE — compact small files
#    On a small table like this, OPTIMIZE won't do much (there's only 1 file).
#    But on a production table with thousands of files from incremental loads,
#    OPTIMIZE can reduce file count by 10-100x.
#
#    When to run OPTIMIZE:
#      - After a large batch load (INSERT/MERGE created many files)
#      - As a scheduled job (daily/weekly)
#      - Before a major query (optimize the data you're about to query)
#
#    OPTIMIZE is idempotent — running it on an already-optimized table is a no-op.
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Running OPTIMIZE ─────────────────────────────")
with conn.cursor() as cur:
    cur.execute(f"OPTIMIZE {table_name}")
    rows = cur.fetchall()
    # OPTIMIZE returns a row with metrics: numFilesAdded, numFilesRemoved, etc.
    if rows:
        for row in rows:
            for col_name, value in zip(cur.description, row):
                if col_name[0] in ("numFilesAdded", "numFilesRemoved", "totalFiles"):
                    print(f"    {col_name[0]}: {value}")
    print("    OPTIMIZE complete.")

# ─────────────────────────────────────────────────────────────────────────────
# 3. Z-ORDER — multi-dimensional data skipping
#    We Z-ORDER by (product_id, sale_date) because these are the columns
#    most commonly used in WHERE clauses for fact tables.
#
#    After Z-ORDER:
#      - Files are rewritten so that rows with similar (product_id, sale_date)
#        values are co-located in the same files.
#      - When you query WHERE product_id = 2, Delta can skip files that
#        don't contain product_id = 2.
#      - The more selective your filter, the more files are skipped.
#
#    Z-ORDER is expensive (rewrites all files) — run it infrequently.
#    Typical cadence: weekly or monthly, after OPTIMIZE.
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Running Z-ORDER BY (product_id, sale_date) ───")
with conn.cursor() as cur:
    cur.execute(f"OPTIMIZE {table_name} ZORDER BY (product_id, sale_date)")
    rows = cur.fetchall()
    print("    Z-ORDER complete.")

# ─────────────────────────────────────────────────────────────────────────────
# 4. Demonstrate data skipping
#    After Z-ORDER, queries filtering on Z-ORDER columns should scan fewer files.
#    We can see this by comparing the query plan.
#
#    EXPLAIN shows the physical plan — look for:
#      - "PushedFilters" — filters pushed down to the file scan level
#      - "PartitionFilters" — partition-level pruning
#      - "DataFilters" — row-level filters within files
#
#    On a small table, the benefit is minimal. On a 1TB table, Z-ORDER
#    can reduce scanned data from 1TB to 10GB (99% reduction).
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Data skipping demonstration ──────────────────")
print(f"    Query: SELECT * WHERE product_id = 2")

with conn.cursor() as cur:
    # Run the query
    cur.execute(f"""
        SELECT product_id, sale_date, quantity, total_amount
        FROM   {table_name}
        WHERE  product_id = 2
        ORDER  BY sale_date
    """)
    rows = cur.fetchall()
    print(f"    Rows returned: {len(rows)}")

    # Show the EXPLAIN plan
    cur.execute(f"""
        EXPLAIN FORMATTED
        SELECT * FROM {table_name} WHERE product_id = 2
    """)
    plan_rows = cur.fetchall()
    # Look for data skipping info in the plan
    for plan_row in plan_rows:
        plan_text = str(plan_row[0])
        if "PushedFilters" in plan_text or "DataFilters" in plan_text:
            print(f"    Plan: {plan_text[:120]}...")
            break

print("\n    Note: On a small table, data skipping is minimal.")
print("    On a 1TB table with billions of rows, Z-ORDER can reduce")
print("    scanned data by 90-99%.")

# ─────────────────────────────────────────────────────────────────────────────
# 5. DESCRIBE DETAIL — post-optimization stats
#    Compare these stats with the pre-OPTIMIZE stats to see the impact.
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n  ── DESCRIBE DETAIL (after OPTIMIZE) ───────────")
with conn.cursor() as cur:
    cur.execute(f"DESCRIBE DETAIL {table_name}")
    detail = {row[0]: row[1] for row in cur.fetchall()}

for key in ("format", "location", "sizeInBytes", "numFiles"):
    value = detail.get(key, "N/A")
    if key == "sizeInBytes" and isinstance(value, int):
        value = f"{value / 1024:.1f} KB" if value < 1_000_000 else f"{value / 1_000_000:.1f} MB"
    print(f"    {key:<16} {value}")

# ─────────────────────────────────────────────────────────────────────────────
# 6. Best practices summary
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Best Practices ───────────────────────────────")
print("    1. OPTIMIZE after large batch loads (daily)")
print("    2. Z-ORDER on high-cardinality filter columns (weekly/monthly)")
print("    3. PARTITION BY low-cardinality columns (date, country)")
print("    4. VACUUM after OPTIMIZE to reclaim storage (RETAIN 168 HOURS)")
print("    5. Monitor query performance before/after optimization")
print("    6. Don't over-optimize small tables — the cost outweighs the benefit")

conn.close()
print()
