"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 05-01 · EXPLAIN, Indexes & Query Optimization                        ║
║  Making PostgreSQL queries faster.                                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Demonstrates EXPLAIN ANALYZE, index strategies, and common anti-patterns.

CONCEPTS
────────
EXPLAIN:
  - Shows the query execution plan without running the query.
  - EXPLAIN ANALYZE actually runs the query and shows real timing.
  - Key concepts:
    - Seq Scan: reads every row (slow for large tables)
    - Index Scan: uses an index to find rows (fast)
    - Bitmap Heap Scan: uses index to find blocks, then reads blocks
    - Nested Loop: joins by iterating (fine for small inputs)
    - Hash Join: builds hash table for join (good for large inputs)
    - Sort: orders rows (expensive for large datasets)

Index types:
  - B-tree (default): good for =, <, >, BETWEEN, LIKE 'prefix%'
  - Composite: (col1, col2) — leftmost prefix rule applies
  - Partial: WHERE condition — only indexes a subset of rows
  - Covering: INCLUDE columns — index-only scans

Anti-patterns:
  - SELECT * — fetches all columns, prevents index-only scans
  - Functions on indexed columns: WHERE UPPER(name) = ... (can't use index)
  - Implicit type conversion: WHERE int_column = '123' (prevents index use)
  - OR conditions: WHERE a = 1 OR b = 2 (often causes seq scan)

USAGE
─────
    python 01_explain_and_indexes.py

EXPECTED OUTPUT
───────────────
    ── EXPLAIN & Indexes ───────────────────────────────────

      ── Before Index ─────────────────────────────────────
        Seq Scan on orders  (cost=... rows=...)

      ── After Index ──────────────────────────────────────
        Index Scan using idx_orders_customer on orders  (cost=... rows=...)

      ── Composite Index Demo ─────────────────────────────
        Uses index on (customer_id, order_date)
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _pg_connect import get_connection, LAB_SCHEMA, ensure_lab_schema

conn = get_connection()
ensure_lab_schema(conn)

print("\n── EXPLAIN & Indexes ───────────────────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# 1. EXPLAIN ANALYZE — see the actual execution plan
#    This is the #1 tool for query optimization in PostgreSQL.
#    It shows: scan type, estimated vs actual rows, execution time.
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── EXPLAIN ANALYZE (before index) ──────────────────")
with conn.cursor() as cur:
    cur.execute(f"""
        EXPLAIN ANALYZE
        SELECT * FROM {LAB_SCHEMA}.orders WHERE customer_id = 3
    """)
    rows = cur.fetchall()
    for row in rows:
        plan = row[0]
        if plan:
            print(f"    {plan.strip()}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Create an index and compare
#    The index on customer_id lets PostgreSQL jump directly to matching rows
#    instead of scanning the entire table.
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Creating index on orders(customer_id) ───────────")
with conn.cursor() as cur:
    cur.execute(f"""
        CREATE INDEX IF NOT EXISTS idx_orders_cust_lookup
        ON {LAB_SCHEMA}.orders(customer_id)
    """)
    conn.commit()
    print("    Index created.")

print("\n  ── EXPLAIN ANALYZE (after index) ───────────────────")
with conn.cursor() as cur:
    cur.execute(f"""
        EXPLAIN ANALYZE
        SELECT * FROM {LAB_SCHEMA}.orders WHERE customer_id = 3
    """)
    rows = cur.fetchall()
    for row in rows:
        plan = row[0]
        if plan:
            print(f"    {plan.strip()}")

# ─────────────────────────────────────────────────────────────────────────────
# 3. Composite index — (customer_id, order_date)
#    A composite index can serve queries on:
#      - customer_id alone (leftmost prefix)
#      - customer_id AND order_date
#      - customer_id with order_date range
#    But NOT order_date alone (leftmost rule).
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Composite Index Demo ────────────────────────────")
with conn.cursor() as cur:
    cur.execute(f"""
        CREATE INDEX IF NOT EXISTS idx_orders_cust_date
        ON {LAB_SCHEMA}.orders(customer_id, order_date)
    """)
    conn.commit()

    cur.execute(f"""
        EXPLAIN ANALYZE
        SELECT order_id, order_date, total_amount
        FROM {LAB_SCHEMA}.orders
        WHERE customer_id = 3 AND order_date >= '2024-01-15'
    """)
    rows = cur.fetchall()
    for (plan,) in rows[:5]:  # Show first 5 lines
        print(f"    {plan.strip()}")

# ─────────────────────────────────────────────────────────────────────────────
# 4. Anti-pattern: function on indexed column prevents index use
#    WHERE UPPER(name) = 'ALICE' can't use an index on name.
#    Fix: create a functional index: CREATE INDEX ON table(UPPER(name))
#    Or better: store data in consistent case and query without functions.
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Anti-Pattern: Function on Column ────────────────")
with conn.cursor() as cur:
    cur.execute(f"""
        EXPLAIN ANALYZE
        SELECT * FROM {LAB_SCHEMA}.customers WHERE UPPER(first_name) = 'ALICE'
    """)
    rows = cur.fetchall()
    for (plan,) in rows[:3]:
        print(f"    {plan.strip()}")
    print("    ↑ Seq Scan — UPPER() prevents index use on first_name")

conn.close()
print()
