"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 04-03 · Advanced Aggregation — $facet, $bucket, $merge               ║
║  Multi-dimensional analytics and materialized view patterns.                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Master advanced aggregation patterns used in real analytics pipelines:
  - $facet  → run multiple sub-pipelines in ONE pass (like pivot tables)
  - $bucket → histogram buckets with custom ranges
  - $merge  → write aggregation output back to a collection (materialized views)
  - $setWindowFields → running totals, moving averages, rank

CONCEPTS
────────
$facet:
  - Runs multiple aggregation sub-pipelines simultaneously on the SAME input.
  - Each sub-pipeline is independent and produces its own result array.
  - Output: one document with one field per facet.
  - Use case: building "faceted search" results (filters + counts) in one query.
  - Equivalent to multiple GROUP BY queries but in a single round-trip.

$bucket:
  - Groups documents into predefined numeric ranges (bins/histogram).
  - "boundaries" defines the bin edges (must be monotonically increasing).
  - "default" catches values below the first boundary or above the last.
  - $bucketAuto → lets MongoDB decide the bin boundaries automatically.

$merge (MongoDB 4.2+):
  - Writes pipeline results into a target collection.
  - More powerful than $out (which fully overwrites).
  - whenMatched: "merge"    → update matched documents (like SQL MERGE).
  - whenMatched: "replace"  → replace matched document entirely.
  - whenNotMatched: "insert" → insert new document.
  - whenNotMatched: "discard" → skip new documents.
  - USE CASE: incremental materialized view refresh. Run nightly to update
    a pre-aggregated summary collection — queries read the summary (fast),
    not the raw collection (slow).

$setWindowFields (MongoDB 5.0+):
  - SQL window functions — running totals, lag/lead, rank, dense_rank.
  - "partitionBy" → like PARTITION BY in SQL.
  - "sortBy"      → defines the ordering within the window.
  - "output"      → computed fields using window functions:
      $sum        → running total
      $avg        → moving average
      $rank / $denseRank → rank within partition
      $shift      → access previous/next document value (lag/lead)

USAGE
─────
    python 03_advanced_pipeline.py
