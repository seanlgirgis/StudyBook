"""
+==============================================================================+
|  NUGGET 02-03 . Retry and Backoff Patterns                                   |
|  Implement robust consumer retry logic with exponential backoff.             |
+==============================================================================+

CONCEPTS
--------
  Why Retry?
    Transient failures (network hiccup, downstream service temporarily down)
    should be retried. Permanent failures (malformed message, schema mismatch)
    should NOT be retried -- they belong in the Dead Letter Queue (DLQ).

  Exponential Backoff:
    Wait time doubles with each retry attempt.
    Formula: wait = base_delay * (2 ** attempt)
    Jitter (random offset): prevents thundering herd when many consumers retry.

  Retry vs. Re-queue:
    - Local retry: catch exception, sleep, retry in-process. Fast but blocks.
    - Re-queue to retry topic: publish failed message to a retry topic with
      backoff metadata. Consumer reads retry topic with delay. More robust.

  Max Retries:
    After N failures, send to Dead Letter Queue (DLQ) for manual investigation.

  Kafka producer retries (separate from consumer retries):
    - Producer has built-in retries (retries=N, retry_backoff_ms=M).
    - These handle transient broker failures during produce.

DEMONSTRATION
-------------
  1. Consumer with local exponential backoff (simulated transient error).
  2. Re-queue to retry topic after local retries exhausted.
  3. DLQ routing for permanent failures.

USAGE
-----
    python 03_retry_backoff.py
"""
from __future__ import annotations

import json
import random
import sys
import time
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _kafka_connect import BROKER, require_broker

require_broker(BROKER)

from kafka import KafkaConsumer, KafkaProducer

print("\n-- Nugget 02-03: Retry and Backoff Patterns --")
print(f"  Broker: {BROKER}")
print()

TOPIC = "lab.reliability.test"
DLQ_TOPIC = "lab.dlq"

producer = KafkaProducer(
    bootstrap_servers=BROKER,
    acks="all",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    request_timeout_ms=15_000,
)

# ─────────────────────────────────────────────────────────────────────────────
# Helper: exponential backoff with jitter
# ─────────────────────────────────────────────────────────────────────────────
def backoff_seconds(attempt: int, base: float = 0.1, cap: float = 2.0) -> float:
    """Return seconds to wait before attempt N (exponential + full jitter)."""
    exp = min(base * (2 ** attempt), cap)
    return random.uniform(0, exp)


# ─────────────────────────────────────────────────────────────────────────────
# Simulate a flaky downstream service
# ─────────────────────────────────────────────────────────────────────────────
call_count = 0
FAIL_FIRST_N = 2  # fail the first 2 calls, then succeed


def flaky_write(payload: dict) -> None:
    """Simulates a downstream service that fails transiently."""
    global call_count
    call_count += 1
    if call_count <= FAIL_FIRST_N:
        raise ConnectionError(f"Downstream service unavailable (call #{call_count})")
    # Success after FAIL_FIRST_N calls


# ─────────────────────────────────────────────────────────────────────────────
# 1. Exponential backoff with local retry
# ─────────────────────────────────────────────────────────────────────────────
print("  [1] Local retry with exponential backoff:")

MAX_RETRIES = 5
test_event = {"event_id": str(uuid.uuid4()), "data": "retry_demo_payload", "ts": int(time.time())}

attempt = 0
success = False
while attempt <= MAX_RETRIES:
    try:
        flaky_write(test_event)
        print(f"    Attempt {attempt + 1}: [OK] Write succeeded")
        success = True
        break
    except ConnectionError as exc:
        wait = backoff_seconds(attempt)
        print(f"    Attempt {attempt + 1}: [FAIL] {exc}  -- retrying in {wait:.2f}s")
        time.sleep(wait)
        attempt += 1

if not success:
    print(f"    [EXHAUSTED] All {MAX_RETRIES} retries failed -- sending to DLQ")
print()

# ─────────────────────────────────────────────────────────────────────────────
# 2. Producer retry settings (automatic broker-level retries)
# ─────────────────────────────────────────────────────────────────────────────
print("  [2] Producer built-in retries (retry_backoff_ms):")

retry_producer = KafkaProducer(
    bootstrap_servers=BROKER,
    acks="all",
    retries=5,              # retry up to 5 times on transient produce failure
    retry_backoff_ms=100,   # wait 100ms between retries (doubles each attempt)
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    request_timeout_ms=15_000,
)

for i in range(3):
    ev = {"seq": i, "producer": "retry_producer", "ts": int(time.time())}
    meta = retry_producer.send(TOPIC, value=ev).get(timeout=15)
    print(f"    Produced seq={i}  partition={meta.partition}  offset={meta.offset}")

retry_producer.flush()
retry_producer.close()
print(f"    Producer configured with retries=5, retry_backoff_ms=100")
print()

# ─────────────────────────────────────────────────────────────────────────────
# 3. DLQ routing: send unrecoverable messages to the Dead Letter Queue
# ─────────────────────────────────────────────────────────────────────────────
print("  [3] DLQ routing for permanent failures:")

# Simulate messages -- some are valid, some are "poison" (permanently bad)
mixed_events = [
    {"event_id": str(uuid.uuid4()), "value": 42,   "type": "valid"},
    {"event_id": str(uuid.uuid4()), "value": None,  "type": "poison_null"},
    {"event_id": str(uuid.uuid4()), "value": -999,  "type": "poison_negative"},
    {"event_id": str(uuid.uuid4()), "value": 100,  "type": "valid"},
]

processed_count = 0
dlq_count = 0

for ev in mixed_events:
    is_valid = ev.get("value") is not None and ev["value"] > 0
    if is_valid:
        processed_count += 1
        print(f"    PROCESS  event_id={ev['event_id'][:8]}...  value={ev['value']}")
    else:
        # Send to DLQ with failure metadata
        dlq_payload = {
            **ev,
            "dlq_reason": f"Invalid value: {ev['value']}",
            "dlq_ts": int(time.time()),
            "original_topic": TOPIC,
        }
        producer.send(DLQ_TOPIC, value=dlq_payload)
        dlq_count += 1
        print(f"    DLQ      event_id={ev['event_id'][:8]}...  reason=invalid_value({ev['value']})")

producer.flush()
producer.close()

print()
print(f"    Processed: {processed_count}  Sent to DLQ: {dlq_count}")
print()

print("  Nugget 02-03 complete.")
print()
print("  Key takeaways:")
print("    - Transient errors: retry with exponential backoff + jitter.")
print("    - Permanent errors: skip retry, send to DLQ for investigation.")
print("    - Producer retries (retries=N) handle produce-side transients.")
print("    - Consumer retries are application logic (not Kafka-native).")
print("    - DLQ pattern: always include original topic, failure reason, timestamp.")
print()
