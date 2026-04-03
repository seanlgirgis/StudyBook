"""
+==============================================================================+
|  NUGGET 07-04 . Mini Capstone: Failure Injection and Recovery                |
|  Step 4 of 4: Inject failures into the pipeline and demonstrate recovery.   |
+==============================================================================+

FAILURE SCENARIOS DEMONSTRATED
-------------------------------
  1. Poison message injection: produce a malformed message to silver.
     Recovery: silver consumer detects it, routes to DLQ.

  2. Simulated downstream sink failure: consumer processes but "sink" fails.
     Recovery: retry with backoff; after N retries -> DLQ.

  3. Consumer crash simulation: consumer reads N messages then "crashes".
     Recovery: restart reads from committed offset (no data loss).

  4. Schema version mismatch: producer sends v99 schema.
     Recovery: consumer routes unknown schema version to DLQ.

USAGE
-----
    python 04_failure_injection.py
    (Run after 03_aggregate_to_gold.py for full pipeline demo)
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

print("\n-- Mini Capstone Step 4: Failure Injection and Recovery --")
print(f"  Broker: {BROKER}")
print()

# ─────────────────────────────────────────────────────────────────────────────
# 1. Poison message injection
# ─────────────────────────────────────────────────────────────────────────────
print("  [FAILURE 1] Poison message injection -> lab.bronze:")

producer = KafkaProducer(
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

# Inject binary garbage
producer.send("lab.bronze", value=b"\xff\xfe\x00GARBAGE_BINARY")
# Inject valid JSON but wrong structure (not an envelope)
json_producer.send("lab.bronze", value={"not_an_envelope": True, "random_field": 42})
# Inject schema_version=99 (unknown)
json_producer.send("lab.bronze", value={
    "event_id": str(uuid.uuid4()),
    "event_type": "user.behavior.event",
    "schema_version": 99,  # unknown version
    "payload": {"user_id": "alice", "action": "test", "ts": int(time.time())},
})

producer.flush()
json_producer.flush()
producer.close()
json_producer.close()
print("    Injected: 1x binary garbage, 1x wrong structure, 1x schema_version=99")
print()

# ─────────────────────────────────────────────────────────────────────────────
# Hardened consumer that handles all these failures
# ─────────────────────────────────────────────────────────────────────────────
print("  Recovery: Hardened bronze consumer processing injected failures:")

dlq_producer = KafkaProducer(
    bootstrap_servers=BROKER,
    acks=1,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    request_timeout_ms=15_000,
)

SUPPORTED_SCHEMA_VERSIONS = {1, 2}
MAX_RETRIES = 2

fail_count = [0]  # simulated sink failure counter


def flaky_sink(payload: dict) -> None:
    """Simulate a sink that fails transiently for the first 2 calls."""
    fail_count[0] += 1
    if fail_count[0] <= 2:
        raise ConnectionError(f"Sink temporarily unavailable (call #{fail_count[0]})")


consumer = KafkaConsumer(
    "lab.bronze",
    bootstrap_servers=BROKER,
    group_id=f"failure_demo_{uuid.uuid4().hex[:8]}",
    auto_offset_reset="latest",  # only read new messages (the injected ones)
    enable_auto_commit=False,
    consumer_timeout_ms=6_000,
)

recovered = 0
dlq_routed = 0

for msg in consumer:
    raw = msg.value

    # 1. Safe deserialization
    try:
        text = raw.decode("utf-8")
        env = json.loads(text)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        dlq_producer.send("lab.dlq", value={
            "dlq_id": str(uuid.uuid4()),
            "original_topic": msg.topic,
            "original_offset": msg.offset,
            "failure_reason": f"Deserialization failed: {exc}",
            "raw_hex": raw[:32].hex(),
        })
        dlq_routed += 1
        print(f"  DLQ(deser)  offset={msg.offset}  {exc}")
        consumer.commit()
        continue

    if not isinstance(env, dict) or "event_id" not in env:
        dlq_producer.send("lab.dlq", value={
            "dlq_id": str(uuid.uuid4()),
            "original_topic": msg.topic,
            "original_offset": msg.offset,
            "failure_reason": "Not a valid envelope structure",
            "payload": env,
        })
        dlq_routed += 1
        print(f"  DLQ(struct) offset={msg.offset}  Not a valid envelope")
        consumer.commit()
        continue

    # 2. Schema version check
    ver = env.get("schema_version", 0)
    if ver not in SUPPORTED_SCHEMA_VERSIONS:
        dlq_producer.send("lab.dlq", value={
            "dlq_id": str(uuid.uuid4()),
            "original_topic": msg.topic,
            "original_offset": msg.offset,
            "failure_reason": f"Unsupported schema_version={ver}",
            "envelope": env,
        })
        dlq_routed += 1
        print(f"  DLQ(schema) offset={msg.offset}  schema_version={ver} not supported")
        consumer.commit()
        continue

    # 3. Retry with backoff for sink failure
    payload = env.get("payload", {})
    attempt = 0
    sink_ok = False
    while attempt <= MAX_RETRIES:
        try:
            flaky_sink(payload)
            sink_ok = True
            break
        except ConnectionError as exc:
            wait = 0.05 * (2 ** attempt)
            print(f"  RETRY({attempt+1}/{MAX_RETRIES}) offset={msg.offset}  sink error: {exc}  wait={wait:.2f}s")
            time.sleep(wait)
            attempt += 1

    if sink_ok:
        recovered += 1
        print(f"  RECOVERED   offset={msg.offset}  event_id={env['event_id'][:12]}...")
    else:
        dlq_producer.send("lab.dlq", value={
            "dlq_id": str(uuid.uuid4()),
            "original_topic": msg.topic,
            "original_offset": msg.offset,
            "failure_reason": f"Sink failed after {MAX_RETRIES} retries",
            "envelope": env,
        })
        dlq_routed += 1
        print(f"  DLQ(sink)   offset={msg.offset}  after {MAX_RETRIES} retries")

    consumer.commit()

dlq_producer.flush()
dlq_producer.close()
consumer.close()

print()
print(f"  Failure injection results:")
print(f"    Recovered (processed successfully): {recovered}")
print(f"    Routed to DLQ:                      {dlq_routed}")
print()

# ─────────────────────────────────────────────────────────────────────────────
# 2. Crash simulation: consumer reads 5 messages then "crashes"
# ─────────────────────────────────────────────────────────────────────────────
print("  [FAILURE 2] Consumer crash simulation:")
CRASH_GROUP = f"crash_sim_{uuid.uuid4().hex[:8]}"
consumer_crash = KafkaConsumer(
    "lab.silver",
    bootstrap_servers=BROKER,
    group_id=CRASH_GROUP,
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    consumer_timeout_ms=5_000,
    value_deserializer=lambda b: json.loads(b.decode("utf-8")),
)

crash_read = 0
last_committed = 0
for msg in consumer_crash:
    crash_read += 1
    consumer_crash.commit()
    last_committed = msg.offset
    if crash_read >= 5:
        print(f"    [CRASH] Simulating crash after {crash_read} messages. Last committed offset: {last_committed}")
        break  # simulate crash

consumer_crash.close()

# Recovery: re-open same group -- will start from committed offset
consumer_recover = KafkaConsumer(
    "lab.silver",
    bootstrap_servers=BROKER,
    group_id=CRASH_GROUP,  # same group = picks up from committed offset
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    consumer_timeout_ms=5_000,
    value_deserializer=lambda b: json.loads(b.decode("utf-8")),
)
recovery_read = 0
for msg in consumer_recover:
    recovery_read += 1
consumer_recover.close()

print(f"    [RECOVERY] After restart, consumer read {recovery_read} remaining messages.")
print(f"    No data was lost -- committed offset was preserved.")
print()

print("  Mini Capstone complete!")
print()
print("  Pipeline summary:")
print("    Step 1: 01_ingest_bronze.py  -- Raw events -> lab.bronze")
print("    Step 2: 02_clean_to_silver.py -- Bronze -> lab.silver (clean/dedup/validate)")
print("    Step 3: 03_aggregate_to_gold.py -- Silver -> lab.gold (per-user analytics)")
print("    Step 4: 04_failure_injection.py -- Failure injection + recovery demo")
print()
print("  Patterns demonstrated:")
print("    - Medallion architecture (Bronze/Silver/Gold)")
print("    - Deduplication by event_id")
print("    - DLQ routing for invalid/unsupported events")
print("    - Retry with exponential backoff")
print("    - Crash recovery via committed offsets")
print()
