# Interview Questions — Streaming for Data Engineering

> Topics covered: Kafka concepts · consumer groups · CDC · event-driven ingestion · delivery semantics
> Levels: Starter | Mid | Senior | Architect

---

## Kafka Concepts

### Level 1 — Starter

**Q1: In c001_kafka_concepts_demo.py, the `TopicLog` class only allows `append` operations and never modifies existing events. Why is Kafka's log append-only, and what guarantees does this provide?**
What a good answer covers:
- Append-only logs are immutable; once written, an offset's content never changes
- This makes reads safe without locks: multiple consumers can read concurrently without affecting writers
- Replication is simpler: followers just replay the leader's append log
- The trade-off is that corrections must be modeled as new events, not in-place updates
Why this is asked: immutability is Kafka's foundational design choice and drives all downstream architectural decisions.

**Q2: The `Consumer` class in c001_kafka_concepts_demo.py tracks its own `offset`. Explain what an offset is and why each consumer maintains its own.**
What a good answer covers:
- An offset is a monotonically increasing integer that uniquely identifies each message's position within a partition
- Each consumer (group) independently tracks its read position; advancing one consumer's offset does not affect others
- This enables multiple consumers to process the same topic at different speeds — a reporting consumer and a real-time alert consumer can coexist on the same topic
- Offsets are committed back to Kafka (or an external store) so consumers can resume after a restart
Why this is asked: independent offsets are what make Kafka's pub/sub model scalable; this is tested in every Kafka interview.

**Q3: What is a Kafka topic, and how is it different from a queue in a traditional message broker (e.g., RabbitMQ)?**
What a good answer covers:
- A Kafka topic is a durable, ordered, partitioned log; messages are retained for a configurable period regardless of consumption
- A traditional queue delivers each message to exactly one consumer and deletes it after acknowledgment
- Kafka allows multiple independent consumer groups to read the full log; reprocessing is possible by resetting offsets
- Kafka is better suited for event streaming and replay; queues are better for point-to-point task distribution
Why this is asked: contrasting Kafka with traditional queues reveals whether the candidate understands Kafka's design philosophy.

**Q4: What is a Kafka partition, and why does the number of partitions matter for throughput?**
What a good answer covers:
- A partition is an ordered, immutable sub-sequence of a topic; a topic is split across one or more partitions
- Each partition is handled by one consumer instance within a consumer group, enabling parallelism
- More partitions = more parallelism = higher throughput, up to the number of consumer instances
- Trade-off: more partitions increase broker overhead, replication lag, and leader election time on failure
Why this is asked: partition sizing is the primary Kafka capacity planning decision.

### Level 2 — Mid

**Q1: The `Consumer.read` method in c001_kafka_concepts_demo.py reads from `self.offset` and updates it. What is the difference between auto-commit and manual offset commit, and when would you choose each?**
What a good answer covers:
- Auto-commit: Kafka periodically commits the current offset; simple but can commit before processing is complete, leading to message loss on failure
- Manual commit: the application explicitly commits after successfully processing each batch; ensures at-least-once delivery
- For DE pipelines writing to a warehouse, manual commit is standard: commit only after the write succeeds
- Auto-commit is acceptable for stateless consumers (e.g., logging, monitoring) where message loss is tolerable
Why this is asked: offset commit strategy directly determines delivery semantics, a core DE reliability concern.

**Q2: How does Kafka achieve fault tolerance for messages — what happens to data if a broker fails?**
What a good answer covers:
- Each partition has one leader and N-1 replicas on different brokers; the replication factor N is configurable
- Writes go to the leader; followers replicate asynchronously (or synchronously if `acks=all`)
- If the leader fails, one of the in-sync replicas (ISR) is elected as the new leader; no data is lost if `acks=all` was used
- `acks=0`: fire-and-forget, possible data loss; `acks=1`: leader acknowledges, replica lag can cause loss; `acks=all`: safest
Why this is asked: replication and `acks` settings are standard Kafka reliability questions.

**Q3: What is log compaction in Kafka, and how does it differ from time-based retention?**
What a good answer covers:
- Time-based retention deletes all messages older than a configured age (e.g., 7 days), regardless of key
- Log compaction retains the latest message per key indefinitely; older messages with the same key are garbage-collected
- Compacted topics are used for changelog streams and state reconstruction (e.g., a table of current customer records)
- A compacted topic is not suitable for time-series analytics where all historical events are needed; time-based retention is better for that
Why this is asked: log compaction is often confused with retention; understanding the difference shows depth of Kafka knowledge.

**Q4: What does producer `acks=all` combined with `min.insync.replicas=2` guarantee, and what are the availability trade-offs?**
What a good answer covers:
- `acks=all` means the leader waits for all ISRs to acknowledge before responding to the producer
- `min.insync.replicas=2` means at least 2 replicas (including the leader) must be in sync; if fewer are available, the producer write is rejected
- Together they prevent data loss even if one broker fails after the write
- Trade-off: if only one broker is alive, writes are rejected — durability is prioritized over availability
Why this is asked: the interaction between `acks` and `min.insync.replicas` is a frequent senior-level Kafka question tested even at mid level.

### Level 3 — Senior

**Q1: A Kafka topic receives out-of-order events because producers from different geographic regions have clock skew. Your downstream warehouse query requires event-time ordering. How do you handle this?**
What a good answer covers:
- Kafka guarantees order within a partition but not across partitions or across producers with clock skew
- Use event-time watermarks in a stream processor (Flink, Spark Structured Streaming): allow a configurable late-arrival window before closing a time window
- Late events that arrive after the watermark can be routed to a side output / dead-letter table for reconciliation
- In batch: sort by event_time after landing in Bronze; window functions in Silver use event_time, not ingestion_time
Why this is asked: event-time vs. processing-time ordering is a core streaming engineering challenge.

