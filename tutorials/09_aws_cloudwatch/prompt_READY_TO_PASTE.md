# READY TO PASTE INTO CHATGPT
# Copy everything between the === markers below (include the === lines themselves as delimiters)
# Open a FRESH ChatGPT chat — do not reuse a previous topic's chat
# After ChatGPT acknowledges, say: "generate file 01"
# Then: "generate file 02" ... "generate file 03" ... "generate file 04" ... "generate file 05"
# Then: "generate readme"
# Then: "generate capstone file emit_pipeline_metrics.py"
# Then: "generate capstone file setup_alarms.py"
# Then: "generate capstone file build_dashboard.py"
# Then: "generate capstone file insights_queries.py"
# Then: "generate capstone file capstone.py"
# Then: "generate capstone file cleanup.py"
# Then: "generate capstone file test_capstone.py"
# Then: "generate capstone brief.md"
# Save each file immediately after ChatGPT generates it.
# ============================================================

===

You are generating educational Python tutorial files for a Senior Data Engineer
personal study system. Every file you generate must be:
- COMPLETE and FULLY RUNNABLE — no placeholders, no TODO comments, no `pass` statements,
  no "implement this yourself" notes, no skeleton functions
- Production-quality with heavy WHY comments
- Tested against real AWS (boto3)

If a file would be too long for one response, continue in the next message without
waiting to be asked. Never truncate a file mid-function.

TOPIC: AWS CloudWatch for Data Engineers
SLUG: aws-cloudwatch
PRIORITY: Toyota Interview Prep
INFRASTRUCTURE: AWS (boto3, real AWS account, profile="study")

===== CODING STANDARDS =====

FILE HEADER — every file starts with:
# ============================================================
# Topic   : AWS CloudWatch for Data Engineers
# File    : NN_filename.py
# Covers  : one-line description
# Prereqs : pip install boto3 | AWS credentials | profile: study
# Run     : python filename.py
# ============================================================

COMMENTS: Explain WHY. CloudWatch is the operational backbone — explain metric
namespaces, dimensions, resolution, and cost implications of high-resolution metrics.

ENVIRONMENT VARIABLES — declare at the top of every file:
  AWS_REGION          — default "us-east-1"
  AWS_PROFILE         — default "study"
  CW_NAMESPACE        — default "StudyBook/Pipeline"
  CW_LOG_GROUP_NAME   — default "/studybook/pipeline"
  CW_ALARM_SNS_ARN    — optional, skip alarm SNS wiring if not set

DOCSTRINGS — every function must have:
  - One-line summary
  - WHY field: the senior insight behind this approach
  - Args with types and descriptions
  - Returns with type
  - Raises if applicable

CODE RULES:
  - Python 3.11+, type hints on all signatures
  - os.environ for ALL config — never hardcode
  - Specific exception handling — never bare except:
  - boto3 ClientError caught by Error.Code, not by message string
  - Every file ends with if __name__ == "__main__": that runs a full demo

CLEANUP — MANDATORY IN EVERY FILE:
  - Every main() that creates AWS resources wraps the demo in try/finally
  - cleanup() is always in the finally block — it runs even if the demo crashes
  - cleanup() catches ResourceNotFoundException / ResourceNotFound and continues silently
  - Print ⚠️  COST WARNING immediately after creating any billable resource
  - Print ✅  Cleanup complete. No ongoing charges. at end of every cleanup()
  - CloudWatch resources that cost money: alarms ($0.10/alarm/month),
    dashboards ($3/dashboard/month), log groups ($0.50/GB ingested + storage),
    custom metrics ($0.30/metric/month after first 10)

===== FILES TO GENERATE =====

