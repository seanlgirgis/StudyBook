"""
NUGGET 01-03 (Bridge) -- Subqueries in Databricks SQL
=======================================================
Covers: correlated subqueries, IN/EXISTS, scalar subqueries,
        derived tables, lateral views.

PostgreSQL -> Databricks SQL transfer notes:
  - Scalar subqueries in SELECT: identical syntax
  - IN/NOT IN: identical; Databricks rewrites to semi/anti-joins
  - EXISTS/NOT EXISTS: identical; preferred over IN for NULL safety
  - LATERAL VIEW: Databricks uses LATERAL VIEW EXPLODE for array expansion
    (PostgreSQL uses UNNEST, Snowflake uses FLATTEN/LATERAL JOIN)
  - Correlated subqueries are supported but expensive -- prefer window
    functions or CTEs for repeated correlated patterns

Usage:
    python 03_subqueries.py
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
print("  Nugget 01-03: Subqueries")
print("=" * 64)

conn = get_connection()
with conn.cursor() as cur:

    # ── 1. Scalar subquery in SELECT ───────────────────────────────────────
    # A scalar subquery returns exactly one row and one column.
    # Used here to compare each order to the overall average.
    # PostgreSQL: identical syntax.
    # Note: if the subquery returns > 1 row, Databricks raises an error.
    print()
    print("  [1] Scalar subquery: orders vs overall average")
    cur.execute(f"""
        SELECT
            order_id,
            customer_id,
            total_amount,
            (SELECT AVG(total_amount) FROM {C}.{S}.sales_orders
             WHERE status = 'Shipped') AS avg_shipped,
            ROUND(total_amount -
                  (SELECT AVG(total_amount) FROM {C}.{S}.sales_orders
                   WHERE status = 'Shipped'), 2) AS diff_from_avg
        FROM {C}.{S}.sales_orders
        WHERE status = 'Shipped'
        ORDER BY diff_from_avg DESC
        LIMIT 5
    """)
    rows = cur.fetchall()
    check("Scalar subquery avg comparison", rows, 1)

    # ── 2. IN subquery: customers who bought Electronics ──────────────────
    # IN is rewritten internally to a semi-join by Databricks.
    # PostgreSQL rewrites IN to semi-join too.
    # Caveat: IN returns FALSE for NULL comparisons -- use EXISTS for
    # NULL-safe filtering.
    print()
    print("  [2] IN subquery: customers who ordered Electronics")
    cur.execute(f"""
        SELECT customer_id, customer_name, region
        FROM {C}.{S}.customers
        WHERE customer_id IN (
            SELECT DISTINCT o.customer_id
            FROM {C}.{S}.sales_orders o
            INNER JOIN {C}.{S}.products p ON o.product_id = p.product_id
            WHERE p.category = 'Electronics'
        )
        ORDER BY customer_id
    """)
    rows = cur.fetchall()
    check("IN subquery Electronics buyers", rows, 1)

    # ── 3. NOT IN vs NOT EXISTS: anti-join ────────────────────────────────
    # NOT EXISTS is NULL-safe; NOT IN is not (returns no rows if subquery
    # contains any NULL). Best practice: use NOT EXISTS.
    print()
    print("  [3] NOT EXISTS: customers with no cancelled orders")
    cur.execute(f"""
        SELECT c.customer_id, c.customer_name
        FROM {C}.{S}.customers c
        WHERE NOT EXISTS (
            SELECT 1
            FROM {C}.{S}.sales_orders o
            WHERE o.customer_id = c.customer_id
              AND o.status = 'Cancelled'
        )
        ORDER BY c.customer_id
        LIMIT 5
    """)
    rows = cur.fetchall()
    check("NOT EXISTS no-cancelled-order customers", rows, 1)

    # ── 4. Derived table (subquery in FROM) ───────────────────────────────
    # A subquery in FROM acts like a temporary table for the outer query.
    # In Databricks this is usually a candidate to replace with a CTE
    # (next nugget) for readability. Both approaches produce identical plans.
    print()
    print("  [4] Derived table: top-spending regions")
    cur.execute(f"""
        SELECT
            region_summary.region,
            region_summary.total_revenue,
            region_summary.order_count
        FROM (
            SELECT
                region,
                SUM(total_amount)  AS total_revenue,
                COUNT(*)           AS order_count
            FROM {C}.{S}.sales_orders
            WHERE status = 'Shipped'
            GROUP BY region
        ) AS region_summary
        WHERE region_summary.total_revenue > 1000
        ORDER BY total_revenue DESC
    """)
    rows = cur.fetchall()
    check("Derived table top regions", rows, 1)

    # ── 5. Correlated subquery: above-average spend per region ────────────
    # A correlated subquery references columns from the outer query.
    # Each outer row triggers a re-evaluation of the inner query.
    # Expensive but sometimes the clearest expression of intent.
    # Prefer window functions (next module) for repeated correlated patterns.
    print()
    print("  [5] Correlated subquery: orders above regional average")
    cur.execute(f"""
        SELECT
            o.order_id,
            o.customer_id,
            o.region,
            o.total_amount
        FROM {C}.{S}.sales_orders o
        WHERE o.total_amount > (
            SELECT AVG(i.total_amount)
            FROM {C}.{S}.sales_orders i
            WHERE i.region = o.region
              AND i.status = 'Shipped'
        )
        AND o.status = 'Shipped'
        ORDER BY o.region, o.total_amount DESC
        LIMIT 5
    """)
    rows = cur.fetchall()
    check("Correlated: above regional average", rows, 1)

    # ── 6. Subquery in HAVING ──────────────────────────────────────────────
    # Subqueries can appear in HAVING clauses to compare group aggregates
    # against global aggregates or external values.
    print()
    print("  [6] Subquery in HAVING: above-average revenue regions")
    cur.execute(f"""
        SELECT
            region,
            SUM(total_amount) AS revenue
        FROM {C}.{S}.sales_orders
        WHERE status = 'Shipped'
        GROUP BY region
        HAVING SUM(total_amount) > (
            SELECT AVG(region_rev)
            FROM (
                SELECT region, SUM(total_amount) AS region_rev
                FROM {C}.{S}.sales_orders
                WHERE status = 'Shipped'
                GROUP BY region
            ) AS sub
        )
        ORDER BY revenue DESC
    """)
    rows = cur.fetchall()
    check("HAVING with subquery (above avg region)", rows, 1)

conn.close()

print()
print(DIVIDER)
passed = sum(1 for _, ok in results if ok)
total  = len(results)
print(f"  Nugget 01-03: {passed}/{total} checks passed")
print(DIVIDER)
print()
if passed < total:
    sys.exit(1)
