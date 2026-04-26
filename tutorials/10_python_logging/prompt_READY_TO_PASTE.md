# READY TO PASTE INTO CHATGPT
# Open a FRESH ChatGPT chat. Copy everything between the === markers.
# After acknowledgment follow this sequence:
#   "generate file 01"
#   "generate file 02"
#   "generate file 03"
#   "generate file 04"
#   "generate file 05"
#   "generate readme"
#   "generate capstone file pipeline_logger.py"
#   "generate capstone file example_pipeline.py"
#   "generate capstone file test_pipeline_logger.py"
#   "generate capstone brief.md"
# Save each file immediately after generation.
# ============================================================

===

You are generating educational Python tutorial files for a Senior Data Engineer
personal study system. Every file you generate must be:
- COMPLETE and FULLY RUNNABLE — no placeholders, no TODO comments, no `pass` statements,
  no skeleton functions, no "implement this" notes
- Production-quality with heavy WHY comments
- Runnable with: python filename.py

If a file would be too long for one response, continue immediately without waiting.
Never truncate a file mid-function.

TOPIC: Python Logging for Data Engineers
SLUG: python-logging
PRIORITY: Toyota Interview Prep
INFRASTRUCTURE: Pure Python — stdlib logging + structlog + python-json-logger
  No AWS. No Docker. No credentials.

===== CODING STANDARDS =====

FILE HEADER — every file starts with:
# ============================================================
# Topic   : Python Logging for Data Engineers
# File    : NN_filename.py
# Covers  : one-line description
# Prereqs : pip install structlog python-json-logger
# Run     : python filename.py
# ============================================================

ENVIRONMENT VARIABLES:
  LOG_DIR   — directory for log file output (default: /tmp/studybook/logs)
              Create it automatically if it does not exist.

COMMENTS: Explain WHY. Logging is the #1 debugging tool in production pipelines.
  Explain every design decision: why propagation matters, why % formatting beats
  f-strings inside log calls, why structured JSON beats plain text at scale.

DOCSTRINGS — every function must have:
  - One-line summary
  - WHY field: the senior insight — what separates this from a junior answer
  - Args with types
  - Returns with type
  - Raises if applicable

CODE RULES:
  - Python 3.11+, type hints on all signatures
  - No hardcoded paths — use LOG_DIR env var with pathlib.Path
  - Specific exception handling — never bare except:
  - Every file ends with if __name__ == "__main__": that runs a full working demo
  - No placeholder functions — every function body is complete and runnable

===== FILES TO GENERATE =====

01_logging_fundamentals.py
  Purpose: Python stdlib logging done right — hierarchy, handlers, formatters, levels
  Key concepts: root logger vs named loggers, handler/logger level distinction,
    propagation, RotatingFileHandler, why print() is not a substitute for logging
  Functions:
    - get_log_dir() -> Path
        — read LOG_DIR env var, default /tmp/studybook/logs, create if missing
    - get_basic_logger(name: str, level: int = logging.INFO) -> logging.Logger
        WHY: named loggers isolate modules — root logger is a global footgun
        — StreamHandler to stdout, no file, minimal setup
    - get_file_logger(name: str, log_file: Path,
        max_bytes: int = 10_000_000, backup_count: int = 5) -> logging.Logger
        WHY: RotatingFileHandler beats TimedRotatingFileHandler for pipelines
        because pipeline log volume correlates with data size, not clock time
        — include format: timestamp | level | logger_name | message
    - get_dual_logger(name: str, log_file: Path) -> logging.Logger
        — console handler at INFO, file handler at DEBUG, same logger
        WHY: console shows the summary; file captures the full trace for post-mortem
    - demonstrate_hierarchy() -> None
        — create parent "pipeline" and child "pipeline.extract" logger
        — show that child logs propagate to parent unless propagate=False
        — show the double-logging gotcha when root handler is also configured
    - demonstrate_level_filter() -> None
        — show: logger.setLevel(DEBUG) + handler.setLevel(INFO) → INFO reaches handler
        — show: logger.setLevel(INFO) + handler.setLevel(DEBUG) → DEBUG never reaches handler
        WHY: the effective level is the HIGHER (more restrictive) of logger vs handler
    - bad_vs_good_formatting() -> None
        — bad:  logger.debug(f"Processing {expensive_call()}")  # evaluated even if DEBUG disabled
        — good: logger.debug("Processing %s", value)             # lazy: only formats if level passes
        WHY: f-string is evaluated before the level check; % args are evaluated only if the
        message will actually be emitted — critical in tight loops
  Main block:
    - create dual logger writing to LOG_DIR/01_fundamentals.log
    - simulate a 5-iteration pipeline loop emitting DEBUG, INFO, WARNING, ERROR per iteration
    - print last 10 lines of the log file after the run
    - call demonstrate_hierarchy() and demonstrate_level_filter()
    - call bad_vs_good_formatting()

