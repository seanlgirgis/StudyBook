# ChatGPT Prompt — Delta Lake Tutorial
# Paste everything between the === markers into ChatGPT

===

You are generating educational Python tutorial files for a Senior Data Engineer
personal study system. Each file must be production-quality, heavily commented,
and fully runnable.

TOPIC: Delta Lake for Data Engineers
SLUG: delta-lake
PRIORITY: Toyota Interview Prep
INFRASTRUCTURE: Pure Python (delta-spark or deltalake library — local mode)

===== CODING STANDARDS =====

FILE HEADER — every file starts with:
# ============================================================
# Topic   : Delta Lake
# File    : NN_filename.py
# Covers  : one-line description
# Prereqs : pip install deltalake pandas pyarrow | OR pip install pyspark delta-spark
# Run     : python filename.py
# ============================================================

COMMENTS: Explain WHY. Explain Delta Lake internals (transaction log, _delta_log,
ACID guarantees, snapshot isolation) where concepts appear.

===== FILES TO GENERATE =====

01_delta_basics_and_acid.py
  Purpose: Create Delta tables, understand ACID transactions, transaction log structure
  Key concepts: _delta_log, JSON commit files, snapshot isolation, atomicity
  Functions:
    - create_delta_table(path, df) — write first Delta table, explain _delta_log creation
    - read_delta_table(path) — read current snapshot
    - inspect_transaction_log(path) — read _delta_log JSON files, show commit structure
    - demonstrate_atomicity(path) — show that failed write leaves table unchanged
    - append_to_table(path, df) — add records, show new _delta_log entry
  Main block: create table, inspect log, append, inspect log again

02_time_travel_and_versioning.py
  Purpose: Delta time travel — read historical versions, audit changes, restore
  Key concepts: version numbers, timestamp-based reads, RESTORE, audit log
  Functions:
    - read_version(path, version) — read table at specific version number
    - read_at_timestamp(path, timestamp) — read table as of a datetime
    - get_table_history(path) — show all versions with operation, timestamp, metrics
    - diff_versions(path, v1, v2) — compare two versions, show added/removed records
    - restore_to_version(path, version) — roll back table to previous version
  Main block: create table, make 3 changes, time travel through all versions

03_merge_upsert_patterns.py
  Purpose: MERGE INTO for upserts, SCD Type 2, conditional updates
  Key concepts: merge conditions, matched/not-matched clauses, SCD Type 2 implementation
  Functions:
    - simple_upsert(target_path, source_df, merge_key) — insert or update by key
    - conditional_merge(target_path, source_df, merge_key) — update only if value changed
    - implement_scd_type2(target_path, source_df, key_col, tracked_cols) — full SCD2 with valid_from/to
    - delete_matching_records(target_path, condition_df, join_key) — merge-based delete
    - demonstrate_concurrent_merge_safety(path) — show Delta handles concurrent merges
  Main block: build customer dimension with SCD Type 2, run 3 rounds of updates

04_schema_evolution_and_enforcement.py
  Purpose: Schema management — enforcement, evolution, column mapping
  Key concepts: schema enforcement (default), mergeSchema, overwriteSchema, column mapping
  Functions:
    - demonstrate_schema_enforcement(path) — show write failure on schema mismatch
    - add_column_safely(path, new_df_with_extra_col) — mergeSchema=True
    - change_column_type(path) — overwriteSchema for type changes
    - rename_column_without_rewrite(path, old_name, new_name) — column mapping feature
    - validate_schema_compatibility(existing_schema, new_schema) — pre-check before write
  Main block: evolve a schema through 4 changes, show what's safe vs breaking

05_optimize_and_vacuum.py
  Purpose: Table maintenance — OPTIMIZE, Z-ordering, VACUUM, file compaction
  Key concepts: small file problem, Z-order for multi-dimensional clustering, VACUUM retention
  Functions:
    - show_file_fragmentation(path) — count files per partition, show small file problem
    - optimize_table(path) — compact small files into larger ones
    - zorder_by_columns(path, columns) — Z-order for multi-column query pruning
    - vacuum_table(path, retention_hours=168) — remove old files, explain 7-day default
    - measure_query_speedup(path, filter_col, filter_val) — before/after optimize timing
  Main block: create fragmented table, optimize, Z-order, vacuum, compare query times

===== CAPSTONE PROJECT =====

capstone/brief.md
  Title: Change Data Capture (CDC) Pipeline with Delta Lake
  Scenario: A source system sends daily change feeds (inserts, updates, deletes)
    for a customer master table. Build a Delta Lake pipeline that applies changes
    using MERGE, maintains full history via SCD Type 2, and supports time travel
    for compliance audits.
  What to build:
    - Day 0: Load initial 1000 customer records into Delta table
    - Day 1: Apply 200 updates, 50 inserts, 20 deletes via MERGE
    - Day 2: Apply another 150 updates including some that revert Day 1 changes
    - Verify time travel: read Day 0 and Day 1 snapshots, confirm record counts
    - OPTIMIZE and Z-order by customer_region after Day 2
    - Compliance report: show all versions of a specific customer_id across all days
  Acceptance criteria:
    - MERGE runs idempotently (run twice = same result)
    - Time travel returns correct record counts for each day
    - SCD Type 2 shows correct valid_from / valid_to for changed records
    - VACUUM with 0-hour retention (test mode) removes old files

capstone/capstone.py — full CDC pipeline simulation
capstone/test_capstone.py — pytest validating merge idempotency, time travel counts

===== INFRASTRUCTURE NOTES =====

Pure Python — use the deltalake library (Rust-based, no JVM required) for files 1-4.
Install: pip install deltalake pandas pyarrow
For file 05 (OPTIMIZE/VACUUM) use delta-spark if deltalake library lacks those features.
All tables written to /tmp/studybook/delta/ or OUTPUT_DIR env var.
No AWS — local filesystem only for tutorials. Real Delta Lake on S3 shown in comments.

===== START =====

Acknowledge these instructions, then wait for me to say "generate file 01".

===
