"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 02-02 · Window Functions                                             ║
║  Analytics without GROUP BY — row-level computations across partitions.      ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Demonstrates ranking, lag/lead, running totals, and moving averages.

CONCEPTS
────────
Window functions compute across a set of rows related to the current row,
but unlike GROUP BY, they don't collapse rows — each input row produces
one output row.

Syntax:  function() OVER (PARTITION BY ... ORDER BY ... frame_clause)

  PARTITION BY  — divides rows into groups (like GROUP BY, but per-row output)
  ORDER BY      — defines row order within each partition
  frame_clause  — which rows to include in the calculation:
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW  → running total
    ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING          → moving average

Key functions:
  ROW_NUMBER()       — unique rank (1, 2, 3, 4 — no ties)
  RANK()             — rank with gaps (1, 2, 2, 4 — ties get same rank)
  DENSE_RANK()       — rank without gaps (1, 2, 2, 3 — ties get same rank)
  LAG(col, n)        — value from n rows before current
  LEAD(col, n)       — value from n rows after current
  SUM() OVER (...)   — running aggregate
  NTILE(n)           — divide rows into n roughly equal buckets

USAGE
─────
    python 02_window_functions.py

EXPECTED OUTPUT
───────────────
    ── Window Functions ────────────────────────────────────

      ── Order Ranking per Customer ──────────────────────
        Customer          Order#  Amount    Rank
        ----------------  ------  --------  ----
        Alice Johnson     1       1,299.99  1
        ...

      ── Running Revenue by Date ─────────────────────────
        Date         Daily     Running Total
        -----------  --------  -------------
        2024-01-01   1,299.99  1,299.99
        ...

      ── Order-to-Order Change ───────────────────────────
        Customer          Order#  Amount    Prev Amount  Change
        ----------------  ------  --------  -----------  --------
        Alice Johnson     2       89.99     1,299.99     -93.1%
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _pg_connect import get_connection, LAB_SCHEMA, ensure_lab_schema

conn = get_connection()
ensure_lab_schema(conn)

print("\n── Window Functions ────────────────────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# 1. ROW_NUMBER, RANK, DENSE_RANK — ranking orders per customer
#    ROW_NUMBER: always unique (breaks ties arbitrarily)
#    RANK: same rank for ties, skips next number (1, 2, 2, 4)
#    DENSE_RANK: same rank for ties, no skips (1, 2, 2, 3)
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Order Ranking per Customer ──────────────────────")
with conn.cursor() as cur:
    cur.execute(f"""
        SELECT
            c.first_name || ' ' || c.last_name AS customer,
            o.order_id,
            o.total_amount,
            ROW_NUMBER()  OVER (PARTITION BY o.customer_id ORDER BY o.total_amount DESC) AS rn,
            RANK()        OVER (PARTITION BY o.customer_id ORDER BY o.total_amount DESC) AS rk,
            DENSE_RANK()  OVER (PARTITION BY o.customer_id ORDER BY o.total_amount DESC) AS drk
        FROM   {LAB_SCHEMA}.orders o
        JOIN   {LAB_SCHEMA}.customers c ON o.customer_id = c.customer_id
        WHERE  o.total_amount IS NOT NULL
        ORDER  BY c.customer_id, rn
        LIMIT  15
    """)
    rows = cur.fetchall()

print(f"    {'Customer':<18} {'Order#':<7} {'Amount':<10} {'RN':<4} {'RK':<4} {'DRK'}")
print(f"    {'-'*18} {'-'*7} {'-'*10} {'-'*4} {'-'*4} {'-'*3}")
for cust, oid, amt, rn, rk, drk in rows:
    print(f"    {cust:<18} {oid:<7} ${amt:>8,.2f} {rn:<4} {rk:<4} {drk}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Running total — SUM() OVER with frame clause
#    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW means:
#    "sum all rows from the start of the partition up to and including this row"
#    This is the classic running total pattern.
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Running Revenue by Date ─────────────────────────")
with conn.cursor() as cur:
    cur.execute(f"""
        SELECT
            order_date,
            ROUND(SUM(total_amount), 2) AS daily_revenue,
            ROUND(SUM(SUM(total_amount)) OVER (
                ORDER BY order_date
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ), 2) AS running_total
        FROM   {LAB_SCHEMA}.orders
        WHERE  status != 'cancelled' AND total_amount IS NOT NULL
        GROUP  BY order_date
        ORDER  BY order_date
        LIMIT  15
    """)
    rows = cur.fetchall()

print(f"    {'Date':<12} {'Daily':<12} {'Running Total'}")
print(f"    {'-'*12} {'-'*12} {'-'*13}")
for date, daily, running in rows:
    print(f"    {str(date):<12} ${daily:>10,.2f} ${running:>12,.2f}")

# ─────────────────────────────────────────────────────────────────────────────
# 3. LAG/LEAD — compare current row to previous/next row
#    LAG(total_amount, 1) gets the previous row's amount within the partition.
#    This is how you calculate period-over-period change without self-joins.
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Order-to-Order Change ───────────────────────────")
with conn.cursor() as cur:
    cur.execute(f"""
        WITH ranked AS (
            SELECT
                c.first_name || ' ' || c.last_name AS customer,
                o.order_id,
                o.total_amount,
                LAG(o.total_amount) OVER (
                    PARTITION BY o.customer_id ORDER BY o.order_date, o.order_id
                ) AS prev_amount
            FROM   {LAB_SCHEMA}.orders o
            JOIN   {LAB_SCHEMA}.customers c ON o.customer_id = c.customer_id
            WHERE  o.total_amount IS NOT NULL AND o.status != 'cancelled'
        )
        SELECT customer, order_id, total_amount, prev_amount,
               CASE WHEN prev_amount IS NOT NULL AND prev_amount > 0
                    THEN ROUND(100.0 * (total_amount - prev_amount) / prev_amount, 1)
               END AS pct_change
        FROM   ranked
        WHERE  prev_amount IS NOT NULL
        ORDER  BY customer, order_id
        LIMIT  10
    """)
    rows = cur.fetchall()

print(f"    {'Customer':<18} {'Order#':<7} {'Amount':<10} {'Prev':<10} {'Change'}")
print(f"    {'-'*18} {'-'*7} {'-'*10} {'-'*10} {'-'*7}")
for cust, oid, amt, prev, pct in rows:
    pct_str = f"{pct:+.1f}%" if pct is not None else "N/A"
    prev_str = f"${prev:,.2f}" if prev else "N/A"
    print(f"    {cust:<18} {oid:<7} ${amt:>8,.2f} {prev_str:<10} {pct_str}")

conn.close()
print()
