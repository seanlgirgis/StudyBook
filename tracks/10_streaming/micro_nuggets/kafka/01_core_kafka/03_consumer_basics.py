"""
+==============================================================================+
|  NUGGET 01-03 . Consumer Basics                                              |
|  Offsets, consumer groups, commit strategies, and poll patterns.             |
+==============================================================================+

CONCEPTS
--------
  Consumer Group:
    Set of consumers sharing a group_id. Kafka automatically assigns each
    partition to exactly one consumer in the group.
    - 1 consumer: reads all partitions.
    - N consumers (N = partition count): each reads one partition in parallel.
    - N consumers > partition count: some consumers sit idle.
    - Different group_ids are completely independent -- each gets its own offsets.

  Offset:
    Position of a message within a partition (0-indexed, monotonically increasing).
    The consumer commits its current offset so it knows where to resume after a
    restart or rebalance.

  Commit Strategies:
    - auto_commit (enable_auto_commit=True): broker auto-commits every
      auto_commit_interval_ms milliseconds. Risk: commits before processing done.
    - manual sync:  consumer.commit()  -- blocks until broker confirms.
    - manual async: consumer.commit_async() -- non-blocking.

  auto_offset_reset:
    - "earliest": start from the beginning of the topic (offset 0) when no
      committed offset exists for this group.
    - "latest": start from the end -- only consume messages produced after
      this consumer first started.

  consumer_timeout_ms:
    After this many ms with no new messages, iteration stops (StopIteration).
    Use this in scripts to avoid infinite loops.

OPERATIONS COVERED
------------------
  1. Simple consume (auto-commit, read all from beginning)
  2. Manual commit with per-message processing acknowledgment
  3. Multiple groups reading the same topic independently
  4. Seek to specific offset (replay from position)
  5. Consumer assignment and partition info

USAGE
-----
    python 03_consumer_basics.py
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

from kafka import KafkaConsumer, KafkaProducer, TopicPartition

print("\n-- Nugget 01-03: Consumer Basics --")
print(f"  Broker: {BROKER}")
print()

# Seed a few fresh messages for demos
_producer = KafkaProducer(
    bootstrap_servers=BROKER,
    acks=1,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    request_timeout_ms=10_000,
)
_ts = int(time.time())
for i in range(8):
    _producer.send("lab.raw.events", value={"seq": i, "ts": _ts, "nugget": "03_consumer"})
_producer.flush()
_producer.close()

# ─────────────────────────────────────────────────────────────────────────────
# 1. Simple consume -- auto-commit, read from earliest
# ─────────────────────────────────────────────────────────────────────────────
print("  [1] Simple consume (auto-commit, earliest):")
GROUP_1 = f"consumer_basics_group1_{uuid.uuid4().hex[:6]}"

consumer = KafkaConsumer(
    "lab.raw.events",
    bootstrap_servers=BROKER,
    group_id=GROUP_1,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    consumer_timeout_ms=5_000,
    value_deserializer=safe_json_deserializer,
)

count = 0
for msg in consumer:
    count += 1
consumer.close()

print(f"    Group {GROUP_1[:24]}... read {count} messages from lab.raw.events")
print()

# ─────────────────────────────────────────────────────────────────────────────
# 2. Manual commit -- safer for at-least-once processing
#    Process the message THEN commit. If the process crashes before commit,
#    the message is re-delivered on restart (at-least-once semantics).
# ─────────────────────────────────────────────────────────────────────────────
print("  [2] Manual commit (at-least-once processing):")
GROUP_2 = f"consumer_basics_group2_{uuid.uuid4().hex[:6]}"

consumer2 = KafkaConsumer(
    "lab.raw.events",
    bootstrap_servers=BROKER,
    group_id=GROUP_2,
    auto_offset_reset="earliest",
    enable_auto_commit=False,   # we commit manually
    consumer_timeout_ms=5_000,
    value_deserializer=safe_json_deserializer,
    max_poll_records=10,
)

processed = 0
for msg in consumer2:
    # Simulate processing
    _ = msg.value
    processed += 1
    # Commit current offset synchronously after processing
    consumer2.commit()

consumer2.close()
print(f"    Processed and committed {processed} messages.")
print(f"    Safety: if process crashes before commit(), message is re-delivered.")
print()

# ─────────────────────────────────────────────────────────────────────────────
# 3. Two independent groups -- each gets ALL messages
#    Different group_ids maintain separate offset pointers.
# ─────────────────────────────────────────────────────────────────────────────
print("  [3] Independent consumer groups -- each reads full topic:")

for group_name in ["analytics_team", "alerts_service"]:
    c = KafkaConsumer(
        "lab.raw.events",
        bootstrap_servers=BROKER,
        group_id=f"{group_name}_{uuid.uuid4().hex[:6]}",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        consumer_timeout_ms=4_000,
    )
    n = sum(1 for _ in c)
    c.close()
    print(f"    Group '{group_name}' read {n} messages independently")

print()

# ─────────────────────────────────────────────────────────────────────────────
# 4. Consumer partition assignment and offset introspection
# ─────────────────────────────────────────────────────────────────────────────
print("  [4] Partition assignment and offset info:")

GROUP_4 = f"consumer_basics_group4_{uuid.uuid4().hex[:6]}"
consumer4 = KafkaConsumer(
    "lab.raw.events",
    bootstrap_servers=BROKER,
    group_id=GROUP_4,
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    consumer_timeout_ms=3_000,
)

# Force assignment by polling once
consumer4.poll(timeout_ms=2_000)
assignment = consumer4.assignment()
print(f"    Partitions assigned to this consumer: {sorted(tp.partition for tp in assignment)}")

for tp in sorted(assignment, key=lambda x: x.partition):
    pos = consumer4.position(tp)
    end = consumer4.end_offsets([tp])[tp]
    print(f"      Partition {tp.partition}: current_position={pos}  log_end_offset={end}  lag={end - pos}")

consumer4.close()
print()

print("  Nugget 01-03 complete.")
print()
print("  Key takeaways:")
print("    - Consumer groups partition the load; different groups get independent copies.")
print("    - auto_offset_reset='earliest' ensures lab scripts replay from the start.")
print("    - Manual commit + process-before-commit = at-least-once semantics.")
print("    - consumer_timeout_ms prevents infinite loops in batch scripts.")
print()

