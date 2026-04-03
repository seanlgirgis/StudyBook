"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 02-02 · Update Operators                                             ║
║  Surgical document mutations — the MongoDB way to avoid full rewrites.       ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Master MongoDB's update operators for precise field-level mutations.
Never replace a document when you only need to change one field.

CONCEPTS
────────
Update operation anatomy:
  collection.update_one(filter, update, upsert=False)
  collection.update_many(filter, update)
  collection.find_one_and_update(filter, update, return_document=ReturnDocument.AFTER)

  - filter   → which documents to match (same MQL as find).
  - update   → what to change (must use operators — plain dict = error in 4.x).
  - upsert   → if True, inserts a new document when no match is found.

Update operators (grouped by purpose):

  FIELD OPERATORS
  ───────────────
  $set        → set field to value (creates field if absent)
                {"$set": {"status": "active", "updated_at": now}}

  $unset      → remove a field entirely (value doesn't matter, use "" or 1)
                {"$unset": {"temp_field": ""}}

  $rename     → rename a field atomically
                {"$rename": {"old_name": "new_name"}}

  $setOnInsert → only applies during an upsert insert (ignored on updates)
                {"$setOnInsert": {"created_at": now}}

  $currentDate → server-sets to current date (avoids client clock skew)
                {"$currentDate": {"updated_at": True}}

  NUMERIC OPERATORS
  ─────────────────
  $inc        → increment by N (use negative for decrement)
                {"$inc": {"stock": -1, "sold_count": 1}}

  $mul        → multiply by N
                {"$mul": {"price": 0.9}}   ← 10% discount

  $min        → only update if new value is LESS than current
  $max        → only update if new value is GREATER than current
                Useful for watermarks: {"$max": {"high_score": new_score}}

  ARRAY OPERATORS
  ───────────────
  $push       → append a value to an array (creates array if absent)
                {"$push": {"tags": "sale"}}

  $push + $each → append multiple values at once
                {"$push": {"tags": {"$each": ["clearance", "limited"]}}}

  $addToSet   → append ONLY if value is not already in the array (set semantics)
                {"$addToSet": {"tags": "wireless"}}  ← no-op if already there

  $pull       → remove all elements matching a value or condition
                {"$pull": {"tags": "old-tag"}}

  $pop        → remove first (-1) or last (1) element of array
                {"$pop": {"history": -1}}

  $push + $slice → maintain a fixed-size sliding window array
                {"$push": {"recent_prices": {"$each": [199.99], "$slice": -5}}}

ReturnDocument:
  find_one_and_update returns the document BEFORE update by default.
  Use return_document=ReturnDocument.AFTER to get the post-update version.

USAGE
─────
    python 02_update_operators.py
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

from pymongo import ReturnDocument

sys.path.insert(0, str(Path(__file__).parent.parent))
from _mg_connect import get_lab_db

db = get_lab_db()
db.drop_collection("inventory")
inv = db["inventory"]

now = datetime.now(tz=timezone.utc)

# Seed data
inv.insert_many([
    {"_id": "sku-001", "name": "Mechanical Keyboard", "price": 109.0, "stock": 25,
     "sold_count": 0, "tags": ["mechanical", "wireless"], "status": "active",
     "price_history": [109.0], "updated_at": now},
    {"_id": "sku-002", "name": "Gaming Mouse", "price": 69.99, "stock": 50,
     "sold_count": 10, "tags": ["gaming", "wired"], "status": "active",
     "price_history": [79.99, 69.99], "updated_at": now},
    {"_id": "sku-003", "name": "Monitor Stand", "price": 45.00, "stock": 5,
     "sold_count": 3, "tags": ["desk"], "status": "low_stock",
     "price_history": [45.00], "updated_at": now},
])

print("\n── Update Operators ──────────────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# $set — change one or more fields, create if absent
# ─────────────────────────────────────────────────────────────────────────────
result = inv.update_one(
    {"_id": "sku-001"},
    {"$set": {"status": "featured", "updated_at": datetime.now(tz=timezone.utc)}}
)
doc = inv.find_one({"_id": "sku-001"}, {"status": 1, "_id": 0})
print(f"\n  [$set]      sku-001 status → {doc['status']}")

# ─────────────────────────────────────────────────────────────────────────────
# $inc — decrement stock, increment sold_count atomically
# Atomicity is per-document: both increments happen together or not at all.
# ─────────────────────────────────────────────────────────────────────────────
inv.update_one(
    {"_id": "sku-001"},
    {"$inc": {"stock": -3, "sold_count": 3}}
)
doc = inv.find_one({"_id": "sku-001"}, {"stock": 1, "sold_count": 1, "_id": 0})
print(f"  [$inc]      sku-001 stock={doc['stock']}, sold_count={doc['sold_count']}")

# ─────────────────────────────────────────────────────────────────────────────
# $mul — apply 10% discount across ALL products in a category
# ─────────────────────────────────────────────────────────────────────────────
inv.update_many(
    {"tags": "gaming"},
    {"$mul": {"price": 0.9}}  # multiply price by 0.9 → 10% off
)
doc = inv.find_one({"_id": "sku-002"}, {"price": 1, "_id": 0})
print(f"  [$mul]      sku-002 price after 10% discount: {doc['price']:.2f}")

# ─────────────────────────────────────────────────────────────────────────────
# $unset — remove a field (field disappears from the document entirely)
# ─────────────────────────────────────────────────────────────────────────────
inv.update_one({"_id": "sku-003"}, {"$set": {"temp_flag": True}})
inv.update_one({"_id": "sku-003"}, {"$unset": {"temp_flag": ""}})
doc = inv.find_one({"_id": "sku-003"})
print(f"  [$unset]    sku-003 'temp_flag' present: {'temp_flag' in doc}")

# ─────────────────────────────────────────────────────────────────────────────
# $max — update only if new value is greater (watermark pattern)
# Useful for tracking high-water-marks: highest stock seen, max score, etc.
# ─────────────────────────────────────────────────────────────────────────────
inv.update_one({"_id": "sku-001"}, {"$max": {"peak_stock": 30}})
inv.update_one({"_id": "sku-001"}, {"$max": {"peak_stock": 15}})  # no-op: 15 < 30
doc = inv.find_one({"_id": "sku-001"}, {"peak_stock": 1, "_id": 0})
print(f"  [$max]      sku-001 peak_stock: {doc['peak_stock']}  (set to 30, then tried 15)")

# ─────────────────────────────────────────────────────────────────────────────
# $push — append to array
# ─────────────────────────────────────────────────────────────────────────────
inv.update_one({"_id": "sku-001"}, {"$push": {"tags": "sale"}})
doc = inv.find_one({"_id": "sku-001"}, {"tags": 1, "_id": 0})
print(f"  [$push]     sku-001 tags: {doc['tags']}")

# ─────────────────────────────────────────────────────────────────────────────
# $addToSet — idempotent append (no duplicates)
# Push "wireless" which sku-001 already has → no-op.
# Push "ergonomic" which it does not → appended.
# ─────────────────────────────────────────────────────────────────────────────
inv.update_one({"_id": "sku-001"}, {"$addToSet": {"tags": "wireless"}})    # already there
inv.update_one({"_id": "sku-001"}, {"$addToSet": {"tags": "ergonomic"}})   # new
doc = inv.find_one({"_id": "sku-001"}, {"tags": 1, "_id": 0})
print(f"  [$addToSet] sku-001 tags: {doc['tags']}  (no duplicate 'wireless')")

# ─────────────────────────────────────────────────────────────────────────────
# $pull — remove matching elements from array
# ─────────────────────────────────────────────────────────────────────────────
inv.update_one({"_id": "sku-001"}, {"$pull": {"tags": "sale"}})
doc = inv.find_one({"_id": "sku-001"}, {"tags": 1, "_id": 0})
print(f"  [$pull]     sku-001 tags after removing 'sale': {doc['tags']}")

# ─────────────────────────────────────────────────────────────────────────────
# $push + $slice — sliding window: keep only the last 3 prices in history
# ─────────────────────────────────────────────────────────────────────────────
for new_price in [99.0, 89.0, 79.0]:
    inv.update_one(
        {"_id": "sku-001"},
        {"$push": {"price_history": {"$each": [new_price], "$slice": -3}}}
    )
doc = inv.find_one({"_id": "sku-001"}, {"price_history": 1, "_id": 0})
print(f"  [$slice]    sku-001 price_history (last 3): {doc['price_history']}")

# ─────────────────────────────────────────────────────────────────────────────
# upsert — insert if not found, update if found
# setOnInsert only runs when a new doc is created (upsert insert path).
# ─────────────────────────────────────────────────────────────────────────────
doc = inv.find_one_and_update(
    {"_id": "sku-999"},
    {
        "$set":        {"name": "New Gadget", "stock": 10},
        "$setOnInsert": {"created_at": datetime.now(tz=timezone.utc)},
    },
    upsert=True,
    return_document=ReturnDocument.AFTER,
)
print(f"  [upsert]    sku-999 created: {doc}")
print()