01_custom_metrics.py
  Purpose: Emit and query custom CloudWatch metrics — the foundation of operational visibility
  Key concepts: namespaces, dimensions, metric resolution (standard=60s vs high-res=1s),
    StatisticSets for batching, cost ($0.30/metric/month beyond free tier)
  Functions:
    - get_cw_client() → boto3.client
        WHY: centralise session creation so profile/region comes from env
    - put_metric(namespace: str, metric_name: str, value: float, unit: str,
        dimensions: dict[str,str], high_resolution: bool = False) → None
        WHY: high_resolution=True costs 3× — explain when 1s resolution is worth it
    - put_metric_batch(namespace: str, metrics: list[dict]) → None
        — batch up to 20 metrics per PutMetricData call (API limit)
        WHY: batching reduces API call count and cost
    - put_statistic_set(namespace: str, metric_name: str, dimensions: dict[str,str],
        sample_count: int, sum: float, min_val: float, max_val: float) → None
        WHY: pre-aggregated stats avoid sending every raw data point — saves API calls
        for high-throughput pipelines
    - get_metric_statistics(namespace: str, metric_name: str, dimensions: dict[str,str],
        start: datetime, end: datetime, period_s: int, stat: str) → list[dict]
        — return list of {Timestamp, value, Unit}
    - list_metrics_in_namespace(namespace: str) → list[dict]
        — paginated; return [{MetricName, Dimensions}]
    - calculate_metric_cost(metric_count: int) → dict
        — return {free_tier: 10, billable: max(0, metric_count-10),
                  monthly_usd: billable * 0.30, note: str}
  Main block:
    - emit 50 synthetic "records_processed" data points spanning 2 hours (use
      datetime arithmetic to backfill timestamps, not time.sleep)
    - emit 1 StatisticSet representing a batch of 1000 records
    - retrieve hourly Average for the last 3 hours, print as table
    - list all metrics in the namespace
    - print cost calculation for 10 and 50 custom metrics
    - cleanup: no persistent resources created by this file (metrics expire naturally)

02_log_groups_and_insights.py
  Purpose: CloudWatch Logs — structured logging, log groups, retention, Logs Insights queries
  Key concepts: log groups vs log streams, structured JSON logs, retention policies,
    Logs Insights query syntax, cost ($0.50/GB ingestion + $0.005/GB storage)
  Functions:
    - get_logs_client() → boto3.client
    - create_log_group(group_name: str, retention_days: int = 30) → None
        WHY: always set retention — unlimited retention = unlimited cost
    - ensure_log_stream(group_name: str, stream_name: str) → None
        — create stream if it doesn't exist; idempotent
    - put_log_events(group_name: str, stream_name: str, messages: list[str]) → None
        — handle sequenceToken automatically (required for subsequent calls)
        WHY: sequenceToken is a gotcha — omitting it causes InvalidSequenceTokenException
    - put_structured_log(group_name: str, stream_name: str, event: dict) → None
        — json.dumps event, add timestamp, call put_log_events
    - query_logs_insights(group_name: str, query_string: str,
        start: datetime, end: datetime, limit: int = 100) → list[dict]
        — start query, poll with 2s sleep until Complete, return results
        WHY: Insights is async — must poll; billed per GB scanned so keep windows short
    - common_queries() → dict[str, str]
        — return 4 named query strings:
          "pipeline_errors": filter @message like /ERROR/ | sort @timestamp desc
          "slow_jobs": filter duration_ms > 5000 | stats avg(duration_ms) by job_name
          "hourly_volume": stats count(*) as events by bin(1h)
          "error_rate": stats sum(is_error) / count(*) * 100 as error_pct by bin(1h)
    - set_retention_policy(group_name: str, days: int) → None
    - delete_log_group(group_name: str) → None — idempotent
  Main block:
    - create log group with 7-day retention
    - emit 30 structured JSON log events: mix of INFO (pipeline stage completions)
      and ERROR (simulated failures) with fields: level, job_name, stage,
      duration_ms, records_in, records_out, error_msg (on errors)
    - run all 4 common_queries() against the last hour, print results
    - cleanup in finally: delete_log_group

