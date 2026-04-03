"""
+==============================================================================+
|  NUGGET 07-01 . Mini Capstone: Ingest Raw Events -> Bronze Topic             |
|  Step 1 of 4: Simulate raw event ingestion into the bronze layer.            |
+==============================================================================+

MEDALLION ARCHITECTURE IN KAFKA
---------------------------------
  Bronze: raw, unvalidated events. Exactly as received from the source.
  Silver: cleaned, deduplicated, validated events. Ready for analysis.
  Gold:   aggregated / analytical results. Ready for dashboards / ML.

  Topic mapping:
    lab.bronze  <-- raw events (this script)
    lab.silver  <-- cleaned events (02_clean_to_silver.py)
    lab.gold    <-- aggregates (03_aggregate_to_gold.py)

THIS SCRIPT (Step 1):
  Simulates a data source producing raw click + order events to lab.bronze.
  Includes realistic noise:
    - Some events missing required fields (validation fails downstream)
    - Some events with duplicate event_ids (dedup downstream)
    - Some events with out-of-order timestamps (late events)
    - All events wrapped in the standard envelope

USAGE
-----
    python 01_ingest_bronze.py
"""
from __future__ import annotations

import json
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _kafka_connect import BROKER, require_broker

require_broker(BROKER)

from kafka import KafkaProducer

print("\n-- Mini Capstone Step 1: Ingest Raw Events -> Bronze --")
print(f"  Broker: {BROKER}")
print(f"  Target topic: lab.bronze")
print()

producer = KafkaProducer(
    bootstrap_servers=BROKER,
    acks="all",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda k: k.encode("utf-8") if isinstance(k, str) else k,
    request_timeout_ms=15_000,
)

now = int(time.time())
users = ["alice", "bob", "carol", "dave", "eve"]
pages = ["/home", "/products", "/checkout", "/search", "/about"]
actions = ["page_view", "click", "purchase", "add_to_cart", "search"]

counts = {"valid": 0, "missing_field": 0, "duplicate": 0, "out_of_order": 0}
DUPLICATE_ID = str(uuid.uuid4())

for i in range(80):
    user = users[i % len(users)]

    # Normal event
    payload = {
        "event_id":   str(uuid.uuid4()),
        "user_id":    user,
        "action":     actions[i % len(actions)],
        "page":       pages[i % len(pages)],
        "ts":         now + i,
        "session_id": f"sess_{user}_{i // 10}",
        "amount":     round(5.0 + (i % 20) * 3.5, 2) if actions[i % len(actions)] == "purchase" else None,
    }

    # Inject noise
    if i % 15 == 0 and i > 0:
        # Missing required field (user_id missing)
        del payload["user_id"]
        counts["missing_field"] += 1
    elif i % 20 == 0 and i > 0:
        # Duplicate event_id
        payload["event_id"] = DUPLICATE_ID
        counts["duplicate"] += 1
    elif i % 25 == 0 and i > 0:
        # Out-of-order: timestamp 120s in the past
        payload["ts"] = now - 120 + (i % 10)
        counts["out_of_order"] += 1
    else:
        counts["valid"] += 1

    envelope = {
        "event_id":       payload.get("event_id", str(uuid.uuid4())),
        "event_type":     "user.behavior.event",
        "schema_version": 1,
        "source_service": "web_tracker",
        "produced_at":    datetime.now(timezone.utc).isoformat(),
        "payload":        payload,
    }

    key = payload.get("user_id", user)
    producer.send("lab.bronze", key=key, value=envelope)

producer.flush()
producer.close()

total = sum(counts.values())
print(f"  Ingested {total} raw events to lab.bronze:")
print(f"    Valid events:          {counts['valid']}")
print(f"    Missing user_id:       {counts['missing_field']}  (will be caught in silver)")
print(f"    Duplicate event_ids:   {counts['duplicate']}   (will be deduped in silver)")
print(f"    Out-of-order ts:       {counts['out_of_order']}    (will be flagged in silver)")
print()
print("  Bronze = raw zone. No validation here -- store first, clean later.")
print()
print("  Next: python 02_clean_to_silver.py")
print()
