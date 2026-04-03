# Kafka Streaming Micro-Nuggets

Production-grade Kafka fundamentals for Data Engineering interview readiness.
Runnable on Windows with a local Docker Kafka stack.

---

## Quick Start (Copy-Paste)

### Step 1 -- Activate virtual environment

```powershell
cd D:\StudyBook
.\.venv\Scripts\Activate.ps1
```

If you get an execution policy error:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### Step 2 -- Install dependencies

```powershell
pip install --upgrade pip
pip install kafka-python
```

Verify:
```powershell
python -c "import kafka; print(kafka.__version__)"
```

### Step 3 -- Start the Docker streaming stack

```powershell
pwsh D:\StudyBook\_infra\scripts\infra_up.ps1 -Group streaming
```

Wait ~30 seconds for Kafka to fully start.

Check health:
```powershell
pwsh D:\StudyBook\_infra\scripts\infra_health.ps1
```

Confirm Kafka UI is up: http://localhost:8080

### Step 4 -- Run prerequisite check

```powershell
cd D:\StudyBook\tracks\10_streaming\micro_nuggets\kafka
python 00_setup\00_prereq_check.py
```

Expected output:
```
-- Kafka Prerequisite Check --

  [OK] Python 3.12.x
  [OK] kafka-python 2.x.x

  Broker config:
    BROKER: localhost:9092

  TCP probe to localhost:9092 ...
  [OK] Broker reachable

  Smoke test (produce + consume) ...
  [OK] Round-trip: sent b'hello-kafka-...' -> received back

  All prerequisites met. Ready to run nuggets!
```

### Step 5 -- Create topics and seed data

```powershell
python 00_setup\01_seed_lab.py
```

### Step 6 -- Run a single nugget

```powershell
python 01_core_kafka\01_topic_management.py
python 01_core_kafka\02_producer_basics.py
python 01_core_kafka\03_consumer_basics.py
```

### Step 7 -- Run all nuggets

```powershell
python run_all_kafka_nuggets.py
```

With options:
```powershell
# Stop on first failure
python run_all_kafka_nuggets.py --stop-on-fail

# Show output from passing scripts too
python run_all_kafka_nuggets.py --show-pass-output

# Skip setup scripts (topics already exist)
python run_all_kafka_nuggets.py --skip-setup

# Longer timeout per script
python run_all_kafka_nuggets.py --timeout 180
```

### Step 8 -- Reset lab (delete all lab topics)

```powershell
# Preview what would be deleted
python 00_setup\99_reset_lab.py --dry-run

# Actually delete
python 00_setup\99_reset_lab.py --confirm

# Delete and re-seed in one step
python 00_setup\99_reset_lab.py --confirm --reseed
```

### Step 9 -- Stop Docker stack

```powershell
pwsh D:\StudyBook\_infra\scripts\infra_down.ps1 -Group streaming
```

---

## Folder Structure

```
kafka/
  _kafka_connect.py              Shared Kafka connection helper (no secrets needed)
  run_all_kafka_nuggets.py       Run-all runner with PASS/FAIL output
  KAFKA_GLOSSARY.md              Plain-English definitions of all key terms
  KAFKA_SPEEDY_STORY_AND_INTERVIEW.md  Story + 30+ interview Q&A
  README.md                      This file

  00_setup/
    00_prereq_check.py           Python version, kafka-python, broker probe, smoke test
    01_seed_lab.py               Create topics + seed starter messages (idempotent)
    99_reset_lab.py              Delete all lab.* topics (requires --confirm)

  01_core_kafka/
    01_topic_management.py       Create, list, describe, delete topics
    02_producer_basics.py        Keys, partitioning, acks, callbacks, batching
    03_consumer_basics.py        Offsets, consumer groups, manual commit
    04_ordering_guarantees.py    Per-partition ordering, keyed vs. unkeyed

  02_reliability/
    01_at_least_once_demo.py     Duplicate simulation + dedup fix
    02_idempotent_producer.py    Broker-level + application-level idempotency
    03_retry_backoff.py          Exponential backoff, producer retries, DLQ routing
    04_dead_letter_topic.py      DLQ pattern: route, inspect, replay
    05_poison_message_handling.py  Binary garbage, schema errors, crash-loop fix

  03_schema_and_contracts/
    01_json_envelope.py          Standard envelope + event-type routing
    02_versioned_schema.py       v1/v2 backward-compatible evolution
    03_contract_validation.py    Producer-side + consumer-side validation

  04_stream_processing_patterns/
    01_tumbling_window.py        Fixed non-overlapping buckets
    02_sliding_window.py         Overlapping windows, rate alerts
    03_watermark_late_events.py  Watermark-based window closing, side output
    04_dedup_by_event_id.py      Rolling TTL dedup cache
    05_out_of_order_events.py    Detection + reorder buffer

  05_operations/
    01_consumer_lag.py           Lag = end_offset - committed_offset per partition
    02_rebalance_notes.py        Triggers, listener hooks, tuning params
    03_partition_skew.py         Hot-key detection + composite key fix
    04_throughput_counters.py    msg/s benchmark, error counters, latency percentiles
    05_troubleshooting.py        Full diagnostic sweep + error reference

  06_interview_drills/
    01_interview_drills.py       12 runnable drills with concise model answers

  07_mini_capstone/
    01_ingest_bronze.py          Raw events -> lab.bronze (with deliberate noise)
    02_clean_to_silver.py        Bronze -> lab.silver (dedup, validate, DLQ)
    03_aggregate_to_gold.py      Silver -> lab.gold (per-user analytics)
    04_failure_injection.py      Poison msg, sink failure, crash recovery demo
```

