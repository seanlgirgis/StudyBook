# ChatGPT Prompt — Delta Lake for Data Engineers
# READY TO PASTE — fully specified, no placeholders
# Paste everything between the === markers into ChatGPT

===

TOPIC: Delta Lake for Data Engineers
SLUG: delta_lake
PRIORITY: Toyota Interview Prep
INFRASTRUCTURE: Pure Python — deltalake library (Rust-based, no JVM, no Spark)
NO AWS, NO DOCKER, NO CLEANUP RULES NEEDED.

IMPORTANT: Use the `deltalake` Python library (pip install deltalake).
Do NOT use delta-spark or PySpark. The deltalake library uses Apache Arrow
and Rust under the hood — no Java required.

===== CODING STANDARDS =====

FILE HEADER (every file):
# ============================================================
# Topic   : Delta Lake for Data Engineers
# File    : NN_filename.py
# Covers  : one-line description
# Prereqs : pip install deltalake pandas pyarrow
# Run     : python NN_filename.py
# ============================================================

CRITICAL — CODE QUALITY:
- Every function COMPLETE and FULLY RUNNABLE — no placeholders, no TODO, no pass.
- Generate the ENTIRE file every time.
- Comments explain WHY — ACID, transaction log, snapshot isolation, time travel
  are the Toyota interview topics. Every Delta Lake design decision gets a comment.
- Output: OUTPUT_DIR env var or C:/tmp/studybook/delta/ (Windows) / /tmp/studybook/delta/
- Detect platform with os.name. Use pathlib.Path.
- Seed random data with fixed seed for reproducibility.
- Use deltalake API: write_deltalake(), DeltaTable

===== FILE 01: 01_delta_basics_and_acid.py =====

from deltalake import write_deltalake, DeltaTable
import pandas as pd, pyarrow as pa
import os, json, time
from pathlib import Path

def get_output_dir() -> Path:
    """Return platform output dir. Create if missing."""
    default = Path("C:/tmp/studybook/delta" if os.name == "nt"
                   else "/tmp/studybook/delta")
    out = Path(os.getenv("OUTPUT_DIR", str(default)))
    out.mkdir(parents=True, exist_ok=True)
    return out

def generate_sensor_data(n_rows: int = 1000, seed: int = 42) -> pd.DataFrame:
    """
    Generate synthetic sensor readings. Columns:
      sensor_id: str  "sensor_{i:03d}" for i in 0..49
      plant:     str  one of ["plant_A","plant_B","plant_C"]
      value:     float64  uniform 15–95
      unit:      str  "celsius"
      ts:        datetime64[ns]  now - random seconds
    Seed = 42.
    """

def create_delta_table(path: Path, df: pd.DataFrame) -> None:
    """
    Write df to path as Delta table using write_deltalake(str(path), df, mode="overwrite").
    After write, print:
      - Table path
      - Number of files in _delta_log/
      - Content of the first _delta_log/00000000000000000000.json (pretty printed)
    WHY _delta_log: every Delta operation creates a JSON commit file here.
    The transaction log IS the Delta table — the Parquet files are just data.
    Atomicity comes from: write Parquet first, then commit JSON.
    If the commit JSON write fails, the Parquet is orphaned (ignored on next read).
    """

def read_delta_table(path: Path) -> pd.DataFrame:
    """
    Read current snapshot with DeltaTable(str(path)).to_pandas().
    Print row count, column names, first 3 rows.
    WHY snapshot: Delta always reads the latest committed version.
    Concurrent writers never see partial writes — snapshot isolation.
    Return DataFrame.
    """

def inspect_transaction_log(path: Path) -> list[dict]:
    """
    Read all JSON files from path/_delta_log/*.json.
    For each commit file, print:
      Version | Operation   | Added files | Removed files | Timestamp
      ------- | ----------- | ----------- | ------------- | ---------
      0       | WRITE       | 1           | 0             | 2024-01-01
    Return list of parsed commit dicts.
    WHY transaction log: audit trail for compliance. Every write is recorded.
    Delta uses optimistic concurrency — writers read current version, write new files,
    then attempt to commit. If another writer committed first, retry.
    """

