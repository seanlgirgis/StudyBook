"""
+==============================================================================+
|  NUGGET 07-02 . Mini Capstone: Bronze -> Silver (Clean + Dedup + Validate)   |
|  Step 2 of 4: Consume bronze, clean, validate, dedup, produce to silver.    |
+==============================================================================+

SILVER LAYER PROCESSING
-----------------------
  1. Consume from lab.bronze
  2. Validate required fields (user_id, action, ts)
  3. Deduplicate by event_id
  4. Filter out-of-order events beyond allowed_lateness
  5. Normalize payload (add missing optional fields with defaults)
  6. Produce clean events to lab.silver
  7. Route bad events to lab.dlq

QUALITY METRICS TRACKED
-----------------------
  - consumed: total messages read from bronze
  - validated: passed all checks
  - deduped: dropped as duplicate event_id
  - invalid: failed field validation -> DLQ
  - late: out-of-order beyond allowed_lateness -> flagged but still accepted

USAGE
-----
    python 02_clean_to_silver.py
    (Run after 01_ingest_bronze.py)
"""
from __future__ import annotations

import json
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _kafka_connect import BROKER, require_broker, safe_json_deserializer

require_broker(BROKER)

from kafka import KafkaConsumer, KafkaProducer

print("\n-- Mini Capstone Step 2: Bronze -> Silver --")
print(f"  Broker: {BROKER}")
print(f"  Source: lab.bronze  ->  Sink: lab.silver  (bad -> lab.dlq)")
print()

ALLOWED_LATENESS_S = 60  # flag events older than 60s

# Producers
silver_producer = KafkaProducer(
    bootstrap_servers=BROKER,
    acks="all",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda k: k.encode("utf-8") if isinstance(k, str) else k,
    request_timeout_ms=15_000,
)

dlq_producer = KafkaProducer(
    bootstrap_servers=BROKER,
    acks=1,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    request_timeout_ms=15_000,
)

# Dedup state
seen_event_ids: set[str] = set()

# Counters
counters = {
    "consumed":   0,
    "validated":  0,
    "deduped":    0,
    "invalid":    0,
    "late":       0,
    "dlq":        0,
}

now = int(time.time())

def validate_payload(payload: dict) -> list[str]:
    errors = []
    if not payload.get("user_id"):
        errors.append("Missing required field: user_id")
    if not payload.get("action"):
        errors.append("Missing required field: action")
    ts = payload.get("ts")
    if ts is None or not isinstance(ts, int):
        errors.append("Invalid or missing ts")
    return errors


def normalize(payload: dict) -> dict:
    """Add optional fields with defaults."""
    return {
        "event_id":   payload.get("event_id", str(uuid.uuid4())),
        "user_id":    payload["user_id"],
        "action":     payload["action"],
        "page":       payload.get("page", "/unknown"),
        "ts":         payload["ts"],
        "session_id": payload.get("session_id", "unknown"),
        "amount":     payload.get("amount"),
        "currency":   payload.get("currency", "USD"),
        "_silver_ts": int(time.time()),
        "_from_bronze": True,
    }


# Consumer
consumer = KafkaConsumer(
    "lab.bronze",
    bootstrap_servers=BROKER,
    group_id=f"silver_pipeline_{uuid.uuid4().hex[:8]}",
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    consumer_timeout_ms=8_000,
    value_deserializer=safe_json_deserializer,
)

for msg in consumer:
    counters["consumed"] += 1
    env = msg.value

    if not isinstance(env, dict):
        counters["invalid"] += 1
        counters["dlq"] += 1
        consumer.commit()
        continue

    eid = env.get("event_id", "?")
    payload = env.get("payload", {})

    # Deduplication
    if eid in seen_event_ids:
        counters["deduped"] += 1
        print(f"  DEDUP    event_id={eid[:12]}...")
        consumer.commit()
        continue
    seen_event_ids.add(eid)

    # Validation
    errors = validate_payload(payload)
    if errors:
        counters["invalid"] += 1
        counters["dlq"] += 1
        dlq_msg = {
            "dlq_id": str(uuid.uuid4()),
            "original_topic": msg.topic,
            "original_offset": msg.offset,
            "original_payload": payload,
            "failure_reason": "; ".join(errors),
            "failure_ts": int(time.time()),
        }
        dlq_producer.send("lab.dlq", value=dlq_msg)
        print(f"  INVALID  event_id={eid[:12]}...  errors={errors}")
        consumer.commit()
        continue

    # Late event check
    ev_ts = payload.get("ts", 0)
    is_late = (now - ev_ts) > ALLOWED_LATENESS_S
    if is_late:
        counters["late"] += 1

    # Normalize and produce to silver
    clean_payload = normalize(payload)
    silver_envelope = {
        "event_id":       eid,
        "event_type":     env.get("event_type", "user.behavior.event"),
        "schema_version": 2,
        "source_service": "silver_pipeline",
        "produced_at":    datetime.now(timezone.utc).isoformat(),
        "is_late":        is_late,
        "payload":        clean_payload,
    }
    silver_producer.send("lab.silver", key=clean_payload["user_id"], value=silver_envelope)
    counters["validated"] += 1
    status = " [LATE]" if is_late else ""
    print(f"  SILVER   event_id={eid[:12]}...  user={clean_payload['user_id']}  action={clean_payload['action']}{status}")
    consumer.commit()

silver_producer.flush()
silver_producer.close()
dlq_producer.flush()
dlq_producer.close()
consumer.close()

print()
print(f"  Bronze -> Silver pipeline complete:")
print(f"    consumed:   {counters['consumed']}")
print(f"    validated:  {counters['validated']}")
print(f"    deduped:    {counters['deduped']}")
print(f"    invalid:    {counters['invalid']}  (routed to lab.dlq)")
print(f"    late:       {counters['late']}  (accepted but flagged)")
print()
print("  Next: python 03_aggregate_to_gold.py")
print()

