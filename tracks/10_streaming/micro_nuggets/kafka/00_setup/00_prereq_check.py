"""
+==============================================================================+
|  NUGGET 00-00 . Prerequisite Check                                           |
|  Verify your environment before running any other nugget.                    |
+==============================================================================+

PURPOSE
-------
Checks everything needed is in place:
  1. Python version (>= 3.9)
  2. Required package installed (kafka-python)
  3. Kafka broker TCP reachability (localhost:9092)
  4. Produce + consume smoke test (round-trip message)

WHY KAFKA IS DIFFERENT FROM ATLAS/SNOWFLAKE
--------------------------------------------
  - Kafka is self-hosted (Docker container) -- no cloud account required.
  - No TLS or auth for this local lab stack (PLAINTEXT listener).
  - Connection = just host:port -- no URI, no password.
  - kafka-python is the pure-Python client (no C extensions, beginner-safe).

KAFKA VS TRADITIONAL DATABASES
--------------------------------
  - Kafka stores streams of immutable events (append-only log).
  - No DELETE or UPDATE -- consumers read at an offset and advance forward.
  - Multiple consumers can read the same data independently (each has its own
    offset pointer per consumer group).
  - Kafka retains messages for a configurable retention period even after
    consumers have read them (default 7 days).

USAGE
-----
    python 00_prereq_check.py

EXPECTED OUTPUT
---------------
    -- Kafka Prerequisite Check --

      [OK] Python 3.12.x
      [OK] kafka-python 2.x.x

      Broker config:
        BROKER: localhost:9092
        Source: env_file (.env.local KAFKA_PORT=9092)

      TCP probe to localhost:9092 ...
      [OK] Broker reachable

      Smoke test (produce + consume) ...
      [OK] Round-trip: sent "hello-kafka-<ts>" -> received back

      All prerequisites met. Ready to run nuggets!
"""
from __future__ import annotations

import sys
import time
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _kafka_connect import BROKER, probe_broker, require_broker

print("\n-- Kafka Prerequisite Check --")

# -----------------------------------------------------------------------------
# 1. Python version
# -----------------------------------------------------------------------------
py_ok = sys.version_info >= (3, 9)
status = "OK" if py_ok else "FAIL"
print(f"\n  [{status}] Python {sys.version.split()[0]}  (requires >= 3.9)")
if not py_ok:
    print("  Fix: upgrade Python to 3.9 or newer.")
    sys.exit(1)

# -----------------------------------------------------------------------------
# 2. Package check
#    kafka-python: pure-Python Kafka client.
#    No C extensions, no librdkafka -- works on all platforms out of the box.
# -----------------------------------------------------------------------------
try:
    import kafka
    version = getattr(kafka, "__version__", "unknown")
    print(f"  [OK] kafka-python {version}")
except ImportError:
    print("  [FAIL] kafka-python -- NOT INSTALLED")
    print("         Fix: pip install kafka-python")
    sys.exit(1)

# -----------------------------------------------------------------------------
# 3. Broker config
# -----------------------------------------------------------------------------
print(f"\n  Broker config:")
print(f"    BROKER: {BROKER}")
print(f"    Source: .env.local (KAFKA_PORT) or default 9092")

# -----------------------------------------------------------------------------
# 4. TCP probe
# -----------------------------------------------------------------------------
print(f"\n  TCP probe to {BROKER} ...")
if probe_broker(BROKER):
    print(f"  [OK] Broker reachable")
else:
    print(f"  [FAIL] Broker NOT reachable at {BROKER}")
    print()
    print("  Fix:")
    print("    Start the streaming stack:")
    print(r"      pwsh D:\StudyBook\_infra\scripts\infra_up.ps1 -Group streaming")
    print("    Wait ~30 s, then re-run this check.")
    print("    Confirm at http://localhost:8080 (Kafka UI)")
    sys.exit(1)

# -----------------------------------------------------------------------------
# 5. Smoke test: produce + consume round-trip
# -----------------------------------------------------------------------------
print("\n  Smoke test (produce + consume) ...")
SMOKE_TOPIC = "__prereq_smoke_test__"
payload = f"hello-kafka-{int(time.time())}".encode()

try:
    from kafka import KafkaProducer, KafkaConsumer
    from kafka.admin import KafkaAdminClient, NewTopic
    from kafka.errors import TopicAlreadyExistsError

    # Ensure smoke topic exists
    admin = KafkaAdminClient(bootstrap_servers=BROKER, request_timeout_ms=10_000)
    try:
        admin.create_topics([NewTopic(SMOKE_TOPIC, num_partitions=1, replication_factor=1)])
    except TopicAlreadyExistsError:
        pass
    admin.close()

    # Produce
    producer = KafkaProducer(
        bootstrap_servers=BROKER,
        acks=1,
        request_timeout_ms=10_000,
    )
    future = producer.send(SMOKE_TOPIC, value=payload)
    record_metadata = future.get(timeout=10)
    producer.flush()
    producer.close()

    # Consume
    consumer = KafkaConsumer(
        SMOKE_TOPIC,
        bootstrap_servers=BROKER,
        group_id=f"prereq_smoke_{uuid.uuid4().hex[:8]}",
        auto_offset_reset="earliest",
        consumer_timeout_ms=8_000,
        enable_auto_commit=False,
    )
    received = None
    for msg in consumer:
        if msg.value == payload:
            received = msg.value
            break
    consumer.close()

    if received:
        print(f"  [OK] Round-trip: sent {payload!r} -> received back")
    else:
        print("  [FAIL] Consumer did not receive the smoke message within timeout.")
        print("         This may indicate broker startup is still in progress.")
        print("         Wait 15 s and retry.")
        sys.exit(1)

except Exception as exc:
    print(f"  [FAIL] Smoke test error: {exc}")
    print()
    print("  Common causes:")
    print("    - Broker just started: wait 20-30 s and retry")
    print("    - Wrong KAFKA_PORT in .env.local")
    print("    - Another process holding port 9092")
    sys.exit(1)

print()
print("  All prerequisites met. Ready to run nuggets!")
print()
