# Spark Structured Streaming Speedy Story & Interview Guide

## The 30-Second Story

> "Spark Structured Streaming is Spark's high-level streaming API that treats streaming
> like a micro-batch SQL problem. You write DataFrame operations on an unbounded 'streaming
> table' and Spark handles the incremental processing. It supports event-time, watermarks,
> stateful operations, and exactly-once semantics. For data engineers, it's the bridge
> between real-time Kafka ingestion and batch-style data lake transformations."

---

## Core Architecture

```
┌──────────────┐     ┌─────────────────────────┐     ┌──────────────┐
│   Source     │────▶│  Streaming Query        │────▶│   Sink       │
│   (Kafka,    │     │  (micro-batch engine)   │     │  (console,   │
│    files,    │     │                         │     │   parquet,   │
│    socket)   │     │  1. Read offset         │     │   kafka,     │
│              │     │  2. Process batch       │     │   foreach)   │
│              │     │  3. Write output        │     │              │
│              │     │  4. Commit offset       │     │              │
└──────────────┘     └─────────────────────────┘     └──────────────┘
                            │
                     ┌──────▼───────┐
                     │  Checkpoint  │
                     │  (offsets +  │
                     │   state)     │
                     └──────────────┘
```

---

## Key Concepts for Interviews

### 1. Micro-Batch Processing

Spark Structured Streaming processes data in small batches (typically 1-10 seconds).
Each batch reads new data since the last offset, processes it, and writes output.
This gives near-real-time latency with batch-style fault tolerance.

### 2. Event-Time vs Processing-Time

**Event-time:** When the event actually happened (embedded in the data).
**Processing-time:** When Spark received the event (system clock).
Late events are common — event-time processing handles them correctly.

### 3. Watermark

A watermark tells Spark: "don't wait forever for events older than X."
Formula: `watermark = max_event_time - delay_threshold`
Events older than the watermark are dropped, preventing unbounded state growth.

### 4. Output Modes

| Mode | When to Use | What It Emits |
|------|------------|---------------|
| Append | Non-aggregation queries | Only new rows |
| Update | Aggregations with updates | Changed rows only |
| Complete | Full aggregations | All rows every batch |

### 5. Checkpoint

Saves query state (offsets, aggregations, state store) to durable storage.
On restart, the query resumes from the last checkpoint — no data loss.

---

## Deep Interview Questions

### Q: "How does Spark Structured Streaming work?"

> "It treats a streaming data source as an unbounded table. You write standard
> DataFrame operations (filter, groupBy, join) and Spark executes them as
> micro-batches. Each batch reads new data since the last committed offset,
> processes it, writes output, and commits the new offset to checkpoint storage."

### Q: "What's the difference between event-time and processing-time?"

> "Event-time is when the event actually happened (a timestamp in the data).
> Processing-time is when Spark received it (system clock). They differ because
> of network delays, retries, and out-of-order delivery. Event-time is essential
> for correct windowing — you want to group events by when they happened, not
> when they arrived."

### Q: "What is a watermark and why do you need it?"

> "A watermark tells Spark how long to wait for late events. It's calculated as
> max_event_time minus a delay threshold. Events older than the watermark are
> dropped. Without a watermark, state grows unbounded — Spark must keep all
> historical state forever, eventually causing OOM. Watermarks are required for
> stateful streaming to be production-ready."

### Q: "Explain exactly-once semantics in Spark Streaming."

> "Spark guarantees exactly-once processing from source to sink. This means:
> 1. The source must be replayable (Kafka offsets, file positions).
> 2. Checkpoint saves the query state.
> 3. The sink must be idempotent (file sink writes unique paths per batch).
> If the query fails and restarts, it replays from the checkpoint and produces
> the same output — no duplicates, no data loss."

### Q: "How do you handle late-arriving data?"

> "Use event-time with a watermark. The watermark defines how late an event can
> be and still be processed. Events within the watermark window are included in
> aggregations. Events older than the watermark are dropped. For example, a
> 10-minute watermark means events up to 10 minutes late are processed, but
> anything older is discarded."

### Q: "What output mode would you use for a running total?"

> "Update mode. It emits only the rows that changed since the last batch. For a
> running total, each user's total updates when new events arrive. Complete mode
> would emit all users every batch (expensive). Append mode doesn't work for
> aggregations because aggregated rows can change."

### Q: "How do you debug a slow streaming query?"

> "1. Check query.recentProgress for input rate vs processing rate.
> 2. If processedRowsPerSecond < inputRowsPerSecond, you have backpressure.
> 3. Check spark.sql.shuffle.partitions — default 200 is too high for small streams.
> 4. Check checkpoint size — large state means too much data is being tracked.
> 5. Reduce watermark delay if state is growing unbounded."

### Q: "What happens if a streaming query crashes mid-batch?"

> "On restart, Spark reads the checkpoint to find the last committed offset.
> It replays from that offset — the current batch is reprocessed. If the sink
> is idempotent (file sink with unique paths), the reprocessed batch produces
> the same output. This is the exactly-once guarantee."

---

## Quick Reference

```python
# Read stream
df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "topic_name") \
    .option("startingOffsets", "earliest") \
    .load()

# Parse JSON
df = df.selectExpr("CAST(value AS STRING) as json_str") \
       .select(from_json("json_str", schema).alias("data")) \
       .select("data.*")

# Watermark + window
df.withWatermark("event_time", "10 minutes") \
  .groupBy(window("event_time", "5 minutes"), "event_type") \
  .count()

# Write stream
query = df.writeStream \
    .format("parquet") \
    .outputMode("append") \
    .option("checkpointLocation", "/path/to/checkpoint") \
    .option("path", "/path/to/output") \
    .trigger(processingTime="5 seconds") \
    .start()

# Monitor
print(query.lastProgress)    # Latest batch metrics
print(query.recentProgress)  # Last 100 batches
print(query.status)          # Active/idle/terminated
```

---

## Citi Narrative Hook

> "At Citi, we used Spark Structured Streaming for real-time telemetry ingestion.
> Events flowed from Kafka through bronze (raw), silver (validated), and gold
> (aggregated) layers. The watermark pattern was critical — without it, our state
> stores grew unbounded during peak traffic. Checkpoint recovery saved us multiple
> times when worker nodes crashed mid-batch."

---

Last updated: 2026-04-02
