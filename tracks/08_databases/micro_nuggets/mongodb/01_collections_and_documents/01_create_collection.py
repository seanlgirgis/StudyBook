"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 01-01 · Collections & Documents                                      ║
║  The MongoDB equivalent of CREATE TABLE + INSERT — but schema-free.          ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Create a collection, insert single documents, and explore the BSON type system.
Understand how MongoDB's document model differs from relational tables.

CONCEPTS
────────
Document Model:
  - A MongoDB "document" is a BSON object — conceptually a JSON object on disk.
  - Each document lives in a "collection" (analogous to a table), but documents
    in the same collection do NOT need the same shape. This is called a
    "flexible schema" or "schema-less" design (though schema validation is
    available and recommended for production).
  - The document model enables "embedding" — storing related data together
    inside one document rather than across multiple joined tables.

_id field:
  - Every document MUST have a unique "_id" field.
  - If you omit it, pymongo automatically generates an ObjectId.
  - ObjectId is a 12-byte BSON value:
      4 bytes  → Unix timestamp (seconds)  ← creation time embedded!
      5 bytes  → random machine+process identifier
      3 bytes  → incrementing counter
  - ObjectId("...").generation_time returns a UTC datetime — built-in audit.
  - You can supply your own _id (string, int, UUID, etc.) but it must be unique.

BSON Types (a superset of JSON):
  - String       → str
  - Int32/Int64  → int  (pymongo auto-picks based on magnitude)
  - Double       → float
  - Boolean      → bool
  - Date         → datetime.datetime  (always UTC in MongoDB!)
  - ObjectId     → bson.ObjectId
  - Array        → list
  - Document     → dict
  - Null         → None
  - Decimal128   → bson.Decimal128    (exact decimal, for financial data)
  - Binary       → bytes / bson.Binary
  - Regex        → bson.Regex

insert_one() vs insert_many():
  - insert_one(doc)       → inserts one document, returns InsertOneResult.
  - insert_many(docs)     → inserts a list, returns InsertManyResult.
  - result.inserted_id    → the _id of the inserted document.
  - result.inserted_ids   → list of _ids (insert_many).
  - Both operations are atomic at the document level.

find_one() vs find():
  - find_one(filter)      → returns the first matching document (or None).
  - find(filter)          → returns a Cursor (lazy iterator).
  - Always pass a filter — find_one({}) scans every document.
  - Projection: second argument limits which fields are returned.
    {"field": 1} → include; {"field": 0} → exclude. Mix is not allowed
    (except for _id which can always be excluded: {"_id": 0, "field": 1}).

USAGE
─────
    python 01_create_collection.py

EXPECTED OUTPUT
───────────────
    ── Collections & Documents ──────────────────────

      Dropped old products collection (clean start).

      Inserted product _id: 507f1f77bcf86cd799439011  (ObjectId)
      Created at: 2026-04-03 xx:xx:xx UTC

      Inserted product with custom _id: laptop-001

      Found by ObjectId:    {'_id': ObjectId('...'), 'sku': 'WH-1000XM5', ...}
      Found by custom _id:  {'_id': 'laptop-001', 'name': 'MacBook Pro 14', ...}

      BSON types in the headphones document:
        _id         → ObjectId  (bson.objectid.ObjectId)
        sku         → str       (builtins.str)
        name        → str
        price       → Decimal128 (bson.decimal128.Decimal128)
        stock       → int       (builtins.int)
        in_stock    → bool      (builtins.bool)
        tags        → list      (builtins.list)
        specs       → dict      (builtins.dict)
        created_at  → datetime  (datetime.datetime)

      Collection 'products' now has 2 documents.
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

from bson import Decimal128, ObjectId

sys.path.insert(0, str(Path(__file__).parent.parent))
from _mg_connect import get_lab_db

db = get_lab_db()

print("\n── Collections & Documents ──────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# Setup: drop and recreate for a clean demo
# drop_collection() is safe to call even if the collection doesn't exist.
# MongoDB creates the collection implicitly on the first insert.
# ─────────────────────────────────────────────────────────────────────────────
db.drop_collection("products")
print("\n  Dropped old products collection (clean start).")

products = db["products"]

# ─────────────────────────────────────────────────────────────────────────────
# insert_one — auto-generated ObjectId
#
# Decimal128 for price:
#   NEVER use float for money. float(35.99) → 35.990000000000000213 (IEEE 754).
#   bson.Decimal128("35.99") stores exactly 35.99 using 128-bit decimal math.
#   In Python, cast back with: float(doc["price"].to_decimal())
#
# datetime must be UTC-aware or naive-UTC:
#   MongoDB always stores dates as UTC milliseconds since epoch.
#   datetime.now(tz=timezone.utc) is the correct way to get a UTC timestamp.
#   datetime.now() (without tz) works too — pymongo treats naive datetimes as UTC.
# ─────────────────────────────────────────────────────────────────────────────
result = products.insert_one({
    "sku":        "WH-1000XM5",
    "name":       "Sony WH-1000XM5 Headphones",
    "category":   "audio",
    "price":      Decimal128("349.99"),
    "stock":      42,
    "in_stock":   True,
    "tags":       ["wireless", "noise-cancelling", "bluetooth"],
    "specs":      {"driver_size_mm": 30, "battery_hours": 30, "weight_g": 250},
    "created_at": datetime.now(tz=timezone.utc),
})

oid = result.inserted_id
print(f"\n  Inserted product _id: {oid}  (ObjectId)")
print(f"  Created at: {oid.generation_time.strftime('%Y-%m-%d %H:%M:%S')} UTC")

# ─────────────────────────────────────────────────────────────────────────────
# insert_one — custom _id
# Use custom _id when you have a natural unique key (SKU, user_id, etc.).
# Downside: you lose the creation-time embedded in ObjectId.
# ─────────────────────────────────────────────────────────────────────────────
products.insert_one({
    "_id":        "laptop-001",
    "name":       "MacBook Pro 14",
    "category":   "computers",
    "price":      Decimal128("1999.00"),
    "stock":      8,
    "in_stock":   True,
    "tags":       ["apple", "m3", "laptop"],
    "specs":      {"ram_gb": 16, "storage_gb": 512, "display_inch": 14.2},
    "created_at": datetime.now(tz=timezone.utc),
})
print("  Inserted product with custom _id: laptop-001")

# ─────────────────────────────────────────────────────────────────────────────
# find_one — query by ObjectId and by string _id
# Querying by ObjectId requires passing an actual ObjectId, not a string.
# ─────────────────────────────────────────────────────────────────────────────
headphones = products.find_one({"_id": oid})
laptop     = products.find_one({"_id": "laptop-001"})

print(f"\n  Found by ObjectId:    {headphones}")
print(f"  Found by custom _id:  {laptop}")

# ─────────────────────────────────────────────────────────────────────────────
# BSON type inspection — understand what Python types pymongo uses
# ─────────────────────────────────────────────────────────────────────────────
print("\n  BSON types in the headphones document:")
for field, value in headphones.items():
    type_name = type(value).__module__ + "." + type(value).__qualname__
    print(f"    {field:<14} → {type(value).__qualname__:<12} ({type_name})")

total = products.count_documents({})
print(f"\n  Collection 'products' now has {total} documents.")
print()
