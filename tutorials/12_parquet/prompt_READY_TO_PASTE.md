# ChatGPT Prompt — Parquet for Data Engineers
# READY TO PASTE — fully specified, no placeholders
# Paste everything between the === markers into ChatGPT

===

TOPIC: Parquet for Data Engineers
SLUG: parquet
PRIORITY: Toyota Interview Prep
INFRASTRUCTURE: Pure Python — pyarrow, pandas, duckdb, local filesystem
NO AWS, NO DOCKER, NO CLEANUP RULES NEEDED.

===== CODING STANDARDS =====

FILE HEADER (every file must start with this block):
# ============================================================
# Topic   : Parquet for Data Engineers
# File    : NN_filename.py
# Covers  : one-line description
# Prereqs : pip install pyarrow pandas duckdb
# Run     : python NN_filename.py
# ============================================================

CRITICAL — CODE QUALITY:
- Every function must be COMPLETE and FULLY RUNNABLE — no placeholders, no TODO
  comments, no pass statements, no "add logic here" stubs.
- Generate the ENTIRE file contents each time. Never truncate with "..." or "rest is same".
- Comments explain WHY — Parquet internals matter in interviews. Make it visceral:
  compare file sizes, query times. Use real numbers printed to console.
- Env vars: OUTPUT_DIR (default: /tmp/studybook/parquet/ on Linux/Mac,
  C:/tmp/studybook/parquet/ on Windows — detect with os.name)
- Use pathlib.Path throughout. Create directories with exist_ok=True.
- Every main() prints a clear section header before each demo block.

===== FILE 01: 01_parquet_basics_and_internals.py =====

Purpose: Understand Parquet from the inside — columnar storage, row groups, footer
metadata, column statistics. Every concept tested in Toyota-level interviews.

Implement these functions in this exact order:

def get_output_dir() -> Path:
    """Return OUTPUT_DIR from env or platform-specific default. Create if missing."""
    # os.name == 'nt' → C:/tmp/studybook/parquet/
    # otherwise → /tmp/studybook/parquet/

def generate_analytics_dataset(rows: int = 500_000) -> pd.DataFrame:
    """
    Synthetic e-commerce events. Columns:
      user_id:    string  "user_000001" … "user_010000"  (random choice of 10k users)
      product_id: string  "prod_0001"  … "prod_1000"    (random choice of 1k products)
      category:   string  one of ["electronics","clothing","books","food","sports"]
      amount:     float64 uniform 1.0–500.0, 2 decimal places
      ts:         datetime64[ns] last 90 days, random
      country:    string  one of ["US","UK","DE","FR","JP","AU","CA","BR"] with realistic weights
    Set numpy random seed = 42 for reproducibility.
    """

def write_parquet(df: pd.DataFrame, path: str, row_group_size: int = 100_000) -> None:
    """
    Write df to path as Parquet with SNAPPY compression.
    Use pyarrow.parquet.write_table with row_group_size parameter.
    Convert pandas DataFrame to pyarrow Table first.
    Print: path, row_group_size, total rows written.
    """

def read_parquet(path: str, columns: list[str] = None) -> pd.DataFrame:
    """
    Read Parquet file. If columns is not None, read only those columns
    (demonstrate columnar read-skipping). Print columns read, rows returned,
    and a note explaining WHY column projection reduces I/O.
    """

def inspect_parquet_file(path: str) -> dict:
    """
    Use pyarrow.parquet.ParquetFile to extract metadata. Return dict with:
      num_row_groups:  int
      schema_fields:   list of field names
      total_rows:      int
      file_size_bytes: int  (os.path.getsize)
      row_groups:      list of dicts, one per row group:
        { rg_index, num_rows, total_compressed_bytes,
          columns: list of { name, compression, encodings, compressed_bytes,
                             has_statistics, min_value, max_value, null_count } }
    Print a formatted summary: schema, row group count, per-column stats.
    Explain in a comment why min/max stats enable predicate pushdown.
    """

def compare_csv_vs_parquet(df: pd.DataFrame, output_dir: Path) -> dict:
    """
    Write the same DataFrame as both CSV and Parquet (SNAPPY).
    Time each write and read. Return:
      { csv_size_bytes, parquet_size_bytes, compression_ratio,
        csv_write_ms, parquet_write_ms,
        csv_read_ms,  parquet_read_ms }
    Print a formatted comparison table showing ratio and speedup.
    """

def explain_row_groups(path: str) -> None:
    """
    Print for each row group: index, row offset (first row number), row count,
    compressed size. Then explain: row groups are the unit of predicate pushdown —
    if a filter eliminates an entire row group, those bytes are never read from disk.
    """

def main():
    out = get_output_dir()
    df = generate_analytics_dataset(rows=500_000)
    path = str(out / "ecommerce_events.parquet")

    print("\n=== WRITE & READ ===")
    write_parquet(df, path, row_group_size=100_000)
    df_back = read_parquet(path, columns=["user_id", "amount", "country"])

    print("\n=== INTERNAL METADATA ===")
    metadata = inspect_parquet_file(path)
    # print formatted summary

    print("\n=== CSV vs PARQUET ===")
    stats = compare_csv_vs_parquet(df, out)
    # print table

    print("\n=== ROW GROUPS ===")
    explain_row_groups(path)

if __name__ == "__main__":
    main()

Expected output (approximate numbers acceptable, ratios must be realistic):
  CSV size:     ~45 MB
  Parquet size: ~6 MB   (compression ratio ~7.5×)
  Row groups:   5        (500k rows / 100k per group)

