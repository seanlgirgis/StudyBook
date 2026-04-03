"""
+==============================================================================+
|  NUGGET 02-05 . Poison Message Handling                                      |
|  Detect and safely isolate messages that crash the consumer.                 |
+==============================================================================+

CONCEPTS
--------
  Poison Message:
    A message that consistently causes the consumer to crash or hang when
    processed. Without protection, a poison message can put the consumer in
    an infinite restart loop (crash -> restart -> re-read -> crash).

  Common Poison Message Types:
    - Invalid JSON / binary garbage
    - Schema version mismatch (unknown fields, wrong types)
    - Value that triggers a bug in processing logic (division by zero, None)
    - Message that causes infinite loops in processing
    - Oversized message that exhausts memory

  Detection Strategy:
    1. Wrap processing in try/except.
    2. Track failure count per (topic, partition, offset).
    3. If failure count exceeds threshold -> route to DLQ and advance offset.

  Poison Message vs. Transient Error:
    - Transient error: succeeds on retry (network hiccup). -> Retry with backoff.
    - Poison message: fails on every retry. -> DLQ after N failures.
    The retry count distinguishes them.

DEMONSTRATION
-------------
  1. Consumer that crashes on bad input (naive -- DO NOT use in production).
  2. Hardened consumer with poison message detection.
  3. Binary garbage handling (non-UTF-8, non-JSON payload).
  4. Safe deserialization with fallback.

USAGE
-----
    python 05_poison_message_handling.py
"""
from __future__ import annotations

import json
import sys
import time
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _kafka_connect import BROKER, require_broker

require_broker(BROKER)

from kafka import KafkaConsumer, KafkaProducer

print("\n-- Nugget 02-05: Poison Message Handling --")
print(f"  Broker: {BROKER}")
print()

TOPIC = "lab.reliability.test"
DLQ_TOPIC = "lab.dlq"

# ─────────────────────────────────────────────────────────────────────────────
# Seed a mix: valid JSON, invalid JSON, valid but logic-crashing message
# ─────────────────────────────────────────────────────────────────────────────
print("  Seeding mixed valid/poison messages ...")

raw_producer = KafkaProducer(
    bootstrap_servers=BROKER,
    acks="all",
    request_timeout_ms=15_000,
)

json_producer = KafkaProducer(
    bootstrap_servers=BROKER,
    acks="all",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    request_timeout_ms=15_000,
)

# Valid JSON events
for i in range(4):
    ev = {"event_id": str(uuid.uuid4()), "value": 10 + i, "ts": int(time.time())}
    json_producer.send(TOPIC, value=ev)

# POISON 1: raw binary garbage (not decodable as UTF-8 JSON)
raw_producer.send(TOPIC, value=b"\xff\xfe\x00\x01GARBAGE")

# Valid JSON
for i in range(3):
    ev = {"event_id": str(uuid.uuid4()), "value": 20 + i, "ts": int(time.time())}
    json_producer.send(TOPIC, value=ev)

# POISON 2: valid JSON but causes logic crash (division by zero trigger)
json_producer.send(TOPIC, value={"event_id": str(uuid.uuid4()), "value": 0, "poison": True})

# More valid
for i in range(3):
    ev = {"event_id": str(uuid.uuid4()), "value": 30 + i, "ts": int(time.time())}
    json_producer.send(TOPIC, value=ev)

json_producer.flush()
raw_producer.flush()
json_producer.close()
raw_producer.close()

print("    Seeded 10 valid + 2 poison messages.")
print()

# ─────────────────────────────────────────────────────────────────────────────
# Hardened consumer: safe deser + poison detection
# ─────────────────────────────────────────────────────────────────────────────
print("  [1] Hardened consumer with poison message detection:")

dlq_producer = KafkaProducer(
    bootstrap_servers=BROKER,
    acks=1,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    request_timeout_ms=15_000,
)

