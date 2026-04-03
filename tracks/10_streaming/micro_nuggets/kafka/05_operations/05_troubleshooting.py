"""
+==============================================================================+
|  NUGGET 05-05 . Troubleshooting Guide                                        |
|  Diagnostic scripts for common Kafka problems.                               |
+==============================================================================+

COMMON PROBLEMS AND DIAGNOSTICS
---------------------------------
  1. Broker unreachable (NoBrokersAvailable)
  2. Topic not found
  3. Consumer group stuck / lag not decreasing
  4. Messages not being consumed
  5. High rebalance frequency
  6. Message decode errors
  7. Slow consumer (processing bottleneck)

This script runs a full diagnostic sweep and reports on each area.

USAGE
-----
    python 05_troubleshooting.py
"""
from __future__ import annotations

import json
import socket
import sys
import time
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _kafka_connect import BROKER, LAB_TOPICS, probe_broker

print("\n-- Nugget 05-05: Troubleshooting Diagnostics --")
print(f"  Broker: {BROKER}")
print()

print(f"  {'='*60}")
print(f"  DIAGNOSTIC SWEEP")
print(f"  {'='*60}")
print()

issues: list[str] = []
ok: list[str] = []

# ─────────────────────────────────────────────────────────────────────────────
# 1. Broker TCP connectivity
# ─────────────────────────────────────────────────────────────────────────────
print("  [1] Broker TCP connectivity:")
if probe_broker(BROKER):
    ok.append(f"Broker reachable at {BROKER}")
    print(f"    [OK] Broker reachable at {BROKER}")
else:
    issues.append(f"Broker NOT reachable at {BROKER}")
    print(f"    [FAIL] Broker NOT reachable at {BROKER}")
    print(f"    Fix: pwsh D:\\StudyBook\\_infra\\scripts\\infra_up.ps1 -Group streaming")
    print(f"    Then wait 30s and re-run.")
    print()
    print("  Stopping diagnostics -- broker is down.")
    sys.exit(1)
print()

from kafka import KafkaAdminClient, KafkaConsumer, KafkaProducer, TopicPartition
from kafka.errors import KafkaError

# ─────────────────────────────────────────────────────────────────────────────
# 2. Topic existence check
# ─────────────────────────────────────────────────────────────────────────────
print("  [2] Lab topic existence check:")
try:
    consumer_temp = KafkaConsumer(
        bootstrap_servers=BROKER,
        consumer_timeout_ms=3_000,
    )
    existing_topics = set(consumer_temp.topics())
    consumer_temp.close()

    for topic in sorted(LAB_TOPICS.keys()):
        if topic in existing_topics:
            ok.append(f"Topic exists: {topic}")
            print(f"    [OK]     {topic}")
        else:
            issues.append(f"Topic missing: {topic}")
            print(f"    [MISSING] {topic}")

    if any(t not in existing_topics for t in LAB_TOPICS):
        print()
        print(f"    Fix: python 00_setup/01_seed_lab.py")
except Exception as exc:
    issues.append(f"Could not list topics: {exc}")
    print(f"    [FAIL] Could not list topics: {exc}")

print()

# ─────────────────────────────────────────────────────────────────────────────
# 3. Quick produce/consume round-trip test
# ─────────────────────────────────────────────────────────────────────────────
print("  [3] Round-trip produce/consume test:")
DIAG_TOPIC = "lab.raw.events"
DIAG_PAYLOAD = f"diag_{uuid.uuid4().hex[:8]}".encode()

