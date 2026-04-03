"""
+==============================================================================+
|  NUGGET 04-02 . Sliding Window Aggregation                                   |
|  Overlapping windows for smoothed, continuously updated metrics.             |
+==============================================================================+

CONCEPTS
--------
  Sliding Window:
    Fixed-size window that advances by a slide interval (< window size).
    Events can belong to MULTIPLE windows simultaneously.
    Provides smoother, more frequent results than tumbling windows.

  Parameters:
    window_size:  how long each window spans (e.g., 60 seconds)
    slide_step:   how often a new window starts (e.g., 15 seconds)

  Example: window=60s, slide=15s
    Window 1: [T,    T+60)  -- starts at T
    Window 2: [T+15, T+75)  -- starts at T+15
    Window 3: [T+30, T+90)  -- starts at T+30
    ...
    An event at T+40 belongs to windows 1, 2, and 3.

  Sliding vs. Tumbling:
    - Tumbling: each event in exactly ONE window. Low overlap overhead.
    - Sliding:  each event in MULTIPLE windows. Higher compute, smoother.
    - Use sliding for: moving averages, rate alerts, anomaly detection.

  Hop Window (Session vs. Sliding):
    - Sliding window has fixed size + fixed slide.
    - Session window: gaps between events define window boundaries.
      (Not covered here -- see Kafka Streams / Flink for session windows.)

DEMONSTRATION
-------------
  1. Compute event rate per sliding 60s window with 15s slide.
  2. Show how an event appears in multiple windows.
  3. Detect rate spike (simple alerting).

USAGE
-----
    python 02_sliding_window.py
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

from kafka import KafkaConsumer, KafkaProducer

print("\n-- Nugget 04-02: Sliding Window Aggregation --")
print(f"  Broker: {BROKER}")
print()

TOPIC = "lab.clickstream"
WINDOW_S = 60    # 60-second window
SLIDE_S  = 15    # slide every 15 seconds

# Seed events
print(f"  Seeding events (sliding window: {WINDOW_S}s window, {SLIDE_S}s slide) ...")

producer = KafkaProducer(
    bootstrap_servers=BROKER,
    acks="all",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda k: k.encode("utf-8") if isinstance(k, str) else k,
    request_timeout_ms=15_000,
)

now = int(time.time())
base = now - 2 * WINDOW_S  # start events 2 windows ago

events_seeded = []
for i in range(60):
    ev = {
        "event_id": str(uuid.uuid4()),
        "user_id":  f"user_{i % 5}",
        "ts":       base + i * 2,  # one event every 2 seconds
        "value":    1 + (i % 5),
    }
    events_seeded.append(ev)
    producer.send(TOPIC, key=ev["user_id"], value=ev)

producer.flush()
producer.close()
print(f"    Seeded {len(events_seeded)} events from ts={base} to ts={base + len(events_seeded)*2}")
print()

# Consume all events
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BROKER,
    group_id=f"sliding_window_{uuid.uuid4().hex[:8]}",
    auto_offset_reset="earliest",
    consumer_timeout_ms=6_000,
    value_deserializer=lambda b: json.loads(b.decode("utf-8")),
)

all_events = []
for msg in consumer:
    ev = msg.value
    if "ts" in ev:
        all_events.append(ev)
consumer.close()

all_events.sort(key=lambda e: e["ts"])
if not all_events:
    print("  No events found.")
    sys.exit(0)

ts_min = all_events[0]["ts"]
ts_max = all_events[-1]["ts"]

# ─────────────────────────────────────────────────────────────────────────────
# Compute sliding windows
# ─────────────────────────────────────────────────────────────────────────────
def get_sliding_windows(ts_min: int, ts_max: int, window_s: int, slide_s: int):
    """Generate all (start, end) sliding windows covering [ts_min, ts_max]."""
    first_start = (ts_min // slide_s) * slide_s
    start = first_start
    while start <= ts_max:
        yield (start, start + window_s)
        start += slide_s


print(f"  Sliding window results ({WINDOW_S}s window, {SLIDE_S}s slide):")
print(f"  {'win_start':12}  {'win_end':10}  {'events':8}  {'sum_value':10}  {'rate/min':10}")
print(f"  {'-'*62}")

spike_threshold = 20  # events per window = alert threshold
alert_windows = []

for win_start, win_end in get_sliding_windows(ts_min, ts_max, WINDOW_S, SLIDE_S):
    # Events that fall within this window
    window_events = [e for e in all_events if win_start <= e["ts"] < win_end]
    if not window_events:
        continue
    count = len(window_events)
    total_val = sum(e.get("value", 0) for e in window_events)
    rate_per_min = count / (WINDOW_S / 60)

    spike = " [SPIKE]" if count >= spike_threshold else ""
    print(f"  {win_start:<12}  {win_end:<10}  {count:<8}  {total_val:<10}  {rate_per_min:<10.1f}{spike}")
    if count >= spike_threshold:
        alert_windows.append((win_start, win_end, count))

print()

# ─────────────────────────────────────────────────────────────────────────────
# Show that one event falls in multiple windows
# ─────────────────────────────────────────────────────────────────────────────
if all_events:
    sample_event = all_events[len(all_events) // 2]  # pick a middle event
    containing = [
        (ws, we) for ws, we in get_sliding_windows(ts_min, ts_max, WINDOW_S, SLIDE_S)
        if ws <= sample_event["ts"] < we
    ]
    print(f"  Event ts={sample_event['ts']} belongs to {len(containing)} windows:")
    for ws, we in containing[:5]:
        print(f"    [{ws}, {we})")
    if len(containing) > 5:
        print(f"    ... and {len(containing)-5} more")
    print()

if alert_windows:
    print(f"  [ALERT] {len(alert_windows)} window(s) exceeded threshold of {spike_threshold} events:")
    for ws, we, cnt in alert_windows:
        print(f"    [{ws}, {we}) -- {cnt} events")
    print()

print("  Nugget 04-02 complete.")
print()
print("  Key takeaways:")
print("    - Sliding window: events belong to multiple windows (window/slide ratio).")
print("    - Use for moving averages, rate alerts, anomaly detection.")
print("    - Higher overlap ratio = smoother metrics but more compute.")
print("    - Production: Flink / Kafka Streams have native sliding window APIs.")
print()
