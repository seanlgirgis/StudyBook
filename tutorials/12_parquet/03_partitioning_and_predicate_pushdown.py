# ============================================================
# Topic   : Parquet for Data Engineers
# File    : 03_partitioning_and_predicate_pushdown.py
# Covers  : Hive partitioning, partition pruning, row group pushdown
# Prereqs : pip install pyarrow pandas duckdb
# Run     : python 03_partitioning_and_predicate_pushdown.py
# ============================================================

from __future__ import annotations

import os
import shutil
import time
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.dataset as ds
import pyarrow.parquet as pq


def get_output_dir() -> Path:
    """Same pattern."""
    default = Path("C:/tmp/studybook/parquet/") if os.name == "nt" else Path("/tmp/studybook/parquet/")
    output_dir = Path(os.getenv("OUTPUT_DIR", str(default)))
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


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
    np.random.seed(42)

    devices = np.array([f"device_{i:04d}" for i in range(100)])
    plants = np.array(["plant_A", "plant_B", "plant_C"])
    sensors = np.array(["temperature", "pressure", "vibration", "humidity"])

    now = pd.Timestamp.now().floor("s")
    seconds_in_year = 365 * 24 * 60 * 60
    random_seconds = np.random.randint(0, seconds_in_year, size=rows)
    ts = now - pd.to_timedelta(random_seconds, unit="s")

    df = pd.DataFrame(
        {
            "device_id": np.random.choice(devices, size=rows),
            "plant_id": np.random.choice(plants, size=rows),
            "sensor_type": np.random.choice(sensors, size=rows),
            "value": np.random.random(size=rows).astype("float64"),
            "ts": ts,
        }
    )

    df["year"] = df["ts"].dt.year.astype("int32")
    df["month"] = df["ts"].dt.month.astype("int32")

    return df


def write_partitioned_dataset(
    df: pd.DataFrame,
    output_dir: Path,
    partition_cols: list[str],
) -> None:
    """
    Use pyarrow.dataset.write_dataset with hive partitioning.
    partition_cols example: ["plant_id", "year", "month"]
    Hive layout: output_dir/plant_id=plant_A/year=2024/month=1/part-0.parquet
    Use SNAPPY compression, max_rows_per_file=200_000.
    Print total files written and directory tree (2 levels deep).
    """
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    table = pa.Table.from_pandas(df, preserve_index=False)

    ds.write_dataset(
        table,
        base_dir=output_dir,
        format="parquet",
        partitioning=partition_cols,
        partitioning_flavor="hive",
        existing_data_behavior="overwrite_or_ignore",
        max_rows_per_file=200_000,
        max_rows_per_group=100_000,
        file_options=ds.ParquetFileFormat().make_write_options(compression="SNAPPY"),
    )

    files = list(output_dir.rglob("*.parquet"))
    print(f"Total files written: {len(files)}")

    print("\nDirectory tree (2 levels deep):")
    for plant_dir in sorted(output_dir.iterdir()):
        if plant_dir.is_dir():
            print(f"  {plant_dir.name}/")
            for year_dir in sorted(plant_dir.iterdir()):
                if year_dir.is_dir():
                    print(f"    {year_dir.name}/")


def count_files_in_dataset(dataset_path: Path) -> dict:
    """
    Walk dataset directory. Return:
      { total_files: int, files_per_partition: dict,
        avg_file_size_mb: float, min_file_size_mb: float, max_file_size_mb: float }
    Flag small files: print warning if any file < 1 MB.
    """
    files = list(dataset_path.rglob("*.parquet"))
    if not files:
        raise FileNotFoundError(f"No Parquet files found under {dataset_path}")

    sizes = [f.stat().st_size for f in files]

    files_per_partition: dict[str, int] = {}
    for f in files:
        parent = f.parent.relative_to(dataset_path)
        key = str(parent)
        files_per_partition[key] = files_per_partition.get(key, 0) + 1

    stats = {
        "total_files": len(files),
        "files_per_partition": files_per_partition,
        "avg_file_size_mb": float(np.mean(sizes) / 1_000_000),
        "min_file_size_mb": float(np.min(sizes) / 1_000_000),
        "max_file_size_mb": float(np.max(sizes) / 1_000_000),
    }

    print(f"Total Parquet files: {stats['total_files']}")
    print(f"Average file size:   {stats['avg_file_size_mb']:.2f} MB")
    print(f"Smallest file size:  {stats['min_file_size_mb']:.2f} MB")
    print(f"Largest file size:   {stats['max_file_size_mb']:.2f} MB")

    if any(size < 1_000_000 for size in sizes):
        print(
            "⚠️ Warning: Small files detected (<1 MB). "
            "In production, too many tiny Parquet files increase metadata overhead "
            "and reduce scan efficiency."
        )

    return stats