03_alarms_and_composite_alarms.py
  Purpose: CloudWatch Alarms — metric alarms, anomaly detection, composite alarms
  Key concepts: threshold vs anomaly detection, alarm states (OK/ALARM/INSUFFICIENT_DATA),
    composite alarms for reducing alert noise, SNS notifications
  Functions:
    - get_cw_client() → boto3.client
    - create_metric_alarm(name: str, namespace: str, metric: str,
        dimensions: dict[str,str], threshold: float, comparison: str,
        evaluation_periods: int, period_s: int, statistic: str,
        sns_arn: str | None = None) → str
        — return alarm ARN; print ⚠️ COST: $0.10/month
        comparison values: GreaterThanThreshold / LessThanThreshold etc.
    - create_anomaly_detection_alarm(name: str, metric_name: str, namespace: str,
        dimensions: dict[str,str], band_width: float = 2.0) → str
        — create AnomalyDetector then alarm using ANOMALY_DETECTION_BAND
        WHY: anomaly detection adapts to weekly patterns — better than static thresholds
        for pipelines with variable load
    - create_composite_alarm(name: str, alarm_rule: str,
        sns_arn: str | None = None) → str
        — alarm_rule syntax: "ALARM(\"alarm-name-1\") OR ALARM(\"alarm-name-2\")"
        WHY: composite alarms reduce SNS noise — only alert when 2+ signals fire together
    - get_alarm_state(alarm_name: str) → dict
        — return {StateValue, StateReason, StateUpdatedTimestamp}
    - get_alarm_history(alarm_name: str, days: int = 7) → list[dict]
    - list_alarms_in_state(state: str = "ALARM") → list[str]
        — return alarm names in given state
    - delete_alarm(name: str) → None — idempotent
    - delete_alarms(names: list[str]) → None — batch delete
  Main block:
    - emit some synthetic metrics into the namespace so alarms have data
    - create 3 metric alarms:
        records_low: records_processed < 500 for 2 × 5min periods
        error_spike: error_count > 0 for 1 × 5min period
        latency_high: duration_ms p90 > 30000 for 2 × 5min periods
    - create composite alarm: pipeline_unhealthy = error_spike OR latency_high
    - print state of all 4 alarms
    - cleanup in finally: delete all 4 alarms

04_dashboards_and_embedded_metrics.py
  Purpose: CloudWatch Dashboards and Embedded Metric Format (EMF)
  Key concepts: dashboard JSON widget spec, EMF (emit metrics via logs — avoids PutMetricData cost),
    difference: EMF metrics are free up to log ingestion cost vs $0.30/metric/month for custom
  Functions:
    - get_cw_client() → boto3.client
    - get_logs_client() → boto3.client
    - build_metric_widget(title: str, metrics: list[list], period_s: int,
        stat: str, width: int = 12, height: int = 6) → dict
        — metrics format: [["Namespace","MetricName",{"stat":"Average"}], ...]
        WHY: understanding widget JSON is needed to build dashboards programmatically
    - build_text_widget(markdown: str, width: int = 12, height: int = 3) → dict
    - build_alarm_widget(alarm_arns: list[str], width: int = 12, height: int = 4) → dict
    - create_dashboard(name: str, widgets: list[dict]) → str
        — arrange widgets in a grid (x/y/width/height), return dashboard URL
        — print ⚠️ COST: $3.00/month per dashboard
    - get_dashboard_url(name: str, region: str) → str
        — return: https://console.aws.amazon.com/cloudwatch/home?region={region}#dashboards:name={name}
    - put_emf_metric(log_group: str, stream_name: str, namespace: str,
        metrics: dict[str, float], dimensions: dict[str, str]) → None
        — write a valid EMF-formatted JSON log line (includes _aws.CloudWatchMetrics block)
        WHY: EMF lets you emit metrics as structured logs — no extra PutMetricData call,
        no per-metric charge beyond log ingestion, zero code change from regular logging
    - delete_dashboard(name: str) → None — idempotent
  Main block:
    - create log group for EMF
    - emit 20 EMF log entries (simulating 20 pipeline runs with records_in, records_out,
      duration_ms, error_count dimensions: pipeline_name, environment)
    - build a 4-widget dashboard:
        widget 1: records_in and records_out line graph (12×6)
        widget 2: duration_ms average bar chart (12×6)
        widget 3: error_count sum (12×4)
        widget 4: text widget — "Pipeline Health — StudyBook Tutorial" (24×3)
    - print dashboard URL
    - cleanup in finally: delete_dashboard, delete log group

