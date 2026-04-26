# ============================================================
# Topic   : Parquet for Data Engineers
# File    : test_capstone.py
# Covers  : Pytest validation for the Parquet capstone pipeline
# Prereqs : pip install pyarrow pandas duckdb pytest
# Run     : pytest capstone/test_capstone.py -v
# ============================================================

from __future__ import annotations

import os
from pathlib import Path

import duckdb
import pandas as pd
import pyarrow.parquet as pq
import pytest


def get_output_dir() -> Path:
    """Resolve OUTPUT_DIR the same way as the study files."""
    default = Path("C:/tmp/studybook/parquet/") if os.name == "nt" else Path("/tmp/studybook/parquet/")
    return Path(os.getenv("OUTPUT_DIR", str(default)))


OUTPUT_DIR = get_output_dir()

CAPSTONE_DIR = OUTPUT_DIR / "capstone_single_file"
RAW_DIR = CAPSTONE_DIR / "raw"
PARTITIONED_DIR = CAPSTONE_DIR / "partitioned_zstd"
SMALL_FILES_DIR = CAPSTONE_DIR / "small_files"
COMPACTED_DIR = CAPSTONE_DIR / "compacted"

RAW_CSV = RAW_DIR / "iot_raw.csv"
RAW_PARQUET = RAW_DIR / "iot_raw_snappy.parquet"


@pytest.fixture(scope="session")
def raw_df() -> pd.DataFrame:
    """Load the raw SNAPPY Parquet file once."""
    assert RAW_PARQUET.exists(), (
        f"Run capstone first: {RAW_PARQUET} not found. "
        "Example: python capstone/06_parquet_capstone_pipeline.py"
    )
    return pd.read_parquet(RAW_PARQUET)


@pytest.fixture(scope="session")
def duckdb_con():
    """DuckDB connection with a view over the partitioned dataset."""
    assert PARTITIONED_DIR.exists(), (
        f"Run capstone first: {PARTITIONED_DIR} not found. "
        "Example: python capstone/06_parquet_capstone_pipeline.py"
    )

    glob = str(PARTITIONED_DIR / "**" / "*.parquet").replace("\\", "/")

    con = duckdb.connect()
    con.execute(
        f"""
        CREATE OR REPLACE VIEW iot_partitioned AS
        SELECT *
        FROM read_parquet('{glob}', hive_partitioning=true)
        """
    )

    yield con
    con.close()


def parquet_dir_size(path: Path) -> int:
    """Return total bytes for all Parquet files under a directory."""
    return sum(f.stat().st_size for f in path.rglob("*.parquet"))


def parquet_row_count(path: Path) -> int:
    """Return total row count for all Parquet files under a directory."""
    return sum(pq.read_metadata(f).num_rows for f in path.rglob("*.parquet"))


def test_raw_files_exist():
    """Capstone should create both raw CSV and raw Parquet outputs."""
    assert RAW_CSV.exists(), f"Missing raw CSV: {RAW_CSV}"
    assert RAW_PARQUET.exists(), f"Missing raw Parquet: {RAW_PARQUET}"


def test_raw_dataset_has_expected_row_count(raw_df: pd.DataFrame):
    """The capstone generates 1,000,000 rows by default."""
    assert len(raw_df) == 1_000_000


def test_required_columns_present(raw_df: pd.DataFrame):
    """The capstone dataset should contain all required analytics columns."""
    required = {
        "device_id",
        "plant_id",
        "sensor_type",
        "value",
        "unit",
        "ts",
        "anomaly_flag",
        "year",
        "month",
        "day",
    }

    missing = required - set(raw_df.columns)
    assert not missing, f"Missing columns: {missing}"


def test_anomaly_rate_is_reasonable(raw_df: pd.DataFrame):
    """Anomalies should be rare but present."""
    rate = raw_df["anomaly_flag"].mean()
    assert 0.01 <= rate <= 0.05, f"Unexpected anomaly rate: {rate:.4f}"


def test_parquet_smaller_than_csv():
    """SNAPPY Parquet should be much smaller than raw CSV."""
    csv_size = RAW_CSV.stat().st_size
    parquet_size = RAW_PARQUET.stat().st_size

    assert parquet_size < csv_size, (
        f"Expected Parquet smaller than CSV. "
        f"CSV={csv_size / 1e6:.2f} MB, Parquet={parquet_size / 1e6:.2f} MB"
    )