def read_with_filter(dataset_path: Path, filters) -> pd.DataFrame:
    """
    Open dataset with pyarrow.dataset.dataset(). Apply filters using
    pyarrow filter expressions. Print rows returned.
    Example filter: ds.field("plant_id") == "plant_A"
    """
    dataset = ds.dataset(dataset_path, format="parquet", partitioning="hive")
    table = dataset.to_table(filter=filters)
    df = table.to_pandas()

    print(f"Rows returned: {len(df):,}")
    return df


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
    dataset = ds.dataset(dataset_path, format="parquet", partitioning="hive")
    all_files = list(dataset_path.rglob("*.parquet"))

    start = time.perf_counter()
    unfiltered_df = dataset.to_table().to_pandas()
    unfiltered_ms = (time.perf_counter() - start) * 1000

    filter_expr = ds.field("plant_id") == plant_id

    start = time.perf_counter()
    filtered_df = dataset.to_table(filter=filter_expr).to_pandas()
    filtered_ms = (time.perf_counter() - start) * 1000

    filtered_files = [f for f in all_files if f"plant_id={plant_id}" in str(f)]
    speedup_x = unfiltered_ms / filtered_ms if filtered_ms > 0 else float("inf")
    pct_files_scanned = (len(filtered_files) / len(all_files)) * 100 if all_files else 0.0

    result = {
        "unfiltered_ms": unfiltered_ms,
        "filtered_ms": filtered_ms,
        "speedup_x": speedup_x,
        "unfiltered_file_count": len(all_files),
        "filtered_file_count": len(filtered_files),
        "pct_files_scanned": pct_files_scanned,
    }

    print(f"WITHOUT partition filter: {unfiltered_ms:.0f} ms | {len(unfiltered_df):,} rows")
    print(f"WITH partition filter:    {filtered_ms:.0f} ms | {len(filtered_df):,} rows")
    print(f"Files scanned:            {len(filtered_files)} / {len(all_files)}")
    print(f"Approx scan fraction:     {pct_files_scanned:.1f}%")

    print(
        "\nPartition pruning means files in other partitions are never opened. "
        "This is OS-level skipping based on directory names like plant_id=plant_A, "
        "not row-level filtering after the data has already been read."
    )

    return result


