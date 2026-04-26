# ============================================================
# Topic   : Parquet for Data Engineers
# File    : 06_parquet_capstone_pipeline.py
# Covers  : End-to-end Parquet storage layer: ingest, optimize, partition, compact, query
# Prereqs : pip install pyarrow pandas duckdb
# Run     : python 06_parquet_capstone_pipeline.py
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
import pyarrow.dataset as ds
import pyarrow.parquet as pq


def get_output_dir() -> Path:
    """Return OUTPUT_DIR from env or platform-specific default. Create if missing."""
    default = Path("C:/tmp/studybook/parquet/") if os.name == "nt" else Path("/tmp/studybook/parquet/")
    output_dir = Path(os.getenv("OUTPUT_DIR", str(default)))
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def fresh_dir(path: Path) -> None:
    """Delete and recreate a directory so benchmark results are clean."""
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def generate_iot_dataset(rows: int = 1_000_000) -> pd.DataFrame:
    """
    Generate a realistic IoT dataset for a production-style Parquet capstone.
    """
    np.random.seed(42)

    devices = np.array([f"device_{i:04d}" for i in range(500)])
    plants = np.array(["plant_A", "plant_B", "plant_C"])
    sensor_types = np.array(["temperature", "pressure", "vibration", "humidity"])

    sensor_type = np.random.choice(sensor_types, size=rows)

    value = np.empty(rows, dtype="float64")
    value[sensor_type == "temperature"] = np.random.uniform(15, 95, size=(sensor_type == "temperature").sum())
    value[sensor_type == "pressure"] = np.random.uniform(1, 10, size=(sensor_type == "pressure").sum())
    value[sensor_type == "vibration"] = np.random.uniform(0, 50, size=(sensor_type == "vibration").sum())
    value[sensor_type == "humidity"] = np.random.uniform(20, 100, size=(sensor_type == "humidity").sum())

    unit_map = {
        "temperature": "C",
        "pressure": "bar",
        "vibration": "mm/s",
        "humidity": "%",
    }

    now = pd.Timestamp.now().floor("s")
    random_seconds = np.random.randint(0, 30 * 24 * 60 * 60, size=rows)
    ts = now - pd.to_timedelta(random_seconds, unit="s")

    df = pd.DataFrame(
        {
            "device_id": np.random.choice(devices, size=rows),
            "plant_id": np.random.choice(plants, size=rows, p=[0.34, 0.33, 0.33]),
            "sensor_type": sensor_type,
            "value": np.round(value, 3),
            "unit": [unit_map[s] for s in sensor_type],
            "ts": ts,
        }
    )

    thresholds = df.groupby("sensor_type")["value"].transform(lambda s: s.quantile(0.98))
    df["anomaly_flag"] = df["value"] >= thresholds
    df["year"] = df["ts"].dt.year.astype("int32")
    df["month"] = df["ts"].dt.month.astype("int32")
    df["day"] = df["ts"].dt.day.astype("int32")

    return df


def write_raw_csv_and_parquet(df: pd.DataFrame, raw_dir: Path) -> dict:
    """Write raw CSV and raw SNAPPY Parquet baseline."""
    fresh_dir(raw_dir)

    csv_path = raw_dir / "iot_raw.csv"
    parquet_path = raw_dir / "iot_raw_snappy.parquet"

    start = time.perf_counter()
    df.to_csv(csv_path, index=False)
    csv_write_ms = (time.perf_counter() - start) * 1000

    start = time.perf_counter()
    pq.write_table(pa.Table.from_pandas(df, preserve_index=False), parquet_path, compression="SNAPPY")
    parquet_write_ms = (time.perf_counter() - start) * 1000

    stats = {
        "csv_path": str(csv_path),
        "parquet_path": str(parquet_path),
        "csv_size_mb": csv_path.stat().st_size / 1_000_000,
        "parquet_size_mb": parquet_path.stat().st_size / 1_000_000,
        "csv_write_ms": csv_write_ms,
        "parquet_write_ms": parquet_write_ms,
    }

    print(f"Raw CSV:          {stats['csv_size_mb']:.2f} MB | {csv_write_ms:.0f} ms")
    print(f"Raw Parquet:      {stats['parquet_size_mb']:.2f} MB | {parquet_write_ms:.0f} ms")
    print(f"CSV is {stats['csv_size_mb'] / stats['parquet_size_mb']:.1f}× larger than SNAPPY Parquet.")

    return stats


