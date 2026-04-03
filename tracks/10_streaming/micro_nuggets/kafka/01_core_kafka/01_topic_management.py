"""
+==============================================================================+
|  NUGGET 01-01 . Topic Management                                             |
|  Create, list, describe, and delete Kafka topics programmatically.           |
+==============================================================================+

CONCEPTS
--------
  Topic:
    Named, append-only log. Producers write to it; consumers read from it.
    A topic is split into one or more partitions.

  Partition:
    Ordered, immutable sequence of records. The unit of parallelism.
    More partitions = higher throughput (more consumers can read in parallel).
    BUT: more partitions = more leader elections and metadata overhead.

  Replication Factor:
    How many brokers hold a copy of each partition.
    replication_factor=1 means no redundancy (fine for local lab).
    Production minimum: 3 (one leader, two followers in ISR).

  ISR (In-Sync Replica):
    Set of replicas that are caught up with the partition leader.
    acks="all" waits for all ISR replicas to confirm -- ensures durability.

OPERATIONS COVERED
------------------
  1. List all topics
  2. Create a topic with partition and replication settings
  3. Describe topic (partition count, replication, leader)
  4. Idempotent creation (topic already exists case)
  5. Delete a topic

USAGE
-----
    python 01_topic_management.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _kafka_connect import BROKER, require_broker

require_broker(BROKER)

from kafka import KafkaAdminClient, KafkaConsumer
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError, UnknownTopicOrPartitionError

DEMO_TOPIC = "lab.demo.topic_management"

print("\n-- Nugget 01-01: Topic Management --")
print(f"  Broker: {BROKER}")
print()

admin = KafkaAdminClient(bootstrap_servers=BROKER, request_timeout_ms=15_000)

# ─────────────────────────────────────────────────────────────────────────────
# 1. List existing topics
# ─────────────────────────────────────────────────────────────────────────────
consumer_temp = KafkaConsumer(bootstrap_servers=BROKER, consumer_timeout_ms=2_000)
all_topics = sorted(consumer_temp.topics())
consumer_temp.close()

print("  [1] All topics visible on broker:")
if all_topics:
    for t in all_topics:
        print(f"      {t}")
else:
    print("      (none yet)")
print()

# ─────────────────────────────────────────────────────────────────────────────
# 2. Create a topic
# ─────────────────────────────────────────────────────────────────────────────
print(f"  [2] Creating topic: {DEMO_TOPIC}")
print(f"      num_partitions=3, replication_factor=1")
try:
    admin.create_topics([
        NewTopic(
            name=DEMO_TOPIC,
            num_partitions=3,
            replication_factor=1,
            topic_configs={
                "retention.ms": str(60 * 60 * 1000),  # 1 hour retention
                "cleanup.policy": "delete",
            },
        )
    ])
    print("      [OK] Topic created")
except TopicAlreadyExistsError:
    print("      [INFO] Topic already exists -- skipping creation")
print()

# ─────────────────────────────────────────────────────────────────────────────
# 3. Describe topic
# ─────────────────────────────────────────────────────────────────────────────
print(f"  [3] Describing topic: {DEMO_TOPIC}")
try:
    description = admin.describe_topics([DEMO_TOPIC])
    for topic_meta in description:
        name = topic_meta.get("topic", "?")
        partitions = topic_meta.get("partitions", [])
        print(f"      Topic:      {name}")
        print(f"      Partitions: {len(partitions)}")
        for p in partitions:
            pid = p.get("partition", "?")
            leader = p.get("leader", "?")
            replicas = p.get("replicas", [])
            isr = p.get("isr", [])
            print(f"        Partition {pid}: leader={leader}  replicas={replicas}  isr={isr}")
except Exception as exc:
    print(f"      [WARN] Could not describe topic: {exc}")
print()

# ─────────────────────────────────────────────────────────────────────────────
# 4. Idempotent creation demo
# ─────────────────────────────────────────────────────────────────────────────
print(f"  [4] Idempotent creation -- creating {DEMO_TOPIC} again:")
try:
    admin.create_topics([NewTopic(name=DEMO_TOPIC, num_partitions=3, replication_factor=1)])
    print("      Created (unexpected)")
except TopicAlreadyExistsError:
    print("      [OK] TopicAlreadyExistsError caught -- safe to ignore in idempotent setup")
print()

# ─────────────────────────────────────────────────────────────────────────────
# 5. Delete topic
# ─────────────────────────────────────────────────────────────────────────────
print(f"  [5] Deleting topic: {DEMO_TOPIC}")
try:
    admin.delete_topics([DEMO_TOPIC], timeout_ms=10_000)
    print("      [OK] Topic deleted")
except Exception as exc:
    print(f"      [WARN] Delete returned: {exc}")
print()

admin.close()

print("  Nugget 01-01 complete.")
print()
print("  Key takeaways:")
print("    - Topics are the unit of organization in Kafka.")
print("    - Partitions define parallelism; replication_factor defines durability.")
print("    - Creating a topic that already exists raises TopicAlreadyExistsError.")
print("    - Delete is async; the broker confirms but cleanup happens in background.")
print()