**Q2: Kafka topic partition count cannot easily be decreased. Walk through the process of safely increasing partition count on a production topic without losing data or disrupting consumers.**
What a good answer covers:
- Increasing partition count is non-destructive: existing messages stay in their current partitions; new messages are distributed across all partitions
- Impact on consumers: key-based routing changes — messages with the same key may now go to a different partition, breaking ordering guarantees for that key
- Safe approach: add partitions during a low-traffic window; if key ordering matters, consider creating a new topic with the higher partition count and migrating consumers
- Monitoring: watch consumer lag on all partitions after the change to confirm even distribution
Why this is asked: partition management is a real operational task that reveals production Kafka experience.

**Q3: How does Kafka handle backpressure — what happens when consumers are slower than producers, and how do you detect and respond to this in a DE pipeline?**
What a good answer covers:
- Kafka buffers messages in the partitions; consumers simply lag behind; the producer is never blocked by slow consumers
- Consumer lag (the difference between the latest offset and the committed consumer offset) is the key metric
- Detection: monitor `kafka.consumer.group.lag` via JMX, Confluent Control Center, or `kafka-consumer-groups.sh`
- Response: scale out consumer instances (up to partition count), optimize the processing logic, or increase micro-batch size to reduce per-message overhead
Why this is asked: consumer lag is the primary operational metric for Kafka-based pipelines.

### Level 4 — Architect

**Q1: Design a lambda architecture that uses Kafka as the ingestion backbone, a batch layer (SQL warehouse with window functions from c098_window_functions_demo.py), and a speed layer (stream processor) to serve real-time and historical analytics from a single logical query interface.**
What a good answer covers:
- Kafka is the source of truth for all events; both layers consume from it
- Speed layer: Flink/Spark Streaming reads Kafka, maintains stateful aggregations in a serving store (Redis, Pinot, Druid) for sub-minute latency
- Batch layer: warehouse job reprocesses full Kafka history (or Bronze table) nightly using window functions; results are written to a Gold table
- Query interface: a federated query layer (Trino, Spark SQL) merges batch results with speed-layer results; the speed layer result replaces the batch result for recent time windows
- Operational complexity is high; kappa architecture (stream-only) is often preferred for simpler maintenance
Why this is asked: lambda architecture design is a canonical architect-level streaming question connecting all DE tracks.

**Q2: Your organization needs to ensure that Kafka topics containing PII comply with GDPR right-to-erasure requirements. Design a compliant architecture given that Kafka is an immutable append-only log.**
What a good answer covers:
- Option 1: crypto-shredding — encrypt PII fields per customer with a customer-specific key stored in a key management service; on erasure, delete the key so historical events become undecipherable
- Option 2: topic compaction with tombstone events — produce a tombstone (null value) for the customer's key on deletion; compaction removes all previous values for that key from the log
- Compaction tombstones only work for compacted topics; time-based retention topics require waiting for natural expiry
- Downstream consumers that have already processed the data (Bronze tables, warehouses) require separate erasure pipelines (connecting to c003_cdc_demo.py DELETE event handling)
Why this is asked: GDPR compliance in an immutable log is a real architectural challenge with no perfect solution.

---

## Consumer Groups

### Level 1 — Starter

**Q1: What is a Kafka consumer group, and how does it enable parallel consumption from a topic?**
What a good answer covers:
- A consumer group is a set of consumers that cooperate to consume a topic; each partition is assigned to exactly one consumer in the group at a time
- If a group has fewer consumers than partitions, some consumers handle multiple partitions; if more consumers than partitions, some consumers are idle
- Different consumer groups are completely independent — they each maintain their own offsets and consume the full topic independently
Why this is asked: consumer groups are the basis of Kafka's scalability model.

**Q2: What happens to partition assignments when a new consumer joins or leaves a consumer group?**
What a good answer covers:
- Kafka triggers a rebalance: all partition assignments are revoked and redistributed among the active consumers in the group
- During a rebalance, consumption pauses for all consumers in the group (in the classic rebalance protocol)
- Incremental Cooperative Rebalancing (introduced in Kafka 2.4) reduces disruption by only revoking partitions that need to move
- Rebalances caused by consumer crashes are a common source of processing latency spikes in production pipelines
Why this is asked: rebalances are the main source of consumer group operational issues.

**Q3: If a consumer group has 3 consumers and a topic has 6 partitions, how are partitions distributed? What if there are 8 consumers?**
What a good answer covers:
- 3 consumers / 6 partitions: each consumer gets 2 partitions (with the default RangeAssignor or RoundRobinAssignor)
- 8 consumers / 6 partitions: 6 consumers each get 1 partition; 2 consumers are idle — you cannot have more active consumers than partitions
- The assignment strategy (RangeAssignor, RoundRobinAssignor, StickyAssignor) determines which consumer gets which partitions
Why this is asked: the partition-per-consumer limit is a fundamental constraint that affects capacity planning.

**Q4: How do you reset a consumer group's offsets to reprocess messages from the beginning of a topic?**
What a good answer covers:
- Use `kafka-consumer-groups.sh --reset-offsets --to-earliest --group <group> --topic <topic> --execute`
- The consumer group must be inactive (no running consumers) before resetting offsets
- Resetting to earliest triggers full reprocessing; resetting to a specific offset allows partial reprocessing
- In application code: set `auto.offset.reset=earliest` for new groups; for existing groups, explicit reset is required
Why this is asked: offset reset for reprocessing is a routine DE operational task.

### Level 2 — Mid

**Q1: What is consumer lag and why is it the most important operational metric for a Kafka-based data pipeline?**
What a good answer covers:
- Consumer lag = latest offset in partition − consumer's committed offset; it represents the number of unprocessed messages
- Growing lag means the consumer cannot keep up with the producer; it will eventually fall behind the retention window, causing message loss
- Lag should be monitored per partition, not just per topic — one slow partition can hide behind averaged metrics
- Alert thresholds: absolute lag (e.g., > 100k messages) and age of oldest unprocessed message (e.g., > 30 minutes)
Why this is asked: lag monitoring is the primary on-call concern for anyone operating Kafka pipelines.

