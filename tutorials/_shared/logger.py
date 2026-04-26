# ============================================================
# Shared Structured Logger
# _shared/logger.py
#
# Provides JSON-structured logging for all tutorial files.
# Structured logging means every log line is a machine-readable
# JSON record — queryable in CloudWatch Logs Insights, ELK,
# or any log aggregation platform.
#
# Usage in any tutorial file:
#   import sys; sys.path.insert(0, str(Path(__file__).parents[2] / "_shared"))
#   from logger import get_logger
#   logger = get_logger("my-topic")
#   logger.info("Stage complete", records_in=1000, records_out=998, duration_s=1.4)
# ============================================================

import logging
import os
import sys
from typing import Any

# python-json-logger is the standard library for structured JSON logging in Python.
# It extends the built-in logging module rather than replacing it, so all existing
# logging infrastructure (handlers, levels, filters) still works.
try:
    from pythonjsonlogger import jsonlogger
    _JSON_AVAILABLE = True
except ImportError:
    _JSON_AVAILABLE = False

# ── Configuration ─────────────────────────────────────────────
# LOG_LEVEL controls verbosity. In production pipelines, use INFO.
# During development and debugging, set to DEBUG to see all detail.
LOG_LEVEL  = os.environ.get("LOG_LEVEL", "INFO").upper()
LOG_FORMAT = os.environ.get("LOG_FORMAT", "json")   # "json" or "text"

# Fields included in every log record automatically.
# In a real pipeline these come from the run context — injected once
# at pipeline start and carried through all stages via LoggerAdapter.
DEFAULT_FIELDS = {
    "app"     : "studybook-tutorial",
    "env"     : os.environ.get("ENVIRONMENT", "dev"),
}


class ContextLogger(logging.LoggerAdapter):
    """
    A LoggerAdapter that merges context fields into every log record.

    Why LoggerAdapter instead of a Filter?
    LoggerAdapter lets you pass extra fields as keyword arguments at the
    call site (logger.info("msg", run_id="abc", stage="enrich")) and
    merges them with the persistent context set at construction time.
    Filters run passively and can't accept call-site kwargs cleanly.

    Usage:
        logger = get_logger("pipeline", run_id="run-001", pipeline="citi-etl")
        logger.info("Stage started", stage="extract", records_expected=50000)
    """

    def process(self, msg: str, kwargs: dict) -> tuple[str, dict]:
        """
        Merge adapter context with call-site extra fields before emission.

        Args:
            msg: log message string
            kwargs: logging call kwargs (may contain 'extra' dict)

        Returns:
            tuple of (msg, merged kwargs)
        """
        # Call-site kwargs like logger.info("msg", stage="x") arrive as
        # top-level kwargs in LoggerAdapter. We need to move them into
        # the 'extra' dict so the JSON formatter picks them up as fields.
        extra = {**self.extra}

        # Pull any keyword args that aren't standard logging args into extra.
        # Standard logging kwargs: exc_info, stack_info, stacklevel, extra
        standard_kwargs = {"exc_info", "stack_info", "stacklevel", "extra"}
        call_extra = {k: v for k, v in kwargs.items() if k not in standard_kwargs}
        extra.update(call_extra)
        extra.update(kwargs.get("extra", {}))

        # Remove call-site kwargs from top-level to avoid TypeError
        for k in call_extra:
            kwargs.pop(k, None)

        kwargs["extra"] = extra
        return msg, kwargs


def get_logger(name: str, **context: Any) -> ContextLogger:
    """
    Return a structured logger with persistent context fields.

    Every log record emitted by this logger will include:
    - Standard fields: timestamp, level, logger name, message
    - Default fields: app, env (from DEFAULT_FIELDS)
    - Context fields: whatever you pass as kwargs here
    - Call-site fields: whatever you pass when calling logger.info() etc.

    Args:
        name: logger name — use the topic or module name
        **context: persistent fields added to every record from this logger
                   e.g. run_id="abc-123", pipeline="citi-etl", stage="extract"

    Returns:
        ContextLogger: a LoggerAdapter wrapping the named logger

    Example:
        logger = get_logger("aws-kinesis", run_id="run-001")
        logger.info("Put record", stream="my-stream", partition_key="sensor-01")
        # Output: {"timestamp": "...", "level": "INFO", "message": "Put record",
        #          "app": "studybook-tutorial", "run_id": "run-001",
        #          "stream": "my-stream", "partition_key": "sensor-01"}
    """
    base_logger = logging.getLogger(name)
    base_logger.setLevel(LOG_LEVEL)

    # Avoid adding duplicate handlers if get_logger() is called multiple times
    if not base_logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(LOG_LEVEL)

        if _JSON_AVAILABLE and LOG_FORMAT == "json":
            # JSON formatter: every field is a top-level key in the JSON object.
            # The format string defines which standard LogRecord attributes to include.
            formatter = jsonlogger.JsonFormatter(
                fmt="%(asctime)s %(name)s %(levelname)s %(message)s",
                rename_fields={"asctime": "timestamp", "levelname": "level", "name": "logger"},
            )
        else:
            # Fallback text formatter for local dev when python-json-logger is not installed
            formatter = logging.Formatter(
                fmt="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
                datefmt="%Y-%m-%dT%H:%M:%S",
            )

        handler.setFormatter(formatter)
        base_logger.addHandler(handler)

    # Merge default fields with caller-supplied context
    merged_context = {**DEFAULT_FIELDS, **context}
    return ContextLogger(base_logger, merged_context)


if __name__ == "__main__":
    # Demonstrate structured logging with context injection
    print("Structured Logger Demo")
    print("-" * 40)

    # Basic logger
    log = get_logger("demo")
    log.info("Basic log message")
    log.warning("Something unexpected happened", detail="disk at 85%")

    # Logger with persistent context — simulates a pipeline run
    pipeline_log = get_logger("pipeline", run_id="run-20260425-001", pipeline="citi-etl")
    pipeline_log.info("Pipeline started", stage="extract", source="oracle")
    pipeline_log.info("Stage complete", stage="extract", records_in=50000, duration_s=12.4)
    pipeline_log.error("Stage failed", stage="enrich", error="join key null rate 45%", exc_info=False)

    print("\nNote: set LOG_FORMAT=text for human-readable output during dev")
    print("      set LOG_FORMAT=json for structured output in production")