===== FILE 02: 02_compression_and_encoding.py =====

Purpose: Parquet compression codecs and column encodings — choose the right codec
for your workload. Print hard numbers that stick in an interviewer's memory.

def get_output_dir() -> Path:
    """Same as file 01."""

def generate_benchmark_dataset(rows: int = 200_000) -> pd.DataFrame:
    """
    Mixed-type dataset for encoding demo. Columns:
      id:         int64   sequential 0…rows-1
      category:   string  one of 5 values — LOW cardinality (dictionary encoding fires)
      subcategory: string  one of 100 values — MEDIUM cardinality
      description: string  uuid4 per row — HIGH cardinality (dictionary encoding skips)
      value:      float64 random
      timestamp:  int64   unix timestamps, monotonically increasing (delta encoding)
    Seed = 42.
    """

def write_with_codec(df: pd.DataFrame, path: str, compression: str) -> dict:
    """
    Write df with given compression codec. Measure write time and read time.
    Return:
      { codec: str, size_bytes: int, size_mb: float,
        write_ms: float, read_ms: float }
    Valid codecs: "NONE", "SNAPPY", "GZIP", "ZSTD", "BROTLI"
    """

def benchmark_codecs(df: pd.DataFrame, output_dir: Path) -> pd.DataFrame:
    """
    Call write_with_codec for all 5 codecs.
    Return a DataFrame with columns:
      codec, size_mb, compression_ratio, write_ms, read_ms
    Sort by size_mb ascending.
    compression_ratio = NONE_size / codec_size
    Print the table with annotations:
      SNAPPY  → "Best for streaming / Kafka / real-time"
      GZIP    → "Good compression, slow writes — cold storage"
      ZSTD    → "Best size+speed for analytics workloads ← RECOMMENDED"
      BROTLI  → "Smallest files, slowest writes — archive only"
      NONE    → "No compression — maximum read speed, maximum cost"
    """

def demonstrate_dictionary_encoding(output_dir: Path) -> None:
    """
    Create two DataFrames:
      low_card:  1M rows, 'category' column with 5 unique values
      high_card: 1M rows, 'description' column with 1M unique uuid4 values
    Write each as Parquet. Inspect per-column encoding from metadata.
    Print:
      Low cardinality  → encoding: RLE_DICTIONARY → size: X bytes
      High cardinality → encoding: PLAIN          → size: Y bytes
    Explain why: dictionary encoding maps each unique value to an int, then
    stores run-length encoded integers — transformative for repeated strings.
    """

def show_encoding_in_metadata(path: str) -> None:
    """
    Open file with pyarrow.parquet.ParquetFile. For each column in row group 0,
    print: column_name, encodings (list), compression.
    Expected encodings to highlight: PLAIN, RLE_DICTIONARY, DELTA_BINARY_PACKED.
    """

def choose_codec(read_heavy: bool, write_heavy: bool, need_splittable: bool) -> str:
    """
    Decision function. Returns recommended codec string with a one-line reason.
    Rules:
      need_splittable → "SNAPPY"  (Hadoop MapReduce requires splittable codecs)
      write_heavy and not read_heavy → "SNAPPY"
      read_heavy and not write_heavy → "ZSTD"
      balanced workload → "ZSTD"
      archive / infrequent reads → "BROTLI"
    Print recommendation and reason. Return codec string.
    """

def main():
    out = get_output_dir()
    df = generate_benchmark_dataset(rows=200_000)

    print("\n=== CODEC BENCHMARK ===")
    results = benchmark_codecs(df, out)
    print(results.to_string(index=False))

    print("\n=== DICTIONARY ENCODING DEMO ===")
    demonstrate_dictionary_encoding(out)

    print("\n=== ENCODING METADATA ===")
    snappy_path = str(out / "bench_SNAPPY.parquet")
    show_encoding_in_metadata(snappy_path)

    print("\n=== CODEC RECOMMENDATION ===")
    choose_codec(read_heavy=True, write_heavy=False, need_splittable=False)
    choose_codec(read_heavy=False, write_heavy=True, need_splittable=False)
    choose_codec(read_heavy=False, write_heavy=False, need_splittable=True)

if __name__ == "__main__":
    main()

===== FILE 03: 03_partitioning_and_predicate_pushdown.py =====

Purpose: Hive partitioning + predicate pushdown. Show the query speedup with hard numbers.
This is the most important Parquet concept for Toyota/data lake interviews.

def get_output_dir() -> Path:
    """Same pattern."""

def generate_partitioned_dataset(rows: int = 1_000_000) -> pd.DataFrame:
    """
    IoT sensor readings. Columns:
      device_id:   string  "device_{i:04d}" for i in 0..99
      plant_id:    string  one of ["plant_A","plant_B","plant_C"]
      sensor_type: string  one of ["temperature","pressure","vibration","humidity"]
      value:       float64 random
      ts:          datetime64[ns] last 12 months, random
      year:        int32   extracted from ts
      month:       int32   extracted from ts
    Seed = 42.
    """

def write_partitioned_dataset(df: pd.DataFrame, output_dir: Path,
                               partition_cols: list[str]) -> None:
    """
    Use pyarrow.dataset.write_dataset with hive partitioning.
    partition_cols example: ["plant_id", "year", "month"]
    Hive layout: output_dir/plant_id=plant_A/year=2024/month=1/part-0.parquet
    Use SNAPPY compression, max_rows_per_file=200_000.
    Print total files written and directory tree (2 levels deep).
    """

