"""
+==============================================================================+
|  NUGGET 05-04 . Throughput and Error Counters                                |
|  Measure producer/consumer throughput and track processing errors.           |
+==============================================================================+

CONCEPTS
--------
  Throughput Metrics:
    - msg/s: messages processed per second
    - bytes/s: bytes processed per second
    - p50/p95/p99 latency: percentile processing latency

  Producer Throughput:
    - Limited by: network, batch_size, linger_ms, acks setting.
    - acks=0 is fastest (no wait). acks="all" is slowest but safest.
    - Compression (gzip/snappy/lz4) reduces bytes but adds CPU.

  Consumer Throughput:
    - Limited by: processing logic speed, commit frequency, network.
    - Parallelism: add consumers to match partition count.
    - batch processing: poll() returns up to max_poll_records at once.

  Error Counters:
    - deserialization_errors: bad payload encoding
    - validation_errors: schema contract violations
    - processing_errors: downstream sink failures
    - dlq_sent: messages routed to DLQ

  Instrumentation Pattern:
    In production: emit metrics to Prometheus/Graphite.
    In this lab: print a rolling metrics summary every N seconds.

USAGE
-----
    python 04_throughput_counters.py
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

from kafka import KafkaConsumer, KafkaProducer

print("\n-- Nugget 05-04: Throughput and Error Counters --")
print(f"  Broker: {BROKER}")
print()

TOPIC = "lab.raw.events"
BATCH = 200

# ─────────────────────────────────────────────────────────────────────────────
# Producer throughput benchmark
# ─────────────────────────────────────────────────────────────────────────────
print(f"  [1] Producer throughput benchmark (N={BATCH}):")

configs = [
    ("acks=0   linger=0ms",   dict(acks=0,     linger_ms=0)),
    ("acks=1   linger=0ms",   dict(acks=1,     linger_ms=0)),
    ("acks=all linger=0ms",   dict(acks="all", linger_ms=0)),
    ("acks=all linger=20ms",  dict(acks="all", linger_ms=20)),
]

ts = int(time.time())
for label, kwargs in configs:
    p = KafkaProducer(
        bootstrap_servers=BROKER,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        request_timeout_ms=15_000,
        **kwargs,
    )
    t0 = time.perf_counter()
    futures = []
    for i in range(BATCH):
        ev = {"seq": i, "ts": ts, "data": "x" * 50}  # ~70 byte payload
        f = p.send(TOPIC, value=ev)
        if kwargs.get("acks") != 0:
            futures.append(f)
    # Wait for all outstanding sends
    if futures:
        for f in futures:
            f.get(timeout=15)
    p.flush()
    elapsed = time.perf_counter() - t0
    p.close()
    rate = BATCH / elapsed
    print(f"    {label}:  {rate:8.0f} msg/s  ({elapsed:.3f}s for {BATCH} msgs)")

print()

# ─────────────────────────────────────────────────────────────────────────────
# Consumer throughput with instrumentation
# ─────────────────────────────────────────────────────────────────────────────
print(f"  [2] Consumer throughput with counters:")

# Counters
counters = {
    "total_consumed": 0,
    "total_bytes": 0,
    "deserialization_errors": 0,
    "validation_errors": 0,
    "processing_errors": 0,
    "successful": 0,
}

latencies: list[float] = []

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BROKER,
    group_id=f"throughput_demo_{uuid.uuid4().hex[:8]}",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    consumer_timeout_ms=6_000,
    max_poll_records=50,
)

t_start = time.perf_counter()
REPORT_EVERY = 100

for msg in consumer:
    t0 = time.perf_counter()
    counters["total_consumed"] += 1
    counters["total_bytes"] += len(msg.value) if msg.value else 0

    try:
        value = json.loads(msg.value.decode("utf-8"))
    except Exception:
        counters["deserialization_errors"] += 1
        continue

    # Simulate light validation
    if not isinstance(value, dict):
        counters["validation_errors"] += 1
        continue

    # Simulate processing
    counters["successful"] += 1
    latencies.append(time.perf_counter() - t0)

    # Rolling report
    if counters["total_consumed"] % REPORT_EVERY == 0:
        elapsed = time.perf_counter() - t_start
        rate = counters["total_consumed"] / elapsed if elapsed > 0 else 0
        print(f"    [{counters['total_consumed']:5d}]  rate={rate:.0f} msg/s  "
              f"bytes={counters['total_bytes']:8}  errors={counters['deserialization_errors']}")

consumer.close()

elapsed_total = time.perf_counter() - t_start
avg_rate = counters["total_consumed"] / elapsed_total if elapsed_total > 0 else 0
bytes_per_s = counters["total_bytes"] / elapsed_total if elapsed_total > 0 else 0

print()
print(f"  [3] Final throughput summary:")
print(f"    total_consumed:        {counters['total_consumed']}")
print(f"    successful:            {counters['successful']}")
print(f"    deserialization_errors:{counters['deserialization_errors']}")
print(f"    validation_errors:     {counters['validation_errors']}")
print(f"    elapsed_s:             {elapsed_total:.2f}")
print(f"    avg_rate:              {avg_rate:.0f} msg/s")
print(f"    throughput:            {bytes_per_s / 1024:.1f} KB/s")

if latencies:
    latencies.sort()
    p50 = latencies[int(len(latencies) * 0.50)] * 1000
    p95 = latencies[int(len(latencies) * 0.95)] * 1000
    p99 = latencies[int(len(latencies) * 0.99)] * 1000
    print(f"    latency p50:           {p50:.2f}ms")
    print(f"    latency p95:           {p95:.2f}ms")
    print(f"    latency p99:           {p99:.2f}ms")

print()
print("  Nugget 05-04 complete.")
print()
print("  Key takeaways:")
print("    - acks=all adds latency but ensures durability.")
print("    - linger_ms > 0 improves throughput by batching multiple sends.")
print("    - Track deserialization_errors, validation_errors separately from processing_errors.")
print("    - In production: emit counters to Prometheus/Datadog/Grafana.")
print()
