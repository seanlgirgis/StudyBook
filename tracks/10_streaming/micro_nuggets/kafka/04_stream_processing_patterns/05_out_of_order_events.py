"""
+==============================================================================+
|  NUGGET 04-05 . Out-of-Order Event Demonstration                             |
|  Understand ordering challenges and event-time sorting strategies.           |
+==============================================================================+

CONCEPTS
--------
  Why Events Arrive Out of Order:
    - Network delays: packet from mobile device arrives 10s late.
    - Producer batching: producer buffers events, sends as batch.
    - Multi-partition: consumers read partitions in parallel -> merge is unordered.
    - Clock skew: producer device has incorrect system clock.
    - Retry with backoff: retried messages land after later messages.

  Detecting Out-of-Order Events:
    Track the maximum event_ts seen so far per key.
    If a new event has ts < max_ts, it is out of order.

  Handling Out-of-Order Events:
    1. Reorder buffer: accumulate events for T seconds, then sort and emit.
    2. Watermark: close windows only after allowed_lateness has passed.
    3. Late event side output: route to a "late" topic.
    4. Ignore ordering: for aggregations where order doesn't matter.

  Reorder Buffer:
    Collect events for a configurable delay (e.g., 5s).
    After the delay, sort by event_ts and process in order.
    Trade-off: accuracy vs. latency.

  Key-based Ordering:
    Kafka guarantees ordering within a partition.
    If you use a consistent key, all events for that key land in one partition.
    But: a single consumer per partition -> no cross-partition ordering guarantee.

DEMONSTRATION
-------------
  1. Produce events with simulated out-of-order timestamps.
  2. Detect out-of-order arrival.
  3. Apply reorder buffer (sort by event_ts within a batch).
  4. Compare arrival order vs. event_ts order.

USAGE
-----
    python 05_out_of_order_events.py
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

print("\n-- Nugget 04-05: Out-of-Order Events --")
print(f"  Broker: {BROKER}")
print()

TOPIC = "lab.raw.events"
REORDER_BUFFER_S = 10  # collect for 10s, then sort

# ─────────────────────────────────────────────────────────────────────────────
# Produce events with out-of-order timestamps
# (Kafka preserves ARRIVAL order within a partition; event_ts may be unordered)
# ─────────────────────────────────────────────────────────────────────────────
print("  Producing events with out-of-order timestamps:")

producer = KafkaProducer(
    bootstrap_servers=BROKER,
    acks="all",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda k: k.encode("utf-8") if isinstance(k, str) else k,
    request_timeout_ms=15_000,
)

now = int(time.time())
# Event timestamps: intentionally out of order (simulating network delays, clock skew)
# Arrival index -> event_ts offset from now
out_of_order_specs = [
    ("alice", now - 5),    # arrives 1st, ts=now-5
    ("alice", now - 3),    # arrives 2nd, ts=now-3 (in order)
    ("alice", now - 8),    # arrives 3rd, ts=now-8 (OUT OF ORDER -- 5s late)
    ("alice", now - 2),    # arrives 4th, ts=now-2 (in order)
    ("alice", now - 10),   # arrives 5th, ts=now-10 (OUT OF ORDER -- 8s late)
    ("alice", now),        # arrives 6th, ts=now (in order)
    ("bob",   now - 6),
    ("bob",   now - 4),
    ("bob",   now - 15),   # OUT OF ORDER for bob
    ("bob",   now - 1),
]

seeded = []
for i, (user, ev_ts) in enumerate(out_of_order_specs):
    ev = {
        "event_id":    str(uuid.uuid4()),
        "user_id":     user,
        "ts":          ev_ts,
        "arrival_idx": i,
    }
    seeded.append(ev)
    producer.send(TOPIC, key=user, value=ev)
    print(f"  Produce arrival_idx={i:2}  user={user}  ts={ev_ts}")

producer.flush()
producer.close()
print()

# ─────────────────────────────────────────────────────────────────────────────
# Consume in arrival order, detect out-of-order events
# ─────────────────────────────────────────────────────────────────────────────
print("  Consuming in arrival order, detecting out-of-order events:")

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BROKER,
    group_id=f"ooo_demo_{uuid.uuid4().hex[:8]}",
    auto_offset_reset="earliest",
    consumer_timeout_ms=6_000,
    value_deserializer=safe_json_deserializer,
)

arrived = []
for msg in consumer:
    ev = msg.value
    if "arrival_idx" in ev:
        arrived.append(ev)
consumer.close()

# Detect out-of-order per user
max_ts_per_user: dict[str, int] = {}
ooo_count = 0

print(f"  {'arrival_idx':14}  {'user':8}  {'ts':12}  {'status'}")
print(f"  {'-'*55}")

for ev in arrived:
    user = ev.get("user_id", "?")
    ts = ev.get("ts", 0)
    idx = ev.get("arrival_idx", "?")
    max_ts = max_ts_per_user.get(user, 0)
    if ts < max_ts:
        ooo_count += 1
        status = f"OUT-OF-ORDER (late by {max_ts - ts}s)"
    else:
        max_ts_per_user[user] = ts
        status = "in-order"
    print(f"  {idx!s:<14}  {user:<8}  {ts:<12}  {status}")

print()
print(f"  Out-of-order events detected: {ooo_count} / {len(arrived)}")
print()

# ─────────────────────────────────────────────────────────────────────────────
# Reorder buffer: sort by event_ts within the batch
# ─────────────────────────────────────────────────────────────────────────────
print(f"  Reorder buffer: sorting batch by event_ts:")

# Sort all arrived events by event_ts (this is the reorder buffer output)
sorted_events = sorted(arrived, key=lambda e: e["ts"])

print(f"  {'pos':6}  {'user':8}  {'ts':12}  {'arrival_idx'}")
print(f"  {'-'*42}")
for i, ev in enumerate(sorted_events):
    print(f"  {i:<6}  {ev.get('user_id', '?'):<8}  {ev.get('ts'):<12}  {ev.get('arrival_idx', '?')}")

# Check if now in order
ts_seq = [ev["ts"] for ev in sorted_events]
is_ordered = all(ts_seq[i] <= ts_seq[i+1] for i in range(len(ts_seq)-1))
print()
print(f"  After reorder buffer: globally ordered = {is_ordered}")
print()

print("  Nugget 04-05 complete.")
print()
print("  Key takeaways:")
print("    - Kafka preserves ARRIVAL order per partition, not event_ts order.")
print("    - Out-of-order: detect by tracking max_ts per key.")
print("    - Reorder buffer: collect for N seconds, sort by event_ts, then process.")
print("    - Larger buffer window = better ordering, higher latency.")
print("    - Production solution: Flink event-time processing with watermarks.")
print()

