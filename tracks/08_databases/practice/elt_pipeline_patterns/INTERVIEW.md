# Interview Questions — ELT Pipeline Patterns

> Topics covered: staging/raw/curated layer design · full load vs incremental · watermarks · schema evolution · data contracts
> Levels: Starter | Mid | Senior | Architect

---

## Topic 1 — Staging / Raw / Curated Layer Design

*Reference files: `c001_staging_raw_curated_demo.py`, `d00_staging_raw_curated_story.md`*

---

**Q1: What is the purpose of a staging layer in a data pipeline?**
What a good answer covers:
- Staging is a temporary landing zone that holds incoming data exactly as received, preserving file boundaries and original field values
- It decouples ingestion from transformation so failures in later stages do not require re-fetching source data
- In `c001_staging_raw_curated_demo.py`, each row in staging retains the original file name and all raw text fields without any casting or cleaning
Why this is asked: Tests whether the candidate understands the separation of concerns between landing data and processing it.

**Q2: How does the raw layer differ from the staging layer?**
What a good answer covers:
- Raw is a persistent, append-only history of every record ever received, including duplicates and dirty data
- Staging is transient and is often truncated after each load cycle, while raw is never deleted
- Raw rows in `c001_staging_raw_curated_demo.py` carry a `load_ts` metadata timestamp, enabling full audit trails
Why this is asked: Checks that the candidate can articulate why two pre-transformation layers both exist.

**Q3: What transformations are appropriate for the curated layer but not for staging or raw?**
What a good answer covers:
- Type casting (string "120.50" to a float), null handling, and deduplication belong in the curated layer
- Negative amounts and missing customer names from `c001_staging_raw_curated_demo.py` would be flagged or excluded at the curated stage
- Business rules such as "REFUND rows are excluded from revenue totals" are applied here, not at ingest
Why this is asked: Reveals whether the candidate knows where business logic should live in a medallion architecture.

**Q4: Why should a curated layer row reference the raw layer rather than the original source file?**
What a good answer covers:
- Referencing raw preserves lineage: any curated record can be traced back to the exact raw row and load batch
- Re-processing curated data from raw is faster and cheaper than re-pulling from the source system
- Avoids re-applying network calls and source-system load when a downstream model needs to be rebuilt
Why this is asked: Assesses understanding of data lineage and the cost of re-ingestion.

---

**Q5: Order o101 appears in both daily files in `c001_staging_raw_curated_demo.py`. How should each layer handle this duplicate?**
What a good answer covers:
- Staging and raw both keep both copies, tagged with their respective file names and load timestamps
- The curated layer deduplicates using a business key (order_id) plus a tiebreaker such as latest load_ts or source precedence
- The deduplication strategy should be documented and deterministic so reruns produce identical output
Why this is asked: Tests practical handling of the most common real-world ingestion problem.

**Q6: A retailer's source system sends a full file daily instead of only changed records. How does the raw layer design absorb this without causing storage to grow unboundedly?**
What a good answer covers:
- Partition the raw table by load date so old partitions can be dropped or archived after a defined retention window
- Compaction jobs can merge small daily partitions into monthly archives while retaining the audit record
- Retention policies are driven by compliance requirements, not just storage cost
Why this is asked: Connects layer design to operational concerns interviewers expect mid-level engineers to have thought about.

**Q7: How would you expose the curated layer to downstream BI tools while protecting it from pipeline reruns that temporarily break the table?**
What a good answer covers:
- Write curated output to a versioned location or use atomic swap (write to a staging table, then rename/swap)
- Use a view that always points to the last successfully validated partition, so in-progress writes are invisible to consumers
- Delta Lake or Iceberg snapshots eliminate the swap complexity by giving readers a consistent version
Why this is asked: Tests awareness of read/write isolation and zero-downtime delivery to consumers.

**Q8: A new business unit wants to add columns to the curated orders table. Walk through the governance process from request to production.**
What a good answer covers:
- Column additions require a schema change proposal reviewed against existing downstream consumers to assess breaking impact
- Non-breaking additions (new nullable column) can be merged with a migration script and updated dbt model
- The raw layer stays unchanged; only the curated transformation SQL and the data contract are updated
- Change is tested in a dev environment against a sample of raw history before promotion
Why this is asked: Evaluates whether the candidate treats schema changes as an engineering discipline, not just an ALTER TABLE.

---

**Q9: A compliance audit requires proving that a curated revenue figure published 90 days ago is correct. Design a lineage path from the published figure back to the source file.**
What a good answer covers:
- Curated row retains a raw_id foreign key; raw row retains file_name and load_ts from the staging record
- If using Delta Lake or Iceberg, time travel to the curated table snapshot at the audit date gives the exact figure
- Audit trail includes the transformation version (git commit or dbt run ID) that produced the curated row
- Lineage tools (OpenLineage, Marquez) can automate this trace if instrumented at pipeline execution time
Why this is asked: Senior candidates must show they design for auditability from the start, not after regulators ask.

