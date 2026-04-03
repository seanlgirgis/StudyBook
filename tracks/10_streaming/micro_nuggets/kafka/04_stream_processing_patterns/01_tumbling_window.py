"""
+==============================================================================+
|  NUGGET 04-01 . Tumbling Window Aggregation                                  |
|  Aggregate events into fixed, non-overlapping time buckets.                  |
+==============================================================================+

CONCEPTS
--------
  Tumbling Window:
    Fixed-size, non-overlapping time window.
    Example: "sum of sales for each 60-second period"
    Window [T, T+60) starts exactly where [T-60, T) ended.
    Every event belongs to EXACTLY ONE window.

  Window Assignment:
    Given event timestamp T and window size W:
      window_start = floor(T / W) * W
      window_end   = window_start + W

  Processing Approaches:
    1. Micro-batch: consume a batch, assign windows, aggregate, emit.
       Simple but has fixed latency = batch interval.
    2. Stateful streaming: maintain running aggregates per window key.
       Kafka Streams / Flink / Spark Structured Streaming do this natively.
       This nugget implements the micro-batch approach with kafka-python.

  Watermark / Closing Windows:
    How do you know a window is "done"?
    Answer: wait for a watermark -- a timestamp threshold after which no
    earlier events are expected. Then emit and evict the window.
    (Watermarks are covered in nugget 04-03.)

DEMONSTRATION
-------------
  1. Seed clickstream events with timestamps spanning several windows.
  2. Assign each event to a 30-second tumbling window.
  3. Aggregate page_view count and total session_duration per window.
  4. Emit aggregated results.

USAGE
-----
    python 01_tumbling_window.py
"""
from __future__ import annotations

import json
import math
import sys
import time
import uuid
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _kafka_connect import BROKER, require_broker

require_broker(BROKER)

from kafka import KafkaConsumer, KafkaProducer

print("\n-- Nugget 04-01: Tumbling Window Aggregation --")
print(f"  Broker: {BROKER}")
print()

TOPIC = "lab.clickstream"
WINDOW_SECONDS = 30  # 30-second tumbling windows

# ─────────────────────────────────────────────────────────────────────────────
# Seed clickstream events spanning ~3 windows
# ─────────────────────────────────────────────────────────────────────────────
print(f"  Seeding clickstream events (spanning ~3 x {WINDOW_SECONDS}s windows) ...")

producer = KafkaProducer(
    bootstrap_servers=BROKER,
    acks="all",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda k: k.encode("utf-8") if isinstance(k, str) else k,
    request_timeout_ms=15_000,
)

# Base time: round down to nearest window boundary, go back 2 windows
now = int(time.time())
window_base = (now // WINDOW_SECONDS) * WINDOW_SECONDS - 2 * WINDOW_SECONDS

pages = ["/home", "/products", "/search", "/checkout", "/account"]
users = ["alice", "bob", "carol", "dave"]
event_count = 0

for i in range(50):
    # Distribute events across 3 windows with irregular spacing
    offset_s = (i * 4) % (WINDOW_SECONDS * 3)
    ev_ts = window_base + offset_s
    ev = {
        "event_id":       str(uuid.uuid4()),
        "user_id":        users[i % len(users)],
        "page":           pages[i % len(pages)],
        "duration_s":     (i % 10) + 1,
        "ts":             ev_ts,
    }
    producer.send(TOPIC, key=ev["user_id"], value=ev)
    event_count += 1

producer.flush()
producer.close()
print(f"    Seeded {event_count} events  window_base={window_base}  W={WINDOW_SECONDS}s")
print()

# ─────────────────────────────────────────────────────────────────────────────
# Window helper
# ─────────────────────────────────────────────────────────────────────────────
def assign_tumbling_window(ts: int, window_s: int) -> tuple[int, int]:
    """Return (window_start, window_end) for an event timestamp."""
    start = (ts // window_s) * window_s
    return start, start + window_s


# ─────────────────────────────────────────────────────────────────────────────
# Consume and aggregate into tumbling windows
# ─────────────────────────────────────────────────────────────────────────────
print(f"  Consuming and aggregating into {WINDOW_SECONDS}s tumbling windows:")

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BROKER,
    group_id=f"tumbling_window_{uuid.uuid4().hex[:8]}",
    auto_offset_reset="earliest",
    consumer_timeout_ms=7_000,
    value_deserializer=lambda b: json.loads(b.decode("utf-8")),
)

# Window accumulators: key = window_start
windows: dict[int, dict] = defaultdict(lambda: {
    "event_count": 0,
    "total_duration_s": 0.0,
    "unique_users": set(),
    "pages": defaultdict(int),
})

total_msgs = 0
for msg in consumer:
    ev = msg.value
    ts = ev.get("ts", 0)
    win_start, win_end = assign_tumbling_window(ts, WINDOW_SECONDS)
    w = windows[win_start]
    w["event_count"] += 1
    w["total_duration_s"] += ev.get("duration_s", 0)
    w["unique_users"].add(ev.get("user_id", "unknown"))
    w["pages"][ev.get("page", "?")] += 1
    total_msgs += 1

consumer.close()

print(f"    Total messages consumed: {total_msgs}")
print()
print(f"  Window Results ({WINDOW_SECONDS}s tumbling):")
print(f"  {'window_start':12}  {'window_end':10}  {'events':8}  {'users':6}  {'avg_dur_s':10}  top_page")
print(f"  {'-'*70}")

for win_start in sorted(windows.keys()):
    w = windows[win_start]
    win_end = win_start + WINDOW_SECONDS
    avg_dur = w["total_duration_s"] / w["event_count"] if w["event_count"] else 0
    top_page = max(w["pages"], key=w["pages"].get) if w["pages"] else "?"
    n_users = len(w["unique_users"])
    print(f"  {win_start:<12}  {win_end:<10}  {w['event_count']:<8}  {n_users:<6}  {avg_dur:<10.1f}  {top_page}")

print()
print("  Nugget 04-01 complete.")
print()
print("  Key takeaways:")
print("    - Tumbling windows: non-overlapping, each event in exactly one window.")
print("    - Window key = floor(ts / W) * W -- deterministic from event timestamp.")
print("    - Aggregate event_count, sums, unique sets per window.")
print("    - Production: use Kafka Streams, Flink, or Spark Structured Streaming.")
print("    - kafka-python micro-batch is fine for low-throughput batch processing.")
print()
