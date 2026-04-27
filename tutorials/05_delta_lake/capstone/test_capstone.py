# ============================================================
# Topic   : Delta Lake for Data Engineers
# File    : test_capstone.py
# Covers  : pytest validation for CDC capstone
# Prereqs : pip install pytest deltalake pandas pyarrow
# Run     : pytest capstone/test_capstone.py -v
# ============================================================

import shutil
import sys
from pathlib import Path

import pytest
from deltalake import DeltaTable

sys.path.insert(0, str(Path(__file__).parent))

from capstone import (
    TABLE_PATH,
    generate_customers,
    apply_cdc_changes,
    run_day_0,
    run_day_1,
    run_day_2,
    run_optimize_and_vacuum,
)


@pytest.fixture()
def clean_table():
    if TABLE_PATH.exists():
        shutil.rmtree(TABLE_PATH)

    TABLE_PATH.parent.mkdir(parents=True, exist_ok=True)

    yield TABLE_PATH

    if TABLE_PATH.exists():
        shutil.rmtree(TABLE_PATH)


def test_day0_creates_1000_rows_at_version_zero(clean_table):
    run_day_0(clean_table)

    dt = DeltaTable(str(clean_table))
    assert dt.version() == 0
    assert len(dt.to_pandas()) == 1000


def test_day1_cdc_results_in_1030_rows(clean_table):
    run_day_0(clean_table)
    run_day_1(clean_table)

    dt = DeltaTable(str(clean_table))
    assert dt.version() == 3
    assert len(dt.to_pandas()) == 1030


def test_day2_results_in_1042_rows(clean_table):
    run_day_0(clean_table)
    run_day_1(clean_table)
    run_day_2(clean_table)

    dt = DeltaTable(str(clean_table))
    assert dt.version() == 4
    assert len(dt.to_pandas()) == 1042


def test_time_travel_versions_have_expected_row_counts(clean_table):
    run_day_0(clean_table)
    run_day_1(clean_table)
    run_day_2(clean_table)

    expected = {
        0: 1000,
        3: 1030,
        4: 1042,
    }

    for version, expected_rows in expected.items():
        dt = DeltaTable(str(clean_table))
        dt.load_as_version(version)
        assert len(dt.to_pandas()) == expected_rows


def test_transaction_log_exists(clean_table):
    run_day_0(clean_table)

    log_dir = clean_table / "_delta_log"
    assert log_dir.exists()
    assert len(list(log_dir.glob("*.json"))) >= 1


def test_apply_cdc_upsert_is_idempotent_for_row_count(clean_table):
    run_day_0(clean_table)

    updates = generate_customers(
        25,
        seed=99,
        version_ts="2024-01-05",
        start_id=0,
    )

    apply_cdc_changes(clean_table, updates, "upsert")
    rows_after_first = len(DeltaTable(str(clean_table)).to_pandas())

    apply_cdc_changes(clean_table, updates, "upsert")
    rows_after_second = len(DeltaTable(str(clean_table)).to_pandas())

    assert rows_after_first == rows_after_second


def test_delete_removes_expected_rows(clean_table):
    run_day_0(clean_table)

    delete_df = generate_customers(
        10,
        seed=123,
        version_ts="2024-01-05",
        start_id=0,
    )[["customer_id"]]

    result = apply_cdc_changes(clean_table, delete_df, "delete")

    dt = DeltaTable(str(clean_table))
    assert result["deleted"] == 10
    assert len(dt.to_pandas()) == 990


def test_optimize_creates_newer_delta_version(clean_table):
    run_day_0(clean_table)
    run_day_1(clean_table)
    run_day_2(clean_table)

    before_version = DeltaTable(str(clean_table)).version()

    run_optimize_and_vacuum(clean_table)

    after_version = DeltaTable(str(clean_table)).version()

    assert after_version > before_version