from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _db_connect import LAB_CATALOG, get_connection

print("\n-- Phase 2 · 05-02 File Ingest Idempotency --")

conn = get_connection()
with conn.cursor() as cur:
    cur.execute(f"USE CATALOG {LAB_CATALOG}")
    cur.execute("CREATE SCHEMA IF NOT EXISTS phase2_ingest")

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS phase2_ingest.file_ledger (
            file_name STRING,
            file_checksum STRING,
            first_seen_at TIMESTAMP,
            last_seen_at TIMESTAMP,
            status STRING
        ) USING DELTA
        """
    )

    cur.execute(
        """
        MERGE INTO phase2_ingest.file_ledger t
        USING (
          SELECT 'orders_2026_04_02.csv' AS file_name, 'sha256:abc123' AS file_checksum, 'processed' AS status
          UNION ALL
          SELECT 'orders_2026_04_04.csv', 'sha256:ghi789', 'processed'
        ) s
        ON t.file_name = s.file_name AND t.file_checksum = s.file_checksum
        WHEN MATCHED THEN UPDATE SET
          t.last_seen_at = current_timestamp(),
          t.status = s.status
        WHEN NOT MATCHED THEN INSERT (file_name, file_checksum, first_seen_at, last_seen_at, status)
          VALUES (s.file_name, s.file_checksum, current_timestamp(), current_timestamp(), s.status)
        """
    )

    cur.execute("SELECT COUNT(*) FROM phase2_ingest.file_ledger")
    count = cur.fetchone()[0]

    cur.execute(
        """
        SELECT file_name, file_checksum, status
        FROM phase2_ingest.file_ledger
        ORDER BY last_seen_at DESC
        """
    )
    rows = cur.fetchall()

conn.close()

print(f"  Ledger rows: {count}")
for r in rows:
    print(f"  - {r[0]} | {r[1]} | {r[2]}")
print("\nDone. Same-file replays now update metadata instead of duplicating ingest state.\n")