**Q2: Describe the StickyAssignor partition assignment strategy and when it is preferable to the default RoundRobinAssignor.**
What a good answer covers:
- StickyAssignor tries to maintain previous partition assignments during rebalances, only moving partitions that need to change
- RoundRobinAssignor reassigns all partitions round-robin after every rebalance, causing unnecessary partition movement
- StickyAssignor reduces rebalance impact: consumers keep their in-flight processing state for retained partitions; no unnecessary cache invalidation
- Prefer StickyAssignor for stateful consumers (e.g., those maintaining per-partition accumulators)
Why this is asked: assignment strategy choice affects pipeline stability under failure scenarios.

**Q3: Two consumer groups read from the same Kafka topic: one writes to a warehouse (batch-style micro-batches) and one triggers real-time alerts. How do you ensure the warehouse consumer's lag does not affect the alert consumer?**
What a good answer covers:
- Consumer groups are independent; the warehouse consumer's lag has zero effect on the alert consumer's offset or throughput
- Both groups can fall behind independently without affecting each other
- The risk is that the warehouse consumer falls so far behind it exceeds the topic's retention period — ensure retention is long enough (at least 2x the maximum expected batch delay)
- Monitor both groups' lag independently; set separate alerting thresholds based on each group's SLA
Why this is asked: the independence of consumer groups is a key Kafka concept that is often misunderstood.

**Q4: What is the role of `__consumer_offsets` in Kafka, and what happens if this internal topic becomes a bottleneck?**
What a good answer covers:
- `__consumer_offsets` is a compacted Kafka topic that stores committed offsets for all consumer groups
- Every offset commit from every consumer group is written to this topic; it is replicated like any other topic
- Bottleneck symptoms: high commit latency, consumer group coordinator timeouts, rebalances triggered by missed heartbeats
- Mitigation: increase the replication factor, reduce commit frequency (commit every N messages instead of every message), or use an external offset store (Redis, database) for high-frequency consumers
Why this is asked: `__consumer_offsets` performance is a real bottleneck in high-throughput Kafka clusters.

### Level 3 — Senior

**Q1: A consumer group processes a partitioned Kafka topic and writes results to a warehouse table partitioned by customer ID. What data skew problems can arise, and how do you mitigate them?**
What a good answer covers:
- If a few high-volume customers dominate the Kafka partition (due to key-based partitioning), those partitions are larger and slower to process
- The consumer assigned to a hot partition becomes the bottleneck; other consumers are idle
- Mitigation: use a salted key (customer_id + suffix) to spread hot keys across more partitions; requires downstream de-salting logic
- Alternative: use a round-robin producer assignment and handle ordering at the consumer level or accept that ordering is by processing time, not event time
Why this is asked: key-based skew is a common production problem in Kafka pipelines with high-cardinality keys.

**Q2: You want to migrate a consumer group from one Kafka cluster to another (e.g., upgrading from on-prem to cloud) with zero message loss and minimal downtime. Describe the migration strategy.**
What a good answer covers:
- Set up MirrorMaker 2 (or Confluent Replicator) to replicate the source topic to the target cluster in real time
- Start the new consumer group on the target cluster; initially, it processes replicated messages in parallel with the source consumer group
- Once the target consumer group is confirmed to be processing correctly and lag is near zero, cut over application producers to the target cluster
- Decommission the source consumer group after a validation window; shut down MirrorMaker
- Offset translation: MirrorMaker 2 maintains an offset mapping between source and target; use this to reset the target consumer group to the correct position
Why this is asked: Kafka cluster migrations are a real senior DE task that requires careful sequencing.

**Q3: How do consumer group heartbeats work, and what configuration parameters control the balance between fast failure detection and unnecessary rebalances?**
What a good answer covers:
- Each consumer sends heartbeats to the group coordinator at `heartbeat.interval.ms` intervals
- If the coordinator does not receive a heartbeat within `session.timeout.ms`, it considers the consumer dead and triggers a rebalance
- `max.poll.interval.ms` is the maximum time between `poll()` calls; exceeding it also triggers a rebalance (designed for slow processing consumers)
- Tuning: `session.timeout.ms` should be 3x `heartbeat.interval.ms`; `max.poll.interval.ms` should be set to the maximum expected processing time per batch
Why this is asked: misconfigured heartbeat/session timeouts cause phantom rebalances that are hard to diagnose.

### Level 4 — Architect

**Q1: Design a consumer group architecture for a pipeline that ingests CDC events (from c003_cdc_demo.py) and applies them to a warehouse table, guaranteeing exactly-once semantics end-to-end.**
What a good answer covers:
- Use Kafka transactions on the producer side: CDC events are produced atomically with `transactional.id` set
- Consumer reads with `isolation.level=read_committed` to skip uncommitted transactional messages
- Warehouse writes are idempotent: use MERGE with the CDC sequence number as a deduplication key; only apply events with a sequence > the last applied sequence stored in a watermark table
- Offset commit and warehouse write are coordinated: commit the Kafka offset only after the warehouse MERGE succeeds (manual commit, at-least-once delivery) + idempotent MERGE (deduplication) = effectively exactly-once
- Failure scenario: if the MERGE succeeds but the offset commit fails, the next run will re-apply the same CDC events; the idempotent MERGE is a no-op for already-applied sequences
Why this is asked: exactly-once end-to-end semantics is one of the most nuanced architect-level streaming questions.

**Q2: Your organization runs 200 independent consumer groups across 50 Kafka topics. How do you design the operational framework for managing, monitoring, and governing consumer groups at scale?**
What a good answer covers:
- Centralized offset and lag monitoring: aggregate all consumer group metrics into a metrics platform (Prometheus + Grafana, Datadog) with per-group dashboards and alerts
- Consumer group registry: a configuration-as-code repository (Git) that declares every consumer group, its topic, and its SLA; deviations trigger alerts
- Access control: use Kafka ACLs to restrict which service accounts can create or modify consumer groups on production topics
- Runbook automation: standardized procedures for common operations (offset reset, scaling consumers, rebalance investigation) implemented as CLI tools or internal APIs
- Connects to orchestration: consumer group health checks are gates in Airflow DAGs — a downstream transformation does not run if the upstream consumer group has excessive lag
Why this is asked: operating Kafka at scale requires organizational tooling, not just technical knowledge.

