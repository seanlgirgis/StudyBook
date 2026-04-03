"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 05-01 · Data Modeling — Embedding vs Referencing                     ║
║  The most important architectural decision in MongoDB design.                ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Compare embedding (denormalized) vs referencing (normalized) patterns,
understand when each is appropriate, and implement advanced patterns
like the Subset Pattern and the Bucket Pattern.

CONCEPTS
────────
Embedding (denormalized):
  - Store related data INSIDE the parent document as subdocuments or arrays.
  - Reads are single-document operations — no joins needed.
  - Write amplification: updating embedded data requires updating the parent.
  - Document size limit: 16 MB per document.
  - Use when:
      • "One-to-Few" (order + 3-5 line items): embed.
      • Data is always read together.
      • The embedded list is bounded in size.
      • Strong ownership (the child has no independent existence).

Referencing (normalized):
  - Store only the related document's _id; issue a $lookup or separate query.
  - Flexible — either side can query independently.
  - Write-once — updating a referenced doc is a single write, not N writes.
  - Use when:
      • "One-to-Many" / "One-to-Squillions" (user → millions of events).
      • The child has its own lifecycle independent of the parent.
      • Embedded array would grow unboundedly.
      • Multiple parents reference the same child (M-to-N).

The Subset Pattern:
  - Embed only the MOST RECENT / MOST RELEVANT N items from a large list.
  - Keep the full list in a separate collection.
  - Example: embed the 5 most recent reviews in the product doc.
             Query the "reviews" collection for the full list.
  - Balances read performance (hot data in one doc) with storage efficiency.

The Bucket Pattern:
  - Groups time-series data (e.g., IoT readings) into "bucket" documents.
  - Instead of one document per reading, store N readings per document.
  - Reduces document count from millions to thousands.
  - Enables efficient range queries with a single index scan.
  - Pattern: {sensor_id, hour, readings: [{ts, value}, ...], count, avg}

Polymorphic Pattern:
  - Multiple types of documents with different shapes in the same collection.
  - Add a "type" discriminator field.
  - All shapes share a common query field (e.g., "event_time").
  - Use when objects share some attributes but vary in others.

USAGE
─────
    python 01_embedding_pattern.py
