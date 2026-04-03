"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 06-02 · Bulk Write Operations                                        ║
║  Mix inserts, updates, and deletes in one atomic batch.                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Use bulk_write() to combine multiple different operations into a single
server round-trip — maximizing throughput for write-heavy pipelines.

CONCEPTS
────────
bulk_write(operations, ordered=True):
  - Sends a mixed list of write operations to the server in ONE batch.
  - More efficient than individual round-trips: one network hop, one ack.
  - Operations can be: InsertOne, UpdateOne, UpdateMany, ReplaceOne,
                        DeleteOne, DeleteMany.

bulk_write vs insert_many:
  - insert_many:  only inserts.
  - bulk_write:   any mix of insert / update / delete / replace.
  - For pure inserts, insert_many is slightly more efficient.
  - For mixed workloads (ETL, CDC apply), bulk_write is the right tool.

ordered parameter (same semantics as insert_many):
  - ordered=True  (default): stops on first error.
  - ordered=False: continues on errors, reports all at end via BulkWriteError.
    Use ordered=False for parallel-safe upsert pipelines.

BulkWriteResult fields:
  .inserted_count    → how many InsertOne succeeded
  .matched_count     → how many docs matched an update/replace filter
  .modified_count    → how many docs were actually changed
  .upserted_count    → how many upserts created new docs
  .deleted_count     → how many docs were deleted
  .upserted_ids      → dict of {batch_index: _id} for upserted documents

Upsert in bulk:
  UpdateOne(..., upsert=True) in a bulk_write is the standard pattern for
  syncing external data into MongoDB. It's the equivalent of SQL's MERGE.

CDC apply pattern:
  A common data engineering pattern is to consume CDC events from Kafka
  and apply them in bulk to MongoDB:
    INSERT event  → InsertOne (or UpdateOne with upsert=True for idempotency)
    UPDATE event  → UpdateOne
    DELETE event  → DeleteOne
  Process in ordered=False batches of N events for maximum throughput.
  Checkpoint the Kafka offset only after bulk_write succeeds.

USAGE
─────
    python 02_bulk_write_ops.py
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

from pymongo import InsertOne, UpdateOne, UpdateMany, DeleteOne, ReplaceOne
from pymongo.errors import BulkWriteError

sys.path.insert(0, str(Path(__file__).parent.parent))
from _mg_connect import get_lab_db

db = get_lab_db()
db.drop_collection("catalog")
col = db["catalog"]
now = datetime.now(tz=timezone.utc)

