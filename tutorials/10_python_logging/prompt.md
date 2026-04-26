# ChatGPT Prompt — Python Logging Tutorial
# Paste everything between the === markers into ChatGPT

===

TOPIC: Python Logging for Data Engineers
SLUG: python-logging
PRIORITY: Toyota Interview Prep
INFRASTRUCTURE: Pure Python (no AWS, no Docker) — stdlib logging + structlog

===== CODING STANDARDS =====

FILE HEADER:
# ============================================================
# Topic   : Python Logging for Data Engineers
# File    : NN_filename.py
# Covers  : one-line description
# Prereqs : pip install structlog python-json-logger | no AWS needed
# Run     : python filename.py
# ============================================================

COMMENTS: Explain WHY. Logging is the #1 debugging tool in production. Explain
why structured JSON logging beats print statements and plain text logs. Explain
propagation, handler hierarchy, performance implications of logging.
No env vars required — all config shown inline.

===== FILES TO GENERATE =====

01_logging_fundamentals.py
  Purpose: Python stdlib logging — hierarchy, handlers, formatters, levels — the right way
  Key concepts: logger hierarchy (root vs named), propagation, handler vs logger level,
    why print() is not logging, performance cost of string formatting before level check
  Functions:
    - get_basic_logger(name, level=logging.INFO) → logging.Logger — minimal correct setup
    - get_file_logger(name, log_file, max_bytes=10_000_000, backup_count=5) → Logger
      — RotatingFileHandler, explain why size-based rotation beats time-based for pipelines
    - get_dual_logger(name, log_file) → Logger — console (INFO) + file (DEBUG) handlers
    - demonstrate_hierarchy() — show parent/child loggers, propagation, how to stop it
    - demonstrate_level_filter() — show logger vs handler level interaction (common gotcha)
    - bad_vs_good_formatting() — show % lazy vs f-string (expensive) vs % args (cheap) pattern
  Main block: set up dual logger, run a simulated pipeline loop with DEBUG/INFO/WARNING/ERROR,
    show log file content, explain what each line means

02_structured_json_logging.py
  Purpose: Structured logging — JSON output, correlation IDs, context propagation
  Key concepts: why structured logs (grep-able, Splunk/CloudWatch parseable),
    python-json-logger, context dict pattern, correlation ID per pipeline run
  Functions:
    - get_json_logger(name, level=logging.INFO) → Logger — python-json-logger JsonFormatter
    - add_pipeline_context(logger, run_id, pipeline_name, environment) → Logger
      — add persistent fields to every log line from this logger
    - log_with_extra(logger, level, message, **fields)
      — emit structured log with arbitrary extra fields merged into JSON
    - generate_run_id() → str — uuid4 short form for correlation
    - parse_json_log_file(log_file) → list[dict] — read back structured logs for analysis
    - summarize_run(log_file, run_id) → dict — filter by run_id, count by level, find errors
  Main block: simulate a 3-stage pipeline (extract→transform→load), emit structured JSON logs
    with run_id throughout, parse log file, print run summary

03_structlog_advanced.py
  Purpose: structlog — the modern way to do structured logging in Python data pipelines
  Key concepts: processors pipeline, bound loggers, context variables, async compatibility
  Functions:
    - configure_structlog(json_output=True, level="INFO")
      — production-ready structlog config with timestamp, level, caller info
    - get_bound_logger(name, **initial_context) → structlog.BoundLogger
      — bind context at creation time (pipeline_name, env, etc.)
    - demonstrate_context_binding() — show bind() and unbind() for request/job scoping
    - demonstrate_processor_pipeline() — custom processor that adds duration_ms to log
    - log_dataframe_operation(logger, operation, input_rows, output_rows, duration_ms)
      — standard DE operation log entry
    - configure_dev_vs_prod(environment: str) → None
      — dev: colored human-readable; prod: JSON for log aggregator
  Main block: configure for prod JSON output, run a simulated Spark-like transformation
    pipeline with per-stage structured logs, show how logs look in both dev and prod mode

