"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  CAPSTONE 02 · Aggregate Silver Layer                                        ║
║  Transform raw events into structured daily metrics via $merge.              ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Build the Silver layer: aggregate raw Bronze events into per-day, per-type
metrics and write them incrementally to silver_metrics using $merge.

DESIGN
──────
Silver layer goals:
  1. Deduplicate raw events (event_id uniqueness already enforced in Bronze).
  2. Compute daily aggregates: total events, unique users, revenue, error rates.
  3. Write results incrementally — re-running this script safely updates
     existing days and inserts new ones ($merge with whenMatched="replace").
  4. Add data quality flags: mark days with anomalously high error rates.

Pipeline stages used:
  $match       → filter to a date range (supports incremental runs)
  $group       → group by date + event_type
  $facet       → compute per-day summary alongside per-type breakdown
  $addFields   → compute derived metrics (error_rate, avg_order_value)
  $merge       → upsert results into silver_metrics

USAGE
─────
    python 02_aggregate_silver.py

EXPECTED OUTPUT
───────────────
    ── CAPSTONE 02 · Aggregate Silver Layer ──────────

      Raw events: 500
      Date range: 2026-03-04 → 2026-04-03

      Running day+type aggregation pipeline...
      Silver layer: 174 metric documents written to silver_metrics.

      Sample silver records (last 5 days, purchases):
        2026-04-02  purchase  events=6  users=5  revenue=$1234.56  errors=0
        ...

      Data quality flags:
        High error days (error_rate > 20%): N
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _mg_connect import get_lab_db

db = get_lab_db()
print("\n── CAPSTONE 02 · Aggregate Silver Layer ──────────")

raw_events    = db["raw_events"]
silver_col    = db["silver_metrics"]
runs_col      = db["ingestion_runs"]

n_raw = raw_events.count_documents({})
if n_raw == 0:
    print("  [!] raw_events is empty. Run 01_land_raw_events.py first.")
    sys.exit(1)

print(f"\n  Raw events: {n_raw}")

# ─────────────────────────────────────────────────────────────────────────────
# Date range info
# ─────────────────────────────────────────────────────────────────────────────
date_range = list(raw_events.aggregate([
    {"$group": {
        "_id":    None,
        "min_ts": {"$min": "$event_ts"},
        "max_ts": {"$max": "$event_ts"},
    }},
]))[0]
min_date = date_range["min_ts"].strftime("%Y-%m-%d")
max_date = date_range["max_ts"].strftime("%Y-%m-%d")
print(f"  Date range: {min_date} → {max_date}")

# ─────────────────────────────────────────────────────────────────────────────
# Silver aggregation pipeline
# Groups by (date_str, event_type) — each unique combination = one silver doc.
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n  Running day+type aggregation pipeline...")
run_ts = datetime.now(tz=timezone.utc)

pipeline = [
    # 1. Add a string date field for grouping
    {"$addFields": {
        "date_str": {
            "$dateToString": {"format": "%Y-%m-%d", "date": "$event_ts"}
        }
    }},

    # 2. Group by date + event_type
    {"$group": {
        "_id": {
            "date":       "$date_str",
            "event_type": "$event_type",
        },
        "event_count":   {"$sum": 1},
        "unique_users":  {"$addToSet": "$user_id"},
        "unique_sessions": {"$addToSet": "$session_id"},

        # Revenue — only purchase events have an amount field
        "total_revenue": {"$sum": {"$ifNull": ["$amount", 0]}},
        "purchase_count": {
            "$sum": {"$cond": [{"$eq": ["$event_type", "purchase"]}, 1, 0]}
        },

        # Error tracking
        "error_count": {
            "$sum": {"$cond": [{"$eq": ["$event_type", "error"]}, 1, 0]}
        },
        "error_codes": {
            "$addToSet": {"$ifNull": ["$error_code", "$$REMOVE"]}
        },

        # Device breakdown
        "mobile_count":  {"$sum": {"$cond": [{"$eq": ["$device", "mobile"]},  1, 0]}},
        "desktop_count": {"$sum": {"$cond": [{"$eq": ["$device", "desktop"]}, 1, 0]}},

        # Countries
        "countries": {"$addToSet": "$country"},
    }},

    # 3. Reshape — unwrap the composite _id, compute derived metrics
    {"$project": {
        "_id":         {"$concat": ["$_id.date", "|", "$_id.event_type"]},  # composite PK
        "date":        "$_id.date",
        "event_type":  "$_id.event_type",
        "event_count": 1,
        "unique_users":    {"$size": "$unique_users"},
        "unique_sessions": {"$size": "$unique_sessions"},
        "total_revenue":   {"$round": ["$total_revenue", 2]},
        "avg_order_value": {
            "$cond": [
                {"$gt": ["$purchase_count", 0]},
                {"$round": [{"$divide": ["$total_revenue", "$purchase_count"]}, 2]},
                None,
            ]
        },
        "purchase_count":  1,
        "error_count":     1,
        "error_codes":     1,
        "mobile_pct": {
            "$round": [
                {"$multiply": [{"$divide": ["$mobile_count", "$event_count"]}, 100]}, 1
            ]
        },
        "country_count":  {"$size": "$countries"},
        "countries":       1,

        # Data quality flag
        "high_error_day": {
            "$gt": [
                {"$divide": ["$error_count", "$event_count"]},
                0.20,   # flag days where > 20% of events are errors
            ]
        },
        "computed_at": run_ts,
    }},

    # 4. Sort for readability (does not affect $merge)
    {"$sort": {"date": -1, "event_type": 1}},

    # 5. $merge — upsert into silver_metrics
    #    whenMatched="replace": overwrite the entire doc (full recompute per day).
    #    whenNotMatched="insert": create new day records.
    {"$merge": {
        "into":           "silver_metrics",
        "on":             "_id",
        "whenMatched":    "replace",
        "whenNotMatched": "insert",
    }},
]

raw_events.aggregate(pipeline)  # $merge writes directly — no cursor results

n_silver = silver_col.count_documents({})
print(f"  Silver layer: {n_silver} metric documents written to silver_metrics.")

# ─────────────────────────────────────────────────────────────────────────────
# Sample output — most recent purchase records
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n  Sample silver records (recent purchases):")
for doc in (silver_col.find(
    {"event_type": "purchase"},
    {"_id": 0, "date": 1, "event_type": 1, "event_count": 1,
     "unique_users": 1, "total_revenue": 1, "avg_order_value": 1},
).sort("date", -1).limit(5)):
    print(f"    {doc['date']}  {doc['event_type']:<14} "
          f"events={doc['event_count']}  users={doc['unique_users']}  "
          f"revenue=${doc.get('total_revenue', 0):.2f}  "
          f"avg=${doc.get('avg_order_value') or 0:.2f}")

# ─────────────────────────────────────────────────────────────────────────────
# Data quality summary
# ─────────────────────────────────────────────────────────────────────────────
high_error = silver_col.count_documents({"high_error_day": True})
print(f"\n  Data quality flags:")
print(f"    High error days (error_rate > 20%): {high_error}")

# ─────────────────────────────────────────────────────────────────────────────
# Record the silver run
# ─────────────────────────────────────────────────────────────────────────────
import uuid
runs_col.insert_one({
    "run_id":        str(uuid.uuid4()),
    "stage":         "silver",
    "collection":    "silver_metrics",
    "started_at":    run_ts,
    "completed_at":  datetime.now(tz=timezone.utc),
    "input_docs":    n_raw,
    "output_docs":   n_silver,
    "status":        "success",
})

print(f"\n  Silver layer complete. Run 03_upsert_gold.py next.")
print()
