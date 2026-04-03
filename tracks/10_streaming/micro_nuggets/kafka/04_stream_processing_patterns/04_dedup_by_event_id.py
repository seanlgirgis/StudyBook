"""
+==============================================================================+
|  NUGGET 04-04 . Deduplication by event_id + event_time                      |
|  Idempotent consumer pattern using event_id deduplication.                  |
+==============================================================================+

CONCEPTS
--------
  Why Deduplication?
    In at-least-once delivery, the same message may be delivered multiple times.
    If the consumer writes to a database or downstream system, duplicate writes
    corrupt data (double-counted metrics, duplicate orders, etc.).

  Dedup Window:
    Storing every seen event_id forever is expensive.
    Use a dedup WINDOW: only track event_ids seen within the last N seconds/hours.
    Events older than the window are assumed unique or irrelevant.

  Dedup Storage Options:
    1. In-memory set (this nugget): fast, lost on restart. OK for short windows.
    2. Redis SET with TTL: survives restarts, fast, distributed.
    3. Database unique index (INSERT IGNORE / ON CONFLICT DO NOTHING): durable.
    4. Bloom filter: probabilistic, very memory-efficient, occasional false positives.

  Dedup by (event_id, event_time):
    Occasionally two different events have the same ID (bug in upstream producer).
    Adding event_time as a secondary key reduces false dedup collisions.
    But: standard practice is to treat event_id alone as unique (UUID guarantees this).

DEMONSTRATION
-------------
  1. Produce events with intentional duplicates.
  2. Consume with in-memory dedup set.
  3. Show dedup metrics.
  4. Demonstrate time-windowed dedup (rolling TTL).

USAGE
-----
    python 04_dedup_by_event_id.py
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

print("\n-- Nugget 04-04: Deduplication by event_id --")
print(f"  Broker: {BROKER}")
print()

TOPIC = "lab.raw.events"
DEDUP_WINDOW_S = 300  # keep event_ids seen in last 5 minutes

# ─────────────────────────────────────────────────────────────────────────────
# Seed events with deliberate duplicates
# ─────────────────────────────────────────────────────────────────────────────
print("  Seeding events with duplicates ...")

producer = KafkaProducer(
    bootstrap_servers=BROKER,
    acks="all",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    request_timeout_ms=15_000,
)

fixed_ids = [str(uuid.uuid4()) for _ in range(5)]  # IDs that will appear multiple times
ts = int(time.time())
sent_total = 0

# Produce unique events
for i in range(15):
    ev = {"event_id": str(uuid.uuid4()), "seq": i, "ts": ts + i, "type": "unique"}
    producer.send(TOPIC, value=ev)
    sent_total += 1

# Produce events with duplicate IDs (simulating retries / producer bugs)
for fixed_id in fixed_ids:
    for dup_n in range(3):  # each ID appears 3 times
        ev = {"event_id": fixed_id, "seq": 999, "ts": ts, "type": "duplicate", "dup_n": dup_n}
        producer.send(TOPIC, value=ev)
        sent_total += 1

producer.flush()
producer.close()
print(f"    Sent {sent_total} total messages ({len(fixed_ids)} IDs appear 3x each = {len(fixed_ids)*3} duplicates)")
print()

# ─────────────────────────────────────────────────────────────────────────────
# Consume with dedup logic
# ─────────────────────────────────────────────────────────────────────────────
print("  Consuming with event_id deduplication:")

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BROKER,
    group_id=f"dedup_demo_{uuid.uuid4().hex[:8]}",
    auto_offset_reset="earliest",
    consumer_timeout_ms=7_000,
    value_deserializer=safe_json_deserializer,
    enable_auto_commit=False,
)

# Dedup state: {event_id: first_seen_ts}
dedup_cache: dict[str, int] = {}
dedup_evictions = 0

processed = 0
duplicates_dropped = 0
no_id = 0

now = time.time()

for msg in consumer:
    ev = msg.value
    eid = ev.get("event_id")
    ev_ts = ev.get("ts", int(time.time()))
    processing_ts = int(time.time())

    # Evict stale entries from dedup cache (rolling TTL)
    stale_keys = [k for k, v in dedup_cache.items() if processing_ts - v > DEDUP_WINDOW_S]
    for k in stale_keys:
        del dedup_cache[k]
        dedup_evictions += 1

    if not eid:
        no_id += 1
        consumer.commit()
        continue

    if eid in dedup_cache:
        # Duplicate: drop silently
        duplicates_dropped += 1
    else:
        # First time seeing this event_id
        dedup_cache[eid] = processing_ts
        processed += 1

    consumer.commit()

consumer.close()

print(f"    Total consumed:       {processed + duplicates_dropped + no_id}")
print(f"    Processed (unique):   {processed}")
print(f"    Dropped (duplicates): {duplicates_dropped}")
print(f"    No event_id:          {no_id}")
print(f"    Cache evictions:      {dedup_evictions}")
print(f"    Final cache size:     {len(dedup_cache)}")
print()

# ─────────────────────────────────────────────────────────────────────────────
# Demonstrate dedup by (event_id + event_time) composite key
# ─────────────────────────────────────────────────────────────────────────────
print("  Composite dedup key: (event_id, event_time):")
print("  This catches cases where two events share an ID but are genuinely different.")

composite_events = [
    {"event_id": "SHARED-ID-001", "ts": 1000, "data": "event at ts=1000"},
    {"event_id": "SHARED-ID-001", "ts": 2000, "data": "different event, same ID, different ts"},
    {"event_id": "SHARED-ID-001", "ts": 1000, "data": "true duplicate"},  # same ID + ts
]

composite_cache: set[tuple] = set()
for ev in composite_events:
    key = (ev["event_id"], ev["ts"])
    if key in composite_cache:
        print(f"    DROP   key={key}  data={ev['data']!r}")
    else:
        composite_cache.add(key)
        print(f"    ACCEPT key={key}  data={ev['data']!r}")

print()
print("  Nugget 04-04 complete.")
print()
print("  Key takeaways:")
print("    - event_id (UUID) makes deduplication straightforward.")
print("    - In-memory dedup: fast but lost on restart. Add Redis/DB for durability.")
print("    - Rolling TTL cache avoids unbounded memory growth.")
print("    - Commit AFTER dedup check (not before) for correct at-least-once behavior.")
print("    - Composite key (event_id, ts) catches ID collisions from buggy producers.")
print()

