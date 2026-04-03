"""
+==============================================================================+
|  NUGGET 01-04 . Ordering Guarantees                                          |
|  How Kafka maintains order and when it breaks.                               |
+==============================================================================+

CONCEPTS
--------
  Kafka Ordering Rule:
    Messages within a SINGLE PARTITION are strictly ordered (FIFO).
    Messages ACROSS PARTITIONS have NO ordering guarantee.

  Why ordering matters:
    User "alice" places order #1, then cancels order #1.
    If these land on different partitions, a consumer may see cancel BEFORE place.
    Solution: use the order_id (or user_id) as the message key.
    Same key -> same partition -> correct sequence always.

  When ordering breaks:
    - Multiple partitions without keying: round-robin distributes messages.
    - Producer retries with acks=1 can cause duplicates/reordering.
    - Idempotent producer (enable_idempotence=True) prevents reorder from retries.

  Single-partition topics:
    The simplest way to guarantee global order.
    Drawback: single-partition = no parallelism (one consumer at a time).

OPERATIONS COVERED
------------------
  1. Ordered produce and consume on single partition
  2. Unkeyed produce across partitions -> observe interleaved order
  3. Keyed produce -> show same key always same partition (consistent order)
  4. Demonstrate global order breaks with multiple partitions

USAGE
-----
    python 04_ordering_guarantees.py
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

from kafka import KafkaAdminClient, KafkaConsumer, KafkaProducer, TopicPartition
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError

print("\n-- Nugget 01-04: Ordering Guarantees --")
print(f"  Broker: {BROKER}")
print()

admin = KafkaAdminClient(bootstrap_servers=BROKER, request_timeout_ms=15_000)

ORDER_TOPIC_SINGLE = "lab.demo.ordering_single"
ORDER_TOPIC_MULTI  = "lab.demo.ordering_multi"

for tname, nparts in [(ORDER_TOPIC_SINGLE, 1), (ORDER_TOPIC_MULTI, 3)]:
    try:
        admin.create_topics([NewTopic(name=tname, num_partitions=nparts, replication_factor=1)])
    except TopicAlreadyExistsError:
        pass

admin.close()

producer = KafkaProducer(
    bootstrap_servers=BROKER,
    acks="all",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    request_timeout_ms=15_000,
)

# ─────────────────────────────────────────────────────────────────────────────
# 1. Single partition -- strict global ordering
# ─────────────────────────────────────────────────────────────────────────────
print("  [1] Single-partition topic -- strict global order:")
seq_expected = list(range(10))
for seq in seq_expected:
    producer.send(ORDER_TOPIC_SINGLE, value={"seq": seq, "ts": int(time.time())})
producer.flush()

consumer = KafkaConsumer(
    ORDER_TOPIC_SINGLE,
    bootstrap_servers=BROKER,
    group_id=f"ordering_demo_{uuid.uuid4().hex[:6]}",
    auto_offset_reset="earliest",
    consumer_timeout_ms=5_000,
    value_deserializer=lambda b: json.loads(b.decode("utf-8")),
)
received_seqs = [msg.value["seq"] for msg in consumer]
consumer.close()

in_order = received_seqs == sorted(received_seqs)
print(f"    Sent:     {seq_expected}")
print(f"    Received: {received_seqs}")
print(f"    In order: {in_order}  (single partition = always ordered)")
print()

# ─────────────────────────────────────────────────────────────────────────────
# 2. Multi-partition WITHOUT key -- round-robin, no global ordering
# ─────────────────────────────────────────────────────────────────────────────
print("  [2] Multi-partition WITHOUT key -- round-robin (no global order):")
for seq in range(12):
    producer.send(ORDER_TOPIC_MULTI, value={"seq": seq, "ts": int(time.time())})
producer.flush()

c2 = KafkaConsumer(
    ORDER_TOPIC_MULTI,
    bootstrap_servers=BROKER,
    group_id=f"ordering_demo2_{uuid.uuid4().hex[:6]}",
    auto_offset_reset="earliest",
    consumer_timeout_ms=5_000,
    value_deserializer=lambda b: json.loads(b.decode("utf-8")),
)
msgs2 = [(msg.partition, msg.value["seq"]) for msg in c2]
c2.close()

print(f"    Messages by (partition, seq):")
for part, seq in msgs2:
    print(f"      partition={part}  seq={seq}")
global_seqs = [s for _, s in msgs2]
print(f"    Global seq order: {global_seqs}")
print(f"    Is globally sorted: {global_seqs == sorted(global_seqs)}")
print(f"    -> Global ordering NOT guaranteed across partitions")
print()

# ─────────────────────────────────────────────────────────────────────────────
# 3. Multi-partition WITH key -- per-key ordering guaranteed
# ─────────────────────────────────────────────────────────────────────────────
print("  [3] Multi-partition WITH key -- per-key ordering:")
user_events: dict[str, list[int]] = {"alice": [], "bob": [], "carol": []}
for seq in range(15):
    user = list(user_events.keys())[seq % 3]
    user_events[user].append(seq)
    producer.send(
        ORDER_TOPIC_MULTI,
        key=user.encode("utf-8"),
        value={"user": user, "seq": seq},
    )
producer.flush()

c3 = KafkaConsumer(
    ORDER_TOPIC_MULTI,
    bootstrap_servers=BROKER,
    group_id=f"ordering_demo3_{uuid.uuid4().hex[:6]}",
    auto_offset_reset="earliest",
    consumer_timeout_ms=5_000,
    value_deserializer=lambda b: json.loads(b.decode("utf-8")),
)
per_key_received: dict[str, list[int]] = {"alice": [], "bob": [], "carol": []}
per_key_partition: dict[str, set] = {"alice": set(), "bob": set(), "carol": set()}

for msg in c3:
    v = msg.value
    if isinstance(v, dict) and "user" in v:
        per_key_received[v["user"]].append(v["seq"])
        per_key_partition[v["user"]].add(msg.partition)
c3.close()

for user in ["alice", "bob", "carol"]:
    seqs = per_key_received[user]
    partitions = per_key_partition[user]
    ordered = seqs == sorted(seqs) if seqs else True
    print(f"    {user:6}: partition(s)={partitions}  seqs={seqs}  ordered={ordered}")

print()

producer.close()

# Cleanup demo topics
admin2 = KafkaAdminClient(bootstrap_servers=BROKER, request_timeout_ms=10_000)
try:
    admin2.delete_topics([ORDER_TOPIC_SINGLE, ORDER_TOPIC_MULTI])
except Exception:
    pass
admin2.close()

print("  Nugget 01-04 complete.")
print()
print("  Key takeaways:")
print("    - Ordering is guaranteed per partition only, not globally.")
print("    - Use message keys to group related events onto the same partition.")
print("    - key=None -> round-robin -> no ordering guarantee.")
print("    - Single-partition topics have global order but sacrifice parallelism.")
print("    - Idempotent producer (enable_idempotence=True) prevents reorder from retries.")
print()
