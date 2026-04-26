# ============================================================
# Topic   : Python Logging for Data Engineers
# File    : capstone/pipeline_logger.py
# Covers  : Reusable structured logging library for data pipelines
# Prereqs : pip install structlog python-json-logger
# Run     : python pipeline_logger.py
# ============================================================

from __future__ import annotations

import json
import logging
import os
import sys
import time
import uuid
from contextlib import contextmanager
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Generator

from pythonjsonlogger import jsonlogger


DEFAULT_LOG_DIR = Path(os.getenv("LOG_DIR", "/tmp/studybook/logs"))
DEFAULT_ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")


def get_log_dir(subdir: str = "") -> Path:
    """
    Return the configured log directory, optionally nested under a subdirectory.

    WHY:
        A reusable library should never hardcode output paths inside business
        logic. Centralizing path resolution keeps every pipeline consistent and
        lets schedulers override log location with LOG_DIR.

    Args:
        subdir (str): Optional child directory under the default log directory.

    Returns:
        Path: Created log directory.

    Raises:
        OSError: If the directory cannot be created.
    """
    env_dir = os.getenv("LOG_DIR")

    if env_dir:
        base_dir = Path(env_dir)
    else:
        if os.name == "nt":
            local_app_data = os.getenv("LOCALAPPDATA")
            base_dir = Path(local_app_data) / "studybook" / "logs" if local_app_data else Path.home() / "studybook" / "logs"
        else:
            base_dir = DEFAULT_LOG_DIR

    log_dir = base_dir / subdir if subdir else base_dir
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir


def generate_run_id() -> str:
    """
    Generate a short run correlation ID.

    WHY:
        Correlation IDs are the backbone of production observability. They allow
        one pipeline run to be traced across stages, files, retries, and alerts.

    Args:
        None.

    Returns:
        str: 8-character UUID hex prefix.

    Raises:
        None.
    """
    return uuid.uuid4().hex[:8]


class SamplingFilter(logging.Filter):
    """
    Sampling filter for noisy low-level logs.

    WHY:
        Production systems should never sample away WARNING or ERROR records, but
        DEBUG logs can overwhelm disk and aggregation systems. Sampling preserves
        visibility while controlling cost.
    """

    def __init__(self, sample_rate: float = 0.10) -> None:
        """
        Initialize the sampling filter.

        WHY:
            Making sample rate explicit prevents hidden production behavior and
            lets teams tune verbosity by environment.

        Args:
            sample_rate (float): Fraction of DEBUG records to keep.

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
        Decide whether the record should be emitted.

        WHY:
            Important records must always pass. Only DEBUG records are sampled
            because they are usually diagnostic rather than operational signals.

        Args:
            record (logging.LogRecord): Candidate log record.

        Returns:
            bool: True when the record should be emitted.

        Raises:
            None.
        """
        if record.levelno >= logging.INFO:
            return True

        return uuid.uuid4().int % 10_000 < int(self.sample_rate * 10_000)