def count_files_in_dataset(dataset_path: Path) -> dict:
    """
    Walk dataset directory. Return:
      { total_files: int, files_per_partition: dict,
        avg_file_size_mb: float, min_file_size_mb: float, max_file_size_mb: float }
    Flag small files: print warning if any file < 1 MB.
    """

def read_with_filter(dataset_path: Path, filters) -> pd.DataFrame:
    """
    Open dataset with pyarrow.dataset.dataset(). Apply filters using
    pyarrow filter expressions. Print rows returned.
    Example filter: ds.field("plant_id") == "plant_A"
    """

def demonstrate_partition_pruning(dataset_path: Path, plant_id: str = "plant_A") -> dict:
    """
    Time two reads:
      1. WITHOUT partition filter: scan all files
      2. WITH partition filter: plant_id == plant_id
    Return:
      { unfiltered_ms: float, filtered_ms: float, speedup_x: float,
        unfiltered_file_count: int, filtered_file_count: int,
        pct_files_scanned: float }
    Print comparison. Explain: partition pruning means files in other partitions
    are never opened — OS-level skipping, not row-level filtering.
    """

def demonstrate_row_group_pushdown(path: str, filter_col: str = "sensor_type",
                                    filter_value: str = "temperature") -> dict:
    """
    On a SINGLE non-partitioned Parquet file with multiple row groups:
    Time full read vs filtered read using pyarrow filters.
    Return: { full_read_ms, filtered_ms, full_rows, filtered_rows }
    Explain: row group statistics (min/max per column) allow skipping entire
    row groups without reading their pages — this is predicate pushdown.
    """

def design_partition_strategy(query_patterns: list[str],
                               cardinality_map: dict) -> str:
    """
    Simple rule-based advisor. Rules:
      - Partition columns must appear in WHERE clauses of most queries
      - Avoid high cardinality (>10k unique values) as partition key → too many small files
      - Prefer columns with 3–100 unique values
      - At most 3 partition levels for manageability
    Print recommendation as numbered list with reasoning.
    Return recommended partition columns as comma-separated string.

    Example call:
      design_partition_strategy(
          query_patterns=["WHERE region=? AND date=?", "WHERE region=?"],
          cardinality_map={"region": 5, "date": 365, "device_id": 10000}
      )
    """

def main():
    out = get_output_dir()
    df = generate_partitioned_dataset(rows=1_000_000)

    part_dir = out / "iot_partitioned"
    print("\n=== WRITE PARTITIONED DATASET ===")
    write_partitioned_dataset(df, part_dir, partition_cols=["plant_id", "year", "month"])

    print("\n=== DATASET FILE COUNT ===")
    stats = count_files_in_dataset(part_dir)
    print(stats)

    print("\n=== PARTITION PRUNING BENCHMARK ===")
    pruning = demonstrate_partition_pruning(part_dir, plant_id="plant_A")
    print(f"Speedup: {pruning['speedup_x']:.1f}×  |  "
          f"Files scanned: {pruning['pct_files_scanned']:.1f}%")

    print("\n=== ROW GROUP PUSHDOWN ===")
    single_file = str(out / "ecommerce_events.parquet")  # from file 01
    if Path(single_file).exists():
        rg_stats = demonstrate_row_group_pushdown(single_file)
        print(rg_stats)

    print("\n=== PARTITION STRATEGY ADVISOR ===")
    design_partition_strategy(
        query_patterns=["WHERE plant_id=? AND sensor_type=?", "WHERE plant_id=?"],
        cardinality_map={"plant_id": 3, "sensor_type": 4, "device_id": 100}
    )

if __name__ == "__main__":
    main()

===== FILE 04: 04_schema_evolution_and_compatibility.py =====

Purpose: Schema evolution — the silent killer in production data lakes.
Understand what Parquet can and cannot do without Delta Lake / Iceberg.

def get_output_dir() -> Path: ...

def write_v1_schema(output_dir: Path) -> str:
    """
    Write 50k rows with v1 schema:
      device_id: string, sensor_type: string, value: float32, ts: int64 (unix ms)
    Use SNAPPY. Save to output_dir/schema_evolution/v1/part-0.parquet
    Return file path.
    """

def write_v2_schema_add_column(output_dir: Path) -> str:
    """
    Add nullable column 'unit' (string, nullable). 50k rows.
    Rows have unit = one of ["C","PSI","mm/s","RH%"] or None (20% null).
    Save to output_dir/schema_evolution/v2/part-0.parquet. Return path.
    SAFE CHANGE: adding a nullable column is always backward-compatible.
    """

def write_v3_schema_widen_type(output_dir: Path) -> str:
    """
    Widen value column from float32 → float64. Add 'firmware_version' string column.
    50k rows. Save to output_dir/schema_evolution/v3/part-0.parquet. Return path.
    SAFE CHANGE: widening numeric types is backward-compatible (float32 reads as float64).
    """

def read_with_schema_merge(dataset_path: Path) -> pd.DataFrame:
    """
    Read v1 + v2 + v3 files together using pyarrow.parquet.ParquetDataset
    with schema merge. Columns missing in older files become null.
    Print final schema and null counts per column.
    Return merged DataFrame.
    """

