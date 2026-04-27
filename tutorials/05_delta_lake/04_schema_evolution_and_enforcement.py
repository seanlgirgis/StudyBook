# ============================================================
# Topic   : Delta Lake for Data Engineers
# File    : 04_schema_evolution_and_enforcement.py
# Covers  : Schema enforcement, schema evolution, compatibility checks
# Prereqs : pip install deltalake pandas pyarrow
# Run     : python 04_schema_evolution_and_enforcement.py
# ============================================================

from deltalake import DeltaTable, write_deltalake
import pandas as pd
import pyarrow as pa
from pathlib import Path
import os
import shutil


def get_output_dir() -> Path:
    """Return platform output dir. Create if missing."""
    default = Path("C:/tmp/studybook/delta" if os.name == "nt" else "/tmp/studybook/delta")
    out = Path(os.getenv("OUTPUT_DIR", str(default)))
    out.mkdir(parents=True, exist_ok=True)
    return out


def demonstrate_schema_enforcement(path: Path) -> None:
    """
    Show Delta's default schema enforcement.

    WHY enforcement:
    Raw data lake folders can be corrupted when writers silently introduce
    incompatible schemas. Delta blocks incompatible writes by default.
    """
    print("Current schema:")
    print(DeltaTable(str(path)).schema().to_json())

    df_extra_col = pd.DataFrame(
        {
            "sensor_id": ["s999"],
            "value": [99.9],
            "ts": pd.to_datetime(["2024-01-02 00:00:00"]),
            "firmware_version": ["v1.2.3"],
        }
    )

    try:
        write_deltalake(str(path), df_extra_col, mode="append")
        print("Unexpected: extra-column write succeeded")
    except Exception as exc:
        print("Schema enforcement blocked incompatible write ✓")
        print(f"Extra-column error: {type(exc).__name__}: {exc}")

    df_bad_type = pd.DataFrame(
        {
            "sensor_id": ["s998"],
            "value": ["not-a-float"],
            "ts": pd.to_datetime(["2024-01-02 00:01:00"]),
        }
    )

    try:
        write_deltalake(str(path), df_bad_type, mode="append")
        print("Unexpected: bad-type write succeeded")
    except Exception as exc:
        print("Schema enforcement blocked incompatible type change ✓")
        print(f"Bad-type error: {type(exc).__name__}: {exc}")


