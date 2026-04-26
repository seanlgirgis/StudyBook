# ChatGPT Prompt — Parquet Tutorial
# Paste everything between the === markers into ChatGPT

===

TOPIC: Parquet for Data Engineers
SLUG: parquet
PRIORITY: Toyota Interview Prep
INFRASTRUCTURE: Pure Python — pyarrow, pandas, local filesystem

===== CODING STANDARDS =====

FILE HEADER:
# ============================================================
# Topic   : Parquet for Data Engineers
# File    : NN_filename.py
# Covers  : one-line description
# Prereqs : pip install pyarrow pandas | no AWS or Docker needed
# Run     : python filename.py
# ============================================================

COMMENTS: Explain WHY. Parquet internals matter in interviews — explain columnar storage,
row groups, page encoding, dictionary encoding, predicate pushdown. Make it visceral:
compare file sizes, query times before and after. Use real numbers.
Env vars: OUTPUT_DIR (default: /tmp/studybook/parquet/)

===== FILES TO GENERATE =====

01_parquet_basics_and_internals.py
  Purpose: Understand Parquet from the inside — file format, schema, row groups, metadata
  Key concepts: columnar storage vs row-based, row groups (default 128MB), pages,
    footer metadata, column statistics (min/max), why columnar is faster for analytics
  Functions:
    - write_parquet(df: pd.DataFrame, path: str, row_group_size: int = 100_000) → None
    - read_parquet(path: str, columns: list[str] = None) → pd.DataFrame
      — columns= parameter shows columnar read-skipping
    - inspect_parquet_file(path: str) → dict
      — use pyarrow.parquet.ParquetFile to show: num_row_groups, schema, total_rows,
        file_size_bytes, per-column stats (min, max, null_count, compression)
    - compare_csv_vs_parquet(df: pd.DataFrame, output_dir: str) → dict
      — write same data as CSV and Parquet, compare: file size, write time, read time
    - explain_row_groups(path: str) → None
      — print row group count, rows per group, which group a given row falls in
    - generate_analytics_dataset(rows: int) → pd.DataFrame
      — synthetic e-commerce events: user_id, product_id, category, amount, ts, country
  Main block: generate 500k row dataset, write as CSV and Parquet, inspect internals,
    print size comparison (expect 5-10× compression), show column stats

02_compression_and_encoding.py
  Purpose: Parquet compression codecs and column encodings — choose wisely for your data
  Key concepts: SNAPPY vs GZIP vs ZSTD vs BROTLI, dictionary encoding, RLE,
    delta encoding for sorted columns, when each encoding fires automatically
  Functions:
    - write_with_codec(df: pd.DataFrame, path: str, compression: str) → dict
      — returns {codec, size_bytes, write_ms, read_ms}
    - benchmark_codecs(df: pd.DataFrame, output_dir: str) → pd.DataFrame
      — test all codecs: NONE, SNAPPY, GZIP, ZSTD, BROTLI; return comparison DataFrame
    - demonstrate_dictionary_encoding(output_dir: str) → None
      — create column with high cardinality vs low cardinality, compare sizes;
        explain: low-cardinality columns get dictionary encoded automatically
    - show_encoding_in_metadata(path: str) → None
      — inspect per-column encodings from file metadata (PLAIN, RLE_DICTIONARY, DELTA)
    - choose_codec(read_heavy: bool, write_heavy: bool, need_splittable: bool) → str
      — decision function: returns recommended codec with reasoning
  Main block: benchmark all codecs on 200k row dataset, print table sorted by size,
    annotate with recommended use case for each codec