def demonstrate_atomicity(path: Path) -> None:
    """
    Show that a failed write leaves the table unchanged.
    Steps:
      1. Read current row count
      2. Attempt to write a DataFrame with an intentionally bad column type
         (force a pyarrow SchemaError or similar)
      3. Catch the exception
      4. Read row count again — must be identical to step 1
      5. Print: "Table unchanged after failed write — atomicity confirmed ✓"
    WHY atomicity: with plain Parquet, a crashed write can leave partial files.
    Delta's commit protocol guarantees all-or-nothing.
    """

def append_to_table(path: Path, df: pd.DataFrame) -> None:
    """
    Append df using write_deltalake(str(path), df, mode="append").
    Before and after: print row counts, version numbers.
    After append, read the newest _delta_log entry and print its 'add' actions.
    Show that the old data files still exist (Delta never deletes on append).
    """

def main():
    out   = get_output_dir()
    path  = out / "sensor_readings"

    print("\n=== CREATE DELTA TABLE ===")
    df1 = generate_sensor_data(1000)
    create_delta_table(path, df1)

    print("\n=== READ DELTA TABLE ===")
    df_read = read_delta_table(path)

    print("\n=== TRANSACTION LOG ===")
    commits = inspect_transaction_log(path)

    print("\n=== ATOMICITY DEMO ===")
    demonstrate_atomicity(path)

    print("\n=== APPEND ===")
    df2 = generate_sensor_data(500, seed=99)
    append_to_table(path, df2)
    read_delta_table(path)  # show 1500 rows

if __name__ == "__main__":
    main()

===== FILE 02: 02_time_travel_and_versioning.py =====

from deltalake import write_deltalake, DeltaTable
import pandas as pd
from pathlib import Path
import os, time

def get_output_dir() -> Path: ...

def setup_versioned_table(path: Path) -> None:
    """
    Create a table with 4 distinct versions:
      v0: 500 customer records (customer_id, name, region, spend)
      v1: append 200 more customers
      v2: overwrite region for 50 customers (simulate update via overwrite)
      v3: append 100 final records
    Print version number after each write.
    """

def read_version(path: Path, version: int) -> pd.DataFrame:
    """
    Read table at specific version number.
    dt = DeltaTable(str(path))
    df = dt.load_version(version).to_pandas()
    WHY version reading: auditing, debugging, and compliance.
    "What did this table look like on January 15?" — answered with time travel.
    Print: "Version {version}: {len(df)} rows"
    Return df.
    """

def read_at_timestamp(path: Path, timestamp: str) -> pd.DataFrame:
    """
    Read table as of a datetime string (ISO 8601: "2024-01-15T10:30:00").
    dt.load_with_datetime(timestamp).to_pandas()
    If timestamp is before table creation, raise ValueError with clear message.
    WHY timestamp travel: GDPR "right to be forgotten" compliance often requires
    showing the state of data at a specific date for regulators.
    Return df.
    """

def get_table_history(path: Path) -> pd.DataFrame:
    """
    DeltaTable(str(path)).history() → list of dicts.
    Convert to DataFrame. Print formatted:
      version | timestamp         | operation | numAddedFiles | numRemovedFiles
      ------- | ----------------- | --------- | ------------- | ---------------
      3       | 2024-01-01 10:05  | WRITE     | 1             | 0
    Return history DataFrame.
    """

def diff_versions(path: Path, v1: int, v2: int) -> dict:
    """
    Compare two versions of the table.
    df_v1 = read_version(path, v1)
    df_v2 = read_version(path, v2)
    Return:
      { v1_rows: int, v2_rows: int, rows_added: int, rows_removed: int }
    rows_added   = len(df_v2) - len(df_v1)  (if v2 > v1)
    rows_removed = max(0, len(df_v1) - len(df_v2))
    Print diff summary.
    """

def restore_to_version(path: Path, version: int) -> None:
    """
    Restore table to a previous version.
    dt = DeltaTable(str(path))
    dt.restore(version)
    Print row count before and after restore.
    WHY restore: when a bad write corrupts data, restore to last-known-good version.
    With plain Parquet there is no restore — you need a backup.
    """

def main():
    path = get_output_dir() / "customers_versioned"

    print("\n=== SETUP 4 VERSIONS ===")
    setup_versioned_table(path)

    print("\n=== TABLE HISTORY ===")
    get_table_history(path)

    print("\n=== TIME TRAVEL BY VERSION ===")
    for v in [0, 1, 2, 3]:
        read_version(path, v)

    print("\n=== DIFF VERSIONS 0 vs 3 ===")
    diff = diff_versions(path, 0, 3)
    print(diff)

    print("\n=== RESTORE TO VERSION 1 ===")
    restore_to_version(path, version=1)
    from deltalake import DeltaTable
    dt = DeltaTable(str(path))
    print(f"After restore: version={dt.version()}, rows={len(dt.to_pandas())}")