05_container_and_lambda_monitoring.py
  Purpose: Monitoring data pipelines in containers and Lambda — patterns for Toyota IoT stack
  Key concepts: metric filters (extract metrics from log text), subscription filters
    (stream logs to another destination), Lambda built-in metrics, cost calculator
  Functions:
    - get_cw_client() → boto3.client
    - get_logs_client() → boto3.client
    - create_metric_filter(log_group: str, filter_name: str, pattern: str,
        metric_namespace: str, metric_name: str,
        metric_value: str = "1", default_value: float = 0) → None
        — extract a metric from log text without changing application code
        WHY: metric filters let ops teams add observability to existing logs retroactively
        pattern examples: "ERROR", "[level=ERROR]", "{ $.level = \"ERROR\" }"
    - delete_metric_filter(log_group: str, filter_name: str) → None — idempotent
    - get_lambda_metrics(function_name: str, start: datetime, end: datetime,
        period_s: int = 300) → dict[str, list[dict]]
        — fetch Duration, Errors, Throttles, ConcurrentExecutions for the function
        — return dict keyed by metric name; each value is list of {Timestamp, value}
        WHY: these 4 metrics cover 90% of Lambda operational concerns
    - build_ecs_monitoring_queries() → dict[str, str]
        — return 3 Logs Insights queries for Container Insights:
          "task_cpu": query CpuUtilized grouped by TaskDefinitionFamily
          "task_memory": query MemoryUtilized grouped by TaskDefinitionFamily
          "task_errors": filter @message like /ERROR/ | count by TaskDefinitionFamily
    - calculate_cw_cost(custom_metrics: int, log_gb_month: float,
        dashboard_count: int, alarm_count: int,
        insights_gb_scanned: float = 0) → dict
        — return full line-item breakdown:
          metrics_cost: max(0, custom_metrics - 10) * 0.30
          log_ingestion_cost: log_gb_month * 0.50
          log_storage_cost: log_gb_month * 0.005 * 30  # approx 30-day retention
          dashboard_cost: dashboard_count * 3.00
          alarm_cost: alarm_count * 0.10
          insights_cost: insights_gb_scanned * 0.005
          total_monthly_usd: sum of all above
    - build_data_pipeline_runbook(pipeline_name: str, alarm_names: list[str]) → str
        — return a formatted markdown runbook string with:
          for each alarm: what it means, immediate action, escalation path
  Main block:
    - create a log group, emit 15 log events (mix of plain text with ERROR keyword
      and JSON structured events)
    - create a metric filter extracting error_count from ERROR keyword
    - wait 5 seconds, then query the metric to show it populated
    - print Lambda metrics structure (use a real function name from env or skip gracefully
      if LAMBDA_FUNCTION_NAME not set)
    - print ECS Insights query strings
    - print cost breakdown for: 50 custom metrics, 10GB logs/month,
      2 dashboards, 10 alarms, 5GB Insights scanned
    - print the runbook for a pipeline named "iot-ingest" with 3 alarms
    - cleanup in finally: delete metric filter, delete log group

===== README =====

Generate README.md for the 09_aws_cloudwatch directory with these exact sections:

1. Prerequisites — PowerShell commands to load environment and set env vars:
   - ..\..\env_setter.ps1 -NonInteractive
   - $env:AWS_PROFILE = "study"
   - $env:AWS_REGION = "us-east-1"
   - $env:CW_NAMESPACE = "StudyBook/Pipeline"
   - $env:CW_LOG_GROUP_NAME = "/studybook/pipeline"
   - Note: CW_ALARM_SNS_ARN is optional — alarms work without it

2. Phase 1 — Setup Scripts: one entry per file (01–05) with:
   - exact PowerShell run command
   - 2-sentence "what it does"
   - 1-sentence "key takeaway"

3. Phase 2 — Capstone: exact run order with commands:
   python capstone\emit_pipeline_metrics.py
   python capstone\setup_alarms.py
   python capstone\build_dashboard.py
   python capstone\insights_queries.py
   python capstone\capstone.py
   python capstone\test_capstone.py
   python capstone\cleanup.py

4. Emergency Cleanup — one-liner to delete everything if script crashes:
   python -c "
   import os, boto3
   cw = boto3.client('cloudwatch', region_name='us-east-1')
   logs = boto3.client('logs', region_name='us-east-1')
   for alarm in ['cw-records-low','cw-error-spike','cw-latency-high','cw-pipeline-unhealthy','capstone-records-low','capstone-errors','capstone-lag','capstone-unhealthy']:
       try: cw.delete_alarms(AlarmNames=[alarm]); print(f'Deleted alarm: {alarm}')
       except: pass
   for group in ['/studybook/pipeline', '/studybook/capstone/pipeline']:
       try: logs.delete_log_group(logGroupName=group); print(f'Deleted log group: {group}')
       except: pass
   for dash in ['studybook-pipeline', 'capstone-pipeline-health']:
       try: cw.delete_dashboards(DashboardNames=[dash]); print(f'Deleted dashboard: {dash}')
       except: pass
   print('Emergency cleanup done.')
   "