"""
from __future__ import annotations

import sys
import random
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _mg_connect import get_lab_db

db = get_lab_db()
db.drop_collection("transactions")
db.drop_collection("daily_summary")

print("\n── Advanced Aggregation ──────────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# Seed 300 transactions across categories, regions, and 90-day range
# ─────────────────────────────────────────────────────────────────────────────
random.seed(55)
categories = ["Electronics", "Clothing", "Books", "Sports", "Home"]
regions    = ["North", "South", "East", "West"]
base = datetime.now(tz=timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

txns = []
for _ in range(300):
    amount = round(random.uniform(5.0, 1200.0), 2)
    txns.append({
        "category": random.choice(categories),
        "region":   random.choice(regions),
        "amount":   amount,
        "qty":      random.randint(1, 5),
        "date":     base - timedelta(days=random.randint(0, 89)),
    })
col = db["transactions"]
col.insert_many(txns)
print(f"\n  Seeded {col.count_documents({})} transactions.")

# ─────────────────────────────────────────────────────────────────────────────
# 1. $facet — multi-dimensional analytics in one query
#    Sub-pipeline A: revenue by category
#    Sub-pipeline B: price distribution histogram
#    Sub-pipeline C: region breakdown
# ─────────────────────────────────────────────────────────────────────────────
pipeline = [{"$facet": {
    "by_category": [
        {"$group": {"_id": "$category", "revenue": {"$sum": "$amount"}, "count": {"$sum": 1}}},
        {"$sort": {"revenue": -1}},
    ],
    "price_histogram": [
        {"$bucket": {
            "groupBy": "$amount",
            "boundaries": [0, 50, 150, 300, 600, 1300],
            "default": "out_of_range",
            "output": {"count": {"$sum": 1}, "total": {"$sum": "$amount"}},
        }},
    ],
    "by_region": [
        {"$group": {"_id": "$region", "revenue": {"$sum": "$amount"}}},
        {"$sort": {"revenue": -1}},
    ],
}}]
facets = list(col.aggregate(pipeline))[0]

print(f"\n  [$facet] Revenue by category:")
for r in facets["by_category"]:
    print(f"    {r['_id']:<15} ${r['revenue']:>8.2f}  ({r['count']} orders)")

print(f"\n  [$facet] Price histogram (amount buckets):")
for b in facets["price_histogram"]:
    label = str(b["_id"])
    print(f"    ${label:<10}  count={b['count']}  total=${b['total']:.2f}")

print(f"\n  [$facet] Revenue by region:")
for r in facets["by_region"]:
    print(f"    {r['_id']:<8} ${r['revenue']:>8.2f}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. $bucketAuto — auto-bucket into N equal-frequency bins
# ─────────────────────────────────────────────────────────────────────────────
pipeline = [
    {"$bucketAuto": {
        "groupBy":  "$amount",
        "buckets":  5,
        "output":   {"count": {"$sum": 1}, "avg_amount": {"$avg": "$amount"}},
    }}
]
print(f"\n  [$bucketAuto] 5 automatic price buckets:")
for b in col.aggregate(pipeline):
    lo = b["_id"]["min"]
    hi = b["_id"]["max"]
    print(f"    ${lo:6.2f}–${hi:6.2f}  count={b['count']}  avg=${b['avg_amount']:.2f}")

# ─────────────────────────────────────────────────────────────────────────────
# 3. $merge — write aggregation to a summary collection (materialized view)
#    Build a daily revenue summary and write it to "daily_summary".
#    On subsequent runs, $merge UPSERTS so existing days are updated.
# ─────────────────────────────────────────────────────────────────────────────
pipeline = [
    {"$group": {
        "_id":     {"$dateToString": {"format": "%Y-%m-%d", "date": "$date"}},
        "revenue": {"$sum": "$amount"},
        "orders":  {"$sum": 1},
        "avg_order": {"$avg": "$amount"},
    }},
    {"$addFields": {"date_str": "$_id", "refreshed_at": datetime.now(tz=timezone.utc)}},
    {"$merge": {
        "into":           "daily_summary",
        "on":             "_id",           # match on date string
        "whenMatched":    "merge",         # update existing
        "whenNotMatched": "insert",        # insert new
    }},
]
col.aggregate(pipeline)  # no results — $merge writes to the target collection
summary_col = db["daily_summary"]
total_days = summary_col.count_documents({})
print(f"\n  [$merge] daily_summary populated: {total_days} days")
# Show the 3 highest revenue days
for doc in summary_col.find({}, {"_id": 1, "revenue": 1, "orders": 1}).sort("revenue", -1).limit(3):
    print(f"    {doc['_id']}  revenue=${doc['revenue']:.2f}  orders={doc['orders']}")

# ─────────────────────────────────────────────────────────────────────────────
# 4. $setWindowFields — running total and rank by category
#    Only available on MongoDB 5.0+ (Atlas M0 free tier runs MongoDB 7.x).
# ─────────────────────────────────────────────────────────────────────────────
try:
    pipeline = [
        {"$match": {"category": "Electronics"}},
        {"$sort": {"date": 1}},
        {"$setWindowFields": {
            "partitionBy": "$category",
            "sortBy":      {"date": 1},
            "output": {
                "running_total": {
                    "$sum": "$amount",
                    "window": {"documents": ["unbounded", "current"]},
                },
                "moving_avg_3": {
                    "$avg": "$amount",
                    "window": {"documents": [-2, 0]},   # 3-doc moving average
                },
            },
        }},
        {"$project": {"_id": 0, "date": {"$dateToString": {"format": "%Y-%m-%d", "date": "$date"}},
                      "amount": 1, "running_total": {"$round": ["$running_total", 2]},
                      "moving_avg_3": {"$round": ["$moving_avg_3", 2]}}},
        {"$limit": 5},
    ]
    results = list(col.aggregate(pipeline))
    print(f"\n  [$setWindowFields] Electronics — running total & 3-doc moving avg:")
    for r in results:
        print(f"    {r['date']}  amount=${r['amount']:.2f}  "
              f"running=${r['running_total']:.2f}  avg3=${r.get('moving_avg_3', 0):.2f}")
except Exception as e:
    print(f"\n  [$setWindowFields] Not supported on this MongoDB version: {e}")

# cleanup
db.drop_collection("daily_summary")
print()
