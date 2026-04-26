# ============================================================
# Topic   : Python Logging for Data Engineers
# File    : capstone/example_pipeline.py
# Covers  : Example ETL pipeline using pipeline_logger library
# Prereqs : pip install structlog python-json-logger
# Run     : python example_pipeline.py
# ============================================================

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any

# ---- Import capstone library (portable across tutorials) ----
sys.path.insert(0, str(Path(__file__).parent))
from pipeline_logger import (  # noqa: E402
    get_pipeline_logger,
    log_stage,
    log_dataframe_stats,
    generate_run_id,
    get_log_dir,
)


# =========================
# Pipeline Stages
# =========================

def extract(logger) -> list[dict[str, Any]]:
    """
    Simulate data extraction.

    WHY:
        Extraction logs must show volume and latency. This is where upstream
        issues first appear.

    Args:
        logger: PipelineLogger

    Returns:
        list[dict]: synthetic records
    """
    with log_stage(logger, "extract") as log:
        time.sleep(0.05)

        records = [{"id": i, "value": i * 10} for i in range(1000)]

        log_dataframe_stats(
            log,
            stage_name="extract",
            row_count=1000,
            col_count=2,
        )

        return records


def validate(logger, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Simulate validation stage.

    WHY:
        Validation is where silent data loss often happens. Logging before/after
        counts is critical.

    Args:
        logger: PipelineLogger
        records: input data

    Returns:
        list[dict]: cleaned records
    """
    with log_stage(logger, "validate") as log:
        time.sleep(0.05)

        # Inject 30 bad records
        for i in range(30):
            records[i]["value"] = None

        before = len(records)
        cleaned = [r for r in records if r["value"] is not None]
        after = len(cleaned)

        log_dataframe_stats(
            log,
            stage_name="validate",
            row_count=after,
            col_count=2,
        )

        return cleaned


def transform(logger, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Simulate transformation stage.

    WHY:
        Transform steps often add computed fields and can be slow.

    Args:
        logger: PipelineLogger
        records: input data

    Returns:
        list[dict]: transformed records
    """
    with log_stage(logger, "transform") as log:
        time.sleep(0.1)

        transformed = [
            {**r, "computed": r["value"] * 2}
            for r in records
        ]

        log_dataframe_stats(
            log,
            stage_name="transform",
            row_count=len(transformed),
            col_count=3,
        )

        return transformed


def load(logger, records: list[dict[str, Any]]) -> int:
    """
    Simulate load stage.

    WHY:
        Load stage must confirm how many records were actually written.

    Args:
        logger: PipelineLogger
        records: data to write

    Returns:
        int: count written
    """
    with log_stage(logger, "load") as log:
        output_file = get_log_dir("capstone") / "example_output.jsonl"

        with output_file.open("w", encoding="utf-8") as f:
            for record in records:
                f.write(json.dumps(record) + "\n")

        log_dataframe_stats(
            log,
            stage_name="load",
            row_count=len(records),
            col_count=len(records[0]) if records else 0,
        )

        return len(records)


# =========================
# Pipeline Runner
# =========================

def _summarize_log(log_file: Path, run_id: str) -> dict[str, Any]:
    """
    Simple log summary.

    WHY:
        Demonstrates post-run analysis similar to file 02.

    Args:
        log_file: log file
        run_id: correlation id

    Returns:
        dict summary
    """
    records = []

    for line in log_file.read_text().splitlines():
        try:
            records.append(json.loads(line))
        except Exception:
            continue

    filtered = [r for r in records if r.get("run_id") == run_id]

    stages = set()
    for r in filtered:
        if "stage" in r:
            stages.add(r["stage"])

    return {
        "run_id": run_id,
        "stages_completed": sorted(stages),
        "total_events": len(filtered),
    }


def run_pipeline() -> None:
    """
    Execute full pipeline.

    WHY:
        Demonstrates real usage of pipeline_logger across stages.
    """
    run_id = generate_run_id()

    log_file = get_log_dir("capstone") / "example_pipeline.log"

    logger = get_pipeline_logger(
        pipeline_name="example-pipeline",
        run_id=run_id,
        environment="dev",
        log_file=log_file,
    )

    records = extract(logger)
    records = validate(logger, records)
    records = transform(logger, records)
    count = load(logger, records)

    print(f"\nLoaded {count} records")

    summary = _summarize_log(log_file, run_id)

    print("\n--- Pipeline Summary ---")
    print(json.dumps(summary, indent=2))

    # ---- Failure demo ----
    try:
        with log_stage(logger, "publish"):
            raise ValueError("Destination unavailable")
    except ValueError:
        print("\nPublish stage failed as expected (check logs)")


# =========================
# Main
# =========================

if __name__ == "__main__":
    run_pipeline()