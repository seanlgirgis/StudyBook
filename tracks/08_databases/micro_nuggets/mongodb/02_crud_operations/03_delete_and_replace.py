"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 02-03 · Delete & Replace                                             ║
║  Removing documents and full-document replacement patterns.                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Understand the full spectrum of delete and replace operations in MongoDB,
including soft-delete patterns used in production data pipelines.

CONCEPTS
────────
delete_one(filter):
  - Removes the FIRST document that matches the filter.
  - Returns DeleteResult with .deleted_count (0 or 1).
  - Use when you have a unique filter (like _id) or want to remove just one.

delete_many(filter):
  - Removes ALL documents matching the filter.
  - Returns DeleteResult with .deleted_count.
  - delete_many({}) empties the collection (does NOT drop indexes).
  - DANGER: always double-check the filter before running delete_many.

find_one_and_delete(filter):
  - Atomically finds, returns, and deletes a document in one round-trip.
  - Returns the deleted document (or None if no match).
  - Use for: queue consumption, "pop" patterns, audit-before-delete.

replace_one(filter, replacement, upsert=False):
  - Replaces the ENTIRE matched document with a new one.
  - The replacement must NOT contain update operators ($set, $inc, etc.).
  - The _id field is preserved (not replaced) even if omitted from replacement.
  - Returns UpdateResult with .matched_count and .modified_count.

replace_one vs update_one:
  - update_one + $set: surgical — changes ONLY the specified fields.
  - replace_one:       nuclear  — replaces EVERYTHING except _id.
  - Use replace_one when you have a complete new version of the document
    (e.g. syncing from an external source). Use update for partial edits.

Soft-delete pattern:
  - Rather than deleting, set {"deleted": True, "deleted_at": timestamp}.
  - All queries filter with {"deleted": {"$ne": True}}.
  - Enables recovery, audit trails, and change stream replay.
  - Compound index on {deleted: 1, <query_field>: 1} prevents full scans.
  - Standard in data pipelines where downstream consumers need a CDC feed.

TTL-based cleanup:
  - Create a TTL index on the deleted_at field for automatic purge:
      col.create_index("deleted_at", expireAfterSeconds=2592000)  # 30 days
  - Covered in nugget 07_operations/01_ttl_and_capped.py.

USAGE
─────
    python 03_delete_and_replace.py
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _mg_connect import get_lab_db

db = get_lab_db()
db.drop_collection("events")
col = db["events"]
now = datetime.now(tz=timezone.utc)

col.insert_many([
    {"_id": "ev-001", "type": "click",    "user": "u1", "ts": now, "deleted": False},
    {"_id": "ev-002", "type": "purchase", "user": "u1", "ts": now, "deleted": False},
    {"_id": "ev-003", "type": "click",    "user": "u2", "ts": now, "deleted": False},
    {"_id": "ev-004", "type": "click",    "user": "u2", "ts": now, "deleted": False},
    {"_id": "ev-005", "type": "login",    "user": "u3", "ts": now, "deleted": False},
    {"_id": "ev-006", "type": "logout",   "user": "u3", "ts": now, "deleted": False},
])

print("\n── Delete & Replace ──────────────────────────────")
print(f"\n  Seeded {col.count_documents({})} events.")

# ─────────────────────────────────────────────────────────────────────────────
# delete_one — remove exactly one document
# ─────────────────────────────────────────────────────────────────────────────
result = col.delete_one({"_id": "ev-006"})
print(f"\n  [delete_one]   Deleted ev-006: deleted_count={result.deleted_count}")

# ─────────────────────────────────────────────────────────────────────────────
# delete_many — remove all matching
# ─────────────────────────────────────────────────────────────────────────────
result = col.delete_many({"type": "click", "user": "u2"})
print(f"  [delete_many]  Deleted u2 clicks: deleted_count={result.deleted_count}")
print(f"  Remaining: {col.count_documents({})}")

# ─────────────────────────────────────────────────────────────────────────────
# find_one_and_delete — atomic fetch + remove (queue pop pattern)
# Useful for: background workers pulling work items, audit-before-delete.
# ─────────────────────────────────────────────────────────────────────────────
popped = col.find_one_and_delete({"type": "click"})
print(f"\n  [find_one_and_delete] Popped event: {popped['_id']} (type={popped['type']})")
print(f"  Remaining: {col.count_documents({})}")

# ─────────────────────────────────────────────────────────────────────────────
# replace_one — full document replacement
# The entire document is replaced except the _id field.
# ─────────────────────────────────────────────────────────────────────────────
r = col.replace_one(
    {"_id": "ev-002"},
    {
        # Note: _id can be omitted — MongoDB preserves it.
        "type":       "purchase_v2",
        "user":       "u1",
        "amount":     99.99,
        "currency":   "USD",
        "ts":         datetime.now(tz=timezone.utc),
        "deleted":    False,
        # "source" field from original is GONE — full replacement.
    }
)
doc = col.find_one({"_id": "ev-002"})
print(f"\n  [replace_one]  ev-002 after replace: {doc}")

# ─────────────────────────────────────────────────────────────────────────────
# Soft-delete pattern — production standard
# Rather than deleting, mark deleted=True with a timestamp.
# Queries always filter with {"deleted": {"$ne": True}}.
# ─────────────────────────────────────────────────────────────────────────────
col.insert_many([
    {"_id": f"ev-10{i}", "type": "view", "user": f"u{i}", "deleted": False}
    for i in range(1, 6)
])

# Soft-delete ev-101 and ev-102
col.update_many(
    {"_id": {"$in": ["ev-101", "ev-102"]}},
    {"$set": {"deleted": True, "deleted_at": datetime.now(tz=timezone.utc)}},
)

active_count  = col.count_documents({"deleted": {"$ne": True}})
deleted_count = col.count_documents({"deleted": True})
print(f"\n  [soft-delete]  Active events:  {active_count}")
print(f"                 Deleted events: {deleted_count} (still in DB, queryable)")

# Recovery: un-delete ev-101
col.update_one(
    {"_id": "ev-101"},
    {"$set": {"deleted": False}, "$unset": {"deleted_at": ""}},
)
print(f"  [soft-recover] ev-101 recovered. Active now: {col.count_documents({'deleted': {'$ne': True}})}")
print()