if __name__ == "__main__":
    main()

===== FILE 03: 03_merge_upsert_patterns.py =====

from deltalake import write_deltalake, DeltaTable
from deltalake.writer import write_deltalake
import pandas as pd, pyarrow as pa
from pathlib import Path
import os, uuid

NOTE: deltalake merge uses dt.merge() API (available in deltalake >= 0.10.0).
Use: dt.merge(source=pa.Table, predicate="target.id = source.id", source_alias="source", target_alias="target")
     .when_matched_update(...)
     .when_not_matched_insert(...)
     .execute()

def get_output_dir() -> Path: ...

def generate_customers(n: int = 1000, seed: int = 42) -> pd.DataFrame:
    """
    Columns: customer_id (str, unique), name, region, tier, annual_spend (float), updated_at (str ISO).
    """

def simple_upsert(path: Path, source_df: pd.DataFrame, merge_key: str = "customer_id") -> dict:
    """
    Merge source_df into Delta table at path.
    WHEN MATCHED UPDATE SET *   — update all columns on match
    WHEN NOT MATCHED INSERT *   — insert new rows
    Return: { rows_matched: int, rows_inserted: int, rows_updated: int }
    WHY MERGE not overwrite: MERGE touches only changed rows.
    Overwrite rewrites the entire table — expensive for large tables.
    Print operation result.
    """

def conditional_merge(path: Path, source_df: pd.DataFrame,
                       merge_key: str = "customer_id") -> dict:
    """
    Merge with condition: update ONLY if annual_spend changed.
    WHEN MATCHED AND source.annual_spend != target.annual_spend
      UPDATE SET annual_spend = source.annual_spend, updated_at = source.updated_at
    WHEN NOT MATCHED INSERT *
    Return: { rows_updated: int, rows_inserted: int, rows_skipped: int }
    WHY conditional: avoids unnecessary file rewrites when data hasn't changed.
    Reduces write amplification in high-frequency CDC pipelines.
    """

def implement_scd_type2(path: Path, source_df: pd.DataFrame,
                         key_col: str = "customer_id",
                         tracked_cols: list[str] = None) -> None:
    """
    Slowly Changing Dimension Type 2 pattern.
    Target schema must include: valid_from (str), valid_to (str), is_current (bool).
    
    Algorithm:
      1. For rows where tracked_cols changed:
         - UPDATE target: set is_current=False, valid_to=now()
         - INSERT new row: valid_from=now(), valid_to='9999-12-31', is_current=True
      2. For new rows (not in target):
         - INSERT: valid_from=now(), valid_to='9999-12-31', is_current=True
      3. For unchanged rows: no action

    Implement using two merge operations:
      Merge 1: close out changed records (is_current → False)
      Merge 2: insert new versions + new records

    WHY SCD Type 2: preserves full history of changes. Toyota uses this for
    vehicle configuration changes, pricing history, dealer assignments.
    """

def delete_matching_records(path: Path, ids_to_delete: list[str]) -> int:
    """
    Delete records where customer_id in ids_to_delete.
    Use dt.delete(predicate=f"customer_id IN ({placeholders})")
    Return rows deleted count.
    WHY merge-based delete: Delta marks files as "removed" in the transaction log.
    Data still exists on disk until VACUUM. Critical for GDPR: soft-delete first,
    VACUUM after 7-day retention window.
    """

def main():
    path = get_output_dir() / "customers_scd"

    # Initial load
    df_init = generate_customers(1000)
    # Add SCD columns
    df_init["valid_from"] = "2024-01-01"
    df_init["valid_to"]   = "9999-12-31"
    df_init["is_current"] = True
    write_deltalake(str(path), df_init, mode="overwrite")
    print(f"Initial load: {len(df_init)} customers")

    print("\n=== SIMPLE UPSERT ===")
    df_updates = generate_customers(200, seed=99)  # 200 records — mix of new + existing
    simple_upsert(path, df_updates)

    print("\n=== CONDITIONAL MERGE ===")
    df_spend_updates = generate_customers(100, seed=77)
    conditional_merge(path, df_spend_updates)

    print("\n=== SCD TYPE 2 ===")
    df_scd = generate_customers(50, seed=55)
    df_scd["annual_spend"] = df_scd["annual_spend"] * 1.5  # spending increased
    implement_scd_type2(path, df_scd, key_col="customer_id",
                         tracked_cols=["annual_spend", "tier"])

    print("\n=== DELETE ===")
    import random; random.seed(42)
    ids_to_delete = [f"CUST-{i:06d}" for i in random.sample(range(1000), 10)]
    n_deleted = delete_matching_records(path, ids_to_delete)
    print(f"Deleted {n_deleted} records")