===== CAPSTONE PROJECT =====

The capstone is a COMPLETE, FULLY RUNNABLE Pipeline Observability Stack.
Every capstone file must have the same production quality as the setup files —
complete functions, WHY docstrings, try/finally cleanup. NO SHELLS. NO PLACEHOLDERS.

Title: Pipeline Observability Stack
Scenario: A simulated Kinesis → Glue → S3 pipeline runs hourly. You are building
  the complete CloudWatch observability layer for it from scratch.

Shared constants (put in each capstone file that needs them):
  NAMESPACE = os.getenv("CW_NAMESPACE", "StudyBook/CapstoneP")
  LOG_GROUP = os.getenv("CW_LOG_GROUP_NAME", "/studybook/capstone/pipeline")
  PIPELINE_NAME = "iot-ingest-hourly"
  AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
  AWS_PROFILE = os.getenv("AWS_PROFILE", "study")

---

capstone/emit_pipeline_metrics.py — COMPLETE FILE
  Purpose: Simulate 24 hours of hourly pipeline runs emitting realistic metrics
  Functions:
    - get_cw_client() → boto3.client
    - get_logs_client() → boto3.client
    - simulate_pipeline_run(hour_offset: int, inject_failure: bool = False) → dict
        — return realistic metrics for one run:
          records_in: random 8000-12000
          records_out: records_in * random(0.97, 1.0) unless inject_failure
          error_count: 0 normally; random(1,10) if inject_failure
          duration_ms: random 8000-25000 normally; random 35000-60000 if inject_failure
          lag_seconds: random 10-60 normally; random 400-900 if inject_failure
    - emit_run_metrics(run: dict, hour_offset: int) → None
        — use put_metric_data with Timestamp = now - timedelta(hours=hour_offset)
        — emit all 5 metrics as a batch (one PutMetricData call)
        — emit a structured JSON log event to LOG_GROUP for the same run
    - emit_24_hours(failure_hours: list[int] = [6, 18]) → None
        — loop hour 23 down to 0, call simulate_pipeline_run + emit_run_metrics
        — inject_failure=True for hours in failure_hours
        — print progress: "Hour -{hour}: records_in={n}, errors={e}, lag={l}s"
  Main block:
    - create log group with 7-day retention
    - call emit_24_hours(failure_hours=[4, 16])
    - print "Emitted 24 hours of pipeline metrics. 2 failure hours injected (4h ago, 16h ago)."

---

capstone/setup_alarms.py — COMPLETE FILE
  Purpose: Create 5 alarms covering all key pipeline health signals
  Functions:
    - get_cw_client() → boto3.client
    - create_alarm(name: str, metric: str, threshold: float, comparison: str,
        eval_periods: int, period_s: int, statistic: str,
        treat_missing: str = "notBreaching") → str
        — create alarm in NAMESPACE with dimension PipelineName=PIPELINE_NAME
        — print ⚠️ COST: $0.10/month per alarm
        — return alarm name
    - create_all_alarms() → list[str]
        — create and return names of all 5 alarms:
          1. "capstone-records-low": records_out < 7000, 2 of 2 periods, 5min
          2. "capstone-errors": error_count >= 1, 1 of 1 period, 5min
          3. "capstone-duration-high": duration_ms > 30000, 2 of 2 periods, 5min, stat=p90
          4. "capstone-lag-high": lag_seconds > 300, 1 of 1 period, 5min
          5. "capstone-unhealthy" (composite): ALARM("capstone-errors") OR ALARM("capstone-lag-high")
    - print_alarm_states(alarm_names: list[str]) → None
        — for each alarm: print name, StateValue, StateReason (truncated to 80 chars)
    - delete_all_alarms(alarm_names: list[str]) → None — idempotent, batch delete
  Main block (try/finally):
    - alarm_names = create_all_alarms()
    - wait 3 seconds
    - print_alarm_states(alarm_names)
    - print "5 alarms created. Check AWS Console > CloudWatch > Alarms."
    - NOTE: do NOT call delete in main — alarms are used by capstone.py and cleanup.py
    - Instead print: "Run capstone/cleanup.py to remove all resources."

