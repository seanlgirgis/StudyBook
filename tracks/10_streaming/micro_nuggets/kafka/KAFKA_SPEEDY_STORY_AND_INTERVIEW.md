# Kafka Speedy Story and Interview Guide

Guided storyline from beginner to Data Engineering-ready, with 30+ interview
Q&A linked to runnable nuggets.

---

## The Story: From "What is Kafka?" to Production-Ready

### Chapter 1 -- The Problem Kafka Solves

You work at an e-commerce company. Every second, thousands of users click,
search, and buy. Your analytics team wants real-time dashboards. Your fraud
team wants instant alerts. Your recommendation engine needs user behavior.

The old approach: each system polls the database. The database melts.

The Kafka approach: every user action is an **event** published to a **topic**.
Any system that needs it **subscribes** and reads independently. The producer
does not care about consumers. Consumers do not block each other.

Kafka is a **distributed, replicated, persistent log** of events. It is:
- **Persistent**: messages are stored on disk (not lost on consumer crash)
- **Replicated**: copies on multiple brokers (not lost on broker crash)
- **Scalable**: topics are split into partitions (scale throughput linearly)
- **Decoupled**: producers and consumers are independent

Runnable proof: `00_setup/00_prereq_check.py`

---

### Chapter 2 -- Topics, Partitions, Offsets

A **topic** is a named stream (e.g., `user.behavior.events`).
A topic is split into **partitions** (e.g., 3 partitions). Each partition is
an ordered, immutable sequence of records.

Every record in a partition has an **offset** -- its sequential position.
Consumer A reads offset 0, 1, 2, 3...  Consumer B (different group) also
reads from offset 0, independently.

Key insight: Kafka does not "deliver" messages. Consumers pull and track their
own position. This enables: replaying history, multiple independent readers,
and backpressure-free decoupling.

Runnable: `01_core_kafka/01_topic_management.py`

---

### Chapter 3 -- Producers and Keys

The producer publishes records. A record has:
- **key** (optional): determines which partition the record lands on
- **value**: the payload (usually JSON bytes)
- **timestamp**: when the event occurred

Partitioning rule: `partition = hash(key) % num_partitions`

Without a key: round-robin (balanced, no ordering guarantee).
With a key: same key always goes to same partition (ordering guaranteed per key).

This is why `user_id` is the canonical key for e-commerce events -- all of
Alice's events land in one partition in the order they were produced.

Runnable: `01_core_kafka/02_producer_basics.py`  
Runnable: `01_core_kafka/04_ordering_guarantees.py`

---

### Chapter 4 -- Consumers and Consumer Groups