print("\n── Bulk Write Operations ─────────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Mixed bulk_write: inserts + update + delete in one batch
# ─────────────────────────────────────────────────────────────────────────────
# Seed a few existing docs first
col.insert_many([
    {"_id": "P001", "name": "Old Keyboard",   "price": 89.0,  "status": "active"},
    {"_id": "P002", "name": "Old Mouse",      "price": 45.0,  "status": "active"},
    {"_id": "P003", "name": "Discontinued",   "price": 5.0,   "status": "active"},
])

operations = [
    # Insert new products
    InsertOne({"_id": "P004", "name": "Mechanical KB",     "price": 109.0, "status": "active", "created_at": now}),
    InsertOne({"_id": "P005", "name": "Wireless Trackpad", "price": 79.99, "status": "active", "created_at": now}),

    # Update an existing product's price
    UpdateOne({"_id": "P001"}, {"$set": {"price": 99.0, "name": "Pro Keyboard", "updated_at": now}}),

    # Upsert — insert if not found, update if found
    UpdateOne(
        {"_id": "P006"},   # doesn't exist yet
        {"$set": {"name": "USB-C Hub", "price": 29.99, "status": "active"},
         "$setOnInsert": {"created_at": now}},
        upsert=True,
    ),

    # Mark all items with price < 10 as discontinued
    UpdateMany({"price": {"$lt": 10.0}}, {"$set": {"status": "discontinued"}}),

    # Delete the old discontinued product
    DeleteOne({"_id": "P003"}),

    # Replace P002 entirely (except _id)
    ReplaceOne({"_id": "P002"}, {"_id": "P002", "name": "Ergonomic Mouse", "price": 59.99,
                                  "status": "active", "updated_at": now}),
]

result = col.bulk_write(operations, ordered=True)

print(f"\n  Mixed bulk_write results:")
print(f"    inserted_count:   {result.inserted_count}")
print(f"    matched_count:    {result.matched_count}")
print(f"    modified_count:   {result.modified_count}")
print(f"    upserted_count:   {result.upserted_count}  (P006 was created via upsert)")
print(f"    deleted_count:    {result.deleted_count}")
print(f"    upserted_ids:     {result.upserted_ids}")

print(f"\n  Catalog after bulk_write ({col.count_documents({})} docs):")
for doc in col.find({}, {"name": 1, "price": 1, "status": 1}).sort("_id", 1):
    print(f"    {doc['_id']}  {doc['name']:<22} ${doc['price']:.2f}  [{doc['status']}]")

# ─────────────────────────────────────────────────────────────────────────────
# 2. ordered=False — continue on errors (e.g. duplicate key)
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n  Testing unordered bulk with partial failure:")
operations_with_dup = [
    InsertOne({"_id": "P007", "name": "Webcam",   "price": 79.0}),
    InsertOne({"_id": "P004", "name": "DUPLICATE", "price": 0.0}),  # duplicate _id → error
    InsertOne({"_id": "P008", "name": "Monitor",  "price": 299.0}),  # should still succeed
]
try:
    result = col.bulk_write(operations_with_dup, ordered=False)
except BulkWriteError as exc:
    details = exc.details
    print(f"    inserted_count: {details['nInserted']}  (P007 and P008 succeeded)")
    print(f"    errors:         {len(details['writeErrors'])}  (P004 duplicate)")
    for err in details["writeErrors"]:
        print(f"      index={err['index']} code={err['code']} "
              f"keyValue={err.get('keyValue', {})}")

print(f"  Catalog now has {col.count_documents({})} documents.")

# ─────────────────────────────────────────────────────────────────────────────
# 3. CDC apply pattern — simulate processing Kafka-style CDC events
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n  CDC apply pattern (simulated Kafka events → bulk_write):")

cdc_events = [
    {"op": "INSERT", "_id": "P010", "name": "Gaming Chair",   "price": 399.0},
    {"op": "UPDATE", "_id": "P007", "fields": {"price": 85.0, "stock": 50}},
    {"op": "DELETE", "_id": "P008"},
    {"op": "INSERT", "_id": "P011", "name": "Standing Desk",  "price": 599.0},
    {"op": "UPDATE", "_id": "P004", "fields": {"name": "Mechanical KB Pro"}},
]

def build_bulk_ops(events: list[dict]) -> list:
    ops = []
    for ev in events:
        if ev["op"] == "INSERT":
            ops.append(UpdateOne(
                {"_id": ev["_id"]},
                {"$set": {k: v for k, v in ev.items() if k not in ("op", "_id")},
                 "$setOnInsert": {"created_at": now}},
                upsert=True,
            ))
        elif ev["op"] == "UPDATE":
            ops.append(UpdateOne(
                {"_id": ev["_id"]},
                {"$set": {**ev.get("fields", {}), "updated_at": now}},
            ))
        elif ev["op"] == "DELETE":
            ops.append(DeleteOne({"_id": ev["_id"]}))
    return ops

result = col.bulk_write(build_bulk_ops(cdc_events), ordered=False)
print(f"    Processed {len(cdc_events)} CDC events:")
print(f"    upserted={result.upserted_count}  modified={result.modified_count}  "
      f"deleted={result.deleted_count}")

db.drop_collection("catalog")
print()
