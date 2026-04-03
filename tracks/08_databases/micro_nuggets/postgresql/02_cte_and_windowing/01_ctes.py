"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 02-01 · Common Table Expressions (CTEs)                              ║
║  Breaking complex queries into readable, composable steps.                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Demonstrates non-recursive and recursive CTEs — PostgreSQL's most powerful
query structuring tool.

CONCEPTS
────────
WITH clause (CTE):
  - Names a subquery so you can reference it by name later in the same query.
  - Makes complex queries readable — each CTE is a named step.
  - In PostgreSQL < 12, CTEs are "optimization fences" — always materialized.
    This means the CTE runs fully even if the outer query doesn't need all rows.
  - In PostgreSQL 12+, the optimizer can inline CTEs when safe (like subqueries).
  - Use MATERIALIZED keyword to force materialization: WITH cte AS MATERIALIZED (...)

Recursive CTE:
  - WITH RECURSIVE cte_name AS (
        SELECT ...  -- anchor member (base case)
      UNION ALL
        SELECT ...  -- recursive member (references cte_name)
    )
  - Runs until the recursive member returns no rows.
  - Used for: hierarchical data, date series generation, graph traversal.

USAGE
─────
    python 01_ctes.py

EXPECTED OUTPUT
───────────────
    ── CTEs ──────────────────────────────────────────────

      ── Revenue by Customer (CTE) ──────────────────────
        Customer          Orders  Revenue
        ----------------  ------  ---------
        Alice Johnson     8       2,349.97
        ...

      ── Conversion Funnel (CTE chain) ──────────────────
        Step              Count  Conversion
        ----------------  -----  ----------
        page_view         80     100.0%
        product_view      50     62.5%
        add_to_cart       30     37.5%
        purchase          20     25.0%

      ── Date Series (Recursive CTE) ────────────────────
        Generated 30 dates from 2024-01-01 to 2024-01-30
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _pg_connect import get_connection, LAB_SCHEMA, ensure_lab_schema

conn = get_connection()
ensure_lab_schema(conn)

print("\n── CTEs ──────────────────────────────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Simple CTE — revenue by customer
#    A CTE lets you name an intermediate result and reference it cleanly.
#    Without CTEs, this would be a nested subquery — harder to read.
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Revenue by Customer (CTE) ──────────────────────")
with conn.cursor() as cur:
    cur.execute(f"""
        WITH customer_revenue AS (
            SELECT
                c.customer_id,
                c.first_name || ' ' || c.last_name AS customer_name,
                COUNT(o.order_id)  AS order_count,
                COALESCE(SUM(o.total_amount), 0) AS total_revenue
            FROM   {LAB_SCHEMA}.customers c
            LEFT   JOIN {LAB_SCHEMA}.orders o
                   ON c.customer_id = o.customer_id
            GROUP  BY c.customer_id, c.first_name, c.last_name
        )
        SELECT customer_name, order_count, total_revenue
        FROM   customer_revenue
        ORDER  BY total_revenue DESC
        LIMIT  10
    """)
    rows = cur.fetchall()

print(f"    {'Customer':<18} {'Orders':<7} {'Revenue'}")
print(f"    {'-'*18} {'-'*7} {'-'*10}")
for name, orders, revenue in rows:
    print(f"    {name:<18} {orders:<7} ${revenue:>9,.2f}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. CTE chain — conversion funnel
#    Multiple CTEs in one query — each builds on the previous.
#    This is how you model a funnel: count distinct users at each step.
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Conversion Funnel (CTE chain) ──────────────────")
with conn.cursor() as cur:
    cur.execute(f"""
        WITH funnel AS (
            SELECT
                event_type,
                COUNT(DISTINCT COALESCE(customer_id::text, session_id)) AS unique_users
            FROM   {LAB_SCHEMA}.events
            WHERE  event_type IN ('page_view', 'product_view', 'add_to_cart', 'purchase')
            GROUP  BY event_type
        ),
        ordered AS (
            SELECT
                event_type,
                unique_users,
                ROW_NUMBER() OVER (ORDER BY
                    CASE event_type
                        WHEN 'page_view'     THEN 1
                        WHEN 'product_view'  THEN 2
                        WHEN 'add_to_cart'   THEN 3
                        WHEN 'purchase'      THEN 4
                    END
                ) AS step_num
            FROM funnel
        )
        SELECT
            o.event_type,
            o.unique_users,
            ROUND(100.0 * o.unique_users / NULLIF(f.unique_users, 0), 1) AS pct_of_top
        FROM ordered o
        JOIN ordered f ON f.step_num = 1
        ORDER BY o.step_num
    """)
    rows = cur.fetchall()

print(f"    {'Step':<18} {'Count':<7} {'% of Top'}")
print(f"    {'-'*18} {'-'*7} {'-'*9}")
for step, count, pct in rows:
    print(f"    {step:<18} {count:<7} {pct:>8.1f}%")

# ─────────────────────────────────────────────────────────────────────────────
# 3. Recursive CTE — generate a date series
#    WITH RECURSIVE runs the anchor query once, then repeatedly applies
#    the recursive member until it returns no rows.
#    This is PostgreSQL's equivalent of a numbers/dates table generator.
#
#    Alternative: SELECT generate_series('2024-01-01'::date, '2024-01-30'::date, '1 day')
#    But recursive CTEs work on any database that supports them (not just PG).
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Date Series (Recursive CTE) ────────────────────")
with conn.cursor() as cur:
    cur.execute("""
        WITH RECURSIVE dates AS (
            SELECT DATE '2024-01-01' AS d
            UNION ALL
            SELECT d + 1
            FROM   dates
            WHERE  d < DATE '2024-01-30'
        )
        SELECT COUNT(*) AS date_count, MIN(d) AS start_date, MAX(d) AS end_date
        FROM   dates
    """)
    count, start, end = cur.fetchone()
    print(f"    Generated {count} dates from {start} to {end}")

conn.close()
print()
