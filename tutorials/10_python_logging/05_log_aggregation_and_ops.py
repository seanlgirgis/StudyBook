# ============================================================
# Topic   : Python Logging for Data Engineers
# File    : 05_log_aggregation_and_ops.py
# Covers  : Log rotation, sampling filters, schema contracts, and shipping config snippets
# Prereqs : pip install structlog python-json-logger
# Run     : python 05_log_aggregation_and_ops.py
# ============================================================

from __future__ import annotations

import json
import logging
import os
import random
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

from pythonjsonlogger import jsonlogger


def get_log_dir() -> Path:
    """
    Return the configured log directory, creating it if needed.

    WHY:
        Production logging should be configurable and cross-platform. LOG_DIR
        lets schedulers and deployment tools choose the location, while the
        default stays writable on both Windows and Unix-like systems.

    Args:
        None.

    Returns:
        Path: Directory where log files should be written.

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


def build_rotating_handler(
    log_file: Path,
    max_size_mb: int = 100,
    backup_count: int = 7,
) -> RotatingFileHandler:
    """
    Build a rotating JSON file handler.

    WHY:
        RotatingFileHandler is the right default for pipeline logs because it
        gives bounded disk usage, predictable file names, and avoids time-zone
        edge cases that can affect time-based rotation.

    Args:
        log_file (Path): File path for the active log file.
        max_size_mb (int): Maximum active file size in megabytes.
        backup_count (int): Number of rotated files to keep.

    Returns:
        RotatingFileHandler: Configured rotating handler.

    Raises:
        OSError: If the parent directory cannot be created.
    """
    log_file.parent.mkdir(parents=True, exist_ok=True)

    handler = RotatingFileHandler(
        log_file,
        maxBytes=max_size_mb * 1024 * 1024,
        backupCount=backup_count,
        encoding="utf-8",
    )
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(
        jsonlogger.JsonFormatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s "
            "%(run_id)s %(stage)s %(duration_ms)s %(records_in)s %(records_out)s "
            "%(error_type)s %(query_id)s %(batch_num)s"
        )
    )
    return handler


class SamplingFilter(logging.Filter):
    """
    Filter that samples DEBUG and INFO logs while always keeping WARNING+.

    WHY:
        A busy pipeline can emit hundreds of thousands of DEBUG or INFO lines
        per minute. Sampling preserves statistical visibility without filling
        disks or overwhelming log aggregation systems. WARNING, ERROR, and
        CRITICAL logs must never be sampled away.
    """

    def __init__(self, sample_rate: float = 0.10) -> None:
        """
        Initialize the sampling filter.

        WHY:
            The sample rate should be explicit and tunable. Ten percent is a
            common starting point: enough visibility for trends, much less noise.

        Args:
            sample_rate (float): Fraction of DEBUG/INFO records to keep.

        Returns:
            None.

        Raises:
            ValueError: If sample_rate is outside [0.0, 1.0].
        """
        super().__init__()

        if not 0.0 <= sample_rate <= 1.0:
            raise ValueError("sample_rate must be between 0.0 and 1.0")

        self.sample_rate = sample_rate

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Decide whether a log record should be emitted.

        WHY:
            Sampling low-severity logs reduces volume. Keeping WARNING and above
            guarantees important operational events are never dropped.

        Args:
            record (logging.LogRecord): Candidate log record.

        Returns:
            bool: True if the record should be emitted, False otherwise.

        Raises:
            None.
        """
        if record.levelno >= logging.WARNING:
            return True

        return random.random() < self.sample_rate


def define_log_schema() -> dict[str, Any]:
    """
    Return the JSON schema contract for pipeline log entries.

    WHY:
        A schema contract lets ops, SRE, and data engineering agree on what every
        log line must contain. It becomes the API between pipeline code and the
        monitoring system.

    Args:
        None.

    Returns:
        dict[str, Any]: Simplified schema contract.

    Raises:
        None.
    """
    return {
        "required": {
            "timestamp": "ISO8601 timestamp or logging asctime",
            "level": "Log severity such as INFO, WARNING, ERROR",
            "logger": "Logger name",
            "message": "Human-readable event description",
            "run_id": "Correlation ID for one pipeline run",
        },
        "optional": {
            "stage": "Pipeline stage such as extract, transform, load",
            "duration_ms": "Operation duration in milliseconds",
            "records_in": "Input record count",
            "records_out": "Output record count",
            "error_type": "Exception class name",
            "query_id": "Query identifier",
            "batch_num": "Batch number for progress logging",
        },
    }


