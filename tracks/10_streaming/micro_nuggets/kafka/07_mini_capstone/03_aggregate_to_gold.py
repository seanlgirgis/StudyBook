"""
+==============================================================================+
|  NUGGET 07-03 . Mini Capstone: Silver -> Gold (Aggregate)                    |
|  Step 3 of 4: Consume silver, aggregate per user, produce to gold.          |
+==============================================================================+

GOLD LAYER AGGREGATION
-----------------------
  Consume from lab.silver (clean events).
  Compute per-user analytics:
    - total_events: count of all events
    - purchase_count: number of purchases
    - total_spend: sum of purchase amounts
    - pages_visited: unique pages
    - first_seen_ts / last_seen_ts: activity window
    - top_action: most frequent action

  Produce aggregated user profiles to lab.gold.
  Also write a local JSON summary (for inspection without Kafka consumer).

USAGE
-----
    python 03_aggregate_to_gold.py
    (Run after 02_clean_to_silver.py)
"""
from __future__ import annotations

import json
import sys
import time
import uuid
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _kafka_connect import BROKER, require_broker

require_broker(BROKER)

from kafka import KafkaConsumer, KafkaProducer

print("\n-- Mini Capstone Step 3: Silver -> Gold (Aggregate) --")
print(f"  Broker: {BROKER}")
print(f"  Source: lab.silver  ->  Sink: lab.gold + local summary")
print()

# ─────────────────────────────────────────────────────────────────────────────
# Consume all silver events and aggregate per user
# ─────────────────────────────────────────────────────────────────────────────
consumer = KafkaConsumer(
    "lab.silver",
    bootstrap_servers=BROKER,
    group_id=f"gold_agg_{uuid.uuid4().hex[:8]}",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    consumer_timeout_ms=8_000,
    value_deserializer=lambda b: json.loads(b.decode("utf-8")),
)

user_stats: dict[str, dict] = defaultdict(lambda: {
    "total_events":    0,
    "purchase_count":  0,
    "total_spend":     0.0,
    "pages_visited":   set(),
    "actions":         defaultdict(int),
    "first_seen_ts":   None,
    "last_seen_ts":    None,
    "is_late_events":  0,
})

silver_count = 0
for msg in consumer:
    env = msg.value
    if not isinstance(env, dict):
        continue
    payload = env.get("payload", {})
    user_id = payload.get("user_id")
    if not user_id:
        continue

    silver_count += 1
    s = user_stats[user_id]
    s["total_events"] += 1
    s["actions"][payload.get("action", "unknown")] += 1
    s["pages_visited"].add(payload.get("page", "/unknown"))

    amount = payload.get("amount")
    if amount is not None and amount > 0:
        s["purchase_count"] += 1
        s["total_spend"] += amount

    ts = payload.get("ts", 0)
    if s["first_seen_ts"] is None or ts < s["first_seen_ts"]:
        s["first_seen_ts"] = ts
    if s["last_seen_ts"] is None or ts > s["last_seen_ts"]:
        s["last_seen_ts"] = ts

    if env.get("is_late"):
        s["is_late_events"] += 1

consumer.close()
print(f"  Read {silver_count} events from silver layer.")
print()

# ─────────────────────────────────────────────────────────────────────────────
# Produce aggregated profiles to gold topic
# ─────────────────────────────────────────────────────────────────────────────
gold_producer = KafkaProducer(
    bootstrap_servers=BROKER,
    acks="all",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda k: k.encode("utf-8") if isinstance(k, str) else k,
    request_timeout_ms=15_000,
)

gold_records = []
print(f"  User profiles produced to lab.gold:")
print(f"  {'user_id':10}  {'events':7}  {'purchases':10}  {'spend':8}  {'pages':7}  top_action")
print(f"  {'-'*65}")

for user_id, s in sorted(user_stats.items()):
    top_action = max(s["actions"], key=s["actions"].get) if s["actions"] else "none"
    profile = {
        "user_id":       user_id,
        "total_events":  s["total_events"],
        "purchase_count": s["purchase_count"],
        "total_spend":   round(s["total_spend"], 2),
        "pages_visited": sorted(s["pages_visited"]),
        "top_action":    top_action,
        "first_seen_ts": s["first_seen_ts"],
        "last_seen_ts":  s["last_seen_ts"],
        "is_late_events": s["is_late_events"],
        "_aggregated_at": int(time.time()),
        "_schema_version": 1,
    }
    gold_records.append(profile)

    envelope = {
        "event_id":       str(uuid.uuid4()),
        "event_type":     "analytics.user.profile",
        "schema_version": 1,
        "source_service": "gold_pipeline",
        "produced_at":    datetime.now(timezone.utc).isoformat(),
        "payload":        profile,
    }
    gold_producer.send("lab.gold", key=user_id, value=envelope)
    print(f"  {user_id:<10}  {s['total_events']:<7}  {s['purchase_count']:<10}  "
          f"{round(s['total_spend'],2):<8}  {len(s['pages_visited']):<7}  {top_action}")

gold_producer.flush()
gold_producer.close()

# ─────────────────────────────────────────────────────────────────────────────
# Write local summary JSON
# ─────────────────────────────────────────────────────────────────────────────
summary_path = Path(__file__).parent / "gold_summary.json"
with open(summary_path, "w", encoding="utf-8") as f:
    json.dump(gold_records, f, indent=2)

print()
print(f"  Gold profiles produced: {len(gold_records)}")
print(f"  Local summary written:  {summary_path.name}")
print()
print("  Next: python 04_failure_injection.py")
print()
