# ============================================================
# Topic   : Parquet for Data Engineers
# File    : 02_compression_and_encoding.py
# Covers  : Compression codecs, dictionary encoding, metadata inspection
# Prereqs : pip install pyarrow pandas duckdb
# Run     : python 02_compression_and_encoding.py
# ============================================================

from __future__ import annotations

import os
import time
import uuid
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


def get_output_dir() -> Path:
    """Same as file 01."""
    default = Path("C:/tmp/studybook/parquet/") if os.name == "nt" else Path("/tmp/studybook/parquet/")
    output_dir = Path(os.getenv("OUTPUT_DIR", str(default)))
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def generate_benchmark_dataset(rows: int = 200_000) -> pd.DataFrame:
    """
    Mixed-type dataset for encoding demo. Columns:
      id:          int64   sequential 0…rows-1
      category:    string  one of 5 values — LOW cardinality (dictionary encoding fires)
      subcategory: string  one of 100 values — MEDIUM cardinality
      description: string  uuid4 per row — HIGH cardinality (dictionary encoding skips)
      value:       float64 random
      timestamp:   int64   unix timestamps, monotonically increasing (delta encoding)
    Seed = 42.
    """
    np.random.seed(42)

    categories = np.array(["electronics", "clothing", "books", "food", "sports"])
    subcategories = np.array([f"subcategory_{i:03d}" for i in range(100)])

    base_ts = 1_700_000_000

    return pd.DataFrame(
        {
            "id": np.arange(rows, dtype=np.int64),
            "category": np.random.choice(categories, size=rows),
            "subcategory": np.random.choice(subcategories, size=rows),
            "description": [str(uuid.uuid4()) for _ in range(rows)],
            "value": np.random.random(size=rows).astype("float64"),
            "timestamp": np.arange(base_ts, base_ts + rows, dtype=np.int64),
        }
    )


def write_with_codec(df: pd.DataFrame, path: str, compression: str) -> dict:
    """
    Write df with given compression codec. Measure write time and read time.
    Return:
      { codec: str, size_bytes: int, size_mb: float,
        write_ms: float, read_ms: float }
    Valid codecs: "NONE", "SNAPPY", "GZIP", "ZSTD", "BROTLI"
    """
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    codec = None if compression == "NONE" else compression.lower()

    start = time.perf_counter()
    table = pa.Table.from_pandas(df, preserve_index=False)
    pq.write_table(
        table,
        output_path,
        compression=codec,
        row_group_size=100_000,
        use_dictionary=True,
    )
    write_ms = (time.perf_counter() - start) * 1000

    start = time.perf_counter()
    _ = pq.read_table(output_path).to_pandas()
    read_ms = (time.perf_counter() - start) * 1000

    size_bytes = output_path.stat().st_size

    return {
        "codec": compression,
        "size_bytes": size_bytes,
        "size_mb": size_bytes / 1_000_000,
        "write_ms": write_ms,
        "read_ms": read_ms,
    }


