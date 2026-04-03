"""
NUGGET 01-01 (Bridge) -- SQL Joins in Databricks SQL
======================================================
Covers: INNER JOIN, LEFT JOIN, aggregating joins, multi-table joins.

PostgreSQL -> Databricks SQL transfer notes:
  - Syntax is identical: JOIN ... ON ...
  - USING clause works the same way
  - Databricks handles large joins with broadcast hints for small tables
  - Key difference: Databricks uses Adaptive Query Execution (AQE) to
    automatically choose between sort-merge join and broadcast join at
    runtime. PostgreSQL uses a fixed plan chosen at parse time.

Usage:
    python 01_joins.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _db_bridge_connect import get_connection, LAB_CATALOG, LAB_SCHEMA

C = LAB_CATALOG
S = LAB_SCHEMA
DIVIDER = "-" * 64

results = []


def check(label: str, rows, expect_min: int = 1) -> None:
    ok = rows is not None and len(rows) >= expect_min
    status = "PASS" if ok else "FAIL"
    results.append((label, ok))
    print(f"  {status}  {label}  ({len(rows) if rows else 0} rows)")
    if ok and rows:
        # Print first 3 rows for visibility
        for r in rows[:3]:
            print(f"         {r}")


print()
print("=" * 64)
print("  Nugget 01-01: SQL Joins")
print("=" * 64)

conn = get_connection()
with conn.cursor() as cur:

    # ── 1. INNER JOIN: orders + customers ─────────────────────────────────
    # INNER JOIN returns only rows where the key exists in BOTH tables.
    # In Databricks, this compiles to a hash join or sort-merge join
    # depending on table sizes. For small lookup tables, AQE may
    # automatically broadcast the smaller side (like PostgreSQL's
    # nested loop for small tables).
    print()
    print("  [1] INNER JOIN: orders with customer names")
    cur.execute(f"""
        SELECT
            o.order_id,
            c.customer_name,
            o.order_date,
            o.total_amount
        FROM {C}.{S}.sales_orders o
        INNER JOIN {C}.{S}.customers c ON o.customer_id = c.customer_id
        WHERE o.status = 'Shipped'
        ORDER BY o.order_id
        LIMIT 5
    """)
    rows = cur.fetchall()
    check("INNER JOIN orders+customers (shipped, limit 5)", rows, 5)

    # ── 2. LEFT JOIN: find customers with no orders ────────────────────────
    # LEFT JOIN returns all rows from the left table even if there is no
    # match on the right. NULL in the right-side column signals no match.
    # This is identical in PostgreSQL, Snowflake, and Databricks SQL.
    print()
    print("  [2] LEFT JOIN: customers with no orders")
    cur.execute(f"""
        SELECT
            c.customer_id,
            c.customer_name,
            c.region,
            o.order_id
        FROM {C}.{S}.customers c
        LEFT JOIN {C}.{S}.sales_orders o ON c.customer_id = o.customer_id
        WHERE o.order_id IS NULL
        ORDER BY c.customer_id
    """)
    rows = cur.fetchall()
    # In our seed data every customer has at least one order; result may be 0
    status = "PASS"  # structural pass — query ran correctly
    results.append(("LEFT JOIN no-order customers", True))
    print(f"  PASS  LEFT JOIN no-order customers  ({len(rows)} rows -- 0 is valid)")

    # ── 3. Aggregating JOIN: total spend per customer ──────────────────────
    # GROUP BY after a JOIN is the standard pattern for summary reports.
    # Databricks SQL supports all standard aggregate functions.
    # PostgreSQL equivalent is identical syntax.
    print()
    print("  [3] Aggregating JOIN: total spend per customer")
    cur.execute(f"""
        SELECT
            c.customer_name,
            c.region,
            COUNT(o.order_id)           AS order_count,
            SUM(o.total_amount)         AS total_spend,
            AVG(o.total_amount)         AS avg_order_value
        FROM {C}.{S}.customers c
        INNER JOIN {C}.{S}.sales_orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_name, c.region
        ORDER BY total_spend DESC
        LIMIT 5
    """)
    rows = cur.fetchall()
    check("Aggregating JOIN top 5 spenders", rows, 5)

    # ── 4. Three-table JOIN: orders + customers + products ─────────────────
    # Multi-table JOINs work identically across PostgreSQL, Snowflake,
    # and Databricks SQL. Databricks AQE may reorder the join tree at
    # runtime for optimal performance.
    print()
    print("  [4] Three-table JOIN: orders + customers + products")
    cur.execute(f"""
        SELECT
            o.order_id,
            c.customer_name,
            p.product_name,
            p.category,
            o.quantity,
            o.total_amount
        FROM {C}.{S}.sales_orders o
        INNER JOIN {C}.{S}.customers c ON o.customer_id = c.customer_id
        INNER JOIN {C}.{S}.products  p ON o.product_id  = p.product_id
        WHERE p.category = 'Electronics'
        ORDER BY o.order_id
        LIMIT 5
    """)
    rows = cur.fetchall()
    check("Three-table JOIN (Electronics only)", rows, 1)

    # ── 5. Self-JOIN: customers in the same region ─────────────────────────
    # Self-JOINs are useful for comparing rows within the same table.
    # Example: find customer pairs in the same region.
    print()
    print("  [5] Self-JOIN: customer pairs in same region")
    cur.execute(f"""
        SELECT
            a.customer_name AS customer_a,
            b.customer_name AS customer_b,
            a.region
        FROM {C}.{S}.customers a
        INNER JOIN {C}.{S}.customers b
            ON a.region = b.region AND a.customer_id < b.customer_id
        ORDER BY a.region, a.customer_id
        LIMIT 5
    """)
    rows = cur.fetchall()
    check("Self-JOIN same-region pairs (limit 5)", rows, 1)

    # ── 6. JOIN with BROADCAST hint ────────────────────────────────────────
    # BROADCAST hint tells Databricks to broadcast the smaller table to
    # all executors, avoiding a shuffle for the join.
    # PostgreSQL equivalent: no direct hint; relies on planner statistics.
    # Snowflake equivalent: automatic broadcast for tables < 10 MB by default.
    print()
    print("  [6] JOIN with /*+ BROADCAST */ hint (products is small)")
    cur.execute(f"""
        SELECT /*+ BROADCAST(p) */
            o.order_id,
            p.product_name,
            o.total_amount
        FROM {C}.{S}.sales_orders o
        INNER JOIN {C}.{S}.products p ON o.product_id = p.product_id
        ORDER BY o.order_id
        LIMIT 3
    """)
    rows = cur.fetchall()
    check("BROADCAST hint join", rows, 1)

conn.close()

# ── Summary ───────────────────────────────────────────────────────────────
print()
print(DIVIDER)
passed = sum(1 for _, ok in results if ok)
total  = len(results)
print(f"  Nugget 01-01: {passed}/{total} checks passed")
print(DIVIDER)
print()
if passed < total:
    sys.exit(1)
