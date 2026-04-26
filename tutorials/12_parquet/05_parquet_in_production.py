# ============================================================
# Topic   : Parquet for Data Engineers
# File    : 05_parquet_in_production.py
# Covers  : Production Parquet patterns, file sizing, compaction, DuckDB queries
# Prereqs : pip install pyarrow pandas duckdb
# Run     : python 05_parquet_in_production.py
# ============================================================

from __future__ import annotations

import os
import shutil
import time
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


def get_output_dir() -> Path:
    """Return OUTPUT_DIR from env or platform-specific default. Create if missing."""
    default = Path("C:/tmp/studybook/parquet/") if os.name == "nt" else Path("/tmp/studybook/parquet/")
    output_dir = Path(os.getenv("OUTPUT_DIR", str(default)))
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def optimize_file_count(
    total_rows: int,
    target_file_size_mb: int = 128,
    avg_row_size_bytes: int = 200,
) -> dict:
    """
    Calculate optimal number of files and rows per file.
    Return:
      { total_rows, avg_row_size_bytes, target_file_size_mb,
        rows_per_file: int, num_files: int,
        actual_file_size_mb: float }
    Print explanation: "Target 128MB–512MB per Parquet file. Too small → metadata overhead.
    Too large → slow partial reads and imbalanced parallelism."
    """
    target_bytes = target_file_size_mb * 1_000_000
    rows_per_file = max(1, target_bytes // avg_row_size_bytes)
    num_files = int(np.ceil(total_rows / rows_per_file))
    actual_file_size_mb = (rows_per_file * avg_row_size_bytes) / 1_000_000

    result = {
        "total_rows": total_rows,
        "avg_row_size_bytes": avg_row_size_bytes,
        "target_file_size_mb": target_file_size_mb,
        "rows_per_file": int(rows_per_file),
        "num_files": num_files,
        "actual_file_size_mb": actual_file_size_mb,
    }

    print(f"Total rows:           {total_rows:,}")
    print(f"Average row size:     {avg_row_size_bytes:,} bytes")
    print(f"Target file size:     {target_file_size_mb} MB")
    print(f"Rows per file:        {rows_per_file:,}")
    print(f"Recommended files:    {num_files:,}")
    print(f"Actual file size est: {actual_file_size_mb:.1f} MB")
    print(
        "\nTarget 128MB–512MB per Parquet file. Too small → metadata overhead "
        "and slow planning. Too large → slow partial reads and imbalanced parallelism."
    )

    return result


def write_chunked(df: pd.DataFrame, output_dir: Path, chunk_size: int) -> list[str]:
    """
    Split df into chunks of chunk_size rows. Write each chunk as a separate
    Parquet file: part-{i:04d}.parquet with SNAPPY compression.
    Return list of written file paths.
    Print: files written, average file size.
    """
    if output_dir.exists():
        for existing_file in output_dir.glob("*.parquet"):
            existing_file.unlink()
    output_dir.mkdir(parents=True, exist_ok=True)

    written: list[str] = []

    for i, start in enumerate(range(0, len(df), chunk_size)):
        chunk = df.iloc[start : start + chunk_size]
        path = output_dir / f"part-{i:04d}.parquet"
        table = pa.Table.from_pandas(chunk, preserve_index=False)
        pq.write_table(table, path, compression="SNAPPY")
        written.append(str(path))

    sizes = [Path(p).stat().st_size for p in written]
    avg_size_mb = np.mean(sizes) / 1_000_000 if sizes else 0.0

    print(f"Files written:     {len(written)}")
    print(f"Average file size: {avg_size_mb:.2f} MB")

    return written


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
    files = sorted(
        f for f in dataset_path.glob("*.parquet")
        if "compacted" not in f.parts
    )

    if not files:
        raise FileNotFoundError(f"No Parquet files found in {dataset_path}")

    before_file_count = len(files)
    before_total_size_bytes = sum(f.stat().st_size for f in files)

    dfs = [pd.read_parquet(f) for f in files]
    df = pd.concat(dfs, ignore_index=True)
    total_rows = len(df)

    avg_row_size_bytes = before_total_size_bytes / total_rows
    target_bytes = target_size_mb * 1_000_000
    rows_per_file = max(1, int(target_bytes // avg_row_size_bytes))

    compacted_dir = dataset_path / "compacted"
    if compacted_dir.exists():
        shutil.rmtree(compacted_dir)

    written = write_chunked(df, compacted_dir, rows_per_file)

    after_file_count = len(written)
    after_total_size_bytes = sum(Path(p).stat().st_size for p in written)
    compacted_rows = sum(pq.read_metadata(p).num_rows for p in written)

    result = {
        "before_file_count": before_file_count,
        "after_file_count": after_file_count,
        "before_total_size_mb": before_total_size_bytes / 1_000_000,
        "after_total_size_mb": after_total_size_bytes / 1_000_000,
        "total_rows": total_rows,
        "rows_preserved": compacted_rows == total_rows,
    }

    print("\nCompaction summary:")
    print(f"Before: {before_file_count} files | {before_total_size_bytes / 1_000_000:.2f} MB")
    print(f"After:  {after_file_count} files | {after_total_size_bytes / 1_000_000:.2f} MB")
    print(f"Rows preserved: {result['rows_preserved']} ({total_rows:,} rows)")
    print(
        "Why this matters: query engines pay overhead per file. Compaction reduces "
        "metadata reads, file opens, and planning time."
    )

    return result


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
    pandas_times = []
    pyarrow_times = []

    for _ in range(3):
        start = time.perf_counter()
        _ = pd.read_parquet(path)
        pandas_times.append((time.perf_counter() - start) * 1000)

    for _ in range(3):
        start = time.perf_counter()
        _ = pq.read_table(path).to_pandas()
        pyarrow_times.append((time.perf_counter() - start) * 1000)

    pandas_median_ms = float(np.median(pandas_times))
    pyarrow_median_ms = float(np.median(pyarrow_times))

    if pandas_median_ms <= pyarrow_median_ms:
        faster = "pandas"
        speedup_pct = ((pyarrow_median_ms - pandas_median_ms) / pyarrow_median_ms) * 100
    else:
        faster = "pyarrow"
        speedup_pct = ((pandas_median_ms - pyarrow_median_ms) / pandas_median_ms) * 100

    result = {
        "pandas_median_ms": pandas_median_ms,
        "pyarrow_median_ms": pyarrow_median_ms,
        "faster": faster,
        "speedup_pct": speedup_pct,
    }

    print(f"pandas median read:  {pandas_median_ms:.0f} ms")
    print(f"pyarrow median read: {pyarrow_median_ms:.0f} ms")
    print(f"Faster: {faster} by {speedup_pct:.1f}%")
    print("Note: differences matter most on large files and repeated production scans.")

    return result


def show_spark_parquet_config() -> None:
    """
    Print recommended Spark configuration for Parquet.
    """
    configs = [
        (
            "spark.sql.parquet.compression.codec",
            "zstd",
            "Use ZSTD for strong analytics compression with good read speed.",
        ),
        (
            "spark.sql.parquet.filterPushdown",
            "true",
            "Enable predicate pushdown so Spark can skip row groups using Parquet stats.",
        ),
        (
            "spark.sql.parquet.mergeSchema",
            "false",
            "Schema merging is expensive; enable only for controlled evolution reads.",
        ),
        (
            "spark.sql.files.maxPartitionBytes",
            "134217728",
            "Target 128MB input splits for balanced parallelism.",
        ),
        (
            "spark.sql.parquet.columnarReaderBatchSize",
            "4096",
            "Read batches column-wise to improve vectorized execution efficiency.",
        ),
        (
            "parquet.block.size",
            "134217728",
            "Use 128MB row groups; row groups are the unit of predicate pushdown.",
        ),
        (
            "parquet.page.size",
            "1048576",
            "Use 1MB pages for efficient compression and page-level reads.",
        ),
    ]

    print("Recommended Spark Parquet configuration:\n")
    for key, value, explanation in configs:
        print(f"{key} = {value}")
        print(f"  → {explanation}")


def simulate_athena_query(dataset_path: Path, sql: str, label: str = "") -> dict:
    """
    Use duckdb.connect() to run SQL on local Parquet files.
    Return: { label: str, rows: int, duration_ms: float, preview: str }
    where preview is the first 3 rows as a string.
    Print query label, duration, row count.
    """
    _ = dataset_path
    con = duckdb.connect()

    try:
        start = time.perf_counter()
        df = con.execute(sql).fetchdf()
        duration_ms = (time.perf_counter() - start) * 1000
    finally:
        con.close()

    preview = df.head(3).to_string(index=False)

    result = {
        "label": label,
        "rows": len(df),
        "duration_ms": duration_ms,
        "preview": preview,
    }

    print(f"{label or 'DuckDB query'}: {duration_ms:.0f} ms | {len(df):,} rows")
    print(preview)

    return result


def main() -> None:
    out = get_output_dir()

    print("\n=== FILE SIZING CALCULATOR ===")
    calc = optimize_file_count(total_rows=10_000_000, avg_row_size_bytes=150)
    print(calc)

    print("\n=== WRITE 100 SMALL FILES ===")
    np.random.seed(42)
    df = pd.DataFrame(
        {
            "device_id": [f"d{i:04d}" for i in np.random.randint(0, 100, 500_000)],
            "value": np.random.rand(500_000),
            "ts": pd.date_range("2024-01-01", periods=500_000, freq="1min"),
        }
    )

    small_dir = out / "small_files"
    small_dir.mkdir(parents=True, exist_ok=True)
    write_chunked(df, small_dir, chunk_size=5_000)

    print("\n=== COMPACT SMALL FILES ===")
    compact_stats = compact_small_files(small_dir, target_size_mb=128)
    print(compact_stats)

    print("\n=== PYARROW vs PANDAS BENCHMARK ===")
    sample_path = str(out / "ecommerce_events.parquet")
    if Path(sample_path).exists():
        bm = benchmark_pyarrow_vs_pandas(sample_path)
        print(bm)
    else:
        print("Run file 01 first to create ecommerce_events.parquet")

    print("\n=== SPARK PARQUET CONFIG ===")
    show_spark_parquet_config()

    print("\n=== DUCKDB / ATHENA SIMULATION ===")
    part_dir = out / "iot_partitioned"
    if part_dir.exists():
        glob = str(part_dir / "**" / "*.parquet").replace("\\", "/")

        simulate_athena_query(
            part_dir,
            sql=(
                f"SELECT plant_id, COUNT(*) AS cnt "
                f"FROM read_parquet('{glob}', hive_partitioning=true) "
                f"GROUP BY plant_id "
                f"ORDER BY plant_id"
            ),
            label="Row count per plant",
        )

        simulate_athena_query(
            part_dir,
            sql=(
                f"SELECT sensor_type, AVG(value) AS avg_val "
                f"FROM read_parquet('{glob}', hive_partitioning=true) "
                f"WHERE plant_id='plant_A' "
                f"GROUP BY sensor_type "
                f"ORDER BY sensor_type"
            ),
            label="Avg value per sensor type (plant_A)",
        )
    else:
        print("Run file 03 first to create partitioned dataset")


if __name__ == "__main__":
    main()