def test_partitioned_dataset_exists_and_has_hive_layout():
    """Optimized dataset should use Hive-style partition folders."""
    assert PARTITIONED_DIR.exists(), f"Missing partitioned dir: {PARTITIONED_DIR}"

    parquet_files = list(PARTITIONED_DIR.rglob("*.parquet"))
    assert parquet_files, "No Parquet files found in partitioned dataset"

    paths = [str(p) for p in parquet_files]
    assert any("plant_id=plant_A" in p for p in paths)
    assert any("year=" in p for p in paths)
    assert any("month=" in p for p in paths)


def test_partition_filter_returns_only_requested_plant(duckdb_con):
    """Filtering plant_A should return only plant_A rows."""
    result = duckdb_con.execute(
        """
        SELECT DISTINCT plant_id
        FROM iot_partitioned
        WHERE plant_id = 'plant_A'
        ORDER BY plant_id
        """
    ).fetchdf()

    assert len(result) == 1
    assert result["plant_id"].iloc[0] == "plant_A"


def test_partitioned_dataset_contains_all_plants(duckdb_con):
    """The partitioned dataset should include all three plants."""
    result = duckdb_con.execute(
        """
        SELECT DISTINCT plant_id
        FROM iot_partitioned
        ORDER BY plant_id
        """
    ).fetchdf()

    assert set(result["plant_id"].tolist()) == {"plant_A", "plant_B", "plant_C"}


def test_sensor_aggregation_returns_four_sensor_types(duckdb_con):
    """A core analytics query should return all four sensor types."""
    result = duckdb_con.execute(
        """
        SELECT sensor_type, AVG(value) AS avg_value
        FROM iot_partitioned
        WHERE plant_id = 'plant_A'
        GROUP BY sensor_type
        ORDER BY sensor_type
        """
    ).fetchdf()

    assert len(result) == 4
    assert set(result["sensor_type"].tolist()) == {
        "humidity",
        "pressure",
        "temperature",
        "vibration",
    }


def test_partitioned_rows_match_raw_rows(raw_df: pd.DataFrame):
    """Partitioned output should preserve all rows."""
    assert PARTITIONED_DIR.exists(), f"Missing partitioned dir: {PARTITIONED_DIR}"

    partitioned_rows = parquet_row_count(PARTITIONED_DIR)
    assert partitioned_rows == len(raw_df), (
        f"Row count mismatch: raw={len(raw_df):,}, "
        f"partitioned={partitioned_rows:,}"
    )


def test_small_files_and_compacted_outputs_exist():
    """Capstone should create both small files and compacted output."""
    assert SMALL_FILES_DIR.exists(), f"Missing small files dir: {SMALL_FILES_DIR}"
    assert COMPACTED_DIR.exists(), f"Missing compacted dir: {COMPACTED_DIR}"

    assert list(SMALL_FILES_DIR.glob("*.parquet")), "No small Parquet files found"
    assert list(COMPACTED_DIR.glob("*.parquet")), "No compacted Parquet files found"


def test_compaction_reduces_file_count_and_preserves_rows():
    """Compaction should reduce file count while preserving row count."""
    small_files = list(SMALL_FILES_DIR.glob("*.parquet"))
    compacted_files = list(COMPACTED_DIR.glob("*.parquet"))

    assert len(small_files) > len(compacted_files), (
        f"Expected fewer compacted files. "
        f"small={len(small_files)}, compacted={len(compacted_files)}"
    )

    small_rows = parquet_row_count(SMALL_FILES_DIR)
    compacted_rows = parquet_row_count(COMPACTED_DIR)

    assert small_rows == compacted_rows, (
        f"Row count mismatch after compaction: "
        f"small={small_rows:,}, compacted={compacted_rows:,}"
    )


def test_compaction_reduces_or_maintains_total_size():
    """
    Compaction should usually reduce total size because metadata overhead drops.
    Allow equality to avoid failing on codec/version-specific edge cases.
    """
    small_size = parquet_dir_size(SMALL_FILES_DIR)
    compacted_size = parquet_dir_size(COMPACTED_DIR)

    assert compacted_size <= small_size, (
        f"Expected compacted size <= small file size. "
        f"small={small_size / 1e6:.2f} MB, "
        f"compacted={compacted_size / 1e6:.2f} MB"
    )