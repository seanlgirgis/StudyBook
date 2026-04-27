# ============================================================
# Topic   : Delta Lake for Data Engineers
# File    : 05_optimize_and_vacuum.py
# Covers  : Small files, OPTIMIZE compact, Z-order, VACUUM, query timing
# Prereqs : pip install deltalake pandas pyarrow
# Run     : python 05_optimize_and_vacuum.py
# ============================================================

from deltalake import DeltaTable, write_deltalake
import pandas as pd
from pathlib import Path
import os
import shutil
import random
import time


def get_output_dir() -> Path:
    default = Path("C:/tmp/studybook/delta" if os.name == "nt" else "/tmp/studybook/delta")
    out = Path(os.getenv("OUTPUT_DIR", str(default)))
    out.mkdir(parents=True, exist_ok=True)
    return out


def generate_sensor_data(n_rows: int = 20, seed: int = 42) -> pd.DataFrame:
    random.seed(seed)
    plants = ["plant_A", "plant_B", "plant_C"]

    return pd.DataFrame(
        {
            "sensor_id": [f"sensor_{random.randint(0, 99):03d}" for _ in range(n_rows)],
            "plant": [random.choice(plants) for _ in range(n_rows)],
            "value": [round(random.uniform(15, 95), 3) for _ in range(n_rows)],
            "ts": pd.date_range("2024-01-01", periods=n_rows, freq="1min"),
        }
    )


def active_file_paths(path: Path) -> list[Path]:
    """
    Return active Parquet files from the latest Delta snapshot.

    WHY:
    Delta's current table state is defined by the transaction log, not simply by
    every Parquet file sitting in the directory.
    """
    dt = DeltaTable(str(path))
    files = []

    for uri in dt.file_uris():
        if uri.startswith("file:///"):
            files.append(Path(uri.replace("file:///", "")))
        elif uri.startswith("file://"):
            files.append(Path(uri.replace("file://", "")))
        else:
            files.append(path / uri)

    return files


def show_file_fragmentation(path: Path) -> dict:
    """
    Show active file count and size distribution.

    WHY small files hurt:
    Each file has open/read/list overhead. Many tiny files slow scans even when
    the total data size is small.
    """
    files = active_file_paths(path)
    sizes = [f.stat().st_size for f in files if f.exists()]

    file_count = len(sizes)
    total_size_mb = sum(sizes) / (1024 * 1024)
    avg_size_mb = total_size_mb / file_count if file_count else 0
    min_size_mb = min(sizes) / (1024 * 1024) if sizes else 0
    max_size_mb = max(sizes) / (1024 * 1024) if sizes else 0

    print(f"Small file problem: {file_count} files avg {avg_size_mb * 1024:.0f} KB each")

    return {
        "file_count": file_count,
        "total_size_mb": total_size_mb,
        "avg_size_mb": avg_size_mb,
        "min_size_mb": min_size_mb,
        "max_size_mb": max_size_mb,
    }


def create_fragmented_table(path: Path, n_appends: int = 50) -> None:
    """
    Simulate streaming ingestion.

    WHY:
    Streaming systems often write frequent small batches. Without compaction,
    these create many tiny files.
    """
    if path.exists():
        shutil.rmtree(path)

    first = generate_sensor_data(20, seed=0)
    write_deltalake(str(path), first, mode="overwrite")

    for i in range(1, n_appends):
        batch = generate_sensor_data(20, seed=i)
        write_deltalake(str(path), batch, mode="append")

    stats = show_file_fragmentation(path)
    print(f"Created fragmented table with {stats['file_count']} active files")


def optimize_table(path: Path) -> dict:
    """
    Compact small files.

    WHY OPTIMIZE:
    Combines many small files into fewer larger files. This reduces file-open
    overhead and improves scan efficiency.
    """
    before = show_file_fragmentation(path)
    t0 = time.perf_counter()

    metrics = DeltaTable(str(path)).optimize.compact()

    compact_ms = (time.perf_counter() - t0) * 1000
    after = show_file_fragmentation(path)

    before_files = before["file_count"]
    after_files = after["file_count"]

    return {
        "before_files": before_files,
        "after_files": after_files,
        "reduction_ratio": before_files / after_files if after_files else 0,
        "before_size_mb": before["total_size_mb"],
        "after_size_mb": after["total_size_mb"],
        "compact_ms": compact_ms,
        "metrics": metrics,
    }


