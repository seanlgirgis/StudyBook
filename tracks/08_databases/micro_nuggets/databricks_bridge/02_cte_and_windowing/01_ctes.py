"""
NUGGET 02-01 (Bridge) -- CTEs (Common Table Expressions)
==========================================================
Covers: basic CTEs, chained CTEs, CTEs for deduplication,
        and recursive-style patterns using iterative CTEs.

PostgreSQL -> Databricks SQL transfer notes:
  - WITH ... AS (...) syntax is identical
  - Multiple CTEs chained with commas: identical
  - Recursive CTEs (WITH RECURSIVE): Databricks SQL does NOT support
    WITH RECURSIVE. The workaround is iterative processing in Python
    or using Spark DataFrame API for graph traversal.
  - Databricks CTEs are non-materialized by default (inlined into plan).
    PostgreSQL CTEs are materialized by default in PG < 12, inlined in PG >= 12.

Snowflake note:
  Snowflake also supports CTEs but NOT WITH RECURSIVE.
  Both Databricks and Snowflake require graph/recursive work to be done
  in application code or procedural blocks.

Usage:
    python 01_ctes.py
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
print("  Nugget 02-01: CTEs")
print("=" * 64)

conn = get_connection()
with conn.cursor() as cur:

    # ── 1. Single CTE ──────────────────────────────────────────────────────
    # CTE makes complex queries readable by naming intermediate results.
    # The planner inlines this unless it is referenced multiple times
    # (in which case it may materialize it as an optimization barrier).
    print()
    print("  [1] Single CTE: shipped orders summary")
    cur.execute(f"""
        WITH shipped_orders AS (
            SELECT
                customer_id,
                COUNT(*)          AS order_count,
                SUM(total_amount) AS total_spend
            FROM {C}.{S}.sales_orders
            WHERE status = 'Shipped'
            GROUP BY customer_id
        )
        SELECT
            c.customer_name,
            so.order_count,
            so.total_spend
        FROM shipped_orders so
        INNER JOIN {C}.{S}.customers c ON so.customer_id = c.customer_id
        ORDER BY total_spend DESC
        LIMIT 5
    """)
    rows = cur.fetchall()
    check("Single CTE shipped summary", rows, 5)

    # ── 2. Chained CTEs ────────────────────────────────────────────────────
    # Multiple CTEs separated by commas. Each CTE can reference earlier ones.
    # Identical syntax in PostgreSQL, Snowflake, and BigQuery.
    print()
    print("  [2] Chained CTEs: category revenue ranked by region")
    cur.execute(f"""
        WITH order_details AS (
            SELECT
                o.region,
                p.category,
                o.total_amount
            FROM {C}.{S}.sales_orders o
            INNER JOIN {C}.{S}.products p ON o.product_id = p.product_id
            WHERE o.status = 'Shipped'
        ),
        region_category_revenue AS (
            SELECT
                region,
                category,
                SUM(total_amount) AS revenue
            FROM order_details
            GROUP BY region, category
        ),
        ranked AS (
            SELECT
                region,
                category,
                revenue,
                RANK() OVER (PARTITION BY region ORDER BY revenue DESC) AS rank_in_region
            FROM region_category_revenue
        )
        SELECT region, category, revenue, rank_in_region
        FROM ranked
        WHERE rank_in_region = 1
        ORDER BY region
    """)
    rows = cur.fetchall()
    check("Chained CTEs top category per region", rows, 1)

    # ── 3. CTE used multiple times ─────────────────────────────────────────
    # When a CTE is referenced more than once, Databricks may materialize it.
    # In PostgreSQL >= 12, this requires the MATERIALIZED keyword to force it.
    print()
    print("  [3] CTE referenced twice: region vs global comparison")
    cur.execute(f"""
        WITH region_revenue AS (
            SELECT
                region,
                SUM(total_amount) AS revenue
            FROM {C}.{S}.sales_orders
            WHERE status = 'Shipped'
            GROUP BY region
        )
        SELECT
            r.region,
            r.revenue                                                AS region_revenue,
            (SELECT SUM(revenue) FROM region_revenue)               AS global_revenue,
            ROUND(r.revenue * 100.0 /
                  (SELECT SUM(revenue) FROM region_revenue), 2)     AS pct_of_total
        FROM region_revenue r
        ORDER BY pct_of_total DESC
    """)
    rows = cur.fetchall()
    check("CTE referenced twice (pct of total)", rows, 1)

    # ── 4. CTE for deduplication ──────────────────────────────────────────
    # CTEs are the standard pattern for ROW_NUMBER-based deduplication.
    # This is the same approach used in PostgreSQL DELETE using CTEs,
    # Snowflake MERGE, and Databricks MERGE (see 04_de_patterns).
    print()
    print("  [4] CTE deduplication pattern (dry-run SELECT)")
    cur.execute(f"""
        WITH ranked_orders AS (
            SELECT
                order_id,
                customer_id,
                product_id,
                order_date,
                total_amount,
                ROW_NUMBER() OVER (
                    PARTITION BY customer_id, product_id, order_date
                    ORDER BY order_id
                ) AS rn
            FROM {C}.{S}.sales_orders
        )
        SELECT order_id, customer_id, product_id, order_date, total_amount
        FROM ranked_orders
        WHERE rn = 1
        ORDER BY order_id
        LIMIT 5
    """)
    rows = cur.fetchall()
    check("CTE dedup (rn=1, limit 5)", rows, 5)

    # ── 5. CTE as a readability refactor of a subquery ────────────────────
    # This is the exact same query as Nugget 01-03 derived-table example,
    # rewritten as a CTE. Plans are often identical; readability wins.
    print()
    print("  [5] CTE vs subquery equivalence")
    cur.execute(f"""
        WITH region_summary AS (
            SELECT
                region,
                SUM(total_amount)  AS total_revenue,
                COUNT(*)           AS order_count
            FROM {C}.{S}.sales_orders
            WHERE status = 'Shipped'
            GROUP BY region
        )
        SELECT region, total_revenue, order_count
        FROM region_summary
        WHERE total_revenue > 1000
        ORDER BY total_revenue DESC
    """)
    rows = cur.fetchall()
    check("CTE equivalent to derived table", rows, 1)

conn.close()

print()
print(DIVIDER)
passed = sum(1 for _, ok in results if ok)
total  = len(results)
print(f"  Nugget 02-01: {passed}/{total} checks passed")
print()
print("  NOTE: Databricks SQL does NOT support WITH RECURSIVE.")
print("        Use Spark DataFrame API or iterative Python for graph work.")
print(DIVIDER)
print()
if passed < total:
    sys.exit(1)