---

## Change Data Capture (CDC)

### Level 1 — Starter

**Q1: In c003_cdc_demo.py, the `ChangeTable._emit` method produces events with an `op` field set to "INSERT", "UPDATE", or "DELETE". What is CDC and why is it valuable for data pipelines?**
What a good answer covers:
- CDC captures every data modification in a source database and emits it as a stream of change events
- It eliminates the need for full table scans or timestamp-based polling to detect changes
- CDC enables real-time or near-real-time replication, audit trails, and event-driven downstream processing
- The `before` and `after` fields in the demo show the full state change, enabling both auditing and state reconstruction
Why this is asked: CDC is a foundational concept for modern data engineering and is tested in most senior DE interviews.

**Q2: The `_emit` method in c003_cdc_demo.py includes both `before` and `after` images in each event. What are these, and why does an UPDATE event need both?**
What a good answer covers:
- `before` is the row state immediately before the change; `after` is the row state immediately after
- For INSERT: `before` is NULL; `after` is the new row
- For DELETE: `before` is the deleted row; `after` is NULL
- For UPDATE: both are present; `before` enables audit trails (what changed from what), while `after` is used for current-state reconstruction
- Some CDC systems emit only the `after` image (reduced logging mode); this limits auditability
Why this is asked: before/after image semantics are fundamental to understanding CDC event structure.

**Q3: What is the difference between log-based CDC and trigger-based CDC?**
What a good answer covers:
- Log-based CDC reads the database's transaction log (WAL in PostgreSQL, binlog in MySQL, redo log in Oracle) to capture changes without modifying the source schema
- Trigger-based CDC adds database triggers that write change records to an audit table on every INSERT/UPDATE/DELETE
- Log-based is preferred: lower overhead on the source, captures all changes including bulk operations, does not require DDL changes
- Trigger-based has higher overhead and can be missed if triggers are disabled or bypassed
Why this is asked: log-based CDC (Debezium) is the industry standard; candidates should know why.

**Q4: What is a tombstone event in Kafka CDC, and what does it represent?**
What a good answer covers:
- A tombstone is a Kafka message with a non-null key and a null value
- In CDC, a tombstone signals that a record with that key has been deleted
- Log-compacted topics use tombstones to eventually remove all prior messages for that key from the log
- Consumers must handle tombstones explicitly — failing to do so can result in deleted records remaining in downstream systems
Why this is asked: tombstone handling is a common source of bugs in CDC consumers.

### Level 2 — Mid

**Q1: How would you use the CDC events from c003_cdc_demo.py (with seq, op, before, after fields) to reconstruct the current state of the source table in a warehouse?**
What a good answer covers:
- Land all CDC events in a Bronze table preserving all fields including seq, op, before, after
- Apply events in seq order: for INSERT and UPDATE, upsert the `after` image keyed by the primary key; for DELETE, remove or soft-delete the row
- Use a MERGE statement or QUALIFY-based deduplication: `QUALIFY ROW_NUMBER() OVER (PARTITION BY key ORDER BY seq DESC) = 1` then filter out DELETE operations
- Current state is accurate only if all events are applied in order; gaps in seq indicate missing events
Why this is asked: CDC-to-warehouse state reconstruction is a core DE use case.

**Q2: A CDC pipeline falls behind by 2 hours due to a consumer outage. When it recovers, it replays 2 hours of events. What problems can this cause downstream and how do you mitigate them?**
What a good answer covers:
- Downstream consumers that depend on near-real-time data will have stale data for 2 hours, then receive a burst
- If downstream writes are not idempotent, the replay burst may cause duplicate inserts or incorrect aggregations
- Mitigation: ensure all downstream writes are idempotent (MERGE with deduplication key, not INSERT); design dashboards to show data-as-of timestamps, not just latest values
- Backpressure: the burst may overwhelm the warehouse; consider rate-limiting the replay or processing it in a dedicated "catch-up" pipeline
Why this is asked: CDC pipeline recovery is a real operational scenario that tests end-to-end pipeline design thinking.

**Q3: How does Debezium capture changes from PostgreSQL, and what database configuration must be enabled on the source?**
What a good answer covers:
- Debezium reads PostgreSQL's Write-Ahead Log (WAL) using logical replication; it creates a replication slot on the source
- Required: `wal_level = logical` in postgresql.conf; the replication user needs REPLICATION privilege
- Debezium decodes WAL records into CDC events (Kafka messages) without modifying the source schema
- Risk: a replication slot that is not consumed causes WAL files to accumulate indefinitely on the source disk — monitor replication slot lag
Why this is asked: Debezium + PostgreSQL is one of the most common CDC setups; operational knowledge of the configuration is expected.

**Q4: What is initial snapshot in CDC, and why is it necessary when setting up a new CDC pipeline for an existing table?**
What a good answer covers:
- When Debezium (or any CDC tool) starts for the first time, it cannot rely solely on the WAL because the WAL does not contain the full history of the table
- An initial snapshot reads all existing rows from the source table as INSERT events, establishing the baseline state in the target
- During the snapshot, the source table is briefly locked (or a consistent read snapshot is taken) to ensure consistency
- After the snapshot, Debezium switches to streaming from the WAL; the combination gives a complete and consistent initial state
Why this is asked: the snapshot phase is where most first-time CDC deployments encounter issues.

### Level 3 — Senior

**Q1: The `ChangeTable` in c003_cdc_demo.py uses a monotonically increasing `seq` for ordering. In a production distributed CDC system, what can go wrong with ordering and how is it addressed?**
What a good answer covers:
- Distributed systems may have multiple WAL readers (for high availability); events from different readers may arrive out of order
- Network latency between the CDC source and Kafka can cause events from the same table to interleave with events from other tables
- Addressing: use the database's LSN (Log Sequence Number) or transaction ID as the ordering key, not arrival time; sort by LSN in the consumer before applying
- For multi-table CDC streams on a single topic, events from different tables may be interleaved; partition by table + primary key to ensure per-key ordering within a partition
Why this is asked: production CDC ordering problems are subtle and reveal depth of distributed systems knowledge.

