"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 04-01 · Aggregation Pipeline — Basics                                ║
║  MongoDB's answer to GROUP BY, HAVING, subqueries — all in one pipeline.     ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Master the core aggregation pipeline stages: $match, $group, $project,
$sort, $limit, $skip, $count, $addFields. These cover 90% of analytics.

CONCEPTS
────────
Aggregation Pipeline:
  - A sequence of stages; each stage transforms the document stream.
  - Documents flow through stages like Unix pipes: stage1 | stage2 | stage3.
  - Executed server-side — only the final result is sent over the network.
  - Returns a Cursor (lazy); call list() or iterate to consume.

  collection.aggregate([stage1, stage2, ...])

Key stages:
  $match   → filter (like WHERE / HAVING). MUST be first when possible
             so MongoDB can use indexes. $match after $group filters groups.

  $group   → aggregate by a key. Always has "_id" (the group key).
             _id: null   → aggregate the entire collection (no grouping).
             _id: "$field" → group by that field.
             _id: {"a": "$a", "b": "$b"} → group by composite key.

             Accumulators:
               $sum, $avg, $min, $max  → numeric aggregation
               $count                  → count documents in group (4.4+)
               $push                   → collect values into an array
               $addToSet               → collect unique values
               $first, $last           → first/last value in the group

  $project → reshape documents. 1 = include, 0 = exclude.
             Computed fields: {"$project": {"full": {"$concat": ["$a", " ", "$b"]}}}
             Suppress _id: {"$project": {"_id": 0, "name": 1}}

  $addFields → add or overwrite fields without excluding others.
               Safer than $project when you don't want to list every field.

  $sort     → sort the stream. -1 = DESC, 1 = ASC.
              If $sort is the FIRST stage, it can use a collection index.
              After $group, it sorts the aggregated results.

  $limit    → keep only first N documents.
  $skip     → skip first N documents.
  $count    → output a single doc {"count": N} — replaces $group + $count.

  $unwind   → deconstruct an array field into one doc per element.
              Without $unwind, $group on an array field treats the whole array as the key.

  $out      → write the pipeline output to a collection (overwrites!).
  $merge    → upsert pipeline output into a collection (non-destructive).

Aggregation vs find():
  - find() is a filter + projection — it cannot group, join, or compute.
  - aggregate() is the full analytics engine.
  - For simple reads, prefer find() (lighter). For analytics, use aggregate().

USAGE
─────
    python 01_basic_pipeline.py
