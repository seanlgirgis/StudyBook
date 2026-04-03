"""
PURPOSE
    Demonstrate every SQL join type using the lab e-commerce schema.

CONCEPTS
    INNER JOIN      — Only rows with matches in BOTH tables.
    LEFT JOIN       — All left rows; NULLs when right has no match.
    RIGHT JOIN      — All right rows; NULLs when left has no match.
    FULL OUTER JOIN — All rows from BOTH tables; NULLs where no match.
    CROSS JOIN      — Cartesian product: every left row x every right row.

USAGE
    python 01_joins.py

EXPECTED OUTPUT
    ── INNER JOIN: customers with orders ──
    Alice Johnson    | 5 orders | $4,523.45
    ...

    ── LEFT JOIN: all customers + order count ──
    Jack Taylor      | 0 orders   <-- preserved with NULL right side

    ── CROSS JOIN: products x categories ──
    Laptop Pro 15    | Accessories  (cross-category pairs only)
    ... (8 products x 3 categories = 24 rows, limited to 12)
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _pg_connect import get_connection, LAB_SCHEMA, ensure_lab_schema


def run(conn, label, sql):
    """Execute a query and print results with a header."""
    print(f"\n── {label} {'─' * (60 - len(label))}")
    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]
        print(" | ".join(f"{c:<16}" for c in cols))
        print("-" * 80)
        for row in rows:
            print(" | ".join(f"{str(v):<16}" for v in row))
        print(f"  ({len(rows)} rows)")


def main():
    print("\n" + "=" * 64)
    print("  PostgreSQL Joins — INNER, LEFT, RIGHT, FULL, CROSS")
    print("=" * 64)

    conn = get_connection()
    ensure_lab_schema(conn)

    # ── INNER JOIN ──────────────────────────────────────────────────────
    # Only customers with at least one order. Optimizer uses hash/merge join.
    run(conn, "INNER JOIN: customers with orders", f"""
        SELECT c.first_name || ' ' || c.last_name  AS customer,
               COUNT(o.order_id)                    AS order_count,
               COALESCE(SUM(o.total_amount), 0)::numeric(10,2) AS total_spent
        FROM   {LAB_SCHEMA}.customers c
        INNER JOIN {LAB_SCHEMA}.orders o
               ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.first_name, c.last_name
        ORDER BY total_spent DESC
        LIMIT 5
    """)

    # ── LEFT JOIN ───────────────────────────────────────────────────────
    # ALL customers, even those with zero orders. NULLs = no matching order.
    run(conn, "LEFT JOIN: all customers + order count", f"""
        SELECT c.first_name || ' ' || c.last_name  AS customer,
               c.city,
               COUNT(o.order_id)                    AS order_count
        FROM   {LAB_SCHEMA}.customers c
        LEFT JOIN {LAB_SCHEMA}.orders o
               ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.first_name, c.last_name, c.city
        ORDER BY order_count DESC, customer
    """)

    # ── RIGHT JOIN ──────────────────────────────────────────────────────
    # ALL orders, even those with no customer. Rarely used — prefer LEFT JOIN.
    run(conn, "RIGHT JOIN: all orders + customer info", f"""
        SELECT c.first_name || ' ' || c.last_name  AS customer,
               o.order_id,
               o.order_date,
               o.status
        FROM   {LAB_SCHEMA}.customers c
        RIGHT JOIN {LAB_SCHEMA}.orders o
               ON c.customer_id = o.customer_id
        ORDER BY o.order_id
        LIMIT 10
    """)

    # ── FULL OUTER JOIN ─────────────────────────────────────────────────
    # ALL rows from BOTH tables. Use case: find orphaned records on either side.
    run(conn, "FULL OUTER JOIN: unmatched on either side", f"""
        SELECT c.first_name || ' ' || c.last_name  AS customer,
               o.order_id,
               o.status
        FROM   {LAB_SCHEMA}.customers c
        FULL OUTER JOIN {LAB_SCHEMA}.orders o
               ON c.customer_id = o.customer_id
        WHERE  o.order_id IS NULL    -- customers with NO orders
            OR c.customer_id IS NULL -- orders with NO customer (orphans)
        ORDER BY customer NULLS LAST, o.order_id
    """)

    # ── CROSS JOIN ──────────────────────────────────────────────────────
    # Cartesian product: every left row x every right row.
    # Use case: generate all combinations. WARNING: rows = left * right.
    run(conn, "CROSS JOIN: products x categories", f"""
        SELECT p.name          AS product,
               c.category      AS category_combination
        FROM   {LAB_SCHEMA}.products p
        CROSS JOIN (SELECT DISTINCT category FROM {LAB_SCHEMA}.products) c
        WHERE  p.category <> c.category   -- show only cross-category pairs
        ORDER BY p.name, c.category
        LIMIT 12
    """)

    conn.close()
    print("\n  Key takeaway: INNER for intersections, OUTER for completeness, CROSS for combinations.\n")


if __name__ == "__main__":
    main()
