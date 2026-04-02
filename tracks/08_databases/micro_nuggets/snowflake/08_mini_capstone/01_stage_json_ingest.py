"""
Mini Capstone 01: Ingest small JSON files into an internal stage.

PURPOSE
- Demonstrate the first step of most modern ELT pipelines: land raw files first.

TEACHABLE CONCEPTS
- Internal stage: Snowflake-managed landing area for files.
- File format object: reusable parsing rules (JSON, CSV, Parquet, etc.).
- PUT command: uploads local files into a stage.
- JSONL pattern: one JSON object per line, common for event streams.

EXPECTED OUTPUT (typical)
    -- Stage files --
      @NUGGET_CAP_STAGE/sample_events.jsonl

    Done: raw JSON landed in stage.

NOTES
- This script writes a tiny local sample file next to itself (`sample_events.jsonl`).
- In production, raw files usually come from object storage or upstream systems.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Reuse shared credential/session helper from the nugget root.
sys.path.insert(0, str(Path(__file__).parent.parent))
from _sf_connect import get_connection

# Local demo file to upload with PUT.
LOCAL_FILE = Path(__file__).with_name("sample_events.jsonl")

# Tiny event batch so the learning loop stays fast and readable.
records = [
    {"event_id": 1, "customer_id": 101, "event_type": "page_view",   "event_ts": "2026-04-02T09:00:00Z", "amount": 0},
    {"event_id": 2, "customer_id": 102, "event_type": "add_to_cart", "event_ts": "2026-04-02T09:02:00Z", "amount": 35.5},
    {"event_id": 3, "customer_id": 102, "event_type": "purchase",    "event_ts": "2026-04-02T09:05:00Z", "amount": 35.5},
]

# JSONL = one JSON object per line. Easy to stream and parse.
LOCAL_FILE.write_text("\n".join(json.dumps(r) for r in records) + "\n", encoding="utf-8")

conn = get_connection(autocommit=True)
with conn.cursor() as cur:
    # Create reusable JSON parsing config.
    cur.execute("CREATE OR REPLACE FILE FORMAT NUGGET_CAP_JSON_FF TYPE = JSON")

    # Create internal stage bound to that file format.
    cur.execute("CREATE OR REPLACE STAGE NUGGET_CAP_STAGE FILE_FORMAT = NUGGET_CAP_JSON_FF")

    # PUT uploads local file to stage. OVERWRITE keeps reruns idempotent.
    put_path = LOCAL_FILE.as_posix()
    cur.execute(f"PUT file://{put_path} @NUGGET_CAP_STAGE AUTO_COMPRESS=FALSE OVERWRITE=TRUE")

    # LIST verifies what Snowflake sees in stage.
    cur.execute("LIST @NUGGET_CAP_STAGE")
    rows = cur.fetchall()

print("\n-- Stage files --")
for r in rows:
    print("  ", r[0])
print("\nDone: raw JSON landed in stage.")