02_structured_json_logging.py
  Purpose: Structured JSON logging — machine-parseable logs for CloudWatch/Splunk/ELK
  Key concepts: python-json-logger, extra fields, correlation IDs, log file analysis
  Functions:
    - get_log_dir() -> Path
    - generate_run_id() -> str
        — return first 8 chars of uuid4 hex — short enough to type, unique enough for a session
        WHY: correlation IDs are the single most important logging practice for distributed
        pipelines — without them, tracing a request across 10 log files is guesswork
    - get_json_logger(name: str, log_file: Path,
        level: int = logging.INFO) -> logging.Logger
        — use pythonjsonlogger.jsonlogger.JsonFormatter
        — format includes: timestamp, level, name, message, plus any extra fields
        WHY: JSON logs can be queried with jq, Logs Insights, Splunk, or any log aggregator
        without a custom parser
    - get_contextual_logger(name: str, log_file: Path,
        run_id: str, pipeline_name: str, environment: str) -> logging.Logger
        — subclass logging.LoggerAdapter to inject run_id, pipeline_name, environment
        into every log record automatically
        WHY: LoggerAdapter is cleaner than passing context as extra= on every call
    - log_with_extra(logger: logging.Logger, level: str,
        message: str, **fields) -> None
        — emit log at given level, merging fields into the JSON record
    - parse_json_log_file(log_file: Path) -> list[dict]
        — read file, json.loads() each line, skip malformed lines, return list
    - summarize_run(log_file: Path, run_id: str) -> dict
        — parse file, filter to run_id, return:
          {run_id, total_events, by_level: {INFO: n, WARNING: n, ERROR: n},
           errors: [list of error messages], duration_ms: last_ts - first_ts}
  Main block:
    - generate run_id
    - get contextual logger writing to LOG_DIR/02_structured.log
    - simulate 3-stage pipeline (extract → transform → load):
        extract: 3 INFO events (connecting, fetching, done), 1 WARNING (slow response)
        transform: 4 INFO events (validating, deduplicating, enriching, done),
                   1 ERROR (simulated bad record with exc_info details)
        load: 2 INFO events (writing, done)
    - parse log file, call summarize_run, print the summary dict

