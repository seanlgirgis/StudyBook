from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _db_connect import LAB_CATALOG, get_connection

print("\n-- Phase 2 · 05-03 CDC Pattern (MERGE Apply Changes) --")

conn = get_connection()
with conn.cursor() as cur:
    cur.execute(f"USE CATALOG {LAB_CATALOG}")
    cur.execute("CREATE SCHEMA IF NOT EXISTS phase2_ingest")

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS phase2_ingest.customers_silver (
          customer_id INT,
          email STRING,
          tier STRING,
          updated_at TIMESTAMP
        ) USING DELTA
        """
    )

    cur.execute("DELETE FROM phase2_ingest.customers_silver")
    cur.execute(
        """
        INSERT INTO phase2_ingest.customers_silver VALUES
          (1, 'alice@old.com', 'bronze', current_timestamp()),
          (2, 'bob@corp.com', 'silver', current_timestamp())
        """
    )

    cur.execute(
        """
        CREATE OR REPLACE TEMP VIEW cdc_events AS
        SELECT 1 AS customer_id, 'alice@new.com' AS email, 'silver' AS tier, 'U' AS op
        UNION ALL
        SELECT 3, 'carol@corp.com', 'gold', 'I'
        UNION ALL
        SELECT 2, 'bob@corp.com', 'silver', 'D'
        """
    )

    cur.execute(
        """
        MERGE INTO phase2_ingest.customers_silver t
        USING cdc_events s
        ON t.customer_id = s.customer_id
        WHEN MATCHED AND s.op = 'D' THEN DELETE
        WHEN MATCHED AND s.op = 'U' THEN UPDATE SET
          t.email = s.email,
          t.tier = s.tier,
          t.updated_at = current_timestamp()
        WHEN NOT MATCHED AND s.op IN ('I','U') THEN INSERT (customer_id, email, tier, updated_at)
          VALUES (s.customer_id, s.email, s.tier, current_timestamp())
        """
    )

    cur.execute(
        """
        SELECT customer_id, email, tier
        FROM phase2_ingest.customers_silver
        ORDER BY customer_id
        """
    )
    rows = cur.fetchall()

conn.close()

print("  Final silver state:")
for r in rows:
    print(f"  - id={r[0]} email={r[1]} tier={r[2]}")
print("\nDone. This is the core CDC apply-changes pattern used in production pipelines.\n")
