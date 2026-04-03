"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 04-02 · $lookup & $unwind — MongoDB Joins                            ║
║  Joining collections in a document database (with tradeoffs).                ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Perform LEFT OUTER JOINs across collections using $lookup, and flatten
embedded arrays with $unwind to enable group-by on array elements.

CONCEPTS
────────
$lookup (basic form — equality join):
  {
    "$lookup": {
      "from":         "other_collection",    # collection to join
      "localField":   "local_field",         # field in current docs
      "foreignField": "foreign_field",       # field in 'from' collection
      "as":           "result_array_name",   # output array field name
    }
  }
  - Equivalent to LEFT OUTER JOIN: documents with no match get an empty array.
  - The result is embedded as an ARRAY (even if the join is 1-to-1).
  - Always add $unwind after $lookup on 1-to-1 joins to flatten the array.

$lookup (pipeline form — more powerful, MongoDB 3.6+):
  {
    "$lookup": {
      "from":     "other_collection",
      "let":      {"local_var": "$local_field"},   # variables from current doc
      "pipeline": [
          {"$match": {"$expr": {"$eq": ["$$local_var", "$foreign_field"]}}},
          {"$project": {"only_needed_fields": 1}},  # project here = less network
      ],
      "as": "result_array_name",
    }
  }
  - More flexible: can join on computed expressions, ranges, multiple fields.
  - Can include an inner $project to limit which fields are joined.
  - $expr allows using aggregation expressions inside $match.

$unwind:
  {
    "$unwind": {
      "path":                    "$array_field",
      "preserveNullAndEmptyArrays": True,  # keep docs with null/empty array
      "includeArrayIndex":       "idx",  # add a field with the element index
    }
  }
  - Short form: {"$unwind": "$array_field"} — drops docs with null/empty array.
  - Turns one doc with N array elements into N separate documents.
  - Use case: group by per-tag, per-item analysis of embedded arrays.

When NOT to use $lookup:
  - MongoDB is optimized for the document model — embed what you query together.
  - $lookup across large collections is expensive (no hash joins before 5.2,
    uses nested-loop join). Keep related data embedded when possible.
  - Use $lookup for: occasional analytics, reporting, low-frequency joins.
  - For high-frequency joins, denormalize (embed) the data instead.

USAGE
─────
    python 02_lookup_and_unwind.py
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _mg_connect import get_lab_db

db = get_lab_db()
db.drop_collection("customers")
db.drop_collection("orders_lu")
db.drop_collection("line_items")