"""
from __future__ import annotations

import sys
import random
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _mg_connect import get_lab_db

db = get_lab_db()
db.drop_collection("sales_agg")
col = db["sales_agg"]

print("\n── Aggregation Pipeline — Basics ─────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# Seed 200 sales documents
# ─────────────────────────────────────────────────────────────────────────────
random.seed(99)
products   = ["Keyboard", "Mouse", "Monitor", "Headphones", "Webcam"]
regions    = ["North", "South", "East", "West"]
base       = datetime.now(tz=timezone.utc)
sales_docs = []
for i in range(200):
    qty = random.randint(1, 10)
    price = round(random.uniform(15.0, 500.0), 2)
    sales_docs.append({
        "product":    random.choice(products),
        "region":     random.choice(regions),
        "qty":        qty,
        "unit_price": price,
        "total":      round(qty * price, 2),
        "date":       base - timedelta(days=random.randint(0, 89)),
        "rep":        f"rep_{random.randint(1, 10):02d}",
    })
col.insert_many(sales_docs)
print(f"\n  Seeded {col.count_documents({})} sales documents.")

# ─────────────────────────────────────────────────────────────────────────────
# 1. $match + $group + $sort — revenue by product
#    Equivalent SQL:
#      SELECT product, COUNT(*) AS orders, SUM(total) AS revenue,
#             AVG(total) AS avg_order, MAX(total) AS max_order
#      FROM sales
#      WHERE total > 50
#      GROUP BY product
#      ORDER BY revenue DESC
# ─────────────────────────────────────────────────────────────────────────────
pipeline = [
    {"$match": {"total": {"$gt": 50}}},
    {"$group": {
        "_id":       "$product",
        "orders":    {"$sum": 1},
        "revenue":   {"$sum": "$total"},
        "avg_order": {"$avg": "$total"},
        "max_order": {"$max": "$total"},
    }},
    {"$sort": {"revenue": -1}},
]
results = list(col.aggregate(pipeline))
print(f"\n  Revenue by product (total > $50):")
print(f"    {'Product':<12} {'Orders':>7} {'Revenue':>10} {'Avg Order':>10} {'Max Order':>10}")
print(f"    {'-'*12} {'-'*7} {'-'*10} {'-'*10} {'-'*10}")
for r in results:
    print(f"    {r['_id']:<12} {r['orders']:>7} "
          f"${r['revenue']:>9.2f} ${r['avg_order']:>9.2f} ${r['max_order']:>9.2f}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Composite group key — region + product
# ─────────────────────────────────────────────────────────────────────────────
pipeline = [
    {"$group": {
        "_id":     {"region": "$region", "product": "$product"},
        "revenue": {"$sum": "$total"},
    }},
    {"$sort": {"revenue": -1}},
    {"$limit": 5},
    {"$project": {
        "_id":     0,
        "region":  "$_id.region",
        "product": "$_id.product",
        "revenue": {"$round": ["$revenue", 2]},
    }},
]
results = list(col.aggregate(pipeline))
print(f"\n  Top 5 region+product combos by revenue:")
for r in results:
    print(f"    {r['region']:<8} {r['product']:<12} ${r['revenue']:.2f}")

# ─────────────────────────────────────────────────────────────────────────────
# 3. $addFields — compute new derived fields without dropping others
#    Compute a "discount_price" = unit_price * 0.85 and "label"
# ─────────────────────────────────────────────────────────────────────────────
pipeline = [
    {"$match": {"product": "Monitor"}},
    {"$addFields": {
        "discount_price": {"$round": [{"$multiply": ["$unit_price", 0.85]}, 2]},
        "label": {"$concat": ["$product", " — ", "$region"]},
    }},
    {"$project": {"_id": 0, "label": 1, "unit_price": 1, "discount_price": 1, "total": 1}},
    {"$sort": {"total": -1}},
    {"$limit": 3},
]
results = list(col.aggregate(pipeline))
print(f"\n  Monitor discounts (15% off):")
for r in results:
    print(f"    {r['label']:<30} list=${r['unit_price']:.2f}  sale=${r['discount_price']:.2f}")

# ─────────────────────────────────────────────────────────────────────────────
# 4. Grand total with _id: null (aggregate the whole collection)
# ─────────────────────────────────────────────────────────────────────────────
pipeline = [
    {"$group": {
        "_id":          None,
        "total_revenue": {"$sum": "$total"},
        "total_orders":  {"$sum": 1},
        "avg_order":     {"$avg": "$total"},
    }},
    {"$project": {
        "_id":           0,
        "total_revenue": {"$round": ["$total_revenue", 2]},
        "total_orders":  1,
        "avg_order":     {"$round": ["$avg_order", 2]},
    }},
]
summary = list(col.aggregate(pipeline))[0]
print(f"\n  Grand totals: orders={summary['total_orders']}, "
      f"revenue=${summary['total_revenue']}, avg=${summary['avg_order']}")

# ─────────────────────────────────────────────────────────────────────────────
# 5. $count — count documents matching a filter (one-liner alternative to $group)
# ─────────────────────────────────────────────────────────────────────────────
pipeline = [
    {"$match": {"region": "North", "total": {"$gt": 100}}},
    {"$count": "north_high_value_orders"},
]
result = list(col.aggregate(pipeline))
count = result[0]["north_high_value_orders"] if result else 0
print(f"  North region, orders > $100: {count}")
print()
