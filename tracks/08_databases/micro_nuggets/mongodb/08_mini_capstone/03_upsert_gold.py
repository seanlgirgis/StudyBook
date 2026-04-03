"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  CAPSTONE 03 · Upsert Gold Layer                                             ║
║  Build the final dashboard-ready Gold collection from Silver metrics.        ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Build the Gold layer: aggregate Silver metrics into compact, dashboard-ready
summaries and upsert them into gold_dashboard using bulk_write.

GOLD LAYER DESIGN
─────────────────
The Gold layer contains one document per "business entity" that a dashboard
or API reads directly:
  - overall_summary: single doc with KPIs across all time
  - daily_kpi_{YYYY-MM-DD}: one doc per day with all event type rollups
  - top_events_week: top event types by volume in the last 7 days

Why upsert (not $merge pipeline):
  - We read Silver, compute in Python, and write Gold via bulk_write.
  - This pattern mirrors Databricks SCD Type 2 / Snowflake MERGE.
  - Idempotent: safe to re-run; existing Gold docs are overwritten.
  - Python gives us full flexibility (ML scoring, external API lookups, etc.)
    that a pure MongoDB aggregation pipeline cannot easily do.

USAGE
─────
    python 03_upsert_gold.py

EXPECTED OUTPUT
───────────────
    ── CAPSTONE 03 · Upsert Gold Layer ───────────────

      Silver docs: 174
      Building Gold documents...

      overall_summary:
        total_events=500  unique_users=100  revenue=$12,345.67  days_covered=30

      Daily KPI docs upserted: 30

      Top 5 event types (all time):
        page_view     201 events  (40.2%)
        click         125 events  (25.0%)
        ...

      Gold layer complete. Pipeline run summary:
        Bronze: 500 docs  Silver: 174 docs  Gold: 32 docs
