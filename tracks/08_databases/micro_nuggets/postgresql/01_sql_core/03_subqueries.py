"""
PURPOSE
    Demonstrate subquery patterns: correlated, EXISTS/NOT EXISTS, IN/NOT IN, ANY/ALL.

CONCEPTS
    Scalar subquery     — Returns a single value; usable as any expression.
    Correlated subquery — References outer columns; runs once per outer row.
    EXISTS / NOT EXISTS — Tests row existence; short-circuits on first match.
    IN / NOT IN         — Set membership; NOT IN is dangerous with NULLs.
    ANY / ALL           — Compare a value against a set from a subquery.

USAGE
    python 03_subqueries.py

EXPECTED OUTPUT
    ── Scalar: overall average order value ──
    $512.34

    ── Correlated: customers with above-average orders ──
    Alice Johnson    | avg $623.45  (overall avg: $512.34)

    ── NOT EXISTS: customers who never ordered ──
    Jack Taylor      | signed up 2023-10-01

    ── ALL: products pricier than every Accessory ──
    Laptop Pro 15    | $1,299.99
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
        print(" | ".join(f"{c:<20}" for c in cols))
        print("-" * 80)
        for row in rows:
            print(" | ".join(f"{str(v):<20}" for v in row))
        print(f"  ({len(rows)} rows)")


def main():
    print("\n" + "=" * 64)
    print("  PostgreSQL Subqueries — Correlated, EXISTS, IN, ANY/ALL")
    print("=" * 64)

    conn = get_connection()
    ensure_lab_schema(conn)

    # ── Correlated subquery ─────────────────────────────────────────────
    # Inner query references outer c.customer_id, so it re-executes per row.
    # PERFORMANCE: For large tables, prefer JOIN + window function instead.
    run(conn, "Correlated: customers with above-average orders", f"""
        SELECT c.first_name || ' ' || c.last_name  AS customer,
               (SELECT ROUND(AVG(o2.total_amount), 2)
                FROM   {LAB_SCHEMA}.orders o2
                WHERE  o2.customer_id = c.customer_id
                  AND  o2.status <> 'cancelled'
               )::numeric(10,2) AS personal_avg,
               (SELECT ROUND(AVG(o3.total_amount), 2)
                FROM   {LAB_SCHEMA}.orders o3
                WHERE  o3.status <> 'cancelled'
               )::numeric(10,2) AS overall_avg
        FROM   {LAB_SCHEMA}.customers c
        WHERE  (SELECT AVG(o2.total_amount)
                FROM   {LAB_SCHEMA}.orders o2
                WHERE  o2.customer_id = c.customer_id
                  AND  o2.status <> 'cancelled'
               ) > (SELECT AVG(o3.total_amount)
                     FROM   {LAB_SCHEMA}.orders o3
                     WHERE  o3.status <> 'cancelled')
        ORDER BY personal_avg DESC
    """)

    # ── NOT EXISTS ──────────────────────────────────────────────────────
    # Finds rows where subquery returns ZERO rows. SAFER than NOT IN with NULLs.
    run(conn, "NOT EXISTS: customers who never ordered", f"""
        SELECT c.first_name || ' ' || c.last_name  AS customer,
               c.signup_date,
               c.city
        FROM   {LAB_SCHEMA}.customers c
        WHERE  NOT EXISTS (
            SELECT 1
            FROM   {LAB_SCHEMA}.orders o
            WHERE  o.customer_id = c.customer_id
        )
        ORDER BY c.signup_date
    """)

    # ── IN ──────────────────────────────────────────────────────────────
    # Tests value match against subquery result set. Optimizer converts to semi-join.
    run(conn, "IN: products in delivered orders", f"""
        SELECT DISTINCT p.name,
               p.category,
               p.price::numeric(10,2) AS price
        FROM   {LAB_SCHEMA}.products p
        WHERE  p.product_id IN (
            SELECT oi.product_id
            FROM   {LAB_SCHEMA}.order_items oi
            JOIN   {LAB_SCHEMA}.orders o ON o.order_id = oi.order_id
            WHERE  o.status = 'delivered'
        )
        ORDER BY p.price DESC
    """)

    # ── ANY ─────────────────────────────────────────────────────────────
    # value < ANY(subquery) = "less than at least one value" (= < MAX).
    run(conn, "ANY: products cheaper than some Electronics item", f"""
        SELECT p.name,
               p.category,
               p.price::numeric(10,2) AS price
        FROM   {LAB_SCHEMA}.products p
        WHERE  p.price < ANY (
            SELECT p2.price
            FROM   {LAB_SCHEMA}.products p2
            WHERE  p2.category = 'Electronics'
        )
        AND p.category <> 'Electronics'
        ORDER BY p.price DESC
    """)

    # ── ALL ─────────────────────────────────────────────────────────────
    # value > ALL(subquery) = "greater than every value" (= > MAX).
    run(conn, "ALL: products pricier than every Accessory", f"""
        SELECT p.name,
               p.category,
               p.price::numeric(10,2) AS price
        FROM   {LAB_SCHEMA}.products p
        WHERE  p.price > ALL (
            SELECT p2.price
            FROM   {LAB_SCHEMA}.products p2
            WHERE  p2.category = 'Accessories'
        )
        AND p.category <> 'Accessories'
        ORDER BY p.price DESC
    """)

    conn.close()
    print("\n  Key takeaway: EXISTS for existence checks, IN for small sets, correlated for per-row comparisons, ANY/ALL for set comparisons.\n")


if __name__ == "__main__":
    main()