"""
from __future__ import annotations

import sys
import random
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _mg_connect import get_lab_db

db = get_lab_db()
print("\n── Data Modeling Patterns ────────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Embedding pattern — order with line items (One-to-Few)
#    An order has 1–5 items. Items are always queried with the order.
#    Embedding makes one-document reads trivially fast.
# ─────────────────────────────────────────────────────────────────────────────
db.drop_collection("orders_embedded")
orders_emb = db["orders_embedded"]

orders_emb.insert_one({
    "_id":         "ORD-001",
    "customer_id": "C001",
    "status":      "shipped",
    "created_at":  datetime.now(tz=timezone.utc),
    # Line items EMBEDDED — no join needed to show an order receipt
    "line_items": [
        {"sku": "WH-1000XM5", "name": "Sony Headphones", "qty": 1, "price": 349.99},
        {"sku": "ANKER-HUB",  "name": "Anker USB-C Hub",  "qty": 2, "price": 29.99},
    ],
    "total": 409.97,
    "shipping": {
        "carrier": "FedEx",
        "tracking": "FX123456789",
        "estimated_delivery": datetime.now(tz=timezone.utc) + timedelta(days=3),
    },
})

order = orders_emb.find_one({"_id": "ORD-001"})
print(f"\n  [Embedding] Order ORD-001 fetched in ONE query:")
print(f"    Customer: {order['customer_id']}  Total: ${order['total']:.2f}")
print(f"    Items: {len(order['line_items'])} embedded line items")
for item in order["line_items"]:
    print(f"      - {item['name']}  x{item['qty']}  @${item['price']:.2f}")

# Update an embedded field — requires knowing the array index or using $
orders_emb.update_one(
    {"_id": "ORD-001", "line_items.sku": "WH-1000XM5"},
    {"$set": {"line_items.$.price": 329.99}},   # $ = positional operator
)
updated = orders_emb.find_one({"_id": "ORD-001"}, {"line_items": 1, "_id": 0})
print(f"    Price updated via positional $: {updated['line_items'][0]['price']}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Referencing pattern — user → events (One-to-Squillions)
#    A user can generate millions of events. Embedding would blow the 16 MB limit.
#    Events reference the user_id — the user document stays small.
# ─────────────────────────────────────────────────────────────────────────────
db.drop_collection("users_ref")
db.drop_collection("events_ref")
users_ref  = db["users_ref"]
events_ref = db["events_ref"]

users_ref.insert_one({
    "_id":      "U001",
    "name":     "Alice",
    "email":    "alice@example.com",
    "created":  datetime.now(tz=timezone.utc),
})

# 1,000 events would blow up the doc. References keep user doc tiny.
events_ref.insert_many([
    {"user_id": "U001", "type": "page_view", "url": f"/product/{i}",
     "ts": datetime.now(tz=timezone.utc) - timedelta(minutes=i)}
    for i in range(20)
])

user     = users_ref.find_one({"_id": "U001"})
ev_count = events_ref.count_documents({"user_id": "U001"})
print(f"\n  [Referencing] User doc size stays small:")
print(f"    User fields: {list(user.keys())}  (no events embedded)")
print(f"    Events for U001 in events collection: {ev_count}")

# ─────────────────────────────────────────────────────────────────────────────
# 3. Subset Pattern — embed only the 3 most recent reviews
#    Full reviews stay in a separate collection.
# ─────────────────────────────────────────────────────────────────────────────
db.drop_collection("products_sub")
db.drop_collection("reviews_full")
products_sub = db["products_sub"]
reviews_full = db["reviews_full"]

random.seed(1)
all_reviews = [
    {"product_id": "P001", "user": f"user_{i}", "score": random.randint(1,5),
     "body": f"Review {i}: great product" if i % 3 != 0 else "Could be better.",
     "ts": datetime.now(tz=timezone.utc) - timedelta(days=i)}
    for i in range(50)
]
reviews_full.insert_many(all_reviews)

# Embed only the 3 most recent in the product doc
recent_3 = sorted(all_reviews, key=lambda r: r["ts"], reverse=True)[:3]
products_sub.insert_one({
    "_id":         "P001",
    "name":        "Sony WH-1000XM5",
    "avg_score":   round(sum(r["score"] for r in all_reviews) / len(all_reviews), 2),
    "review_count": len(all_reviews),
    # Subset: only last 3 reviews embedded for fast product page render
    "recent_reviews": [{"user": r["user"], "score": r["score"], "body": r["body"][:40]}
                       for r in recent_3],
})
doc = products_sub.find_one({"_id": "P001"})
print(f"\n  [Subset] Product P001:")
print(f"    avg_score={doc['avg_score']}  total_reviews={doc['review_count']}")
print(f"    Embedded recent reviews: {len(doc['recent_reviews'])}")
print(f"    Full reviews in separate collection: {reviews_full.count_documents({'product_id': 'P001'})}")

# ─────────────────────────────────────────────────────────────────────────────
# 4. Bucket Pattern — IoT sensor readings grouped by hour
#    Instead of 1 doc per reading, store N readings per bucket doc.
#    Reduces index size, enables efficient range reads.
# ─────────────────────────────────────────────────────────────────────────────
db.drop_collection("sensor_buckets")
buckets = db["sensor_buckets"]
base = datetime.now(tz=timezone.utc).replace(minute=0, second=0, microsecond=0)

for hour_offset in range(3):
    hour_start = base - timedelta(hours=hour_offset)
    readings   = [round(20.0 + random.gauss(0, 2), 2) for _ in range(60)]  # 60 per hour
    buckets.insert_one({
        "sensor_id":  "SENSOR-A",
        "hour":       hour_start,
        "readings":   readings,
        "count":      len(readings),
        "avg":        round(sum(readings) / len(readings), 2),
        "min":        min(readings),
        "max":        max(readings),
    })

doc = buckets.find_one({"sensor_id": "SENSOR-A"}, {"_id": 0, "hour": 0})
print(f"\n  [Bucket] IoT bucket: {buckets.count_documents({})} documents cover 3 hours")
print(f"    Each bucket: count={doc['count']} readings, avg={doc['avg']}°C, "
      f"min={doc['min']}°C, max={doc['max']}°C")

# cleanup
for c in ["orders_embedded", "users_ref", "events_ref",
          "products_sub", "reviews_full", "sensor_buckets"]:
    db.drop_collection(c)
print()