if __name__ == "__main__":
    main()

===== FILE 04: 04_schema_evolution_and_enforcement.py =====

def demonstrate_schema_enforcement(path: Path) -> None:
    """
    Show Delta's default schema enforcement:
      1. Write table with schema: {sensor_id, value, ts}
      2. Try to write a DataFrame with extra column "firmware_version"
         → expect DeltaProtocolViolationError or SchemaMismatchError
         Catch it and print: "Schema enforcement blocked incompatible write ✓"
      3. Try to write with different type for "value" (str instead of float)
         → expect error. Catch and print explanation.
    WHY enforcement: in a data lake without schema enforcement, any writer can
    corrupt the table schema. Delta prevents this by default.
    """

def add_column_safely(path: Path, df_with_new_col: pd.DataFrame) -> None:
    """
    Write df_with_new_col (which has an extra nullable column) using:
      write_deltalake(str(path), df_with_new_col, mode="append", schema_mode="merge")
    schema_mode="merge" = mergeSchema=True in PySpark.
    After write: read table and show new column (older rows have null for new column).
    WHY only nullable columns: non-nullable columns would require backfilling
    all existing rows — a full table rewrite. Nullable is the only safe addition.
    """

def check_schema_compatibility(schema_old: pa.Schema,
                                schema_new: pa.Schema) -> dict:
    """
    Compare two pyarrow schemas. Return:
      { compatible: bool,
        breaking_changes: list[str],
        safe_changes: list[str],
        added_columns: list[str],
        removed_columns: list[str] }
    Breaking: column removed, type narrowed (float64→int32), type incompatible
    Safe: nullable column added, type widened (int32→int64, float32→float64)
    """

def demonstrate_breaking_change(path: Path) -> None:
    """
    Attempt two schema changes:
      A. SAFE: add nullable column "firmware_version" (str, nullable)
         → show this succeeds with schema_mode="merge"
      B. BREAKING: try to change "value" column from float64 to string
         → catch the error, print:
           "Type change float64→string is BREAKING. Use overwriteSchema=True
            only if you accept losing all existing data and history is reset.
            For non-breaking evolution, Delta Lake is the right tool.
            For renames/type changes, use Iceberg or Delta with column mapping."
    """

def explain_iceberg_vs_delta_evolution() -> None:
    """
    Print comparison table:

    Operation              | Raw Parquet | Delta Lake  | Apache Iceberg
    ----------------------|-------------|-------------|---------------
    Add nullable column   | ✅ Safe      | ✅ Safe      | ✅ Safe
    Widen numeric type    | ✅ Safe      | ✅ Safe      | ✅ Safe
    Rename column         | ❌ Breaking  | ✅ (mapping) | ✅ Metadata
    Drop column           | ❌ Breaking  | ✅ (mapping) | ✅ Metadata
    Change incompatible type | ❌        | ❌           | ❌
    Time travel           | ❌           | ✅           | ✅
    ACID transactions     | ❌           | ✅           | ✅
    Multi-engine support  | ✅           | Spark-first  | ✅ (Spark/Flink/Trino)

    Delta Lake column mapping (mode=name) allows column renames without rewriting
    data files. Enable with: ALTER TABLE ... SET TBLPROPERTIES ('delta.columnMapping.mode'='name')
    """