**Q2: How do schema changes on the source table (ALTER TABLE ADD COLUMN, DROP COLUMN) affect a CDC pipeline, and what is the role of a schema registry?**
What a good answer covers:
- A new column on the source appears in `after` images after the ALTER; consumers reading the old schema see the new column as unexpected or missing
- A dropped column disappears from `after` images; consumers expecting it will receive NULLs or errors
- Schema registry (Confluent Schema Registry, AWS Glue Schema Registry): stores versioned Avro/Protobuf/JSON schemas; producers register new schemas on change; consumers negotiate schema compatibility
- Compatibility modes: BACKWARD (new schema can read old data), FORWARD (old schema can read new data), FULL (both) — FULL is safest for CDC pipelines
- Debezium emits schema change events; downstream consumers can use these to trigger DDL updates on the target
Why this is asked: schema evolution is the most common production CDC failure mode.

**Q3: You are designing a CDC pipeline for a multi-tenant SaaS database where each tenant has thousands of tables. How do you scale the CDC infrastructure without deploying a Debezium connector per table?**
What a good answer covers:
- One Debezium connector per database (not per table) can capture changes from all tables in that database via WAL
- Use topic routing rules to route changes from different tables to different Kafka topics automatically (Debezium `topic.creation` config and SMTs)
- For multi-tenant where each tenant has its own database, deploy one connector per database but use a shared Kafka cluster and standardized topic naming
- Consumer-side: a single consumer group with a table-routing dispatcher can handle all tenants, applying changes to the correct target tables
Why this is asked: scaling CDC beyond a single table is a real infrastructure design challenge.

### Level 4 — Architect

**Q1: Design an end-to-end CDC pipeline that feeds both a real-time OLAP store (for dashboards) and a data warehouse (for historical analysis), handling schema evolution, late data, and GDPR erasure.**
What a good answer covers:
- Source: Debezium reads PostgreSQL WAL, publishes to Kafka with schema registry (Avro, FULL compatibility)
- Real-time path: Flink reads Kafka, applies CDC events to a stateful table in Apache Pinot or ClickHouse; dashboard queries run against Pinot/ClickHouse with sub-second latency
- Batch path: Kafka CDC events land in Bronze (Delta Lake); Silver layer applies MERGE using CDC seq for deduplication; Gold layer is materialized for analysis
- Schema evolution: schema registry enforces compatibility; Flink and Silver MERGE jobs are updated via rolling deployment when breaking changes are approved
- Late data: CDC seq ordering in Silver; reprocessing window handles out-of-order events
- GDPR erasure: DELETE events in CDC trigger soft-delete flags in both paths; crypto-shredding for Kafka retention; Bronze partition rewrite for physical erasure
Why this is asked: end-to-end CDC architecture connecting real-time and batch paths is the defining architect-level DE question.

**Q2: Your CDC pipeline processes financial transactions. Regulators require a complete, tamper-evident audit trail of every change to every record for 7 years. How does CDC facilitate this, and what additional guarantees are needed?**
What a good answer covers:
- CDC naturally captures every INSERT, UPDATE, DELETE with before/after images — a complete audit trail by design
- Tamper-evidence requires that the audit log itself is immutable: store CDC events in a write-once object store (S3 Object Lock, GCS Retention Policy) or a blockchain-anchored log
- Kafka retention must be set to at least 7 years for the audit topics, or events must be archived to cold storage with the same retention
- Audit queries: a Gold audit table reconstructing the full history of each record (every state transition) enables regulatory queries
- Connecting to warehouse SQL: window functions (c098_window_functions_demo.py) over the CDC event table provide point-in-time state reconstruction for any timestamp
Why this is asked: financial audit trail requirements force candidates to think about immutability, retention, and compliance beyond standard CDC use cases.

---

## Event-Driven Ingestion

### Level 1 — Starter

**Q1: What is event-driven ingestion, and how does it differ from scheduled batch ingestion?**
What a good answer covers:
- Event-driven ingestion triggers a data pipeline when a specific event occurs (file arrives, CDC event emitted, API webhook fires) rather than on a fixed time schedule
- Batch ingestion runs on a schedule (hourly, daily) regardless of whether new data exists
- Event-driven reduces latency (data is processed as it arrives) and avoids wasted compute (no run if no data)
- Trade-off: event-driven pipelines are harder to debug and monitor; scheduled pipelines have predictable resource usage
Why this is asked: event-driven vs. batch is a fundamental architectural choice in DE.

**Q2: What is a Kafka consumer as an event trigger — how can a Kafka message arrival initiate a data pipeline job?**
What a good answer covers:
- A consumer reads a control message (e.g., "file X has landed in S3") and triggers a downstream pipeline job
- The trigger can invoke an Airflow DAG via its REST API, submit a Spark job, or call a serverless function (Lambda, Cloud Functions)
- This pattern decouples the event producer from the pipeline orchestrator; the Kafka topic acts as a durable queue for trigger events
- Back-pressure: if the pipeline is busy, trigger messages accumulate in Kafka and are processed when capacity is available
Why this is asked: Kafka-as-trigger is a common pattern for event-driven DE architectures.

**Q3: What is a dead-letter topic (DLT) in event-driven ingestion, and why is it important?**
What a good answer covers:
- A DLT is a Kafka topic where messages that cannot be processed (malformed, schema mismatch, processing error) are routed instead of being discarded
- Without a DLT, failed messages either block the consumer (if retried indefinitely) or are silently dropped (data loss)
- DLT messages retain the original message plus metadata (error reason, timestamp, consumer ID) for debugging and reprocessing
- Monitoring the DLT message count is a key pipeline health indicator
Why this is asked: dead-letter handling is a production reliability pattern that separates novice from experienced DE candidates.

