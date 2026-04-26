# ============================================================
# Topic   : Python Logging for Data Engineers
# File    : 01_logging_fundamentals.py
# Covers  : Python stdlib logging hierarchy, handlers, formatters, levels, propagation, and rotation
# Prereqs : pip install structlog python-json-logger
# Run     : python 01_logging_fundamentals.py
# ============================================================

from __future__ import annotations

import logging
import os
import sys
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path

def get_log_dir() -> Path:
    """
    Return the configured log directory, creating it if needed.

    WHY:
        Hardcoding /tmp is Unix-specific and looks awkward on Windows.
        A senior implementation adapts to the OS:

        - Linux/macOS → /tmp/studybook/logs (standard ephemeral location)
        - Windows     → %LOCALAPPDATA%/studybook/logs (user-safe writable location)

        This avoids permission issues and keeps logs in expected locations
        per platform conventions.

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
            # Windows: use LOCALAPPDATA (e.g., C:\Users\<user>\AppData\Local)
            base = Path(os.getenv("LOCALAPPDATA", Path.home()))
            log_dir = base / "studybook" / "logs"
        else:
            # Linux/macOS
            log_dir = Path("/tmp/studybook/logs")

    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir
    
    
def _reset_logger(logger: logging.Logger) -> None:
    """
    Remove existing handlers from a logger so demos are repeatable.

    WHY:
        Logging handlers are sticky. If setup code runs twice in a notebook,
        test, or long-lived process, duplicate handlers cause duplicate log
        lines. Senior engineers make logger configuration idempotent.

    Args:
        logger (logging.Logger): Logger to clean up.

    Returns:
        None.

    Raises:
        None.
    """
    for handler in list(logger.handlers):
        handler.close()
        logger.removeHandler(handler)


def get_basic_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Create a named stdout logger with a minimal formatter.

    WHY:
        Named loggers isolate modules. The root logger is a global footgun
        because any imported library can modify it and unexpectedly change
        your application's output.

    Args:
        name (str): Logger name, usually __name__ or a pipeline component name.
        level (int): Logger threshold, such as logging.INFO or logging.DEBUG.

    Returns:
        logging.Logger: Configured logger writing to stdout.

    Raises:
        None.
    """
    logger = logging.getLogger(name)
    _reset_logger(logger)

    logger.setLevel(level)
    logger.propagate = False

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter("%(levelname)s | %(name)s | %(message)s"))

    logger.addHandler(handler)
    return logger


def get_file_logger(
    name: str,
    log_file: Path,
    max_bytes: int = 10_000_000,
    backup_count: int = 5,
) -> logging.Logger:
    """
    Create a named logger that writes to a rotating file.

    WHY:
        RotatingFileHandler is often better than TimedRotatingFileHandler for
        data pipelines because pipeline log volume usually correlates with data
        size, not clock time. A huge daily run should rotate by bytes before it
        fills the disk.

    Args:
        name (str): Logger name.
        log_file (Path): File path for log output.
        max_bytes (int): Maximum size of one log file before rotation.
        backup_count (int): Number of rotated files to keep.

    Returns:
        logging.Logger: Configured file logger.

    Raises:
        OSError: If the parent directory cannot be created.
    """
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    _reset_logger(logger)

    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    )

    logger.addHandler(handler)
    return logger


def get_dual_logger(name: str, log_file: Path) -> logging.Logger:
    """
    Create a logger with INFO console output and DEBUG file output.

    WHY:
        Console logs should tell operators what is happening now. File logs
        should preserve the detailed trace needed for post-mortems. Splitting
        levels by handler gives both audiences the right signal.

    Args:
        name (str): Logger name.
        log_file (Path): File path for detailed logs.

    Returns:
        logging.Logger: Logger with console and rotating file handlers.

    Raises:
        OSError: If the parent directory cannot be created.
    """
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    _reset_logger(logger)

    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter("%(levelname)s | %(message)s"))

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10_000_000,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    )

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger


def demonstrate_hierarchy() -> None:
    """
    Demonstrate parent/child loggers, propagation, and double-logging.

    WHY:
        Logger hierarchy is one of the most common production logging bugs.
        A child logger like pipeline.extract automatically propagates to the
        parent logger pipeline unless propagation is disabled. If root is also
        configured, the same record can appear multiple times.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """
    print("\n--- demonstrate_hierarchy() ---")

    root = logging.getLogger()
    _reset_logger(root)
    root.setLevel(logging.DEBUG)

    root_handler = logging.StreamHandler(sys.stdout)
    root_handler.setLevel(logging.DEBUG)
    root_handler.setFormatter(logging.Formatter("ROOT    | %(name)s | %(message)s"))
    root.addHandler(root_handler)

    parent = logging.getLogger("pipeline")
    _reset_logger(parent)
    parent.setLevel(logging.DEBUG)
    parent.propagate = True

    parent_handler = logging.StreamHandler(sys.stdout)
    parent_handler.setLevel(logging.DEBUG)
    parent_handler.setFormatter(logging.Formatter("PARENT  | %(name)s | %(message)s"))
    parent.addHandler(parent_handler)

    child = logging.getLogger("pipeline.extract")
    _reset_logger(child)
    child.setLevel(logging.DEBUG)

    print("Child propagates to parent and root, so this appears twice:")
    child.info("extract started")

    print("Now disable child propagation and add a child handler:")
    child.propagate = False
    child_handler = logging.StreamHandler(sys.stdout)
    child_handler.setLevel(logging.DEBUG)
    child_handler.setFormatter(logging.Formatter("CHILD   | %(name)s | %(message)s"))
    child.addHandler(child_handler)
    child.info("extract started without parent/root duplication")

    _reset_logger(root)
    _reset_logger(parent)
    _reset_logger(child)