def benchmark_codecs(df: pd.DataFrame, output_dir: Path) -> pd.DataFrame:
    """
    Call write_with_codec for all 5 codecs.
    Return a DataFrame with columns:
      codec, size_mb, compression_ratio, write_ms, read_ms
    Sort by size_mb ascending.
    compression_ratio = NONE_size / codec_size
    Print the table with annotations.
    """
    codecs = ["NONE", "SNAPPY", "GZIP", "ZSTD", "BROTLI"]
    rows = []

    for codec in codecs:
        path = output_dir / f"bench_{codec}.parquet"
        stats = write_with_codec(df, str(path), codec)
        rows.append(stats)

    none_size = next(row["size_bytes"] for row in rows if row["codec"] == "NONE")

    result = pd.DataFrame(rows)
    result["compression_ratio"] = none_size / result["size_bytes"]
    result = result[["codec", "size_mb", "compression_ratio", "write_ms", "read_ms"]]
    result = result.sort_values("size_mb").reset_index(drop=True)

    annotations = {
        "SNAPPY": "Best for streaming / Kafka / real-time",
        "GZIP": "Good compression, slow writes — cold storage",
        "ZSTD": "Best size+speed for analytics workloads ← RECOMMENDED",
        "BROTLI": "Smallest files, slowest writes — archive only",
        "NONE": "No compression — maximum read speed, maximum cost",
    }

    print("Codec  | Size MB | Ratio vs NONE | Write ms | Read ms | Interview note")
    print("-------|---------|---------------|----------|---------|----------------")
    for _, row in result.iterrows():
        codec = row["codec"]
        print(
            f"{codec:<6} | "
            f"{row['size_mb']:7.2f} | "
            f"{row['compression_ratio']:13.2f} | "
            f"{row['write_ms']:8.0f} | "
            f"{row['read_ms']:7.0f} | "
            f"{annotations[codec]}"
        )

    print(
        "\nTakeaway: compression is a workload decision. SNAPPY optimizes ingestion speed; "
        "ZSTD usually wins for analytics because it cuts scan bytes without crushing write speed."
    )

    return result


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
    np.random.seed(42)

    rows = 1_000_000
    low_path = output_dir / "dictionary_low_cardinality.parquet"
    high_path = output_dir / "dictionary_high_cardinality.parquet"

    low_card = pd.DataFrame(
        {
            "category": np.random.choice(
                ["electronics", "clothing", "books", "food", "sports"],
                size=rows,
            )
        }
    )

    high_card = pd.DataFrame(
        {
            "description": [str(uuid.uuid4()) for _ in range(rows)]
        }
    )

    pq.write_table(
        pa.Table.from_pandas(low_card, preserve_index=False),
        low_path,
        compression="SNAPPY",
        use_dictionary=True,
    )
    pq.write_table(
        pa.Table.from_pandas(high_card, preserve_index=False),
        high_path,
        compression="SNAPPY",
        use_dictionary=True,
    )

    low_meta = pq.ParquetFile(low_path).metadata.row_group(0).column(0)
    high_meta = pq.ParquetFile(high_path).metadata.row_group(0).column(0)

    low_encodings = list(low_meta.encodings)
    high_encodings = list(high_meta.encodings)

    low_size = low_path.stat().st_size
    high_size = high_path.stat().st_size

    low_label = "RLE_DICTIONARY" if "RLE_DICTIONARY" in low_encodings else str(low_encodings)
    high_label = "PLAIN" if "PLAIN" in high_encodings else str(high_encodings)

    print(f"Low cardinality  → encoding: {low_label:<24} → size: {low_size:,} bytes")
    print(f"High cardinality → encoding: {high_label:<24} → size: {high_size:,} bytes")
    print(f"Size ratio: high-cardinality UUID strings are {high_size / low_size:.1f}× larger.")

    print(
        "\nWhy it matters: dictionary encoding stores each repeated string once, maps it to "
        "a small integer, then compresses those integers with RLE/bit-packing. Five repeated "
        "categories become tiny integer codes. One million UUIDs have almost no repetition, "
        "so dictionary encoding cannot save much."
    )


def show_encoding_in_metadata(path: str) -> None:
    """
    Open file with pyarrow.parquet.ParquetFile. For each column in row group 0,
    print: column_name, encodings (list), compression.
    Expected encodings to highlight: PLAIN, RLE_DICTIONARY, DELTA_BINARY_PACKED.
    """
    parquet_file = pq.ParquetFile(path)
    row_group = parquet_file.metadata.row_group(0)

    print("Column       | Encodings                              | Compression")
    print("-------------|----------------------------------------|------------")

    for col_index in range(row_group.num_columns):
        column = row_group.column(col_index)
        encodings = list(column.encodings)
        print(
            f"{column.path_in_schema:<12} | "
            f"{str(encodings):<38} | "
            f"{column.compression}"
        )

    print(
        "\nHow to read this: RLE_DICTIONARY usually appears on repeated strings. "
        "PLAIN appears for raw values or dictionary pages. Some integer/timestamp-heavy "
        "files may expose delta-style encodings depending on writer settings and Arrow version."
    )


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
    if need_splittable:
        recommendation = "SNAPPY"
        reason = "Hadoop-style split-heavy jobs usually expect splittable, fast codecs."
    elif write_heavy and not read_heavy:
        recommendation = "SNAPPY"
        reason = "Write-heavy ingestion benefits from cheap CPU and fast compression."
    elif read_heavy and not write_heavy:
        recommendation = "ZSTD"
        reason = "Read-heavy analytics usually wins by reducing scan bytes."
    elif not read_heavy and not write_heavy:
        recommendation = "BROTLI"
        reason = "Infrequent reads/archive workloads can trade CPU for smaller files."
    else:
        recommendation = "ZSTD"
        reason = "Balanced workloads usually benefit from ZSTD's size/speed tradeoff."

    print(
        f"read_heavy={read_heavy}, write_heavy={write_heavy}, "
        f"need_splittable={need_splittable} → {recommendation}: {reason}"
    )

    return recommendation


def main() -> None:
    out = get_output_dir()
    df = generate_benchmark_dataset(rows=200_000)

    print("\n=== CODEC BENCHMARK ===")
    results = benchmark_codecs(df, out)
    print("\nSorted result DataFrame:")
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