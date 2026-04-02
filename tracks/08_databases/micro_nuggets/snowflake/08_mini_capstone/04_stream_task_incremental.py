"""
Mini Capstone 04: Add Stream + Task for incremental updates.

PURPOSE
- Show Snowflake-native incremental processing without external orchestrator code.

TEACHABLE CONCEPTS
- Stream: change data capture object on top of a source table.
- Task: scheduled SQL job inside Snowflake.
- CDC loop: stream captures new rows, task MERGEs into curated target.

EXPECTED OUTPUT (typical)
    Task status row:
    (..., 'NUGGET_CAP_MERGE_TASK', 'started' or 'scheduled', ...)

    Done: stream and task pipeline is wired.

NOTES
- Warehouse is set to COMPUTE_WH in this demo. Change if your account uses another warehouse.
- SCHEDULE uses cron every minute for learning visibility.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _sf_connect import get_connection

conn = get_connection(autocommit=True)
with conn.cursor() as cur:
    # Stream tracks changes on raw table since last stream consumption.
    cur.execute("CREATE OR REPLACE STREAM NUGGET_CAP_RAW_STREAM ON TABLE NUGGET_CAP_RAW_EVENTS")

    # Task runs a MERGE from stream into curated table.
    cur.execute("""
        CREATE OR REPLACE TASK NUGGET_CAP_MERGE_TASK
        WAREHOUSE = COMPUTE_WH
        SCHEDULE = 'USING CRON * * * * * UTC'
        AS
        MERGE INTO NUGGET_CAP_CURATED_EVENTS tgt
        USING (
            SELECT
                payload:event_id::NUMBER         AS event_id,
                payload:customer_id::NUMBER      AS customer_id,
                payload:event_type::STRING       AS event_type,
                payload:event_ts::TIMESTAMP_NTZ  AS event_ts,
                payload:amount::NUMBER(12,2)     AS amount
            FROM NUGGET_CAP_RAW_STREAM
            WHERE METADATA$ACTION IN ('INSERT')
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

    # Resume task so schedule becomes active.
    cur.execute("ALTER TASK NUGGET_CAP_MERGE_TASK RESUME")

    # For demo speed, trigger one immediate run now.
    cur.execute("EXECUTE TASK NUGGET_CAP_MERGE_TASK")

    # Read task metadata for quick verification.
    cur.execute("SHOW TASKS LIKE 'NUGGET_CAP_MERGE_TASK'")
    task_row = cur.fetchone()

print("\nTask status row:")
print(task_row)
print("\nDone: stream and task pipeline is wired.")