**Q10: Your team processes 50 source systems with different file formats into the same raw zone. How do you prevent schema drift in one system from corrupting unrelated curated tables?**
What a good answer covers:
- Each source system has an isolated raw partition or table prefix so a bad schema does not touch other sources' data
- Schema validation at the staging-to-raw boundary (see `c001_schema_validation_demo.py` in the data quality track) catches drift before it lands in raw
- Curated jobs subscribe only to their own source's raw partition, so failures are blast-radius-contained
- Alerting on unexpected column additions or type changes triggers a human review before the next curated run
Why this is asked: Assesses systems thinking and blast-radius containment under scale.

**Q11: Describe how you would migrate an existing three-layer ELT architecture from a monolithic SQL warehouse to a lakehouse without downtime for consumers.**
What a good answer covers:
- Run the old warehouse and new lakehouse in parallel, dual-writing to both from the raw layer for a defined cutover window
- Validate curated output parity between warehouse and lakehouse before switching consumer connections
- Use feature flags or virtual schemas so consumers transparently redirect to the new layer
- Decommission the warehouse only after consumer SLAs have been met on the lakehouse for N consecutive days
Why this is asked: Senior/architect-level migration planning is a common real-world scenario.

---

**Q12: An executive wants a single "golden record" for each customer across five source systems with conflicting data. How do you design the curated layer to support entity resolution at scale, and how does this interact with your streaming pipeline?**
What a good answer covers:
- Entity resolution requires a match-and-merge step between raw ingestion and curated output, often run as a separate job (Master Data Management layer)
- Confidence scores from fuzzy matching must be stored alongside the golden record so downstream teams understand provenance
- In a streaming context (Kafka/Flink), incremental entity resolution means each new event may trigger a re-merge, requiring idempotent merge logic in the curated layer
- Changes to the golden record must propagate downstream via a CDC event stream so analytics tables stay consistent without full reloads
Why this is asked: Connects the three-layer model to MDM, streaming, and downstream analytics — a full-stack design question for architects.

**Q13: Your organization wants to enforce a data mesh architecture where domain teams own their curated tables. Redesign the staging/raw/curated pattern so domain teams have autonomy without sacrificing cross-domain data quality.**
What a good answer covers:
- Shared raw zone with read access for all teams; domain teams write only to their own namespace
- Each domain team publishes a data product backed by their curated table, with a declared data contract (schema, SLAs, quality expectations)
- A central platform team owns the staging ingestion framework; domain teams own transformation logic from raw onward
- Cross-domain joins happen only through published data products, not by directly querying another team's raw partition
- Data contracts from `c005_data_contracts_demo.py` become the governance mechanism replacing central schema review
Why this is asked: Tests whether the candidate can reason about organizational architecture, not just technical architecture.

---

## Topic 2 — Full Load vs Incremental

*Reference file: `c002_full_vs_incremental_demo.py`*

---

**Q1: What is a full load and when is it appropriate?**
What a good answer covers:
- A full load truncates the target table and reloads every row from the source on each pipeline run
- Appropriate when source systems do not expose change metadata (no updated_at column, no CDC stream)
- Also appropriate for small reference tables (lookup codes, currency rates) where the full dataset is cheap to reload
Why this is asked: Verifies the candidate knows this is not a universal default but a deliberate choice with tradeoffs.

**Q2: What is an incremental load and what information does it require from the source?**
What a good answer covers:
- An incremental load fetches only rows that changed since the last successful run, typically filtered by a timestamp or sequence number
- Requires the source to expose a reliable change indicator such as `updated_at`, `created_at`, or a CDC log
- `c002_full_vs_incremental_demo.py` would demonstrate filtering on a high-water mark to retrieve only new or modified rows
Why this is asked: Checks that the candidate understands the dependency on source-side metadata.

**Q3: What problems arise when you rely on `updated_at` for incremental loads but the source system allows back-dated updates?**
What a good answer covers:
- Back-dated updates set `updated_at` to a time earlier than the current high-water mark, so they are invisible to the incremental filter
- The resulting pipeline silently misses updates, causing stale data in the curated layer
- Mitigation options include CDC (capturing every row change event), full reload with deduplication, or a rolling lookback window that re-scans the last N days
Why this is asked: Tests whether the candidate is aware of the silent failure mode that bites incremental pipelines in production.

**Q4: How does dbt differentiate a full refresh from an incremental run, and why does this matter for your pipeline design?**
What a good answer covers:
- In dbt, `--full-refresh` drops and rebuilds the target table; a normal incremental run appends or merges only new rows based on the `is_incremental()` filter
- Developers must test both modes because the incremental logic can diverge from the full-refresh output when the merge key or filter has edge cases
- Pipeline scheduling must account for periodic full refreshes to correct any drift accumulated through incremental runs
Why this is asked: Connects incremental patterns to real tooling that interviewers expect mid-level dbt users to understand.

---

**Q5: A table has 500 million rows and a full load takes 4 hours. Propose a migration to incremental loading without breaking downstream consumers during the transition.**
What a good answer covers:
- Add an `updated_at` column to the source if absent, or enable CDC; validate it captures all change types (inserts, updates, deletes)
- Run full load and incremental in parallel for one cycle to verify row counts and key metrics match before switching
- Soft-launch incremental by running it on a copy of the table, promoting only after parity validation
- Communicate the cutover date to downstream teams and confirm no consumers depend on the full-reload timing guarantee
Why this is asked: Tests practical migration planning under production constraints.