def check_schema_compatibility(schema_old, schema_new) -> dict:
    """
    Compare two pyarrow schemas. Return:
      { compatible: bool,
        breaking_changes: list[str],   e.g. ["column 'value' type changed int→str"]
        safe_changes: list[str],       e.g. ["added nullable column 'unit'"]
        removed_columns: list[str],
        added_columns: list[str] }
    Breaking changes:
      - type change that is not a widening (e.g. float→string, int→string)
      - column removal
      - renaming (removal + add = breaking)
    Safe changes:
      - add nullable column
      - widen numeric type (int32→int64, float32→float64)
    """

def demonstrate_breaking_change(output_dir: Path) -> None:
    """
    Show two scenarios side by side:

    SCENARIO A (safe): Write 1k rows with schema_v1, then 1k rows with schema_v2
      (added nullable column). Read both. No errors.

    SCENARIO B (breaking): Write 1k rows where 'value' is float64. Write 1k rows
      where 'value' is string. Try to read both together — catch the ArrowInvalid
      or ArrowNotImplementedError exception. Print the error message clearly,
      then explain: "This is why you need Delta Lake or Apache Iceberg for column renames
      and type changes — Parquet alone has no schema registry."
    """

def explain_iceberg_vs_parquet_evolution() -> None:
    """
    Print a formatted comparison table:
    
    Operation              | Raw Parquet | Delta Lake | Apache Iceberg
    ----------------------|-------------|------------|---------------
    Add nullable column   | ✅ Safe      | ✅ Safe     | ✅ Safe
    Widen numeric type    | ✅ Safe      | ✅ Safe     | ✅ Safe
    Rename column         | ❌ Breaking  | ✅ Metadata | ✅ Metadata
    Drop column           | ❌ Breaking  | ✅ Metadata | ✅ Metadata
    Change type (str→int) | ❌ Breaking  | ❌ Breaking | ❌ Breaking
    Time-travel reads     | ❌ No        | ✅ Yes      | ✅ Yes
    ACID transactions     | ❌ No        | ✅ Yes      | ✅ Yes

    Key insight: Parquet is a file format. Delta Lake and Iceberg add a
    transaction log / metadata layer on top. Column renames are metadata-only
    operations in Iceberg — zero file rewrite needed.
    """

def main():
    out = get_output_dir()

    print("\n=== WRITE 3 SCHEMA VERSIONS ===")
    v1 = write_v1_schema(out)
    v2 = write_v2_schema_add_column(out)
    v3 = write_v3_schema_widen_type(out)

    print("\n=== SCHEMA MERGE READ ===")
    evo_dir = out / "schema_evolution"
    df_merged = read_with_schema_merge(evo_dir)
    print(f"Merged rows: {len(df_merged)}  Columns: {list(df_merged.columns)}")

    print("\n=== COMPATIBILITY CHECK ===")
    import pyarrow.parquet as pq
    s1 = pq.read_schema(v1)
    s3 = pq.read_schema(v3)
    compat = check_schema_compatibility(s1, s3)
    print(compat)

    print("\n=== BREAKING CHANGE DEMO ===")
    demonstrate_breaking_change(out)

    print("\n=== ICEBERG vs PARQUET EVOLUTION ===")
    explain_iceberg_vs_parquet_evolution()

if __name__ == "__main__":
    main()

===== FILE 05: 05_parquet_in_production.py =====

Purpose: Production Parquet patterns — file sizing, compaction, DuckDB as Athena simulator.
The DuckDB-as-Athena pattern is a real Toyota/Capital One interview topic.

def get_output_dir() -> Path: ...

def optimize_file_count(total_rows: int, target_file_size_mb: int = 128,
                        avg_row_size_bytes: int = 200) -> dict:
    """
    Calculate optimal number of files and rows per file.
    Return:
      { total_rows, avg_row_size_bytes, target_file_size_mb,
        rows_per_file: int, num_files: int,
        actual_file_size_mb: float }
    Print explanation: "Target 128MB–512MB per Parquet file. Too small → metadata overhead.
    Too large → slow partial reads and imbalanced parallelism."
    """

def write_chunked(df: pd.DataFrame, output_dir: Path, chunk_size: int) -> list[str]:
    """
    Split df into chunks of chunk_size rows. Write each chunk as a separate
    Parquet file: part-{i:04d}.parquet with SNAPPY compression.
    Return list of written file paths.
    Print: files written, average file size.
    """

def compact_small_files(dataset_path: Path, target_size_mb: int = 128) -> dict:
    """
    Read all .parquet files in dataset_path into a single DataFrame.
    Calculate target rows per file from target_size_mb and actual avg row size.
    Write compacted files to dataset_path / "compacted/" using write_chunked.
    Return:
      { before_file_count: int, after_file_count: int,
        before_total_size_mb: float, after_total_size_mb: float,
        total_rows: int, rows_preserved: bool }
    Print before/after comparison.
    """

def benchmark_pyarrow_vs_pandas(path: str) -> dict:
    """
    Read the same file using both:
      1. pd.read_parquet(path)                         — pandas engine
      2. pyarrow.parquet.read_table(path).to_pandas()  — pyarrow engine
    Time 3 runs each, take median. Return:
      { pandas_median_ms: float, pyarrow_median_ms: float,
        faster: str, speedup_pct: float }
    Print comparison. Note: difference matters most on large files.
    """

