"""
Mini Capstone 05: Demonstrate recovery with Time Travel.

PURPOSE
- Show recovery workflow after accidental DROP using UNDROP + Time Travel validation.

TEACHABLE CONCEPTS
- UNDROP restores dropped objects inside retention window.
- AT(STATEMENT => ...) is a stable Time Travel anchor for demos/tests.
- Statement anchors are safer than fixed OFFSET for newly created tables.

EXPECTED OUTPUT (typical)
    Rows before drop: 3
    Rows after undrop: 3
    Rows at anchored statement time (Time Travel): 3

    Done: recovery workflow demonstrated.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _sf_connect import get_connection

conn = get_connection(autocommit=True)
with conn.cursor() as cur:
    # Baseline read and capture query id as valid Time Travel anchor.
    cur.execute("SELECT COUNT(*) FROM NUGGET_CAP_CURATED_EVENTS")
    before = cur.fetchone()[0]
    anchor_query_id = cur.sfqid

    # Optional snapshot table so learners can inspect pre-drop state directly.
    cur.execute("CREATE OR REPLACE TABLE NUGGET_CAP_CURATED_SNAPSHOT AS SELECT * FROM NUGGET_CAP_CURATED_EVENTS")

    # Simulate accidental destructive operation.
    cur.execute("DROP TABLE IF EXISTS NUGGET_CAP_CURATED_EVENTS")

    # Recover dropped table from Time Travel retention window.
    cur.execute("UNDROP TABLE NUGGET_CAP_CURATED_EVENTS")
    cur.execute("SELECT COUNT(*) FROM NUGGET_CAP_CURATED_EVENTS")
    after = cur.fetchone()[0]

    # Validate historical state with anchored statement-time query.
    cur.execute(f"""
        SELECT COUNT(*)
        FROM NUGGET_CAP_CURATED_EVENTS
        AT(STATEMENT => '{anchor_query_id}')
    """)
    past = cur.fetchone()[0]

print(f"\nRows before drop: {before}")
print(f"Rows after undrop: {after}")
print(f"Rows at anchored statement time (Time Travel): {past}")
print("\nDone: recovery workflow demonstrated.")