failure_counts: dict[str, int] = {}  # key: "topic:partition:offset"
MAX_FAILURES = 3  # after 3 failures, send to DLQ
processed = 0
dlq_routed = 0

def safe_deserialize(raw_bytes: bytes) -> tuple[dict | None, str | None]:
    """Try to decode raw bytes as UTF-8 JSON. Return (value, error_msg)."""
    try:
        text = raw_bytes.decode("utf-8")
        return json.loads(text), None
    except UnicodeDecodeError:
        return None, f"Non-UTF-8 binary garbage ({len(raw_bytes)} bytes)"
    except json.JSONDecodeError as e:
        return None, f"Invalid JSON: {e}"


def process_event(ev: dict) -> None:
    """Simulate processing -- crashes on poison=True."""
    if ev.get("poison"):
        raise ValueError(f"Logic crash: value={ev.get('value')} is a poison trigger")
    # Normal processing
    _ = 100 / ev["value"]  # safe because value != 0 for non-poison events


consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BROKER,
    group_id=f"poison_demo_{uuid.uuid4().hex[:8]}",
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    consumer_timeout_ms=7_000,
)

for msg in consumer:
    msg_key = f"{msg.topic}:{msg.partition}:{msg.offset}"

    # Safe deserialization
    value, deser_error = safe_deserialize(msg.value)
    if deser_error:
        # Binary garbage -- no point retrying, send straight to DLQ
        dlq_payload = {
            "dlq_id": str(uuid.uuid4()),
            "original_topic": msg.topic,
            "original_partition": msg.partition,
            "original_offset": msg.offset,
            "original_payload_hex": msg.value[:32].hex(),
            "failure_reason": deser_error,
            "failure_ts": int(time.time()),
            "retry_count": 0,
        }
        dlq_producer.send(DLQ_TOPIC, value=dlq_payload)
        dlq_routed += 1
        print(f"    DLQ(deser)  offset={msg.offset}  reason={deser_error}")
        consumer.commit()
        continue

    # Track failure count per message position
    failure_counts.setdefault(msg_key, 0)

    try:
        process_event(value)
        processed += 1
        print(f"    PROCESS     offset={msg.offset}  event_id={value.get('event_id', '?')[:8]}...  value={value.get('value')}")
        consumer.commit()

    except Exception as exc:
        failure_counts[msg_key] += 1
        if failure_counts[msg_key] >= MAX_FAILURES:
            # Poison message confirmed -- send to DLQ
            dlq_payload = {
                "dlq_id": str(uuid.uuid4()),
                "original_topic": msg.topic,
                "original_partition": msg.partition,
                "original_offset": msg.offset,
                "original_payload": value,
                "failure_reason": str(exc),
                "failure_ts": int(time.time()),
                "retry_count": failure_counts[msg_key],
            }
            dlq_producer.send(DLQ_TOPIC, value=dlq_payload)
            dlq_routed += 1
            print(f"    DLQ(poison) offset={msg.offset}  after {failure_counts[msg_key]} failures: {exc}")
            consumer.commit()  # advance past the poison message
        else:
            print(f"    RETRY({failure_counts[msg_key]})     offset={msg.offset}  {exc}")
            # In a real system: sleep + poll again (or re-seek to this offset)
            # For demo: just try again immediately via loop
            from kafka import TopicPartition as _TP
            consumer.seek(_TP(msg.topic, msg.partition), msg.offset)  # seek back for retry

dlq_producer.flush()
dlq_producer.close()
consumer.close()

print()
print(f"    Processed: {processed}  DLQ: {dlq_routed}")
print()

print("  Nugget 02-05 complete.")
print()
print("  Key takeaways:")
print("    - Always wrap deserialization in try/except -- never trust raw bytes.")
print("    - Track (topic, partition, offset) failure count to detect poison messages.")
print("    - After N failures, commit and route to DLQ (don't loop forever).")
print("    - Binary garbage: skip retry immediately and DLQ.")
print("    - Add consumer.seek() to retry the same offset before committing.")
print()
