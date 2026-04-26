# ============================================================
# Topic   : Parquet for Data Engineers
# File    : 01_parquet_basics_and_internals.py
# Covers  : Parquet basics, internals, row groups, metadata, CSV comparison
# Prereqs : pip install pyarrow pandas duckdb
# Run     : python 01_parquet_basics_and_internals.py
# ============================================================

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any

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
    np.random.seed(42)

    users = np.array([f"user_{i:06d}" for i in range(1, 10_001)])
    products = np.array([f"prod_{i:04d}" for i in range(1, 1_001)])
    categories = np.array(["electronics", "clothing", "books", "food", "sports"])
    countries = np.array(["US", "UK", "DE", "FR", "JP", "AU", "CA", "BR"])
    country_weights = np.array([0.34, 0.12, 0.11, 0.09, 0.10, 0.07, 0.10, 0.07])

    now = pd.Timestamp.now().floor("s")
    seconds_in_90_days = 90 * 24 * 60 * 60
    random_seconds = np.random.randint(0, seconds_in_90_days, size=rows)

    df = pd.DataFrame(
        {
            "user_id": np.random.choice(users, size=rows),
            "product_id": np.random.choice(products, size=rows),
            "category": np.random.choice(categories, size=rows),
            "amount": np.round(np.random.uniform(1.0, 500.0, size=rows), 2).astype("float64"),
            "ts": now - pd.to_timedelta(random_seconds, unit="s"),
            "country": np.random.choice(countries, size=rows, p=country_weights),
        }
    )

    return df


def write_parquet(df: pd.DataFrame, path: str, row_group_size: int = 100_000) -> None:
    """
    Write df to path as Parquet with SNAPPY compression.
    Use pyarrow.parquet.write_table with row_group_size parameter.
    Convert pandas DataFrame to pyarrow Table first.
    Print: path, row_group_size, total rows written.
    """
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    table = pa.Table.from_pandas(df, preserve_index=False)
    pq.write_table(
        table,
        output_path,
        compression="SNAPPY",
        row_group_size=row_group_size,
    )

    print(f"Parquet written: {output_path}")
    print(f"Row group size:  {row_group_size:,}")
    print(f"Rows written:    {len(df):,}")


def read_parquet(path: str, columns: list[str] | None = None) -> pd.DataFrame:
    """
    Read Parquet file. If columns is not None, read only those columns
    (demonstrate columnar read-skipping). Print columns read, rows returned,
    and a note explaining WHY column projection reduces I/O.
    """
    df = pd.read_parquet(path, columns=columns)

    cols_display = columns if columns is not None else "ALL COLUMNS"
    print(f"Columns read:  {cols_display}")
    print(f"Rows returned: {len(df):,}")
    print(
        "Why this is fast: Parquet stores data by column, so reading only "
        "['user_id', 'amount', 'country'] skips the byte ranges for product_id, "
        "category, and ts instead of pulling the whole file from disk."
    )

    return df


def _scalar_to_python(value: Any) -> Any:
    """Convert PyArrow metadata scalar values into clean printable Python values."""
    if value is None:
        return None
    if hasattr(value, "as_py"):
        return value.as_py()
    return value


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
    parquet_file = pq.ParquetFile(path)
    metadata = parquet_file.metadata
    schema_fields = parquet_file.schema_arrow.names
    file_size_bytes = os.path.getsize(path)

    result: dict[str, Any] = {
        "num_row_groups": metadata.num_row_groups,
        "schema_fields": schema_fields,
        "total_rows": metadata.num_rows,
        "file_size_bytes": file_size_bytes,
        "row_groups": [],
    }

    print(f"File: {path}")
    print(f"Size: {file_size_bytes / 1_000_000:.2f} MB")
    print(f"Rows: {metadata.num_rows:,}")
    print(f"Row groups: {metadata.num_row_groups}")
    print(f"Schema fields: {', '.join(schema_fields)}")

    for rg_index in range(metadata.num_row_groups):
        row_group = metadata.row_group(rg_index)

        rg_dict: dict[str, Any] = {
            "rg_index": rg_index,
            "num_rows": row_group.num_rows,
            "total_compressed_bytes": row_group.total_byte_size,
            "columns": [],
        }

        print(
            f"\nRow group {rg_index}: "
            f"{row_group.num_rows:,} rows, "
            f"{row_group.total_byte_size / 1_000_000:.2f} MB compressed logical size"
        )

        for col_index in range(row_group.num_columns):
            column = row_group.column(col_index)
            stats = column.statistics

            has_stats = stats is not None
            min_value = _scalar_to_python(stats.min) if has_stats and stats.has_min_max else None
            max_value = _scalar_to_python(stats.max) if has_stats and stats.has_min_max else None
            null_count = stats.null_count if has_stats else None

            col_dict = {
                "name": column.path_in_schema,
                "compression": column.compression,
                "encodings": list(column.encodings),
                "compressed_bytes": column.total_compressed_size,
                "has_statistics": has_stats,
                "min_value": min_value,
                "max_value": max_value,
                "null_count": null_count,
            }
            rg_dict["columns"].append(col_dict)

            print(
                f"  {column.path_in_schema:<12} "
                f"codec={column.compression:<8} "
                f"bytes={column.total_compressed_size:>10,} "
                f"stats={str(has_stats):<5} "
                f"min={min_value!s:<24} "
                f"max={max_value!s:<24} "
                f"nulls={null_count}"
            )

        result["row_groups"].append(rg_dict)

    # Predicate pushdown works because the footer stores min/max per column per row group.
    # If WHERE amount > 1000 and a row group's amount.max is 499.99, the engine can skip
    # that entire row group without reading its data pages from disk.
    print(
        "\nPredicate pushdown insight: min/max statistics live in the Parquet footer. "
        "Query engines read the footer first, then skip row groups whose stats prove "
        "they cannot match the WHERE clause."
    )

    return result