**Q6: Your incremental pipeline has been running for six months. A bug in the transformation logic was silently miscalculating a column for three months. How do you fix the historical data?**
What a good answer covers:
- Identify the exact date range affected using the pipeline version history or git log
- Re-run the transformation from raw for the affected date range using the corrected logic (raw layer is the source of truth)
- Use a MERGE or OVERWRITE strategy scoped to the affected partition to avoid reprocessing unaffected data
- Validate the fix against a known-good sample before promoting, and add a regression test to catch the same class of bug
Why this is asked: Assesses incident response skills and trust in the raw layer as the recovery foundation.

**Q7: How do deletes propagate correctly in an incremental pipeline that does not use CDC?**
What a good answer covers:
- Without CDC, deleted rows are invisible to an incremental filter because there is no updated row to detect
- Common solutions: source system provides a soft-delete flag (`is_deleted = true`); or a daily reconciliation job compares source and target row counts by partition and issues explicit deletes for missing keys
- Hard deletes require either CDC or periodic full reloads of the affected key range
- GDPR right-to-erasure requirements make robust delete propagation a compliance issue, not just an accuracy issue
Why this is asked: Deletes are the hardest change type in incremental pipelines; senior candidates must have a concrete strategy.

**Q8: At what row count or data volume threshold would you recommend switching from a full load to incremental, and what factors influence that threshold?**
What a good answer covers:
- No universal threshold; the decision depends on load window (is 4 hours acceptable?), source system capacity, downstream SLA, and cost of the compute
- A table that fits in a single file and loads in under 30 seconds rarely needs incremental complexity
- Tables exceeding the pipeline window budget or imposing significant read load on the source are primary candidates for incrementalization
- Operational complexity of incremental (watermark management, delete handling) must be weighed against the cost savings
Why this is asked: Architect-level thinking about when simplicity beats optimization.

---

**Q9: Design an incremental pipeline for a source that provides only a daily snapshot file (no deltas, no timestamps) and must support late-arriving corrections.**
What a good answer covers:
- Treat each daily file as a full snapshot for that partition date; raw layer stores every version of every snapshot
- Compute deltas programmatically by comparing today's snapshot to yesterday's snapshot using set operations on the primary key
- Late-arriving corrections reprocess only the affected snapshot date's partition in the curated layer
- This pattern handles deletes naturally because rows absent from today's snapshot are flagged as removed
Why this is asked: Tests the ability to build incremental semantics on top of a source that does not natively support them.

**Q10: A streaming pipeline and a batch incremental pipeline both write to the same curated table. How do you prevent conflicts and ensure idempotency?**
What a good answer covers:
- Use a MERGE/UPSERT keyed on the business primary key so both writers converge on the same final state
- Partition the table by event date so the streaming writer owns the current-day partition and the batch writer owns completed historical partitions
- Idempotency requires that re-running either pipeline with the same input produces identical output; use deterministic keys and avoid sequence-generated IDs
- Delta Lake's optimistic concurrency control (transaction log) prevents file-level conflicts between concurrent writers
Why this is asked: Cross-pipeline write coordination is a senior-level design concern.

**Q11: A business analyst reports that the daily incremental run shows a 20% revenue spike every Monday. Diagnose whether this is a data quality issue or a pipeline design issue.**
What a good answer covers:
- First check whether Monday is the first run after a weekend gap; if so, Friday/Saturday/Sunday data is accumulating in the incremental window, causing an apparent spike
- Compare the incremental Monday total to a full-reload Monday total; if they match, the spike is real business data
- Check the high-water mark: if the watermark is not being persisted correctly, Monday may be re-loading data from the prior week
- If the pipeline uses event_time for windowing, check whether weekend events arrive late and fall into the Monday window
Why this is asked: Blends pipeline debugging with data intuition — a practical mid/senior interview scenario.

---

**Q12: Your company acquires a new business unit whose source system uses a proprietary binary format with no timestamp columns and no CDC capability. Design an end-to-end incremental strategy.**
What a good answer covers:
- Extract a full snapshot daily into the raw zone; use file hashing or row-level checksums to identify changed rows between snapshots
- Build a change detection layer that materializes deltas from consecutive snapshots, feeding only the delta to the curated pipeline
- Because this is compute-intensive, schedule the change detection job during off-peak hours and cache the prior snapshot's hash index
- Long term, lobby for CDC or a timestamp column at the source; document the current approach's limitations (cannot detect multi-field updates that hash-collide)
- Connect to streaming: if near-real-time is ever required, this architecture must be replaced with a CDC connector (Debezium, etc.)
Why this is asked: Architect-level question covering the full spectrum from no-metadata sources to future-state migration.

**Q13: Explain how you would implement a self-healing incremental pipeline that automatically detects and corrects data drift between source and target without manual intervention.**
What a good answer covers:
- Schedule a daily reconciliation job that computes row counts and sum/hash of key metrics per partition and compares source to target
- When drift exceeds a configurable threshold, the pipeline automatically triggers a full reload of the affected partition
- Results are logged to a quality dashboard (see `c001_schema_validation_demo.py` and anomaly detection patterns); alerts fire only when auto-healing fails or drift exceeds a second, higher threshold
- Connect to the data contract track: SLA breach detection triggers the self-healing workflow automatically
- Architect consideration: self-healing must be idempotent and must not cascade into unnecessary full reloads of downstream dependents
Why this is asked: Tests whether the candidate can design autonomous, production-grade pipeline reliability systems.