def show_spark_parquet_config() -> None:
    """
    Print recommended Spark configuration for Parquet (no Spark runtime needed —
    just print the config block as a string). Include:
      spark.sql.parquet.compression.codec = zstd
      spark.sql.parquet.filterPushdown = true
      spark.sql.parquet.mergeSchema = false        # set true only when needed — expensive
      spark.sql.files.maxPartitionBytes = 134217728 # 128MB
      spark.sql.parquet.columnarReaderBatchSize = 4096
      parquet.block.size = 134217728               # 128MB row group
      parquet.page.size = 1048576                  # 1MB page
    For each config print a one-line explanation.
    """

def simulate_athena_query(dataset_path: Path, sql: str, label: str = "") -> dict:
    """
    Use duckdb.connect() to run SQL on local Parquet files.
    The SQL uses read_parquet(glob_pattern) or a VIEW registered on the dataset.
    Return: { label: str, rows: int, duration_ms: float, preview: str }
    where preview is the first 3 rows as a string (df.head(3).to_string()).
    Print query label, duration, row count.
    """

def main():
    out = get_output_dir()

    print("\n=== FILE SIZING CALCULATOR ===")
    calc = optimize_file_count(total_rows=10_000_000, avg_row_size_bytes=150)
    print(calc)

    print("\n=== WRITE 100 SMALL FILES ===")
    import pandas as pd, numpy as np
    np.random.seed(42)
    df = pd.DataFrame({
        "device_id": [f"d{i:04d}" for i in np.random.randint(0, 100, 500_000)],
        "value": np.random.rand(500_000),
        "ts": pd.date_range("2024-01-01", periods=500_000, freq="1min"),
    })
    small_dir = out / "small_files"
    small_dir.mkdir(exist_ok=True)
    write_chunked(df, small_dir, chunk_size=5_000)   # 100 files × 5k rows

    print("\n=== COMPACT SMALL FILES ===")
    compact_stats = compact_small_files(small_dir, target_size_mb=128)
    print(compact_stats)

    print("\n=== PYARROW vs PANDAS BENCHMARK ===")
    sample_path = str(out / "ecommerce_events.parquet")
    from pathlib import Path as P
    if P(sample_path).exists():
        bm = benchmark_pyarrow_vs_pandas(sample_path)
        print(bm)
    else:
        print("Run file 01 first to create ecommerce_events.parquet")

    print("\n=== SPARK PARQUET CONFIG ===")
    show_spark_parquet_config()

    print("\n=== DUCKDB / ATHENA SIMULATION ===")
    # Register the partitioned dataset from file 03 if it exists
    part_dir = out / "iot_partitioned"
    if part_dir.exists():
        glob = str(part_dir / "**" / "*.parquet")
        simulate_athena_query(
            part_dir,
            sql=f"SELECT plant_id, COUNT(*) as cnt FROM read_parquet('{glob}', hive_partitioning=true) GROUP BY plant_id",
            label="Row count per plant"
        )
        simulate_athena_query(
            part_dir,
            sql=f"SELECT sensor_type, AVG(value) as avg_val FROM read_parquet('{glob}', hive_partitioning=true) WHERE plant_id='plant_A' GROUP BY sensor_type",
            label="Avg value per sensor type (plant_A)"
        )
    else:
        print("Run file 03 first to create partitioned dataset")

if __name__ == "__main__":
    main()

===== CAPSTONE PROJECT =====

Title: High-Performance Analytics Storage Layer
Scenario: An IoT fleet generates 10M sensor records per day. Design and implement
a Parquet storage layer enabling fast analytics with minimal storage cost.

Directory layout:
  capstone/
    setup.py            ← generates 10M records and saves raw CSV
    write_optimized.py  ← writes partitioned ZSTD Parquet + SNAPPY baseline
    query_benchmark.py  ← 5 DuckDB analytics queries (simulates Athena)
    compact.py          ← simulates 1 day of small files then compacts them
    test_capstone.py    ← pytest, 7 tests

===== CAPSTONE FILE: setup.py =====

"""
Generates 10M synthetic IoT records and saves raw CSV.
Run this first — all other capstone scripts depend on its output.
"""

OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", default_output_dir()))  # same pattern

RAW_CSV = OUTPUT_DIR / "capstone" / "raw" / "sensor_readings_10m.csv"
RAW_PARQUET = OUTPUT_DIR / "capstone" / "raw" / "sensor_readings_10m.parquet"

DEVICES = [f"device_{i:03d}" for i in range(50)]
PLANTS  = ["plant_A", "plant_B", "plant_C"]
SENSORS = ["temperature", "pressure", "vibration", "humidity"]
DEVICE_TO_PLANT = {d: PLANTS[i % 3] for i, d in enumerate(DEVICES)}

def generate_iot_records(n_rows: int = 10_000_000, seed: int = 42) -> pd.DataFrame:
    """
    Return DataFrame with columns:
      device_id:   string  sampled from DEVICES (50 devices)
      plant_id:    string  determined by DEVICE_TO_PLANT mapping
      sensor_type: string  sampled from SENSORS
      value:       float64 realistic ranges per sensor_type:
                     temperature: 15.0–95.0
                     pressure:    1.0–10.0
                     vibration:   0.0–50.0
                     humidity:    20.0–100.0
      unit:        string  temperature→"C", pressure→"bar", vibration→"mm/s", humidity→"%"
      ts:          datetime64[ns] random within last 30 days
      year:        int32   extracted from ts
      month:       int32   extracted from ts
      day:         int32   extracted from ts
      anomaly_flag: bool   True for ~2% of records (value > 95th percentile per sensor_type)

    Generate in chunks of 1_000_000 rows to avoid OOM. Concatenate and return.
    Print progress every 1M rows: "Generated 1,000,000 / 10,000,000 rows..."
    """