def write_optimized_partitioned(df: pd.DataFrame, output_dir: Path) -> dict:
    """
    Write optimized ZSTD Parquet using Hive partitioning.
    Partition columns: plant_id/year/month
    """
    fresh_dir(output_dir)

    table = pa.Table.from_pandas(df, preserve_index=False)

    start = time.perf_counter()
    ds.write_dataset(
        table,
        base_dir=output_dir,
        format="parquet",
        partitioning=["plant_id", "year", "month"],
        partitioning_flavor="hive",
        max_rows_per_file=250_000,
        max_rows_per_group=100_000,
        existing_data_behavior="overwrite_or_ignore",
        file_options=ds.ParquetFileFormat().make_write_options(compression="ZSTD"),
    )
    write_ms = (time.perf_counter() - start) * 1000

    files = list(output_dir.rglob("*.parquet"))
    total_size = sum(f.stat().st_size for f in files)

    stats = {
        "path": str(output_dir),
        "file_count": len(files),
        "total_size_mb": total_size / 1_000_000,
        "write_ms": write_ms,
    }

    print(f"Optimized partitioned ZSTD: {stats['total_size_mb']:.2f} MB")
    print(f"Files written:              {stats['file_count']}")
    print(f"Write time:                 {write_ms:.0f} ms")
    print("Layout: plant_id=<plant>/year=<year>/month=<month>/part-*.parquet")

    return stats


def write_small_files(df: pd.DataFrame, small_dir: Path, rows_per_file: int = 5_000) -> dict:
    """Simulate streaming writes that create many tiny Parquet files."""
    fresh_dir(small_dir)

    start = time.perf_counter()
    files = []

    for i, offset in enumerate(range(0, len(df), rows_per_file)):
        chunk = df.iloc[offset : offset + rows_per_file]
        path = small_dir / f"part-{i:04d}.parquet"
        pq.write_table(pa.Table.from_pandas(chunk, preserve_index=False), path, compression="SNAPPY")
        files.append(path)

    duration_ms = (time.perf_counter() - start) * 1000
    total_size = sum(f.stat().st_size for f in files)

    stats = {
        "file_count": len(files),
        "total_size_mb": total_size / 1_000_000,
        "avg_file_size_kb": (total_size / len(files)) / 1_000 if files else 0,
        "write_ms": duration_ms,
    }

    print(f"Small files written: {stats['file_count']}")
    print(f"Total size:          {stats['total_size_mb']:.2f} MB")
    print(f"Avg file size:       {stats['avg_file_size_kb']:.1f} KB")
    print("This is the classic small-file problem: too many file opens and metadata reads.")

    return stats