def demonstrate_row_group_pushdown(
    path: str,
    filter_col: str = "category",
    filter_value: str = "books",
) -> dict:
    """
    On a SINGLE non-partitioned Parquet file with multiple row groups:
    Time full read vs filtered read using pyarrow filters.
    Return: { full_read_ms, filtered_ms, full_rows, filtered_rows }
    Explain: row group statistics (min/max per column) allow skipping entire
    row groups without reading their pages — this is predicate pushdown.
    """
    parquet_file = pq.ParquetFile(path)
    available_columns = set(parquet_file.schema_arrow.names)

    if filter_col not in available_columns:
        raise ValueError(
            f"Column {filter_col!r} not found in {path}. "
            f"Available columns: {sorted(available_columns)}"
        )

    start = time.perf_counter()
    full_table = pq.read_table(path)
    full_df = full_table.to_pandas()
    full_read_ms = (time.perf_counter() - start) * 1000

    start = time.perf_counter()
    filtered_table = pq.read_table(path, filters=[(filter_col, "==", filter_value)])
    filtered_df = filtered_table.to_pandas()
    filtered_ms = (time.perf_counter() - start) * 1000

    result = {
        "full_read_ms": full_read_ms,
        "filtered_ms": filtered_ms,
        "full_rows": len(full_df),
        "filtered_rows": len(filtered_df),
    }

    print(f"Filter used: {filter_col} == {filter_value!r}")
    print(f"Full read:   {full_read_ms:.0f} ms | {len(full_df):,} rows")
    print(f"Filtered:    {filtered_ms:.0f} ms | {len(filtered_df):,} rows")

    print("\nRow group statistics from footer:")
    for rg_index in range(parquet_file.metadata.num_row_groups):
        row_group = parquet_file.metadata.row_group(rg_index)
        for col_index in range(row_group.num_columns):
            column = row_group.column(col_index)
            if column.path_in_schema == filter_col and column.statistics is not None:
                stats = column.statistics
                print(
                    f"  Row group {rg_index}: "
                    f"rows={row_group.num_rows:,}, "
                    f"min={stats.min!r}, max={stats.max!r}, "
                    f"nulls={stats.null_count}"
                )

    print(
        "\nPredicate pushdown works because Parquet stores min/max statistics per column "
        "per row group. If a filter proves an entire row group cannot match, the engine "
        "skips that row group without reading its data pages. For low-cardinality columns "
        "like category, every row group may still contain every category, so the speedup "
        "can be modest — but the mechanism is the key interview concept."
    )

    return result


def design_partition_strategy(query_patterns: list[str], cardinality_map: dict) -> str:
    """
    Simple rule-based advisor. Rules:
      - Partition columns must appear in WHERE clauses of most queries
      - Avoid high cardinality (>10k unique values) as partition key → too many small files
      - Prefer columns with 3–100 unique values
      - At most 3 partition levels for manageability
    Print recommendation as numbered list with reasoning.
    Return recommended partition columns as comma-separated string.
    """
    print("Query patterns:")
    for pattern in query_patterns:
        print(f"  - {pattern}")

    scored_candidates: list[tuple[str, int, int]] = []

    print("\nPartition Strategy Recommendation:")
    item = 1
    for col, cardinality in cardinality_map.items():
        appears_in_queries = sum(1 for q in query_patterns if col in q)
        if cardinality > 10_000:
            print(
                f"{item}. ❌ Avoid {col}: {cardinality:,} unique values creates too many "
                "directories and small files."
            )
        elif 3 <= cardinality <= 100:
            print(
                f"{item}. ✅ Strong candidate {col}: {cardinality:,} unique values and "
                f"appears in {appears_in_queries} query pattern(s)."
            )
            scored_candidates.append((col, appears_in_queries, cardinality))
        else:
            print(
                f"{item}. ⚠️ Use {col} carefully: {cardinality:,} unique values may be "
                "too low or too high depending on query volume."
            )
        item += 1

    scored_candidates.sort(key=lambda x: (-x[1], x[2]))
    selected = [col for col, _, _ in scored_candidates[:3]]
    recommendation = ", ".join(selected)

    print(
        "\nRules of thumb: choose columns that appear in WHERE clauses, avoid very high "
        "cardinality keys, prefer 3–100 unique values, and keep partition depth to at most "
        "3 levels."
    )
    print(f"Recommended partition columns: {recommendation}")

    return recommendation


def main() -> None:
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
    print(
        f"Speedup: {pruning['speedup_x']:.1f}×  |  "
        f"Files scanned: {pruning['pct_files_scanned']:.1f}%"
    )

    print("\n=== ROW GROUP PUSHDOWN ===")
    single_file = str(out / "ecommerce_events.parquet")
    if Path(single_file).exists():
        rg_stats = demonstrate_row_group_pushdown(
            single_file,
            filter_col="category",
            filter_value="books",
        )
        print(rg_stats)
    else:
        print("Run file 01 first to create ecommerce_events.parquet")

    print("\n=== PARTITION STRATEGY ADVISOR ===")
    design_partition_strategy(
        query_patterns=["WHERE plant_id=? AND sensor_type=?", "WHERE plant_id=?"],
        cardinality_map={"plant_id": 3, "sensor_type": 4, "device_id": 100},
    )


if __name__ == "__main__":
    main()