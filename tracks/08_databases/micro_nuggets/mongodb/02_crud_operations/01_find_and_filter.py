"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 02-01 · Find & Filter                                                ║
║  The MongoDB query language — comparison, logical, element, and regex ops.   ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Master the MongoDB Query Language (MQL) filter operators.
Every read and update operation uses filters — this is the foundation.

CONCEPTS
────────
MQL Filter Syntax:
  {"field": value}            → equality match (implicit $eq)
  {"field": {"$op": value}}   → comparison operator

Comparison operators:
  $eq   → equal             {"age": {"$eq": 30}}  or  {"age": 30}
  $ne   → not equal         {"status": {"$ne": "inactive"}}
  $gt   → greater than      {"price": {"$gt": 100}}
  $gte  → ≥                 {"stock": {"$gte": 1}}
  $lt   → less than
  $lte  → ≤
  $in   → in list           {"category": {"$in": ["audio", "computers"]}}
  $nin  → not in list

Logical operators:
  $and  → all conditions    {"$and": [{"a": 1}, {"b": 2}]}
           (implicit when you list multiple fields in one filter)
  $or   → any condition     {"$or": [{"cat": "audio"}, {"cat": "gaming"}]}
  $nor  → none match
  $not  → negates one op    {"price": {"$not": {"$gt": 500}}}

Element operators:
  $exists → field exists    {"warranty": {"$exists": True}}
  $type   → BSON type       {"_id": {"$type": "string"}}

Array operators:
  $all        → array contains all listed values
  $elemMatch  → at least one element matches a sub-filter
  $size       → array has exactly N elements

String / Regex:
  {"name": {"$regex": "sony", "$options": "i"}}  → case-insensitive regex

Projection (second arg to find / find_one):
  {"field": 1}         → include (all others excluded, except _id)
  {"field": 0}         → exclude (all others included)
  {"_id": 0, "name": 1} → include name, exclude _id
  Cannot mix include/exclude (except _id)

Cursor methods (chainable):
  .sort(key, direction)   → direction: 1 = ASC, -1 = DESC
  .limit(n)               → max n results
  .skip(n)                → skip first n results (for pagination)
  .count_documents(filter) → efficient server-side count (no cursor needed)

USAGE
─────
    python 01_find_and_filter.py

EXPECTED OUTPUT
───────────────
    ── Find & Filter ─────────────────────────────────

      Loaded 10 product fixtures.

      [eq]    Products in 'audio' category: 3
      [in]    Products in audio or gaming: 5
      [gt]    Products priced > 200: 3
      [range] Products $50–$300: 5
      [and]   In-stock audio > $100: 2
      [or]    Audio or price < 30: 4
      [regex] Names containing 'pro' (case-insensitive): 2
      [exists] Products WITH a 'warranty_years' field: 3
      [array] Products tagged 'wireless': 3

      Top 3 most expensive (name + price):
        MacBook Pro 16  1999.00
        Sony WH-1000XM5  349.99
        Jabra Elite 85h  249.00

      Page 2 (skip 3, limit 3) sorted by price DESC:
        ...
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pymongo
from bson import Decimal128

sys.path.insert(0, str(Path(__file__).parent.parent))
from _mg_connect import get_lab_db

db = get_lab_db()
db.drop_collection("products_filter")
col = db["products_filter"]

# ─────────────────────────────────────────────────────────────────────────────
# Fixture data — 10 products across categories with varied attributes
# ─────────────────────────────────────────────────────────────────────────────
fixtures = [
    {"name": "Sony WH-1000XM5",    "category": "audio",     "price": 349.99, "stock": 42,  "in_stock": True,  "tags": ["wireless", "noise-cancelling"], "warranty_years": 2},
    {"name": "Jabra Elite 85h",     "category": "audio",     "price": 249.00, "stock": 15,  "in_stock": True,  "tags": ["wireless", "bluetooth"],         "warranty_years": 2},
    {"name": "Sennheiser HD 400S",  "category": "audio",     "price": 79.95,  "stock": 30,  "in_stock": True,  "tags": ["wired", "over-ear"]},
    {"name": "MacBook Pro 16",      "category": "computers", "price": 1999.00,"stock": 4,   "in_stock": True,  "tags": ["apple", "m3"],                   "warranty_years": 1},
    {"name": "Logitech MX Master",  "category": "peripherals","price": 99.99, "stock": 100, "in_stock": True,  "tags": ["wireless", "ergonomic"]},
    {"name": "Razer DeathAdder",    "category": "gaming",    "price": 69.99,  "stock": 55,  "in_stock": True,  "tags": ["wired", "gaming"]},
    {"name": "SteelSeries Arctis",  "category": "gaming",    "price": 179.99, "stock": 20,  "in_stock": True,  "tags": ["wireless", "gaming", "headset"]},
    {"name": "Anker USB-C Hub",     "category": "accessories","price": 29.99, "stock": 200, "in_stock": True,  "tags": ["usb-c", "hub"]},
    {"name": "Keychron K2 Pro",     "category": "peripherals","price": 109.00,"stock": 0,   "in_stock": False, "tags": ["mechanical", "wireless"],        "warranty_years": 1},
    {"name": "Elgato Stream Deck",  "category": "streaming", "price": 149.99, "stock": 35,  "in_stock": True,  "tags": ["streaming", "macro"]},
]
col.insert_many(fixtures)
print(f"\n── Find & Filter ─────────────────────────────────")
print(f"\n  Loaded {col.count_documents({})} product fixtures.")

