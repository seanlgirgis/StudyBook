# Snowflake Micro-Nuggets Story (Fast Intro + Interview View)

## Why Snowflake, Not Just "Regular" Databases?
Snowflake is still a database platform, but it is built for modern data engineering workloads where scale, concurrency, and mixed data types matter more than classic single-engine RDBMS assumptions.

Key differences you should internalize:
- Compute and storage are separated: you can scale warehouse compute up/down without redesigning tables.
- Multiple virtual warehouses: many teams can run heavy queries concurrently with less contention.
- Native cloud-first workflows: staging, COPY INTO, external storage, and account-level governance are first-class.
- Semi-structured support: VARIANT + FLATTEN make JSON workflows practical.
- Data lifecycle safety: Time Travel and zero-copy cloning reduce fear when experimenting.

For DE learners, this means you learn both SQL fundamentals and modern production patterns in one place.

## Learning Goal of This Nugget Lane
This is a speed lane: each nugget is a 5-10 minute focused exercise that answers one concrete question.

If you complete this lane, you should be able to:
- Connect and reason about context (role, warehouse, database, schema).
- Build and evolve objects quickly (DDL).
- Perform common pipeline mutations safely (DML + MERGE).
- Load files into Snowflake and work with stages.
- Query JSON and nested payloads for event pipelines.
- Use Time Travel/UNDROP for recovery.
- Understand Streams/Tasks for CDC automation.
- Discuss governance, performance, and metadata with confidence.

## Nugget Journey Map
Run in this order for fastest understanding:

1. `00_setup`
- `00_prereq_check.py`
- `01_connection.py`
- `02_session_context.py`

2. `02_ddl_basics`
- `01_create_db_schema.py`
- `02_create_table.py`
- `03_clone_table.py`

3. `03_dml_basics`
- `01_insert_select.py`
- `02_merge.py`
- `03_update_delete.py`

4. `04_loading_data`
- `01_internal_stage_put.py`
- `02_copy_into_table.py`
- `03_file_formats.py`
- `04_external_stage_s3.py`

5. `05_semi_structured`
- `01_variant_column.py`
- `02_query_json.py`
- `03_flatten.py`

6. `06_time_travel`
- `01_query_past.py`
- `02_undrop.py`

7. `07_streams_and_tasks`
- `01_stream_on_table.py`
- `02_task_basic.py`
- `03_stream_task_pipeline.py`

8. `99_end`
- `99_reset_lab.py`

## Suggested 60-Minute Sprint
If you only have one hour, do this minimal path:
- `00_setup/01_connection.py`
- `02_ddl_basics/02_create_table.py`
- `03_dml_basics/02_merge.py`
- `05_semi_structured/03_flatten.py`
- `06_time_travel/02_undrop.py`
- `07_streams_and_tasks/01_stream_on_table.py`

## What This Teaches in DE Terms
- Data modeling startup: database/schema/table creation.
- Incremental loading: MERGE patterns.
- Raw-to-curated ingestion: stages and COPY INTO.
- Event payload handling: VARIANT + FLATTEN.
- Operational resilience: Time Travel + UNDROP.
- CDC pipeline thinking: Streams and Tasks.

## Interview View Questions
Use these as quick self-checks after each section.

Core concepts:

**Why does Snowflake separate compute from storage?**
It lets you scale query power independently from data size, avoid overprovisioning, and pay for compute only while workloads run.

**What problem do virtual warehouses solve in a multi-team environment?**
They isolate compute contention, so one team's heavy queries do not slow other teams using the same shared data.

**When would you use a dedicated warehouse for one workload?**
Use one for critical or spiky workloads (for example BI dashboards, production ELT, or ML feature jobs) when you need predictable performance and clearer cost control.

DDL and modeling:

**When would you choose TRANSIENT over PERMANENT tables?**
Choose TRANSIENT for reproducible intermediate data where fail-safe retention is not worth extra storage cost; keep PERMANENT for business-critical durable data.

**What is zero-copy clone and why is it useful for testing?**
A clone creates a near-instant logical copy without physically copying data at creation time, so you can test safely and cheaply on realistic data.

