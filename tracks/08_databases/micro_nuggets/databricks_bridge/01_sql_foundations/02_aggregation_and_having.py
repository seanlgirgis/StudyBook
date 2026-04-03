"""
NUGGET 01-02 (Bridge) -- Aggregation and HAVING
=================================================
Covers: GROUP BY, aggregate functions, HAVING, ROLLUP, CUBE, GROUPING SETS.

PostgreSQL -> Databricks SQL transfer notes:
  - GROUP BY / HAVING syntax is identical
  - ROLLUP, CUBE, GROUPING SETS work the same way
  - FILTER clause on aggregates supported in both (SQL:2003 standard)
  - Databricks adds APPROX_COUNT_DISTINCT for approximate cardinality
    (uses HyperLogLog sketch -- faster than COUNT(DISTINCT x) on big data)

Snowflake note:
  Snowflake also supports ROLLUP/CUBE/GROUPING SETS with identical syntax.
  APPROX_COUNT_DISTINCT is HLL_ESTIMATE() in Snowflake.

Usage:
    python 02_aggregation_and_having.py
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
print("  Nugget 01-02: Aggregation and HAVING")
print("=" * 64)

conn = get_connection()
with conn.cursor() as cur:

    # ── 1. Basic GROUP BY + standard aggregates ────────────────────────────
    print()
    print("  [1] Basic GROUP BY: sales metrics by region")
    cur.execute(f"""
        SELECT
            region,
            COUNT(*)                    AS order_count,
            SUM(total_amount)           AS revenue,
            AVG(total_amount)           AS avg_order,
            MIN(total_amount)           AS min_order,
            MAX(total_amount)           AS max_order
        FROM {C}.{S}.sales_orders
        WHERE status = 'Shipped'
        GROUP BY region
        ORDER BY revenue DESC
    """)
    rows = cur.fetchall()
    check("GROUP BY region revenue", rows, 1)

    # ── 2. HAVING: filter on aggregated result ─────────────────────────────
    # HAVING filters AFTER aggregation, WHERE filters BEFORE.
    # PostgreSQL analogy: identical.
    # Rule of thumb: use WHERE for row-level filters, HAVING for group filters.
    print()
    print("  [2] HAVING: regions with revenue > 2000")
    cur.execute(f"""
        SELECT
            region,
            COUNT(*)            AS order_count,
            SUM(total_amount)   AS revenue
        FROM {C}.{S}.sales_orders
        WHERE status != 'Cancelled'
        GROUP BY region
        HAVING SUM(total_amount) > 2000
        ORDER BY revenue DESC
    """)
    rows = cur.fetchall()
    check("HAVING revenue > 2000", rows, 1)

    # ── 3. Multi-level GROUP BY ────────────────────────────────────────────
    print()
    print("  [3] Multi-level GROUP BY: category + region")
    cur.execute(f"""
        SELECT
            p.category,
            o.region,
            COUNT(*)            AS orders,
            SUM(o.total_amount) AS revenue
        FROM {C}.{S}.sales_orders o
        INNER JOIN {C}.{S}.products p ON o.product_id = p.product_id
        GROUP BY p.category, o.region
        ORDER BY p.category, revenue DESC
    """)
    rows = cur.fetchall()
    check("Category + region breakdown", rows, 1)

    # ── 4. COUNT DISTINCT ──────────────────────────────────────────────────
    # COUNT(DISTINCT col) is exact but scans the full column.
    # On very large datasets, use APPROX_COUNT_DISTINCT for speed.
    print()
    print("  [4] COUNT(DISTINCT): unique customers per region")
    cur.execute(f"""
        SELECT
            region,
            COUNT(DISTINCT customer_id)         AS unique_customers,
            APPROX_COUNT_DISTINCT(customer_id)  AS approx_customers
        FROM {C}.{S}.sales_orders
        GROUP BY region
        ORDER BY unique_customers DESC
    """)
    rows = cur.fetchall()
    check("COUNT DISTINCT customers per region", rows, 1)

    # ── 5. ROLLUP: subtotals and grand total ───────────────────────────────
    # ROLLUP generates subtotal rows for hierarchical groupings.
    # Equivalent in PostgreSQL, Snowflake, and SQL Server.
    # NULL in a ROLLUP row = the subtotal/grand-total aggregation level.
    print()
    print("  [5] ROLLUP: revenue with subtotals by region+status")
    cur.execute(f"""
        SELECT
            COALESCE(region, '(ALL REGIONS)')   AS region,
            COALESCE(status, '(ALL STATUSES)')  AS status,
            SUM(total_amount)                   AS revenue
        FROM {C}.{S}.sales_orders
        GROUP BY ROLLUP(region, status)
        ORDER BY region, status
    """)
    rows = cur.fetchall()
    check("ROLLUP region+status", rows, 2)

    # ── 6. GROUPING SETS: custom grouping combinations ─────────────────────
    # GROUPING SETS lets you specify exactly which combinations to aggregate.
    # More flexible than ROLLUP or CUBE.
    print()
    print("  [6] GROUPING SETS: by region only + by status only")
    cur.execute(f"""
        SELECT
            region,
            status,
            SUM(total_amount) AS revenue
        FROM {C}.{S}.sales_orders
        GROUP BY GROUPING SETS ((region), (status))
        ORDER BY region NULLS LAST, status NULLS LAST
    """)
    rows = cur.fetchall()
    check("GROUPING SETS region | status", rows, 2)

    # ── 7. FILTER clause on aggregates ────────────────────────────────────
    # FILTER (WHERE ...) applies a per-aggregate row filter.
    # Equivalent to conditional SUM pattern: SUM(CASE WHEN ... END)
    # PostgreSQL supports this; SQL standard (SQL:2003).
    print()
    print("  [7] FILTER on aggregate: shipped vs cancelled revenue")
    cur.execute(f"""
        SELECT
            region,
            SUM(total_amount) FILTER (WHERE status = 'Shipped')   AS shipped_revenue,
            SUM(total_amount) FILTER (WHERE status = 'Cancelled') AS cancelled_revenue,
            COUNT(*)          FILTER (WHERE status = 'Returned')  AS return_count
        FROM {C}.{S}.sales_orders
        GROUP BY region
        ORDER BY shipped_revenue DESC NULLS LAST
    """)
    rows = cur.fetchall()
    check("FILTER per-aggregate revenue", rows, 1)

conn.close()

print()
print(DIVIDER)
passed = sum(1 for _, ok in results if ok)
total  = len(results)
print(f"  Nugget 01-02: {passed}/{total} checks passed")
print(DIVIDER)
print()
if passed < total:
    sys.exit(1)