**Q4: How does an event-driven ingestion pipeline handle idempotency — ensuring that processing the same event twice does not produce duplicate data?**
What a good answer covers:
- Assign a unique event ID to each ingested event at the source; store processed event IDs in a deduplication table or cache
- Before processing, check if the event ID has already been processed; skip if so
- For warehouse writes, use MERGE with the event ID as the deduplication key
- Idempotency is required for at-least-once delivery (the standard Kafka guarantee): events may be redelivered on consumer restart
Why this is asked: idempotency is the key design principle that makes event-driven pipelines reliable.

### Level 2 — Mid

**Q1: Describe the fan-out pattern in event-driven ingestion: a single Kafka event triggers multiple downstream pipelines. What are the operational risks and how do you manage them?**
What a good answer covers:
- Fan-out: multiple independent consumer groups each process the same event for different purposes (warehouse write, real-time alert, ML feature update)
- Risk 1: one slow consumer group does not affect others, but if it falls too far behind, it may exceed topic retention (data loss)
- Risk 2: an error in one consumer group's processing does not automatically alert other groups; each must be monitored independently
- Management: set retention long enough for the slowest consumer; monitor all groups' lag; use DLTs per consumer group for failed events
Why this is asked: fan-out is a common event-driven pattern with non-obvious operational complexity.

**Q2: How do you implement exactly-once event-driven ingestion from an S3 file arrival trigger to a warehouse table?**
What a good answer covers:
- S3 event notification (S3 → SNS → SQS or directly to Lambda) triggers the ingestion job with the file path
- The ingestion job checks a processed-files table before loading; if the file has already been loaded, skip and acknowledge the SQS message
- Load the file to a staging table, then MERGE into the target table using a file-level batch ID as the deduplication key
- Acknowledge the SQS message only after the MERGE succeeds; if the process crashes before acknowledgment, SQS re-delivers the message and the idempotent MERGE is a no-op
Why this is asked: S3-triggered ingestion with exactly-once semantics is a canonical DE pipeline pattern.

**Q3: What is schema-on-read versus schema-on-write in the context of event-driven ingestion, and what are the trade-offs for a data lake?**
What a good answer covers:
- Schema-on-write: validate and cast to a defined schema at ingest time; rejects non-conforming data early; downstream queries are fast because types are known
- Schema-on-read: land raw events as-is (JSON, Avro, raw bytes); apply schema at query time; flexible but slower queries and harder to catch data quality issues early
- For event-driven ingestion: schema-on-write at the Bronze-to-Silver boundary is a common compromise — land raw in Bronze (schema-on-read), validate and type-cast in Silver (schema-on-write)
- Schema registries (Confluent, AWS Glue) enforce schema-on-write at the Kafka producer level for structured event streams
Why this is asked: schema strategy is a fundamental data lake design decision.

**Q4: How do you handle a burst of events that temporarily exceeds the processing capacity of your event-driven ingestion pipeline?**
What a good answer covers:
- Kafka naturally buffers excess events in the partitions; consumers process at their own rate without dropping messages
- Scale out consumers horizontally up to the partition count; auto-scaling (Kubernetes HPA on consumer lag metrics) handles predictable bursts
- For warehouse writes, micro-batch larger chunks during burst to amortize per-write overhead
- If the burst is sustained, it may indicate a need to increase partition count, add consumer instances permanently, or optimize processing logic
Why this is asked: burst handling is a real operational challenge and tests understanding of Kafka's buffering model.

### Level 3 — Senior

**Q1: Design an event-driven ingestion pipeline for a high-volume e-commerce platform that processes 100,000 order events per second with end-to-end latency under 10 seconds to a serving layer.**
What a good answer covers:
- Producers write order events to Kafka with `acks=all`; 50+ partitions on the orders topic for parallelism
- Flink consumer group reads from Kafka, validates schema against registry, enriches events (customer lookup from a broadcast state), writes to Iceberg Bronze within 3-4 seconds of event production
- Silver Flink job: applies business rules (order status normalization, currency conversion), writes to Iceberg Silver within 2-3 seconds
- Serving layer: ClickHouse or Apache Pinot ingests from Kafka directly (bypassing the warehouse) for sub-second dashboard queries
- Warehouse Silver/Gold is eventually consistent (minutes behind); serving layer is real-time; consumers are directed to the appropriate store based on latency requirement
Why this is asked: high-volume, low-latency pipeline design is a realistic architect-level question.

**Q2: A data science team wants to consume raw events from Kafka to build ML training datasets. How do you design the event schema and Kafka topic structure to serve both real-time operational pipelines and batch ML training workloads from the same source?**
What a good answer covers:
- Use a rich event schema (Avro with schema registry) that includes all fields needed by both consumers; avoid stripping fields for brevity
- Separate topics by domain (orders, users, products) so each team subscribes only to relevant topics
- For ML training: create a dedicated consumer group that writes events to a Parquet-based data lake partition; data scientists read from the lake, not directly from Kafka
- Schema compatibility: FULL compatibility in the registry ensures both old and new consumers can read all schema versions
- Replay: configure sufficient retention (30+ days) or archive to S3; data scientists can reprocess historical events by resetting offsets or reading from the archive
Why this is asked: serving multiple consumers from a single Kafka topic requires careful schema and retention design.

**Q3: How do you implement end-to-end data lineage for an event-driven ingestion pipeline spanning Kafka, Bronze, Silver, and Gold layers?**
What a good answer covers:
- Propagate a trace ID (correlation ID) from the source event through every transformation; store it as a column in Bronze, Silver, and Gold tables
- Use an open lineage standard (OpenLineage, Apache Atlas, DataHub) to emit lineage events from each job: "job X read from topic Y, wrote to table Z"
- The lineage graph shows which Gold column was derived from which Kafka topic event field
- For debugging: a bad Gold value can be traced back to the originating Kafka event using the trace ID
Why this is asked: end-to-end lineage is a governance requirement in mature DE organizations.

### Level 4 — Architect

