"""
+==============================================================================+
|  NUGGET 05-03 . Partition Skew Detection                                     |
|  Detect and diagnose uneven message distribution across partitions.          |
+==============================================================================+

CONCEPTS
--------
  Partition Skew:
    When some partitions receive significantly more messages than others.
    This causes certain consumers (each owning one partition) to fall behind
    while others sit idle.

  Causes of Partition Skew:
    1. Hot key: one message key (e.g., "alice") accounts for 80% of traffic.
       All alice events land on the same partition.
    2. Custom partitioner: poor hashing leads to uneven distribution.
    3. Null key: unkeyed messages use round-robin, which is usually balanced.
    4. Temporal skew: bursty producers flood one partition temporarily.

  Detecting Skew:
    - Compare message counts across partitions.
    - Skew ratio = max_partition_count / avg_partition_count
    - Skew > 2x is noticeable. Skew > 5x is problematic.

  Fixing Partition Skew:
    1. Composite key: instead of user_id alone, use user_id + timestamp_bucket.
       This spreads a hot user across multiple partitions.
    2. Random key or null key: distribute without ordering requirement.
    3. Increase partition count: more partitions = finer-grained distribution.
    4. Custom partitioner: route based on estimated load.

DEMONSTRATION
-------------
  1. Produce hot-key events (simulate skew).
  2. Count messages per partition.
  3. Calculate skew metrics.
  4. Show composite key fix.

USAGE
-----
    python 03_partition_skew.py
"""
from __future__ import annotations

import json
import sys
import time
import uuid
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _kafka_connect import BROKER, require_broker

require_broker(BROKER)

from kafka import KafkaAdminClient, KafkaConsumer, KafkaProducer, TopicPartition
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError

print("\n-- Nugget 05-03: Partition Skew Detection --")
print(f"  Broker: {BROKER}")
print()

SKEW_TOPIC = "lab.demo.skew_test"
PARTITIONS = 4

admin = KafkaAdminClient(bootstrap_servers=BROKER, request_timeout_ms=15_000)
try:
    admin.create_topics([NewTopic(name=SKEW_TOPIC, num_partitions=PARTITIONS, replication_factor=1)])
except TopicAlreadyExistsError:
    pass
admin.close()

# ─────────────────────────────────────────────────────────────────────────────
# 1. Produce with hot-key skew (alice dominates)
# ─────────────────────────────────────────────────────────────────────────────
print("  [1] Producing with hot-key skew:")
print(f"    Traffic split: alice=60%, bob=25%, carol=10%, dave=5%")

producer = KafkaProducer(
    bootstrap_servers=BROKER,
    acks="all",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda k: k.encode("utf-8") if isinstance(k, str) else k,
    request_timeout_ms=15_000,
)

# Hot key distribution
traffic = (
    [("alice", 60)] +
    [("bob",   25)] +
    [("carol", 10)] +
    [("dave",   5)]
)
ts = int(time.time())
events_sent = []
for user, count in traffic:
    for i in range(count):
        ev = {"event_id": str(uuid.uuid4()), "user_id": user, "ts": ts + i}
        producer.send(SKEW_TOPIC, key=user, value=ev)
        events_sent.append((user, ev))

producer.flush()
producer.close()
print(f"    Sent {len(events_sent)} events (100 total).")
print()

# ─────────────────────────────────────────────────────────────────────────────
# 2. Consume and count messages per partition
# ─────────────────────────────────────────────────────────────────────────────
print("  [2] Counting messages per partition:")

consumer = KafkaConsumer(
    SKEW_TOPIC,
    bootstrap_servers=BROKER,
    group_id=f"skew_check_{uuid.uuid4().hex[:8]}",
    auto_offset_reset="earliest",
    consumer_timeout_ms=6_000,
    value_deserializer=lambda b: json.loads(b.decode("utf-8")),
)

partition_counts: dict[int, int] = defaultdict(int)
user_partition: dict[str, set] = defaultdict(set)

for msg in consumer:
    partition_counts[msg.partition] += 1
    if isinstance(msg.value, dict):
        user_partition[msg.value.get("user_id", "?")].add(msg.partition)

consumer.close()

# ─────────────────────────────────────────────────────────────────────────────
# 3. Skew metrics
# ─────────────────────────────────────────────────────────────────────────────
print(f"  {'partition':10}  {'message_count':14}  {'pct':8}  bar")
print(f"  {'-'*50}")

total = sum(partition_counts.values())
for p in range(PARTITIONS):
    count = partition_counts.get(p, 0)
    pct = count / total * 100 if total else 0
    bar = "#" * (count // 3)
    print(f"  {p:<10}  {count:<14}  {pct:<8.1f}  {bar}")

print()
print(f"  User -> Partition mapping:")
for user, partitions in sorted(user_partition.items()):
    print(f"    {user:<8} -> partitions {sorted(partitions)}")

if partition_counts:
    max_count = max(partition_counts.values())
    min_count = min(partition_counts.values()) if any(v > 0 for v in partition_counts.values()) else 0
    avg_count = total / PARTITIONS
    skew_ratio = max_count / avg_count if avg_count > 0 else 1.0
    print()
    print(f"  Skew metrics:")
    print(f"    max_partition={max_count}  min={min_count}  avg={avg_count:.1f}  skew_ratio={skew_ratio:.2f}x")
    if skew_ratio > 3:
        print(f"    [WARN] Skew ratio {skew_ratio:.1f}x exceeds 3x threshold!")
    elif skew_ratio > 1.5:
        print(f"    [INFO] Moderate skew ({skew_ratio:.1f}x). Monitor for consumer lag.")
    else:
        print(f"    [OK] Skew within acceptable range.")

print()

# ─────────────────────────────────────────────────────────────────────────────
# 4. Fix: composite key to spread hot user
# ─────────────────────────────────────────────────────────────────────────────
print("  [4] Fix: composite key = user_id + bucket (spreads hot key):")

producer2 = KafkaProducer(
    bootstrap_servers=BROKER,
    acks="all",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda k: k.encode("utf-8") if isinstance(k, str) else k,
    request_timeout_ms=15_000,
)

composite_partition_counts: dict[int, int] = defaultdict(int)
N_BUCKETS = PARTITIONS  # spread across N buckets

for i in range(60):  # only alice's events
    bucket = i % N_BUCKETS
    composite_key = f"alice_{bucket}"  # alice_0, alice_1, alice_2, alice_3
    ev = {"event_id": str(uuid.uuid4()), "user_id": "alice", "bucket": bucket, "ts": ts + i}
    meta = producer2.send(SKEW_TOPIC, key=composite_key, value=ev).get(timeout=10)
    composite_partition_counts[meta.partition] += 1

producer2.flush()
producer2.close()

print(f"  Composite key partition distribution (alice's traffic):")
for p in range(PARTITIONS):
    count = composite_partition_counts.get(p, 0)
    bar = "#" * count
    print(f"    partition={p}  count={count:<4}  {bar}")
print()

# Cleanup
admin2 = KafkaAdminClient(bootstrap_servers=BROKER, request_timeout_ms=10_000)
try:
    admin2.delete_topics([SKEW_TOPIC])
except Exception:
    pass
admin2.close()

print("  Nugget 05-03 complete.")
print()
print("  Key takeaways:")
print("    - Hot keys cause partition skew -> consumer lag on specific partitions.")
print("    - Skew ratio = max_count / avg_count. Alert at > 3x.")
print("    - Fix: composite key (user_id + bucket) spreads load.")
print("    - Or: null key -> round-robin (gives up per-key ordering).")
print("    - Monitor partition lag per-partition, not just total lag.")
print()