# ─────────────────────────────────────────────────────────────────────────────
# Equality — implicit $eq
# ─────────────────────────────────────────────────────────────────────────────
n = col.count_documents({"category": "audio"})
print(f"\n  [eq]    Products in 'audio' category: {n}")

# ─────────────────────────────────────────────────────────────────────────────
# $in — match any value in a list
# ─────────────────────────────────────────────────────────────────────────────
n = col.count_documents({"category": {"$in": ["audio", "gaming"]}})
print(f"  [in]    Products in audio or gaming: {n}")

# ─────────────────────────────────────────────────────────────────────────────
# $gt — comparison
# Note: comparing float prices stored as Python float (not Decimal128 here)
# ─────────────────────────────────────────────────────────────────────────────
n = col.count_documents({"price": {"$gt": 200}})
print(f"  [gt]    Products priced > 200: {n}")

n = col.count_documents({"price": {"$gte": 50, "$lte": 300}})
print(f"  [range] Products $50–$300: {n}")

# ─────────────────────────────────────────────────────────────────────────────
# $and — implicit AND (multiple keys in one dict)
# Both conditions must match the SAME document.
# ─────────────────────────────────────────────────────────────────────────────
n = col.count_documents({"category": "audio", "in_stock": True, "price": {"$gt": 100}})
print(f"  [and]   In-stock audio > $100: {n}")

# ─────────────────────────────────────────────────────────────────────────────
# $or — at least one condition matches
# ─────────────────────────────────────────────────────────────────────────────
n = col.count_documents({"$or": [{"category": "audio"}, {"price": {"$lt": 30}}]})
print(f"  [or]    Audio or price < 30: {n}")

# ─────────────────────────────────────────────────────────────────────────────
# $regex — case-insensitive substring match
# $options: "i" = case-insensitive, "m" = multiline, "s" = dot-all
# ─────────────────────────────────────────────────────────────────────────────
n = col.count_documents({"name": {"$regex": "pro", "$options": "i"}})
print(f"  [regex] Names containing 'pro' (case-insensitive): {n}")

# ─────────────────────────────────────────────────────────────────────────────
# $exists — field present or absent
# ─────────────────────────────────────────────────────────────────────────────
n = col.count_documents({"warranty_years": {"$exists": True}})
print(f"  [exists] Products WITH a 'warranty_years' field: {n}")

# ─────────────────────────────────────────────────────────────────────────────
# Array query — find documents where 'tags' array contains a value
# MongoDB automatically queries inside arrays for equality.
# ─────────────────────────────────────────────────────────────────────────────
n = col.count_documents({"tags": "wireless"})
print(f"  [array] Products tagged 'wireless': {n}")

# ─────────────────────────────────────────────────────────────────────────────
# Projection + sort + limit
# {"name": 1, "price": 1, "_id": 0} → return only name and price, no _id
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n  Top 3 most expensive (name + price):")
for doc in col.find({}, {"name": 1, "price": 1, "_id": 0}).sort("price", pymongo.DESCENDING).limit(3):
    print(f"    {doc['name']:<30} {doc['price']:.2f}")

# ─────────────────────────────────────────────────────────────────────────────
# Pagination — skip + limit
# WARNING: skip() is O(n) — it scans and discards n documents.
# For large collections, use range-based pagination instead:
#   find({"_id": {"$gt": last_seen_id}}).limit(page_size)
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n  Page 2 (skip 3, limit 3) sorted by price DESC:")
cursor = (col.find({}, {"name": 1, "price": 1, "_id": 0})
            .sort("price", pymongo.DESCENDING)
            .skip(3)
            .limit(3))
for doc in cursor:
    print(f"    {doc['name']:<30} {doc['price']:.2f}")

print()