The consumer reads from topics. A **consumer group** (shared `group_id`) splits
partitions across instances:
- 1 consumer: reads all 3 partitions
- 3 consumers: one partition each (maximum parallelism)
- 5 consumers: 3 active, 2 idle (can't exceed partition count)

Each consumer in a group reads a disjoint set of partitions.
Different groups are completely independent -- both read the full topic.

Runnable: `01_core_kafka/03_consumer_basics.py`

---

### Chapter 5 -- Delivery Semantics

**At-most-once**: commit before processing. Risk: data loss if crash between
commit and processing. Use for non-critical logs/metrics.

**At-least-once**: commit after processing. Risk: duplicates if crash between
processing and commit (consumer re-reads on restart). Most common in DE pipelines.

**Exactly-once**: idempotent producer + transactional API. Eliminates duplicates
end-to-end. Complex; use for billing/financial systems.

The practical approach for most DE pipelines:
- Use at-least-once
- Assign UUID `event_id` to every event at the source
- Deduplicate by `event_id` at the sink (upsert / INSERT IGNORE)

Runnable: `02_reliability/01_at_least_once_demo.py`  
Runnable: `02_reliability/02_idempotent_producer.py`

---

### Chapter 6 -- Reliability Patterns

**Dead Letter Queue (DLQ)**: route messages that repeatedly fail to a separate
topic. Prevents one bad message from blocking the pipeline. Monitor DLQ lag
and alert on non-zero messages.

**Retry with backoff**: `wait = base * 2^attempt + jitter`. Handles transient
failures without thundering herd.

**Poison message**: a message that consistently crashes the consumer. Track
failure count per (topic, partition, offset). After N failures, DLQ it.

Runnable: `02_reliability/03_retry_backoff.py`  
Runnable: `02_reliability/04_dead_letter_topic.py`  
Runnable: `02_reliability/05_poison_message_handling.py`

---

### Chapter 7 -- Schema and Contracts

Every Kafka event should carry an **event envelope**:
```json
{
  "event_id":       "uuid",
  "event_type":     "commerce.order.placed",
  "schema_version": 2,
  "source_service": "order_service",
  "produced_at":    "2025-01-01T00:00:00Z",
  "payload":        { ... }
}
```

**Schema evolution**: only make backward-compatible changes (add optional fields
with defaults). Never rename or remove required fields without a migration plan.
Include `schema_version` so consumers can branch on version.

For strict schema enforcement in production: use Confluent Schema Registry with
Avro, Protobuf, or JSON Schema.

Runnable: `03_schema_and_contracts/01_json_envelope.py`  
Runnable: `03_schema_and_contracts/02_versioned_schema.py`  
Runnable: `03_schema_and_contracts/03_contract_validation.py`

---

### Chapter 8 -- Stream Processing Patterns

**Tumbling window**: fixed non-overlapping buckets. "Sales per 60-second period."
Each event belongs to exactly one window.

**Sliding window**: overlapping windows advancing by a slide interval. "5-minute
rolling average, updated every 1 minute." Event belongs to multiple windows.

**Watermark**: `watermark = max_event_ts - allowed_lateness`. Windows close
when watermark passes `window_end`. Handles late/out-of-order events correctly.

**Deduplication**: track seen `event_id`s. Use in-memory set (lost on restart)
or Redis TTL set (durable). Evict stale entries to bound memory.

Runnable: `04_stream_processing_patterns/01_tumbling_window.py`  
Runnable: `04_stream_processing_patterns/03_watermark_late_events.py`  
Runnable: `04_stream_processing_patterns/04_dedup_by_event_id.py`

---

### Chapter 9 -- Operations

**Consumer lag** = `log_end_offset - committed_offset`. Total lag is the primary
health metric. Alert when lag trends upward. Fix: add consumers or optimize
processing.

**Partition skew**: some partitions get far more messages. Root cause: hot key.
Fix: composite key (`user_id + bucket`) or null key (round-robin, no ordering).

**Rebalance**: all consumers pause. Use `CooperativeStickyAssignor` for
incremental rebalance (only affected partitions move). Commit offsets in
`on_partitions_revoked` to avoid re-reads.

Runnable: `05_operations/01_consumer_lag.py`  
Runnable: `05_operations/02_rebalance_notes.py`  
Runnable: `05_operations/03_partition_skew.py`

---

## 30+ Interview Q&A

### Core Concepts

**Q1: What is Kafka and when would you use it?**  
A: Kafka is a distributed, replicated, persistent event log. Use it when you
need: high-throughput event streaming, decoupled producer-consumer architecture,
event replay, or fan-out (multiple consumers reading the same events). Common
use cases: clickstream, CDC (Change Data Capture), log aggregation, microservice
event bus.

> Runnable: `01_core_kafka/01_topic_management.py`

---

**Q2: How does Kafka guarantee message ordering?**  
A: Ordering is guaranteed within a single partition only. Use a consistent key
so related events hash to the same partition. Global ordering (across partitions)
is not guaranteed. For strict global ordering: use a single-partition topic
(sacrifices parallelism).

> Runnable: `01_core_kafka/04_ordering_guarantees.py`

---

**Q3: What is a consumer group and how does partition assignment work?**  
A: A consumer group is a set of consumers sharing a `group_id`. Kafka's group
coordinator assigns each partition to exactly one consumer in the group. Max
parallelism = number of partitions. Adding more consumers than partitions is
wasteful (excess consumers sit idle).

> Runnable: `01_core_kafka/03_consumer_basics.py`

---

**Q4: What is an offset in Kafka? How is it used?**  
A: An offset is the sequential ID of a record within a partition (0-indexed,
monotonically increasing). The consumer commits its current offset to Kafka so
it can resume from the correct position after a restart or rebalance.
`auto_offset_reset="earliest"` starts from the beginning when no offset is
committed.

---

**Q5: What is `auto_offset_reset` and when does it apply?**  
A: Applied when no committed offset exists for the consumer group on a partition.
`earliest`: start from offset 0 (re-read all history). `latest`: start from the
current end (only consume new messages). In lab scripts use `earliest` to replay;
in production consumers typically use `latest`.

---

### Delivery Semantics

**Q6: What are the three Kafka delivery semantics?**  
A: At-most-once (commit before processing; data loss possible, no duplicates).
At-least-once (commit after processing; no data loss, duplicates possible).
Exactly-once (idempotent producer + transactions; no loss, no duplicates; complex).

> Runnable: `02_reliability/01_at_least_once_demo.py`

---

**Q7: How do you achieve at-least-once semantics in a Kafka consumer?**  
A: Set `enable_auto_commit=False`, process the message, then call `consumer.commit()`.
If the consumer crashes between processing and commit, the message is re-read on
restart. The downstream sink must handle duplicates (upsert by event_id).

---

**Q8: What is the idempotent producer and when should you use it?**  
A: `enable_idempotence=True` causes the broker to assign a Producer ID and track
sequence numbers. Retried sends are deduplicated at the broker -- consumers never
see duplicates from producer retries. Use when `retries > 0` and you need
broker-level dedup (still need application-level dedup for the sink).

> Runnable: `02_reliability/02_idempotent_producer.py`

---

**Q9: How do you implement exactly-once semantics?**  
A: Requires: idempotent producer + transactional producer (`begin_transaction`,
`commit_transaction`) + consumer with `isolation.level=read_committed`. This
ensures atomic consume-process-produce. Practical alternative: at-least-once +
idempotent sink (upsert by event_id in the database). The latter is simpler and
correct for most DE use cases.

---

**Q10: What is a Dead Letter Queue in Kafka and what goes in it?**  
A: A topic where messages that could not be processed are routed after exhausting
retries. DLQ messages should contain: original_topic, original_partition,
original_offset, original_payload, failure_reason, failure_ts, retry_count.
Monitor DLQ lag and alert on non-zero messages. Fix root cause, then replay.

> Runnable: `02_reliability/04_dead_letter_topic.py`

---

**Q11: What is a poison message? How do you handle it?**  
A: A message that consistently crashes the consumer. Track failure count per
(topic, partition, offset). After N failures (e.g., 3), send to DLQ and commit
the offset (advance past it). Without this, the consumer enters an infinite
restart loop.

> Runnable: `02_reliability/05_poison_message_handling.py`

---

### Reliability and Retries

**Q12: What retry strategy should a consumer use?**  
A: Exponential backoff with jitter: `wait = base * 2^attempt + random(0, base)`.
Retry transient errors (network, timeout). Send to DLQ after N failures or
immediately for permanent errors (bad schema, null required field).

> Runnable: `02_reliability/03_retry_backoff.py`

---

**Q13: What happens if acks=1 and the leader crashes immediately after acknowledging?**  
A: The message may be lost. The leader acknowledged before replicating to
followers. If the leader crashes before replication, the new leader won't have
this message. Solution: `acks="all"` ensures all ISR replicas confirm before
the producer considers the send successful.

---

### Schema and Contracts

**Q14: What is a schema event envelope?**  
A: A standard JSON wrapper around every Kafka message. Fields: `event_id` (UUID
for dedup), `event_type` (namespaced: "commerce.order.placed"), `schema_version`
(integer), `source_service`, `produced_at` (ISO-8601 UTC). The business payload
is nested under `payload`. Enables routing, versioning, and observability.

> Runnable: `03_schema_and_contracts/01_json_envelope.py`

---

**Q15: What is backward-compatible schema evolution?**  
A: Adding optional fields with defaults is backward-compatible: a consumer using
the new schema can read old messages (uses the default). Breaking changes: rename
a field, change a field type, add a required field with no default. Always include
`schema_version` so consumers can branch on version.

> Runnable: `03_schema_and_contracts/02_versioned_schema.py`

---

**Q16: What is the Confluent Schema Registry and when do you need it?**  
A: A service that stores and enforces Avro/JSON/Protobuf schemas. Producers
register schemas; consumers fetch schema by ID (embedded in message header).
Provides automatic compatibility checking. Not required for JSON with manual
versioning (this lab), but essential for Avro at scale.

---

### Stream Processing

**Q17: What is a tumbling window vs. a sliding window?**  
A: Tumbling window: fixed size, non-overlapping. Each event in exactly one window.
Use for per-interval totals (sales per hour). Sliding window: fixed size, advances
by a smaller slide interval. Events belong to multiple windows. Use for moving
averages and smoothed rate metrics.

> Runnable: `04_stream_processing_patterns/01_tumbling_window.py`  
> Runnable: `04_stream_processing_patterns/02_sliding_window.py`

---

**Q18: What is a watermark in stream processing?**  
A: A timestamp threshold: "no event with event_ts < watermark will arrive."
Formula: `watermark = max_observed_event_ts - allowed_lateness`. Windows close
when watermark passes window_end. Allows aggregating out-of-order event streams
correctly without waiting forever.

> Runnable: `04_stream_processing_patterns/03_watermark_late_events.py`

---

**Q19: How do you handle late events (event time before current watermark)?**  
A: Options: (1) Drop: simplest, acceptable for non-critical metrics. (2) Update:
re-emit the window with late data included. (3) Side output: route to a late-events
topic for manual reconciliation. The choice depends on accuracy requirements and
state management budget.

---

**Q20: How do you deduplicate Kafka messages?**  
A: Assign a UUID `event_id` at the source. On consume, check a seen-set before
processing. If seen: drop. If new: process and add to seen-set. Use in-memory set
for short windows (lost on restart) or Redis TTL SET for durable dedup. Use TTL
to evict stale entries and bound memory growth.

> Runnable: `04_stream_processing_patterns/04_dedup_by_event_id.py`

---

### Operations

**Q21: How do you measure consumer lag?**  
A: `lag = log_end_offset - committed_offset` per partition. Total lag = sum.
Measure with: `kafka-consumer-groups.sh --describe`, Kafka UI at localhost:8080,
or `consumer.end_offsets()` + `consumer.committed()` in Python. Alert when lag
exceeds threshold or trends upward.

> Runnable: `05_operations/01_consumer_lag.py`

---

**Q22: What triggers a Kafka consumer rebalance?**  
A: Consumer joins the group, consumer leaves/crashes, consumer misses heartbeat
within `session.timeout.ms`, consumer's `poll()` gap exceeds
`max.poll.interval.ms`, topic partition count changes, subscription changes.

---

**Q23: How do you minimize rebalance impact?**  
A: Use `CooperativeStickyAssignor` for incremental rebalance (only moves affected
partitions). Commit offsets in `on_partitions_revoked()`. Tune
`max.poll.interval.ms` for slow processors. Deploy consumers in rolling fashion.

> Runnable: `05_operations/02_rebalance_notes.py`

---

**Q24: What is partition skew and how do you fix it?**  
A: When some partitions receive far more messages than others. Caused by hot keys.
The consumer assigned that partition falls behind while others sit idle.
Fix: composite key (`user_id + bucket`) spreads the hot user across N partitions.
Or: use null key (round-robin, gives up per-key ordering).

> Runnable: `05_operations/03_partition_skew.py`

---

**Q25: How many partitions should a topic have?**  
A: Rule of thumb: `partitions = target_throughput / throughput_per_partition`.
A single partition handles ~10-100 MB/s. More partitions = more parallelism but
also more overhead (leader elections, open files, metadata). Start at 3-6.
You can increase partitions later but not decrease without data loss.

---

**Q26: How do you tune linger_ms and batch_size for throughput?**  
A: `linger_ms > 0` causes the producer to wait before sending, accumulating a
larger batch. Higher `batch_size` (bytes) allows larger batches.
Trade-off: higher latency but much higher throughput (10-100x).
For real-time dashboards: low linger_ms. For bulk ingestion: high linger_ms.

> Runnable: `05_operations/04_throughput_counters.py`

---

### Architecture and Design

**Q27: How would you design a real-time fraud detection pipeline with Kafka?**  
A: (1) Transaction events published to `transactions.raw` (key=account_id).
(2) Fraud detection consumer reads with low latency (acks=1, no linger).
(3) Sliding window aggregates per account: txn count and sum in 5 min.
(4) If threshold exceeded: publish alert to `fraud.alerts`.
(5) Alert consumer notifies security team and blocks card via API call.
(6) Failed fraud checks -> DLQ for investigation.
(7) Use `CooperativeStickyAssignor` for zero-downtime deploys.

---

**Q28: What is the Medallion Architecture in a Kafka context?**  
A: Bronze: raw, unvalidated events from producers (store as-is, never reject).
Silver: clean, deduplicated, validated events (DLQ for bad data).
Gold: aggregated analytical results ready for dashboards/ML.
Each layer is a separate set of topics. Consumers process bronze -> silver ->
gold in pipelines.

> Runnable: entire `07_mini_capstone/` sequence

---

**Q29: How does Kafka compare to RabbitMQ or AWS SQS?**  
A: Kafka: persistent log, replay-able, high throughput, partitioned parallelism,
consumer-controlled offsets. Best for: streaming, audit log, event sourcing.
RabbitMQ: traditional message queue, message deleted after consumer ACK,
flexible routing (exchanges), lower throughput. Best for: task queues, RPC.
SQS: managed queue, at-least-once, no replay, auto-scaling. Best for: AWS-native
decoupling, simple task queues.

---

**Q30: What is log compaction and when do you use it?**  
A: `cleanup.policy=compact`: Kafka retains only the LATEST record per key.
Older records with the same key are eventually deleted. Use for state stores:
latest user profile, latest order status, configuration values.
A null-value record (tombstone) signals deletion of that key.
Contrast with `delete` policy: retain for a time period regardless of key.

---

**Q31: How does Kafka handle consumer crash and recovery?**  
A: The consumer commits its offset to Kafka. On restart, it reads the last
committed offset and continues from there. With `enable_auto_commit=True`:
offsets commit every `auto_commit_interval_ms` (default 5s). With manual commit:
offsets commit exactly when you call `consumer.commit()`. No data is lost as long
as offsets were committed before the crash.

> Runnable: `07_mini_capstone/04_failure_injection.py`

---

**Q32: What is the difference between event time and processing time?**  
A: Event time: when the event ACTUALLY HAPPENED (embedded in the payload as `ts`).
Processing time: when Kafka received/processed the event (broker timestamp).
These differ due to: network delays, mobile offline mode, clock skew, retries.
Stream processors should use event time for correct aggregations. kafka-python
requires manual watermark tracking; Flink/Kafka Streams handle it natively.

> Runnable: `04_stream_processing_patterns/03_watermark_late_events.py`

---

## Quick Reference: Key Configurations

| Setting | Recommended Value | Why |
|---|---|---|
| `acks` | `"all"` | Strongest durability |
| `retries` | `5` | Handle transient failures |
| `enable_idempotence` | `True` | Broker-level dedup on retry |
| `linger_ms` | `5-50` | Batching for throughput |
| `auto_offset_reset` | `"earliest"` | Lab scripts replay from start |
| `enable_auto_commit` | `False` | Manual control for at-least-once |
| `session.timeout.ms` | `30000` | Tolerant of slow networks |
| `max.poll.interval.ms` | `300000` | Tolerant of slow processing |
| `partition_assignment_strategy` | `StickyAssignor` | Minimize rebalance impact |

---

## Linked Nuggets by Topic

| Topic | Nugget |
|---|---|
| Setup + prereq check | `00_setup/00_prereq_check.py` |
| Topic create/list/delete | `01_core_kafka/01_topic_management.py` |
| Producer keys + acks | `01_core_kafka/02_producer_basics.py` |
| Consumer groups + offsets | `01_core_kafka/03_consumer_basics.py` |
| Ordering guarantees | `01_core_kafka/04_ordering_guarantees.py` |
| At-least-once + duplicates | `02_reliability/01_at_least_once_demo.py` |
| Idempotent producer | `02_reliability/02_idempotent_producer.py` |
| Retry + backoff | `02_reliability/03_retry_backoff.py` |
| DLQ pattern | `02_reliability/04_dead_letter_topic.py` |
| Poison message handling | `02_reliability/05_poison_message_handling.py` |
| JSON envelope standards | `03_schema_and_contracts/01_json_envelope.py` |
| Schema versioning | `03_schema_and_contracts/02_versioned_schema.py` |
| Contract validation | `03_schema_and_contracts/03_contract_validation.py` |
| Tumbling window | `04_stream_processing_patterns/01_tumbling_window.py` |
| Sliding window | `04_stream_processing_patterns/02_sliding_window.py` |
| Watermarks | `04_stream_processing_patterns/03_watermark_late_events.py` |
| Deduplication | `04_stream_processing_patterns/04_dedup_by_event_id.py` |
| Out-of-order events | `04_stream_processing_patterns/05_out_of_order_events.py` |
| Consumer lag | `05_operations/01_consumer_lag.py` |
| Rebalance | `05_operations/02_rebalance_notes.py` |
| Partition skew | `05_operations/03_partition_skew.py` |
| Throughput metrics | `05_operations/04_throughput_counters.py` |
| Troubleshooting | `05_operations/05_troubleshooting.py` |
| All 12 drills | `06_interview_drills/01_interview_drills.py` |
| Bronze ingest | `07_mini_capstone/01_ingest_bronze.py` |
| Silver clean/dedup | `07_mini_capstone/02_clean_to_silver.py` |
| Gold aggregation | `07_mini_capstone/03_aggregate_to_gold.py` |
| Failure + recovery | `07_mini_capstone/04_failure_injection.py` |