03_partitioning_and_predicate_pushdown.py
  Purpose: Partitioned Parquet datasets — hive partitioning, predicate pushdown, partition pruning
  Key concepts: hive partitioning (country=US/date=2024-01-01/*.parquet), 
    row group statistics for pushdown, partition pruning vs page-level filtering
  Functions:
    - write_partitioned_dataset(df: pd.DataFrame, output_dir: str,
        partition_cols: list[str]) → None
      — use pyarrow.dataset.write_dataset with partitioning
    - read_with_filter(dataset_path: str, filters: list) → pd.DataFrame
      — use pyarrow.dataset filters for predicate pushdown; show rows scanned vs returned
    - demonstrate_partition_pruning(dataset_path: str, partition_col: str,
        filter_value: str) → dict
      — time query WITH and WITHOUT partition filter, show file count difference
    - demonstrate_row_group_pushdown(path: str, filter_col: str,
        filter_value) → dict
      — time filtered read vs full read on single Parquet file (row group stats)
    - design_partition_strategy(query_patterns: list[str],
        cardinality_map: dict) → str
      — return recommended partition columns with explanation
    - count_files_in_dataset(dataset_path: str) → dict
      — walk dataset directory, count files per partition, flag small files
  Main block: partition 1M rows by country + year + month, read with filter,
    print files scanned (should be << total), show timing improvement

04_schema_evolution_and_compatibility.py
  Purpose: Schema evolution — adding columns, type widening, reading old Parquet with new schema
  Key concepts: schema evolution (add nullable cols only safely), type widening (int32→int64),
    backward vs forward compatibility, schema merging
  Functions:
    - write_v1_schema(output_dir: str) → None — baseline schema
    - write_v2_schema_add_column(output_dir: str) → None — adds nullable column (safe)
    - write_v3_schema_widen_type(output_dir: str) → None — widens int32 → int64 (safe)
    - read_with_schema_merge(dataset_path: str) → pd.DataFrame
      — merge_schema=True: read mix of v1+v2+v3 files into unified schema
    - check_schema_compatibility(schema_old, schema_new) → dict
      — returns {compatible: bool, breaking_changes: list, safe_changes: list}
    - demonstrate_breaking_change(output_dir: str) → None
      — rename column (breaking) vs add column (safe): show what fails and why
    - explain_iceberg_vs_parquet_evolution() → None
      — print: why Parquet alone doesn't handle column renames (need Delta/Iceberg for that)
  Main block: write 3 schema versions, read merged dataset, run compatibility check,
    demonstrate safe vs breaking change clearly

05_parquet_in_production.py
  Purpose: Production Parquet patterns — file sizing, writing from PySpark, reading in Athena/Pandas
  Key concepts: small file problem, target file size (128MB-512MB), pandas chunked writes,
    reading Parquet from S3 locally via s3fs, PyArrow vs fastparquet
  Functions:
    - optimize_file_count(total_rows: int, target_file_size_mb: int = 128,
        avg_row_size_bytes: int = 200) → dict
      — calculate: rows per file, number of files, explain why
    - write_chunked(df: pd.DataFrame, output_dir: str, chunk_size: int) → list[str]
      — split DataFrame into chunks, write each as separate Parquet file
    - compact_small_files(dataset_path: str, target_size_mb: int = 128) → dict
      — read all small files, rewrite as fewer larger files, return before/after stats
    - benchmark_pyarrow_vs_pandas(path: str) → dict
      — compare pd.read_parquet vs pyarrow.parquet.read_table for same file
    - show_spark_parquet_config() → None
      — print recommended Spark config for Parquet: spark.sql.parquet.compression.codec,
        parquet.block.size, spark.sql.parquet.filterPushdown, etc. (no Spark runtime needed)
    - simulate_athena_query(dataset_path: str, sql: str) → pd.DataFrame
      — use DuckDB to run SQL on local Parquet files (mimics Athena behavior)
  Main block: write 100 small files, compact to target size, benchmark read,
    run 2 DuckDB queries on Parquet (mimicking Athena)

===== CAPSTONE PROJECT =====

capstone/brief.md
  Title: High-Performance Analytics Storage Layer
  Scenario: An IoT fleet generates 10M sensor records per day. Design and implement
    a Parquet storage layer that enables fast analytics queries with minimal storage cost.
  What to build:
    - generate_data.py: create 10M synthetic IoT records
        (device_id, plant_id, sensor_type, value, unit, ts, anomaly_flag)
    - write_optimized.py: 
        Write as partitioned Parquet (plant_id / year / month)
        ZSTD compression (best size/speed balance for analytics workload)
        128MB target row group size
        Compare against unpartitioned SNAPPY baseline: size, write time
    - query_benchmark.py: 5 analytics queries via DuckDB (simulating Athena):
        1. Last 24h anomalies by plant
        2. Hourly avg per sensor_type for one plant
        3. Top 10 devices by anomaly count (last 7 days)
        4. Monthly aggregation (full scan)
        5. Point lookup by device_id + ts range
        For each: time with and without partition filter, show file scan count
    - compact.py: simulate 1 day of small files (1k files × 10k rows),
        compact to target size, show before/after
    - test_capstone.py: pytest — validate compression benchmark results, schema compatibility

  Acceptance criteria:
    - ZSTD partitioned Parquet is ≥ 5× smaller than original CSV
    - Partition-filtered queries scan < 10% of files vs unfiltered
    - Compaction reduces 1000 files to < 10 files with same total rows
    - All DuckDB queries return correct row counts

capstone/capstone.py — query_benchmark.py (as above)
capstone/test_capstone.py — pytest file

===== INFRASTRUCTURE NOTES =====

Pure Python — no AWS, no Docker required.
Install: pip install pyarrow pandas duckdb
Optional: pip install s3fs (for reading from S3 — shown in comments only)
All data written to OUTPUT_DIR env var or /tmp/studybook/parquet/
DuckDB used to simulate Athena SQL queries on local Parquet files.

===== START =====

Acknowledge these instructions, then wait for me to say "generate file 01".

===
