# ============================================================
# Topic   : Parquet for Data Engineers
# File    : 04_schema_evolution_and_compatibility.py
# Covers  : Schema evolution, compatibility checks, breaking vs safe changes
# Prereqs : pip install pyarrow pandas duckdb
# Run     : python 04_schema_evolution_and_compatibility.py
# ============================================================

from __future__ import annotations

import os
import shutil
from pathlib import Path

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


def _fresh_dir(path: Path) -> None:
    """Delete and recreate a directory so old Parquet files cannot pollute demos."""
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def write_v1_schema(output_dir: Path) -> str:
    """
    Write 50k rows with v1 schema:
      device_id: string, sensor_type: string, value: float32, ts: int64 (unix ms)
    Use SNAPPY. Save to output_dir/schema_evolution/v1/part-0.parquet
    Return file path.
    """
    np.random.seed(42)

    path = output_dir / "schema_evolution" / "v1"
    _fresh_dir(path)
    file_path = path / "part-0.parquet"

    df = pd.DataFrame(
        {
            "device_id": [f"device_{i:04d}" for i in np.random.randint(0, 100, 50_000)],
            "sensor_type": np.random.choice(["temperature", "pressure", "vibration"], 50_000),
            "value": np.random.random(50_000).astype("float32"),
            "ts": np.random.randint(
                1_700_000_000_000,
                1_800_000_000_000,
                50_000,
                dtype=np.int64,
            ),
        }
    )

    pq.write_table(pa.Table.from_pandas(df, preserve_index=False), file_path, compression="SNAPPY")
    print(f"Wrote v1 schema: {file_path}")
    return str(file_path)


def write_v2_schema_add_column(output_dir: Path) -> str:
    """
    Add nullable column 'unit' (string, nullable). 50k rows.
    Rows have unit = one of ["C","PSI","mm/s","RH%"] or None (20% null).
    Save to output_dir/schema_evolution/v2/part-0.parquet. Return path.
    SAFE CHANGE: adding a nullable column is always backward-compatible.
    """
    np.random.seed(43)

    path = output_dir / "schema_evolution" / "v2"
    _fresh_dir(path)
    file_path = path / "part-0.parquet"

    units = np.array(["C", "PSI", "mm/s", "RH%"], dtype=object)
    unit_values = np.random.choice(units, 50_000).astype(object)
    unit_values[np.random.rand(50_000) < 0.20] = None

    df = pd.DataFrame(
        {
            "device_id": [f"device_{i:04d}" for i in np.random.randint(0, 100, 50_000)],
            "sensor_type": np.random.choice(["temperature", "pressure", "vibration"], 50_000),
            "value": np.random.random(50_000).astype("float32"),
            "ts": np.random.randint(
                1_700_000_000_000,
                1_800_000_000_000,
                50_000,
                dtype=np.int64,
            ),
            "unit": unit_values,
        }
    )

    pq.write_table(pa.Table.from_pandas(df, preserve_index=False), file_path, compression="SNAPPY")
    print(f"Wrote v2 schema: {file_path}")
    return str(file_path)


def write_v3_schema_widen_type(output_dir: Path) -> str:
    """
    Widen value column from float32 → float64. Add 'firmware_version' string column.
    50k rows. Save to output_dir/schema_evolution/v3/part-0.parquet. Return path.
    SAFE CHANGE: widening numeric types is backward-compatible (float32 reads as float64).
    """
    np.random.seed(44)

    path = output_dir / "schema_evolution" / "v3"
    _fresh_dir(path)
    file_path = path / "part-0.parquet"

    df = pd.DataFrame(
        {
            "device_id": [f"device_{i:04d}" for i in np.random.randint(0, 100, 50_000)],
            "sensor_type": np.random.choice(["temperature", "pressure", "vibration"], 50_000),
            "value": np.random.random(50_000).astype("float64"),
            "ts": np.random.randint(
                1_700_000_000_000,
                1_800_000_000_000,
                50_000,
                dtype=np.int64,
            ),
            "firmware_version": np.random.choice(["v1.0", "v1.1", "v2.0"], 50_000),
        }
    )

    pq.write_table(pa.Table.from_pandas(df, preserve_index=False), file_path, compression="SNAPPY")
    print(f"Wrote v3 schema: {file_path}")
    return str(file_path)