def demonstrate_level_filter() -> None:
    """
    Demonstrate how logger and handler levels combine.

    WHY:
        The effective threshold is the more restrictive combination of logger
        and handler levels. If the logger blocks DEBUG, a DEBUG handler never
        sees that record. This distinction matters when designing console logs
        versus detailed file logs.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """
    print("\n--- demonstrate_level_filter() ---")

    logger_a = logging.getLogger("level.demo.a")
    _reset_logger(logger_a)
    logger_a.setLevel(logging.DEBUG)
    logger_a.propagate = False

    handler_a = logging.StreamHandler(sys.stdout)
    handler_a.setLevel(logging.INFO)
    handler_a.setFormatter(logging.Formatter("A | %(levelname)s | %(message)s"))
    logger_a.addHandler(handler_a)

    print("Case A: logger DEBUG + handler INFO -> DEBUG blocked by handler")
    logger_a.debug("This DEBUG message is blocked by the handler.")
    logger_a.info("This INFO message reaches the handler.")

    logger_b = logging.getLogger("level.demo.b")
    _reset_logger(logger_b)
    logger_b.setLevel(logging.INFO)
    logger_b.propagate = False

    handler_b = logging.StreamHandler(sys.stdout)
    handler_b.setLevel(logging.DEBUG)
    handler_b.setFormatter(logging.Formatter("B | %(levelname)s | %(message)s"))
    logger_b.addHandler(handler_b)

    print("Case B: logger INFO + handler DEBUG -> DEBUG blocked by logger")
    logger_b.debug("This DEBUG message is blocked before handlers see it.")
    logger_b.info("This INFO message reaches the handler.")

    _reset_logger(logger_a)
    _reset_logger(logger_b)


def _expensive_call() -> str:
    """
    Simulate an expensive value calculation used in a log message.

    WHY:
        Expensive log arguments in tight loops can become real pipeline cost.
        The safest pattern is to avoid doing expensive work unless the level is
        enabled.

    Args:
        None.

    Returns:
        str: Simulated expensive value.

    Raises:
        None.
    """
    time.sleep(0.05)
    return "expensive-value"


def bad_vs_good_formatting() -> None:
    """
    Compare eager f-string formatting with lazy percent-style logging.

    WHY:
        f-strings are evaluated before the logging level check. Percent-style
        logger arguments defer string interpolation until the record is emitted.
        This is critical in tight loops where DEBUG logs are usually disabled.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """
    print("\n--- bad_vs_good_formatting() ---")

    logger = get_basic_logger("formatting.demo", level=logging.INFO)

    start_bad = time.perf_counter()
    logger.debug(f"Processing {_expensive_call()}")
    bad_ms = (time.perf_counter() - start_bad) * 1000

    value = "cheap-precomputed-value"
    start_good = time.perf_counter()
    logger.debug("Processing %s", value)
    good_ms = (time.perf_counter() - start_good) * 1000

    logger.info("Bad f-string DEBUG call still paid %.2f ms", bad_ms)
    logger.info("Good %% formatting DEBUG call paid %.2f ms", good_ms)

    if logger.isEnabledFor(logging.DEBUG):
        expensive_value = _expensive_call()
        logger.debug("Only compute expensive value when DEBUG is enabled: %s", expensive_value)
    else:
        logger.info("Skipped expensive DEBUG-only computation because DEBUG is disabled.")


def _print_last_lines(log_file: Path, line_count: int = 10) -> None:
    """
    Print the last lines of a log file for a simple demo summary.

    WHY:
        A runnable tutorial should prove that file logging worked. Reading the
        tail mirrors what data engineers do during incident triage with tools
        like tail, less, CloudWatch Logs, Splunk, or ELK.

    Args:
        log_file (Path): Log file to read.
        line_count (int): Number of final lines to print.

    Returns:
        None.

    Raises:
        OSError: If the file cannot be read.
    """
    print(f"\n--- Last {line_count} lines of {log_file} ---")
    lines = log_file.read_text(encoding="utf-8").splitlines()
    for line in lines[-line_count:]:
        print(line)


def run_pipeline_demo() -> None:
    """
    Run a five-iteration pipeline simulation using the dual logger.

    WHY:
        Real pipelines emit different levels for different audiences: DEBUG for
        diagnosis, INFO for normal progress, WARNING for recoverable anomalies,
        and ERROR for failures that need investigation.

    Args:
        None.

    Returns:
        None.

    Raises:
        OSError: If log output cannot be written or read.
    """
    log_dir = get_log_dir()
    log_file = log_dir / "01_fundamentals.log"

    logger = get_dual_logger("studybook.pipeline.fundamentals", log_file)

    logger.info("pipeline run started")
    for iteration in range(1, 6):
        logger.debug("iteration %s raw input payload validated", iteration)
        logger.info("iteration %s processed successfully", iteration)

        if iteration == 3:
            logger.warning(
                "iteration %s processed with elevated latency_ms=%s",
                iteration,
                842,
            )

        if iteration == 5:
            try:
                raise ValueError("simulated bad record count mismatch")
            except ValueError as exc:
                logger.error(
                    "iteration %s failed validation: %s",
                    iteration,
                    exc,
                    exc_info=True,
                )

    logger.info("pipeline run completed")
    _print_last_lines(log_file)


if __name__ == "__main__":
    run_pipeline_demo()
    demonstrate_hierarchy()
    demonstrate_level_filter()
    bad_vs_good_formatting()