"""
from __future__ import annotations

import sys
import uuid
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from pymongo import UpdateOne

sys.path.insert(0, str(Path(__file__).parent.parent))
from _mg_connect import get_lab_db

db = get_lab_db()
print("\n── CAPSTONE 03 · Upsert Gold Layer ───────────────")

silver_col  = db["silver_metrics"]
gold_col    = db["gold_dashboard"]
runs_col    = db["ingestion_runs"]

n_silver = silver_col.count_documents({})
if n_silver == 0:
    print("  [!] silver_metrics is empty. Run 02_aggregate_silver.py first.")
    sys.exit(1)

print(f"\n  Silver docs: {n_silver}")
print(f"  Building Gold documents...")
run_ts = datetime.now(tz=timezone.utc)

# ─────────────────────────────────────────────────────────────────────────────
# Read all Silver docs into memory (small dataset — fine for a lab)
# In production, keep this as a $merge pipeline or stream via cursor.
# ─────────────────────────────────────────────────────────────────────────────
silver_docs = list(silver_col.find({}))

# ─────────────────────────────────────────────────────────────────────────────
# 1. Overall summary — single KPI document
# ─────────────────────────────────────────────────────────────────────────────
total_events  = sum(d["event_count"] for d in silver_docs)
total_revenue = sum(d.get("total_revenue", 0) for d in silver_docs)
all_users     = set()
for d in silver_docs:
    # unique_users is a count in Silver — we can't un-dedupe here.
    # Use max approximation or re-aggregate from Bronze for exact count.
    pass
unique_user_count = list(db["raw_events"].aggregate([
    {"$group": {"_id": "$user_id"}},
    {"$count": "n"},
]))[0]["n"]

all_dates = sorted(set(d["date"] for d in silver_docs))
error_docs = [d for d in silver_docs if d["event_type"] == "error"]
total_errors = sum(d["event_count"] for d in error_docs)
overall_error_rate = round(total_errors / total_events * 100, 2) if total_events else 0

purchase_docs = [d for d in silver_docs if d["event_type"] == "purchase"]
total_purchases = sum(d["event_count"] for d in purchase_docs)

overall_doc = {
    "_id":               "overall_summary",
    "total_events":      total_events,
    "unique_users":      unique_user_count,
    "total_revenue":     round(total_revenue, 2),
    "total_purchases":   total_purchases,
    "avg_order_value":   round(total_revenue / total_purchases, 2) if total_purchases else 0,
    "error_rate_pct":    overall_error_rate,
    "days_covered":      len(all_dates),
    "date_from":         min(all_dates) if all_dates else None,
    "date_to":           max(all_dates) if all_dates else None,
    "refreshed_at":      run_ts,
}

print(f"\n  overall_summary:")
print(f"    total_events={overall_doc['total_events']}  "
      f"unique_users={overall_doc['unique_users']}  "
      f"revenue=${overall_doc['total_revenue']:,.2f}  "
      f"days_covered={overall_doc['days_covered']}")
print(f"    purchases={overall_doc['total_purchases']}  "
      f"avg_order=${overall_doc['avg_order_value']:.2f}  "
      f"error_rate={overall_doc['error_rate_pct']}%")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Daily KPI docs — one per day, all event types rolled up
# ─────────────────────────────────────────────────────────────────────────────
days: dict[str, dict] = defaultdict(lambda: {
    "event_count": 0, "revenue": 0.0, "purchases": 0,
    "errors": 0, "unique_users": 0,
    "by_type": {},
})

for d in silver_docs:
    date = d["date"]
    etype = d["event_type"]
    days[date]["event_count"] += d["event_count"]
    days[date]["revenue"]     += d.get("total_revenue", 0)
    days[date]["purchases"]   += d.get("purchase_count", 0)
    days[date]["errors"]      += d.get("error_count", 0)
    days[date]["unique_users"] = max(days[date]["unique_users"], d.get("unique_users", 0))
    days[date]["by_type"][etype] = d["event_count"]

gold_ops = [
    UpdateOne(
        {"_id": "overall_summary"},
        {"$set": overall_doc},
        upsert=True,
    )
]

for date_str, day_data in sorted(days.items()):
    doc = {
        "date":          date_str,
        "event_count":   day_data["event_count"],
        "unique_users":  day_data["unique_users"],
        "revenue":       round(day_data["revenue"], 2),
        "purchases":     day_data["purchases"],
        "error_count":   day_data["errors"],
        "error_rate_pct": round(day_data["errors"] / day_data["event_count"] * 100, 2)
                          if day_data["event_count"] else 0,
        "by_type":       day_data["by_type"],
        "refreshed_at":  run_ts,
    }
    gold_ops.append(UpdateOne(
        {"_id": f"daily_kpi_{date_str}"},
        {"$set": doc},
        upsert=True,
    ))

# ─────────────────────────────────────────────────────────────────────────────
# 3. Top event types summary document (all time)
# ─────────────────────────────────────────────────────────────────────────────
type_totals: dict[str, int] = defaultdict(int)
for d in silver_docs:
    type_totals[d["event_type"]] += d["event_count"]

top_events = sorted(type_totals.items(), key=lambda x: x[1], reverse=True)
top_doc = {
    "_id":         "top_events_alltime",
    "computed_at": run_ts,
    "rankings":    [
        {"rank": i+1, "event_type": etype, "count": cnt,
         "share_pct": round(cnt / total_events * 100, 1)}
        for i, (etype, cnt) in enumerate(top_events)
    ],
}
gold_ops.append(UpdateOne({"_id": "top_events_alltime"}, {"$set": top_doc}, upsert=True))

# ─────────────────────────────────────────────────────────────────────────────
# Bulk upsert all Gold documents
# ─────────────────────────────────────────────────────────────────────────────
result = gold_col.bulk_write(gold_ops, ordered=False)
n_gold = gold_col.count_documents({})
print(f"\n  Daily KPI docs upserted: {len(days)}")
print(f"  Total Gold docs: {n_gold}  "
      f"(upserted={result.upserted_count} modified={result.modified_count})")

print(f"\n  Top 5 event types (all time):")
for rank in top_doc["rankings"][:5]:
    print(f"    {rank['event_type']:<16} {rank['count']:>5} events  ({rank['share_pct']}%)")

# ─────────────────────────────────────────────────────────────────────────────
# Record the Gold run and print pipeline summary
# ─────────────────────────────────────────────────────────────────────────────
runs_col.insert_one({
    "run_id":        str(uuid.uuid4()),
    "stage":         "gold",
    "collection":    "gold_dashboard",
    "started_at":    run_ts,
    "completed_at":  datetime.now(tz=timezone.utc),
    "input_docs":    n_silver,
    "output_docs":   n_gold,
    "status":        "success",
})

n_bronze = db["raw_events"].count_documents({})
print(f"\n  Gold layer complete. Pipeline run summary:")
print(f"    Bronze: {n_bronze} docs  Silver: {n_silver} docs  Gold: {n_gold} docs")
print(f"\n  Run 04_reset_lab.py to clean up all capstone collections.")
print()