03_structlog_advanced.py
  Purpose: structlog — the modern structured logging library for Python pipelines
  Key concepts: processor pipeline, bound loggers, context variables, dev vs prod output
  Functions:
    - get_log_dir() -> Path
    - configure_structlog_prod(log_file: Path) -> None
        — configure structlog for production: JSON renderer, UTC timestamps,
          log level filter, exception formatter, write to file
        WHY: structlog separates configuration (processors) from usage (bound loggers)
        — you configure once at startup, every logger in every module benefits
    - configure_structlog_dev() -> None
        — configure structlog for development: ConsoleRenderer with colors,
          human-readable timestamps, log level filter
        WHY: dev output should be readable by humans; prod output by machines
    - get_bound_logger(name: str, **initial_context) -> structlog.stdlib.BoundLogger
        — return structlog.get_logger(name).bind(**initial_context)
        WHY: binding context at logger creation means every log from this logger
        automatically includes pipeline_name, environment, etc. — zero boilerplate per call
    - demonstrate_context_binding(logger: structlog.stdlib.BoundLogger) -> None
        — show logger.bind(job_id="j-001") → new logger with job_id on every line
        — show logger.unbind("job_id") → removes the key
        — show structlog.contextvars.bind_contextvars() → thread-local context for web/async
    - add_duration_processor(logger, method, event_dict: dict) -> dict
        — custom structlog processor: if event_dict has "start_time", compute
          duration_ms = (time.time() - start_time) * 1000 and add to event_dict
        WHY: processors are the structlog superpower — inject computed fields into every
        log line without changing call sites
    - log_dataframe_operation(logger: structlog.stdlib.BoundLogger, operation: str,
        input_rows: int, output_rows: int, duration_ms: float) -> None
        — emit a structured log for a dataframe transformation:
          {event: "dataframe_op", operation, input_rows, output_rows,
           rows_dropped: input-output, drop_pct: ..., duration_ms}
  Main block:
    - configure_structlog_prod writing to LOG_DIR/03_structlog_prod.json
    - create bound logger with pipeline_name="iot-ingest", environment="dev"
    - simulate 4 dataframe operations (filter, dedupe, enrich, aggregate)
      using log_dataframe_operation, with realistic row counts and timing
    - demonstrate_context_binding()
    - reconfigure for dev (ConsoleRenderer), re-run 2 operations so user sees both formats
    - print "Check LOG_DIR/03_structlog_prod.json for machine-readable output"

04_logging_patterns_for_data_pipelines.py
  Purpose: Production logging patterns every data engineer needs — retry, batch, audit, exceptions
  Key concepts: exc_info=True, context managers for timing, audit trail, slow query detection
  Functions:
    - get_log_dir() -> Path
    - get_pipeline_logger(name: str, log_file: Path) -> logging.Logger
        — JSON logger with run_id injected via LoggerAdapter
    - log_retry(logger: logging.Logger, attempt: int, max_attempts: int,
        error: Exception, next_retry_in_s: float) -> None
        — INFO if attempt < max_attempts, ERROR if final attempt
        — include: attempt, max_attempts, error_type, error_msg, next_retry_in_s
        WHY: retry logs without this context are useless — "retrying" tells you nothing
    - log_batch_progress(logger: logging.Logger, batch_num: int,
        total_batches: int, records_done: int, records_total: int) -> None
        — emit INFO with: batch_num, total_batches, pct_complete, records_done,
          records_total, eta_batches_remaining
        WHY: long-running jobs without progress logs look hung — ops teams kill them
    - log_slow_query(logger: logging.Logger, query_id: str,
        duration_ms: float, threshold_ms: float = 1000,
        query_preview: str = "") -> None
        — emit WARNING if duration_ms > threshold_ms
        — include: query_id, duration_ms, threshold_ms, query_preview (first 100 chars)
        WHY: slow query logs are the fastest path to finding the 1% of queries
        causing 80% of latency
    - log_pipeline_audit(logger: logging.Logger, stage: str, run_id: str,
        input_count: int, output_count: int, dropped_count: int,
        duration_ms: float) -> None
        — emit INFO audit entry — every stage accounts for every record
        WHY: audit logs answer "where did my 50k records go?" in a 3-stage pipeline
        They prove data lineage for compliance and debugging
    - operation_timer(logger: logging.Logger, operation_name: str)
        — context manager using @contextmanager
        — on entry: log INFO "{operation_name} started"
        — on normal exit: log INFO "{operation_name} completed" with duration_ms
        — on exception: log ERROR "{operation_name} failed" with duration_ms + exc_info=True
          then re-raise
        WHY: this pattern beats manual try/except/finally around every operation
    - setup_performance_logger(name: str, perf_log_file: Path) -> logging.Logger
        — separate logger that goes ONLY to a performance log file, not console
        WHY: mixing timing data into the main log creates noise — performance analysis
        needs a clean file with only timing records
  Main block:
    - simulate a complete ETL pipeline with all patterns:
        extract: 3 retry attempts (first 2 fail with simulated ConnectionError)
        transform: 8 batches of 1000 records each with batch progress logs
        transform: 2 slow queries detected (threshold 500ms)
        load: audit log showing input=8000, output=7850, dropped=150
        bonus: one operation_timer wrapping a deliberate exception to show ERROR path
    - write to LOG_DIR/04_patterns.log
    - at end: parse the log file, count by log level, print summary

