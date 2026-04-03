# Spark Structured Streaming Glossary

## B

**Backpressure** — Automatic rate limiting when processing can't keep up with ingestion.
Spark reduces batch size to prevent memory overflow. Monitor via `inputRowsPerSecond`
vs `processedRowsPerSecond`.
→ *Demonstrated in:* `06_operations_and_tuning/01_operations_and_tuning.py`

**Bronze Layer** — Raw, unmodified data ingested from the source. Schema-on-read.
First layer in the medallion architecture.
→ *Demonstrated in:* `05_kafka_to_lake_patterns/01_kafka_to_lake.py`

## C

**Checkpoint** — Saved query state (offsets, aggregations, state store) to durable storage.
Enables recovery after failure without data loss or duplicates.
→ *Demonstrated in:* `04_reliability_and_recovery/01_reliability_and_recovery.py`

**Complete Output Mode** — Emits all rows every micro-batch. Required for aggregations
without a key. Expensive for large state.
→ *Demonstrated in:* `01_streaming_basics/01_streaming_basics.py`

## E

**Event-Time** — When the event actually happened (timestamp in the data).
Different from processing-time (when Spark received it).
→ *Demonstrated in:* `02_event_time_and_windows/01_event_time_watermark.py`

**Exactly-Once** — Each record is processed exactly once, even after failures.
Requires: replayable source + checkpoint + idempotent sink.
→ *Demonstrated in:* `04_reliability_and_recovery/01_reliability_and_recovery.py`

## G

**Gold Layer** — Aggregated, business-ready metrics. Final layer in medallion architecture.
Updated continuously as new data arrives.
→ *Demonstrated in:* `05_kafka_to_lake_patterns/01_kafka_to_lake.py`

## I

**Idempotent Write** — Writing the same data twice produces the same result.
File sink is naturally idempotent (unique paths per batch).
→ *Demonstrated in:* `04_reliability_and_recovery/01_reliability_and_recovery.py`

## L

**Late Data** — Events that arrive after their expected processing window.
Handled by watermark — events within the window are processed, older ones dropped.
→ *Demonstrated in:* `02_event_time_and_windows/01_event_time_watermark.py`

## M

**Micro-Batch** — Small batch of data processed at each trigger interval.
Typical latency: 1-10 seconds. Balances latency vs throughput.
→ *Demonstrated in:* `06_operations_and_tuning/01_operations_and_tuning.py`

## O

**Offset** — Position in the source stream (Kafka offset, file position).
Committed after each batch — enables exactly-once semantics.

**Output Mode** — What rows to emit: Append (new only), Update (changed only),
Complete (all rows).
→ *Demonstrated in:* `01_streaming_basics/01_streaming_basics.py`

## P

**Processing-Time** — When Spark received the event (system clock).
Different from event-time (when the event happened).

## S

**Silver Layer** — Cleaned, validated, deduplicated data. Second layer in medallion.
Schema enforced, bad records filtered.
→ *Demonstrated in:* `05_kafka_to_lake_patterns/01_kafka_to_lake.py`

**Sliding Window** — Overlapping time windows (e.g., 10-min window every 5 min).
Each event can belong to multiple windows.

**State Store** — Internal storage for stateful operations (dedup, aggregations).
Stored in memory + checkpointed to disk.

**Stateful Operation** — Maintains state across micro-batches (unlike stateless map/filter).
Examples: dropDuplicates, groupBy.agg, stream-stream joins.
→ *Demonstrated in:* `03_stateful_processing/01_stateful_processing.py`

## T

**Trigger** — Controls when micro-batches execute.
- `processingTime="5 seconds"`: fixed interval
- `availableNow=True`: process all available data then stop
- `continuous`: sub-second latency (experimental)
→ *Demonstrated in:* `06_operations_and_tuning/01_operations_and_tuning.py`

**Tumbling Window** — Fixed-size, non-overlapping time windows (e.g., every 5 minutes).
Each event belongs to exactly one window.
→ *Demonstrated in:* `02_event_time_and_windows/01_event_time_watermark.py`

## U

**Update Output Mode** — Emits only rows that changed since the last batch.
Used for stateful aggregations where values update over time.
→ *Demonstrated in:* `03_stateful_processing/01_stateful_processing.py`

## W

**Watermark** — Threshold for late data: `max_event_time - delay`.
Events older than the watermark are dropped. Required to bound state growth.
→ *Demonstrated in:* `02_event_time_and_windows/01_event_time_watermark.py`

---

Last updated: 2026-04-02