---

## Service Contract

| Service | Host address | Port |
|---|---|---|
| Kafka broker | localhost | 9092 |
| Zookeeper | localhost | 2181 |
| Kafka UI | http://localhost:8080 | 8080 |
| Container: Kafka | citi_kafka | internal 29092 |
| Container: Zookeeper | citi_zookeeper | 2181 |
| Container: Kafka UI | citi_kafka_ui | 8080 |

---

## Lab Topics

| Topic | Partitions | Purpose |
|---|---|---|
| lab.raw.events | 3 | Raw clickstream / IoT events |
| lab.clean.events | 3 | Validated clean events |
| lab.agg.gold | 1 | Aggregated analytical output |
| lab.reliability.test | 2 | Reliability pattern demos |
| lab.dlq | 1 | Dead Letter Queue |
| lab.orders | 4 | Keyed order events |
| lab.clickstream | 3 | Web clickstream events |
| lab.bronze | 3 | Mini-capstone bronze layer |
| lab.silver | 3 | Mini-capstone silver layer |
| lab.gold | 1 | Mini-capstone gold layer |

---

## Common Errors and Fixes

### Kafka broker unreachable on 9092

```
NoBrokersAvailable: ...
ConnectionError: Kafka broker NOT reachable at localhost:9092
```

Fix:
```powershell
pwsh D:\StudyBook\_infra\scripts\infra_up.ps1 -Group streaming
# Wait 30 seconds, then retry
pwsh D:\StudyBook\_infra\scripts\infra_health.ps1
```

---

### Zookeeper not healthy

The Kafka container depends on Zookeeper being healthy before starting.
If Kafka starts but immediately exits, Zookeeper may not be ready.

Fix:
```powershell
docker logs citi_zookeeper
docker logs citi_kafka
# If needed, restart:
pwsh D:\StudyBook\_infra\scripts\infra_down.ps1 -Group streaming
pwsh D:\StudyBook\_infra\scripts\infra_up.ps1 -Group streaming
```

---

### Topic already exists

```
TopicAlreadyExistsError
```

This is handled gracefully -- seed scripts skip existing topics. Not an error.

---

### Consumer group rebalance delays

```
CommitFailedError: Commit cannot be completed since the group has already rebalanced
```

Fix: increase `max.poll.interval.ms` if processing is slow. Or reduce
`max_poll_records` to process smaller batches faster.

---

### Message decode errors (UnicodeDecodeError / JSONDecodeError)

Means the message payload is not valid UTF-8 JSON. Use the safe deserializer
pattern from `02_reliability/05_poison_message_handling.py`:

```python
try:
    value = json.loads(raw.decode("utf-8"))
except (UnicodeDecodeError, json.JSONDecodeError) as exc:
    # route to DLQ
    pass
```

---

### Windows execution policy (venv activation fails)

```
.\Activate.ps1 cannot be loaded because running scripts is disabled on this system.
```

Fix:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

---

### WinError 10061 (Connection refused)

```
WinError 10061: No connection could be made because the target machine actively refused it
```

Means Docker containers are not running. Start the streaming stack:
```powershell
pwsh D:\StudyBook\_infra\scripts\infra_up.ps1 -Group streaming
```

---

## Dependencies

```
kafka-python    Pure-Python Kafka client. No C extensions, no librdkafka.
                pip install kafka-python
```

No other dependencies required for this lane.

Optional (not used by default):
```
confluent-kafka  High-performance C-extension client.
                 Required for full transactional/exactly-once API.
                 pip install confluent-kafka
```

---

## Next Recommended Phase

After completing the Kafka lane:

1. **Apache Spark Structured Streaming** (`tracks/10_streaming/micro_nuggets/spark/`)
   - Kafka + Spark integration: read streams, apply SQL transformations, write outputs
   - Native tumbling/sliding/session window APIs
   - Checkpointing and fault tolerance

2. **Apache Flink** (if added to the lane)
   - Exactly-once end-to-end with Kafka
   - Native event-time watermarks and late event handling
   - Stateful operators (keyed state, timers)

3. **Kafka Streams** (JVM-based, for Java/Scala track)
   - Stateful stream processing within Kafka
   - KTable, KStream, GlobalKTable
   - Native exactly-once with embedded state stores

4. **Schema Registry** (`tracks/10_streaming/micro_nuggets/schema_registry/`)
   - Avro schema management
   - Producer schema registration
   - Consumer schema resolution by ID
