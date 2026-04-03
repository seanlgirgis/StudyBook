from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _db_connect import LAB_CATALOG, get_connection

print("\n-- Phase 2 · 06-03 Column Masking Demo --")

conn = get_connection()
with conn.cursor() as cur:
    cur.execute(f"USE CATALOG {LAB_CATALOG}")
    cur.execute("CREATE SCHEMA IF NOT EXISTS phase2_security")

    cur.execute("""
        CREATE OR REPLACE TABLE phase2_security.customer_pii (
          customer_id INT,
          email STRING,
          phone STRING
        ) USING DELTA
    """)
    cur.execute("DELETE FROM phase2_security.customer_pii")
    cur.execute("""
        INSERT INTO phase2_security.customer_pii VALUES
          (1, 'alice@example.com', '+1-212-111-2222'),
          (2, 'bob@example.com',   '+1-646-333-4444')
    """)

    # Masking via secured view pattern.
    cur.execute("""
        CREATE OR REPLACE VIEW phase2_security.customer_pii_masked AS
        SELECT
          customer_id,
          CASE
            WHEN lower(current_user()) LIKE '%admin%' THEN email
            ELSE regexp_replace(email, '(^.).*(@.*$)', '$1***$2')
          END AS email,
          CASE
            WHEN lower(current_user()) LIKE '%admin%' THEN phone
            ELSE concat('***-***-', right(phone, 4))
          END AS phone
        FROM phase2_security.customer_pii
    """)

    cur.execute("SELECT current_user()")
    me = cur.fetchone()[0]
    cur.execute("SELECT customer_id, email, phone FROM phase2_security.customer_pii_masked ORDER BY customer_id")
    rows = cur.fetchall()

conn.close()

print(f"  Current user: {me}")
print("  Masked output:")
for r in rows:
    print(f"  - id={r[0]} email={r[1]} phone={r[2]}")
print("\nDone. Concept: enforce PII masking policy at query surface (view/policy).\n")