---

capstone/build_dashboard.py — COMPLETE FILE
  Purpose: Build a 5-widget pipeline health dashboard
  Functions:
    - get_cw_client() → boto3.client
    - build_widgets(namespace: str, pipeline_name: str) → list[dict]
        — return exactly 5 widget dicts for a 24×n grid:
          1. Text header: "# IoT Ingest Pipeline — Health Dashboard" (x=0,y=0,w=24,h=2)
          2. Line graph: records_in + records_out last 24h (x=0,y=2,w=12,h=6)
          3. Line graph: duration_ms avg + p90 last 24h (x=12,y=2,w=12,h=6)
          4. Bar: error_count sum last 24h (x=0,y=8,w=12,h=6)
          5. Number: lag_seconds latest value (x=12,y=8,w=12,h=6)
    - create_pipeline_dashboard(name: str) → str
        — call create_dashboard with the 5 widgets
        — print ⚠️ COST: $3.00/month
        — return dashboard console URL
    - delete_dashboard(name: str) → None — idempotent
  Main block (try/finally — but see NOTE below):
    - url = create_pipeline_dashboard("capstone-pipeline-health")
    - print f"Dashboard created: {url}"
    - NOTE: do NOT delete in main — dashboard is used by capstone.py and cleanup.py
    - print "Run capstone/cleanup.py to remove all resources."

---

capstone/insights_queries.py — COMPLETE FILE
  Purpose: Run 4 Logs Insights queries against the 24h of emitted pipeline logs
  Functions:
    - get_logs_client() → boto3.client
    - run_query(log_group: str, query: str, hours_back: int = 24) → list[dict]
        — start_query, poll every 2s until Complete, return results
        — if results empty, return [] with a note
    - print_results(title: str, results: list[dict]) → None
        — print title + formatted table of results (up to 10 rows)
    - run_all_queries() → None
        — run and print these 4 queries against LOG_GROUP:
          Q1 "Slow pipeline runs (>25s)":
             filter duration_ms > 25000
             | fields @timestamp, job_name, duration_ms, records_in
             | sort duration_ms desc | limit 10
          Q2 "Error summary by hour":
             filter level = "ERROR"
             | stats count(*) as error_count by bin(1h)
             | sort bin desc
          Q3 "Daily throughput":
             stats sum(records_out) as total_out,
                   avg(records_in) as avg_in,
                   count(*) as runs by bin(24h)
          Q4 "Lag trend (5-min buckets)":
             filter ispresent(lag_seconds)
             | stats avg(lag_seconds) as avg_lag, max(lag_seconds) as peak_lag
               by bin(1h) | sort bin asc
  Main block:
    - run_all_queries()
    - print "Insights queries complete."

---

capstone/capstone.py — COMPLETE ORCHESTRATION FILE
  Purpose: Run the full capstone in order and print a final health report
  Functions:
    - run_step(step_name: str, fn: Callable) → bool
        — call fn(), catch any exception, print PASS or FAIL with duration
        — return True if passed
    - print_health_report(alarm_names: list[str], dashboard_url: str) → None
        — print a formatted report:
            PIPELINE OBSERVABILITY STACK — HEALTH REPORT
            ============================================
            Metrics emitted : 24 hourly runs (2 failures injected)
            Alarms created  : 5 (4 metric + 1 composite)
            Dashboard       : <url>
            Failure hours   : -4h ago, -16h ago
            Expected alarms : capstone-errors, capstone-lag-high, capstone-unhealthy → ALARM
            Run insights_queries.py to investigate the failure windows.
  Main block (try/finally with cleanup import):
    - Import and call the main functions from each capstone file in order:
      1. emit_pipeline_metrics: create log group + emit 24h data
      2. setup_alarms: create all 5 alarms, capture alarm_names
      3. build_dashboard: create dashboard, capture url
      4. insights_queries: run all 4 queries
      5. print_health_report(alarm_names, url)
    - finally: print "To delete all resources run: python capstone/cleanup.py"

---

