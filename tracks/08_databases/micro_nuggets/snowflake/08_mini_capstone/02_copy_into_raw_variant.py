"""
Mini Capstone 02: COPY INTO raw table with VARIANT.

PURPOSE
- Move staged raw JSON into a landing table while preserving the full payload.

TEACHABLE CONCEPTS
- Raw landing table: schema-on-read style, keeps original payload for traceability.
- VARIANT: Snowflake's semi-structured type for JSON-like data.
- COPY INTO: scalable bulk ingest from stage to table.
- Metadata columns: filename and row number are key for lineage/debugging.

EXPECTED OUTPUT (typical)
    -- COPY INTO result --
      (<file>, <status>, <rows_loaded>, ...)

    Raw rows loaded: 3
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _sf_connect import get_connection

conn = get_connection(autocommit=True)
with conn.cursor() as cur:
    # Raw table keeps payload + ingestion metadata.
    cur.execute("""
        CREATE OR REPLACE TABLE NUGGET_CAP_RAW_EVENTS (
            src_file STRING,
            src_row_number NUMBER,
            payload VARIANT,
            loaded_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
        )
    """)

    # COPY INTO reads files from stage and maps fields into selected columns.
    cur.execute("""
        COPY INTO NUGGET_CAP_RAW_EVENTS (src_file, src_row_number, payload)
        FROM (
            SELECT METADATA$FILENAME, METADATA$FILE_ROW_NUMBER, $1
            FROM @NUGGET_CAP_STAGE
        )
        FILE_FORMAT = (FORMAT_NAME = NUGGET_CAP_JSON_FF)
        ON_ERROR = CONTINUE
    """)

    # COPY returns per-file load summary rows.
    copy_res = cur.fetchall()

    # Quick verification count.
    cur.execute("SELECT COUNT(*) FROM NUGGET_CAP_RAW_EVENTS")
    cnt = cur.fetchone()[0]

print("\n-- COPY INTO result --")
for row in copy_res:
    print("  ", row)
print(f"\nRaw rows loaded: {cnt}")
