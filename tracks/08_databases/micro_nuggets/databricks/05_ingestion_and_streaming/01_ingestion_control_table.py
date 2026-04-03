from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _db_connect import LAB_CATALOG, get_connection

print("\n-- Phase 2 · 05-01 Ingestion Control Table --")

conn = get_connection()
with conn.cursor() as cur:
    cur.execute(f"USE CATALOG {LAB_CATALOG}")
    cur.execute("CREATE SCHEMA IF NOT EXISTS phase2_ingest")

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS phase2_ingest.ingestion_control (
            source_name STRING,
            batch_id STRING,
            file_name STRING,
            file_checksum STRING,
            loaded_at TIMESTAMP,
            loaded_by STRING,
            status STRING
        ) USING DELTA
        """
    )

    cur.execute(
        """
        INSERT INTO phase2_ingest.ingestion_control
        VALUES
          ('orders_s3', 'b-20260402-001', 'orders_2026_04_02.csv', 'sha256:abc123', current_timestamp(), current_user(), 'loaded'),
          ('orders_s3', 'b-20260402-002', 'orders_2026_04_03.csv', 'sha256:def456', current_timestamp(), current_user(), 'loaded')
        """
    )

    cur.execute(
        """
        SELECT source_name, batch_id, file_name, status, loaded_at
        FROM phase2_ingest.ingestion_control
        ORDER BY loaded_at DESC
        LIMIT 5
        """
    )
    rows = cur.fetchall()

conn.close()

print("  Created/updated: phase2_ingest.ingestion_control")
for r in rows:
    print(f"  - {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]}")
print("\nDone. This table is your idempotency + replay ledger for ingestion runs.\n")