def compact_small_files(small_dir: Path, compacted_dir: Path, target_size_mb: int = 128) -> dict:
    """Compact many small files into fewer larger Parquet files."""
    fresh_dir(compacted_dir)

    files = sorted(small_dir.glob("*.parquet"))
    if not files:
        raise FileNotFoundError(f"No small files found in {small_dir}")

    before_size = sum(f.stat().st_size for f in files)
    before_rows = sum(pq.read_metadata(f).num_rows for f in files)

    df = pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)

    avg_row_bytes = before_size / before_rows
    rows_per_file = max(1, int((target_size_mb * 1_000_000) // avg_row_bytes))

    written = []
    for i, offset in enumerate(range(0, len(df), rows_per_file)):
        chunk = df.iloc[offset : offset + rows_per_file]
        path = compacted_dir / f"part-{i:04d}.parquet"
        pq.write_table(pa.Table.from_pandas(chunk, preserve_index=False), path, compression="SNAPPY")
        written.append(path)

    after_size = sum(f.stat().st_size for f in written)
    after_rows = sum(pq.read_metadata(f).num_rows for f in written)

    stats = {
        "before_file_count": len(files),
        "after_file_count": len(written),
        "before_size_mb": before_size / 1_000_000,
        "after_size_mb": after_size / 1_000_000,
        "rows_preserved": before_rows == after_rows,
    }

    print(f"Before: {stats['before_file_count']} files | {stats['before_size_mb']:.2f} MB")
    print(f"After:  {stats['after_file_count']} files | {stats['after_size_mb']:.2f} MB")
    print(f"Rows preserved: {stats['rows_preserved']}")
    print(f"File count reduction: {stats['before_file_count'] / stats['after_file_count']:.1f}×")

    return stats


def run_duckdb_query(sql: str, label: str) -> dict:
    """Run a DuckDB SQL query and return timing + preview."""
    con = duckdb.connect()

    try:
        start = time.perf_counter()
        df = con.execute(sql).fetchdf()
        duration_ms = (time.perf_counter() - start) * 1000
    finally:
        con.close()

    print(f"\n{label}")
    print(f"Rows returned: {len(df):,}")
    print(f"Duration:      {duration_ms:.0f} ms")
    print(df.head(5).to_string(index=False))

    return {
        "label": label,
        "rows": len(df),
        "duration_ms": duration_ms,
        "preview": df.head(5).to_string(index=False),
    }


def benchmark_queries(partitioned_dir: Path, baseline_path: Path) -> None:
    """Run DuckDB queries simulating Athena-style analytics."""
    partitioned_glob = str(partitioned_dir / "**" / "*.parquet").replace("\\", "/")
    baseline = str(baseline_path).replace("\\", "/")

    run_duckdb_query(
        sql=(
            f"SELECT plant_id, COUNT(*) AS cnt "
            f"FROM read_parquet('{partitioned_glob}', hive_partitioning=true) "
            f"GROUP BY plant_id "
            f"ORDER BY plant_id"
        ),
        label="QUERY 1 — Row count by plant on partitioned dataset",
    )

    run_duckdb_query(
        sql=(
            f"SELECT sensor_type, AVG(value) AS avg_value, COUNT(*) AS readings "
            f"FROM read_parquet('{partitioned_glob}', hive_partitioning=true) "
            f"WHERE plant_id='plant_A' "
            f"GROUP BY sensor_type "
            f"ORDER BY sensor_type"
        ),
        label="QUERY 2 — Partition-pruned plant_A aggregation",
    )

    start = time.perf_counter()
    con = duckdb.connect()
    try:
        part_df = con.execute(
            f"""
            SELECT sensor_type, AVG(value) AS avg_value
            FROM read_parquet('{partitioned_glob}', hive_partitioning=true)
            WHERE plant_id='plant_A'
            GROUP BY sensor_type
            """
        ).fetchdf()
        part_ms = (time.perf_counter() - start) * 1000

        start = time.perf_counter()
        base_df = con.execute(
            f"""
            SELECT sensor_type, AVG(value) AS avg_value
            FROM read_parquet('{baseline}')
            WHERE plant_id='plant_A'
            GROUP BY sensor_type
            """
        ).fetchdf()
        base_ms = (time.perf_counter() - start) * 1000
    finally:
        con.close()

    print("\nQUERY 3 — Partitioned ZSTD vs single-file SNAPPY baseline")
    print(f"Partitioned ZSTD: {part_ms:.0f} ms | rows={len(part_df)}")
    print(f"SNAPPY baseline:  {base_ms:.0f} ms | rows={len(base_df)}")
    print(f"Speedup:          {base_ms / part_ms:.1f}×" if part_ms > 0 else "Speedup: inf")
    print("In S3/Athena, partition pruning matters even more because skipped files are never transferred.")


def inspect_capstone_metadata(partitioned_dir: Path) -> None:
    """Inspect one Parquet file to show compression, row groups, and stats."""
    files = sorted(partitioned_dir.rglob("*.parquet"))
    if not files:
        print("No optimized files found for metadata inspection.")
        return

    sample = files[0]
    parquet_file = pq.ParquetFile(sample)
    metadata = parquet_file.metadata

    print(f"Sample file: {sample}")
    print(f"Rows:        {metadata.num_rows:,}")
    print(f"Row groups:  {metadata.num_row_groups}")

    row_group = metadata.row_group(0)
    print("\nColumn metadata from row group 0:")
    for i in range(row_group.num_columns):
        column = row_group.column(i)
        stats = column.statistics
        print(
            f"  {column.path_in_schema:<15} "
            f"compression={column.compression:<8} "
            f"bytes={column.total_compressed_size:>10,} "
            f"stats={stats is not None}"
        )


def main() -> None:
    out = get_output_dir()
    capstone = out / "capstone_single_file"

    raw_dir = capstone / "raw"
    partitioned_dir = capstone / "partitioned_zstd"
    small_dir = capstone / "small_files"
    compacted_dir = capstone / "compacted"

    print("\n=== CAPSTONE: HIGH-PERFORMANCE ANALYTICS STORAGE LAYER ===")
    print("Scenario: IoT fleet generates sensor readings. Build an optimized Parquet layer.")

    print("\n=== 1. GENERATE RAW DATA ===")
    df = generate_iot_dataset(rows=1_000_000)
    print(f"Generated rows: {len(df):,}")
    print(df.head(3).to_string(index=False))

    print("\n=== 2. WRITE RAW CSV + BASELINE PARQUET ===")
    raw_stats = write_raw_csv_and_parquet(df, raw_dir)

    print("\n=== 3. WRITE OPTIMIZED PARTITIONED ZSTD DATASET ===")
    optimized_stats = write_optimized_partitioned(df, partitioned_dir)

    print("\n=== 4. STORAGE COMPARISON ===")
    print("Format                  | Files | Size MB | vs CSV")
    print("------------------------|-------|---------|-------")
    print(f"Raw CSV                 |     1 | {raw_stats['csv_size_mb']:7.2f} | 1.0×")
    print(
        f"SNAPPY single baseline  |     1 | {raw_stats['parquet_size_mb']:7.2f} | "
        f"{raw_stats['csv_size_mb'] / raw_stats['parquet_size_mb']:.1f}×"
    )
    print(
        f"ZSTD partitioned        | {optimized_stats['file_count']:5d} | "
        f"{optimized_stats['total_size_mb']:7.2f} | "
        f"{raw_stats['csv_size_mb'] / optimized_stats['total_size_mb']:.1f}×"
    )

    print("\n=== 5. METADATA INSPECTION ===")
    inspect_capstone_metadata(partitioned_dir)

    print("\n=== 6. SIMULATE SMALL FILE PROBLEM ===")
    small_stats = write_small_files(df, small_dir, rows_per_file=5_000)

    print("\n=== 7. COMPACT SMALL FILES ===")
    compact_stats = compact_small_files(small_dir, compacted_dir, target_size_mb=128)

    print("\n=== 8. DUCKDB / ATHENA-STYLE QUERIES ===")
    benchmark_queries(partitioned_dir, Path(raw_stats["parquet_path"]))

    print("\n=== CAPSTONE SUMMARY ===")
    print("You built an end-to-end Parquet storage layer with:")
    print("  1. Raw CSV ingestion")
    print("  2. SNAPPY Parquet baseline")
    print("  3. ZSTD compressed Hive-partitioned analytics dataset")
    print("  4. Metadata inspection")
    print("  5. Small-file simulation")
    print("  6. Compaction")
    print("  7. DuckDB SQL benchmarks")
    print("\nInterview line:")
    print(
        "“I designed a local data-lake style Parquet layer with compression, "
        "partition pruning, compaction, and DuckDB query benchmarking.”"
    )


if __name__ == "__main__":
    main()