def add_column_safely(path: Path, df_with_new_col: pd.DataFrame) -> None:
    """
    Add a nullable column using schema_mode='merge'.

    WHY nullable column:
    Existing rows do not have this value, so Delta fills older rows with null.
    This avoids a full backfill rewrite.
    """
    write_deltalake(
        str(path),
        df_with_new_col,
        mode="append",
        schema_mode="merge",
    )

    dt = DeltaTable(str(path))
    df = dt.to_pandas()

    print(f"Schema evolved successfully at version {dt.version()}")
    print(f"Rows after append: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    print("\nSample rows with firmware_version:")
    print(df[["sensor_id", "value", "firmware_version"]].tail(5).to_string(index=False))


def check_schema_compatibility(schema_old: pa.Schema, schema_new: pa.Schema) -> dict:
    """
    Compare two pyarrow schemas.

    Breaking:
      - removed column
      - incompatible type change
      - narrowing numeric type

    Safe:
      - nullable column added
      - widening numeric type
    """
    old_fields = {field.name: field for field in schema_old}
    new_fields = {field.name: field for field in schema_new}

    added_columns = [name for name in new_fields if name not in old_fields]
    removed_columns = [name for name in old_fields if name not in new_fields]

    breaking_changes: list[str] = []
    safe_changes: list[str] = []

    for name in added_columns:
        if new_fields[name].nullable:
            safe_changes.append(f"Added nullable column: {name}")
        else:
            breaking_changes.append(f"Added non-nullable column without backfill: {name}")

    for name in removed_columns:
        breaking_changes.append(f"Removed column: {name}")

    numeric_widening = {
        pa.int32(): [pa.int64(), pa.float32(), pa.float64()],
        pa.int64(): [pa.float64()],
        pa.float32(): [pa.float64()],
    }

    for name in old_fields.keys() & new_fields.keys():
        old_type = old_fields[name].type
        new_type = new_fields[name].type

        if old_type == new_type:
            continue

        if old_type in numeric_widening and new_type in numeric_widening[old_type]:
            safe_changes.append(f"Widened type for {name}: {old_type} -> {new_type}")
        else:
            breaking_changes.append(f"Incompatible type change for {name}: {old_type} -> {new_type}")

    return {
        "compatible": len(breaking_changes) == 0,
        "breaking_changes": breaking_changes,
        "safe_changes": safe_changes,
        "added_columns": added_columns,
        "removed_columns": removed_columns,
    }


def demonstrate_breaking_change(path: Path) -> None:
    """
    Demonstrate safe and breaking schema changes.

    WHY:
    Delta supports controlled evolution, but it still protects the table from
    unsafe changes that would confuse readers.
    """
    df_safe = pd.DataFrame(
        {
            "sensor_id": ["s_safe"],
            "value": [123.45],
            "ts": pd.to_datetime(["2024-01-03 00:00:00"]),
            "firmware_version": ["v2.0.0"],
        }
    )

    try:
        write_deltalake(str(path), df_safe, mode="append", schema_mode="merge")
        print("SAFE change succeeded: nullable column firmware_version added ✓")
    except Exception as exc:
        print(f"Unexpected safe-change failure: {type(exc).__name__}: {exc}")

    df_breaking = pd.DataFrame(
        {
            "sensor_id": ["s_break"],
            "value": ["now-a-string"],
            "ts": pd.to_datetime(["2024-01-03 00:01:00"]),
            "firmware_version": ["v2.0.1"],
        }
    )

    try:
        write_deltalake(str(path), df_breaking, mode="append")
        print("Unexpected: breaking type change succeeded")
    except Exception as exc:
        print("Type change float64→string is BREAKING.")
        print("Delta blocked the write to protect the table ✓")
        print(f"Breaking-change error: {type(exc).__name__}: {exc}")
        print(
            "Use overwrite/schema replacement only if you intentionally accept "
            "a major table rewrite. For renames/drops, prefer metadata-aware "
            "features such as Delta column mapping or Apache Iceberg."
        )


def explain_iceberg_vs_delta_evolution() -> None:
    """Print comparison table for lakehouse table formats."""
    rows = [
        ("Add nullable column", "SAFE", "SAFE", "SAFE"),
        ("Widen numeric type", "✅ Safe", "✅ Safe", "✅ Safe"),
        ("Rename column", "BREAKING", "SAFE (mapping)", "SAFE (metadata)"),
        ("Drop column", "❌ Breaking", "✅ With column mapping", "✅ Metadata"),
        ("Change incompatible type", "❌", "❌", "❌"),
        ("Time travel", "❌", "✅", "✅"),
        ("ACID transactions", "❌", "✅", "✅"),
        ("Multi-engine support", "✅ Files only", "✅ Growing ecosystem", "✅ Strong multi-engine"),
    ]

    print(f"{'Operation':<28} | {'Raw Parquet':<14} | {'Delta Lake':<22} | {'Apache Iceberg'}")
    print("-" * 92)

    for operation, parquet, delta, iceberg in rows:
        print(f"{operation:<28} | {parquet:<14} | {delta:<22} | {iceberg}")

    print(
        "\nInterview note: Delta Lake gives ACID, time travel, schema enforcement, "
        "and schema evolution on top of Parquet files. Iceberg is especially strong "
        "for metadata-only schema operations across many query engines."
    )


def main():
    path = get_output_dir() / "schema_evo"

    if path.exists():
        shutil.rmtree(path)

    df_v1 = pd.DataFrame(
        {
            "sensor_id": [f"s{i:03d}" for i in range(100)],
            "value": [float(i) for i in range(100)],
            "ts": pd.date_range("2024-01-01", periods=100, freq="1min"),
        }
    )

    write_deltalake(str(path), df_v1, mode="overwrite")

    print("\n=== SCHEMA ENFORCEMENT ===")
    demonstrate_schema_enforcement(path)

    print("\n=== ADD COLUMN SAFELY ===")
    df_v2 = df_v1.copy()
    df_v2["firmware_version"] = "v1.2.3"
    add_column_safely(path, df_v2)

    print("\n=== COMPATIBILITY CHECK ===")
    s1 = pa.schema(
        [
            pa.field("sensor_id", pa.string()),
            pa.field("value", pa.float64()),
        ]
    )

    s2 = pa.schema(
        [
            pa.field("sensor_id", pa.string()),
            pa.field("value", pa.float64()),
            pa.field("firmware_version", pa.string()),
        ]
    )

    result = check_schema_compatibility(s1, s2)
    print(result)

    print("\n=== BREAKING CHANGE DEMO ===")
    demonstrate_breaking_change(path)

    print("\n=== DELTA vs ICEBERG EVOLUTION ===")
    explain_iceberg_vs_delta_evolution()


if __name__ == "__main__":
    main()