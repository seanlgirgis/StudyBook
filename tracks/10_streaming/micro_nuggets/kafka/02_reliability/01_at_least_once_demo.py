"""
+==============================================================================+
|  NUGGET 02-01 . At-Least-Once Semantics Demo                                 |
|  Understand delivery guarantees and how duplicates arise.                    |
+==============================================================================+

CONCEPTS
--------
  Delivery Semantics:

  At-most-once:
    - Producer fires and forgets (acks=0 or no retry).
    - Messages may be LOST if the broker crashes between produce and ACK.
    - No duplicates, but data loss is possible.
    - Use case: metrics where occasional loss is acceptable.

  At-least-once:
    - Producer retries on failure (acks="all", retries > 0).
    - The consumer commits AFTER successfully processing.
    - If the consumer crashes after processing but before commit, the message
      is re-delivered -> consumer must handle DUPLICATES.
    - This is the default Kafka pattern. Most DE pipelines use this.

  Exactly-once:
    - Requires both idempotent producer AND transactional producer+consumer.
    - Complex to implement. Supported natively in Kafka >= 0.11.
    - kafka-python has partial support; full exactly-once needs confluent-kafka.

  How duplicates arise in at-least-once:
    1. Producer sends message.
    2. Broker receives and stores it.
    3. Producer doesn't receive ACK (network timeout).
    4. Producer retries -> broker stores ANOTHER copy.
    5. Consumer reads BOTH copies.

DEMONSTRATION
-------------
  Simulate the at-least-once scenario by:
  1. Producing the same message twice (simulating a retry).
  2. Consuming and counting duplicates.
  3. Deduplicating by event_id (the correct fix).

USAGE
-----
    python 01_at_least_once_demo.py
"""
from __future__ import annotations

import json
import sys
import time
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _kafka_connect import BROKER, require_broker, safe_json_deserializer

require_broker(BROKER)

from kafka import KafkaConsumer, KafkaProducer

print("\n-- Nugget 02-01: At-Least-Once Semantics Demo --")
print(f"  Broker: {BROKER}")
print()

TOPIC = "lab.reliability.test"

producer = KafkaProducer(
    bootstrap_servers=BROKER,
    acks="all",
    retries=3,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    request_timeout_ms=15_000,
)

# ─────────────────────────────────────────────────────────────────────────────
# 1. Produce a set of "normal" events
# ─────────────────────────────────────────────────────────────────────────────
print("  [1] Producing 10 normal events ...")
normal_events = []
ts = int(time.time())
for i in range(10):
    ev = {
        "event_id": str(uuid.uuid4()),
        "seq": i,
        "ts": ts + i,
        "type": "normal",
    }
    normal_events.append(ev)
    producer.send(TOPIC, value=ev)

producer.flush()
print(f"    Sent {len(normal_events)} events.")
print()

# ─────────────────────────────────────────────────────────────────────────────
# 2. Simulate at-least-once: send same event twice (retry scenario)
# ─────────────────────────────────────────────────────────────────────────────
print("  [2] Simulating retry (duplicate) -- same event_id sent twice:")
duplicate_event = {
    "event_id": "FIXED-ID-DEMO-DUPLICATE-0001",
    "seq": 99,
    "ts": ts + 100,
    "type": "retry_duplicate",
}

print(f"    Sending event_id={duplicate_event['event_id']} TWICE (simulates network retry)")
producer.send(TOPIC, value=duplicate_event)
producer.send(TOPIC, value=duplicate_event)  # exact same message again
producer.flush()
print()

# ─────────────────────────────────────────────────────────────────────────────
# 3. Consume and detect duplicates
# ─────────────────────────────────────────────────────────────────────────────
print("  [3] Consuming and detecting duplicates:")
GROUP = f"at_least_once_demo_{uuid.uuid4().hex[:8]}"

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BROKER,
    group_id=GROUP,
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    consumer_timeout_ms=6_000,
    value_deserializer=safe_json_deserializer,
)

seen_ids: dict[str, int] = {}
all_msgs = []
for msg in consumer:
    v = msg.value
    eid = v.get("event_id", "no-id")
    seen_ids[eid] = seen_ids.get(eid, 0) + 1
    all_msgs.append(v)
    consumer.commit()  # commit AFTER processing (at-least-once)
consumer.close()

total = len(all_msgs)
unique = len(seen_ids)
duplicates = {k: v for k, v in seen_ids.items() if v > 1}

print(f"    Total messages consumed: {total}")
print(f"    Unique event_ids:        {unique}")
print(f"    Duplicate event_ids:     {len(duplicates)}")
for eid, count in duplicates.items():
    print(f"      {eid}: seen {count}x")
print()

# ─────────────────────────────────────────────────────────────────────────────
# 4. Deduplication fix: track seen event_ids
# ─────────────────────────────────────────────────────────────────────────────
print("  [4] Deduplication fix (in-memory seen set):")
deduped = []
dedup_set: set[str] = set()
for v in all_msgs:
    eid = v.get("event_id", "no-id")
    if eid not in dedup_set:
        dedup_set.add(eid)
        deduped.append(v)

print(f"    After dedup: {len(deduped)} unique messages (dropped {total - len(deduped)} duplicates)")
print()

producer.close()

print("  Nugget 02-01 complete.")
print()
print("  Key takeaways:")
print("    - At-least-once = retries enabled + commit after processing.")
print("    - Duplicates are EXPECTED in at-least-once. Your consumer must handle them.")
print("    - Dedup by event_id (UUID) is the standard fix.")
print("    - Production dedup: use Redis SET, DynamoDB, or DB upsert on event_id.")
print("    - Exactly-once requires transactional API (complex; often not worth it).")
print()

