"""
+==============================================================================+
|  NUGGET 05-01 . Consumer Lag Estimation                                      |
|  Monitor how far behind consumers are from the latest messages.              |
+==============================================================================+

CONCEPTS
--------
  Consumer Lag:
    The number of messages in a partition that have been produced but NOT YET
    consumed by a specific consumer group.

    lag = log_end_offset - committed_offset

  Why Monitor Lag?
    - High lag = consumers are falling behind producers.
    - Spike in lag = processing slowdown or consumer failure.
    - Lag trending up = time to add more consumers or optimize processing.

  Lag Measurement:
    For each partition:
      1. Get the log_end_offset (latest offset the broker has received).
      2. Get the committed_offset for the consumer group.
      3. lag = log_end_offset - committed_offset

  Lag Tools:
    - kafka-consumer-groups.sh --describe: standard CLI (in the Docker container)
    - Kafka UI at localhost:8080: visual lag display
    - kafka-python: fetch_offsets() and end_offsets()

  Key Metrics to Alert On:
    - total lag > N: consumer is falling behind
    - max_partition_lag >> avg_partition_lag: partition skew
    - lag_rate: lag growing over time = consumer can't keep up

USAGE
-----
    python 01_consumer_lag.py
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

print("\n-- Nugget 05-01: Consumer Lag Estimation --")
print(f"  Broker: {BROKER}")
print()

TOPIC = "lab.raw.events"
GROUP = f"lag_demo_group_{uuid.uuid4().hex[:8]}"

# ─────────────────────────────────────────────────────────────────────────────
# Helper: compute lag for a group on a topic
# ─────────────────────────────────────────────────────────────────────────────
def get_lag_report(topic: str, group_id: str) -> list[dict]:
    """
    Return per-partition lag for a consumer group.
    """
    consumer = KafkaConsumer(
        bootstrap_servers=BROKER,
        group_id=group_id,
        enable_auto_commit=False,
        consumer_timeout_ms=3_000,
    )
    # Get topic partitions
    partitions = consumer.partitions_for_topic(topic)
    if not partitions:
        consumer.close()
        return []

    tps = [TopicPartition(topic, p) for p in partitions]

    # Get end offsets (latest)
    end_offsets = consumer.end_offsets(tps)

    # Get committed offsets for this group
    committed = {}
    for tp in tps:
        offset_and_meta = consumer.committed(tp)
        committed[tp] = offset_and_meta if offset_and_meta is not None else 0

    consumer.close()

    report = []
    for tp in tps:
        end = end_offsets.get(tp, 0)
        com = committed.get(tp, 0)
        lag = max(0, end - com)
        report.append({
            "topic":     tp.topic,
            "partition": tp.partition,
            "end_offset": end,
            "committed_offset": com,
            "lag": lag,
        })
    return sorted(report, key=lambda r: r["partition"])


# ─────────────────────────────────────────────────────────────────────────────
# Step 1: produce 50 messages to the topic
# ─────────────────────────────────────────────────────────────────────────────
print("  [1] Producing 50 messages ...")
producer = KafkaProducer(
    bootstrap_servers=BROKER,
    acks="all",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    request_timeout_ms=15_000,
)
ts = int(time.time())
for i in range(50):
    producer.send(TOPIC, value={"seq": i, "ts": ts + i, "nugget": "05_lag"})
producer.flush()
producer.close()
print("    Produced 50 messages.")
print()

# ─────────────────────────────────────────────────────────────────────────────
# Step 2: check lag BEFORE consuming (should be high)
# ─────────────────────────────────────────────────────────────────────────────
print(f"  [2] Lag report BEFORE consuming (group={GROUP[:28]}...):")
print(f"  {'partition':10}  {'end_offset':12}  {'committed':10}  {'lag':8}")
print(f"  {'-'*46}")

report_before = get_lag_report(TOPIC, GROUP)
total_lag_before = 0
for r in report_before:
    print(f"  {r['partition']:<10}  {r['end_offset']:<12}  {r['committed_offset']:<10}  {r['lag']:<8}")
    total_lag_before += r["lag"]

print(f"  TOTAL LAG: {total_lag_before}")
print()

# ─────────────────────────────────────────────────────────────────────────────
# Step 3: consume 25 messages (partial)
# ─────────────────────────────────────────────────────────────────────────────
print("  [3] Consuming 25 messages (partial) ...")
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BROKER,
    group_id=GROUP,
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    consumer_timeout_ms=5_000,
    value_deserializer=lambda b: json.loads(b.decode("utf-8")),
    max_poll_records=25,
)
consumed = 0
for msg in consumer:
    consumed += 1
    consumer.commit()
    if consumed >= 25:
        break
consumer.close()
print(f"    Consumed {consumed} messages, committed offsets.")
print()

# ─────────────────────────────────────────────────────────────────────────────
# Step 4: check lag AFTER partial consumption
# ─────────────────────────────────────────────────────────────────────────────
print("  [4] Lag report AFTER partial consumption:")
print(f"  {'partition':10}  {'end_offset':12}  {'committed':10}  {'lag':8}")
print(f"  {'-'*46}")

report_after = get_lag_report(TOPIC, GROUP)
total_lag_after = 0
for r in report_after:
    print(f"  {r['partition']:<10}  {r['end_offset']:<12}  {r['committed_offset']:<10}  {r['lag']:<8}")
    total_lag_after += r["lag"]

print(f"  TOTAL LAG: {total_lag_after}  (reduced from {total_lag_before})")
print()

# ─────────────────────────────────────────────────────────────────────────────
# Step 5: CLI equivalent command
# ─────────────────────────────────────────────────────────────────────────────
print("  [5] CLI equivalent (run inside citi_kafka container):")
print(f"    docker exec citi_kafka kafka-consumer-groups --bootstrap-server localhost:9092 \\")
print(f"      --describe --group {GROUP}")
print()
print("    Or view all groups in Kafka UI: http://localhost:8080")
print()

print("  Nugget 05-01 complete.")
print()
print("  Key takeaways:")
print("    - lag = log_end_offset - committed_offset per partition.")
print("    - Monitor total lag AND per-partition lag (skew detection).")
print("    - Alert when lag exceeds threshold or grows over time.")
print("    - Kafka UI at localhost:8080 provides visual lag monitoring.")
print()