05_log_aggregation_and_ops.py
  Purpose: Log management at scale — rotation, sampling, schema contracts, shipping config
  Key concepts: RotatingFileHandler vs WatchedFileHandler, sampling filters,
    log schema as a contract, CloudWatch/Splunk config (shown, not wired)
  Functions:
    - get_log_dir() -> Path
    - build_rotating_handler(log_file: Path, max_size_mb: int = 100,
        backup_count: int = 7) -> logging.handlers.RotatingFileHandler
        WHY: RotatingFileHandler is the right default for pipeline logs —
        bounded disk usage, predictable file names, no time-zone edge cases
    - class SamplingFilter(logging.Filter):
        — __init__(self, sample_rate: float = 0.10)
        — filter(self, record) -> bool
          — always pass WARNING and above; pass DEBUG/INFO only sample_rate fraction
          — use random.random() < sample_rate for the decision
        WHY: a busy pipeline emitting 100k DEBUG lines/min will fill disk and overwhelm
        a log aggregator — sampling at 10% still gives statistical visibility
    - define_log_schema() -> dict
        — return the JSON schema contract for pipeline log entries:
          required fields: timestamp (ISO8601), level, logger, message, run_id
          optional fields: stage, duration_ms, records_in, records_out,
                           error_type, query_id, batch_num
        WHY: a schema contract lets ops, SRE, and data engineering agree on what
        every log line must contain — it becomes the API between your code and
        your monitoring system
    - validate_log_entry(entry: dict, schema: dict) -> tuple[bool, list[str]]
        — return (is_valid, list_of_missing_required_fields)
    - show_cloudwatch_handler_config(log_group: str, stream_name: str) -> str
        — return a formatted string showing how to add watchtower handler
        — code is NOT executed (no AWS) but is printed as a ready-to-use snippet
        WHY: watchtower is the standard Python → CloudWatch bridge in AWS data pipelines
    - show_splunk_handler_config(splunk_host: str, index: str) -> str
        — same pattern for Splunk HEC
    - build_log_rotation_config(log_dir: Path,
        max_size_mb: int = 100, backup_count: int = 7) -> dict
        — return recommended config dict for ops documentation
  Main block:
    - create logger with RotatingFileHandler + SamplingFilter(0.10)
    - emit 200 DEBUG, 50 INFO, 10 WARNING, 5 ERROR log lines
    - show how many were actually written (sampling in effect)
    - validate 3 sample log entries against schema: 1 valid, 1 missing run_id, 1 missing stage
    - print CloudWatch handler config snippet
    - print Splunk handler config snippet
    - print rotation config dict

===== README =====

Generate README.md for the 10_python_logging directory with these exact sections:

1. Prerequisites
   pip install structlog python-json-logger
   Optional: pip install watchtower splunk-handler  (file 05 config snippets only)
   LOG_DIR env var (optional — defaults to /tmp/studybook/logs)

2. Phase 1 — Setup Scripts: one entry per file (01–05) with:
   - exact run command: python setup\01_logging_fundamentals.py
   - 2-sentence what it does
   - 1-sentence key takeaway

3. Phase 2 — Capstone: run order with exact commands:
   python capstone\pipeline_logger.py   (import test — runs self-check)
   python capstone\example_pipeline.py
   pytest capstone\test_pipeline_logger.py -v

4. Why This Matters for Interviews section:
   - 3 bullet points on what Toyota/Capital One interviewers look for in logging answers
   - Expected answer pattern for "How do you observe a production pipeline?"

===== CAPSTONE PROJECT =====

The capstone is a COMPLETE, FULLY RUNNABLE reusable logging library.
Every file must be complete — no placeholders, no TODO, no pass statements.
This library will be used by future tutorials in this studybook system.

Title: pipeline_logger — A Reusable Logging Library for Data Pipelines

---

