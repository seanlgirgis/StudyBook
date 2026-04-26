# ============================================================
# Topic   : Python Logging for Data Engineers
# File    : capstone/test_pipeline_logger.py
# Covers  : Pytest coverage for the reusable pipeline_logger library
# Prereqs : pip install structlog python-json-logger pytest
# Run     : pytest test_pipeline_logger.py -v
# ============================================================

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import pytest

sys.path.insert(0, str(Path(__file__).parent))

from pipeline_logger import (  # noqa: E402
    get_pipeline_logger,
    log_dataframe_stats,
    log_stage,
)


@pytest.fixture
def tmp_log_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """
    Create an isolated temporary log directory for each test.

    WHY:
        Tests should never depend on a developer's real machine paths or shared
        log files. Isolated temp directories make the tests deterministic and
        safe to run repeatedly.

    Args:
        tmp_path (Path): Pytest temporary path fixture.
        monkeypatch (pytest.MonkeyPatch): Pytest environment patch fixture.

    Returns:
        Path: Temporary log directory.

    Raises:
        OSError: If the directory cannot be created.
    """
    log_dir = tmp_path / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("LOG_DIR", str(log_dir))
    return log_dir


def _read_json_lines(log_file: Path) -> list[dict[str, Any]]:
    """
    Read JSON log records from a log file.

    WHY:
        The capstone logger promises machine-readable logs. Tests should parse
        the actual emitted file instead of only checking console output.

    Args:
        log_file (Path): Log file to parse.

    Returns:
        list[dict[str, Any]]: Parsed JSON records.

    Raises:
        OSError: If the log file cannot be read.
        json.JSONDecodeError: If any log line is not valid JSON.
    """
    records: list[dict[str, Any]] = []

    for line in log_file.read_text(encoding="utf-8").splitlines():
        records.append(json.loads(line))

    return records


def test_run_id_present_in_all_records(tmp_log_dir: Path) -> None:
    """
    Verify run_id is injected into every emitted record.

    WHY:
        Missing run_id breaks production traceability. Every log line from one
        pipeline run must be queryable by the same correlation ID.

    Args:
        tmp_log_dir (Path): Temporary log directory fixture.

    Returns:
        None.

    Raises:
        AssertionError: If any record has the wrong run_id.
    """
    log_file = tmp_log_dir / "test.log"

    logger = get_pipeline_logger(
        pipeline_name="test",
        run_id="abc123",
        environment="test",
        log_file=log_file,
    )

    logger.info("one")
    logger.warning("two")
    logger.error("three")
    logger.info("four")
    logger.warning("five")

    records = _read_json_lines(log_file)

    assert len(records) == 5
    assert all(record["run_id"] == "abc123" for record in records)


def test_stage_logs_duration_on_success(tmp_log_dir: Path, capfd: pytest.CaptureFixture[str]) -> None:
    """
    Verify log_stage writes a completed record with duration_ms.

    WHY:
        Stage duration is one of the most important observability fields in a
        pipeline. It answers where the runtime is going.

    Args:
        tmp_log_dir (Path): Temporary log directory fixture.
        capfd (pytest.CaptureFixture[str]): Captures stdout/stderr.

    Returns:
        None.

    Raises:
        AssertionError: If completed duration is missing or invalid.
    """
    log_file = tmp_log_dir / "stage_success.log"

    logger = get_pipeline_logger(
        pipeline_name="stage-success",
        run_id="stage123",
        environment="test",
        log_file=log_file,
    )

    with log_stage(logger, "my_stage"):
        logger.info("doing work", extra={"stage": "my_stage"})

    capfd.readouterr()

    records = _read_json_lines(log_file)
    completed = [
        record
        for record in records
        if record.get("stage") == "my_stage" and "completed" in record.get("message", "")
    ]

    assert completed
    assert isinstance(completed[0]["duration_ms"], (int, float))
    assert completed[0]["duration_ms"] >= 0


