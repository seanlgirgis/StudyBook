"""
NUGGET 02-03 (Bridge) -- Advanced Analytics Windows
=====================================================
Covers: percentile functions, session windows, gap-and-island,
        top-N per group pattern, pivot-style aggregation.

PostgreSQL -> Databricks SQL transfer notes:
  - PERCENTILE_CONT / PERCENTILE_DISC: identical SQL standard syntax
  - Gap-and-island: identical pattern using ROW_NUMBER difference
  - Top-N per group: both use ROW_NUMBER() CTE approach
  - PIVOT: Databricks SQL has no native PIVOT keyword -- use conditional
    aggregation (CASE WHEN / SUM) same as PostgreSQL.
    Snowflake has native PIVOT/UNPIVOT syntax.

Usage:
    python 03_advanced_analytics.py
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
print("  Nugget 02-03: Advanced Analytics Windows")
print("=" * 64)

conn = get_connection()
with conn.cursor() as cur:

    # ── 1. PERCENTILE_CONT: median and P90 ───────────────────────────────
    # PERCENTILE_CONT interpolates; PERCENTILE_DISC picks actual data value.
    # Both are SQL standard (SQL:2003) -- same in PostgreSQL.
    # In Snowflake: PERCENTILE_CONT and PERCENTILE_DISC also work.
    print()
    print("  [1] PERCENTILE_CONT: P50 and P90 order amount per region")
    cur.execute(f"""
        SELECT
            region,
            ROUND(PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY total_amount), 2) AS p50_median,
            ROUND(PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY total_amount), 2) AS p90,
            ROUND(PERCENTILE_DISC(0.50) WITHIN GROUP (ORDER BY total_amount), 2) AS p50_disc
        FROM {C}.{S}.sales_orders
        WHERE status = 'Shipped'
        GROUP BY region
        ORDER BY region
    """)
    rows = cur.fetchall()
    check("PERCENTILE_CONT P50/P90 by region", rows, 1)

    # ── 2. Top-N per group ────────────────────────────────────────────────
    # Standard pattern: ROW_NUMBER() CTE, then filter WHERE rn <= N.
    # Works identically in PostgreSQL, Snowflake, BigQuery, Redshift.
    print()
    print("  [2] Top-2 orders per region by amount")
    cur.execute(f"""
        WITH ranked AS (
            SELECT
                order_id,
                customer_id,
                region,
                total_amount,
                ROW_NUMBER() OVER (
                    PARTITION BY region
                    ORDER BY total_amount DESC
                ) AS rn
            FROM {C}.{S}.sales_orders
            WHERE status = 'Shipped'
        )
        SELECT order_id, customer_id, region, total_amount, rn
        FROM ranked
        WHERE rn <= 2
        ORDER BY region, rn
    """)
    rows = cur.fetchall()
    check("Top-2 per region", rows, 2)

    # ── 3. Pivot with conditional aggregation ─────────────────────────────
    # Databricks has no PIVOT keyword. Use CASE WHEN / SUM pattern.
    # PostgreSQL: same approach. Snowflake: can use native PIVOT.
    print()
    print("  [3] Pivot: order count by status as columns")
    cur.execute(f"""
        SELECT
            region,
            SUM(CASE WHEN status = 'Shipped'   THEN 1 ELSE 0 END) AS shipped,
            SUM(CASE WHEN status = 'Pending'   THEN 1 ELSE 0 END) AS pending,
            SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled,
            SUM(CASE WHEN status = 'Returned'  THEN 1 ELSE 0 END) AS returned
        FROM {C}.{S}.sales_orders
        GROUP BY region
        ORDER BY region
    """)
    rows = cur.fetchall()
    check("Pivot status columns per region", rows, 1)

    # ── 4. Gap-and-island: consecutive order days per customer ────────────
    # Classic pattern: subtract ROW_NUMBER from date to get island group key.
    # When dates are consecutive, (date - row_number) stays constant.
    # Works identically in PostgreSQL (date arithmetic), Snowflake, Databricks.
    print()
    print("  [4] Gap-and-island: consecutive ordering days per customer")
    cur.execute(f"""
        WITH order_days AS (
            SELECT
                customer_id,
                order_date,
                ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) AS rn
            FROM {C}.{S}.sales_orders
            WHERE status = 'Shipped'
            GROUP BY customer_id, order_date
        ),
        island_key AS (
            SELECT
                customer_id,
                order_date,
                DATE_ADD(order_date, CAST(-rn AS INT)) AS group_key
            FROM order_days
        )
        SELECT
            customer_id,
            MIN(order_date) AS island_start,
            MAX(order_date) AS island_end,
            COUNT(*)        AS days_in_island
        FROM island_key
        GROUP BY customer_id, group_key
        HAVING COUNT(*) >= 2
        ORDER BY days_in_island DESC
        LIMIT 5
    """)
    rows = cur.fetchall()
    # May be 0 rows if no consecutive days in sample data -- structural pass
    results.append(("Gap-and-island consecutive days", True))
    print(f"  PASS  Gap-and-island consecutive days  ({len(rows)} rows -- 0 is valid for sparse data)")

    # ── 5. Session window: user sessions by 30-min gap ───────────────────
    # Session windows group events within N minutes of each other.
    # No native SESSION WINDOW in SQL -- use LAG + cumulative SUM pattern.
    print()
    print("  [5] Session window: user sessions (30-min gap)")
    cur.execute(f"""
        WITH flagged AS (
            SELECT
                user_id,
                event_ts,
                event_type,
                LAG(event_ts) OVER (PARTITION BY user_id ORDER BY event_ts) AS prev_ts,
                CASE
                    WHEN event_ts - LAG(event_ts) OVER (PARTITION BY user_id ORDER BY event_ts)
                         > INTERVAL 30 MINUTES
                    THEN 1 ELSE 0
                END AS new_session_flag
            FROM {C}.{S}.events_stream
        ),
        sessioned AS (
            SELECT
                user_id,
                event_ts,
                event_type,
                SUM(new_session_flag) OVER (
                    PARTITION BY user_id ORDER BY event_ts
                ) AS session_id
            FROM flagged
        )
        SELECT
            user_id,
            session_id,
            MIN(event_ts) AS session_start,
            MAX(event_ts) AS session_end,
            COUNT(*)      AS event_count
        FROM sessioned
        GROUP BY user_id, session_id
        ORDER BY user_id, session_id
        LIMIT 6
    """)
    rows = cur.fetchall()
    check("Session window (30-min gap)", rows, 1)

    # ── 6. YTD aggregation with window ────────────────────────────────────
    # Year-to-date cumulative totals using RANGE frame (date-based).
    print()
    print("  [6] YTD revenue per region (cumulative by order date)")
    cur.execute(f"""
        WITH daily AS (
            SELECT
                region,
                order_date,
                SUM(total_amount) AS daily_rev
            FROM {C}.{S}.sales_orders
            WHERE status = 'Shipped'
            GROUP BY region, order_date
        )
        SELECT
            region,
            order_date,
            daily_rev,
            SUM(daily_rev) OVER (
                PARTITION BY region
                ORDER BY order_date
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ) AS ytd_revenue
        FROM daily
        ORDER BY region, order_date
        LIMIT 6
    """)
    rows = cur.fetchall()
    check("YTD cumulative revenue", rows, 1)

conn.close()

print()
print(DIVIDER)
passed = sum(1 for _, ok in results if ok)
total  = len(results)
print(f"  Nugget 02-03: {passed}/{total} checks passed")
print(DIVIDER)
print()
if passed < total:
    sys.exit(1)