**Q1: Design a multi-region active-active event-driven ingestion architecture where events produced in US-East and EU-West must both be available for global analytics while complying with EU data residency requirements.**
What a good answer covers:
- Two independent Kafka clusters: one in US-East, one in EU-West; producers write to their regional cluster
- EU data residency: EU events must not leave the EU region; EU Kafka events replicate only to EU storage (S3 EU, BigQuery EU)
- US events replicate globally (MirrorMaker 2 or Confluent Replicator from US-East to a global cluster excluding EU-resident fields)
- Global analytics: a federated query engine (Trino, BigQuery Omni) queries both regional Bronze tables; EU-resident PII columns are masked or excluded in the global view
- Event ID deduplication: if a global event touches both regions (e.g., a US user ordering from an EU warehouse), the event must be deduplicated across regions using a global event ID
Why this is asked: multi-region compliance is a real architect challenge connecting streaming, governance, and infrastructure.

**Q2: Your event-driven ingestion pipeline has 15 upstream source systems, each with different event formats, schemas, and reliability characteristics. Design a normalization and quality gate layer that standardizes events before they reach the warehouse.**
What a good answer covers:
- Event gateway: a lightweight service (or Kafka Streams application) that receives events from all 15 sources, validates against a source-specific schema (registered in a schema registry), and transforms to a canonical event format
- Canonical schema: a standard envelope (event_id, source_system, event_type, event_time, payload) wraps source-specific payloads; downstream consumers always read the canonical format
- Quality gates: per-source SLA checks (expected event volume, required fields, value range validation); failed events go to source-specific DLTs
- Reliability tiers: high-reliability sources (financial transactions) use `acks=all`; low-reliability sources (clickstream) use `acks=1` with higher throughput
- Connects to orchestration: per-source quality metrics are reported to a data observability platform; SLA breaches trigger alerts and block downstream Gold table refreshes
Why this is asked: multi-source normalization is the real-world complexity of event-driven ingestion at enterprise scale.

---

## Delivery Semantics

### Level 1 — Starter

**Q1: What are the three message delivery semantics in Kafka — at-most-once, at-least-once, and exactly-once — and what does each guarantee?**
What a good answer covers:
- At-most-once: messages may be lost but are never duplicated; achieved by committing offsets before processing
- At-least-once: messages are never lost but may be duplicated; achieved by committing offsets only after successful processing
- Exactly-once: messages are processed exactly once with no loss and no duplication; requires idempotent producers and Kafka transactions
- In practice, at-least-once with idempotent consumers is the most common DE choice because exactly-once has performance overhead
Why this is asked: delivery semantics is one of the most fundamental streaming concepts and appears in almost every interview.

**Q2: What is an idempotent producer in Kafka, and how does it prevent duplicate messages?**
What a good answer covers:
- An idempotent producer assigns a sequence number to each message; the broker deduplicates retries with the same sequence number
- Enabled with `enable.idempotence=true`; Kafka automatically assigns a producer ID (PID) per session
- Prevents duplicates caused by producer retries on transient network errors
- Idempotent producers only guarantee deduplication within a single producer session; a producer restart gets a new PID, so restart-caused duplicates still require consumer-side deduplication
Why this is asked: idempotent producers are the first line of defense against duplicates; understanding their limits is important.

**Q3: How does offset commit timing determine whether a consumer achieves at-most-once or at-least-once delivery?**
What a good answer covers:
- Commit before processing: if the consumer crashes after committing but before processing, the message is lost (at-most-once)
- Commit after processing: if the consumer crashes after processing but before committing, the message is reprocessed on restart (at-least-once)
- For DE pipelines writing to a warehouse: commit after the warehouse write succeeds; combine with idempotent writes for safe at-least-once behavior
Why this is asked: this is the simplest and most important delivery semantics question; every DE candidate should answer it correctly.

**Q4: What is the difference between Kafka transactions and idempotent producers?**
What a good answer covers:
- Idempotent producers prevent duplicates for a single producer within a session
- Kafka transactions provide atomicity across multiple produces and/or consume-produce pairs: either all messages in the transaction are written or none are
- Transactions are used to implement read-process-write pipelines atomically: consume from topic A, process, produce to topic B — all in one atomic transaction
- Transactions require `transactional.id` to be set; they have higher overhead than idempotent-only producers
Why this is asked: the distinction reveals depth of Kafka delivery semantics knowledge.

### Level 2 — Mid

**Q1: Describe the exactly-once semantics (EOS) guarantee in Kafka Streams. What are its limitations?**
What a good answer covers:
- Kafka Streams EOS uses Kafka transactions to atomically commit: consumed offsets + produced output messages in a single transaction
- `processing.guarantee=exactly_once_v2` (the modern setting) achieves EOS within the Kafka ecosystem
- Limitations: EOS only covers Kafka-to-Kafka processing; if output goes to a database or warehouse, the database write is outside the transaction boundary
- Performance: EOS transactions add latency (transaction coordinator round-trips); throughput is lower than at-least-once
Why this is asked: EOS in Kafka Streams is well-understood by candidates who have used it; its limitations reveal production experience.

**Q2: Your pipeline consumes from Kafka and writes to both a Postgres database and a Kafka output topic. How do you achieve exactly-once semantics across both sinks?**
What a good answer covers:
- Kafka-to-Kafka portion: use Kafka transactions to atomically produce to the output topic and commit the input offset
- Kafka-to-Postgres portion: Postgres does not participate in Kafka transactions; you need a two-phase commit (2PC) or an outbox pattern
- Outbox pattern: write to Postgres and a Postgres outbox table in a single Postgres transaction; a separate transactional outbox consumer reads the outbox table and produces to Kafka
- 2PC is complex and generally avoided; the outbox pattern is the practical solution
Why this is asked: exactly-once across heterogeneous sinks is a real architect challenge with no built-in solution.

**Q3: A consumer processes events and writes results to a warehouse. The warehouse write succeeds but the Kafka offset commit fails. What happens on the next consumer restart, and how does your pipeline handle this?**
What a good answer covers:
- On restart, the consumer re-reads from the last committed offset and reprocesses the events whose warehouse write already succeeded
- The warehouse receives duplicate writes; if the write is a naive INSERT, duplicates are introduced
- Mitigation: make the warehouse write idempotent — use MERGE with the event ID as the deduplication key; the second write is a no-op
- This is the standard at-least-once + idempotent-consumer pattern; it achieves effectively-once semantics
Why this is asked: this scenario is the exact real-world manifestation of offset commit failure and tests practical pipeline design.

