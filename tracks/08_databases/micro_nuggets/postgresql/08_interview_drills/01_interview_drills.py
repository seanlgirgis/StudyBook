"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 08-01 · Interview SQL Drills                                         ║
║  Common DE interview questions with model solutions.                         ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Practical SQL interview problems with solutions using our lab data.

CONCEPTS
────────
These are the patterns interviewers actually ask:
  1. Second highest salary → DENSE_RANK or subquery
  2. Consecutive numbers → LAG/LEAD or self-join
  3. Department top 3 salaries → ROW_NUMBER + PARTITION BY
  4. Month-over-month growth → LAG on aggregated data
  5. Find duplicates → GROUP BY + HAVING COUNT > 1
  6. Gaps in sequences → generate_series + LEFT JOIN

USAGE
─────
    python 01_interview_drills.py

EXPECTED OUTPUT
───────────────
    ── Interview Drills ──────────────────────────────────────

      Q1: Second highest product price per category
        Category       Product          Price
        -------------  ---------------  ---------
        Electronics    Monitor 27"      349.99
        ...

      Q2: Customers with 3+ orders
        Customer          Orders
        ----------------  ------
        Alice Johnson     8
        ...
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _pg_connect import get_connection, LAB_SCHEMA, ensure_lab_schema

conn = get_connection()
ensure_lab_schema(conn)

print("\n── Interview Drills ──────────────────────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# Q1: Second highest price per category
#    Interview tests: window functions, DENSE_RANK
# ─────────────────────────────────────────────────────────────────────────────
print("\n  Q1: Second highest product price per category")
with conn.cursor() as cur:
    cur.execute(f"""
        WITH ranked AS (
            SELECT name, category, price,
                   DENSE_RANK() OVER (PARTITION BY category ORDER BY price DESC) AS rn
            FROM {LAB_SCHEMA}.products
        )
        SELECT category, name, price
        FROM ranked WHERE rn = 2
        ORDER BY category
    """)
    rows = cur.fetchall()
    if rows:
        print(f"    {'Category':<14} {'Product':<16} {'Price'}")
        print(f"    {'-'*14} {'-'*16} {'-'*8}")
        for cat, name, price in rows:
            print(f"    {cat:<14} {name:<16} ${price:>7,.2f}")
    else:
        print("    (no second-highest — some categories have only 1 product)")

# ─────────────────────────────────────────────────────────────────────────────
# Q2: Customers with 3+ orders
#    Interview tests: GROUP BY, HAVING, JOIN
# ─────────────────────────────────────────────────────────────────────────────
print("\n  Q2: Customers with 3+ orders")
with conn.cursor() as cur:
    cur.execute(f"""
        SELECT c.first_name || ' ' || c.last_name AS customer,
               COUNT(o.order_id) AS order_count
        FROM   {LAB_SCHEMA}.customers c
        JOIN   {LAB_SCHEMA}.orders o ON c.customer_id = o.customer_id
        GROUP  BY c.customer_id, c.first_name, c.last_name
        HAVING COUNT(o.order_id) >= 3
        ORDER  BY order_count DESC
    """)
    rows = cur.fetchall()
    if rows:
        print(f"    {'Customer':<20} {'Orders'}")
        print(f"    {'-'*20} {'-'*6}")
        for cust, cnt in rows:
            print(f"    {cust:<20} {cnt}")
    else:
        print("    (no customers with 3+ orders yet)")

# ─────────────────────────────────────────────────────────────────────────────
# Q3: Month-over-month revenue growth
#    Interview tests: date truncation, LAG, percentage calculation
# ─────────────────────────────────────────────────────────────────────────────
print("\n  Q3: Month-over-month revenue growth")
with conn.cursor() as cur:
    cur.execute(f"""
        WITH monthly AS (
            SELECT DATE_TRUNC('month', order_date)::date AS month,
                   ROUND(SUM(total_amount), 2) AS revenue
            FROM {LAB_SCHEMA}.orders
            WHERE status != 'cancelled' AND total_amount IS NOT NULL
            GROUP BY DATE_TRUNC('month', order_date)
        )
        SELECT month, revenue,
               LAG(revenue) OVER (ORDER BY month) AS prev_revenue,
               CASE WHEN LAG(revenue) OVER (ORDER BY month) IS NOT NULL
                    THEN ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY month))
                               / LAG(revenue) OVER (ORDER BY month), 1)
               END AS growth_pct
        FROM monthly
        ORDER BY month
    """)
    rows = cur.fetchall()
    if rows:
        print(f"    {'Month':<12} {'Revenue':<12} {'Prev':<12} {'Growth'}")
        print(f"    {'-'*12} {'-'*12} {'-'*12} {'-'*7}")
        for month, rev, prev, growth in rows:
            prev_str = f"${prev:>10,.2f}" if prev else "N/A"
            growth_str = f"{growth:+.1f}%" if growth else "N/A"
            print(f"    {str(month):<12} ${rev:>10,.2f} {prev_str:<12} {growth_str}")
    else:
        print("    (insufficient data for MoM calculation)")

# ─────────────────────────────────────────────────────────────────────────────
# Q4: Find duplicate emails
#    Interview tests: GROUP BY, HAVING, self-awareness of data quality
# ─────────────────────────────────────────────────────────────────────────────
print("\n  Q4: Find duplicate emails")
with conn.cursor() as cur:
    cur.execute(f"""
        SELECT email, COUNT(*) AS occurrences
        FROM {LAB_SCHEMA}.customers
        GROUP BY email
        HAVING COUNT(*) > 1
    """)
    rows = cur.fetchall()
    if rows:
        print(f"    {'Email':<30} {'Count'}")
        print(f"    {'-'*30} {'-'*5}")
        for email, cnt in rows:
            print(f"    {email:<30} {cnt}")
    else:
        print("    No duplicate emails found ✓")

conn.close()
print()