def save_raw(df: pd.DataFrame) -> None:
    """
    Save df as both CSV (RAW_CSV) and Parquet SNAPPY (RAW_PARQUET).
    Print file sizes and time taken for each.
    Print: "Setup complete. Run write_optimized.py next."
    """

def main():
    print("=== CAPSTONE SETUP: Generating 10M IoT Records ===")
    df = generate_iot_records(10_000_000)
    save_raw(df)

===== CAPSTONE FILE: write_optimized.py =====

"""
Writes the 10M records as:
  A. Partitioned ZSTD Parquet (plant_id / year / month)
  B. Single-file SNAPPY Parquet (unpartitioned baseline)
Compares size, write time, and query performance potential.
"""

PARTITIONED_DIR = OUTPUT_DIR / "capstone" / "partitioned"
BASELINE_PATH   = OUTPUT_DIR / "capstone" / "baseline" / "sensor_readings_snappy.parquet"

def load_raw() -> pd.DataFrame:
    """Read RAW_PARQUET if it exists, else read RAW_CSV. Print rows loaded."""

def write_partitioned_zstd(df: pd.DataFrame, output_dir: Path) -> dict:
    """
    Write as hive-partitioned Parquet:
      partition columns: ["plant_id", "year", "month"]
      compression: ZSTD
      max_rows_per_file: 500_000
    Return:
      { path: str, file_count: int, total_size_bytes: int,
        total_size_mb: float, write_ms: float }
    """

def write_baseline_snappy(df: pd.DataFrame, path: Path) -> dict:
    """
    Write as single SNAPPY Parquet file (no partitioning).
    Return: { path: str, size_bytes: int, size_mb: float, write_ms: float }
    """

def print_comparison(zstd: dict, snappy: dict, csv_size_mb: float) -> None:
    """
    Print formatted comparison table:

    Format        | Files | Size (MB) | vs CSV  | Write (s)
    --------------|-------|-----------|---------|----------
    Raw CSV       |   1   | 1200.0    | 1.0×    |  45.2
    SNAPPY single |   1   |  180.0    | 6.7×    |   8.1
    ZSTD part.    |  36   |  120.0    | 10.0×   |  12.3  ← RECOMMENDED
    """

def main():
    df = load_raw()
    zstd_stats  = write_partitioned_zstd(df, PARTITIONED_DIR)
    snappy_stats = write_baseline_snappy(df, BASELINE_PATH)
    csv_size_mb = os.path.getsize(RAW_CSV) / 1_000_000 if RAW_CSV.exists() else 0
    print_comparison(zstd_stats, snappy_stats, csv_size_mb)

===== CAPSTONE FILE: query_benchmark.py =====

"""
5 analytics queries via DuckDB — simulating what Athena would run.
Each query runs twice: once on partitioned ZSTD, once on SNAPPY baseline.
Shows file-scan reduction from partitioning.
"""

import duckdb, time
con = duckdb.connect()

PARTITIONED_GLOB = str(PARTITIONED_DIR / "**" / "*.parquet")
BASELINE_PATH_STR = str(BASELINE_PATH)

def run_timed_query(con, sql: str) -> tuple[pd.DataFrame, float]:
    """Execute sql on con. Return (result_df, duration_ms)."""

def register_datasets(con) -> None:
    """
    Register two VIEWs on the DuckDB connection:
      CREATE OR REPLACE VIEW iot_partitioned AS
        SELECT * FROM read_parquet(PARTITIONED_GLOB, hive_partitioning=true)
      CREATE OR REPLACE VIEW iot_baseline AS
        SELECT * FROM read_parquet(BASELINE_PATH_STR)
    """

def q1_anomalies_last_24h(con) -> dict:
    """
    SQL: SELECT plant_id, COUNT(*) AS anomaly_count
         FROM iot_partitioned
         WHERE anomaly_flag = true
           AND ts >= NOW() - INTERVAL '24 hours'
         GROUP BY plant_id ORDER BY anomaly_count DESC
    Return: { label, rows, duration_ms, preview }
    NOTE: since data is synthetic (last 30 days), filter may return 0 rows —
    that is acceptable; print a note explaining it and show total anomalies instead.
    """

def q2_hourly_avg_by_sensor(con, plant_id: str = "plant_A") -> dict:
    """
    SQL: SELECT DATE_TRUNC('hour', ts) AS hour_bucket,
                sensor_type, AVG(value) AS avg_value, COUNT(*) AS reading_count
         FROM iot_partitioned
         WHERE plant_id = '{plant_id}'
         GROUP BY hour_bucket, sensor_type
         ORDER BY hour_bucket, sensor_type
    """

def q3_top10_devices_by_anomaly(con) -> dict:
    """
    SQL: SELECT device_id, plant_id, COUNT(*) AS anomaly_count
         FROM iot_partitioned
         WHERE anomaly_flag = true
         GROUP BY device_id, plant_id
         ORDER BY anomaly_count DESC LIMIT 10
    """

def q4_monthly_aggregation(con) -> dict:
    """
    SQL: SELECT year, month, sensor_type,
                AVG(value) AS avg_val, MIN(value) AS min_val,
                MAX(value) AS max_val, COUNT(*) AS reading_count
         FROM iot_partitioned
         GROUP BY year, month, sensor_type
         ORDER BY year, month, sensor_type
    (Full scan — worst case. Show that even full scans benefit from ZSTD compression
    via smaller I/O.)
    """

