"""
+==============================================================================+
|  NUGGET 05-02 . Rebalance Behavior                                           |
|  Understand what triggers rebalance and how to minimize impact.              |
+==============================================================================+

CONCEPTS
--------
  Consumer Group Rebalance:
    When the assignment of partitions to consumers in a group changes.
    During rebalance: ALL consumers STOP consuming.
    After rebalance: partitions are re-assigned, consumers resume.

  Rebalance Triggers:
    1. Consumer joins the group (new consumer started).
    2. Consumer leaves the group (consumer stopped/crashed).
    3. Consumer fails heartbeat (session.timeout.ms exceeded).
    4. Topic partition count changes.
    5. Subscription changes (consumer subscribes to new topics).

  Key Timeout Parameters:
    session.timeout.ms (default 10s):
      How long the broker waits for a heartbeat before declaring a consumer dead.
      Lower = faster rebalance on failure. Higher = more tolerant of slow processing.

    heartbeat.interval.ms (default 3s):
      How often the consumer sends heartbeats to the broker.
      Must be < session.timeout.ms. Typically session_timeout/3.

    max.poll.interval.ms (default 5 min):
      Max time between poll() calls before the broker assumes consumer is dead.
      If processing takes longer than this, the consumer is kicked out.
      FIX: increase this value OR reduce batch size.

  Rebalance Strategies:
    RangeAssignor (default): assigns consecutive partitions per topic per consumer.
    RoundRobinAssignor: distributes partitions evenly across consumers.
    StickyAssignor: minimizes partition movement on rebalance (reduces disruption).
    CooperativeStickyAssignor: incremental rebalance -- only reassigns necessary partitions.
      Best choice for production (no full stop-the-world rebalance).

  Commit Before Rebalance (ConsumerRebalanceListener):
    If you use manual commits, commit current offsets before a rebalance.
    Otherwise, after rebalance the consumer may re-read uncommitted messages.

DEMONSTRATION
-------------
  1. Show rebalance listener (on_partitions_revoked / on_partitions_assigned).
  2. Demonstrate partition assignment counts.
  3. Explain key tuning parameters.
  4. Show cooperative sticky assignment configuration.

NOTE: True rebalance demo requires multiple consumer instances. This nugget
      provides a single-consumer demo with listener hooks and explanation.

USAGE
-----
    python 02_rebalance_notes.py
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

from kafka import KafkaConsumer, KafkaProducer, TopicPartition
from kafka.coordinator.assignors.sticky.sticky_assignor import StickyPartitionAssignor

print("\n-- Nugget 05-02: Rebalance Behavior --")
print(f"  Broker: {BROKER}")
print()

TOPIC = "lab.raw.events"

# ─────────────────────────────────────────────────────────────────────────────
# 1. RebalanceListener hooks
# ─────────────────────────────────────────────────────────────────────────────
print("  [1] Consumer with RebalanceListener:")

from kafka import ConsumerRebalanceListener

rebalance_log: list[str] = []


class LabRebalanceListener(ConsumerRebalanceListener):
    def __init__(self, consumer_ref):
        self.consumer = consumer_ref

    def on_partitions_revoked(self, revoked: list):
        """Called BEFORE rebalance starts. Commit here to avoid re-reads."""
        ts = int(time.time())
        msg = f"  [REVOKED]  ts={ts}  partitions={[tp.partition for tp in revoked]}"
        rebalance_log.append(msg)
        print(msg)
        # In production: self.consumer.commit() here
        # to save progress before partitions move to another consumer.

    def on_partitions_assigned(self, assigned: list):
        """Called AFTER rebalance completes. Consumer owns these partitions now."""
        ts = int(time.time())
        msg = f"  [ASSIGNED] ts={ts}  partitions={[tp.partition for tp in assigned]}"
        rebalance_log.append(msg)
        print(msg)


GROUP = f"rebalance_demo_{uuid.uuid4().hex[:8]}"

consumer = KafkaConsumer(
    bootstrap_servers=BROKER,
    group_id=GROUP,
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    consumer_timeout_ms=5_000,
    # Key timeout tuning:
    session_timeout_ms=30_000,       # 30s before broker declares consumer dead
    heartbeat_interval_ms=10_000,    # heartbeat every 10s (must be < session_timeout)
    max_poll_interval_ms=300_000,    # 5 min max between polls (increase for slow processing)
    # Sticky assignment: minimize partition movement on rebalance
    partition_assignment_strategy=[StickyPartitionAssignor],
)

consumer.subscribe([TOPIC], listener=LabRebalanceListener(consumer))

print(f"  Subscribed to {TOPIC} with group={GROUP[:28]}...")
print(f"  Polling once to trigger initial assignment ...")

# First poll triggers the initial join group + rebalance
records = consumer.poll(timeout_ms=5_000)
assigned = consumer.assignment()

print()
print(f"  [2] Partition assignment after join:")
print(f"    Partitions owned by this consumer: {sorted(tp.partition for tp in assigned)}")
print()

# Show per-partition end offsets
end_offsets = consumer.end_offsets(list(assigned))
print(f"  [3] Current offsets for owned partitions:")
print(f"  {'partition':10}  {'end_offset':12}  {'position':10}")
print(f"  {'-'*36}")
for tp in sorted(assigned, key=lambda x: x.partition):
    end = end_offsets.get(tp, 0)
    try:
        pos = consumer.position(tp)
    except Exception:
        pos = "unknown"
    print(f"  {tp.partition:<10}  {end:<12}  {pos}")

consumer.close()
print()

# ─────────────────────────────────────────────────────────────────────────────
# 4. Rebalance tuning reference
# ─────────────────────────────────────────────────────────────────────────────
print("  [4] Rebalance tuning reference:")
params = [
    ("session.timeout.ms",      "30000",  "Time before broker declares consumer dead. Increase for slow networks."),
    ("heartbeat.interval.ms",   "10000",  "Must be < session.timeout.ms / 3. More frequent = earlier failure detection."),
    ("max.poll.interval.ms",    "300000", "Increase if processing each batch takes > default 5 min."),
    ("partition.assignment.strategy", "StickyAssignor", "Minimizes movement. Use CooperativeSticky for incremental rebalance."),
]
for name, value, note in params:
    print(f"    {name:<40}  {value:<12}  {note}")

print()
print("  [5] Rebalance trigger reference:")
triggers = [
    "Consumer joins group (new process started)",
    "Consumer leaves group (process stopped/crashed)",
    "Consumer misses heartbeat within session.timeout.ms",
    "Consumer poll() gap exceeds max.poll.interval.ms",
    "Topic partition count changed",
    "Consumer subscribes to new topics",
]
for t in triggers:
    print(f"    - {t}")
print()

print("  Nugget 05-02 complete.")
print()
print("  Key takeaways:")
print("    - Rebalance = stop-the-world for the consumer group (by default).")
print("    - Use StickyAssignor or CooperativeStickyAssignor to minimize disruption.")
print("    - Commit in on_partitions_revoked() to avoid re-reading messages.")
print("    - Tune max.poll.interval.ms if processing is slow.")
print("    - Monitor rebalance frequency in Kafka UI / JMX metrics.")
print()