def compare_csv_vs_parquet(df: pd.DataFrame, output_dir: Path) -> dict:
    """
    Write the same DataFrame as both CSV and Parquet (SNAPPY).
    Time each write and read. Return:
      { csv_size_bytes, parquet_size_bytes, compression_ratio,
        csv_write_ms, parquet_write_ms,
        csv_read_ms,  parquet_read_ms }
    Print a formatted comparison table showing ratio and speedup.
    """
    csv_path = output_dir / "ecommerce_events.csv"
    parquet_path = output_dir / "ecommerce_events_compare.parquet"

    start = time.perf_counter()
    df.to_csv(csv_path, index=False)
    csv_write_ms = (time.perf_counter() - start) * 1000

    start = time.perf_counter()
    pq.write_table(
        pa.Table.from_pandas(df, preserve_index=False),
        parquet_path,
        compression="SNAPPY",
        row_group_size=100_000,
    )
    parquet_write_ms = (time.perf_counter() - start) * 1000

    start = time.perf_counter()
    csv_df = pd.read_csv(csv_path)
    csv_read_ms = (time.perf_counter() - start) * 1000

    start = time.perf_counter()
    parquet_df = pd.read_parquet(parquet_path)
    parquet_read_ms = (time.perf_counter() - start) * 1000

    csv_size_bytes = csv_path.stat().st_size
    parquet_size_bytes = parquet_path.stat().st_size
    compression_ratio = csv_size_bytes / parquet_size_bytes
    read_speedup = csv_read_ms / parquet_read_ms if parquet_read_ms > 0 else float("inf")

    stats = {
        "csv_size_bytes": csv_size_bytes,
        "parquet_size_bytes": parquet_size_bytes,
        "compression_ratio": compression_ratio,
        "csv_write_ms": csv_write_ms,
        "parquet_write_ms": parquet_write_ms,
        "csv_read_ms": csv_read_ms,
        "parquet_read_ms": parquet_read_ms,
    }

    print("\nFormat   | Size (MB) | Write (ms) | Read (ms)")
    print("---------|-----------|------------|----------")
    print(f"CSV      | {csv_size_bytes / 1_000_000:9.2f} | {csv_write_ms:10.0f} | {csv_read_ms:8.0f}")
    print(
        f"Parquet  | {parquet_size_bytes / 1_000_000:9.2f} | "
        f"{parquet_write_ms:10.0f} | {parquet_read_ms:8.0f}"
    )
    print(f"\nCompression ratio: CSV is {compression_ratio:.1f}× larger than Parquet.")
    print(f"Read speedup:       Parquet read was {read_speedup:.1f}× faster in this run.")
    print(
        f"Validation rows:    CSV={len(csv_df):,}, Parquet={len(parquet_df):,}. "
        "Same data shape, very different storage layout."
    )

    return stats


def explain_row_groups(path: str) -> None:
    """
    Print for each row group: index, row offset (first row number), row count,
    compressed size. Then explain: row groups are the unit of predicate pushdown —
    if a filter eliminates an entire row group, those bytes are never read from disk.
    """
    parquet_file = pq.ParquetFile(path)
    metadata = parquet_file.metadata

    row_offset = 0
    print("Row group | First row | Row count | Compressed logical size (MB)")
    print("----------|-----------|-----------|-----------------------------")

    for rg_index in range(metadata.num_row_groups):
        row_group = metadata.row_group(rg_index)
        print(
            f"{rg_index:9d} | "
            f"{row_offset:9,d} | "
            f"{row_group.num_rows:9,d} | "
            f"{row_group.total_byte_size / 1_000_000:27.2f}"
        )
        row_offset += row_group.num_rows

    print(
        "\nRow groups are the unit of predicate pushdown. If a filter eliminates an "
        "entire row group, those compressed bytes are never read from disk. "
        "That is the difference between scanning a data lake and surgically touching "
        "only the chunks that can contain matching rows."
    )


def main() -> None:
    out = get_output_dir()
    df = generate_analytics_dataset(rows=500_000)
    path = str(out / "ecommerce_events.parquet")

    print("\n=== WRITE & READ ===")
    write_parquet(df, path, row_group_size=100_000)
    df_back = read_parquet(path, columns=["user_id", "amount", "country"])
    print(f"Projected DataFrame shape: {df_back.shape}")

    print("\n=== INTERNAL METADATA ===")
    metadata = inspect_parquet_file(path)
    print(
        f"\nMetadata summary: {metadata['total_rows']:,} rows, "
        f"{metadata['num_row_groups']} row groups, "
        f"{len(metadata['schema_fields'])} columns."
    )

    print("\n=== CSV vs PARQUET ===")
    stats = compare_csv_vs_parquet(df, out)
    print(
        f"\nReturned stats: CSV={stats['csv_size_bytes'] / 1_000_000:.2f} MB, "
        f"Parquet={stats['parquet_size_bytes'] / 1_000_000:.2f} MB, "
        f"ratio={stats['compression_ratio']:.1f}×"
    )

    print("\n=== ROW GROUPS ===")
    explain_row_groups(path)


if __name__ == "__main__":
    main()