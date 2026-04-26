# ============================================================
# Topic   : Python Logging for Data Engineers
# File    : 03_structlog_advanced.py
# Covers  : Advanced structured logging with structlog (processors, context, prod vs dev)
# Prereqs : pip install structlog python-json-logger
# Run     : python 03_structlog_advanced.py
# ============================================================

from __future__ import annotations

import logging
import os
import sys
import time
from pathlib import Path
from typing import Any

import structlog


# =========================
# Core Utilities
# =========================

def get_log_dir() -> Path:
    """
    Return the configured log directory, creating it if needed.

    WHY:
        Same cross-platform strategy as earlier files:
        - Windows     → LOCALAPPDATA
        - Linux/macOS → /tmp
        This keeps behavior predictable and avoids permission issues.

    Returns:
        Path: Directory for logs.
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
# Custom Processor
# =========================

def add_duration_processor(
    logger: Any,
    method_name: str,
    event_dict: dict[str, Any],
) -> dict[str, Any]:
    """
    Add duration_ms if start_time exists.

    WHY:
        Structlog processors allow injecting computed fields globally without
        changing every log call. This is far more scalable than manual timing.

    Args:
        logger: structlog logger (unused, required by signature)
        method_name (str): log level name
        event_dict (dict): event data

    Returns:
        dict: enriched event data
    """
    start_time = event_dict.get("start_time")

    if start_time is not None:
        duration_ms = (time.time() - start_time) * 1000
        event_dict["duration_ms"] = round(duration_ms, 3)

    return event_dict


# =========================
# Structlog Configuration
# =========================

def configure_structlog_prod(log_file: Path) -> None:
    """
    Configure structlog for production JSON logging.

    WHY:
        Production systems require machine-readable logs.
        structlog separates configuration (processors) from usage.

    Args:
        log_file (Path): Output file path.
    """
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            add_duration_processor,
            structlog.processors.add_log_level,
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def configure_structlog_dev() -> None:
    """
    Configure structlog for development console output.

    WHY:
        Developers need readable logs, not dense JSON blobs.

    Args:
        None.
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.TimeStamper(fmt="%H:%M:%S"),
            structlog.processors.add_log_level,
            structlog.dev.ConsoleRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


# =========================
# Logger Creation
# =========================

def get_bound_logger(
    name: str,
    **initial_context: Any,
) -> structlog.stdlib.BoundLogger:
    """
    Return a bound structlog logger.

    WHY:
        Binding context once ensures every log automatically includes metadata
        like pipeline_name, environment, etc.

    Args:
        name (str): logger name
        **initial_context: key-value metadata

    Returns:
        BoundLogger
    """
    return structlog.get_logger(name).bind(**initial_context)


# =========================
# Demonstrations
# =========================

def demonstrate_context_binding(logger: structlog.stdlib.BoundLogger) -> None:
    """
    Demonstrate binding/unbinding context.

    WHY:
        Context evolution is critical in pipelines where jobs spawn sub-jobs.

    Args:
        logger: structlog logger
    """
    print("\n--- demonstrate_context_binding() ---")

    job_logger = logger.bind(job_id="j-001")
    job_logger.info("job started")

    job_logger = job_logger.bind(task="dedupe")
    job_logger.info("task running")

    job_logger = job_logger.unbind("job_id")
    job_logger.info("job_id removed")

    # contextvars example
    structlog.contextvars.bind_contextvars(request_id="req-123")
    logger.info("contextvars applied")
    structlog.contextvars.clear_contextvars()


def log_dataframe_operation(
    logger: structlog.stdlib.BoundLogger,
    operation: str,
    input_rows: int,
    output_rows: int,
    duration_ms: float,
) -> None:
    """
    Log a dataframe transformation.

    WHY:
        Structured logs make it easy to answer:
        - How many rows were dropped?
        - Which step caused data loss?
        - Where is the pipeline slow?

    Args:
        logger: structlog logger
        operation (str)
        input_rows (int)
        output_rows (int)
        duration_ms (float)
    """
    dropped = input_rows - output_rows
    drop_pct = (dropped / input_rows * 100) if input_rows else 0

    logger.info(
        "dataframe_op",
        operation=operation,
        input_rows=input_rows,
        output_rows=output_rows,
        rows_dropped=dropped,
        drop_pct=round(drop_pct, 2),
        duration_ms=duration_ms,
    )


# =========================
# Demo Pipeline
# =========================

def run_demo() -> None:
    """
    Run structlog demonstration pipeline.

    WHY:
        Shows both production JSON logs and developer-friendly logs.
    """
    log_dir = get_log_dir()
    log_file = log_dir / "03_structlog_prod.json"

    # ---- Production mode ----
    configure_structlog_prod(log_file)

    logger = get_bound_logger(
        "pipeline.structlog",
        pipeline_name="iot-ingest",
        environment="dev",
    )

    operations = [
        ("filter", 10000, 9500, 12.5),
        ("dedupe", 9500, 9100, 18.2),
        ("enrich", 9100, 9100, 25.0),
        ("aggregate", 9100, 120, 30.1),
    ]

    for op, inp, out, dur in operations:
        log_dataframe_operation(logger, op, inp, out, dur)

    demonstrate_context_binding(logger)

    # ---- Dev mode ----
    print("\n--- Switching to DEV mode ---\n")
    configure_structlog_dev()

    dev_logger = get_bound_logger(
        "pipeline.structlog.dev",
        pipeline_name="iot-ingest",
        environment="dev",
    )

    for op, inp, out, dur in operations[:2]:
        log_dataframe_operation(dev_logger, op, inp, out, dur)

    print(f"\nCheck log file: {log_file}")


# =========================
# Main
# =========================

if __name__ == "__main__":
    run_demo()