def _unified_schema_for_evolution() -> pa.Schema:
    """
    Explicit schema for merged read.

    Raw Parquet files do not have a transaction log. In production, Delta Lake
    or Iceberg would track schema history. Here we provide the intended final
    schema manually so older files get nulls for missing nullable columns.
    """
    return pa.schema(
        [
            pa.field("device_id", pa.string()),
            pa.field("sensor_type", pa.string()),
            pa.field("value", pa.float64()),
            pa.field("ts", pa.int64()),
            pa.field("unit", pa.string()),
            pa.field("firmware_version", pa.string()),
        ]
    )


def read_with_schema_merge(dataset_path: Path) -> pd.DataFrame:
    """
    Read v1 + v2 + v3 files together using pyarrow.dataset with an explicit
    merged schema. Columns missing in older files become null.
    Print final schema and null counts per column.
    Return merged DataFrame.
    """
    schema = _unified_schema_for_evolution()
    dataset = ds.dataset(dataset_path, format="parquet", schema=schema)

    table = dataset.to_table()
    df = table.to_pandas()

    print("Final merged schema:")
    print(table.schema)

    print("\nNull counts per column:")
    print(df.isnull().sum())

    return df


def is_widening(old: pa.DataType, new: pa.DataType) -> bool:
    """Return True for safe numeric widening."""
    widening_pairs = {
        (pa.int8(), pa.int16()),
        (pa.int8(), pa.int32()),
        (pa.int8(), pa.int64()),
        (pa.int16(), pa.int32()),
        (pa.int16(), pa.int64()),
        (pa.int32(), pa.int64()),
        (pa.float32(), pa.float64()),
    }
    return (old, new) in widening_pairs


def check_schema_compatibility(schema_old: pa.Schema, schema_new: pa.Schema) -> dict:
    """
    Compare two pyarrow schemas. Return:
      { compatible: bool,
        breaking_changes: list[str],
        safe_changes: list[str],
        removed_columns: list[str],
        added_columns: list[str] }
    """
    old_fields = {field.name: field for field in schema_old}
    new_fields = {field.name: field for field in schema_new}

    breaking_changes: list[str] = []
    safe_changes: list[str] = []
    removed_columns: list[str] = []
    added_columns: list[str] = []

    for col_name, old_field in old_fields.items():
        if col_name not in new_fields:
            removed_columns.append(col_name)
            breaking_changes.append(f"column '{col_name}' removed")

    for col_name, new_field in new_fields.items():
        if col_name not in old_fields:
            added_columns.append(col_name)
            if new_field.nullable:
                safe_changes.append(f"added nullable column '{col_name}'")
            else:
                breaking_changes.append(f"added required column '{col_name}'")

    for col_name, old_field in old_fields.items():
        if col_name in new_fields:
            new_field = new_fields[col_name]
            if old_field.type != new_field.type:
                if is_widening(old_field.type, new_field.type):
                    safe_changes.append(
                        f"column '{col_name}' widened {old_field.type} → {new_field.type}"
                    )
                else:
                    breaking_changes.append(
                        f"column '{col_name}' type changed {old_field.type} → {new_field.type}"
                    )

    return {
        "compatible": len(breaking_changes) == 0,
        "breaking_changes": breaking_changes,
        "safe_changes": safe_changes,
        "removed_columns": removed_columns,
        "added_columns": added_columns,
    }


