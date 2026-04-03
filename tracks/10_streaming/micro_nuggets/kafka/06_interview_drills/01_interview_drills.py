"""
+==============================================================================+
|  NUGGET 06-01 . Interview Drills                                             |
|  10+ runnable scenario drills with concise model answers.                    |
+==============================================================================+

Each drill is a RUNNABLE scenario that demonstrates the concept hands-on,
followed by a Q&A block with a concise interview-ready answer.

DRILLS COVERED
--------------
  1.  Ordering guarantee -- prove per-partition ordering
  2.  Offset management -- committed vs. latest
  3.  Consumer group partition assignment
  4.  At-least-once vs. exactly-once trade-offs
  5.  Retry vs. DLQ decision
  6.  Partition count and consumer parallelism
  7.  Message key and partitioning strategy
  8.  Consumer lag measurement
  9.  Rebalance triggers and mitigation
  10. Schema evolution backward compatibility
  11. Idempotent producer vs. application-level idempotency
  12. Watermark and late event handling

USAGE
-----
    python 01_interview_drills.py
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

print("\n" + "=" * 70)
print("  KAFKA INTERVIEW DRILLS")
print("=" * 70)
print(f"  Broker: {BROKER}")
print()

def section(n: int, title: str) -> None:
    print(f"\n{'─'*70}")
    print(f"  DRILL {n:02d}: {title}")
    print(f"{'─'*70}")

def qa(q: str, a: str) -> None:
    print(f"\n  Q: {q}")
    print(f"  A: {a}")


# ─────────────────────────────────────────────────────────────────────────────
# DRILL 01: Ordering guarantee
# ─────────────────────────────────────────────────────────────────────────────
section(1, "Ordering Guarantee")

DRILL_TOPIC = "lab.orders"
producer = KafkaProducer(
    bootstrap_servers=BROKER,
    acks="all",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda k: k.encode("utf-8") if isinstance(k, str) else k,
    request_timeout_ms=15_000,
)

# Produce 6 events for alice -- all must land on same partition
ts = int(time.time())
alice_events = []
for seq in range(6):
    ev = {"event_id": str(uuid.uuid4()), "user": "alice", "seq": seq, "ts": ts + seq}
    meta = producer.send(DRILL_TOPIC, key="alice", value=ev).get(timeout=10)
    alice_events.append((meta.partition, meta.offset, seq))

producer.flush()
producer.close()

partitions_used = set(p for p, _, _ in alice_events)
print(f"\n  Produced 6 events for 'alice'. Partitions used: {partitions_used}")
print(f"  (All same key -> always same partition -> strict ordering guaranteed)")

qa(
    "How does Kafka guarantee message ordering?",
    "Ordering is guaranteed within a single partition only. Use a consistent message key "
    "(e.g., user_id) so all related events hash to the same partition. "
    "Cross-partition ordering is NOT guaranteed."
)

# ─────────────────────────────────────────────────────────────────────────────
# DRILL 02: Offset management
# ─────────────────────────────────────────────────────────────────────────────
section(2, "Offset Management")

GROUP_D2 = f"drill02_{uuid.uuid4().hex[:8]}"
consumer = KafkaConsumer(
    DRILL_TOPIC,
    bootstrap_servers=BROKER,
    group_id=GROUP_D2,
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    consumer_timeout_ms=5_000,
    value_deserializer=lambda b: json.loads(b.decode("utf-8")),
)
consumed = 0
for msg in consumer:
    consumed += 1
    if consumed == 3:
        consumer.commit()
        print(f"\n  Committed after consuming 3 messages. Next read will start at offset+3.")
        break
consumer.close()

# Check committed offsets
c2 = KafkaConsumer(bootstrap_servers=BROKER, group_id=GROUP_D2, consumer_timeout_ms=2_000)
tps = [TopicPartition(DRILL_TOPIC, p) for p in c2.partitions_for_topic(DRILL_TOPIC) or []]
committed = {tp: c2.committed(tp) for tp in tps}
c2.close()
print(f"  Committed offsets: {committed}")

qa(
    "What is a Kafka offset and why does it matter?",
    "An offset is the sequential ID of a message within a partition (0-indexed). "
    "The consumer commits its current offset to Kafka so it knows where to resume "
    "after a restart or rebalance. enable_auto_commit=True commits automatically every "
    "5s; manual commit gives you control for at-least-once guarantees."
)

# ─────────────────────────────────────────────────────────────────────────────
# DRILL 03: Consumer group partition assignment
# ─────────────────────────────────────────────────────────────────────────────
section(3, "Consumer Group Partition Assignment")

GROUP_D3 = f"drill03_{uuid.uuid4().hex[:8]}"
c3 = KafkaConsumer(
    bootstrap_servers=BROKER,
    group_id=GROUP_D3,
    consumer_timeout_ms=3_000,
)
c3.subscribe([DRILL_TOPIC])
c3.poll(timeout_ms=4_000)
assigned = c3.assignment()
c3.close()

print(f"\n  Single consumer in group: owns {len(assigned)} partition(s) from {DRILL_TOPIC}")
print(f"  Partitions: {sorted(tp.partition for tp in assigned)}")

qa(
    "How does Kafka assign partitions to consumers in a group?",
    "The group coordinator assigns partitions so each partition goes to exactly one consumer "
    "in the group. With 3 partitions and 1 consumer: consumer gets all 3. "
    "With 3 partitions and 3 consumers: one partition each. "
    "With 3 partitions and 5 consumers: 3 active, 2 idle. "
    "Adding consumers beyond partition count adds no throughput benefit."
)

# ─────────────────────────────────────────────────────────────────────────────
# DRILL 04: At-least-once vs. exactly-once
# ─────────────────────────────────────────────────────────────────────────────
section(4, "At-Least-Once vs. Exactly-Once")

print("\n  Delivery semantics comparison:")
rows = [
    ("Semantic",        "At-most-once",       "At-least-once",     "Exactly-once"),
    ("acks",            "0",                  "all",               "all + idempotent"),
    ("retries",         "0",                  "> 0",               "sys.maxsize"),
    ("Commit timing",   "before processing",  "after processing",  "transactional"),
    ("Data loss",       "possible",           "never",             "never"),
    ("Duplicates",      "never",              "possible",          "never"),
    ("Complexity",      "simple",             "moderate",          "high"),
    ("Use case",        "metrics/logs",       "most DE pipelines", "financial/billing"),
]
for row in rows:
    print(f"  {row[0]:<18} {row[1]:<22} {row[2]:<22} {row[3]}")

qa(
    "What is exactly-once semantics in Kafka and when should you use it?",
    "Exactly-once requires: idempotent producer (enable_idempotence=True) + transactional "
    "producer/consumer API. This prevents duplicates from retries AND ensures atomic "
    "consume-process-produce. Use for financial transactions or billing. For most DE pipelines, "
    "at-least-once + idempotent sink (upsert by event_id) is simpler and sufficient."
)

# ─────────────────────────────────────────────────────────────────────────────
# DRILL 05: Retry vs. DLQ
# ─────────────────────────────────────────────────────────────────────────────
section(5, "Retry vs. Dead Letter Queue Decision")

print("\n  Decision tree:")
tree = [
    ("Error type",               "Transient (network, timeout)",      "Permanent (bad data, schema)"),
    ("Action",                   "Retry with exponential backoff",    "Send to DLQ immediately"),
    ("Max retries",              "3-5 attempts",                      "0 (DLQ on first failure)"),
    ("DLQ metadata",             "N/A",                               "original_topic, offset, reason"),
    ("Recovery",                 "Automatic (usually succeeds)",      "Manual investigation"),
]
for row in tree:
    print(f"  {row[0]:<25} {row[1]:<40} {row[2]}")

qa(
    "When should you retry a failed message vs. send it to the DLQ?",
    "Retry transient errors (network failure, downstream unavailable) with exponential backoff. "
    "Send to DLQ after N retries fail, or immediately for permanent errors (invalid schema, "
    "null required field). Never retry poison messages -- they block the pipeline. "
    "DLQ messages should carry: original topic, partition, offset, failure reason, retry count."
)

# ─────────────────────────────────────────────────────────────────────────────
# DRILL 06: Partition count and parallelism
# ─────────────────────────────────────────────────────────────────────────────
section(6, "Partition Count and Consumer Parallelism")

print("\n  Max consumer parallelism = number of partitions")
print("  Rule: num_consumers <= num_partitions (excess consumers are idle)")
print()
print("  Partition count trade-offs:")
print("    More partitions: higher throughput, more leader elections, more open files")
print("    Fewer partitions: lower overhead, sequential processing, easier to reason about")
print()
print("  Recommendation: start with 3-6 partitions. Scale up if needed.")

qa(
    "How many partitions should a Kafka topic have?",
    "Rule of thumb: num_partitions = target_throughput_MB/s / throughput_per_partition_MB/s. "
    "A single partition handles ~10-100 MB/s depending on message size. "
    "More partitions = more parallelism but also more overhead (leader elections, open files). "
    "Start at 3-6 for most topics. You can INCREASE partitions later (not decrease without data loss)."
)

# ─────────────────────────────────────────────────────────────────────────────
# DRILL 07: Message key and partitioning
# ─────────────────────────────────────────────────────────────────────────────
section(7, "Message Key and Partitioning Strategy")

# Show the same key always lands on the same partition
producer2 = KafkaProducer(
    bootstrap_servers=BROKER,
    acks=1,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda k: k.encode("utf-8") if isinstance(k, str) else k,
    request_timeout_ms=10_000,
)

print("\n  Producing 3 events per key (same key -> same partition):")
key_partitions: dict[str, set] = {}
for key in ["alice", "bob", "carol"]:
    for _ in range(3):
        meta = producer2.send(DRILL_TOPIC, key=key, value={"key": key}).get(timeout=10)
        key_partitions.setdefault(key, set()).add(meta.partition)

producer2.flush()
producer2.close()

for key, partitions in key_partitions.items():
    print(f"    key={key}: partitions={partitions}  unique={len(partitions)==1}")

qa(
    "What is the role of the message key in Kafka partitioning?",
    "The producer hashes the key (murmur2) to select a partition: partition = hash(key) % num_partitions. "
    "Same key always goes to the same partition -> ordering is guaranteed for that key. "
    "key=None -> round-robin across partitions (no ordering guarantee). "
    "This is why user_id is a common key: all events for one user stay in order."
)

# ─────────────────────────────────────────────────────────────────────────────
# DRILL 08: Consumer lag
# ─────────────────────────────────────────────────────────────────────────────
section(8, "Consumer Lag Measurement")

lag_consumer = KafkaConsumer(
    bootstrap_servers=BROKER,
    group_id=f"drill08_{uuid.uuid4().hex[:8]}",
    consumer_timeout_ms=2_000,
)
lag_consumer.subscribe([DRILL_TOPIC])
lag_consumer.poll(timeout_ms=3_000)
tps = list(lag_consumer.assignment())
if tps:
    ends = lag_consumer.end_offsets(tps)
    committed = {tp: (lag_consumer.committed(tp) or 0) for tp in tps}
    total_lag = sum(ends[tp] - committed[tp] for tp in tps)
    print(f"\n  Consumer group lag on {DRILL_TOPIC}: {total_lag} messages")
    for tp in sorted(tps, key=lambda x: x.partition):
        lag = ends[tp] - committed[tp]
        print(f"    partition={tp.partition}: end={ends[tp]} committed={committed[tp]} lag={lag}")
lag_consumer.close()

qa(
    "How do you measure and alert on consumer lag?",
    "lag = log_end_offset - committed_offset per partition. "
    "Total lag = sum across all partitions. "
    "Monitor with: kafka-consumer-groups.sh --describe, Kafka UI, or fetch_offsets() in code. "
    "Alert when: total_lag > threshold, lag growing over time, "
    "or max_partition_lag >> avg (skew). "
    "Fix: add consumers (up to partition count), optimize processing, or increase partitions."
)

# ─────────────────────────────────────────────────────────────────────────────
# DRILL 09: Rebalance triggers
# ─────────────────────────────────────────────────────────────────────────────
section(9, "Rebalance Triggers and Mitigation")

print("\n  Rebalance triggers:")
triggers = [
    ("Consumer joins group",          "New consumer started"),
    ("Consumer leaves group",         "Process stopped or crashed"),
    ("Heartbeat timeout",             "session.timeout.ms exceeded"),
    ("Poll interval exceeded",        "max.poll.interval.ms exceeded (slow processing)"),
    ("Partition count changed",       "Topic altered"),
    ("Subscription changed",          "Consumer subscribes to new topics"),
]
for trigger, cause in triggers:
    print(f"    {trigger:<30} <- {cause}")

print("\n  Mitigation strategies:")
mitigations = [
    "Use CooperativeStickyAssignor for incremental rebalance (no full stop)",
    "Increase max.poll.interval.ms if processing is slow",
    "Keep session.timeout.ms > 3x heartbeat.interval.ms",
    "Commit in on_partitions_revoked() to prevent re-reads",
    "Deploy consumers in rolling fashion to minimize simultaneous joins/leaves",
]
for m in mitigations:
    print(f"    - {m}")

qa(
    "What causes Kafka consumer rebalance and how do you reduce its impact?",
    "Rebalance is triggered when consumers join/leave the group, miss heartbeats, or take too long "
    "between poll() calls. Impact: all consumers pause during rebalance. "
    "Mitigations: use CooperativeStickyAssignor (incremental), commit offsets before revoke, "
    "increase max.poll.interval.ms for slow processors, and deploy gracefully."
)

# ─────────────────────────────────────────────────────────────────────────────
# DRILL 10: Schema evolution
# ─────────────────────────────────────────────────────────────────────────────
section(10, "Schema Evolution Backward Compatibility")

print("\n  Compatibility rules:")
rules = [
    ("ADD optional field with default", "BACKWARD compatible",  "Safe -- old producers still work"),
    ("REMOVE optional field",           "BACKWARD compatible",  "Consumer ignores missing field"),
    ("ADD required field (no default)", "BREAKING",             "Old producers don't send it"),
    ("RENAME field",                    "BREAKING",             "Old consumers use old name"),
    ("CHANGE field type",               "BREAKING",             "Deserialization fails"),
    ("REMOVE required field",           "FORWARD compatible",   "New producer omits it; old consumer errors"),
]
for change, compat, note in rules:
    print(f"    {change:<35} {compat:<22} {note}")

qa(
    "How do you safely evolve a Kafka event schema without breaking consumers?",
    "Only make backward-compatible changes: add optional fields with defaults. "
    "Include schema_version in every event. Consumers branch on schema_version to handle "
    "multiple versions. Use Confluent Schema Registry with Avro for centralized schema management "
    "and automatic compatibility checks. Never rename or remove required fields."
)

# ─────────────────────────────────────────────────────────────────────────────
# DRILL 11: Idempotent producer
# ─────────────────────────────────────────────────────────────────────────────
section(11, "Idempotent Producer vs. Application-Level Idempotency")

print("\n  Idempotent producer (enable_idempotence=True):")
print("    - Broker assigns Producer ID (PID) + sequence numbers")
print("    - Retries are deduplicated at the BROKER (consumer never sees duplicates)")
print("    - Requires acks=all, retries > 0, max_in_flight <= 5")
print("    - Scope: producer -> broker. Does NOT cover consumer -> sink.")
print()
print("  Application-level idempotency:")
print("    - Assign event_id (UUID) at source")
print("    - Sink uses UPSERT / INSERT IGNORE on event_id (primary key)")
print("    - Covers the full path: producer -> broker -> consumer -> sink")
print("    - Most practical approach for DE pipelines")

qa(
    "What is the difference between idempotent producer and application-level idempotency?",
    "Idempotent producer (enable_idempotence=True) deduplicates retries at the BROKER -- "
    "no duplicate messages reach the topic. But if the consumer crashes after consuming "
    "and before writing to the sink, the message is re-delivered (at-least-once). "
    "Application-level idempotency uses event_id + upsert in the sink to deduplicate "
    "end-to-end. Both layers together provide the strongest guarantees."
)

# ─────────────────────────────────────────────────────────────────────────────
# DRILL 12: Watermark and late events
# ─────────────────────────────────────────────────────────────────────────────
section(12, "Watermark and Late Event Handling")

print("\n  Watermark mechanics:")
print("    max_observed_ts = max event_ts seen by this consumer so far")
print("    watermark       = max_observed_ts - allowed_lateness_s")
print("    Window [T, T+W) closes when watermark > T+W")
print()
print("  Example:")
print("    W=60s, allowed_lateness=30s")
print("    max_observed_ts=1100, watermark=1070")
print("    Window [1000,1060): closed (watermark 1070 > 1060)")
print("    Window [1060,1120): open   (watermark 1070 < 1120)")
print()
print("  Late event options:")
print("    1. DROP: simplest, acceptable for non-critical metrics")
print("    2. UPDATE: re-emit window result with late data")
print("    3. SIDE OUTPUT: route to 'late' topic for reconciliation")

qa(
    "What is a watermark in stream processing and how does it handle late events?",
    "A watermark is a threshold: 'no event with event_ts < watermark will arrive'. "
    "watermark = max_observed_event_ts - allowed_lateness. Windows close when watermark "
    "passes window_end. Late events (event_ts < watermark at arrival) can be dropped, "
    "used to update window results, or routed to a side output topic. "
    "Flink/Kafka Streams implement this natively; kafka-python requires manual tracking."
)

print()
print("=" * 70)
print("  ALL 12 DRILLS COMPLETE")
print("=" * 70)
print()
print("  Link to runnable nuggets:")
print("    Ordering:         01_core_kafka/04_ordering_guarantees.py")
print("    At-least-once:    02_reliability/01_at_least_once_demo.py")
print("    DLQ:              02_reliability/04_dead_letter_topic.py")
print("    Watermarks:       04_stream_processing_patterns/03_watermark_late_events.py")
print("    Consumer lag:     05_operations/01_consumer_lag.py")
print("    Schema evolution: 03_schema_and_contracts/02_versioned_schema.py")
print()
