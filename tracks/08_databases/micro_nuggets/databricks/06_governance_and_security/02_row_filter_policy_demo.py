from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _db_connect import LAB_CATALOG, get_connection

print("\n-- Phase 2 · 06-02 Row Filter Policy Demo --")

conn = get_connection()
with conn.cursor() as cur:
    cur.execute(f"USE CATALOG {LAB_CATALOG}")
    cur.execute("CREATE SCHEMA IF NOT EXISTS phase2_security")

    cur.execute("""
        CREATE OR REPLACE TABLE phase2_security.orders_region (
          order_id INT,
          region STRING,
          amount DECIMAL(12,2)
        ) USING DELTA
    """)
    cur.execute("DELETE FROM phase2_security.orders_region")
    cur.execute("""
        INSERT INTO phase2_security.orders_region VALUES
          (1, 'US', 100.00),
          (2, 'EU', 125.00),
          (3, 'APAC', 99.00)
    """)

    # View-based row filtering pattern (works widely, even if row access policies are unavailable)
    cur.execute("""
        CREATE OR REPLACE VIEW phase2_security.orders_region_filtered AS
        SELECT *
        FROM phase2_security.orders_region
        WHERE
          CASE
            WHEN lower(current_user()) LIKE '%us%' THEN region = 'US'
            WHEN lower(current_user()) LIKE '%eu%' THEN region = 'EU'
            ELSE TRUE
          END
    """)

    cur.execute("SELECT current_user()")
    me = cur.fetchone()[0]
    cur.execute("SELECT order_id, region, amount FROM phase2_security.orders_region_filtered ORDER BY order_id")
    rows = cur.fetchall()

conn.close()

print(f"  Current user: {me}")
print("  Rows visible through filtered view:")
for r in rows:
    print(f"  - order_id={r[0]} region={r[1]} amount={r[2]}")
print("\nDone. Concept: enforce row-level visibility via policy or secured view.\n")