def q5_point_lookup(con, device_id: str = "device_001") -> dict:
    """
    SQL: SELECT * FROM iot_partitioned
         WHERE device_id = '{device_id}'
           AND ts >= CURRENT_DATE - INTERVAL '7 days'
         ORDER BY ts DESC LIMIT 100
    """

def benchmark_partition_vs_baseline(con) -> None:
    """
    Run q2_hourly_avg_by_sensor (a partition-filtered query) on BOTH views.
    Print:
      Partitioned ZSTD:  X ms  (scans ~1/3 of files — plant_A partition only)
      SNAPPY baseline:   Y ms  (scans 100% of file)
      Speedup: Z×
    Note: explain that DuckDB on local disk may not show dramatic speedup,
    but in S3/Athena the difference is enormous due to data transfer cost.
    """

def main():
    register_datasets(con)

    print("\n=== QUERY 1: Anomalies Last 24h ===")
    r1 = q1_anomalies_last_24h(con)
    print(f"  {r1['rows']} rows  |  {r1['duration_ms']:.0f} ms")
    print(r1['preview'])

    print("\n=== QUERY 2: Hourly Avg by Sensor (plant_A) ===")
    r2 = q2_hourly_avg_by_sensor(con, "plant_A")
    print(f"  {r2['rows']} rows  |  {r2['duration_ms']:.0f} ms")
    print(r2['preview'])

    print("\n=== QUERY 3: Top 10 Devices by Anomaly Count ===")
    r3 = q3_top10_devices_by_anomaly(con)
    print(f"  {r3['rows']} rows  |  {r3['duration_ms']:.0f} ms")
    print(r3['preview'])

    print("\n=== QUERY 4: Monthly Aggregation (full scan) ===")
    r4 = q4_monthly_aggregation(con)
    print(f"  {r4['rows']} rows  |  {r4['duration_ms']:.0f} ms")

    print("\n=== QUERY 5: Point Lookup device_001 last 7 days ===")
    r5 = q5_point_lookup(con, "device_001")
    print(f"  {r5['rows']} rows  |  {r5['duration_ms']:.0f} ms")
    print(r5['preview'])

    print("\n=== PARTITION vs BASELINE BENCHMARK ===")
    benchmark_partition_vs_baseline(con)

===== CAPSTONE FILE: compact.py =====

"""
Simulates a day of small files arriving from a streaming pipeline,
then compacts them to target file size.
"""

SMALL_FILES_DIR  = OUTPUT_DIR / "capstone" / "small_files"
COMPACTED_DIR    = OUTPUT_DIR / "capstone" / "compacted"
N_SMALL_FILES    = 1_000
ROWS_PER_FILE    = 10_000     # 1k files × 10k rows = 10M rows total

def generate_small_files(output_dir: Path, n_files: int = N_SMALL_FILES,
                          rows_per_file: int = ROWS_PER_FILE, seed: int = 42) -> dict:
    """
    Write n_files Parquet files (SNAPPY), each with rows_per_file rows.
    Schema: device_id, plant_id, sensor_type, value, ts, anomaly_flag
    (same as main dataset — use same generation logic, smaller batches)
    Print progress every 100 files.
    Return:
      { file_count: int, total_rows: int,
        total_size_mb: float, avg_file_size_kb: float }
    """

def compact_to_target(input_dir: Path, output_dir: Path,
                       target_size_mb: int = 128) -> dict:
    """
    Algorithm:
      1. Read all .parquet files in input_dir into one DataFrame
      2. Calculate avg_row_bytes = total_size_bytes / total_rows
      3. rows_per_file = (target_size_mb * 1_000_000) // avg_row_bytes
      4. Write compacted files using write_chunked logic (reuse or inline)
      5. Verify total_rows matches
    Return:
      { before_file_count: int, after_file_count: int,
        before_size_mb: float, after_size_mb: float,
        total_rows: int, rows_preserved: bool }
    Print before/after summary.
    """

def main():
    print("=== CAPSTONE COMPACT: Simulating Small File Problem ===")

    print(f"\nGenerating {N_SMALL_FILES} small files × {ROWS_PER_FILE:,} rows each...")
    before = generate_small_files(SMALL_FILES_DIR)
    print(f"  {before['file_count']} files  |  "
          f"{before['total_size_mb']:.1f} MB  |  "
          f"avg {before['avg_file_size_kb']:.1f} KB per file")

    print("\nCompacting to 128 MB target file size...")
    after = compact_to_target(SMALL_FILES_DIR, COMPACTED_DIR, target_size_mb=128)
    print(f"\n  BEFORE: {after['before_file_count']} files  |  "
          f"{after['before_size_mb']:.1f} MB")
    print(f"  AFTER:  {after['after_file_count']} files  |  "
          f"{after['after_size_mb']:.1f} MB")
    print(f"  Rows preserved: {after['rows_preserved']}  "
          f"({after['total_rows']:,} rows)")
    print(f"\n  File count reduction: "
          f"{after['before_file_count'] / after['after_file_count']:.0f}×")

===== CAPSTONE FILE: test_capstone.py =====

"""
pytest — 7 tests validating the capstone storage layer.
Run: pytest test_capstone.py -v
"""

import pytest, os, duckdb
import pyarrow.parquet as pq
from pathlib import Path
import pandas as pd