capstone/pipeline_logger.py — THE LIBRARY (complete, importable module)
  Purpose: Reusable logging module any studybook pipeline can import
  This is a library file — it has no main() demo block of its own.
  All functions/classes are fully implemented.

  Module-level constants:
    DEFAULT_LOG_DIR = Path(os.getenv("LOG_DIR", "/tmp/studybook/logs"))
    DEFAULT_ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")

  Functions and classes:

    - get_log_dir(subdir: str = "") -> Path
        — return DEFAULT_LOG_DIR / subdir, creating it if needed

    - generate_run_id() -> str
        — 8-char hex from uuid4

    - class PipelineLogger(logging.LoggerAdapter):
        """
        LoggerAdapter that injects run_id, pipeline_name, and environment
        into every log record automatically.
        WHY: LoggerAdapter is the stdlib way to add persistent context without
        subclassing Logger or wrapping every call site.
        """
        def __init__(self, logger: logging.Logger, run_id: str,
                     pipeline_name: str, environment: str):
            super().__init__(logger, {})
            self.run_id = run_id
            self.pipeline_name = pipeline_name
            self.environment = environment

        def process(self, msg: str, kwargs: dict) -> tuple[str, dict]:
            # merge persistent context into extra dict
            extra = kwargs.setdefault("extra", {})
            extra.update(run_id=self.run_id,
                         pipeline_name=self.pipeline_name,
                         environment=self.environment)
            return msg, kwargs

    - get_pipeline_logger(pipeline_name: str, run_id: str | None = None,
        environment: str = DEFAULT_ENVIRONMENT,
        log_file: Path | None = None,
        level: int = logging.INFO) -> PipelineLogger
        — create underlying Logger with:
            console handler (INFO, human format for dev / JSON for prod)
            file handler (DEBUG, JSON, RotatingFileHandler 50MB/5 backups)
            if log_file is None: write to get_log_dir() / f"{pipeline_name}.log"
        — wrap in PipelineLogger and return
        WHY: single entry point — callers import get_pipeline_logger and nothing else

    - @contextmanager
      log_stage(logger: PipelineLogger, stage_name: str,
        **context_fields) -> Generator[PipelineLogger, None, None]
        — yields a logger bound with stage=stage_name + any context_fields
        — on entry: logs INFO "stage started" with stage_name
        — on normal exit: logs INFO "stage completed" with duration_ms
        — on exception: logs ERROR "stage failed" with duration_ms and exc_info=True,
          then re-raises the original exception
        WHY: context manager pattern eliminates boilerplate try/except/finally
        around every pipeline stage — 3 lines instead of 10

    - log_dataframe_stats(logger: PipelineLogger, stage_name: str,
        row_count: int, col_count: int,
        null_counts: dict[str, int] | None = None,
        sample_cols: list[str] | None = None) -> None
        — emit INFO with shape, null summary, and column list
        WHY: logging dataframe shape after every transformation catches silent data loss

    - def configure_for_environment(environment: str) -> None
        — "dev":     root logger at DEBUG, ConsoleRenderer (structlog-style readable output)
        — "staging": root logger at INFO, JSON to stdout + file
        — "prod":    root logger at WARNING, JSON to file only, SamplingFilter on DEBUG
        WHY: environment-aware logging prevents verbose dev logs from drowning prod systems

---

capstone/example_pipeline.py — COMPLETE DEMO FILE
  Purpose: Show pipeline_logger in action across a realistic 4-stage ETL
  Import everything from capstone/pipeline_logger.py

  Functions:
    - extract(logger: PipelineLogger) -> list[dict]
        — use log_stage(logger, "extract") as ctx:
        — simulate fetching 1000 records (sleep 0.05s to fake latency)
        — log_dataframe_stats: 1000 rows, 5 cols
        — return list of 1000 synthetic dicts
    - validate(logger: PipelineLogger, records: list[dict]) -> list[dict]
        — use log_stage(logger, "validate") as ctx:
        — filter out records missing required fields (inject 30 bad records)
        — log_dataframe_stats: before 1000, after 970
        — return 970 valid records
    - transform(logger: PipelineLogger, records: list[dict]) -> list[dict]
        — use log_stage(logger, "transform") as ctx:
        — enrich each record (add computed field)
        — log_dataframe_stats: 970 rows in, 970 rows out
        — simulate a slow transform (sleep 0.1s) — logs duration
        — return transformed records
    - load(logger: PipelineLogger, records: list[dict]) -> int
        — use log_stage(logger, "load") as ctx:
        — write records to LOG_DIR/example_output.jsonl (one JSON per line)
        — return count written
    - run_pipeline() -> None
        — generate run_id, create PipelineLogger
        — call extract → validate → transform → load in sequence
        — after load: parse the pipeline log file, call summarize_run equivalent,
          print: run_id, stages completed, total records in/out, total duration
        — demonstrate the failure path: call log_stage for a "publish" stage that
          raises ValueError("Destination unavailable") — show ERROR log with traceback

  Main block:
    - run_pipeline()

