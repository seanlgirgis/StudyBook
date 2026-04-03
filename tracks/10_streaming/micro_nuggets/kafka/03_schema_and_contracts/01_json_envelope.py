"""
+==============================================================================+
|  NUGGET 03-01 . JSON Event Envelope Standards                                |
|  Establish a consistent event envelope for all Kafka messages.               |
+==============================================================================+

CONCEPTS
--------
  Event Envelope:
    A standardized wrapper around every Kafka message payload.
    Separates metadata (routing, versioning, tracing) from the business payload.

  Why Envelopes?
    - Schema evolution: add fields to envelope without breaking consumers.
    - Routing: consumers inspect envelope type/version before deserializing payload.
    - Observability: every event carries trace_id, source, schema_version.
    - DLQ: envelope fields help diagnose failures without decoding payload.

  Standard Envelope Fields:
    event_id:       UUID, unique per event -- used for deduplication.
    event_type:     String, namespaced (e.g., "commerce.order.placed").
    schema_version: Integer -- allows consumers to handle multiple versions.
    source_service: Which microservice emitted this event.
    produced_at:    ISO-8601 UTC timestamp when event was created.
    trace_id:       Distributed tracing ID for cross-service correlation.
    payload:        The actual business data (nested JSON object).

  Event Type Naming Convention:
    domain.entity.action  (e.g., "commerce.order.placed", "user.profile.updated")
    This makes routing rules and filtering straightforward.

OPERATIONS COVERED
------------------
  1. Define and validate envelope schema
  2. Produce events with standard envelope
  3. Consume and route events by type
  4. Backward-compatible envelope evolution

USAGE
-----
    python 01_json_envelope.py
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

print("\n-- Nugget 03-01: JSON Event Envelope Standards --")
print(f"  Broker: {BROKER}")
print()

TOPIC = "lab.raw.events"

# ─────────────────────────────────────────────────────────────────────────────
# 1. Envelope builder
# ─────────────────────────────────────────────────────────────────────────────
def make_envelope(
    event_type: str,
    payload: dict[str, Any],
    source_service: str = "lab_nugget",
    schema_version: int = 1,
    trace_id: str | None = None,
) -> dict:
    """
    Build a standard event envelope.
    Every Kafka message in this lane follows this structure.
    """
    return {
        "event_id":       str(uuid.uuid4()),
        "event_type":     event_type,
        "schema_version": schema_version,
        "source_service": source_service,
        "produced_at":    datetime.now(timezone.utc).isoformat(),
        "trace_id":       trace_id or str(uuid.uuid4()),
        "payload":        payload,
    }


REQUIRED_ENVELOPE_FIELDS = {
    "event_id", "event_type", "schema_version", "source_service", "produced_at", "payload"
}

def validate_envelope(msg: dict) -> list[str]:
    """Return list of validation errors. Empty list = valid."""
    errors = []
    missing = REQUIRED_ENVELOPE_FIELDS - set(msg.keys())
    if missing:
        errors.append(f"Missing required fields: {missing}")
    if "schema_version" in msg and not isinstance(msg["schema_version"], int):
        errors.append("schema_version must be an integer")
    if "event_id" in msg:
        try:
            uuid.UUID(msg["event_id"])
        except ValueError:
            errors.append("event_id must be a valid UUID")
    return errors


print("  [1] Envelope builder + validation:")
sample_envelope = make_envelope(
    event_type="commerce.order.placed",
    payload={"order_id": "ORD-9001", "user_id": "alice", "amount": 99.99},
    source_service="order_service",
)
errors = validate_envelope(sample_envelope)
print(f"    Envelope keys: {list(sample_envelope.keys())}")
print(f"    Validation errors: {errors if errors else 'none'}")
print(f"    event_type: {sample_envelope['event_type']}")
print(f"    schema_version: {sample_envelope['schema_version']}")
print()

# ─────────────────────────────────────────────────────────────────────────────
# 2. Produce diverse event types with standard envelope
# ─────────────────────────────────────────────────────────────────────────────
print("  [2] Producing enveloped events:")

producer = KafkaProducer(
    bootstrap_servers=BROKER,
    acks="all",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda k: k.encode("utf-8") if isinstance(k, str) else k,
    request_timeout_ms=15_000,
)

event_definitions = [
    ("commerce.order.placed",    "alice", {"order_id": "ORD-1", "amount": 49.99, "items": 2}),
    ("commerce.order.cancelled", "alice", {"order_id": "ORD-1", "reason": "changed_mind"}),
    ("user.profile.updated",     "bob",   {"field": "email", "new_value": "bob@example.com"}),
    ("commerce.order.placed",    "carol", {"order_id": "ORD-2", "amount": 149.00, "items": 5}),
    ("analytics.page.viewed",    "dave",  {"page": "/products", "duration_s": 12}),
]

sent_events = []
for event_type, user_id, payload in event_definitions:
    env = make_envelope(event_type=event_type, payload=payload, source_service="order_service")
    meta = producer.send(TOPIC, key=user_id, value=env).get(timeout=10)
    sent_events.append(env)
    print(f"    Sent type={event_type:35}  partition={meta.partition}  offset={meta.offset}")

producer.flush()
producer.close()
print()

# ─────────────────────────────────────────────────────────────────────────────
# 3. Consumer: route by event_type
# ─────────────────────────────────────────────────────────────────────────────
print("  [3] Consuming and routing by event_type:")

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BROKER,
    group_id=f"envelope_demo_{uuid.uuid4().hex[:8]}",
    auto_offset_reset="earliest",
    consumer_timeout_ms=6_000,
    value_deserializer=safe_json_deserializer,
)

routed: dict[str, int] = {}
validation_failures = 0

for msg in consumer:
    env = msg.value
    if not isinstance(env, dict):
        continue
    errs = validate_envelope(env)
    if errs:
        validation_failures += 1
        continue
    etype = env.get("event_type", "unknown")
    domain = etype.split(".")[0]  # "commerce", "user", "analytics"
    routed[domain] = routed.get(domain, 0) + 1

consumer.close()

print(f"    Routing summary:")
for domain, count in sorted(routed.items()):
    print(f"      domain={domain:12}  messages={count}")
print(f"    Validation failures: {validation_failures}")
print()

print("  Nugget 03-01 complete.")
print()
print("  Key takeaways:")
print("    - Every event should carry: event_id, event_type, schema_version, produced_at.")
print("    - event_id enables deduplication; trace_id enables distributed tracing.")
print("    - Route consumers by event_type (or domain prefix) for separation of concerns.")
print("    - Validate envelope on consume, not just on produce.")
print()