---

## Topic 3 — Watermarks

*Reference file: `c003_watermarks_demo.py`*

---

**Q1: What is a high-water mark in the context of data pipelines?**
What a good answer covers:
- A high-water mark is the maximum event_time (or sequence value) successfully processed in a previous run
- The next pipeline run fetches only records with an event_time greater than the stored high-water mark
- In `c003_watermarks_demo.py`, `high_water_mark` is updated after each event is accepted, preventing re-processing of already-ingested records
Why this is asked: Confirms the candidate understands the most common incremental state management mechanism.

**Q2: What is a watermark in stream processing, and how does it differ from a high-water mark?**
What a good answer covers:
- A watermark is a threshold that declares "all events with event_time earlier than this value have arrived" — it allows the engine to close windows and emit results
- A high-water mark tracks the last successfully processed point; a watermark tracks how far behind real time the processing engine is willing to wait
- In `c003_watermarks_demo.py`, `LATE_TOLERANCE_MINUTES` defines the watermark lag: events more than 5 minutes behind the current max event_time are considered too late
Why this is asked: Distinguishes two related but distinct concepts that candidates frequently conflate.

**Q3: What happens to a late-arriving event in `c003_watermarks_demo.py` when it falls outside the late tolerance window?**
What a good answer covers:
- The event's event_time is earlier than (max_event_time - LATE_TOLERANCE_MINUTES), so the pipeline classifies it as too late to process in the current window
- The event is either dropped or routed to a dead-letter queue for manual review
- Dropping late events means the pipeline prioritizes timeliness over completeness; the appropriate policy depends on the business requirement
Why this is asked: Tests understanding of the completeness-vs-timeliness tradeoff in event processing.

**Q4: Where should a high-water mark be stored so it survives a pipeline restart?**
What a good answer covers:
- External durable storage: a metadata database table, a key-value store (Redis), or a dedicated watermark table in the warehouse
- The watermark must be written atomically with the commit of processed data; writing it after the commit creates a window where a crash causes re-processing
- Storing it in memory only means a restart re-processes the last batch, which is acceptable only if the pipeline is idempotent
Why this is asked: Operationalizes the concept — candidates must know that a watermark is useless if it is not persisted.

---

**Q5: An event pipeline processes events in arrival order, but events frequently arrive out of order due to network jitter. How do you set the late tolerance in `c003_watermarks_demo.py` to balance completeness against latency?**
What a good answer covers:
- Analyze the historical distribution of event lateness (P95, P99 arrival delay) and set tolerance slightly above P99 to accept most late events
- A wider tolerance increases result latency because windows stay open longer before emitting; a tighter tolerance drops more events but emits faster
- Monitor the late-event drop rate in production; adjust tolerance if the drop rate exceeds business-acceptable thresholds
Why this is asked: Connects the mechanical watermark setting to a data-driven tuning process.

**Q6: A pipeline's high-water mark is stored in the same database as the output table, and the database fails mid-run after writing output rows but before updating the watermark. What is the consequence and how do you prevent it?**
What a good answer covers:
- On the next run, the watermark has not advanced, so the pipeline re-fetches and re-processes the same rows, creating duplicates
- Prevention: wrap the watermark update and the output write in the same database transaction (if the target supports it)
- If the target is object storage (no transactions), use idempotent MERGE/UPSERT logic so re-processing the same rows is safe
- Alternatively, derive the watermark from the max event_time in the output table itself rather than storing it separately
Why this is asked: Tests failure-mode reasoning — a key mid-level engineering skill.

**Q7: A regulatory requirement demands that no event older than 7 days be silently dropped. How do you modify the watermark pattern in `c003_watermarks_demo.py` to guarantee this?**
What a good answer covers:
- Remove the silent drop; route late events to a quarantine table with a `late_arrival_reason` tag instead
- Add a monitoring job that alerts if any quarantine event is older than 7 days relative to its original event_time
- Provide a manual reprocessing workflow so operations teams can inject quarantined events into the correct historical window after investigation
Why this is asked: Applies compliance requirements to a technical pattern — important at senior level.

**Q8: How would you implement watermarks in a batch ELT pipeline that does not use a streaming engine like Flink or Spark Structured Streaming?**
What a good answer covers:
- Persist the last successfully processed batch's max event_time in a metadata table (the high-water mark)
- On each run, query the source with `WHERE event_time > :high_water_mark AND event_time <= :current_run_time`
- The upper bound (`current_run_time`) prevents unbounded windows and creates a deterministic batch boundary
- Late-event handling: run a periodic "late arrival" job that scans a wider lookback window and MERGES late records into the target
Why this is asked: Bridges streaming watermark concepts to batch pipelines, where most candidates first encounter the pattern.

---