capstone/cleanup.py — COMPLETE FILE
  Purpose: Delete every resource created by the capstone — idempotent, safe to run twice
  Functions:
    - get_cw_client() → boto3.client
    - get_logs_client() → boto3.client
    - delete_alarms() → None
        — delete these alarm names (idempotent):
          capstone-records-low, capstone-errors, capstone-duration-high,
          capstone-lag-high, capstone-unhealthy
        — print each deletion or "already gone"
    - delete_dashboard() → None
        — delete "capstone-pipeline-health" dashboard (idempotent)
    - delete_log_group() → None
        — delete LOG_GROUP ("/studybook/capstone/pipeline") (idempotent)
    - cleanup_all() → None
        — call delete_alarms(), delete_dashboard(), delete_log_group() in order
        — print ✅ Cleanup complete. No ongoing charges. at end
  Main block:
    - cleanup_all()

---

capstone/test_capstone.py — COMPLETE PYTEST FILE
  Purpose: Test pure logic functions without hitting AWS (no mocking needed for these)
  Test functions (use pytest, no AWS calls):
    - test_simulate_pipeline_run_normal():
        run = simulate_pipeline_run(hour_offset=1, inject_failure=False)
        assert 8000 <= run["records_in"] <= 12000
        assert run["error_count"] == 0
        assert run["duration_ms"] < 30000
        assert run["lag_seconds"] < 300
    - test_simulate_pipeline_run_failure():
        run = simulate_pipeline_run(hour_offset=1, inject_failure=True)
        assert run["error_count"] > 0
        assert run["duration_ms"] > 30000 or run["lag_seconds"] > 300
    - test_build_widgets_returns_five():
        widgets = build_widgets("MyNamespace", "my-pipeline")
        assert len(widgets) == 5
        types = [w["type"] for w in widgets]
        assert "text" in types
        assert types.count("metric") == 4
    - test_calculate_cw_cost_free_tier():
        from 05_container_and_lambda_monitoring import calculate_cw_cost
        cost = calculate_cw_cost(custom_metrics=5, log_gb_month=1,
                                  dashboard_count=1, alarm_count=3)
        assert cost["metrics_cost"] == 0.0   # under free tier
        assert cost["dashboard_cost"] == 3.0
        assert cost["total_monthly_usd"] > 0
    - test_calculate_cw_cost_over_free_tier():
        cost = calculate_cw_cost(custom_metrics=50, log_gb_month=10,
                                  dashboard_count=2, alarm_count=10)
        assert cost["metrics_cost"] == 40 * 0.30   # 50 - 10 free = 40 billable
        assert cost["alarm_cost"] == 10 * 0.10
    - test_alarm_rule_composite_format():
        — test that alarm_rule string for composite alarm follows:
          'ALARM("name1") OR ALARM("name2")' format (simple string assertion)

===== INFRASTRUCTURE NOTES =====

AWS account required. CloudWatch free tier: 10 custom metrics, 5GB logs, 3 dashboards/month.
High-resolution metrics (1s resolution) cost 3× standard — use standard (60s) in all tutorial files.
Logs Insights queries billed per GB scanned — keep query time windows to last 1-3 hours during testing.
Always set log group retention — logs without retention policy cost indefinitely.

CLEANUP RULES — MANDATORY:
- Every main() wraps demo code in try/finally — cleanup() is in the finally block
- Every file that creates a resource has its own cleanup() — do not rely on a separate file
- Cleanup functions catch ResourceNotFoundException and continue without crashing
- Print ⚠️  COST WARNING immediately after creating any billable resource
- Print ✅  Cleanup complete. No ongoing charges. at the end of every cleanup()
- capstone/cleanup.py deletes EVERYTHING and ends with that confirmation line

DANGEROUS RESOURCES IN THIS TOPIC:
- CloudWatch Alarms: $0.10/alarm/month — delete after each file run
- CloudWatch Dashboards: $3.00/dashboard/month — delete after each file run
- CloudWatch Log Groups: $0.50/GB ingested — set 7-day retention AND delete in cleanup
- Custom Metrics: $0.30/metric/month after first 10 — metrics auto-expire, no delete needed

===== START =====

Acknowledge these instructions. Confirm you understand:
1. Every file is COMPLETE and FULLY RUNNABLE — no placeholders, no TODO, no pass statements
2. Every main() uses try/finally with cleanup in the finally block
3. The capstone files are specified function-by-function and must be generated completely
4. After acknowledgment, wait for me to say "generate file 01"

===