**Q4: How does Flink's checkpointing mechanism relate to exactly-once delivery semantics?**
What a good answer covers:
- Flink checkpoints periodically snapshot all operator state and the current Kafka offset atomically
- On failure, Flink restores from the last successful checkpoint, including the Kafka offset; reprocessing starts from that offset
- With two-phase commit sink connectors (e.g., Flink Kafka sink with `Semantic.EXACTLY_ONCE`), output is not committed until the checkpoint succeeds
- This provides end-to-end exactly-once from Kafka source to Kafka sink within Flink; external sinks require idempotent write support
Why this is asked: Flink checkpointing is the primary mechanism for exactly-once in stream processing and is expected knowledge for senior DE roles.

### Level 3 — Senior

**Q1: Your pipeline uses at-least-once delivery and idempotent MERGE to write to a warehouse. A data scientist reports that they see duplicate rows in the Gold table. Walk through the possible causes and your investigation approach.**
What a good answer covers:
- Check 1: is the MERGE deduplication key truly unique? If two events have the same event_id but different payloads, MERGE upserts both — not a duplicate but a data model issue
- Check 2: is the MERGE running on the correct target table? Misrouted writes to the wrong partition can cause apparent duplicates
- Check 3: did the Silver layer introduce duplicates before the Gold MERGE? Trace the event_id from Gold back through Silver to Bronze
- Check 4: are there multiple pipelines writing to Gold concurrently (e.g., backfill + live pipeline)? Concurrent MERGEs can conflict
- Use query: `SELECT event_id, COUNT(*) FROM gold GROUP BY event_id HAVING COUNT(*) > 1` to quantify; sample a duplicate and trace its lineage
Why this is asked: duplicate investigation is a real production task; the systematic approach reveals seniority.

**Q2: Compare the delivery semantics guarantees of Kafka Streams (exactly-once), Apache Flink (exactly-once with checkpointing), and Spark Structured Streaming (at-least-once with idempotent sinks) for a warehouse ingestion use case.**
What a good answer covers:
- Kafka Streams EOS: strong within Kafka ecosystem; warehouse writes require additional idempotency; simpler to operate
- Flink with 2PC sinks: end-to-end exactly-once to compatible sinks (Kafka, Iceberg); checkpoint interval determines recovery point; more operationally complex
- Spark Structured Streaming: at-least-once by default; idempotent warehouse writes (via foreachBatch with MERGE) achieve effectively-once; easier to integrate with existing Spark ecosystem
- For warehouse ingestion: Spark + idempotent MERGE is the most common production choice due to ecosystem maturity and operational simplicity
Why this is asked: comparing frameworks' delivery guarantees is a standard senior DE/architect question.

**Q3: Design a testing strategy to verify that your pipeline delivers exactly-once semantics under failure conditions (consumer crash, broker failure, network partition).**
What a good answer covers:
- Chaos testing: inject failures (kill consumer, disconnect broker) at each stage of the pipeline and verify the target table has no duplicates and no gaps after recovery
- Event counting test: produce exactly N events with known IDs; after pipeline recovery, assert the target contains exactly N rows with those IDs
- Offset assertion: after failure and recovery, verify the consumer's committed offset matches the last successfully processed event
- Use Testcontainers (Kafka + Postgres/warehouse mock) for local integration testing; test each failure scenario as a CI pipeline stage
Why this is asked: testing delivery guarantees under failure is a mature engineering practice that few candidates have implemented.

### Level 4 — Architect

**Q1: Design a financial transaction processing pipeline where exactly-once delivery is a regulatory requirement. The pipeline spans: Kafka source → Flink stream processor → PostgreSQL operational DB → warehouse Gold table. Detail the mechanisms at each boundary.**
What a good answer covers:
- Kafka source → Flink: Flink reads with `isolation.level=read_committed`; checkpointing at 30-second intervals captures offset + operator state atomically
- Flink → PostgreSQL: use the JDBC sink with Flink's two-phase commit; on checkpoint completion, Flink commits the Postgres transaction; on failure, Flink rolls back and retries from the last checkpoint
- PostgreSQL → Warehouse: use the outbox pattern — Flink writes a record to a Postgres outbox table in the same transaction as the operational write; a Debezium connector (connecting to c003_cdc_demo.py) reads the outbox via CDC and produces to a Kafka topic; the warehouse consumer reads from this topic with idempotent MERGE using transaction ID as the deduplication key
- End-to-end: each financial transaction is processed exactly once in Postgres and appears exactly once in the Gold warehouse table; the regulatory audit trail is the CDC event log
Why this is asked: exactly-once across multiple heterogeneous systems is the most challenging delivery semantics architecture question.

**Q2: Your organization is evaluating moving from at-least-once + idempotent writes to native exactly-once semantics (Kafka transactions + Flink EOS). Analyze the cost-benefit trade-offs and make an architectural recommendation.**
What a good answer covers:
- Cost of EOS: lower throughput (transaction coordinator overhead), higher latency (2PC adds round trips), more complex failure modes (transaction timeouts, zombie writers), harder to debug
- Benefit of EOS: eliminates deduplication logic from consumers; reduces complexity for teams unfamiliar with idempotency patterns; eliminates edge cases where deduplication keys are incorrectly designed
- At-least-once + idempotent: higher throughput, lower latency, more portable (works with any sink), but requires careful deduplication key design at every consumer
- Recommendation: for most DE use cases, at-least-once + idempotent MERGE is the better trade-off; EOS is justified only for financial or regulatory use cases where the audit cost of investigating duplicates exceeds the operational cost of EOS
- Migration path: if adopting EOS, start with Kafka-to-Kafka pipelines (lower risk) before extending to external sinks
Why this is asked: architectural recommendations require weighing competing factors — this question tests judgment, not just knowledge.
