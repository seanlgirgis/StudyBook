"""
+==============================================================================+
|  NUGGET 01-02 . Producer Basics                                              |
|  Keys, partitioning strategy, acks, batching, and callbacks.                 |
+==============================================================================+

CONCEPTS
--------
  Producer:
    Publishes records to a Kafka topic. Each record has:
      - key   (optional bytes) -- used to determine partition assignment
      - value (bytes)          -- the actual message payload
      - timestamp              -- event time or broker ingestion time

  Partitioning Strategy:
    - key=None  -> round-robin across partitions (load balanced, no ordering)
    - key=bytes -> consistent hash (murmur2) -> same key always same partition
                   IMPORTANT: this guarantees ordering per key within a topic.
    - custom partitioner: implement __call__(key, partitions, available) -> int

  Acks (Acknowledgment Level):
    - acks=0   : fire-and-forget. Fastest, no durability guarantee.
    - acks=1   : leader ACKs before ISR replicas. Moderate durability.
    - acks="all" (or -1): all ISR replicas ACK. Strongest durability.

  Batching:
    - linger_ms: producer waits this long to accumulate a batch before sending.
    - batch_size: max bytes per batch (default 16 KB).
    - Higher linger_ms = better throughput, higher latency.

OPERATIONS COVERED
------------------
  1. Basic produce (no key, raw bytes)
  2. Produce with key -> partitioning
  3. JSON-serialized produce
  4. Produce with delivery callback (on_send_success / on_send_error)
  5. Batch send with flush

USAGE
-----
    python 02_producer_basics.py
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

from kafka import KafkaProducer
from kafka.errors import KafkaError

print("\n-- Nugget 01-02: Producer Basics --")
print(f"  Broker: {BROKER}")
print()

# ─────────────────────────────────────────────────────────────────────────────
# 1. Basic produce -- raw bytes, no key
#    Without a key, messages are distributed round-robin across partitions.
#    No ordering guarantee across partitions.
# ─────────────────────────────────────────────────────────────────────────────
print("  [1] Basic produce (no key, raw bytes):")

producer = KafkaProducer(
    bootstrap_servers=BROKER,
    acks="all",          # wait for all ISR replicas
    retries=3,
    linger_ms=0,         # send immediately (no batching delay for demo)
    request_timeout_ms=15_000,
)

import json as _json
future = producer.send("lab.raw.events", value=_json.dumps({"msg": "hello from producer_basics"}).encode())
record_meta = future.get(timeout=10)
print(f"    Sent to topic={record_meta.topic}  "
      f"partition={record_meta.partition}  offset={record_meta.offset}")
print()

# ─────────────────────────────────────────────────────────────────────────────
# 2. Produce WITH key -> deterministic partition assignment
#    The same key always lands on the same partition (using murmur2 hash).
#    This is how Kafka guarantees ordering per key (e.g., per user_id).
# ─────────────────────────────────────────────────────────────────────────────
print("  [2] Produce with key -> deterministic partition:")
keys = ["alice", "bob", "carol"]
for user_id in keys:
    for i in range(3):
        payload = f"event_{i}_for_{user_id}".encode()
        future = producer.send(
            "lab.orders",
            key=user_id.encode("utf-8"),
            value=payload,
        )
        meta = future.get(timeout=10)
        print(f"    key={user_id:8}  partition={meta.partition}  offset={meta.offset}")

print()
print("    Observation: same key always -> same partition number.")
print()

# ─────────────────────────────────────────────────────────────────────────────
# 3. JSON-serialized produce (most common pattern in Data Engineering)
# ─────────────────────────────────────────────────────────────────────────────
print("  [3] JSON-serialized events:")

json_producer = KafkaProducer(
    bootstrap_servers=BROKER,
    acks="all",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda k: k.encode("utf-8") if isinstance(k, str) else k,
    request_timeout_ms=15_000,
)

events = [
    {"event_id": str(uuid.uuid4()), "user_id": "alice", "action": "purchase", "amount": 42.99, "ts": int(time.time())},
    {"event_id": str(uuid.uuid4()), "user_id": "bob",   "action": "search",   "query": "kafka", "ts": int(time.time())},
    {"event_id": str(uuid.uuid4()), "user_id": "carol", "action": "page_view","page": "/home",  "ts": int(time.time())},
]

for ev in events:
    future = json_producer.send("lab.raw.events", key=ev["user_id"], value=ev)
    meta = future.get(timeout=10)
    print(f"    Sent event_id={ev['event_id'][:8]}...  action={ev['action']:10}  "
          f"partition={meta.partition}  offset={meta.offset}")

print()

# ─────────────────────────────────────────────────────────────────────────────
# 4. Delivery callback (async fire-and-forget with callback)
#    Instead of future.get() (blocking), attach callbacks.
#    In production: use fire-and-forget with callbacks + flush at end of batch.
# ─────────────────────────────────────────────────────────────────────────────
print("  [4] Delivery callbacks (async pattern):")

delivered: list[dict] = []
errors: list[str] = []


def on_success(metadata) -> None:
    delivered.append({
        "topic": metadata.topic,
        "partition": metadata.partition,
        "offset": metadata.offset,
    })


def on_error(excp) -> None:
    errors.append(str(excp))


for i in range(5):
    event = {"seq": i, "ts": int(time.time()), "event_id": str(uuid.uuid4())}
    json_producer.send("lab.clickstream", value=event).add_callback(on_success).add_errback(on_error)

# flush() blocks until all pending sends are complete and callbacks fired
json_producer.flush()

print(f"    Delivered {len(delivered)} messages, errors: {len(errors)}")
for d in delivered:
    print(f"      partition={d['partition']}  offset={d['offset']}")
print()

# ─────────────────────────────────────────────────────────────────────────────
# 5. Batch throughput demo: linger_ms batching
#    linger_ms=50 means: wait up to 50 ms to accumulate messages before sending.
#    Better throughput for high-volume producers.
# ─────────────────────────────────────────────────────────────────────────────
print("  [5] Batch throughput (linger_ms=50):")

batch_producer = KafkaProducer(
    bootstrap_servers=BROKER,
    acks=1,
    linger_ms=50,
    batch_size=16_384,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    request_timeout_ms=15_000,
)

t0 = time.perf_counter()
BATCH_SIZE = 100
for i in range(BATCH_SIZE):
    batch_producer.send("lab.raw.events", value={"seq": i, "ts": int(time.time())})

batch_producer.flush()
elapsed = time.perf_counter() - t0
rate = BATCH_SIZE / elapsed
print(f"    Sent {BATCH_SIZE} messages in {elapsed:.3f}s  ({rate:.0f} msg/s)")

# Cleanup
producer.close()
json_producer.close()
batch_producer.close()

print()
print("  Nugget 01-02 complete.")
print()
print("  Key takeaways:")
print("    - Key determines partition -> ordering guarantee per key.")
print("    - acks='all' is the safest setting (all ISR must confirm).")
print("    - Use value_serializer to avoid encoding every message manually.")
print("    - Callbacks + flush() enable high-throughput async producing.")
print()
