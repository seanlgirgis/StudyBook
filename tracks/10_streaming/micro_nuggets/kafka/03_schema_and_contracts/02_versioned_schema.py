"""
+==============================================================================+
|  NUGGET 03-02 . Versioned Schema and Backward Compatibility                  |
|  Evolve event schemas without breaking existing consumers.                   |
+==============================================================================+

CONCEPTS
--------
  Schema Evolution:
    As systems grow, event schemas change: new fields added, old fields removed,
    types changed. Kafka retains old messages -- consumers may read old AND new
    versions from the same topic.

  Compatibility Rules (Avro / JSON Schema conventions):

  BACKWARD compatible change (consumer reads new schema, parses old data):
    - ADD optional field with a default value.
    - REMOVE field (consumer ignores it via schema filtering).
    OK: old producers still work. New consumers handle old messages.

  FORWARD compatible change (producer writes new schema, old consumer reads):
    - ADD field (old consumer ignores unknown fields if written defensively).
    - REMOVE required field: NOT forward compatible.

  FULL compatible: both backward AND forward.

  BREAKING changes (avoid):
    - RENAME a field.
    - CHANGE a field type (e.g., int -> string).
    - ADD a required field with no default.

  Versioning Strategy:
    - Include schema_version in the event envelope.
    - Consumers use schema_version to select the correct parsing logic.
    - Run multiple consumer versions in parallel during migration.

OPERATIONS COVERED
------------------
  1. Produce v1 events (baseline schema)
  2. Produce v2 events (backward-compatible: new optional field added)
  3. Consumer handles both v1 and v2 transparently
  4. Demonstrate breaking change detection

USAGE
-----
    python 02_versioned_schema.py
"""
from __future__ import annotations

import json
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent))
from _kafka_connect import BROKER, require_broker, safe_json_deserializer

require_broker(BROKER)

from kafka import KafkaConsumer, KafkaProducer

print("\n-- Nugget 03-02: Versioned Schema and Backward Compatibility --")
print(f"  Broker: {BROKER}")
print()

TOPIC = "lab.raw.events"

# ─────────────────────────────────────────────────────────────────────────────
# Schema definitions
# ─────────────────────────────────────────────────────────────────────────────

# V1 OrderPlaced schema
V1_REQUIRED = {"order_id", "user_id", "amount", "ts"}
V1_OPTIONAL: dict[str, Any] = {}  # no optional fields in v1

# V2 OrderPlaced: adds optional fields (backward compatible with v1)
V2_REQUIRED = {"order_id", "user_id", "amount", "ts"}
V2_OPTIONAL: dict[str, Any] = {
    "currency": "USD",      # new optional field with default
    "channel": "web",       # new optional field with default
    "coupon_code": None,    # new optional field, nullable
}


def validate_v1(payload: dict) -> list[str]:
    missing = V1_REQUIRED - set(payload.keys())
    return [f"Missing v1 field: {f}" for f in missing]


def validate_v2(payload: dict) -> list[str]:
    missing = V2_REQUIRED - set(payload.keys())
    return [f"Missing v2 field: {f}" for f in missing]


def normalize_to_v2(payload: dict, schema_version: int) -> dict:
    """
    Upgrade a v1 payload to v2 by filling in defaults for new optional fields.
    This is the backward-compatibility migration step in the consumer.
    """
    if schema_version >= 2:
        return payload
    # v1 -> v2: apply defaults for new fields
    upgraded = {**payload}
    for field, default in V2_OPTIONAL.items():
        upgraded.setdefault(field, default)
    upgraded["_upgraded_from_v1"] = True
    return upgraded


# ─────────────────────────────────────────────────────────────────────────────
# 1. Produce v1 events
# ─────────────────────────────────────────────────────────────────────────────
print("  [1] Producing v1 OrderPlaced events (original schema):")

producer = KafkaProducer(
    bootstrap_servers=BROKER,
    acks="all",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda k: k.encode("utf-8") if isinstance(k, str) else k,
    request_timeout_ms=15_000,
)

v1_events = []
for i in range(4):
    payload = {
        "order_id": f"ORD-V1-{100 + i}",
        "user_id":  f"user_{i}",
        "amount":   round(10.0 + i * 25.0, 2),
        "ts":       int(time.time()),
    }
    envelope = {
        "event_id":       str(uuid.uuid4()),
        "event_type":     "commerce.order.placed",
        "schema_version": 1,
        "payload":        payload,
        "produced_at":    datetime.now(timezone.utc).isoformat(),
    }
    v1_events.append(envelope)
    meta = producer.send(TOPIC, key=f"user_{i}", value=envelope).get(timeout=10)
    print(f"    v1 order_id={payload['order_id']}  offset={meta.offset}")