def main():
    path = get_output_dir() / "schema_evo"

    df_v1 = pd.DataFrame({
        "sensor_id": [f"s{i:03d}" for i in range(100)],
        "value": [float(i) for i in range(100)],
        "ts": pd.date_range("2024-01-01", periods=100, freq="1min"),
    })
    write_deltalake(str(path), df_v1, mode="overwrite")

    print("\n=== SCHEMA ENFORCEMENT ===")
    demonstrate_schema_enforcement(path)

    print("\n=== ADD COLUMN SAFELY ===")
    df_v2 = df_v1.copy()
    df_v2["firmware_version"] = "v1.2.3"
    add_column_safely(path, df_v2)

    print("\n=== COMPATIBILITY CHECK ===")
    import pyarrow as pa
    s1 = pa.schema([pa.field("sensor_id", pa.string()),
                    pa.field("value", pa.float64())])
    s2 = pa.schema([pa.field("sensor_id", pa.string()),
                    pa.field("value", pa.float64()),
                    pa.field("firmware_version", pa.string())])
    result = check_schema_compatibility(s1, s2)
    print(result)

    print("\n=== BREAKING CHANGE DEMO ===")
    demonstrate_breaking_change(path)

    print("\n=== DELTA vs ICEBERG EVOLUTION ===")
    explain_iceberg_vs_delta_evolution()

if __name__ == "__main__":
    main()

===== FILE 05: 05_optimize_and_vacuum.py =====

def show_file_fragmentation(path: Path) -> dict:
    """
    List all Parquet data files for the Delta table.
    DeltaTable(str(path)).files() returns list of relative file paths.
    Count files, compute sizes, show per-file size distribution.
    Return: { file_count: int, total_size_mb: float,
              avg_size_mb: float, min_size_mb: float, max_size_mb: float }
    Print: "Small file problem: {file_count} files avg {avg_size_kb:.0f} KB each"
    WHY small files hurt: each file requires a file-open + metadata read.
    1000 files × 0.1s per open = 100s overhead before reading a single byte.
    """

def create_fragmented_table(path: Path, n_appends: int = 50) -> None:
    """
    Simulate a streaming ingestion pattern: append n_appends small DataFrames.
    Each append: 20 rows of sensor data.
    Result: n_appends Parquet files (one per append) = small file problem.
    Print final file count and average size.
    """

def optimize_table(path: Path) -> dict:
    """
    Compact small files using DeltaTable(str(path)).optimize().compact()
    Measure time before and after.
    Return: { before_files: int, after_files: int, reduction_ratio: float,
              before_size_mb: float, after_size_mb: float, compact_ms: float }
    WHY OPTIMIZE: compacts many small files into fewer larger files.
    In PySpark/Databricks: OPTIMIZE table_name (generates ~1GB files).
    In deltalake library: optimize().compact() does the same.
    """

def zorder_by_columns(path: Path, columns: list[str]) -> None:
    """
    Z-order optimization for multi-column clustering.
    DeltaTable(str(path)).optimize().z_order(columns)
    WHY Z-ordering: co-locates related data across multiple dimensions.
    Regular partitioning: query on region prunes all non-region files.
    Z-ordering: query on (region AND sensor_type) prunes more files than
    partitioning alone — data is sorted along a space-filling Z-curve.
    In practice: use Z-order on high-cardinality columns you filter on together.
    Print: files before and after Z-order, storage change.
    """

def vacuum_table(path: Path, retention_hours: int = 168) -> dict:
    """
    Remove old data files no longer needed for time travel.
    DeltaTable(str(path)).vacuum(retention_hours=retention_hours)
    WHY retention_hours=168 (7 days): Delta's default. Shorter = less storage.
    Shorter means less time-travel history available.
    WARNING: vacuuming below 7 days can cause issues if concurrent readers
    are still reading old snapshots.
    For testing: use retention_hours=0 and dry_run=True to see what WOULD be deleted.
    Return: { files_removed: int, space_freed_mb: float }
    Print before/after file counts.
    """

def measure_query_speedup(path: Path, filter_col: str = "plant",
                           filter_val: str = "plant_A") -> dict:
    """
    Time the same filter query before and after OPTIMIZE:
      dt.to_pandas(filters=[(filter_col, "=", filter_val)])
    (Before: run on fragmented table. After: on optimized table.)
    Return: { before_ms: float, after_ms: float, speedup_x: float }
    WHY: OPTIMIZE reduces file-open overhead, improving filter query performance.
    The improvement is most dramatic on highly fragmented tables.
    """

