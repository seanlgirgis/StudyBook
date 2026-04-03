"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  CAPSTONE 01 · Land Raw Events (Bronze Layer)                                ║
║  Ingest raw telemetry events into MongoDB — the Bronze tier of the pipeline. ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Simulate a real-world telemetry ingestion pipeline:
  - Generate 500 raw event documents (page_views, clicks, purchases, errors).
  - Write them in idempotent bulk batches (upsert by event_id).
  - Create indexes to support downstream Silver and Gold queries.
  - Record an ingestion run in a control table.

PIPELINE OVERVIEW
─────────────────
  This capstone implements a 3-tier MongoDB data pipeline:

  Bronze:  cap01 — raw events as they arrive (append-only, no transforms)
  Silver:  cap02 — deduplicated, validated, enriched aggregated view
  Gold:    cap03 — upserted business metrics for dashboards

DESIGN DECISIONS
────────────────
  1. Upsert by event_id (not blind insert):
     Idempotent — safe to re-run after partial failures or retries.
     Prevents duplicate events from upstream Kafka/API producers.

  2. landed_at vs event_ts:
     event_ts   = when the event happened in the application.
     landed_at  = when we wrote it to MongoDB.
     Delta between them = pipeline lag — useful for SLA monitoring.

  3. Control table (ingestion_runs):
     Tracks what was ingested, when, and how many documents.
     Enables replay: "re-ingest from batch 5 onwards".
     Pattern mirrors Delta Lake's ingestion control table nugget.

  4. Ordered=False bulk write:
     If a duplicate slips through, the others still land.
     The $upsert pattern anyway makes duplicates harmless.

USAGE
─────
    python 01_land_raw_events.py

EXPECTED OUTPUT
───────────────
    ── CAPSTONE 01 · Land Raw Events ─────────────────

      Generating 500 raw telemetry events...

      Upserting batch 1/5  (100 events)... done  inserted=100 modified=0
      Upserting batch 2/5  (100 events)... done  inserted=100 modified=0
      ...

      Indexes created on raw_events:
        idx_event_ts     (event_ts)
        idx_type         (event_type, event_ts)
        idx_session      (session_id)
        idx_user         (user_id, event_ts)

      Run recorded: run_id=... total_docs=500

      Bronze layer ready. Run 02_aggregate_silver.py next.
"""
from __future__ import annotations

import sys
import random
import uuid
from datetime import datetime, timezone, timedelta
from pathlib import Path

from pymongo import UpdateOne
from pymongo.errors import BulkWriteError
import pymongo

sys.path.insert(0, str(Path(__file__).parent.parent))
from _mg_connect import get_lab_db

db = get_lab_db()
print("\n── CAPSTONE 01 · Land Raw Events ─────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# Setup — drop and recreate collections for a clean capstone run
# ─────────────────────────────────────────────────────────────────────────────
for col_name in ["raw_events", "silver_metrics", "gold_dashboard", "ingestion_runs"]:
    db.drop_collection(col_name)
raw_events = db["raw_events"]
runs_col   = db["ingestion_runs"]

# ─────────────────────────────────────────────────────────────────────────────
# Generate 500 synthetic telemetry events
# ─────────────────────────────────────────────────────────────────────────────
print("\n  Generating 500 raw telemetry events...")
random.seed(2026)
now = datetime.now(tz=timezone.utc)

event_types = ["page_view", "click", "purchase", "error", "search", "add_to_cart"]
pages       = ["/home", "/product/123", "/product/456", "/cart", "/checkout", "/search"]
devices     = ["mobile", "desktop", "tablet"]
countries   = ["US", "UK", "DE", "FR", "CA", "AU", "JP"]

events = []
for i in range(500):
    etype    = random.choices(event_types, weights=[30, 25, 10, 5, 15, 15])[0]
    user_id  = f"U{random.randint(1, 100):04d}"
    session  = f"SES-{random.randint(1, 200):05d}"
    event_ts = now - timedelta(
        days=random.randint(0, 29),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
    )
    event: dict = {
        "event_id":   str(uuid.uuid4()),
        "event_type": etype,
        "user_id":    user_id,
        "session_id": session,
        "event_ts":   event_ts,
        "landed_at":  now,
        "device":     random.choice(devices),
        "country":    random.choice(countries),
        "page":       random.choice(pages),
    }
    if etype == "purchase":
        event["amount"]     = round(random.uniform(10.0, 500.0), 2)
        event["product_id"] = f"P{random.randint(1, 50):03d}"
    if etype == "error":
        event["error_code"] = random.choice(["404", "500", "503", "timeout"])
    events.append(event)

# ─────────────────────────────────────────────────────────────────────────────
# Upsert in batches of 100 (idempotent: safe to re-run)
# ─────────────────────────────────────────────────────────────────────────────
BATCH_SIZE = 100
total_inserted = 0
total_modified = 0

for batch_num, start in enumerate(range(0, len(events), BATCH_SIZE), 1):
    batch = events[start:start + BATCH_SIZE]
    ops   = [
        UpdateOne(
            {"event_id": ev["event_id"]},           # match by natural key
            {"$set": ev, "$setOnInsert": {"_ingested_at": now}},
            upsert=True,
        )
        for ev in batch
    ]
    print(f"  Upserting batch {batch_num}/{len(events)//BATCH_SIZE}  "
          f"({len(batch)} events)...", end="", flush=True)
    try:
        result = raw_events.bulk_write(ops, ordered=False)
        ins = result.upserted_count
        mod = result.modified_count
        total_inserted += ins
        total_modified += mod
        print(f" done  inserted={ins} modified={mod}")
    except BulkWriteError as exc:
        ins = exc.details.get("nUpserted", 0)
        mod = exc.details.get("nModified", 0)
        errs = len(exc.details.get("writeErrors", []))
        total_inserted += ins
        total_modified += mod
        print(f" partial  inserted={ins} modified={mod} errors={errs}")

# ─────────────────────────────────────────────────────────────────────────────
# Create indexes to support Silver and Gold queries
# ─────────────────────────────────────────────────────────────────────────────
raw_events.create_index([("event_ts", pymongo.ASCENDING)],                              name="idx_event_ts")
raw_events.create_index([("event_type", pymongo.ASCENDING), ("event_ts", pymongo.ASCENDING)], name="idx_type")
raw_events.create_index([("session_id", pymongo.ASCENDING)],                             name="idx_session")
raw_events.create_index([("user_id", pymongo.ASCENDING), ("event_ts", pymongo.ASCENDING)], name="idx_user")
raw_events.create_index([("event_id", pymongo.ASCENDING)], unique=True,                  name="idx_event_id")

print(f"\n  Indexes created on raw_events:")
for idx in raw_events.list_indexes():
    if idx["name"] != "_id_":
        print(f"    {idx['name']:<20} {dict(idx['key'])}")

# ─────────────────────────────────────────────────────────────────────────────
# Record ingestion run in control table
# ─────────────────────────────────────────────────────────────────────────────
run_doc = {
    "run_id":     str(uuid.uuid4()),
    "stage":      "bronze",
    "collection": "raw_events",
    "started_at": now,
    "completed_at": datetime.now(tz=timezone.utc),
    "total_events": len(events),
    "inserted": total_inserted,
    "modified": total_modified,
    "status":   "success",
}
runs_col.insert_one(run_doc)
print(f"\n  Run recorded: run_id={run_doc['run_id'][:12]}...  "
      f"total_docs={raw_events.count_documents({})}")

print(f"\n  Bronze layer ready. Run 02_aggregate_silver.py next.")
print()