print("\n── $lookup & $unwind ─────────────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# Seed: customers and their orders (separate collections — normalized model)
# ─────────────────────────────────────────────────────────────────────────────
customers = db["customers"]
orders_col = db["orders_lu"]
items_col  = db["line_items"]
now = datetime.now(tz=timezone.utc)

customers.insert_many([
    {"_id": "C001", "name": "Alice Chen",  "tier": "gold",   "region": "West"},
    {"_id": "C002", "name": "Bob Smith",   "tier": "silver", "region": "East"},
    {"_id": "C003", "name": "Carol Diaz",  "tier": "gold",   "region": "West"},
    {"_id": "C004", "name": "Dave Lee",    "tier": "bronze", "region": "North"},
    # C005 has no orders — for LEFT JOIN demo
    {"_id": "C005", "name": "Eve Torres",  "tier": "silver", "region": "South"},
])

orders_col.insert_many([
    {"_id": "O001", "customer_id": "C001", "total": 349.99, "status": "delivered", "date": now},
    {"_id": "O002", "customer_id": "C001", "total": 99.00,  "status": "delivered", "date": now},
    {"_id": "O003", "customer_id": "C002", "total": 249.00, "status": "shipped",   "date": now},
    {"_id": "O004", "customer_id": "C003", "total": 1999.0, "status": "delivered", "date": now},
    {"_id": "O005", "customer_id": "C003", "total": 45.00,  "status": "pending",   "date": now},
    {"_id": "O006", "customer_id": "C004", "total": 29.99,  "status": "delivered", "date": now},
])

# Line items — one per product per order (embedded array alternative)
items_col.insert_many([
    {"order_id": "O001", "product": "Sony WH-1000XM5", "qty": 1, "price": 349.99},
    {"order_id": "O002", "product": "Logitech MX Master","qty": 1, "price": 99.00},
    {"order_id": "O003", "product": "Jabra Elite 85h",  "qty": 1, "price": 249.00},
    {"order_id": "O004", "product": "MacBook Pro 16",   "qty": 1, "price": 1999.00},
    {"order_id": "O005", "product": "Anker USB-C Hub",  "qty": 1, "price": 45.00},
    {"order_id": "O006", "product": "Anker USB-C Hub",  "qty": 1, "price": 29.99},
])

# ─────────────────────────────────────────────────────────────────────────────
# 1. Basic $lookup — LEFT JOIN customers ← orders
#    For each customer, embed their orders as an array.
# ─────────────────────────────────────────────────────────────────────────────
pipeline = [
    {"$lookup": {
        "from":         "orders_lu",
        "localField":   "_id",
        "foreignField": "customer_id",
        "as":           "orders",
    }},
    {"$project": {
        "_id":       1,
        "name":      1,
        "tier":      1,
        "order_count": {"$size": "$orders"},
        "total_spent": {"$sum": "$orders.total"},
    }},
    {"$sort": {"total_spent": -1}},
]
results = list(customers.aggregate(pipeline))
print(f"\n  Customer order summary (LEFT JOIN — all customers):")
print(f"    {'Name':<15} {'Tier':<8} {'Orders':>7} {'Total Spent':>12}")
print(f"    {'-'*15} {'-'*8} {'-'*7} {'-'*12}")
for r in results:
    print(f"    {r['name']:<15} {r['tier']:<8} {r['order_count']:>7} ${r['total_spent']:>11.2f}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. $lookup pipeline form — join orders with line items, project only needed fields
# ─────────────────────────────────────────────────────────────────────────────
pipeline = [
    {"$match": {"customer_id": {"$in": ["C001", "C003"]}}},
    {"$lookup": {
        "from": "line_items",
        "let":  {"oid": "$_id"},
        "pipeline": [
            {"$match": {"$expr": {"$eq": ["$$oid", "$order_id"]}}},
            {"$project": {"_id": 0, "product": 1, "qty": 1, "price": 1}},
        ],
        "as": "items",
    }},
    {"$project": {"_id": 1, "customer_id": 1, "total": 1, "status": 1, "items": 1}},
]
results = list(orders_col.aggregate(pipeline))
print(f"\n  Orders with line items (C001 + C003):")
for r in results:
    print(f"    Order {r['_id']} (${r['total']:.2f}, {r['status']}):")
    for item in r.get("items", []):
        print(f"      - {item['product']}  qty={item['qty']}  ${item['price']:.2f}")

# ─────────────────────────────────────────────────────────────────────────────
# 3. $unwind — flatten an embedded array to group by element
#    Seed a product collection where each doc has an embedded "reviews" array.
#    $unwind lets us group by individual review scores.
# ─────────────────────────────────────────────────────────────────────────────
db.drop_collection("products_rev")
prods = db["products_rev"]
prods.insert_many([
    {"name": "Headphones", "reviews": [
        {"user": "u1", "score": 5}, {"user": "u2", "score": 4}, {"user": "u3", "score": 3}
    ]},
    {"name": "Keyboard",   "reviews": [
        {"user": "u1", "score": 4}, {"user": "u4", "score": 5}
    ]},
    {"name": "Mouse",      "reviews": [
        {"user": "u2", "score": 2}, {"user": "u3", "score": 3}, {"user": "u5", "score": 4}
    ]},
    {"name": "Webcam",     "reviews": []},  # no reviews — preserveNullAndEmpty demo
])

pipeline = [
    {"$unwind": {
        "path": "$reviews",
        "preserveNullAndEmptyArrays": True,  # keep Webcam (empty reviews array)
    }},
    {"$group": {
        "_id":        "$name",
        "review_count": {"$sum": {"$cond": [{"$ifNull": ["$reviews", False]}, 1, 0]}},
        "avg_score":  {"$avg": "$reviews.score"},
    }},
    {"$sort": {"avg_score": -1}},
]
results = list(prods.aggregate(pipeline))
print(f"\n  Product review averages (after $unwind):")
for r in results:
    avg = f"{r['avg_score']:.2f}" if r["avg_score"] is not None else "N/A"
    print(f"    {r['_id']:<15} reviews={r['review_count']}  avg_score={avg}")

# cleanup
db.drop_collection("products_rev")
print()