def validate_log_entry(entry: dict[str, Any], schema: dict[str, Any]) -> tuple[bool, list[str]]:
    """
    Validate that a log entry contains required schema fields.

    WHY:
        Schema validation catches logging regressions early. If run_id disappears
        from production logs, correlation and incident debugging become much
        harder.

    Args:
        entry (dict[str, Any]): Log entry to validate.
        schema (dict[str, Any]): Schema from define_log_schema().

    Returns:
        tuple[bool, list[str]]: Validation status and missing required fields.

    Raises:
        None.
    """
    required_fields = list(schema.get("required", {}).keys())
    missing = [field for field in required_fields if field not in entry]
    return len(missing) == 0, missing


def show_cloudwatch_handler_config(log_group: str, stream_name: str) -> str:
    """
    Return a ready-to-use CloudWatch handler snippet.

    WHY:
        watchtower is a common Python-to-CloudWatch bridge in AWS data pipelines.
        This tutorial prints the config but does not execute it, so no AWS
        credentials are required.

    Args:
        log_group (str): CloudWatch Logs group name.
        stream_name (str): CloudWatch Logs stream name.

    Returns:
        str: Example configuration snippet.

    Raises:
        None.
    """
    return f'''
# Optional dependency:
#   pip install watchtower

import logging
import watchtower

cloudwatch_handler = watchtower.CloudWatchLogHandler(
    log_group="{log_group}",
    stream_name="{stream_name}",
)

logger = logging.getLogger("pipeline.cloudwatch")
logger.setLevel(logging.INFO)
logger.addHandler(cloudwatch_handler)
'''


def show_splunk_handler_config(splunk_host: str, index: str) -> str:
    """
    Return a ready-to-use Splunk HEC handler snippet.

    WHY:
        Splunk HEC is a common enterprise log ingestion path. This tutorial shows
        the wiring pattern without executing it or requiring credentials.

    Args:
        splunk_host (str): Splunk host URL.
        index (str): Splunk index name.

    Returns:
        str: Example configuration snippet.

    Raises:
        None.
    """
    return f'''
# Optional dependency:
#   pip install splunk-handler

import logging
from splunk_handler import SplunkHandler

splunk_handler = SplunkHandler(
    host="{splunk_host}",
    port=8088,
    token="REPLACE_WITH_HEC_TOKEN",
    index="{index}",
    sourcetype="_json",
    verify=True,
)

logger = logging.getLogger("pipeline.splunk")
logger.setLevel(logging.INFO)
logger.addHandler(splunk_handler)
'''


def build_log_rotation_config(
    log_dir: Path,
    max_size_mb: int = 100,
    backup_count: int = 7,
) -> dict[str, Any]:
    """
    Build an ops-friendly log rotation configuration dictionary.

    WHY:
        Logging decisions should be documented. This config can be pasted into
        runbooks so ops teams understand disk usage, retention, and rotation
        expectations.

    Args:
        log_dir (Path): Directory where logs are written.
        max_size_mb (int): Maximum active log file size.
        backup_count (int): Number of backups retained.

    Returns:
        dict[str, Any]: Rotation configuration.

    Raises:
        None.
    """
    return {
        "log_dir": str(log_dir),
        "rotation_strategy": "size-based",
        "handler": "logging.handlers.RotatingFileHandler",
        "max_size_mb": max_size_mb,
        "backup_count": backup_count,
        "estimated_max_disk_mb_per_log": max_size_mb * (backup_count + 1),
        "why": (
            "Size-based rotation keeps disk usage bounded and tracks pipeline "
            "volume better than clock-based rotation."
        ),
    }


def _reset_logger(logger: logging.Logger) -> None:
    """
    Remove handlers from a logger so repeated runs do not duplicate output.

    WHY:
        Handler duplication is common in notebooks, CLIs, tests, and tutorial
        scripts. Idempotent logger setup prevents confusing duplicate log lines.

    Args:
        logger (logging.Logger): Logger to reset.

    Returns:
        None.

    Raises:
        None.
    """
    for handler in list(logger.handlers):
        handler.close()
        logger.removeHandler(handler)


