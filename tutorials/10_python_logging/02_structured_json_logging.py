# ============================================================
# Topic   : Python Logging for Data Engineers
# File    : 02_structured_json_logging.py
# Covers  : Structured JSON logging with correlation IDs and log analysis
# Prereqs : pip install structlog python-json-logger
# Run     : python 02_structured_json_logging.py
# ============================================================

from __future__ import annotations

import json
import logging
import os
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from pythonjsonlogger import jsonlogger


# =========================
# Core Utilities
# =========================

def get_log_dir() -> Path:
    """
    Return the configured log directory, creating it if needed.

    WHY:
        Cross-platform correctness matters. Logs should go somewhere writable
        and predictable across OSes:

        - Windows     -> %LOCALAPPDATA%/studybook/logs
        - Linux/macOS -> /tmp/studybook/logs

        LOG_DIR still wins when explicitly provided, which is the production-safe
        pattern because schedulers and deployment systems should control runtime paths.

    Args:
        None.

    Returns:
        Path: Directory for logs.

    Raises:
        OSError: If the directory cannot be created.
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


def generate_run_id() -> str:
    """
    Generate a short correlation ID.

    WHY:
        Correlation IDs are the single most important logging practice for
        distributed pipelines. Without them, tracing one request or pipeline run
        across multiple stages, files, services, and retries becomes guesswork.

    Args:
        None.

    Returns:
        str: 8-character hex run ID.

    Raises:
        None.
    """
    return uuid.uuid4().hex[:8]


# =========================
# Logger Creation
# =========================

def _reset_logger(logger: logging.Logger) -> None:
    """
    Remove existing handlers to prevent duplicate logs.

    WHY:
        Logging configuration is global inside a Python process. Re-running setup
        code in tests, notebooks, CLIs, or repeated imports can accidentally add
        duplicate handlers and produce duplicate log lines.

    Args:
        logger (logging.Logger): Logger to clean.

    Returns:
        None.

    Raises:
        None.
    """
    for handler in list(logger.handlers):
        handler.close()
        logger.removeHandler(handler)


def get_json_logger(
    name: str,
    log_file: Path,
    level: int = logging.INFO,
) -> logging.Logger:
    """
    Create a JSON-formatted logger.

    WHY:
        Plain text logs require brittle regex parsing. JSON logs are structured
        records that tools like jq, Splunk, ELK, Datadog, and CloudWatch Logs
        Insights can query without custom parsers.

    Args:
        name (str): Logger name.
        log_file (Path): File path.
        level (int): Logging level.

    Returns:
        logging.Logger: JSON logger.

    Raises:
        OSError: If the log file parent directory cannot be created.
    """
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    _reset_logger(logger)

    logger.setLevel(level)
    logger.propagate = False

    handler = logging.FileHandler(log_file, encoding="utf-8")
    handler.setLevel(level)

    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger


class ContextLoggerAdapter(logging.LoggerAdapter):
    """
    LoggerAdapter that injects persistent context fields.

    WHY:
        Passing extra= on every log call is repetitive and easy to forget.
        LoggerAdapter is the stdlib pattern for attaching stable context like
        run_id, pipeline_name, and environment to every record automatically.
    """

    def process(self, msg: str, kwargs: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        """
        Merge persistent context into each log record.

        WHY:
            This keeps call sites clean while ensuring every emitted record has
            the fields required for production traceability.

        Args:
            msg (str): Original log message.
            kwargs (dict[str, Any]): Logging keyword arguments.

        Returns:
            tuple[str, dict[str, Any]]: Message and updated logging kwargs.

        Raises:
            None.
        """
        extra = kwargs.setdefault("extra", {})
        extra.update(self.extra)
        return msg, kwargs


def get_contextual_logger(
    name: str,
    log_file: Path,
    run_id: str,
    pipeline_name: str,
    environment: str,
) -> logging.LoggerAdapter:
    """
    Create a JSON logger with persistent run context.

    WHY:
        Contextual logging avoids repeating metadata on every call. In real data
        pipelines, every record should answer: which run, which pipeline, which
        environment, and what happened?

    Args:
        name (str): Logger name.
        log_file (Path): Log file path.
        run_id (str): Correlation ID.
        pipeline_name (str): Pipeline name.
        environment (str): Environment name.

    Returns:
        logging.LoggerAdapter: LoggerAdapter with persistent context.

    Raises:
        OSError: If the log file parent directory cannot be created.
    """
    base_logger = get_json_logger(name, log_file)

    return ContextLoggerAdapter(
        base_logger,
        {
            "run_id": run_id,
            "pipeline_name": pipeline_name,
            "environment": environment,
        },
    )


# =========================
# Logging Helpers
# =========================

def log_with_extra(
    logger: logging.Logger | logging.LoggerAdapter,
    level: str,
    message: str,
    **fields: Any,
) -> None:
    """
    Emit a structured log with dynamic event-specific fields.

    WHY:
        Persistent context belongs on every record, but fields like latency_ms,
        stage, record_count, and error_type are event-specific. This helper keeps
        structured logging consistent while avoiding repetitive boilerplate.

    Args:
        logger (logging.Logger | logging.LoggerAdapter): Logger or adapter.
        level (str): Level name such as info, debug, warning, error, or critical.
        message (str): Log message.
        **fields (Any): Extra structured fields for this event.

    Returns:
        None.

    Raises:
        ValueError: If level is not a valid logger method.
    """
    normalized_level = level.lower()

    log_method = getattr(logger, normalized_level, None)
    if log_method is None or not callable(log_method):
        raise ValueError(f"Invalid log level: {level}")

    log_method(message, extra=fields)


# =========================
# Log Analysis
# =========================

def parse_json_log_file(log_file: Path) -> list[dict[str, Any]]:
    """
    Parse a JSON log file into Python dictionaries.

    WHY:
        Production debugging often means asking questions of logs, not reading
        every line manually. Parsing logs into records enables summaries, tests,
        audits, dashboards, and incident analysis.

    Args:
        log_file (Path): File to parse.

    Returns:
        list[dict[str, Any]]: Parsed log records. Malformed lines are skipped.

    Raises:
        OSError: If the log file cannot be read.
    """
    records: list[dict[str, Any]] = []

    if not log_file.exists():
        return records

    for line in log_file.read_text(encoding="utf-8").splitlines():
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue

    return records


def _parse_logging_timestamp(value: str) -> float:
    """
    Convert logging's default timestamp string to epoch seconds.

    WHY:
        logging.Formatter uses timestamps like '2026-04-26 03:23:09,084'.
        time.strptime does not support %f reliably for this format because %f
        is a datetime directive. datetime.strptime correctly parses the
        millisecond component, which makes duration_ms accurate.

    Args:
        value (str): Timestamp string from the JSON log record.

    Returns:
        float: Epoch seconds.

    Raises:
        ValueError: If the timestamp cannot be parsed.
    """
    parsed = datetime.strptime(value, "%Y-%m-%d %H:%M:%S,%f")
    return parsed.timestamp()


def summarize_run(log_file: Path, run_id: str) -> dict[str, Any]:
    """
    Summarize one pipeline run from a JSON log file.

    WHY:
        Engineers rarely inspect production logs line by line. A useful summary
        quickly answers: how many events occurred, what levels appeared, what
        errors happened, and roughly how long the run took.

    Args:
        log_file (Path): Log file.
        run_id (str): Correlation ID to summarize.

    Returns:
        dict[str, Any]: Summary containing counts, errors, and duration_ms.

    Raises:
        OSError: If the log file cannot be read.
    """
    records = parse_json_log_file(log_file)
    filtered = [record for record in records if record.get("run_id") == run_id]

    if not filtered:
        return {
            "run_id": run_id,
            "total_events": 0,
            "by_level": {},
            "errors": [],
            "duration_ms": 0.0,
        }

    by_level: dict[str, int] = {}
    errors: list[str] = []
    timestamps: list[float] = []

    for record in filtered:
        level = str(record.get("levelname", "UNKNOWN"))
        by_level[level] = by_level.get(level, 0) + 1

        if level == "ERROR":
            errors.append(str(record.get("message", "")))

        raw_timestamp = record.get("asctime")
        if isinstance(raw_timestamp, str):
            try:
                timestamps.append(_parse_logging_timestamp(raw_timestamp))
            except ValueError:
                continue

    duration_ms = 0.0
    if len(timestamps) >= 2:
        duration_ms = round((max(timestamps) - min(timestamps)) * 1000, 3)

    return {
        "run_id": run_id,
        "total_events": len(filtered),
        "by_level": by_level,
        "errors": errors,
        "duration_ms": duration_ms,
    }


# =========================
# Demo Pipeline
# =========================

def run_demo() -> None:
    """
    Simulate a structured logging pipeline and print a run summary.

    WHY:
        This demo shows the full structured logging loop: emit JSON logs with
        context, include dynamic event fields, record exception details, parse
        the file, and produce a machine-generated run summary.

    Args:
        None.

    Returns:
        None.

    Raises:
        OSError: If the log file cannot be written or read.
    """
    log_dir = get_log_dir()
    log_file = log_dir / "02_structured.log"

    run_id = generate_run_id()

    logger = get_contextual_logger(
        "pipeline.json",
        log_file,
        run_id=run_id,
        pipeline_name="user-events",
        environment="dev",
    )

    # Extract stage
    log_with_extra(logger, "info", "extract: connecting", stage="extract")
    time.sleep(0.01)
    log_with_extra(logger, "info", "extract: fetching data", stage="extract")
    time.sleep(0.01)
    log_with_extra(
        logger,
        "warning",
        "extract: slow response",
        stage="extract",
        latency_ms=1200,
    )
    time.sleep(0.01)
    log_with_extra(logger, "info", "extract: done", stage="extract", records_out=5000)

    # Transform stage
    time.sleep(0.01)
    log_with_extra(logger, "info", "transform: validating", stage="transform")
    time.sleep(0.01)
    log_with_extra(logger, "info", "transform: deduplicating", stage="transform")
    time.sleep(0.01)
    log_with_extra(logger, "info", "transform: enriching", stage="transform")

    try:
        raise ValueError("bad record encountered")
    except ValueError as exc:
        logger.error(
            "transform failed",
            exc_info=True,
            extra={
                "stage": "transform",
                "error_type": type(exc).__name__,
                "error_msg": str(exc),
            },
        )

    time.sleep(0.01)
    log_with_extra(logger, "info", "transform: done", stage="transform", records_out=4988)

    # Load stage
    time.sleep(0.01)
    log_with_extra(logger, "info", "load: writing output", stage="load")
    time.sleep(0.01)
    log_with_extra(logger, "info", "load: done", stage="load", records_loaded=4988)

    summary = summarize_run(log_file, run_id)

    print("\n--- Pipeline Summary ---")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    run_demo()