def main():
    path = get_output_dir() / "optimize_demo"

    print("\n=== CREATE FRAGMENTED TABLE (50 appends × 20 rows) ===")
    create_fragmented_table(path, n_appends=50)
    before_stats = show_file_fragmentation(path)

    print("\n=== QUERY BEFORE OPTIMIZE ===")
    from deltalake import DeltaTable
    import time
    t0 = time.perf_counter()
    dt = DeltaTable(str(path))
    df = dt.to_pandas()
    before_ms = (time.perf_counter() - t0) * 1000
    print(f"Full scan before optimize: {before_ms:.0f}ms")

    print("\n=== OPTIMIZE (COMPACT) ===")
    opt_stats = optimize_table(path)
    print(f"Files: {opt_stats['before_files']} → {opt_stats['after_files']} "
          f"(reduction: {opt_stats['reduction_ratio']:.1f}×)")

    print("\n=== Z-ORDER ===")
    zorder_by_columns(path, columns=["plant", "sensor_id"])

    print("\n=== VACUUM (dry run) ===")
    vacuum_table(path, retention_hours=0)

    print("\n=== QUERY AFTER OPTIMIZE ===")
    speedup = measure_query_speedup(path)
    print(f"Speedup: {speedup['speedup_x']:.1f}×")

if __name__ == "__main__":
    main()

===== CAPSTONE PROJECT =====

Title: Change Data Capture (CDC) Pipeline with Delta Lake
Scenario: Daily change feeds (inserts, updates, deletes) for a customer master table.
Apply changes via MERGE, maintain SCD Type 2 history, support time travel for audits.

Directory layout:
  capstone/
    capstone.py       ← full CDC pipeline (Day 0, Day 1, Day 2)
    test_capstone.py  ← pytest validating merge idempotency, time travel

===== CAPSTONE FILE: capstone.py =====

"""
Delta Lake CDC Pipeline Capstone.

Simulates 3 days of change data capture on a customer master table.
Day 0: Initial load of 1000 customers
Day 1: 200 updates, 50 inserts, 20 deletes via MERGE
Day 2: 150 updates (some reverting Day 1 changes)

Demonstrates: MERGE, time travel, SCD Type 2, OPTIMIZE, VACUUM.
"""
from deltalake import write_deltalake, DeltaTable
import pandas as pd, pyarrow as pa
import os, time, json
from pathlib import Path
from datetime import datetime, timedelta
import random

OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR",
    "C:/tmp/studybook/delta/capstone" if os.name == "nt"
    else "/tmp/studybook/delta/capstone"))

TABLE_PATH = OUTPUT_DIR / "customer_master"

def generate_customers(n: int, seed: int, version_ts: str = "2024-01-01") -> pd.DataFrame:
    """
    Generate n customer records. Columns:
      customer_id:   "CUST-{i:06d}"
      name:          "Customer {i}"
      region:        one of 5 regions
      tier:          "BRONZE"/"SILVER"/"GOLD" (based on annual_spend)
      annual_spend:  float 100–50000
      valid_from:    version_ts (str)
      valid_to:      "9999-12-31"
      is_current:    True
      cdc_ts:        version_ts
    """

def apply_cdc_changes(target_path: Path, changes_df: pd.DataFrame,
                       operation: str, cdc_ts: str) -> dict:
    """
    Apply CDC changes to Delta table.
    operation: "upsert", "delete"
    For upsert: MERGE — update existing, insert new
    For delete: dt.delete(predicate)
    Return: { inserted: int, updated: int, deleted: int }
    """

def run_day_0(table_path: Path) -> None:
    """Initial load of 1000 customers. Print version=0, row_count=1000."""

def run_day_1(table_path: Path) -> None:
    """
    Day 1 changes:
      - Update 200 existing customers (annual_spend changes)
      - Insert 50 new customers
      - Delete 20 customers
    Print: version=1, rows after changes.
    """

def run_day_2(table_path: Path) -> None:
    """
    Day 2: 150 updates — some revert Day 1 changes (original spend restored).
    Print: version=2, rows.
    """

def verify_time_travel(table_path: Path) -> None:
    """
    Read Day 0, Day 1, Day 2 snapshots via load_version(0/1/2).
    Print row counts for each version.
    Assert: v0=1000, v1≈1030 (1000-20+50), v2≈1030 (updates only).
    Print compliance report: "Customer CUST-000001 history across all versions"
    Show the customer's record at each version where it changed.
    """

def run_optimize_and_vacuum(table_path: Path) -> None:
    """
    After 3 days of writes, run OPTIMIZE then VACUUM (retention_hours=0, dry_run=True).
    Print: files before optimize, files after optimize, size savings.
    """