def _build_ops_logger(log_file: Path) -> logging.Logger:
    """
    Build the demo logger with rotation and sampling.

    WHY:
        Keeping setup in one function makes the demo easier to read and mirrors
        how production applications centralize logging configuration.

    Args:
        log_file (Path): File where records should be written.

    Returns:
        logging.Logger: Configured logger.

    Raises:
        OSError: If the log directory cannot be created.
    """
    logger = logging.getLogger("pipeline.ops")
    _reset_logger(logger)

    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    handler = build_rotating_handler(log_file, max_size_mb=1, backup_count=3)
    handler.addFilter(SamplingFilter(0.10))

    logger.addHandler(handler)
    return logger


def _parse_json_records(log_file: Path) -> list[dict[str, Any]]:
    """
    Parse JSON records from a log file.

    WHY:
        The demo needs to prove sampling actually changed the number of emitted
        records. Parsing the file is the same pattern used in tests and incident
        analysis.

    Args:
        log_file (Path): Log file to parse.

    Returns:
        list[dict[str, Any]]: Parsed records.

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


def run_demo() -> None:
    """
    Run the log aggregation and ops demonstration.

    WHY:
        This connects the operational concerns around logs: keeping volume under
        control, validating schema, documenting rotation, and showing where logs
        would be shipped in real enterprise environments.

    Args:
        None.

    Returns:
        None.

    Raises:
        OSError: If log output cannot be written or read.
    """
    random.seed(42)

    log_dir = get_log_dir()
    log_file = log_dir / "05_ops.log"

    if log_file.exists():
        log_file.unlink()

    logger = _build_ops_logger(log_file)

    for i in range(200):
        logger.debug(
            "debug event",
            extra={
                "run_id": "ops-demo",
                "stage": "debug-sample",
                "batch_num": i,
                "records_in": 100,
                "records_out": 100,
            },
        )

    for i in range(50):
        logger.info(
            "info event",
            extra={
                "run_id": "ops-demo",
                "stage": "info-sample",
                "batch_num": i,
                "records_in": 1000,
                "records_out": 995,
            },
        )

    for i in range(10):
        logger.warning(
            "warning event always kept",
            extra={
                "run_id": "ops-demo",
                "stage": "warning-stage",
                "query_id": f"q-{i}",
                "duration_ms": 1500 + i,
            },
        )

    for i in range(5):
        logger.error(
            "error event always kept",
            extra={
                "run_id": "ops-demo",
                "stage": "error-stage",
                "error_type": "RuntimeError",
                "query_id": f"err-{i}",
            },
        )

    records = _parse_json_records(log_file)
    level_counts: dict[str, int] = {}

    for record in records:
        level = str(record.get("levelname", "UNKNOWN"))
        level_counts[level] = level_counts.get(level, 0) + 1

    schema = define_log_schema()

    sample_entries = [
        {
            "timestamp": "2026-04-26T00:00:00Z",
            "level": "INFO",
            "logger": "pipeline.ops",
            "message": "valid entry",
            "run_id": "abc123",
            "stage": "extract",
        },
        {
            "timestamp": "2026-04-26T00:00:00Z",
            "level": "INFO",
            "logger": "pipeline.ops",
            "message": "missing run_id",
            "stage": "transform",
        },
        {
            "timestamp": "2026-04-26T00:00:00Z",
            "level": "INFO",
            "logger": "pipeline.ops",
            "message": "missing stage but valid because stage is optional",
            "run_id": "xyz789",
        },
    ]

    validation_results = []
    for entry in sample_entries:
        is_valid, missing = validate_log_entry(entry, schema)
        validation_results.append(
            {
                "message": entry["message"],
                "is_valid": is_valid,
                "missing_required_fields": missing,
            }
        )

    print("\n--- Sampling Summary ---")
    print(f"Attempted: 200 DEBUG, 50 INFO, 10 WARNING, 5 ERROR")
    print(f"Actually written: {len(records)} total")
    print(json.dumps(level_counts, indent=2))

    print("\n--- Schema Validation ---")
    print(json.dumps(validation_results, indent=2))

    print("\n--- CloudWatch Handler Config Snippet ---")
    print(show_cloudwatch_handler_config("/studybook/python-logging", "pipeline-ops-demo"))

    print("\n--- Splunk Handler Config Snippet ---")
    print(show_splunk_handler_config("https://splunk.example.com", "studybook"))

    print("\n--- Rotation Config ---")
    print(json.dumps(build_log_rotation_config(log_dir), indent=2))


if __name__ == "__main__":
    run_demo()