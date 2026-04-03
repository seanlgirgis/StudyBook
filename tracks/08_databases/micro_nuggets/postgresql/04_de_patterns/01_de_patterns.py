"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 04-01 · Deduplication, Upserts & SCD Type 2                          ║
║  The most common DE patterns in PostgreSQL.                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Demonstrates deduplication, INSERT ON CONFLICT (upsert), and SCD Type 2.

CONCEPTS
────────
Deduplication with ROW_NUMBER():
  - Assign rank to each duplicate, keep only rank 1.
  - Standard pattern across all SQL databases.

INSERT ... ON CONFLICT (upsert):
  - PostgreSQL's native upsert — insert or update in one statement.
  - ON CONFLICT (unique_column) DO UPDATE SET ...
  - Atomic — no race conditions between check and insert.

SCD Type 2 (Slowly Changing Dimension):
  - Keep full history of changes by adding new rows with date ranges.
  - Current row has valid_to = NULL and is_current = true.
  - When data changes: expire old row, insert new row.

USAGE
─────
    python 01_de_patterns.py

EXPECTED OUTPUT
───────────────
    ── DE Patterns ─────────────────────────────────────────

      ── Deduplication ────────────────────────────────────
        Before: 205 events (with duplicates)
        After:  200 unique events

      ── Upsert (INSERT ON CONFLICT) ──────────────────────
        Inserted/updated 3 products

      ── SCD Type 2 ───────────────────────────────────────
        Employee 1 (Alice Johnson):
          Version 1: Engineering, $90,000 (2022-01-15 → 2023-06-01)
          Version 2: Engineering, $95,000 (2023-06-01 → current)
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _pg_connect import get_connection, LAB_SCHEMA, ensure_lab_schema

conn = get_connection()
ensure_lab_schema(conn)

print("\n── DE Patterns ─────────────────────────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Deduplication — remove duplicate events using ROW_NUMBER()
#    Duplicates happen in real pipelines: retry logic, double ingestion, etc.
#    The pattern: partition by the business key, order by a tiebreaker,
#    keep only row_number = 1.
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Deduplication ────────────────────────────────────")
with conn.cursor() as cur:
    cur.execute(f"SELECT COUNT(*) FROM {LAB_SCHEMA}.events")
    before = cur.fetchone()[0]

    # Add some duplicates for the demo
    cur.execute(f"""
        INSERT INTO {LAB_SCHEMA}.events (customer_id, event_type, page_url, event_time, session_id, device)
        SELECT customer_id, event_type, page_url, event_time, session_id, device
        FROM {LAB_SCHEMA}.events LIMIT 5
    """)
    conn.commit()

    cur.execute(f"SELECT COUNT(*) FROM {LAB_SCHEMA}.events")
    with_dups = cur.fetchone()[0]

    # Deduplicate: keep the row with the lowest event_id for each unique combo
    cur.execute(f"""
        WITH ranked AS (
            SELECT event_id,
                   ROW_NUMBER() OVER (
                       PARTITION BY customer_id, event_type, page_url, event_time, session_id
                       ORDER BY event_id
                   ) AS rn
            FROM {LAB_SCHEMA}.events
        )
        DELETE FROM {LAB_SCHEMA}.events
        WHERE event_id IN (SELECT event_id FROM ranked WHERE rn > 1)
    """)
    conn.commit()

    cur.execute(f"SELECT COUNT(*) FROM {LAB_SCHEMA}.events")
    after = cur.fetchone()[0]

    print(f"    Before: {before} events")
    print(f"    Added:  {with_dups - before} duplicates")
    print(f"    After:  {after} unique events")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Upsert — INSERT ... ON CONFLICT DO UPDATE
#    This is PostgreSQL's answer to MERGE (which PG doesn't have).
#    It's cleaner than MERGE: specify the conflict column and what to do.
#
#    ON CONFLICT (product_id) DO UPDATE SET ...
#    — if product_id exists, update it; otherwise insert.
#
#    The EXCLUDED pseudo-table holds the values that were attempted to insert.
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Upsert (INSERT ON CONFLICT) ──────────────────────")
with conn.cursor() as cur:
    cur.execute(f"""
        INSERT INTO {LAB_SCHEMA}.products (product_id, name, category, price, cost)
        VALUES
            (1, 'Laptop Pro 15 v2', 'Electronics', 1399.99, 850.00),  -- update existing
            (9, 'Tablet 10"',      'Electronics', 599.99, 350.00),   -- insert new
            (10, 'Wireless Charger','Accessories', 39.99, 15.00)     -- insert new
        ON CONFLICT (product_id) DO UPDATE SET
            name  = EXCLUDED.name,
            price = EXCLUDED.price,
            cost  = EXCLUDED.cost
    """)
    conn.commit()
    print("    Inserted/updated 3 products")

    # Show what happened
    cur.execute(f"""
        SELECT product_id, name, price
        FROM {LAB_SCHEMA}.products
        WHERE product_id IN (1, 9, 10)
        ORDER BY product_id
    """)
    for pid, name, price in cur.fetchall():
        print(f"      {pid}: {name} (${price:.2f})")

# ─────────────────────────────────────────────────────────────────────────────
# 3. SCD Type 2 — expire old row, insert new row
#    This is how you maintain a full history of changes in a dimension table.
#    Step 1: Expire the current row (set valid_to = today, is_current = false)
#    Step 2: Insert the new row (valid_from = today, valid_to = NULL, is_current = true)
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── SCD Type 2 ───────────────────────────────────────")
with conn.cursor() as cur:
    # Simulate a salary change for employee 1
    cur.execute(f"""
        UPDATE {LAB_SCHEMA}.employees_hist
        SET valid_to = CURRENT_DATE, is_current = false
        WHERE emp_id = 1 AND is_current = true
    """)

    cur.execute(f"""
        INSERT INTO {LAB_SCHEMA}.employees_hist
            (emp_id, name, department, salary, valid_from, valid_to, is_current)
        VALUES (1, 'Alice Johnson', 'Engineering', 105000, CURRENT_DATE, NULL, true)
    """)
    conn.commit()

    # Show the full history
    cur.execute(f"""
        SELECT emp_id, name, department, salary, valid_from, valid_to, is_current
        FROM {LAB_SCHEMA}.employees_hist
        WHERE emp_id = 1
        ORDER BY valid_from
    """)
    rows = cur.fetchall()
    for emp_id, name, dept, salary, vfrom, vto, is_cur in rows:
        to_str = str(vto) if vto else "current"
        print(f"    {name}: {dept}, ${salary:,.0f} ({vfrom} → {to_str})")

conn.close()
print()