# Resolve paths same way as capstone scripts
OUTPUT_DIR     = Path(os.getenv("OUTPUT_DIR", ...))  # same default
RAW_PARQUET    = OUTPUT_DIR / "capstone" / "raw"    / "sensor_readings_10m.parquet"
PARTITIONED    = OUTPUT_DIR / "capstone" / "partitioned"
BASELINE       = OUTPUT_DIR / "capstone" / "baseline" / "sensor_readings_snappy.parquet"
SMALL_FILES    = OUTPUT_DIR / "capstone" / "small_files"
COMPACTED      = OUTPUT_DIR / "capstone" / "compacted"

# ── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def raw_df():
    """Load raw parquet once for the whole test session."""
    assert RAW_PARQUET.exists(), f"Run setup.py first: {RAW_PARQUET} not found"
    return pd.read_parquet(RAW_PARQUET)

@pytest.fixture(scope="session")
def con():
    c = duckdb.connect()
    glob = str(PARTITIONED / "**" / "*.parquet")
    c.execute(f"CREATE OR REPLACE VIEW iot AS "
              f"SELECT * FROM read_parquet('{glob}', hive_partitioning=true)")
    yield c
    c.close()

# ── Tests ────────────────────────────────────────────────────────────────────

def test_raw_dataset_has_10m_rows(raw_df):
    """setup.py must generate exactly 10,000,000 rows."""
    assert len(raw_df) == 10_000_000, f"Expected 10M rows, got {len(raw_df):,}"

def test_required_columns_present(raw_df):
    """Schema must include all 9 required columns."""
    required = {"device_id", "plant_id", "sensor_type",
                "value", "unit", "ts", "year", "month", "anomaly_flag"}
    missing = required - set(raw_df.columns)
    assert not missing, f"Missing columns: {missing}"

def test_anomaly_flag_rate(raw_df):
    """anomaly_flag should be True for roughly 2% of records (1%–5% tolerance)."""
    rate = raw_df["anomaly_flag"].mean()
    assert 0.01 <= rate <= 0.05, f"Anomaly rate out of range: {rate:.4f}"

def test_zstd_partitioned_smaller_than_snappy_baseline():
    """ZSTD partitioned Parquet must be smaller than SNAPPY single file."""
    assert PARTITIONED.exists(), "Run write_optimized.py first"
    assert BASELINE.exists(),    "Run write_optimized.py first"

    def dir_size(p: Path) -> int:
        return sum(f.stat().st_size for f in p.rglob("*.parquet"))

    zstd_bytes   = dir_size(PARTITIONED)
    snappy_bytes = BASELINE.stat().st_size
    assert zstd_bytes < snappy_bytes, (
        f"ZSTD ({zstd_bytes/1e6:.1f} MB) should be smaller than "
        f"SNAPPY ({snappy_bytes/1e6:.1f} MB)"
    )

def test_partition_filter_returns_correct_plant(con):
    """Querying plant_A partition must return only plant_A rows."""
    result = con.execute(
        "SELECT DISTINCT plant_id FROM iot WHERE plant_id = 'plant_A'"
    ).fetchdf()
    assert len(result) == 1
    assert result["plant_id"].iloc[0] == "plant_A"

def test_monthly_agg_has_all_plants(con):
    """Monthly aggregation must return rows for all 3 plants."""
    result = con.execute(
        "SELECT DISTINCT plant_id FROM iot ORDER BY plant_id"
    ).fetchdf()
    plants = set(result["plant_id"].tolist())
    assert plants == {"plant_A", "plant_B", "plant_C"}, \
        f"Expected 3 plants, got: {plants}"

def test_compaction_reduces_file_count():
    """compact.py must reduce 1000 small files to fewer than 20 files."""
    assert SMALL_FILES.exists(),  "Run compact.py first"
    assert COMPACTED.exists(),    "Run compact.py first"

    small_count    = len(list(SMALL_FILES.rglob("*.parquet")))
    compacted_count = len(list(COMPACTED.rglob("*.parquet")))

    assert small_count >= 900, \
        f"Expected ~1000 small files, found {small_count}"
    assert compacted_count < 20, \
        f"Expected < 20 compacted files, got {compacted_count}"

    # Row count must be preserved
    small_rows    = sum(pq.read_metadata(f).num_rows
                        for f in SMALL_FILES.rglob("*.parquet"))
    compacted_rows = sum(pq.read_metadata(f).num_rows
                         for f in COMPACTED.rglob("*.parquet"))
    assert small_rows == compacted_rows, \
        f"Row count mismatch: {small_rows:,} before vs {compacted_rows:,} after"

===== GENERATION SEQUENCE =====

Acknowledge these instructions, then wait for me to say "generate file 01".

After I confirm each file, I will say "generate file 02", etc.

Generation order:
  "generate file 01"  → 01_parquet_basics_and_internals.py
  "generate file 02"  → 02_compression_and_encoding.py
  "generate file 03"  → 03_partitioning_and_predicate_pushdown.py
  "generate file 04"  → 04_schema_evolution_and_compatibility.py
  "generate file 05"  → 05_parquet_in_production.py
  "generate readme"   → README.md
  "generate setup"    → capstone/setup.py
  "generate write"    → capstone/write_optimized.py
  "generate queries"  → capstone/query_benchmark.py
  "generate compact"  → capstone/compact.py
  "generate tests"    → capstone/test_capstone.py

Each file must be COMPLETE and FULLY RUNNABLE.
No placeholders. No TODO comments. No pass statements.
Generate the ENTIRE file contents every time.

===