def test_stage_logs_error_on_exception(tmp_log_dir: Path) -> None:
    """
    Verify log_stage logs failure and re-raises the original exception.

    WHY:
        Logging an exception is not enough. Production code must preserve failure
        semantics so orchestration tools, retries, and tests can react correctly.

    Args:
        tmp_log_dir (Path): Temporary log directory fixture.

    Returns:
        None.

    Raises:
        AssertionError: If failure is not logged correctly.
    """
    log_file = tmp_log_dir / "stage_error.log"

    logger = get_pipeline_logger(
        pipeline_name="stage-error",
        run_id="err123",
        environment="test",
        log_file=log_file,
    )

    with pytest.raises(RuntimeError):
        with log_stage(logger, "failing_stage"):
            raise RuntimeError("deliberate failure")

    records = _read_json_lines(log_file)
    error_records = [
        record
        for record in records
        if record.get("level") == "ERROR" and "failed" in record.get("message", "")
    ]

    assert error_records
    assert error_records[0]["stage"] == "failing_stage"
    assert error_records[0]["error_type"] == "RuntimeError"

    serialized = json.dumps(error_records[0])
    assert "RuntimeError" in serialized or "deliberate failure" in serialized


def test_json_output_is_parseable(tmp_log_dir: Path) -> None:
    """
    Verify every emitted log line is valid JSON.

    WHY:
        Structured logging only helps if downstream systems can parse every
        record reliably. One malformed line can break ingestion or dashboards.

    Args:
        tmp_log_dir (Path): Temporary log directory fixture.

    Returns:
        None.

    Raises:
        AssertionError: If the number of parseable records is wrong.
        json.JSONDecodeError: If any line is malformed.
    """
    log_file = tmp_log_dir / "parseable.log"

    logger = get_pipeline_logger(
        pipeline_name="parseable",
        run_id="json123",
        environment="test",
        log_file=log_file,
    )

    logger.info("first")
    logger.warning("second")
    logger.error("third")

    records = _read_json_lines(log_file)

    assert len(records) == 3


def test_pipeline_name_in_all_records(tmp_log_dir: Path) -> None:
    """
    Verify pipeline_name is injected into every emitted record.

    WHY:
        In shared logging systems, many pipelines write to the same aggregator.
        pipeline_name lets teams filter logs to the system they own.

    Args:
        tmp_log_dir (Path): Temporary log directory fixture.

    Returns:
        None.

    Raises:
        AssertionError: If any record has the wrong pipeline_name.
    """
    log_file = tmp_log_dir / "pipeline_name.log"

    logger = get_pipeline_logger(
        pipeline_name="my-etl",
        run_id="pipe123",
        environment="test",
        log_file=log_file,
    )

    logger.info("alpha")
    logger.info("beta")
    logger.warning("gamma")

    records = _read_json_lines(log_file)

    assert len(records) == 3
    assert all(record["pipeline_name"] == "my-etl" for record in records)


def test_log_dataframe_stats_emits_shape(tmp_log_dir: Path) -> None:
    """
    Verify dataframe stats logs row_count and col_count.

    WHY:
        Shape logging catches silent data loss and schema drift after each
        transformation. This is a core data engineering observability pattern.

    Args:
        tmp_log_dir (Path): Temporary log directory fixture.

    Returns:
        None.

    Raises:
        AssertionError: If shape fields are missing.
    """
    log_file = tmp_log_dir / "dataframe_stats.log"

    logger = get_pipeline_logger(
        pipeline_name="stats",
        run_id="stats123",
        environment="test",
        log_file=log_file,
    )

    log_dataframe_stats(
        logger,
        "filter",
        row_count=500,
        col_count=8,
    )

    records = _read_json_lines(log_file)

    matching = [
        record
        for record in records
        if record.get("row_count") == 500 and record.get("col_count") == 8
    ]

    assert matching
    assert matching[0]["stage"] == "filter"