try:
    # Produce
    p = KafkaProducer(
        bootstrap_servers=BROKER,
        acks=1,
        request_timeout_ms=10_000,
    )
    t0 = time.perf_counter()
    future = p.send(DIAG_TOPIC, value=DIAG_PAYLOAD)
    meta = future.get(timeout=10)
    produce_ms = (time.perf_counter() - t0) * 1000
    p.flush()
    p.close()
    ok.append(f"Produce to {DIAG_TOPIC} in {produce_ms:.0f}ms")
    print(f"    [OK] Produce: {produce_ms:.0f}ms  partition={meta.partition}  offset={meta.offset}")

    # Consume from that specific offset
    tp = TopicPartition(DIAG_TOPIC, meta.partition)
    c = KafkaConsumer(
        bootstrap_servers=BROKER,
        group_id=f"diag_{uuid.uuid4().hex[:8]}",
        consumer_timeout_ms=6_000,
    )
    c.assign([tp])
    c.seek(tp, meta.offset)
    t1 = time.perf_counter()
    found = False
    for msg in c:
        if msg.value == DIAG_PAYLOAD:
            consume_ms = (time.perf_counter() - t1) * 1000
            found = True
            break
    c.close()

    if found:
        ok.append(f"Consume from {DIAG_TOPIC} in {consume_ms:.0f}ms")
        print(f"    [OK] Consume: {consume_ms:.0f}ms  round_trip={produce_ms + consume_ms:.0f}ms")
    else:
        issues.append("Consume did not receive sent message within timeout")
        print("    [FAIL] Message not received within 6s timeout")

except Exception as exc:
    issues.append(f"Round-trip test failed: {exc}")
    print(f"    [FAIL] {exc}")

print()

# ─────────────────────────────────────────────────────────────────────────────
# 4. Consumer group lag check
# ─────────────────────────────────────────────────────────────────────────────
print("  [4] Active consumer groups and lag:")
try:
    admin = KafkaAdminClient(bootstrap_servers=BROKER, request_timeout_ms=10_000)
    groups = admin.list_consumer_groups()
    lab_groups = [g for g in groups if not g[0].startswith("__")]
    admin.close()

    if lab_groups:
        print(f"    Found {len(lab_groups)} consumer group(s):")
        for group_id, _ in lab_groups[:10]:  # show max 10
            print(f"      {group_id}")
        if len(lab_groups) > 10:
            print(f"      ... and {len(lab_groups) - 10} more")
    else:
        print("    No active consumer groups found.")
    ok.append(f"Consumer groups listed: {len(lab_groups)}")
except Exception as exc:
    issues.append(f"Could not list consumer groups: {exc}")
    print(f"    [FAIL] {exc}")

print()

# ─────────────────────────────────────────────────────────────────────────────
# 5. Common error reference
# ─────────────────────────────────────────────────────────────────────────────
print("  [5] Common errors and fixes:")

error_table = [
    ("NoBrokersAvailable",          "Broker not reachable",
     "Start streaming stack: pwsh infra_up.ps1 -Group streaming"),
    ("TopicAuthorizationFailed",    "Auth failure",
     "Check broker KAFKA_ALLOW_EVERYONE_IF_NO_ACL_FOUND setting"),
    ("CommitFailedError",           "Rebalance during commit",
     "Consumer was kicked out. Increase session.timeout.ms or max.poll.interval.ms"),
    ("RecordTooLargeException",     "Message > max.message.bytes",
     "Increase message.max.bytes on broker or split the message"),
    ("UnicodeDecodeError",          "Binary garbage in value",
     "Use safe_deserialize wrapper (see 02_reliability/05_poison_message)"),
    ("WinError 10061",              "Windows TCP refused",
     "Docker containers not running. Run infra_up.ps1 -Group streaming"),
]

for err, cause, fix in error_table:
    print(f"    {err}")
    print(f"      Cause: {cause}")
    print(f"      Fix:   {fix}")
    print()

# ─────────────────────────────────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────────────────────────────────
print(f"  {'='*60}")
print(f"  DIAGNOSTIC SUMMARY")
print(f"  {'='*60}")
print(f"  OK:     {len(ok)}")
print(f"  ISSUES: {len(issues)}")
if issues:
    for issue in issues:
        print(f"    - {issue}")
else:
    print("  All diagnostics passed. System looks healthy.")
print()

print("  Nugget 05-05 complete.")
print()
