"""
NUGGET 02-02 (Bridge) -- Window Functions
==========================================
Covers: ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD, running totals,
        NTILE, FIRST_VALUE/LAST_VALUE, frame clauses.

PostgreSQL -> Databricks SQL transfer notes:
  - OVER (PARTITION BY ... ORDER BY ...) syntax is identical
  - ROWS/RANGE BETWEEN frames: identical
  - LAG/LEAD with offset and default: identical
  - FIRST_VALUE/LAST_VALUE: identical (watch IGNORE NULLS)
  - NTILE: identical
  - Key difference: Databricks evaluates window functions as Spark
    stages with shuffle by partition key. PostgreSQL sorts in memory
    or uses index scans.

Snowflake: identical syntax for all functions listed here.

Usage:
    python 02_window_functions.py
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
    results.append((label, ok))
    status = "PASS" if ok else "FAIL"
    print(f"  {status}  {label}  ({len(rows) if rows else 0} rows)")
    if ok and rows:
        for r in rows[:3]:
            print(f"         {r}")


print()
print("=" * 64)
print("  Nugget 02-02: Window Functions")
print("=" * 64)

conn = get_connection()
with conn.cursor() as cur:

    # ── 1. ROW_NUMBER, RANK, DENSE_RANK ──────────────────────────────────
    # ROW_NUMBER: unique 1..N, no ties
    # RANK:       same rank for ties, gap in sequence (1, 1, 3)
    # DENSE_RANK: same rank for ties, no gap (1, 1, 2)
    print()
    print("  [1] ROW_NUMBER / RANK / DENSE_RANK per region by amount")
    cur.execute(f"""
        SELECT
            order_id,
            region,
            total_amount,
            ROW_NUMBER() OVER (PARTITION BY region ORDER BY total_amount DESC) AS row_num,
            RANK()       OVER (PARTITION BY region ORDER BY total_amount DESC) AS rnk,
            DENSE_RANK() OVER (PARTITION BY region ORDER BY total_amount DESC) AS dense_rnk
        FROM {C}.{S}.sales_orders
        WHERE status = 'Shipped'
        ORDER BY region, total_amount DESC
        LIMIT 8
    """)
    rows = cur.fetchall()
    check("ROW_NUMBER/RANK/DENSE_RANK per region", rows, 4)

    # ── 2. LAG and LEAD: row-to-row comparisons ───────────────────────────
    # LAG(col, offset, default)  -- previous row value
    # LEAD(col, offset, default) -- next row value
    # Useful for period-over-period comparisons in time series.
    print()
    print("  [2] LAG/LEAD: month-over-month order amount per customer")
    cur.execute(f"""
        SELECT
            customer_id,
            order_date,
            total_amount,
            LAG(total_amount, 1, 0)  OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_order,
            LEAD(total_amount, 1, 0) OVER (PARTITION BY customer_id ORDER BY order_date) AS next_order,
            ROUND(total_amount -
                LAG(total_amount, 1, 0) OVER (PARTITION BY customer_id ORDER BY order_date), 2
            ) AS delta_from_prev
        FROM {C}.{S}.sales_orders
        WHERE status = 'Shipped'
        ORDER BY customer_id, order_date
        LIMIT 8
    """)
    rows = cur.fetchall()
    check("LAG/LEAD period comparison", rows, 4)

    # ── 3. Running total (cumulative SUM) ─────────────────────────────────
    # SUM(...) OVER (PARTITION BY x ORDER BY y ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
    # The frame clause ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    # is the default for aggregate window functions ordered by a column.
    print()
    print("  [3] Running total: cumulative revenue per region")
    cur.execute(f"""
        SELECT
            order_id,
            region,
            order_date,
            total_amount,
            SUM(total_amount) OVER (
                PARTITION BY region
                ORDER BY order_date
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ) AS running_total
        FROM {C}.{S}.sales_orders
        WHERE status = 'Shipped'
        ORDER BY region, order_date, order_id
        LIMIT 8
    """)
    rows = cur.fetchall()
    check("Running cumulative SUM per region", rows, 4)

    # ── 4. Moving average (sliding window) ────────────────────────────────
    # ROWS BETWEEN 2 PRECEDING AND CURRENT ROW = 3-row sliding window
    print()
    print("  [4] Moving average: 3-order rolling avg per customer")
    cur.execute(f"""
        SELECT
            customer_id,
            order_date,
            total_amount,
            ROUND(AVG(total_amount) OVER (
                PARTITION BY customer_id
                ORDER BY order_date
                ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
            ), 2) AS rolling_3_avg
        FROM {C}.{S}.sales_orders
        WHERE status = 'Shipped'
        ORDER BY customer_id, order_date
        LIMIT 8
    """)
    rows = cur.fetchall()
    check("3-row rolling average per customer", rows, 1)

    # ── 5. NTILE: quartile bucketing ──────────────────────────────────────
    # NTILE(n) divides rows into n roughly equal buckets.
    # Useful for quartile / decile analysis.
    print()
    print("  [5] NTILE: order value quartiles")
    cur.execute(f"""
        SELECT
            order_id,
            total_amount,
            NTILE(4) OVER (ORDER BY total_amount) AS quartile
        FROM {C}.{S}.sales_orders
        WHERE status = 'Shipped'
        ORDER BY total_amount
        LIMIT 8
    """)
    rows = cur.fetchall()
    check("NTILE quartile bucketing", rows, 4)

    # ── 6. FIRST_VALUE / LAST_VALUE ───────────────────────────────────────
    # Returns the first or last value in the window frame.
    # LAST_VALUE requires ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    # to see the true last value (default frame cuts off at CURRENT ROW).
    print()
    print("  [6] FIRST_VALUE / LAST_VALUE per region")
    cur.execute(f"""
        SELECT
            order_id,
            region,
            order_date,
            total_amount,
            FIRST_VALUE(total_amount) OVER (
                PARTITION BY region ORDER BY order_date
                ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
            ) AS first_order_amount,
            LAST_VALUE(total_amount) OVER (
                PARTITION BY region ORDER BY order_date
                ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
            ) AS last_order_amount
        FROM {C}.{S}.sales_orders
        WHERE status = 'Shipped'
        ORDER BY region, order_date
        LIMIT 6
    """)
    rows = cur.fetchall()
    check("FIRST_VALUE / LAST_VALUE per region", rows, 1)

    # ── 7. PERCENT_RANK and CUME_DIST ─────────────────────────────────────
    # PERCENT_RANK: (rank - 1) / (total_rows - 1), range [0, 1]
    # CUME_DIST:    fraction of rows <= current row, range (0, 1]
    print()
    print("  [7] PERCENT_RANK and CUME_DIST on order amounts")
    cur.execute(f"""
        SELECT
            order_id,
            total_amount,
            ROUND(PERCENT_RANK() OVER (ORDER BY total_amount), 4) AS pct_rank,
            ROUND(CUME_DIST()    OVER (ORDER BY total_amount), 4) AS cume_dist
        FROM {C}.{S}.sales_orders
        WHERE status = 'Shipped'
        ORDER BY total_amount
        LIMIT 5
    """)
    rows = cur.fetchall()
    check("PERCENT_RANK / CUME_DIST", rows, 1)

conn.close()

print()
print(DIVIDER)
passed = sum(1 for _, ok in results if ok)
total  = len(results)
print(f"  Nugget 02-02: {passed}/{total} checks passed")
print(DIVIDER)
print()
if passed < total:
    sys.exit(1)