def zorder_by_columns(path: Path, columns: list[str]) -> None:
    """
    Run Z-order optimization.

    WHY Z-order:
    Z-order clustering helps colocate related values across columns so filtered
    reads can skip more files.
    """
    before = show_file_fragmentation(path)

    try:
        metrics = DeltaTable(str(path)).optimize.z_order(columns)
        print(f"Z-order completed on columns: {columns}")
        print(f"Z-order metrics: {metrics}")
    except Exception as exc:
        print(f"Z-order skipped: {type(exc).__name__}: {exc}")
        print("This is acceptable if the installed delta-rs build does not support Z-order here.")

    after = show_file_fragmentation(path)
    print(f"Files before Z-order: {before['file_count']}, after: {after['file_count']}")


def vacuum_table(path: Path, retention_hours: int = 168) -> dict:
    """
    Vacuum old files no longer referenced by the latest table state.

    WHY retention:
    Old files support time travel. Short retention saves storage but reduces the
    time window available for rollback/audit.
    """
    dt = DeltaTable(str(path))
    before_all_parquet = list(path.rglob("*.parquet"))

    try:
        removable = dt.vacuum(retention_hours=retention_hours, dry_run=True)
    except Exception as exc:
        print(f"Vacuum dry run blocked by safety check: {type(exc).__name__}: {exc}")
        print("Retrying dry run with default 168-hour retention.")
        removable = dt.vacuum(retention_hours=168, dry_run=True)

    space_freed_mb = 0.0
    for item in removable:
        p = Path(item)
        if not p.is_absolute():
            p = path / item
        if p.exists():
            space_freed_mb += p.stat().st_size / (1024 * 1024)

    after_all_parquet = list(path.rglob("*.parquet"))

    print(f"Vacuum dry run found {len(removable)} files eligible for removal")
    print(f"Estimated space that could be freed: {space_freed_mb:.4f} MB")
    print(f"Physical parquet files before/after dry run: {len(before_all_parquet)} / {len(after_all_parquet)}")

    return {
        "files_removed": len(removable),
        "space_freed_mb": space_freed_mb,
    }


def measure_query_speedup(path: Path, filter_col: str = "plant", filter_val: str = "plant_A") -> dict:
    """
    Time a filtered read.

    WHY:
    Compaction usually helps most when a table has many tiny files.
    """
    t0 = time.perf_counter()
    df = DeltaTable(str(path)).to_pandas(filters=[(filter_col, "=", filter_val)])
    elapsed_ms = (time.perf_counter() - t0) * 1000

    print(f"Filtered query {filter_col}={filter_val}: {len(df)} rows in {elapsed_ms:.2f} ms")

    return {
        "elapsed_ms": elapsed_ms,
        "rows_returned": len(df),
    }


def main():
    path = get_output_dir() / "optimize_demo"

    print("\n=== CREATE FRAGMENTED TABLE (50 appends x 20 rows) ===")
    create_fragmented_table(path, n_appends=50)
    before_stats = show_file_fragmentation(path)

    print("\n=== QUERY BEFORE OPTIMIZE ===")
    before_query = measure_query_speedup(path)

    print("\n=== OPTIMIZE (COMPACT) ===")
    opt_stats = optimize_table(path)
    print(
        f"Files: {opt_stats['before_files']} -> {opt_stats['after_files']} "
        f"(reduction: {opt_stats['reduction_ratio']:.1f}x)"
    )
    print(f"Compaction time: {opt_stats['compact_ms']:.2f} ms")

    print("\n=== Z-ORDER ===")
    zorder_by_columns(path, columns=["plant", "sensor_id"])

    print("\n=== VACUUM (dry run) ===")
    vacuum_table(path, retention_hours=0)

    print("\n=== QUERY AFTER OPTIMIZE ===")
    after_query = measure_query_speedup(path)

    speedup_x = before_query["elapsed_ms"] / after_query["elapsed_ms"] if after_query["elapsed_ms"] else 0
    print(f"Speedup: {speedup_x:.1f}x")

    print("\n=== SUMMARY ===")
    print(f"Before optimize files: {before_stats['file_count']}")
    print(f"After optimize files:  {show_file_fragmentation(path)['file_count']}")
    print("OPTIMIZE improved layout while VACUUM dry run showed what old files could be removed.")


if __name__ == "__main__":
    main()