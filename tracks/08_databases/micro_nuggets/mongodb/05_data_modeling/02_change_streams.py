"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 05-02 · Change Streams                                               ║
║  Real-time CDC — watch MongoDB collections like a Kafka consumer.            ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Use MongoDB Change Streams to react to inserts, updates, and deletes in
real time — without polling. Implement CDC (Change Data Capture) patterns
including resume token checkpointing for fault-tolerant pipelines.

CONCEPTS
────────
Change Streams:
  - Available on replica sets and sharded clusters (Atlas is always replica set).
  - Built on MongoDB's oplog (operations log) — the same log used for replication.
  - Returns a cursor that BLOCKS until a change event arrives.
  - Events include: insert, update, delete, replace, drop, rename, invalidate.

watch() API:
  collection.watch()      → watch one collection
  db.watch()              → watch all collections in a database
  client.watch()          → watch all databases (requires admin privileges)

Change event document structure:
  {
    "_id":              <resume token>    ← checkpoint this to resume later
    "operationType":    "insert" | "update" | "delete" | "replace" | ...
    "fullDocument":     <the document>   ← for insert/replace; update needs option
    "documentKey":      {"_id": ...}     ← which document changed
    "updateDescription": {               ← only for operationType="update"
        "updatedFields": {"field": value, ...},
        "removedFields": ["field", ...],
    }
    "ns":               {"db": "...", "coll": "..."}
    "clusterTime":      <Timestamp>
  }

fullDocument on updates:
  By default, update events only contain "updateDescription" (the diff).
  To get the full post-update document:
    watch(full_document="updateLookup")
  ⚠ This is a separate round-trip to fetch the document — adds latency.
  ⚠ If the document is deleted between the update and the lookup, fullDocument is None.

Resume Token:
  - Each change event has a "_id" field that is the resume token.
  - Save this token to durable storage (e.g., another MongoDB collection).
  - On restart: watch(resume_after=saved_token) to pick up from where you left off.
  - Without a resume token, you miss events that occurred while the consumer was down.
  - Atlas also supports startAtOperationTime for time-based resume.

Aggregation pipeline filters on watch():
  - Pass a pipeline to filter which events you receive server-side.
  - Reduces network traffic — you don't receive events you don't care about.
  - Allowed stages: $match, $project, $addFields, $replaceRoot, $redact.
  - Example: only receive insert events on specific fields.

NOTE: This nugget simulates change stream output using a thread for writes,
      with a 5-second timeout to prevent hanging indefinitely.

USAGE
─────
    python 02_change_streams.py
"""
from __future__ import annotations

import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _mg_connect import get_client, LAB_DB

client = get_client()
db     = client[LAB_DB]

print("\n── Change Streams ────────────────────────────────")

db.drop_collection("events_cdc")
col = db["events_cdc"]

# ─────────────────────────────────────────────────────────────────────────────
# Resume token store — in production, save to a dedicated collection or Redis.
# Here we use a simple in-memory dict for demo purposes.
# ─────────────────────────────────────────────────────────────────────────────
checkpoint: dict = {"token": None}
received_events: list = []

# ─────────────────────────────────────────────────────────────────────────────
# Writer thread — simulates application writes during CDC consumption
# ─────────────────────────────────────────────────────────────────────────────
def writer():
    time.sleep(0.5)   # let the watcher open first
    now = datetime.now(tz=timezone.utc)

    # INSERT
    col.insert_one({"_id": "E001", "type": "login",    "user": "alice", "ts": now})
    time.sleep(0.2)
    col.insert_one({"_id": "E002", "type": "purchase", "user": "bob",   "ts": now, "amount": 99.99})
    time.sleep(0.2)

    # UPDATE
    col.update_one({"_id": "E001"}, {"$set": {"status": "logged_out", "updated_at": now}})
    time.sleep(0.2)

    # DELETE
    col.delete_one({"_id": "E002"})
    time.sleep(0.2)

    # REPLACE
    col.replace_one({"_id": "E001"}, {"_id": "E001", "type": "session_end", "user": "alice",
                                       "duration_s": 3600, "ts": now})

# ─────────────────────────────────────────────────────────────────────────────
# Watch with a filter pipeline — only capture insert and delete events
# (updates and replaces will be silently ignored by the server-side filter)
# ─────────────────────────────────────────────────────────────────────────────
filter_pipeline = [
    {"$match": {"operationType": {"$in": ["insert", "delete", "update", "replace"]}}}
]

print(f"\n  Opening change stream on 'events_cdc' (5-second timeout)...")
print(f"  Watching for: insert, update, delete, replace")

writer_thread = threading.Thread(target=writer, daemon=True)
writer_thread.start()

event_count = 0
try:
    with col.watch(pipeline=filter_pipeline, full_document="updateLookup") as stream:
        # max_await_time_ms: how long to block waiting for the next event
        stream.max_await_time_ms = 500

        deadline = time.time() + 5.0   # 5-second total window
        while time.time() < deadline and event_count < 5:
            try:
                change = stream.try_next()   # non-blocking poll
            except Exception:
                break
            if change is None:
                time.sleep(0.1)
                continue

            op    = change["operationType"]
            key   = change.get("documentKey", {})
            token = change["_id"]

            # ─── Checkpoint the resume token ────────────────────────────────
            checkpoint["token"] = token

            event_count += 1
            print(f"\n  Event #{event_count}: {op.upper()}")
            print(f"    documentKey: {key}")

            if op == "insert":
                doc = change.get("fullDocument", {})
                print(f"    fullDocument: type={doc.get('type')}  user={doc.get('user')}")

            elif op == "update":
                desc = change.get("updateDescription", {})
                updated = desc.get("updatedFields", {})
                removed = desc.get("removedFields", [])
                full    = change.get("fullDocument")
                print(f"    updatedFields: {list(updated.keys())}")
                if removed:
                    print(f"    removedFields: {removed}")
                if full:
                    print(f"    fullDocument (via updateLookup): _id={full.get('_id')}")

            elif op == "delete":
                print(f"    (document deleted — no fullDocument available)")

            elif op == "replace":
                doc = change.get("fullDocument", {})
                print(f"    replaced with: {doc}")

            received_events.append({"op": op, "key": key})

except Exception as exc:
    print(f"\n  [!] Stream error: {exc}")

writer_thread.join(timeout=3)

# ─────────────────────────────────────────────────────────────────────────────
# Resume token demo — show what we saved and how to resume
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n  Captured {event_count} events.")
if checkpoint["token"]:
    print(f"  Last resume token saved: {str(checkpoint['token'])[:60]}...")
    print(f"  To resume after restart:")
    print(f"    col.watch(resume_after=saved_token)")
else:
    print(f"  No resume token captured (no events received).")

# ─────────────────────────────────────────────────────────────────────────────
# Summary of all ops received
# ─────────────────────────────────────────────────────────────────────────────
from collections import Counter
counts = Counter(e["op"] for e in received_events)
print(f"\n  Operation counts: {dict(counts)}")

db.drop_collection("events_cdc")
client.close()
print()