**Q9: Your pipeline uses event_time watermarks but the source system's clocks are unreliable and sometimes send events with future timestamps 30 minutes ahead. How do you handle this without breaking the watermark logic?**
What a good answer covers:
- Cap event_time at `processing_time + allowed_clock_skew` before using it for watermark calculation; flag capped events for review
- Separate `event_time` (claimed by source) from `processing_time` (pipeline's clock) and use processing_time as the authoritative watermark
- Alert when the gap between event_time and processing_time exceeds a threshold; investigate the source clock synchronization
- Future-dated events that pass the cap inflate the high-water mark, which would cause subsequent genuine events to appear late — hence the cap is critical
Why this is asked: Clock skew is a production reality that senior candidates must have a defensive strategy for.

**Q10: Design a multi-source watermark system where five upstream services each produce events with their own event_time clocks, all landing in a single unified events table.**
What a good answer covers:
- Maintain a per-source watermark so a slow source does not block progress for fast sources
- The unified table's global watermark is `min(all source watermarks)` if ordering across sources is required; otherwise each source's watermark is independent
- Tag each event with `source_id` and `source_event_time` so per-source late-arrival policies can differ
- Dashboard the per-source watermark lag so SRE teams can identify which source is falling behind
Why this is asked: Scales the single-source pattern to a realistic multi-tenant architecture.

**Q11: A downstream analytics team queries the events table in real time and complains that the most recent 10 minutes of data are always incomplete. Explain why this happens and how you would address it architecturally.**
What a good answer covers:
- Events within the current watermark window have not yet been committed because the pipeline is waiting for the late-tolerance period to expire before closing the window
- Solution: expose a "committed through" timestamp metadata field alongside the table so consumers know the guaranteed complete horizon
- Alternatively, publish two tables: a provisional table (all received events, potentially incomplete) and a final table (watermark-closed windows only)
- Connect to streaming: a Kafka-backed real-time layer can serve the most recent events while the batch pipeline owns the complete historical record
Why this is asked: Connects watermark internals to the consumer experience — a senior-level design concern.

---

**Q12: You need to implement exactly-once event processing across a pipeline that spans Kafka (ingest), Spark (transformation), and Delta Lake (storage). Describe how watermarks and transaction logs interact to achieve this guarantee.**
What a good answer covers:
- Kafka offsets serve as the ingest watermark; Spark checkpoints store the last committed Kafka offset and output watermark atomically
- Delta Lake's transaction log provides the storage-side atomicity: a Spark write either commits fully or rolls back, never leaving partial data
- Exactly-once is achieved by writing the Kafka offset into the Delta Lake transaction log as part of the same commit, so a replay detects the already-committed offset and skips re-processing
- This spans the streaming track (Kafka), the transformation track (Spark watermarks), and the lakehouse track (Delta ACID from `c002_delta_lake_acid_demo.py`)
Why this is asked: Connects watermarks to the full end-to-end exactly-once guarantee that architects must design for.

**Q13: A business requires that all financial events be attributable to a specific business day regardless of when they arrive (events can arrive up to 72 hours late due to offline POS systems). Design a watermark and partition strategy that satisfies both the timeliness SLA for operations and the completeness SLA for finance.**
What a good answer covers:
- Partition the target table by `business_date` (the event's logical date) rather than processing_time
- Operations consumers query a "live" view that includes all events received so far for each business_date, accepting incomplete data for the current and prior two days
- Finance consumers query a "final" view that only exposes a business_date partition after its 72-hour late-arrival window has closed (watermark-gated)
- The watermark for finance is `current_date - 3 days`; a quality check validates that each closed partition's revenue matches the source system's end-of-day report
- Connects to data freshness (data quality track) and data contracts, which formalize the different SLAs for different consumers
Why this is asked: Real-world financial pipelines require exactly this dual-SLA design; tests whether the candidate can satisfy competing consumer requirements simultaneously.

---

## Topic 4 — Schema Evolution

*Reference file: `c004_schema_evolution_demo.py`*

---

**Q1: What is schema evolution and why does it matter in a data pipeline?**
What a good answer covers:
- Schema evolution is the process of changing a table's structure (adding, removing, or altering columns) while keeping existing data and downstream consumers functional
- Without managed evolution, a source-side column addition can crash a pipeline that expects an exact set of fields
- `c004_schema_evolution_demo.py` demonstrates how a pipeline detects and handles incoming data that does not match the registered schema
Why this is asked: Every production pipeline eventually faces schema drift; this baseline question separates those who have dealt with it from those who have not.

**Q2: What is a breaking vs a non-breaking schema change?**
What a good answer covers:
- Non-breaking: adding a new nullable column, widening a data type (int to bigint), or adding a new optional field — existing consumers continue to work
- Breaking: renaming a column, removing a column, narrowing a type (string to int), or changing semantics of an existing field
- Non-breaking changes can often be applied automatically; breaking changes require coordinated migrations with downstream teams
Why this is asked: Establishes vocabulary that is required for any schema governance discussion.

**Q3: How does Delta Lake handle schema evolution differently from a traditional data warehouse?**
What a good answer covers:
- Delta Lake supports `mergeSchema` option on writes, which automatically adds new columns from the incoming DataFrame to the table definition
- Traditional warehouses require explicit DDL (ALTER TABLE ADD COLUMN) before the data can be written
- Delta Lake's schema enforcement mode rejects writes that do not conform to the registered schema unless `mergeSchema` is explicitly enabled
Why this is asked: Tests practical knowledge of a widely used lakehouse tool's schema behavior.

**Q4: What is a schema registry and what role does it play in schema evolution?**
What a good answer covers:
- A schema registry (e.g., Confluent Schema Registry) stores versioned schemas for topics or tables and enforces compatibility rules on new schema submissions
- Compatibility modes include BACKWARD (new schema can read old data), FORWARD (old schema can read new data), and FULL (both directions)
- In ELT pipelines, a registry prevents a producer from publishing a breaking schema change before consumers are updated
Why this is asked: Introduces the governance layer that makes schema evolution safe at scale.

---

**Q5: A source team adds three new columns to their daily export file without notifying the pipeline team. The pipeline fails at the staging-to-raw boundary. Walk through how you would detect, alert on, and recover from this.**
What a good answer covers:
- Detection: schema validation at ingestion (similar to `c001_schema_validation_demo.py`) compares incoming fields to the registered schema and flags extra columns
- Alert: the pipeline fails fast and sends a notification with the list of unexpected fields rather than silently dropping or loading them
- Recovery: if columns are additive and non-breaking, update the schema registry and re-run the failed batch; if breaking, engage the source team before proceeding
- Prevention: establish a data contract (`c005_data_contracts_demo.py`) that requires source teams to notify and get approval before schema changes
Why this is asked: Tests the full detection-alert-recovery lifecycle, not just the technical fix.

**Q6: How do you handle the case where a column is renamed in the source but must continue to appear under the old name in the curated layer for backward compatibility?**
What a good answer covers:
- Map the new source column name to the old curated column name in the transformation layer using a column alias or a config-driven mapping table
- Document the mapping explicitly so future maintainers understand why a column name diverges between raw and curated
- Deprecate the old name in the curated layer on a communicated timeline, migrating consumers to the new name before removing the alias
Why this is asked: Practical backward-compatibility management is a mid-level production skill.

**Q7: Your pipeline uses Avro serialization with schema evolution. A new field is added with a default value. Explain how existing consumers reading old messages are affected.**
What a good answer covers:
- Avro's schema evolution rules allow adding a field with a default value in a BACKWARD-compatible way: old consumers ignore the new field; new consumers see the default when reading old messages
- Readers use their own schema (reader schema) projected onto the writer schema (the schema used when the message was written), so field addition with defaults is safe
- Removing a field with no default would break old consumers trying to read new messages — this is a breaking change
Why this is asked: Tests serialization-level schema evolution, which candidates working with streaming pipelines must understand.

**Q8: How would you design a schema evolution policy for a team of 15 engineers contributing to 40 pipelines to prevent accidental breaking changes from reaching production?**
What a good answer covers:
- Require all schema changes to be proposed as pull requests against a central schema registry; CI runs compatibility checks automatically
- Breaking changes trigger a mandatory review gate that notifies all registered consumers of the affected table
- A deprecation period (e.g., 30 days) during which both old and new schemas are supported gives consumers time to migrate
- Integration tests in CI replay recent historical data against the new schema to catch regressions before merge
Why this is asked: Scales the technical knowledge to an organizational governance process.

---

**Q9: You are migrating a JSON-based schema to Parquet columnar format. Some JSON fields are nested objects that do not map cleanly to a flat Parquet schema. How do you handle this without breaking existing consumers?**
What a good answer covers:
- Flatten nested objects into dot-notation columns (`address.city`) or use Parquet's native nested struct support
- Publish both the legacy JSON and new Parquet datasets during a transition window so consumers can migrate at their own pace
- Test Parquet schema with existing SQL queries to detect any implicit type coercion issues (JSON strings vs typed Parquet columns)
- Update data contracts to specify the new Parquet schema as the canonical format with an explicit cutover date
Why this is asked: Format migration is a common senior engineering challenge, especially when moving to lakehouse architectures.

**Q10: A column's data type must change from VARCHAR(100) to VARCHAR(500) in a high-volume table with 2 billion rows. How do you execute this migration with zero downtime?**
What a good answer covers:
- In columnar formats (Parquet/Delta), column metadata changes do not require rewriting data files immediately; update the schema metadata and rely on reader-side casting for new reads
- In traditional warehouses, use a shadow column strategy: add `column_v2 VARCHAR(500)`, backfill it, then swap at the application layer
- Route new writes to the wide column immediately; backfill historical data asynchronously in batches to avoid locking the table
- Validate that no downstream consumers hard-code VARCHAR(100) as a validation constraint before cutting over
Why this is asked: Type widening at scale requires careful zero-downtime techniques that senior engineers must know.

**Q11: Design a schema versioning system for a data lakehouse where multiple versions of the same table schema must coexist to support consumers that cannot upgrade simultaneously.**
What a good answer covers:
- Store each schema version as a named view or table suffix (`orders_v1`, `orders_v2`) backed by the same underlying Parquet/Delta files
- The transformation layer writes a superset schema containing all columns from all active versions; versioned views project the appropriate subset
- A compatibility matrix documents which consumer versions are compatible with which schema versions
- Sunset old versions on a published schedule with at least 60 days notice; automated tests verify the sunset version is no longer queried before removal
Why this is asked: Multi-version coexistence is an architect-level problem in large organizations with slow-moving consumers.

---

**Q12: A financial reporting pipeline must ensure that schema changes never alter the semantics of a regulatory column (e.g., `gross_revenue`) even if the source system renames or restructures the field. Design a governance layer that enforces this.**
What a good answer covers:
- Define a canonical data model for regulatory columns with locked semantics; all source-to-curated mappings must resolve to this canonical model
- Any change to a source field that maps to a regulatory column triggers an automated regulatory impact assessment before the change is approved
- Immutable audit snapshots (Delta Lake time travel or Iceberg snapshots) allow reconstructing the exact value of `gross_revenue` as of any historical date, independent of subsequent schema changes
- Connect to the data contracts track: regulatory columns are governed by a stricter contract tier with change-freeze periods around reporting dates
Why this is asked: Connects schema governance to regulatory compliance — an architect-level design scenario.

**Q13: Explain how a streaming pipeline using Kafka and Flink must coordinate schema evolution with a batch ELT pipeline that reads from the same Delta Lake table, ensuring neither pipeline is disrupted by a schema change.**
What a good answer covers:
- The Delta Lake table is the shared state; schema changes must be committed to the Delta transaction log before either pipeline reads the new schema
- Flink's Kafka source uses a schema registry; a schema change in Kafka must be backward-compatible or Flink consumers must be updated and redeployed before the new schema is published
- The batch ELT pipeline must test the new Delta schema in a staging environment before the streaming pipeline begins writing the new schema to production
- Coordinate the cutover: pause the streaming pipeline briefly, apply the schema change to Delta Lake, restart the streaming pipeline with the updated schema, then trigger a batch ELT run to validate consistency
- Connects to the lakehouse track (Delta ACID) and streaming architecture
Why this is asked: Cross-pipeline schema coordination is an architect-level distributed systems problem.

---

## Topic 5 — Data Contracts

*Reference file: `c005_data_contracts_demo.py`*

---

**Q1: What is a data contract in the context of a data pipeline?**
What a good answer covers:
- A data contract is a formal agreement between a data producer and its consumers specifying the schema, data types, SLAs (freshness, completeness), and quality expectations for a dataset
- It shifts data quality accountability from consumers to producers, who must validate their output before publishing
- `c005_data_contracts_demo.py` demonstrates how a contract is defined and how violations are detected at the publishing boundary
Why this is asked: Data contracts are a foundational concept in modern data mesh and platform engineering; this question filters candidates who have only worked in ad hoc pipeline cultures.

**Q2: What should a minimal data contract include?**
What a good answer covers:
- Schema definition: column names, data types, nullable constraints
- Freshness SLA: maximum acceptable lag between source event and data availability in the target table
- Quality rules: null rate thresholds, value range constraints, referential integrity expectations
- Versioning and change notification process: how consumers are informed of upcoming changes
Why this is asked: Tests whether the candidate knows what to include, not just that contracts exist.

**Q3: How does a data contract differ from a database schema definition?**
What a good answer covers:
- A database schema defines structure; a data contract also defines behavior (freshness, completeness, quality) and the process for managing changes
- A schema is enforced by the database engine; a data contract is enforced by a pipeline test or a contract validation framework
- Data contracts include ownership, SLA commitments, and escalation paths — none of which appear in a CREATE TABLE statement
Why this is asked: Distinguishes the technical artifact from the organizational agreement.

**Q4: What happens when a producer violates a data contract and how should the pipeline respond?**
What a good answer covers:
- The pipeline should detect the violation at the producer boundary (before data reaches consumers) using validation checks aligned with the contract
- Violations should trigger an alert to the producer's team, not silently pass bad data to consumers
- Depending on severity: quarantine the violating batch, fail the pipeline, or allow partial publication with a quality flag on affected rows
Why this is asked: Tests whether the candidate understands that contracts are enforced, not just documented.

---

**Q5: A downstream BI dashboard breaks because the producer added a new NOT NULL column without notifying consumers. How would a data contract framework have prevented this?**
What a good answer covers:
- The contract's schema section would have required the producer to submit a breaking-change proposal before deployment
- CI checks on the producer's pipeline would have validated the outgoing data against the registered contract version before publishing
- The change notification process would have given consumers a migration window before the new column became mandatory
- This is exactly the class of problem `c005_data_contracts_demo.py` addresses by validating output at the producer boundary
Why this is asked: Makes the abstract concept concrete by tying it to a common real-world failure mode.

**Q6: How do you version a data contract so that a producer can deploy a new version while old consumers continue to work on the previous version?**
What a good answer covers:
- Assign a semantic version to each contract; consumers declare which version they depend on
- Publish both old and new contract versions simultaneously during the deprecation window, backed by versioned views or table snapshots
- Consumers are expected to migrate within the published deprecation window; after the deadline, the old contract version is retired
- A contract registry tracks active consumers per version, preventing producers from sunsetting a version with active dependents
Why this is asked: Applies software versioning discipline to data contracts — a mid-level data platform skill.

**Q7: How would you implement automated contract validation in a CI/CD pipeline for a dbt project?**
What a good answer covers:
- Define contracts as YAML files (schema.yml in dbt) alongside the model SQL; each contract specifies expected column types, tests (not_null, unique, accepted_values), and freshness expectations
- dbt's built-in schema tests enforce type and constraint contracts on every run; add custom generic tests for business-rule constraints
- In CI, run `dbt test` against a staging environment after every pull request; failures block merge
- Contract versions are tracked in git; a PR that changes a contract requires a review from registered consumers (enforced via CODEOWNERS)
Why this is asked: Connects data contracts to real tooling that dbt-using organizations implement.

**Q8: A producer team owns 12 tables consumed by 30 different downstream teams. How do you scale data contract management without requiring the producer team to individually negotiate with each consumer?**
What a good answer covers:
- Publish contracts in a central data catalog (e.g., DataHub, Atlan) where consumers self-register their dependencies on specific tables and contract versions
- Automated impact analysis tools scan the catalog to identify all consumers affected by a proposed contract change, producing a change impact report
- Consumers opt into automated notifications for any contract version they depend on; no manual negotiation required for non-breaking changes
- Breaking changes still require a human review, but the catalog identifies who must be consulted automatically
Why this is asked: Scales the concept to organizational reality — an architect-level operational design problem.

---

**Q9: A streaming pipeline and a batch pipeline both consume data from the same producer table. The contract specifies a 15-minute freshness SLA. How do you verify the contract is met for both consumers differently?**
What a good answer covers:
- The streaming consumer measures freshness as the lag between event_time and processing_time; the 15-minute SLA is checked per-message
- The batch consumer measures freshness as the age of the last successfully loaded partition; a monitoring job checks that the partition is no more than 15 minutes old at the scheduled consumption time
- Contract validation differs per consumer type but the SLA value is the same; the contract framework must support consumer-type-specific validation implementations
- Connects to the data freshness topic in the data quality track and to watermark patterns in this track
Why this is asked: Tests that the candidate can apply the same contract to heterogeneous consumers.

**Q10: A producer's output schema is automatically inferred from a DataFrame at runtime. How does this create contract risk and how do you mitigate it?**
What a good answer covers:
- Runtime schema inference means a code change or data change upstream can silently alter the inferred schema, breaking the contract without any explicit schema change by the developer
- Mitigation: freeze the schema by registering it explicitly in a schema registry or as a Delta Lake schema definition; reject writes that do not match the registered schema
- Add a CI test that runs the pipeline against sample data and asserts the output schema matches the contracted schema
- This is the exact risk that `c001_schema_validation_demo.py` addresses in the data quality track: validate at the boundary, not at the consumer
Why this is asked: Runtime inference is a common anti-pattern; candidates should know why explicit schemas are safer.

**Q11: Design a data contract governance model for a data mesh organization where 10 domain teams independently own and publish data products.**
What a good answer covers:
- Each domain team is responsible for authoring, versioning, and maintaining contracts for their own data products, with no central approval gate for non-breaking changes
- A federated contract registry aggregates all published contracts; a platform team maintains the registry infrastructure but does not own individual contracts
- Cross-domain consumer dependencies are registered in the catalog; the platform team runs compatibility checks when a contract version is proposed for retirement
- Compliance and regulatory columns have an additional central governance layer (a data stewardship council) that approves changes regardless of domain ownership
- Connects to schema evolution governance: the same PR-based approval process applies to both schema changes and contract changes
Why this is asked: Data mesh contract governance is an architect-level organizational design question increasingly asked in platform engineering roles.

---

**Q12: An SLA breach in a data contract triggers a downstream financial report to be delayed by 4 hours, causing a regulatory reporting deadline to be missed. Design a contract monitoring and escalation system that prevents this from happening again.**
What a good answer covers:
- Implement a multi-tier freshness monitor: warn at 50% of the SLA window, alert at 80%, and auto-escalate with incident creation at 95%
- The escalation path includes the producer team's on-call engineer, their manager, and the data platform SRE team — not just a Slack message
- A dependency graph in the contract registry maps the producer's SLA to the downstream report's deadline, so the impact of a delay is quantified automatically at alert time
- Post-incident: conduct an SLA breach review, add a circuit-breaker that pauses dependent pipelines and notifies stakeholders when the breach threshold is hit
- Connect to anomaly detection (data quality track): an unusual data volume drop is an early indicator of an upstream SLA breach, enabling proactive alerting before the deadline is missed
Why this is asked: Connects data contracts to real organizational consequences and tests whether the candidate designs monitoring systems with sufficient urgency and escalation depth.

**Q13: You are designing a data platform for a financial institution that must comply with BCBS 239 (risk data aggregation principles). How do data contracts support the lineage, accuracy, and timeliness requirements of this regulation?**
What a good answer covers:
- BCBS 239 requires that risk data be accurate, complete, timely, and traceable to its source; data contracts formalize and enforce each of these properties
- Lineage: contracts reference the upstream producer and registered schema version, enabling automated lineage graphs from source to regulatory report
- Accuracy: quality rules in the contract (null constraints, value ranges, referential integrity) are validated at every pipeline stage and results are logged for audit
- Timeliness: freshness SLAs in the contract define the maximum acceptable lag; breach logs provide evidence of compliance or non-compliance for auditors
- Connect to the staging/raw/curated topic: the raw layer's immutability and the curated layer's traceability to raw satisfy BCBS 239's data provenance requirements
Why this is asked: Regulatory data governance is an architect-level scenario; tests whether the candidate can connect technical data contract concepts to a named regulatory framework.
