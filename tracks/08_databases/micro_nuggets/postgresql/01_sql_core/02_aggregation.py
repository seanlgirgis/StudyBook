"""
PURPOSE
    Demonstrate SQL aggregation: GROUP BY, HAVING, GROUPING SETS, ROLLUP, CUBE.

CONCEPTS
    GROUP BY          — Collapse rows into groups; one output per group.
    HAVING            — Filter AFTER aggregation (WHERE filters BEFORE).
    GROUPING SETS     — Multiple group-by dimensions in a single pass.
    ROLLUP            — Hierarchical subtotals (grand total at top).
    CUBE              — All possible dimension combinations (full cross-tab).

USAGE
    python 02_aggregation.py

EXPECTED OUTPUT
    ── GROUP BY: revenue per customer ──
    Alice Johnson    | 8 orders | $4,523.45

    ── ROLLUP: revenue by customer with grand total ──
    Alice Johnson    | $4,523.45
    (Grand Total)    | $25,678.90

    ── CUBE: all subtotals for status x category ──
    delivered | Electronics      | $8,900.00
    (All)     | (All Categories) | $25,678.90  <-- grand total
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _pg_connect import get_connection, LAB_SCHEMA, ensure_lab_schema


def run(conn, label, sql):
    """Execute a query and print formatted results."""
    print(f"\n── {label} {'─' * (60 - len(label))}")
    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]
        print(" | ".join(f"{c:<18}" for c in cols))
        print("-" * 80)
        for row in rows:
            print(" | ".join(f"{str(v):<18}" for v in row))
        print(f"  ({len(rows)} rows)")


def main():
    print("\n" + "=" * 64)
    print("  PostgreSQL Aggregation — GROUP BY to CUBE")
    print("=" * 64)

    conn = get_connection()
    ensure_lab_schema(conn)

    # ── Basic GROUP BY ──────────────────────────────────────────────────
    # One output row per unique customer. Use for per-entity summaries.
    run(conn, "GROUP BY: revenue per customer", f"""
        SELECT c.first_name || ' ' || c.last_name  AS customer,
               COUNT(DISTINCT o.order_id)           AS order_count,
               COALESCE(SUM(o.total_amount), 0)::numeric(10,2) AS total_revenue
        FROM   {LAB_SCHEMA}.customers c
        LEFT JOIN {LAB_SCHEMA}.orders o
               ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.first_name, c.last_name
        ORDER BY total_revenue DESC
    """)

    # ── GROUP BY + HAVING ───────────────────────────────────────────────
    # HAVING filters groups AFTER aggregation; WHERE filters rows BEFORE.
    run(conn, "HAVING: customers with revenue > $500", f"""
        SELECT c.first_name || ' ' || c.last_name  AS customer,
               COUNT(o.order_id)                    AS orders,
               SUM(o.total_amount)::numeric(10,2)   AS total_revenue
        FROM   {LAB_SCHEMA}.customers c
        JOIN   {LAB_SCHEMA}.orders o
               ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.first_name, c.last_name
        HAVING SUM(o.total_amount) > 500
        ORDER BY total_revenue DESC
    """)

    # ── ROLLUP ──────────────────────────────────────────────────────────
    # ROLLUP(a, b) produces: (a,b), (a), () — hierarchical subtotals.
    # NULL in rolled-up column marks a super-aggregate row.
    run(conn, "ROLLUP: revenue by customer with grand total", f"""
        SELECT CASE
                 WHEN GROUPING(c.first_name) = 1 THEN '(Grand Total)'
                 ELSE c.first_name || ' ' || c.last_name
               END AS customer,
               COUNT(o.order_id)                  AS orders,
               COALESCE(SUM(o.total_amount), 0)::numeric(10,2) AS revenue
        FROM   {LAB_SCHEMA}.customers c
        LEFT JOIN {LAB_SCHEMA}.orders o
               ON c.customer_id = o.customer_id
        GROUP BY ROLLUP(c.first_name, c.last_name)
        HAVING GROUPING(c.last_name) = 1   -- only show customer + grand total rows
        ORDER BY GROUPING(c.first_name), revenue DESC NULLS LAST
    """)

    # ── CUBE ────────────────────────────────────────────────────────────
    # CUBE(a, b) produces ALL combinations: (a,b), (a), (b), ().
    # 2^n groupings for n dimensions. Use for ad-hoc OLAP exploration.
    run(conn, "CUBE: all subtotals for status x category", f"""
        SELECT CASE WHEN GROUPING(o.status) = 1   THEN '(All Statuses)'
                    ELSE o.status END              AS status,
               CASE WHEN GROUPING(p.category) = 1  THEN '(All Categories)'
                    ELSE p.category END            AS category,
               COUNT(oi.item_id)                   AS items,
               SUM(oi.line_total)::numeric(10,2)   AS revenue
        FROM   {LAB_SCHEMA}.order_items oi
        JOIN   {LAB_SCHEMA}.orders o    ON o.order_id   = oi.order_id
        JOIN   {LAB_SCHEMA}.products p  ON p.product_id = oi.product_id
        GROUP BY CUBE(o.status, p.category)
        ORDER BY GROUPING(o.status), GROUPING(p.category), revenue DESC NULLS LAST
    """)

    # ── GROUPING SETS ───────────────────────────────────────────────────
    # Explicitly list exactly which groupings you want. More efficient than
    # UNION ALL of separate GROUP BY queries — scans tables only once.
    run(conn, "GROUPING SETS: custom aggregation dimensions", f"""
        SELECT COALESCE(c.first_name || ' ' || c.last_name, '(All Customers)') AS customer,
               COALESCE(o.status, '(All Statuses)')  AS status,
               COUNT(o.order_id)                     AS orders,
               COALESCE(SUM(o.total_amount), 0)::numeric(10,2) AS revenue
        FROM   {LAB_SCHEMA}.customers c
        LEFT JOIN {LAB_SCHEMA}.orders o
               ON c.customer_id = o.customer_id
        GROUP BY GROUPING SETS (
            (c.first_name, c.last_name),   -- revenue per customer
            (o.status),                     -- revenue per status
            ()                              -- grand total
        )
        ORDER BY GROUPING(c.first_name), GROUPING(o.status), revenue DESC NULLS LAST
    """)

    conn.close()
    print("\n  Key takeaway: GROUP BY collapses rows, HAVING filters groups, ROLLUP gives hierarchical subtotals, CUBE gives all combos.\n")


if __name__ == "__main__":
    main()
