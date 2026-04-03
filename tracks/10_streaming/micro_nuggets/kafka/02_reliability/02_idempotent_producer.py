"""
+==============================================================================+
|  NUGGET 02-02 . Idempotent Producer                                          |
|  Prevent duplicate writes caused by producer retries.                        |
+==============================================================================+

CONCEPTS
--------
  Idempotent Producer:
    With enable_idempotence=True (Kafka >= 0.11), the broker assigns a
    Producer ID (PID) and tracks sequence numbers per partition.
    If a retry sends a duplicate, the broker detects it and deduplicates
    at the broker side -- the consumer never sees the duplicate.

    Requirements:
      - acks must be "all" (enforced automatically)
      - retries must be > 0 (set to a high value automatically)
      - max_in_flight_requests_per_connection must be <= 5

    kafka-python support:
      - kafka-python >= 2.0 supports enable_idempotence=True.
      - This prevents out-of-order messages caused by retries.
      - It does NOT provide full transactional semantics (for that, use
        confluent-kafka with begin_transaction / commit_transaction).

  Application-level idempotency:
    Even without broker-level idempotence, you can achieve idempotent
    consumption by:
      1. Assigning a stable event_id to every event at the SOURCE.
      2. Using UPSERT (INSERT ... ON CONFLICT DO NOTHING) in the sink.
      3. Tracking a seen-set in Redis or a DB for dedup.

  Idempotent sink pattern:
    The downstream sink (database, S3, etc.) must also be idempotent.
    Kafka idempotent producer only deduplicates at the broker level.
    If the consumer processes and writes to a DB, the DB write must also
    be idempotent (e.g., upsert by primary key).

DEMONSTRATION
-------------
  1. Standard producer without idempotence (baseline).
  2. Idempotent producer enabled -- compare settings.
  3. Application-level idempotent sink simulation (upsert pattern).

USAGE
-----
    python 02_idempotent_producer.py
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

from kafka import KafkaProducer

print("\n-- Nugget 02-02: Idempotent Producer --")
print(f"  Broker: {BROKER}")
print()

TOPIC = "lab.reliability.test"

# ─────────────────────────────────────────────────────────────────────────────
# 1. Standard producer (no idempotence)
# ─────────────────────────────────────────────────────────────────────────────
print("  [1] Standard producer (no idempotence):")

standard_producer = KafkaProducer(
    bootstrap_servers=BROKER,
    acks="all",
    retries=3,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    request_timeout_ms=15_000,
)

events_standard = []
for i in range(5):
    ev = {"event_id": str(uuid.uuid4()), "seq": i, "producer": "standard", "ts": int(time.time())}
    events_standard.append(ev)
    meta = standard_producer.send(TOPIC, value=ev).get(timeout=10)
    print(f"    Sent seq={i}  partition={meta.partition}  offset={meta.offset}")

standard_producer.flush()
standard_producer.close()
print()
print("    Risk: if a retry occurs (network glitch), the broker may store TWO")
print("    copies of the same message. Consumer sees duplicates.")
print()

# ─────────────────────────────────────────────────────────────────────────────
# 2. Idempotent producer (enable_idempotence=True)
# ─────────────────────────────────────────────────────────────────────────────
print("  [2] Idempotent producer (enable_idempotence=True):")

try:
    idempotent_producer = KafkaProducer(
        bootstrap_servers=BROKER,
        enable_idempotence=True,        # broker deduplicates retries
        # acks="all" and retries=sys.maxsize are enforced automatically
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        request_timeout_ms=15_000,
    )

    for i in range(5):
        ev = {"event_id": str(uuid.uuid4()), "seq": i, "producer": "idempotent", "ts": int(time.time())}
        meta = idempotent_producer.send(TOPIC, value=ev).get(timeout=10)
        print(f"    Sent seq={i}  partition={meta.partition}  offset={meta.offset}")

    idempotent_producer.flush()
    idempotent_producer.close()
    print()
    print("    [OK] Idempotent producer active.")
    print("    Broker tracks PID + sequence. Retries are deduplicated at broker.")

except Exception as exc:
    print(f"    [WARN] Idempotent producer not available: {exc}")
    print("    This may occur with older broker versions or kafka-python < 2.0.")
    print("    Falling back to application-level idempotency (see [3]).")

print()

# ─────────────────────────────────────────────────────────────────────────────
# 3. Application-level idempotent sink (most portable approach)
#    Simulate an upsert sink that deduplicates by event_id.
# ─────────────────────────────────────────────────────────────────────────────
print("  [3] Application-level idempotent sink (upsert by event_id):")

# Simulate events -- some are genuine retries (same event_id)
FIXED_ID = "IDEM-FIXED-0001"
events_with_retries = [
    {"event_id": str(uuid.uuid4()), "data": "first unique event"},
    {"event_id": FIXED_ID,          "data": "original send"},
    {"event_id": str(uuid.uuid4()), "data": "second unique event"},
    {"event_id": FIXED_ID,          "data": "retry of same event"},  # retry!
    {"event_id": str(uuid.uuid4()), "data": "third unique event"},
    {"event_id": FIXED_ID,          "data": "second retry"},         # retry again!
]

# Sink simulation: dict keyed by event_id (like a DB table with PK = event_id)
sink_db: dict[str, dict] = {}
inserts = 0
skipped = 0

for ev in events_with_retries:
    eid = ev["event_id"]
    if eid not in sink_db:
        sink_db[eid] = ev
        inserts += 1
        print(f"    INSERT  event_id={eid[:12]}...  data={ev['data']!r}")
    else:
        skipped += 1
        print(f"    SKIP    event_id={eid[:12]}...  (duplicate -- idempotent upsert)")

print()
print(f"    Result: {inserts} inserts, {skipped} duplicates skipped")
print(f"    Sink state: {len(sink_db)} unique events")
print()

print("  Nugget 02-02 complete.")
print()
print("  Key takeaways:")
print("    - enable_idempotence=True deduplicates retries at the BROKER level.")
print("    - Broker-level idempotence only covers producer-to-broker path.")
print("    - Application-level idempotency (upsert by event_id) covers the sink.")
print("    - Both layers are often needed for true end-to-end idempotency.")
print()