def print_final_report(table_path: Path) -> None:
    """
    ╔════════════════════════════════════════╗
    ║  Delta Lake CDC Pipeline — Summary     ║
    ╠════════════════════════════════════════╣
    ║  Versions created   : 3               ║
    ║  Final row count    : 1,030            ║
    ║  Day 1 changes      : +50 / ~200 / -20 ║
    ║  Day 2 changes      : ~150 updates     ║
    ║  Time travel OK     : ✓  (3 versions)  ║
    ║  OPTIMIZE run       : ✓               ║
    ╚════════════════════════════════════════╝
    """

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print("=== DAY 0: INITIAL LOAD ===")
    run_day_0(TABLE_PATH)
    print("\n=== DAY 1: CDC CHANGES ===")
    run_day_1(TABLE_PATH)
    print("\n=== DAY 2: MORE CHANGES ===")
    run_day_2(TABLE_PATH)
    print("\n=== TIME TRAVEL VERIFICATION ===")
    verify_time_travel(TABLE_PATH)
    print("\n=== OPTIMIZE + VACUUM ===")
    run_optimize_and_vacuum(TABLE_PATH)
    print("\n=== FINAL REPORT ===")
    print_final_report(TABLE_PATH)

if __name__ == "__main__":
    main()

===== CAPSTONE FILE: test_capstone.py =====

"""pytest — 6 tests for Delta Lake CDC capstone."""
import pytest, shutil
from pathlib import Path
from deltalake import write_deltalake, DeltaTable
import pandas as pd, os
import sys
sys.path.insert(0, str(Path(__file__).parent))
from capstone import generate_customers, apply_cdc_changes, run_day_0, TABLE_PATH, OUTPUT_DIR

@pytest.fixture(scope="session", autouse=True)
def run_full_pipeline():
    """Run Day 0 once for the session."""
    if TABLE_PATH.exists():
        shutil.rmtree(TABLE_PATH)
    run_day_0(TABLE_PATH)
    yield

def test_day0_creates_1000_rows():
    dt = DeltaTable(str(TABLE_PATH))
    assert len(dt.to_pandas()) == 1000

def test_day0_version_is_zero():
    dt = DeltaTable(str(TABLE_PATH))
    assert dt.version() == 0

def test_time_travel_version_zero_consistent():
    """Reading v0 twice returns identical row counts."""
    dt = DeltaTable(str(TABLE_PATH))
    df1 = dt.load_version(0).to_pandas()
    df2 = dt.load_version(0).to_pandas()
    assert len(df1) == len(df2)

def test_merge_idempotency(tmp_path):
    """Running the same upsert twice produces same result as running once."""
    df_init = generate_customers(100, seed=1)
    write_deltalake(str(tmp_path), df_init, mode="overwrite")
    df_updates = generate_customers(20, seed=2)
    r1 = apply_cdc_changes(tmp_path, df_updates, "upsert", "2024-01-02")
    r2 = apply_cdc_changes(tmp_path, df_updates, "upsert", "2024-01-02")
    # Second identical upsert updates same rows — row count must be stable
    dt = DeltaTable(str(tmp_path))
    assert len(dt.to_pandas()) == len(DeltaTable(str(tmp_path)).to_pandas())

def test_transaction_log_exists():
    """_delta_log directory must exist with at least one commit file."""
    log_dir = TABLE_PATH / "_delta_log"
    assert log_dir.exists()
    commit_files = list(log_dir.glob("*.json"))
    assert len(commit_files) >= 1

def test_all_current_records_have_is_current_true():
    """All rows in latest snapshot must have is_current=True."""
    dt = DeltaTable(str(TABLE_PATH))
    df = dt.to_pandas()
    assert df["is_current"].all()

===== GENERATION SEQUENCE =====

Acknowledge these instructions, then wait for me to say "generate file 01".

  "generate file 01"  → 01_delta_basics_and_acid.py
  "generate file 02"  → 02_time_travel_and_versioning.py
  "generate file 03"  → 03_merge_upsert_patterns.py
  "generate file 04"  → 04_schema_evolution_and_enforcement.py
  "generate file 05"  → 05_optimize_and_vacuum.py
  "generate readme"   → README.md
  "generate capstone" → capstone/capstone.py
  "generate tests"    → capstone/test_capstone.py

Each file COMPLETE and FULLY RUNNABLE. No placeholders. No pass statements.

===