**Which column types are best for IDs, money, timestamps, and JSON payloads?**
IDs usually use NUMBER or stable VARCHAR keys, money should use fixed-point NUMBER(precision, scale), timestamps commonly use TIMESTAMP_NTZ/ LTZ based on timezone needs, and JSON payloads use VARIANT.

DML and ingestion:

**Why is MERGE central to DE pipelines?**
MERGE handles insert/update (and optional delete) in one atomic pattern, which is the core of idempotent incremental loading.

**What is the risk of UPDATE/DELETE without clear filters?**
You can unintentionally modify or remove large portions of data, causing hard-to-detect corruption even if recovery is possible.

**When do you prefer COPY INTO over row-by-row inserts?**
Prefer COPY INTO for file-based bulk ingestion because it is faster, more scalable, and operationally cleaner for production pipelines.

Semi-structured:

**When should you keep JSON in VARIANT vs normalize into relational columns?**
Keep it in VARIANT for flexible/raw ingestion and evolving schemas; normalize when fields are stable, heavily queried, and need stronger governance/performance.

**How does FLATTEN help when arrays are nested?**
FLATTEN explodes array elements into rows so nested structures become queryable with standard SQL joins and filters.

**What is the tradeoff between flexibility and query cost on VARIANT-heavy tables?**
VARIANT gives schema flexibility but can increase scan and compute costs if you do heavy repeated extraction without curated structured layers.

Reliability and operations:

**How does Time Travel reduce production risk?**
It allows querying or restoring past object states, so mistakes can be investigated and reversed without relying only on external backups.

**What is UNDROP actually recovering?**
UNDROP restores dropped objects (for supported retention windows) with their metadata/state so you can recover accidental deletions quickly.

**How would you explain Streams/Tasks as a lightweight CDC pattern?**
Streams track table changes and Tasks schedule SQL processing, together giving a native incremental pipeline loop inside Snowflake.

Performance and governance:

**How do you think about warehouse size vs query latency vs cost?**
Larger warehouses reduce runtime but cost more per unit time; the goal is to right-size by workload SLA, concurrency, and total spend.

**What metadata views would you inspect for query history and storage usage?**
Use ACCOUNT_USAGE and INFORMATION_SCHEMA views (for example QUERY_HISTORY, TABLE_STORAGE_METRICS, and warehouse usage views) to analyze performance and cost behavior.

**How would you isolate noisy workloads without changing schema design?**
Route them to separate warehouses/resource monitors so compute contention is isolated while data model and shared storage remain unchanged.

## Good Practice Rules for This Lane
- Keep object names prefixed (for example `NUGGET_`) to avoid collisions.
- Reset lab state at checkpoints or at the end using `99_end/99_reset_lab.py`.
- Prefer idempotent patterns in scripts so re-run is safe.
- Print meaningful output after each action to confirm behavior.
- Do not put secrets in scripts; rely on your project env/secret flow.

## Next Step (Optional)
Mini capstone is now added to the nugget system under:

Offline-study upgrade applied to all capstone scripts:
- Each file now includes `PURPOSE`, `TEACHABLE CONCEPTS`, and `EXPECTED OUTPUT (typical)` sections.
- Inline comments were expanded to explain pipeline intent and DE reasoning, not just syntax.
- This lets you review and learn from the scripts even without active Snowflake trial access.

- `08_mini_capstone/01_stage_json_ingest.py`
- `08_mini_capstone/02_copy_into_raw_variant.py`
- `08_mini_capstone/03_transform_curated_merge.py`
- `08_mini_capstone/04_stream_task_incremental.py`
- `08_mini_capstone/05_time_travel_recovery_demo.py`

Run them in order to complete the full story:
- Ingest small JSON files into a stage.
- COPY INTO a raw table with VARIANT.
- Transform into a curated table with MERGE.
- Add a Stream + Task for incremental updates.
- Demonstrate recovery with Time Travel.

This mini capstone proves you can connect features into a real DE workflow.