def demonstrate_breaking_change(output_dir: Path) -> None:
    """
    Show safe add-column read and breaking type-conflict read.
    """
    base_path = output_dir / "schema_breaking"
    _fresh_dir(base_path)

    safe_path = base_path / "safe"
    safe_path.mkdir(parents=True, exist_ok=True)

    df_safe_v1 = pd.DataFrame(
        {
            "device_id": [f"device_{i:04d}" for i in range(1_000)],
            "value": np.random.random(1_000).astype("float64"),
        }
    )
    df_safe_v2 = pd.DataFrame(
        {
            "device_id": [f"device_{i:04d}" for i in range(1_000, 2_000)],
            "value": np.random.random(1_000).astype("float64"),
            "unit": ["C"] * 1_000,
        }
    )

    pq.write_table(pa.Table.from_pandas(df_safe_v1, preserve_index=False), safe_path / "part-v1.parquet")
    pq.write_table(pa.Table.from_pandas(df_safe_v2, preserve_index=False), safe_path / "part-v2.parquet")

    print("\nSCENARIO A — SAFE: added nullable column")
    safe_schema = pa.schema(
        [
            pa.field("device_id", pa.string()),
            pa.field("value", pa.float64()),
            pa.field("unit", pa.string()),
        ]
    )
    safe_dataset = ds.dataset(safe_path, format="parquet", schema=safe_schema)
    safe_df = safe_dataset.to_table().to_pandas()
    print(f"Read success: {len(safe_df):,} rows")
    print("Null counts:")
    print(safe_df.isnull().sum())

    breaking_path = base_path / "breaking"
    breaking_path.mkdir(parents=True, exist_ok=True)

    df_break_v1 = pd.DataFrame({"value": np.random.random(1_000).astype("float64")})
    df_break_v2 = pd.DataFrame({"value": ["bad"] * 1_000})

    pq.write_table(pa.Table.from_pandas(df_break_v1, preserve_index=False), breaking_path / "part-float.parquet")
    pq.write_table(pa.Table.from_pandas(df_break_v2, preserve_index=False), breaking_path / "part-string.parquet")

    print("\nSCENARIO B — BREAKING: value changed float64 → string")
    try:
        forced_schema = pa.schema([pa.field("value", pa.float64())])
        breaking_dataset = ds.dataset(breaking_path, format="parquet", schema=forced_schema)
        breaking_dataset.to_table().to_pandas()
        print("Unexpected success: this PyArrow version coerced the data.")
    except (pa.ArrowInvalid, pa.ArrowNotImplementedError, pa.ArrowTypeError, Exception) as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}")
        print(
            "\nThis is why you need Delta Lake or Apache Iceberg for column renames "
            "and type changes — Parquet alone has no schema registry or transaction log."
        )


def explain_iceberg_vs_parquet_evolution() -> None:
    """
    Print formatted comparison table.
    """
    print(
        """
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
    )


def main() -> None:
    out = get_output_dir()

    print("\n=== WRITE 3 SCHEMA VERSIONS ===")
    v1 = write_v1_schema(out)
    v2 = write_v2_schema_add_column(out)
    v3 = write_v3_schema_widen_type(out)

    print("\n=== SCHEMA MERGE READ ===")
    evo_dir = out / "schema_evolution"
    df_merged = read_with_schema_merge(evo_dir)
    print(f"Merged rows: {len(df_merged):,}  Columns: {list(df_merged.columns)}")

    print("\n=== COMPATIBILITY CHECK ===")
    s1 = pq.read_schema(v1)
    s2 = pq.read_schema(v2)
    s3 = pq.read_schema(v3)

    print("v1 → v2:")
    print(check_schema_compatibility(s1, s2))

    print("\nv1 → v3:")
    print(check_schema_compatibility(s1, s3))

    print("\n=== BREAKING CHANGE DEMO ===")
    demonstrate_breaking_change(out)

    print("\n=== ICEBERG vs PARQUET EVOLUTION ===")
    explain_iceberg_vs_parquet_evolution()


if __name__ == "__main__":
    main()