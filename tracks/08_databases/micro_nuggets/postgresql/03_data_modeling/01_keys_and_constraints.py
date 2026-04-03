"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 03-01 · Keys, Constraints & Normalization                            ║
║  Understanding PostgreSQL's data integrity mechanisms.                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Demonstrates primary keys, foreign keys, unique constraints, check constraints,
and the tradeoffs between normalized and denormalized schemas.

USAGE
─────
    python 01_keys_and_constraints.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _pg_connect import get_connection, LAB_SCHEMA, ensure_lab_schema

conn = get_connection()
ensure_lab_schema(conn)

print("\n── Keys, Constraints & Normalization ───────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# 1. List all constraints in the lab schema
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Table Constraints ────────────────────────────────")
with conn.cursor() as cur:
    cur.execute(f"""
        SELECT
            tc.table_name,
            tc.constraint_type,
            STRING_AGG(kcu.column_name, ', ' ORDER BY kcu.ordinal_position) AS columns
        FROM   information_schema.table_constraints tc
        JOIN   information_schema.key_column_usage kcu
               ON tc.constraint_name = kcu.constraint_name
               AND tc.table_schema = kcu.table_schema
        WHERE  tc.table_schema = %s
          AND  tc.constraint_type IN ('PRIMARY KEY', 'FOREIGN KEY', 'UNIQUE', 'CHECK')
        GROUP  BY tc.table_name, tc.constraint_type, tc.constraint_name
        ORDER  BY tc.table_name, tc.constraint_type
    """, (LAB_SCHEMA,))
    rows = cur.fetchall()

print(f"    {'Table':<18} {'Type':<17} {'Column(s)'}")
print(f"    {'-'*18} {'-'*17} {'-'*25}")
for table, ctype, cols in rows:
    print(f"    {table:<18} {ctype:<17} {cols}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Demonstrate constraint violations
#    Each test uses a fresh connection so rollback doesn't affect the main conn.
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Constraint Violation Demo ────────────────────────")

# CHECK constraint: price must be > 0
c = get_connection()
try:
    ensure_lab_schema(c)
    with c.cursor() as cur:
        cur.execute(f"SET search_path TO {LAB_SCHEMA}")
        cur.execute(f"""
            INSERT INTO products (name, category, price, cost)
            VALUES ('Bad Product', 'Test', -10.00, 5.00)
        """)
        c.commit()
        print("    [✗] CHECK constraint did NOT prevent negative price")
except Exception:
    c.rollback()
    print("    [✓] CHECK constraint prevents negative price")
finally:
    c.close()

# FK constraint: can't insert order_items for non-existent order
c = get_connection()
try:
    ensure_lab_schema(c)
    with c.cursor() as cur:
        cur.execute(f"SET search_path TO {LAB_SCHEMA}")
        cur.execute(f"""
            INSERT INTO order_items (order_id, product_id, quantity, unit_price)
            VALUES (99999, 1, 1, 10.00)
        """)
        c.commit()
        print("    [✗] FK constraint did NOT prevent orphaned order_item")
except Exception:
    c.rollback()
    print("    [✓] FK constraint prevents orphaned order_items")
finally:
    c.close()

# UNIQUE constraint: can't insert duplicate email
c = get_connection()
try:
    ensure_lab_schema(c)
    with c.cursor() as cur:
        cur.execute(f"SET search_path TO {LAB_SCHEMA}")
        cur.execute(f"""
            INSERT INTO customers (first_name, last_name, email)
            VALUES ('Dup', 'Test', 'alice@example.com')
        """)
        c.commit()
        print("    [✗] UNIQUE constraint did NOT prevent duplicate email")
except Exception:
    c.rollback()
    print("    [✓] UNIQUE constraint prevents duplicate email")
finally:
    c.close()

conn.close()
print()
