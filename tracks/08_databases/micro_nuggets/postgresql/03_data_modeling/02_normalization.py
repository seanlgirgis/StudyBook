"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 03-02 · Normalization vs Denormalization                             ║
║  When to split data apart vs when to combine it.                             ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Demonstrates the tradeoffs between normalized (3NF) and denormalized schemas
using a practical example.

CONCEPTS
────────
Normalized schema (3NF):
  - Each fact stored in exactly one place.
  - No transitive dependencies (non-key columns depend only on the PK).
  - Example: orders table references customers table — customer name is NOT
    stored in orders. To get customer name, you JOIN.

Denormalized schema:
  - Some facts are duplicated across tables for read performance.
  - Example: orders table includes customer_name directly — no JOIN needed.
  - Risk: if customer changes name, you must update ALL their orders.

When to normalize:
  - Write-heavy workloads (OLTP).
  - Data consistency is critical (financial systems).
  - Storage is constrained.

When to denormalize:
  - Read-heavy workloads (analytics, reporting).
  - JOIN performance is a bottleneck.
  - Data changes infrequently (dimension tables).

Materialized views:
  - PostgreSQL's middle ground — a pre-computed JOIN stored as a table.
  - Refreshed periodically: REFRESH MATERIALIZED VIEW.
  - Gives denormalized read performance with normalized source data.

USAGE
─────
    python 02_normalization.py

EXPECTED OUTPUT
───────────────
    ── Normalization vs Denormalization ────────────────────

      ── Normalized Query (with JOIN) ─────────────────────
        Order#  Customer         Total
        ------  ---------------  ---------
        1       Alice Johnson    1,299.99

      ── Denormalized Query (no JOIN) ─────────────────────
        Order#  Customer         Total
        ------  ---------------  ---------
        1       Alice Johnson    1,299.99

      ── Materialized View ────────────────────────────────
        Created materialized view: pg_lab.gold_customer_summary
        Rows: 10
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _pg_connect import get_connection, LAB_SCHEMA, ensure_lab_schema

conn = get_connection()
ensure_lab_schema(conn)

print("\n── Normalization vs Denormalization ────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Normalized query — requires JOIN to get customer name
#    This is the "correct" 3NF approach. Customer data lives in one place.
#    If Alice changes her name, you update ONE row in customers.
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Normalized Query (with JOIN) ─────────────────────")
with conn.cursor() as cur:
    cur.execute(f"""
        SELECT o.order_id,
               c.first_name || ' ' || c.last_name AS customer,
               o.total_amount
        FROM   {LAB_SCHEMA}.orders o
        JOIN   {LAB_SCHEMA}.customers c ON o.customer_id = c.customer_id
        WHERE  o.status != 'cancelled'
        ORDER  BY o.order_id
        LIMIT  5
    """)
    rows = cur.fetchall()

print(f"    {'Order#':<7} {'Customer':<16} {'Total'}")
print(f"    {'-'*7} {'-'*16} {'-'*10}")
for oid, cust, total in rows:
    print(f"    {oid:<7} {cust:<16} ${total:>9,.2f}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Denormalized table — add customer_name directly to orders
#    This avoids the JOIN but creates redundancy.
#    If Alice changes her name, you must UPDATE all her orders too.
# ─────────────────────────────────────────────────────────────────────────────
with conn.cursor() as cur:
    cur.execute(f"""
        ALTER TABLE {LAB_SCHEMA}.orders
        ADD COLUMN IF NOT EXISTS customer_name VARCHAR(101)
    """)
    cur.execute(f"""
        UPDATE {LAB_SCHEMA}.orders o
        SET customer_name = c.first_name || ' ' || c.last_name
        FROM {LAB_SCHEMA}.customers c
        WHERE o.customer_id = c.customer_id
    """)
    conn.commit()

print("\n  ── Denormalized Query (no JOIN) ─────────────────────")
with conn.cursor() as cur:
    cur.execute(f"""
        SELECT order_id, customer_name, total_amount
        FROM   {LAB_SCHEMA}.orders
        WHERE  status != 'cancelled' AND customer_name IS NOT NULL
        ORDER  BY order_id
        LIMIT  5
    """)
    rows = cur.fetchall()

print(f"    {'Order#':<7} {'Customer':<16} {'Total'}")
print(f"    {'-'*7} {'-'*16} {'-'*10}")
for oid, cust, total in rows:
    print(f"    {oid:<7} {cust:<16} ${total:>9,.2f}")

# ─────────────────────────────────────────────────────────────────────────────
# 3. Materialized view — PostgreSQL's middle ground
#    Pre-computes the JOIN, stores the result.
#    Source data stays normalized; reads are fast.
#    Refresh when needed: REFRESH MATERIALIZED VIEW.
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Materialized View ────────────────────────────────")
with conn.cursor() as cur:
    cur.execute(f"DROP MATERIALIZED VIEW IF EXISTS {LAB_SCHEMA}.gold_customer_summary")
    cur.execute(f"""
        CREATE MATERIALIZED VIEW {LAB_SCHEMA}.gold_customer_summary AS
        SELECT
            c.customer_id,
            c.first_name || ' ' || c.last_name AS customer_name,
            COUNT(o.order_id)   AS total_orders,
            COALESCE(SUM(o.total_amount), 0) AS total_spent,
            MIN(o.order_date)   AS first_order,
            MAX(o.order_date)   AS last_order
        FROM   {LAB_SCHEMA}.customers c
        LEFT   JOIN {LAB_SCHEMA}.orders o
               ON c.customer_id = o.customer_id
              AND o.status != 'cancelled'
        GROUP  BY c.customer_id, c.first_name, c.last_name
    """)
    cur.execute(f"SELECT COUNT(*) FROM {LAB_SCHEMA}.gold_customer_summary")
    count = cur.fetchone()[0]
    conn.commit()
    print(f"    Created materialized view: {LAB_SCHEMA}.gold_customer_summary")
    print(f"    Rows: {count}")

conn.close()
print()
