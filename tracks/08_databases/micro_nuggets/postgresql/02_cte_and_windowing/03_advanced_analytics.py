"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 02-03 · Advanced Analytics (CTEs + Windows Combined)                 ║
║  Real DE patterns: cohort analysis, sessionization, top-N, YoY growth.       ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Combines CTEs and window functions for production-grade analytics patterns.

CONCEPTS
────────
Cohort analysis:
  - Group users by signup period, track behavior over time.
  - Answers: "Do customers who signed up in January spend more than March?"

Sessionization:
  - Group raw events into sessions using time gaps.
  - If gap between events > 30 minutes, it's a new session.
  - Uses LAG() to compare current event time with previous event time.

Top-N per group:
  - ROW_NUMBER() PARTITION BY category ORDER BY revenue DESC
  - Gets the top 3 products per category without complex subqueries.

Year-over-year growth:
  - LAG() on aggregated monthly/quarterly data.
  - Shows growth rate compared to the same period last year.

USAGE
─────
    python 03_advanced_analytics.py

EXPECTED OUTPUT
───────────────
    ── Advanced Analytics ──────────────────────────────────

      ── Top 3 Products per Category ─────────────────────
        Category       Rank  Product           Revenue
        -------------  ----  ----------------  ---------
        Electronics    1     Laptop Pro 15     5,199.96
        ...

      ── Revenue by Device ───────────────────────────────
        Device     Sessions  Events  Conv. Rate
        ---------  --------  ------  ----------
        desktop    35        120     15.0%
        ...
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _pg_connect import get_connection, LAB_SCHEMA, ensure_lab_schema

conn = get_connection()
ensure_lab_schema(conn)

print("\n── Advanced Analytics ──────────────────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Top-N per group — top 3 products per category by revenue
#    ROW_NUMBER() PARTITION BY category gives each product a rank within
#    its category. Then we filter WHERE rn <= 3.
#    This is much cleaner than the old self-join approach for top-N.
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Top 3 Products per Category ─────────────────────")
with conn.cursor() as cur:
    cur.execute(f"""
        WITH product_revenue AS (
            SELECT
                p.category,
                p.name,
                SUM(oi.line_total) AS total_revenue,
                ROW_NUMBER() OVER (
                    PARTITION BY p.category
                    ORDER BY SUM(oi.line_total) DESC
                ) AS rn
            FROM   {LAB_SCHEMA}.order_items oi
            JOIN   {LAB_SCHEMA}.products p ON oi.product_id = p.product_id
            GROUP  BY p.category, p.name
        )
        SELECT category, rn, name, total_revenue
        FROM   product_revenue
        WHERE  rn <= 3
        ORDER  BY category, rn
    """)
    rows = cur.fetchall()

print(f"    {'Category':<14} {'Rank':<5} {'Product':<18} {'Revenue'}")
print(f"    {'-'*14} {'-'*5} {'-'*18} {'-'*10}")
for cat, rn, name, rev in rows:
    print(f"    {cat:<14} {rn:<5} {name:<18} ${rev:>9,.2f}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Revenue by device — simple aggregation with conversion rate
#    Shows how different devices perform in terms of engagement and revenue.
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Revenue by Device ───────────────────────────────")
with conn.cursor() as cur:
    cur.execute(f"""
        WITH device_stats AS (
            SELECT
                device,
                COUNT(DISTINCT session_id) AS sessions,
                COUNT(*) AS events,
                COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN customer_id END) AS purchasers
            FROM {LAB_SCHEMA}.events
            GROUP BY device
        )
        SELECT
            device,
            sessions,
            events,
            ROUND(100.0 * purchasers / NULLIF(sessions, 0), 1) AS conv_rate
        FROM device_stats
        ORDER BY sessions DESC
    """)
    rows = cur.fetchall()

print(f"    {'Device':<10} {'Sessions':<9} {'Events':<7} {'Conv. Rate'}")
print(f"    {'-'*10} {'-'*9} {'-'*7} {'-'*10}")
for device, sessions, events, conv in rows:
    print(f"    {device:<10} {sessions:<9} {events:<7} {conv:>9.1f}%")

# ─────────────────────────────────────────────────────────────────────────────
# 3. Customer activity timeline — LAG to show days between orders
#    This is a real DE pattern: identify gaps in customer activity.
#    Large gaps might indicate churn risk.
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Customer Order Gaps (days between orders) ──────")
with conn.cursor() as cur:
    cur.execute(f"""
        WITH customer_orders AS (
            SELECT
                c.first_name || ' ' || c.last_name AS customer,
                o.order_date,
                LAG(o.order_date) OVER (
                    PARTITION BY o.customer_id ORDER BY o.order_date
                ) AS prev_date
            FROM {LAB_SCHEMA}.orders o
            JOIN {LAB_SCHEMA}.customers c ON o.customer_id = c.customer_id
            WHERE o.status != 'cancelled'
        )
        SELECT customer, order_date, prev_date,
               CASE WHEN prev_date IS NOT NULL
                    THEN order_date - prev_date
               END AS days_since_last
        FROM customer_orders
        WHERE prev_date IS NOT NULL
        ORDER BY days_since_last DESC NULLS LAST
        LIMIT 10
    """)
    rows = cur.fetchall()

print(f"    {'Customer':<18} {'Order Date':<12} {'Prev Date':<12} {'Days Gap'}")
print(f"    {'-'*18} {'-'*12} {'-'*12} {'-'*8}")
for cust, od, prev, gap in rows:
    gap_str = str(gap) if gap is not None else "first"
    print(f"    {cust:<18} {str(od):<12} {str(prev):<12} {gap_str}")

conn.close()
print()
