# ============================================================
# Topic   : Python Concurrency for Data Engineers
# File    : test_capstone.py
# Covers  : pytest validation for concurrent IoT ingestion capstone
# Prereqs : pip install aiohttp aiofiles pyarrow pandas pytest
# Run     : pytest test_capstone.py -v
# ============================================================

from __future__ import annotations

import threading
import time

import pyarrow.parquet as pq
import pytest

from simulate_sources import ENDPOINTS
from pipeline import (
    OUTPUT_DIR,
    PARQUET_SCHEMA,
    TokenBucketRateLimiter,
    enrich_record,
    retry_with_jitter,
    run_pipeline,
)


@pytest.fixture(scope="session")
def pipeline_stats():
    """Run the full pipeline once for the whole test session."""
    return run_pipeline(max_rps=20.0)


@pytest.fixture(scope="session")
def output_parquet(pipeline_stats):
    path = OUTPUT_DIR / "capstone" / "results.parquet"
    assert path.exists(), f"Pipeline must write results.parquet: {path} not found"
    return pq.read_table(path)


def test_pipeline_completes_all_50_endpoints(pipeline_stats):
    """total_endpoints must equal 50."""
    assert pipeline_stats["total_endpoints"] == 50


def test_pipeline_runs_under_10_seconds(pipeline_stats):
    """
    50 endpoints × average latency of ~1s sequential = ~50s.
    Concurrent pipeline must finish in under 10 seconds.
    """
    total_s = pipeline_stats["total_ms"] / 1000
    assert total_s < 10, f"Pipeline too slow: {total_s:.1f}s (expected < 10s)"


def test_rate_limiter_holds_throughput_below_max_rps():
    """
    Submit 20 instant tasks through rate limiter at max_rps=5.
    Wall time must be >= 20/5 - 0.5 = 3.5 seconds.
    """
    limiter = TokenBucketRateLimiter(max_rps=5.0)
    times = []

    def acquire_and_record():
        limiter.acquire()
        times.append(time.monotonic())

    threads = [threading.Thread(target=acquire_and_record) for _ in range(20)]

    t0 = time.monotonic()

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    elapsed = time.monotonic() - t0

    assert len(times) == 20
    assert elapsed >= 3.5, (
        f"Rate limiter too fast: {elapsed:.2f}s for 20 items at 5 rps "
        f"(expected >= 3.5s)"
    )


def test_retry_attempts_exactly_n_times():
    """retry_with_jitter retries exactly max_attempts times then re-raises."""
    attempt_log = []

    @retry_with_jitter(max_attempts=3, base_delay_s=0.01)
    def always_fails():
        attempt_log.append(1)
        raise ValueError("always fails")

    with pytest.raises(ValueError):
        always_fails()

    assert len(attempt_log) == 3, f"Expected 3 attempts, got {len(attempt_log)}"


def test_pipeline_handles_failures_without_crash(pipeline_stats):
    """
    Fetch failures are caught and logged.
    fetched_ok + fetch_errors must equal total_endpoints.
    """
    assert (
        pipeline_stats["fetched_ok"] + pipeline_stats["fetch_errors"]
        == pipeline_stats["total_endpoints"]
    )


def test_output_parquet_has_correct_schema(output_parquet):
    """Parquet file must contain all 11 required columns."""
    required = {field.name for field in PARQUET_SCHEMA}
    actual = set(output_parquet.schema.names)
    missing = required - actual

    assert not missing, f"Missing columns in output: {missing}"


def test_output_parquet_row_count_matches_fetched_ok(pipeline_stats, output_parquet):
    """records_written in stats must equal row count in Parquet file."""
    parquet_rows = output_parquet.num_rows

    assert parquet_rows == pipeline_stats["records_written"], (
        f"Stats say {pipeline_stats['records_written']} written, "
        f"Parquet has {parquet_rows} rows"
    )


def test_enrich_record_adds_expected_fields():
    """enrich_record should produce the exact fields required by the Parquet schema."""
    record = {
        "endpoint_id": "sensor_test",
        "plant": "plant_A",
        "sensor_type": "temperature",
        "value": 90.0,
        "unit": "C",
        "ts": "2026-04-26T00:00:00+00:00",
        "latency_ms": 123.4,
        "_run_id": "run-123",
    }

    enriched = enrich_record(record)

    assert set(enriched) == {field.name for field in PARQUET_SCHEMA}
    assert enriched["pipeline_run_id"] == "run-123"
    assert enriched["anomaly_flag"] is True
    assert enriched["normalised_value"] == pytest.approx((90.0 - 15.0) / (95.0 - 15.0))


def test_endpoint_fixture_has_50_sources():
    """simulate_sources.ENDPOINTS must define exactly 50 simulated endpoints."""
    assert len(ENDPOINTS) == 50