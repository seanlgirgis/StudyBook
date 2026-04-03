"""
+==============================================================================+
|  NUGGET 02-04 . Dead Letter Topic (DLQ) Pattern                              |
|  Route, inspect, and replay failed messages.                                 |
+==============================================================================+

CONCEPTS
--------
  Dead Letter Queue (DLQ):
    A special topic where messages that cannot be processed are routed.
    Prevents a single bad message from blocking the entire pipeline.

  DLQ Message Structure:
    Always include:
      - original_topic: where the message came from
      - original_partition: partition number
      - original_offset: exact position (for replay)
      - original_key: message key
      - original_payload: the raw failed message
      - failure_reason: human-readable error description
      - failure_ts: when the failure occurred
      - retry_count: how many times processing was attempted

  DLQ Lifecycle:
    1. Consumer reads from main topic.
    2. Processing fails (after retries).
    3. Consumer publishes to DLQ with failure metadata.
    4. Consumer commits offset (moves past the failed message).
    5. DLQ monitor/alert notifies team.
    6. Team investigates, fixes logic, then replays from DLQ.

  Replay from DLQ:
    Read DLQ messages, fix the issue, then re-publish to original topic.
    The offset of the original message is lost (it was committed in step 4).

OPERATIONS COVERED
------------------
  1. Producer that sends to DLQ on failure
  2. DLQ inspector (read and display DLQ messages)
  3. DLQ replay (re-publish fixed messages to original topic)

USAGE
-----
    python 04_dead_letter_topic.py
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

print("\n-- Nugget 02-04: Dead Letter Topic (DLQ) Pattern --")
print(f"  Broker: {BROKER}")
print()

MAIN_TOPIC = "lab.reliability.test"
DLQ_TOPIC = "lab.dlq"

producer = KafkaProducer(
    bootstrap_servers=BROKER,
    acks="all",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    request_timeout_ms=15_000,
)

# ─────────────────────────────────────────────────────────────────────────────
# 1. Produce a mix of valid and bad messages to main topic
# ─────────────────────────────────────────────────────────────────────────────
print("  [1] Seeding main topic with valid + malformed messages:")

seed_events = []
for i in range(8):
    # Every 3rd message is malformed (missing required 'amount' for purchase events)
    if i % 3 == 0:
        ev = {"event_id": str(uuid.uuid4()), "type": "purchase", "user_id": f"user_{i}",
              "ts": int(time.time()), "malformed": True}
        # Missing 'amount' field -- will fail validation
    else:
        ev = {"event_id": str(uuid.uuid4()), "type": "purchase", "user_id": f"user_{i}",
              "amount": round(10.0 + i * 5.5, 2), "ts": int(time.time())}
    seed_events.append(ev)
    producer.send(MAIN_TOPIC, key=f"user_{i}".encode(), value=ev)

producer.flush()
print(f"    Seeded {len(seed_events)} messages ({sum(1 for e in seed_events if e.get('malformed'))} malformed)")
print()

# ─────────────────────────────────────────────────────────────────────────────
# 2. Consumer with DLQ routing
# ─────────────────────────────────────────────────────────────────────────────
print("  [2] Consuming with DLQ routing on validation failure:")

GROUP = f"dlq_demo_{uuid.uuid4().hex[:8]}"
consumer = KafkaConsumer(
    MAIN_TOPIC,
    bootstrap_servers=BROKER,
    group_id=GROUP,
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    consumer_timeout_ms=7_000,
    value_deserializer=safe_json_deserializer,
)

processed = 0
dlq_sent = 0

for msg in consumer:
    ev = msg.value
    try:
        # Validation: purchase events must have 'amount'
        if ev.get("type") == "purchase" and "amount" not in ev:
            raise ValueError(f"Purchase event missing 'amount': event_id={ev.get('event_id')}")
        # Simulate processing
        processed += 1
        eid = ev.get("event_id", ev.get("msg_id", "?"))
        print(f"    PROCESS  event_id={eid[:8]}...  amount={ev.get('amount')}")
        consumer.commit()

    except Exception as exc:
        eid = ev.get("event_id", ev.get("msg_id", "?")) if isinstance(ev, dict) else "?"
        # Route to DLQ with full metadata
        dlq_msg = {
            "dlq_id": str(uuid.uuid4()),
            "original_topic": msg.topic,
            "original_partition": msg.partition,
            "original_offset": msg.offset,
            "original_key": msg.key.decode("utf-8") if msg.key else None,
            "original_payload": ev,
            "failure_reason": str(exc),
            "failure_ts": int(time.time()),
            "retry_count": 0,
        }
        producer.send(DLQ_TOPIC, value=dlq_msg)
        dlq_sent += 1
        print(f"    DLQ      event_id={eid[:8]}...  reason={str(exc)[:50]}")
        consumer.commit()  # commit so we don't re-process this message

producer.flush()
consumer.close()
print()
print(f"    Processed: {processed}  Sent to DLQ: {dlq_sent}")
print()

# ─────────────────────────────────────────────────────────────────────────────
# 3. DLQ inspector: read and display DLQ messages
# ─────────────────────────────────────────────────────────────────────────────
print("  [3] DLQ Inspector -- reading failed messages:")

dlq_consumer = KafkaConsumer(
    DLQ_TOPIC,
    bootstrap_servers=BROKER,
    group_id=f"dlq_inspector_{uuid.uuid4().hex[:8]}",
    auto_offset_reset="earliest",
    consumer_timeout_ms=5_000,
    value_deserializer=safe_json_deserializer,
)

dlq_messages = []
for msg in dlq_consumer:
    dlq_messages.append(msg.value)
dlq_consumer.close()

print(f"    DLQ contains {len(dlq_messages)} message(s):")
for d in dlq_messages[-dlq_sent:]:  # show just the ones we just sent
    print(f"      dlq_id={d.get('dlq_id', '?')[:8]}...")
    print(f"        original_topic={d.get('original_topic')}  offset={d.get('original_offset')}")
    print(f"        failure_reason={d.get('failure_reason')}")
print()

# ─────────────────────────────────────────────────────────────────────────────
# 4. Replay: fix and re-publish DLQ messages
# ─────────────────────────────────────────────────────────────────────────────
print("  [4] DLQ Replay -- fix and re-publish:")
replayed = 0
for d in dlq_messages[-dlq_sent:]:
    original = d.get("original_payload", {})
    if original.get("type") == "purchase" and "amount" not in original:
        # Fix: add default amount
        fixed = {**original, "amount": 0.0, "replay_fixed": True, "replay_ts": int(time.time())}
        target_topic = d.get("original_topic", MAIN_TOPIC)
        producer.send(target_topic, value=fixed)
        replayed += 1
        print(f"    REPLAY   event_id={original.get('event_id', '?')[:8]}...  fixed_amount=0.0")

producer.flush()
producer.close()
print()
print(f"    Replayed {replayed} message(s) back to original topic with fix applied.")
print()

print("  Nugget 02-04 complete.")
print()
print("  Key takeaways:")
print("    - DLQ prevents one bad message from blocking the whole pipeline.")
print("    - Always include: original offset, topic, reason, timestamp in DLQ message.")
print("    - Commit after DLQ routing so the consumer advances past the bad message.")
print("    - Replay = read DLQ, fix the issue, re-publish to original topic.")
print("    - Set up monitoring/alerting on DLQ topic lag.")
print()

