# Kafka Glossary

Plain-English definitions for every concept in the Kafka micro-nugget lane.

---

## Broker
A single Kafka server process. Receives messages from producers, stores them in
partitions, and serves them to consumers. In production you run 3+ brokers for
redundancy. In this lab: one broker (`citi_kafka`, `localhost:9092`).

## Topic
A named, append-only log. Producers write to topics; consumers read from topics.
Think of it as a persistent message queue where old messages are not deleted
immediately -- they are retained for a configurable period (default 7 days).

## Partition
A subdivision of a topic. Each partition is an ordered, immutable sequence of
records. Partitions enable parallelism: multiple consumers can read different
partitions simultaneously. The number of partitions is set at topic creation and
can only be increased (never decreased without data loss).

## Offset
The sequential position of a record within a partition (0-indexed). Offsets are
monotonically increasing. The consumer tracks its current offset so it knows
where to resume after a restart or rebalance.

## Producer
A client that publishes records to a Kafka topic. The producer decides which
partition to send to -- either via key hash or round-robin.

## Consumer
A client that reads records from a Kafka topic. A consumer reads records in
offset order from one or more partitions.

## Consumer Group
A set of consumers that share a `group_id`. Kafka automatically assigns
partitions across the group so each partition is read by exactly one consumer.
This enables horizontal scaling. Different groups are completely independent --
they each maintain their own offset pointers.

## Rebalance
When the partition assignment within a consumer group changes. Triggered by:
consumers joining/leaving, heartbeat timeout, subscription changes. During
rebalance, all consumers in the group pause until new assignments are made.
Use `CooperativeStickyAssignor` to minimize disruption (incremental rebalance).

## ISR (In-Sync Replica)
The set of replicas that are fully caught up with the partition leader.
`acks="all"` means the producer waits for all ISR replicas to confirm receipt
before considering a send successful. This is the safest durability setting.

## ACKs (Acknowledgment Level)
How many broker confirmations the producer requires before marking a send done:
- `acks=0`: fire-and-forget. Fastest, no durability.
- `acks=1`: leader confirms. Moderate durability.
- `acks="all"` (or `-1`): all ISR replicas confirm. Strongest durability.

## Idempotent Producer
A producer configured with `enable_idempotence=True`. The broker assigns a
Producer ID (PID) and tracks sequence numbers. Retried sends that the broker
already received are silently deduplicated -- the consumer never sees duplicates.
Requires `acks="all"` and `retries > 0`.

## DLQ (Dead Letter Queue)
A Kafka topic where messages that could not be processed are routed. Prevents a
single bad message ("poison message") from blocking the pipeline. A DLQ message
should carry: original topic, partition, offset, failure reason, timestamp,
and retry count.

## Watermark
A timestamp threshold used in stream processing: "no event with event_ts earlier
than this watermark will arrive." Formula: `watermark = max_observed_event_ts -
allowed_lateness`. Windows are closed when the watermark advances past the window
end. Enables correct aggregation of out-of-order event streams.

## Exactly-Once Semantics (EOS)
A delivery guarantee where each message is processed exactly once end-to-end.
Requires: idempotent producer + transactional producer/consumer API.
Complex to implement correctly. Most DE pipelines use at-least-once + idempotent
sink (upsert by event_id) as a practical alternative.

## At-Least-Once
A delivery guarantee where messages are never lost but may be delivered more than
once (duplicates are possible). Achieved with: `acks="all"`, `retries > 0`, and
committing the offset AFTER processing (not before). Consumers must be idempotent.

## At-Most-Once
A delivery guarantee where messages may be lost but are never delivered twice.
Achieved by committing the offset BEFORE processing. Simplest but risks data loss.

## Partition Skew
When some partitions receive significantly more messages than others. Caused by
hot keys (one key accounts for most traffic). Leads to consumer lag on specific
partitions. Fix: composite key (user_id + bucket) or round-robin (null key).

## Consumer Lag
The number of unconsumed messages in a partition for a specific consumer group.
`lag = log_end_offset - committed_offset`. Total lag is the sum across all
partitions. Monitor with Kafka UI (localhost:8080) or `kafka-consumer-groups.sh`.

## Schema Registry
A service (e.g., Confluent Schema Registry) that stores and enforces Avro/JSON/
Protobuf schemas. Each message carries a 4-byte schema ID; consumers fetch the
schema by ID to deserialize. Provides compatibility checking (backward/forward/
full). Not required for this local lab (uses JSON with manual versioning).

## Backward Compatibility
A schema change is backward-compatible if a consumer using the NEW schema can
read data written with the OLD schema. Safe backward-compatible changes:
add optional fields with defaults, remove optional fields.

## Event Envelope
A standard JSON wrapper around every Kafka message payload. Contains metadata:
`event_id`, `event_type`, `schema_version`, `source_service`, `produced_at`,
`trace_id`. Separates routing/versioning metadata from the business payload.

## Tombstone Record
A record with a null value on a compacted topic. Used to signal "delete this key"
to consumers. Kafka log compaction retains the latest record per key; a tombstone
causes that key to eventually be removed from the compacted log.

## Log Compaction
A cleanup policy (`cleanup.policy=compact`) where Kafka retains only the LATEST
record per key. Useful for state stores (latest user profile, latest order status).
Contrast with `delete` policy (retain messages for a time period then delete).

## Linger.ms
Producer configuration: how long the producer waits to accumulate a batch before
sending. `linger_ms=0`: send immediately (lowest latency). `linger_ms=50`: wait
50ms to fill a batch (higher throughput, higher latency).

## Tumbling Window
A fixed-size, non-overlapping time window. Each event belongs to exactly one
window. Window starts at `floor(ts / W) * W`. Use for per-interval totals.

## Sliding Window
A fixed-size window that advances by a smaller slide interval. Events can belong
to multiple windows simultaneously. Use for moving averages and rate metrics.

## Session Window
A window defined by gaps between events (not fixed size). A session ends when
there is no activity for a configurable gap duration. Supported natively in Kafka
Streams and Flink.

## Medallion Architecture
A data quality pattern for streaming pipelines:
- **Bronze**: raw, unvalidated events (store as-is)
- **Silver**: cleaned, deduplicated, validated events
- **Gold**: aggregated, analytical results (ready for dashboards/ML)
