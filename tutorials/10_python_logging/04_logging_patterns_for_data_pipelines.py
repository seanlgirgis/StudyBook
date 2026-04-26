# ============================================================
# Topic   : Python Logging for Data Engineers
# File    : 04_logging_patterns_for_data_pipelines.py
# Covers  : Production logging patterns: retry, batch, audit, timing, exceptions
# Prereqs : pip install structlog python-json-logger
# Run     : python 04_logging_patterns_for_data_pipelines.py
# ============================================================

from __future__ import annotations

import json
import logging
import os
import random
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from pythonjsonlogger import jsonlogger


# =========================
# Core Utilities
# =========================

def get_log_dir() -> Path:
    """
    Return cross-platform log directory.

    WHY:
        Same OS-aware logic as earlier files. Logging must always succeed
        regardless of where the code runs.

    Returns:
        Path
    """
    env_dir = os.getenv("LOG_DIR")

    if env_dir:
        log_dir = Path(env_dir)
    else:
        if os.name == "nt":
            base = Path(os.getenv("LOCALAPPDATA", Path.home()))
            log_dir = base / "studybook" / "logs"
        else:
            log_dir = Path("/tmp/studybook/logs")

    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir


# =========================
# Logger Setup
# =========================

def _reset_logger(logger: logging.Logger) -> None:
    for handler in list(logger.handlers):
        handler.close()
        logger.removeHandler(handler)


def get_pipeline_logger(name: str, log_file: Path) -> logging.Logger:
    """
    JSON logger for pipeline.

    WHY:
        Consistent structured logging is mandatory for production observability.
    """
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    _reset_logger(logger)

    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    handler = logging.FileHandler(log_file, encoding="utf-8")
    handler.setFormatter(
        jsonlogger.JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    )

    logger.addHandler(handler)
    return logger


# =========================
# Logging Patterns
# =========================

def log_retry(
    logger: logging.Logger,
    attempt: int,
    max_attempts: int,
    error: Exception,
    next_retry_in_s: float,
) -> None:
    """
    Log retry attempts.

    WHY:
        Without attempt counts and delay info, retries are meaningless in logs.
    """
    level = logging.INFO if attempt < max_attempts else logging.ERROR

    logger.log(
        level,
        "retry attempt",
        extra={
            "attempt": attempt,
            "max_attempts": max_attempts,
            "error_type": type(error).__name__,
            "error_msg": str(error),
            "next_retry_in_s": next_retry_in_s,
        },
    )


def log_batch_progress(
    logger: logging.Logger,
    batch_num: int,
    total_batches: int,
    records_done: int,
    records_total: int,
) -> None:
    """
    Log batch progress.

    WHY:
        Long jobs without progress logs look stuck and get killed.
    """
    pct = records_done / records_total * 100
    remaining_batches = total_batches - batch_num

    logger.info(
        "batch progress",
        extra={
            "batch_num": batch_num,
            "total_batches": total_batches,
            "records_done": records_done,
            "records_total": records_total,
            "pct_complete": round(pct, 2),
            "eta_batches_remaining": remaining_batches,
        },
    )


def log_slow_query(
    logger: logging.Logger,
    query_id: str,
    duration_ms: float,
    threshold_ms: float = 1000,
    query_preview: str = "",
) -> None:
    """
    Log slow queries.

    WHY:
        1% of queries usually cause 80% of latency.
    """
    if duration_ms > threshold_ms:
        logger.warning(
            "slow query detected",
            extra={
                "query_id": query_id,
                "duration_ms": duration_ms,
                "threshold_ms": threshold_ms,
                "query_preview": query_preview[:100],
            },
        )


def log_pipeline_audit(
    logger: logging.Logger,
    stage: str,
    run_id: str,
    input_count: int,
    output_count: int,
    dropped_count: int,
    duration_ms: float,
) -> None:
    """
    Audit log per stage.

    WHY:
        Answers: "where did my data go?"
    """
    logger.info(
        "pipeline audit",
        extra={
            "stage": stage,
            "run_id": run_id,
            "input_count": input_count,
            "output_count": output_count,
            "dropped_count": dropped_count,
            "duration_ms": duration_ms,
        },
    )


@contextmanager
def operation_timer(logger: logging.Logger, operation_name: str) -> Generator[None, None, None]:
    """
    Context manager for timing operations.

    WHY:
        Eliminates repetitive try/except/finally blocks.
    """
    start = time.time()
    logger.info(f"{operation_name} started")

    try:
        yield
        duration = (time.time() - start) * 1000
        logger.info(f"{operation_name} completed", extra={"duration_ms": round(duration, 2)})
    except Exception as exc:
        duration = (time.time() - start) * 1000
        logger.error(
            f"{operation_name} failed",
            extra={"duration_ms": round(duration, 2)},
            exc_info=True,
        )
        raise


def setup_performance_logger(name: str, perf_log_file: Path) -> logging.Logger:
    """
    Separate performance logger.

    WHY:
        Mixing timing logs with business logs creates noise.
    """
    perf_logger = logging.getLogger(f"{name}.performance")
    _reset_logger(perf_logger)

    perf_logger.setLevel(logging.INFO)
    perf_logger.propagate = False

    handler = logging.FileHandler(perf_log_file, encoding="utf-8")
    handler.setFormatter(jsonlogger.JsonFormatter())

    perf_logger.addHandler(handler)
    return perf_logger


# =========================
# Demo Pipeline
# =========================

def run_demo() -> None:
    """
    Simulate full ETL pipeline with logging patterns.
    """
    log_dir = get_log_dir()
    log_file = log_dir / "04_patterns.log"

    logger = get_pipeline_logger("pipeline.patterns", log_file)

    run_id = "demo-run"

    # ---- Extract with retries ----
    for attempt in range(1, 4):
        try:
            if attempt < 3:
                raise ConnectionError("temporary network issue")
            logger.info("extract succeeded")
        except ConnectionError as e:
            log_retry(logger, attempt, 3, e, next_retry_in_s=2.0)

    # ---- Transform batching ----
    total_batches = 8
    total_records = 8000

    for batch in range(1, total_batches + 1):
        records_done = batch * 1000
        log_batch_progress(logger, batch, total_batches, records_done, total_records)

        duration = random.uniform(100, 800)
        log_slow_query(logger, f"q-{batch}", duration, threshold_ms=500)

    # ---- Load audit ----
    log_pipeline_audit(
        logger,
        stage="load",
        run_id=run_id,
        input_count=8000,
        output_count=7850,
        dropped_count=150,
        duration_ms=1200,
    )

    # ---- Exception demo ----
    try:
        with operation_timer(logger, "publish"):
            raise ValueError("destination unavailable")
    except ValueError:
        pass

    # ---- Summary ----
    records = []
    for line in log_file.read_text().splitlines():
        try:
            records.append(json.loads(line))
        except Exception:
            continue

    level_counts = {}
    for r in records:
        lvl = r.get("levelname", "UNKNOWN")
        level_counts[lvl] = level_counts.get(lvl, 0) + 1

    print("\n--- Log Summary ---")
    print(level_counts)


if __name__ == "__main__":
    run_demo()