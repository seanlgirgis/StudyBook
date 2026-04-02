"""
Mini Capstone 03: Transform into curated table with MERGE.

PURPOSE
- Convert raw JSON payloads into typed curated rows and upsert idempotently.

TEACHABLE CONCEPTS
- Curated table: strongly typed, analytics-friendly schema.
- MERGE: one statement for insert/update logic (core DE pattern).
- Idempotency: rerunning pipeline does not duplicate records.
- QUALIFY + ROW_NUMBER: keep latest record per business key.

EXPECTED OUTPUT (typical)
    MERGE result: (<rows_inserted>, <rows_updated>, <rows_deleted>)

    -- Curated rows --
      (1, 101, 'page_view', ...)
      (2, 102, 'add_to_cart', ...)
      (3, 102, 'purchase', ...)
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _sf_connect import get_connection

conn = get_connection(autocommit=True)
with conn.cursor() as cur:
    # Curated layer: typed columns for predictable downstream querying.
    cur.execute("""
        CREATE OR REPLACE TABLE NUGGET_CAP_CURATED_EVENTS (
            event_id NUMBER,
            customer_id NUMBER,
            event_type STRING,
            event_ts TIMESTAMP_NTZ,
            amount NUMBER(12,2),
            updated_at TIMESTAMP_NTZ,
            PRIMARY KEY (event_id)
        )
    """)

    # Upsert from raw VARIANT into curated typed columns.
    cur.execute("""
        MERGE INTO NUGGET_CAP_CURATED_EVENTS tgt
        USING (
            SELECT
                payload:event_id::NUMBER         AS event_id,
                payload:customer_id::NUMBER      AS customer_id,
                payload:event_type::STRING       AS event_type,
                payload:event_ts::TIMESTAMP_NTZ  AS event_ts,
                payload:amount::NUMBER(12,2)     AS amount
            FROM NUGGET_CAP_RAW_EVENTS
            QUALIFY ROW_NUMBER() OVER (
                PARTITION BY payload:event_id::NUMBER
                ORDER BY loaded_at DESC
            ) = 1
        ) src
        ON tgt.event_id = src.event_id
        WHEN MATCHED THEN UPDATE SET
            tgt.customer_id = src.customer_id,
            tgt.event_type = src.event_type,
            tgt.event_ts = src.event_ts,
            tgt.amount = src.amount,
            tgt.updated_at = CURRENT_TIMESTAMP()
        WHEN NOT MATCHED THEN INSERT (
            event_id, customer_id, event_type, event_ts, amount, updated_at
        ) VALUES (
            src.event_id, src.customer_id, src.event_type, src.event_ts, src.amount, CURRENT_TIMESTAMP()
        )
    """)

    # MERGE returns operation counts.
    res = cur.fetchone()

    # Inspect curated output.
    cur.execute("SELECT event_id, customer_id, event_type, event_ts, amount FROM NUGGET_CAP_CURATED_EVENTS ORDER BY event_id")
    rows = cur.fetchall()

print("\nMERGE result:", res)
print("\n-- Curated rows --")
for r in rows:
    print("  ", r)