class PipelineLogger(logging.LoggerAdapter):
    """
    LoggerAdapter that injects run_id, pipeline_name, and environment.

    WHY:
        LoggerAdapter is the stdlib way to add persistent context without
        subclassing Logger or wrapping every call site.
    """

    def __init__(
        self,
        logger: logging.Logger,
        run_id: str,
        pipeline_name: str,
        environment: str,
    ) -> None:
        """
        Initialize a pipeline-aware logger adapter.

        WHY:
            These three fields should exist on every production pipeline log.
            Adding them once at construction prevents missing context later.

        Args:
            logger (logging.Logger): Underlying stdlib logger.
            run_id (str): Correlation ID for this pipeline run.
            pipeline_name (str): Human-readable pipeline name.
            environment (str): Runtime environment such as dev, staging, or prod.

        Returns:
            None.

        Raises:
            None.
        """
        super().__init__(logger, {})
        self.run_id = run_id
        self.pipeline_name = pipeline_name
        self.environment = environment

    def process(self, msg: str, kwargs: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        """
        Merge persistent context into every log record.

        WHY:
            This guarantees every log line can be filtered by run_id,
            pipeline_name, and environment in a log aggregator.

        Args:
            msg (str): Original log message.
            kwargs (dict[str, Any]): Logging keyword arguments.

        Returns:
            tuple[str, dict[str, Any]]: Message and updated kwargs.

        Raises:
            None.
        """
        extra = kwargs.setdefault("extra", {})
        extra.update(
            run_id=self.run_id,
            pipeline_name=self.pipeline_name,
            environment=self.environment,
        )
        return msg, kwargs


class _SafeJsonFormatter(jsonlogger.JsonFormatter):
    """
    JSON formatter that fills missing optional fields.

    WHY:
        JSON formatters can raise errors when a format string references fields
        that are absent from a record. A reusable pipeline logger should be
        forgiving at call sites while still producing consistent JSON.
    """

    DEFAULT_FIELDS: dict[str, Any] = {
        "run_id": "",
        "pipeline_name": "",
        "environment": "",
        "stage": "",
        "duration_ms": None,
        "row_count": None,
        "col_count": None,
        "null_counts": None,
        "sample_cols": None,
        "error_type": "",
    }

    def add_fields(
        self,
        log_record: dict[str, Any],
        record: logging.LogRecord,
        message_dict: dict[str, Any],
    ) -> None:
        """
        Add standard fields and normalize names.

        WHY:
            Monitoring tools prefer stable field names. This maps stdlib names
            like levelname/name/asctime to cleaner fields like level/logger/timestamp.

        Args:
            log_record (dict[str, Any]): JSON output dictionary.
            record (logging.LogRecord): Original logging record.
            message_dict (dict[str, Any]): Message dictionary from formatter.

        Returns:
            None.

        Raises:
            None.
        """
        super().add_fields(log_record, record, message_dict)

        for field, default in self.DEFAULT_FIELDS.items():
            log_record.setdefault(field, default)

        log_record["timestamp"] = log_record.pop("asctime", "")
        log_record["level"] = log_record.pop("levelname", record.levelname)
        log_record["logger"] = log_record.pop("name", record.name)


def _reset_logger(logger: logging.Logger) -> None:
    """
    Remove all handlers from a logger.

    WHY:
        Repeated test runs, notebook cells, and import-time setup can duplicate
        handlers. Idempotent setup is required for reliable logging behavior.

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


def _build_json_formatter() -> _SafeJsonFormatter:
    """
    Build the shared JSON formatter.

    WHY:
        A central formatter gives every pipeline the same schema, which is the
        contract between application code and observability tooling.

    Args:
        None.

    Returns:
        _SafeJsonFormatter: Configured JSON formatter.

    Raises:
        None.
    """
    return _SafeJsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s "
        "%(run_id)s %(pipeline_name)s %(environment)s %(stage)s "
        "%(duration_ms)s %(row_count)s %(col_count)s %(null_counts)s "
        "%(sample_cols)s %(error_type)s"
    )


def get_pipeline_logger(
    pipeline_name: str,
    run_id: str | None = None,
    environment: str = DEFAULT_ENVIRONMENT,
    log_file: Path | None = None,
    level: int = logging.INFO,
) -> PipelineLogger:
    """
    Create a reusable pipeline logger.

    WHY:
        This is the single entry point future tutorials should use. Callers get
        console output, JSON file output, rotation, and persistent context
        without knowing logging internals.

    Args:
        pipeline_name (str): Pipeline name.
        run_id (str | None): Optional run ID. Generated when omitted.
        environment (str): Runtime environment.
        log_file (Path | None): Optional explicit log file path.
        level (int): Base logger level.

    Returns:
        PipelineLogger: Context-injecting logger adapter.

    Raises:
        OSError: If the log directory cannot be created.
    """
    resolved_run_id = run_id or generate_run_id()
    resolved_log_file = log_file or get_log_dir() / f"{pipeline_name}.log"
    resolved_log_file.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(f"studybook.pipeline.{pipeline_name}.{resolved_run_id}")
    _reset_logger(logger)

    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    file_handler = RotatingFileHandler(
        resolved_log_file,
        maxBytes=50 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(_build_json_formatter())

    if environment == "prod":
        file_handler.addFilter(SamplingFilter(sample_rate=0.10))

    logger.addHandler(file_handler)

    if environment != "prod":
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)

        if environment == "dev":
            console_handler.setFormatter(
                logging.Formatter(
                    "%(levelname)s | %(message)s "
                    "[run_id=%(run_id)s pipeline=%(pipeline_name)s stage=%(stage)s]"
                )
            )
        else:
            console_handler.setFormatter(_build_json_formatter())

        logger.addHandler(console_handler)

    return PipelineLogger(
        logger=logger,
        run_id=resolved_run_id,
        pipeline_name=pipeline_name,
        environment=environment,
    )


@contextmanager
def log_stage(
    logger: PipelineLogger,
    stage_name: str,
    **context_fields: Any,
) -> Generator[PipelineLogger, None, None]:
    """
    Log stage lifecycle events with timing and exception handling.

    WHY:
        Context managers eliminate repeated try/except/finally boilerplate around
        pipeline stages. Three lines at the call site produce start, completed,
        failed, duration, stage context, and traceback logs.

    Args:
        logger (PipelineLogger): Pipeline logger.
        stage_name (str): Stage name such as extract, validate, transform, load.
        **context_fields (Any): Extra fields to attach to stage lifecycle logs.

    Returns:
        Generator[PipelineLogger, None, None]: The same logger for use inside the block.

    Raises:
        Exception: Re-raises the original exception from the stage block.
    """
    start_time = time.perf_counter()
    logger.info(
        "stage started",
        extra={
            "stage": stage_name,
            **context_fields,
        },
    )

    try:
        yield logger

        duration_ms = round((time.perf_counter() - start_time) * 1000, 3)
        logger.info(
            "stage completed",
            extra={
                "stage": stage_name,
                "duration_ms": duration_ms,
                **context_fields,
            },
        )
    except Exception as exc:
        duration_ms = round((time.perf_counter() - start_time) * 1000, 3)
        logger.error(
            "stage failed",
            extra={
                "stage": stage_name,
                "duration_ms": duration_ms,
                "error_type": type(exc).__name__,
                **context_fields,
            },
            exc_info=True,
        )
        raise


def log_dataframe_stats(
    logger: PipelineLogger,
    stage_name: str,
    row_count: int,
    col_count: int,
    null_counts: dict[str, int] | None = None,
    sample_cols: list[str] | None = None,
) -> None:
    """
    Log dataframe-like shape and null statistics.

    WHY:
        Silent data loss is one of the hardest pipeline bugs. Logging shape after
        every transformation makes row-count drops visible immediately.

    Args:
        logger (PipelineLogger): Pipeline logger.
        stage_name (str): Pipeline stage name.
        row_count (int): Number of rows.
        col_count (int): Number of columns.
        null_counts (dict[str, int] | None): Optional null counts by column.
        sample_cols (list[str] | None): Optional representative column names.

    Returns:
        None.

    Raises:
        None.
    """
    logger.info(
        "dataframe stats",
        extra={
            "stage": stage_name,
            "row_count": row_count,
            "col_count": col_count,
            "null_counts": json.dumps(null_counts or {}, sort_keys=True),
            "sample_cols": json.dumps(sample_cols or [], sort_keys=True),
        },
    )


def configure_for_environment(environment: str) -> None:
    """
    Configure root logging defaults for an environment.

    WHY:
        Environment-aware logging prevents verbose development logs from
        drowning production systems while keeping local debugging friendly.

    Args:
        environment (str): One of dev, staging, or prod.

    Returns:
        None.

    Raises:
        ValueError: If environment is unsupported.
    """
    normalized = environment.lower()

    if normalized == "dev":
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(levelname)s | %(name)s | %(message)s",
            stream=sys.stdout,
            force=True,
        )
    elif normalized == "staging":
        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s",
            stream=sys.stdout,
            force=True,
        )
    elif normalized == "prod":
        logging.basicConfig(
            level=logging.WARNING,
            format="%(message)s",
            handlers=[
                RotatingFileHandler(
                    get_log_dir() / "root-prod.log",
                    maxBytes=50 * 1024 * 1024,
                    backupCount=5,
                    encoding="utf-8",
                )
            ],
            force=True,
        )
    else:
        raise ValueError(
            f"Unsupported environment: {environment}. "
            "Expected one of: dev, staging, prod."
        )


def _self_check() -> None:
    """
    Run a lightweight import/self-check demo.

    WHY:
        The prompt asks this library file to be runnable as an import test.
        A minimal self-check verifies logger creation, stage timing, and JSON
        output without pretending this library is the main demo pipeline.

    Args:
        None.

    Returns:
        None.

    Raises:
        OSError: If the self-check log cannot be written or read.
    """
    log_file = get_log_dir("capstone") / "pipeline_logger_self_check.log"

    logger = get_pipeline_logger(
        pipeline_name="pipeline-logger-self-check",
        run_id="selfcheck",
        environment="dev",
        log_file=log_file,
    )

    with log_stage(logger, "self_check", check_type="import"):
        log_dataframe_stats(
            logger,
            "self_check",
            row_count=3,
            col_count=2,
            null_counts={"id": 0, "value": 1},
            sample_cols=["id", "value"],
        )

    print(f"Self-check complete. JSON log written to: {log_file}")


if __name__ == "__main__":
    _self_check()