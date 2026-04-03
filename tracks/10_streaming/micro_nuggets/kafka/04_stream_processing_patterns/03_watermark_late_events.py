"""
+==============================================================================+
|  NUGGET 04-03 . Watermarks and Late Event Handling                           |
|  Close windows correctly when events arrive out of order.                    |
+==============================================================================+

CONCEPTS
--------
  Event Time vs. Processing Time:
    - Event time: when the event ACTUALLY HAPPENED (in the data: ev["ts"]).
    - Processing time: when Kafka RECEIVED / PROCESSED the event.
    - These differ due to: network delay, device clock skew, mobile offline mode.

  Late Event:
    An event whose event_time is earlier than the current watermark.
    Example: window [T, T+60) has already been emitted at T+60+allowance,
    but a new event arrives with ts=T+30. It's late for that window.

  Watermark:
    A moving threshold: "I believe no event with ts < watermark will arrive."
    Watermark = max(observed_event_ts) - allowed_lateness

    Example: max observed ts = 1000, allowed_lateness = 30s
      watermark = 970
      Window [900, 960): can still receive events until watermark > 960.
                         Once watermark > 960, the window is CLOSED.

  Allowed Lateness:
    The grace period after window_end before a window is forced to close.
    Larger = more accurate (fewer dropped late events) but higher state/memory.
    Typical production values: 30s to 5 minutes.

  What to do with late events (past watermark):
    1. DROP: ignore. Simplest, correct for non-critical metrics.
    2. UPDATE: re-emit the window result with the late data included.
    3. SIDE OUTPUT: emit to a "late events" topic for manual reconciliation.

DEMONSTRATION
-------------
  1. Produce events with artificial out-of-order timestamps.
  2. Compute watermark from observed event times.
  3. Classify events as on-time vs. late.
  4. Handle late events via side output topic.

USAGE
-----
    python 03_watermark_late_events.py
"""
from __future__ import annotations

import json
import sys
import time
import uuid
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _kafka_connect import BROKER, require_broker, safe_json_deserializer

require_broker(BROKER)

from kafka import KafkaConsumer, KafkaProducer

print("\n-- Nugget 04-03: Watermarks and Late Event Handling --")
print(f"  Broker: {BROKER}")
print()

TOPIC = "lab.raw.events"
LATE_EVENTS_TOPIC = "lab.dlq"  # reuse DLQ as late-events side-output
WINDOW_S = 60
ALLOWED_LATENESS_S = 30

# ─────────────────────────────────────────────────────────────────────────────
# Seed events with mixed ordering (simulate out-of-order arrival)
# ─────────────────────────────────────────────────────────────────────────────
print(f"  Seeding out-of-order events (W={WINDOW_S}s, allowed_lateness={ALLOWED_LATENESS_S}s):")

producer = KafkaProducer(
    bootstrap_servers=BROKER,
    acks="all",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda k: k.encode("utf-8") if isinstance(k, str) else k,
    request_timeout_ms=15_000,
)

now = int(time.time())
base = now - 3 * WINDOW_S  # 3 windows ago

# Mix of events: mostly in order, some late by varying amounts
event_specs = [
    # (offset_s, is_late, label)
    (10, False, "on_time"),
    (20, False, "on_time"),
    (35, False, "on_time"),
    (50, False, "on_time"),
    (65, False, "on_time"),   # in window 2
    (80, False, "on_time"),
    (95, False, "on_time"),
    (5,  True,  "late_30s"),  # 30s late -- within allowance
    (25, True,  "late_60s"),  # 60s late -- within allowance (marginal)
    (-15, True, "very_late"), # before base -- VERY late (exceeds allowance)
    (110, False, "on_time"),
    (125, False, "on_time"),
]

seeded_events = []
for offset_s, is_late_flag, label in event_specs:
    ev_ts = base + offset_s
    ev = {
        "event_id":  str(uuid.uuid4()),
        "user_id":   "alice",
        "ts":        ev_ts,
        "label":     label,
        "is_late_seed": is_late_flag,
    }
    seeded_events.append(ev)
    producer.send(TOPIC, key="alice", value=ev)

producer.flush()
producer.close()
print(f"    Seeded {len(seeded_events)} events (base_ts={base}):")
for ev in seeded_events:
    print(f"      ts={ev['ts']:8}  label={ev['label']}")
print()

# ─────────────────────────────────────────────────────────────────────────────
# Consume and process with watermark-based window closing
# ─────────────────────────────────────────────────────────────────────────────
print("  Processing with watermark:")

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BROKER,
    group_id=f"watermark_demo_{uuid.uuid4().hex[:8]}",
    auto_offset_reset="earliest",
    consumer_timeout_ms=7_000,
    value_deserializer=safe_json_deserializer,
)

all_events = [msg.value for msg in consumer if isinstance(msg.value, dict) and "ts" in msg.value]
consumer.close()

# Sort by ARRIVAL order (as-is -- this is what the consumer sees)
# In a real system, kafka offset order is the arrival order.
# For demo, we treat list order as arrival order.

watermark = 0
max_event_ts = 0
windows: dict[int, dict] = defaultdict(lambda: {"events": [], "closed": False})

late_events_producer = KafkaProducer(
    bootstrap_servers=BROKER,
    acks=1,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    request_timeout_ms=15_000,
)

on_time_count = late_count = 0

for ev in all_events:
    ts = ev.get("ts", 0)
    win_start = (ts // WINDOW_S) * WINDOW_S

    # Advance watermark
    if ts > max_event_ts:
        max_event_ts = ts
        watermark = max_event_ts - ALLOWED_LATENESS_S

    # Check if the window this event belongs to is still open
    win_end = win_start + WINDOW_S
    if win_end + ALLOWED_LATENESS_S < watermark:
        # Window is CLOSED -- this event is late
        late_count += 1
        side_output = {
            "type": "late_event",
            "original_event": ev,
            "watermark_at_arrival": watermark,
            "target_window": [win_start, win_end],
            "ts_late_by": watermark - win_end,
        }
        late_events_producer.send(LATE_EVENTS_TOPIC, value=side_output)
        print(f"  [LATE]     ts={ts}  win=[{win_start},{win_end})  "
              f"watermark={watermark}  late_by={watermark - win_end}s")
    else:
        on_time_count += 1
        windows[win_start]["events"].append(ev)
        print(f"  [ON-TIME]  ts={ts}  win=[{win_start},{win_end})  watermark={watermark}")

late_events_producer.flush()
late_events_producer.close()

print()
print(f"  On-time: {on_time_count}  Late (side output): {late_count}")
print()
print(f"  Window summaries (based on on-time events):")
for ws in sorted(windows.keys()):
    we = ws + WINDOW_S
    evts = windows[ws]["events"]
    print(f"    [{ws}, {we}): {len(evts)} events")
print()

print("  Nugget 04-03 complete.")
print()
print("  Key takeaways:")
print("    - Event time (ev.ts) != processing time (broker ingestion time).")
print("    - Watermark = max_observed_event_ts - allowed_lateness.")
print("    - Window closes when watermark > window_end.")
print("    - Late events: drop, update window, or side-output (DLQ/late topic).")
print("    - Large allowed_lateness = more accuracy but more memory/state.")
print()