04_logging_patterns_for_data_pipelines.py
  Purpose: Production logging patterns specific to data engineering — retries, batches, exceptions
  Key concepts: exception logging (exc_info=True), retry logging, batch progress,
    slow query detection, pipeline audit trail
  Functions:
    - log_retry(logger, attempt, max_attempts, error, retry_delay_s)
      — standard retry log pattern with exponential backoff context
    - log_batch_progress(logger, batch_num, total_batches, records_processed, records_total)
      — progress tracking for long-running batch jobs
    - log_slow_query(logger, query_hash, duration_ms, threshold_ms=1000)
      — emit WARNING with query excerpt when over threshold
    - log_pipeline_audit(logger, stage, input_count, output_count, dropped_count, run_id)
      — audit trail entry: every stage logs what went in and came out
    - exception_context_manager(logger, operation_name)
      — context manager: logs entry, success with duration, or ERROR with full traceback
    - setup_performance_logger(name) → Logger
      — separate logger for timing data (goes to metrics file, not main log)
  Main block: simulate a complete ETL pipeline with all patterns active — extract (with retry),
    transform (with batch progress + slow operation), load (with audit), exception mid-run

05_log_aggregation_and_ops.py
  Purpose: Log management at scale — log rotation, shipping to CloudWatch/Splunk, filtering
  Key concepts: WatchedFileHandler vs RotatingFileHandler, watchtower (CloudWatch Logs),
    log sampling for high-volume pipelines, log schema contracts
  Functions:
    - configure_cloudwatch_handler(logger, log_group, stream_name, region)
      — add watchtower handler to existing logger (requires: pip install watchtower)
    - configure_splunk_handler(logger, splunk_host, token, index)
      — add splunk-handler for HEC (requires: pip install splunk-handler)
    - sample_high_volume_logs(logger, record, sample_rate=0.01)
      — custom filter: log only 1% of DEBUG records under load (cost/volume control)
    - define_log_schema() → dict — JSON schema for pipeline log entries (contract for ops team)
    - validate_log_entry(entry: dict, schema: dict) → bool — check entry matches schema
    - build_log_rotation_config(log_dir, max_size_mb=100, backup_count=7) → dict
      — recommended rotation config for data pipeline logs
  Main block: set up RotatingFileHandler, emit high-volume logs with sampling filter,
    show CloudWatch handler config (commented — needs AWS), print log schema contract

===== CAPSTONE PROJECT =====

capstone/brief.md
  Title: Pipeline-Ready Logging Library
  Scenario: Build a reusable logging module that any data pipeline in the studybook
    codebase can import. It must handle structured JSON output, correlation IDs,
    performance tracking, and CloudWatch shipping.
  What to build:
    - pipeline_logger.py: reusable module with:
        get_pipeline_logger(pipeline_name, run_id=None, environment="dev") → BoundLogger
        log_stage(logger, stage_name) — context manager: logs entry/exit with duration
        log_dataframe(logger, df, stage_name) — logs shape, null counts, sample schema
        configure_for_environment(env: str) — dev=pretty, staging/prod=JSON+CloudWatch
    - example_pipeline.py: import pipeline_logger, run a 4-stage ETL with full logging
    - test_pipeline_logger.py: pytest tests:
        test correlation ID appears in all log records
        test stage context manager logs duration on normal exit
        test stage context manager logs ERROR on exception without raising
        test JSON output is parseable

  Acceptance criteria:
    - All log lines from a single pipeline run share the same run_id
    - JSON output is valid and parseable by json.loads()
    - Stage manager logs both success (with ms) and failure (with traceback) correctly
    - Tests pass without AWS credentials

capstone/capstone.py — example_pipeline.py (as above)
capstone/test_capstone.py — pytest file

===== INFRASTRUCTURE NOTES =====

Pure Python — no AWS, no Docker required.
Install: pip install structlog python-json-logger
Optional (file 05 only): pip install watchtower splunk-handler
All output to stdout or /tmp/studybook/logs/ or LOG_DIR env var.
CloudWatch handler code shown but commented — requires AWS credentials.

===== START =====

Acknowledge these instructions, then wait for me to say "generate file 01".

===