print()

# ─────────────────────────────────────────────────────────────────────────────
# 2. Produce v2 events (backward-compatible: new optional fields added)
# ─────────────────────────────────────────────────────────────────────────────
print("  [2] Producing v2 OrderPlaced events (new optional fields: currency, channel):")

v2_events = []
for i in range(4):
    payload = {
        "order_id":    f"ORD-V2-{200 + i}",
        "user_id":     f"user_{i}",
        "amount":      round(50.0 + i * 30.0, 2),
        "ts":          int(time.time()),
        "currency":    "EUR" if i % 2 == 0 else "USD",  # new in v2
        "channel":     "mobile" if i % 2 == 0 else "web",  # new in v2
        "coupon_code": f"SAVE{i * 10}" if i > 0 else None,  # new in v2
    }
    envelope = {
        "event_id":       str(uuid.uuid4()),
        "event_type":     "commerce.order.placed",
        "schema_version": 2,
        "payload":        payload,
        "produced_at":    datetime.now(timezone.utc).isoformat(),
    }
    v2_events.append(envelope)
    meta = producer.send(TOPIC, key=f"user_{i}", value=envelope).get(timeout=10)
    print(f"    v2 order_id={payload['order_id']}  currency={payload['currency']}  offset={meta.offset}")

producer.flush()
producer.close()
print()

# ─────────────────────────────────────────────────────────────────────────────
# 3. Consumer handles both v1 and v2 transparently
# ─────────────────────────────────────────────────────────────────────────────
print("  [3] Consumer reading v1 and v2 -- normalizes to v2 with defaults:")

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BROKER,
    group_id=f"versioned_schema_{uuid.uuid4().hex[:8]}",
    auto_offset_reset="earliest",
    consumer_timeout_ms=6_000,
    value_deserializer=safe_json_deserializer,
)

v1_received = v2_received = other = 0
for msg in consumer:
    env = msg.value
    if not isinstance(env, dict) or env.get("event_type") != "commerce.order.placed":
        other += 1
        continue
    ver = env.get("schema_version", 0)
    payload = env.get("payload", {})
    normalized = normalize_to_v2(payload, ver)

    if ver == 1:
        errs = validate_v1(payload)
        v1_received += 1
        upgraded = normalized.get("_upgraded_from_v1", False)
        print(f"    v1 -> normalized  order_id={payload.get('order_id')}  "
              f"currency={normalized.get('currency')}  upgraded={upgraded}")
    elif ver == 2:
        errs = validate_v2(payload)
        v2_received += 1
        if not errs:
            print(f"    v2 native         order_id={payload.get('order_id')}  "
                  f"currency={payload.get('currency')}  channel={payload.get('channel')}")
    else:
        other += 1

consumer.close()
print()
print(f"    v1 events: {v1_received}  v2 events: {v2_received}  other: {other}")
print()

# ─────────────────────────────────────────────────────────────────────────────
# 4. Breaking change detection
# ─────────────────────────────────────────────────────────────────────────────
print("  [4] Breaking change detection:")

# Simulate what happens if producer sends v3 with renamed field (breaking)
v3_payload = {
    "order_reference": "ORD-V3-999",  # RENAMED from order_id -- BREAKING!
    "buyer_id": "alice",               # RENAMED from user_id  -- BREAKING!
    "total": 199.99,                   # RENAMED from amount   -- BREAKING!
    "ts": int(time.time()),
    "schema_version": 3,
}
errs_v2_against_v3 = validate_v2(v3_payload)
print(f"    v2 validator against v3 payload errors: {errs_v2_against_v3}")
print(f"    -> Renamed fields are BREAKING changes. v2 consumers reject v3 as invalid.")
print()

print("  Nugget 03-02 complete.")
print()
print("  Key takeaways:")
print("    - Backward-compatible: ADD optional fields with defaults.")
print("    - Breaking: RENAME fields, REMOVE required fields, CHANGE types.")
print("    - Include schema_version in every event for consumer branching.")
print("    - Normalize older versions to latest on consume for uniform processing.")
print()