---

capstone/test_pipeline_logger.py — COMPLETE PYTEST FILE
  Purpose: Verify pipeline_logger behaviour without AWS or external dependencies
  Import from pipeline_logger and example_pipeline as needed

  Fixtures:
    - @pytest.fixture
      tmp_log_dir(tmp_path) -> Path
          — return tmp_path / "logs", create it
          — monkeypatch LOG_DIR env var to tmp_path / "logs"

  Test functions:

    - test_run_id_present_in_all_records(tmp_log_dir):
        — create PipelineLogger(pipeline_name="test", run_id="abc123", environment="test",
            log_file=tmp_log_dir/"test.log")
        — emit 5 log lines at different levels
        — parse the log file as JSON lines
        — assert every record has "run_id" == "abc123"

    - test_stage_logs_duration_on_success(tmp_log_dir, capfd):
        — create logger, use log_stage(logger, "my_stage"):
            logger.info("doing work")
        — parse log output (capture stdout or log file)
        — assert a record with stage="my_stage" and "completed" in message exists
        — assert that record has a numeric duration_ms >= 0

    - test_stage_logs_error_on_exception(tmp_log_dir):
        — create logger, wrap log_stage(logger, "failing_stage") around
            raise RuntimeError("deliberate failure")
        — with pytest.raises(RuntimeError): (exception must re-raise)
        — parse log file
        — assert a record with "failed" in message and level="ERROR" exists
        — assert that record has exc_info or "RuntimeError" in the message

    - test_json_output_is_parseable(tmp_log_dir):
        — create logger writing to tmp_log_dir/"parseable.log"
        — emit 3 log lines
        — for each line in the file: json.loads(line) must not raise
        — assert len(records) == 3

    - test_pipeline_name_in_all_records(tmp_log_dir):
        — create PipelineLogger with pipeline_name="my-etl"
        — emit 3 log lines
        — parse log file
        — assert every record has pipeline_name == "my-etl"

    - test_log_dataframe_stats_emits_shape(tmp_log_dir):
        — create logger
        — call log_dataframe_stats(logger, "filter", row_count=500, col_count=8)
        — parse log file
        — assert a record exists containing row_count=500 and col_count=8

---

capstone/brief.md — GENERATE THIS LAST
  Title: pipeline_logger — Reusable Logging Library
  Write the brief AFTER all code files are generated.
  Include: scenario, what was built, how to run, acceptance criteria checklist,
  and a "How to reuse in other tutorials" section showing the 3-line import pattern:
    from pathlib import Path
    import sys; sys.path.insert(0, str(Path(__file__).parent.parent / "capstone"))
    from pipeline_logger import get_pipeline_logger, log_stage

===== INFRASTRUCTURE NOTES =====

Pure Python — no AWS, no Docker required.
Install: pip install structlog python-json-logger
Optional (file 05 config snippets only): pip install watchtower splunk-handler
All file output goes to LOG_DIR env var or /tmp/studybook/logs/ by default.
CloudWatch and Splunk handler code in file 05 is printed as config snippets — not executed.
No credentials needed for any file.
No cleanup required — all output is local files.

===== START =====

Acknowledge these instructions. Confirm you understand:
1. Every file is COMPLETE and FULLY RUNNABLE — no placeholders, no TODO, no pass statements
2. pipeline_logger.py is a real importable library — example_pipeline.py imports from it
3. test_pipeline_logger.py tests real behaviour — all 6 tests must be independently runnable
4. After acknowledgment, wait for me to say "generate file 01"

===
