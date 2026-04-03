"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 01-02 · Bulk Inserts & Ordered vs Unordered Writes                   ║
║  Efficient batch loading and understanding write failure semantics.           ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Insert multiple documents at once and understand the critical difference between
ordered and unordered bulk writes — a common source of production surprises.

CONCEPTS
────────
insert_many(documents, ordered=True):
  - Inserts a list of documents in a single batch operation.
  - ordered=True  (default):
      Documents are inserted in sequence. If one fails (e.g. duplicate _id),
      the batch STOPS at the failure point. Documents BEFORE the error are
      persisted. Documents AFTER are NOT inserted.
      Use for: pipelines where order and atomicity per-doc matters.

  - ordered=False:
      All inserts are attempted regardless of individual failures.
      The driver reports all errors at the end via BulkWriteError.
      Documents that succeeded ARE persisted even if others fail.
      Use for: high-throughput ingestion where partial success is acceptable.

BulkWriteError:
  - Raised by insert_many and bulk_write operations on partial failures.
  - exc.details["writeErrors"] → list of per-document error dicts.
  - exc.details["nInserted"]   → how many documents were actually inserted.

Write Batching:
  - pymongo automatically splits large insert_many calls into ≤ 100,000 doc
    batches (or ≤ 48 MB), matching the MongoDB server's maxWriteBatchSize.
  - You never need to manually chunk for normal inserts.

PyMongo's result types:
  - InsertManyResult.inserted_ids  → list of _ids actually inserted.
  - InsertManyResult.acknowledged  → True if write concern was satisfied.

When to use insert_many vs bulk_write:
  - insert_many  → all inserts, same collection.
  - bulk_write   → mixed operations (inserts + updates + deletes) in one round-trip.
                   Covered in nugget 06_transactions/02_bulk_write_ops.py.

USAGE
─────
    python 02_insert_many.py

EXPECTED OUTPUT
───────────────
    ── Bulk Inserts ──────────────────────────────────

      Inserted 5 orders (ordered). IDs:
        [ObjectId('...'), ObjectId('...'), ...]

      Testing ordered failure:
        Error after 2 inserted: duplicate key error (E11000) on _id='o-DUP'
        Orders in collection after partial ordered insert: 2

      Testing unordered failure:
        Errors: 1 duplicate key error(s)
        Inserted (unordered, skipping dupes): 4
        Total orders in collection: 6
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

from pymongo.errors import BulkWriteError

sys.path.insert(0, str(Path(__file__).parent.parent))
from _mg_connect import get_lab_db

db = get_lab_db()

print("\n── Bulk Inserts ──────────────────────────────────")

db.drop_collection("orders")
orders = db["orders"]

# ─────────────────────────────────────────────────────────────────────────────
# 1. Successful insert_many (all auto-ObjectId _ids)
# ─────────────────────────────────────────────────────────────────────────────
docs = [
    {"customer_id": f"C{i:03d}", "amount": round(10.0 + i * 7.5, 2),
     "status": "pending", "created_at": datetime.now(tz=timezone.utc)}
    for i in range(1, 6)
]
result = orders.insert_many(docs)
print(f"\n  Inserted {len(result.inserted_ids)} orders (ordered). IDs:")
print(f"    {result.inserted_ids}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Ordered insert with a duplicate key in the MIDDLE
#    The third document has the same _id as the second → E11000.
#    With ordered=True, only the first 2 are inserted; items 3–5 are skipped.
# ─────────────────────────────────────────────────────────────────────────────
db.drop_collection("orders")
orders = db["orders"]

ordered_docs = [
    {"_id": "o-001", "customer_id": "C001", "amount": 99.99},
    {"_id": "o-002", "customer_id": "C002", "amount": 149.00},
    {"_id": "o-DUP", "customer_id": "C003", "amount": 50.00},  # will succeed
    {"_id": "o-DUP", "customer_id": "C003", "amount": 50.00},  # DUPLICATE → stops here
    {"_id": "o-005", "customer_id": "C005", "amount": 75.00},  # never reached
]

print(f"\n  Testing ordered failure:")
try:
    orders.insert_many(ordered_docs, ordered=True)
except BulkWriteError as exc:
    n_inserted = exc.details.get("nInserted", 0)
    errors = exc.details.get("writeErrors", [])
    err_code = errors[0].get("code") if errors else "?"
    err_key  = errors[0].get("keyValue") if errors else {}
    print(f"    Error after {n_inserted} inserted: duplicate key error "
          f"(E{err_code}) on _id='{err_key.get('_id', '?')}'")
    count = orders.count_documents({})
    print(f"    Orders in collection after partial ordered insert: {count}")

# ─────────────────────────────────────────────────────────────────────────────
# 3. Unordered insert — skips duplicates, continues with the rest
#    Same batch as above, but with ordered=False.
#    The duplicate "o-DUP" that was already inserted fails; the others succeed.
# ─────────────────────────────────────────────────────────────────────────────
remaining = [
    {"_id": "o-DUP", "customer_id": "C003", "amount": 50.00},  # already in DB → dup
    {"_id": "o-004", "customer_id": "C004", "amount": 88.50},
    {"_id": "o-005", "customer_id": "C005", "amount": 75.00},
    {"_id": "o-006", "customer_id": "C006", "amount": 110.25},
    {"_id": "o-007", "customer_id": "C007", "amount": 33.00},
]

print(f"\n  Testing unordered failure:")
try:
    orders.insert_many(remaining, ordered=False)
except BulkWriteError as exc:
    errors = exc.details.get("writeErrors", [])
    n_inserted = exc.details.get("nInserted", 0)
    print(f"    Errors: {len(errors)} duplicate key error(s)")
    print(f"    Inserted (unordered, skipping dupes): {n_inserted}")

total = orders.count_documents({})
print(f"    Total orders in collection: {total}")
print()
