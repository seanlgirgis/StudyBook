# ChatGPT Prompt — AWS CloudWatch Tutorial
# Paste everything between the === markers into ChatGPT

===

TOPIC: AWS CloudWatch for Data Engineers
SLUG: aws-cloudwatch
PRIORITY: Toyota Interview Prep
INFRASTRUCTURE: AWS (boto3, real AWS account)

===== CODING STANDARDS =====

FILE HEADER:
# ============================================================
# Topic   : AWS CloudWatch for Data Engineers
# File    : NN_filename.py
# Covers  : one-line description
# Prereqs : pip install boto3 | AWS credentials configured
# Run     : python filename.py
# ============================================================

COMMENTS: Explain WHY. CloudWatch is the operational backbone — explain metric
namespaces, dimensions, resolution, and cost implications of high-resolution metrics.
Env vars: AWS_REGION, AWS_PROFILE, CW_LOG_GROUP_NAME, CW_ALARM_SNS_ARN (optional)

===== FILES TO GENERATE =====

01_custom_metrics.py
  Purpose: Emit and query custom CloudWatch metrics — the foundation of operational visibility
  Key concepts: namespaces, dimensions, metric resolution (standard=60s vs high-res=1s),
    StatisticSets for batching, cost ($0.30/metric/month beyond free tier)
  Functions:
    - put_metric(namespace, metric_name, value, unit, dimensions: dict, high_resolution=False)
    - put_metric_batch(namespace, metrics: list[dict]) — batch up to 1000 metrics per call
    - put_statistic_set(namespace, metric_name, dimensions, sample_count, sum, min, max)
      — efficient for pre-aggregated data (saves API calls)
    - get_metric_statistics(namespace, metric_name, dimensions, start, end, period_s, stat)
      — retrieve historical values
    - list_metrics_in_namespace(namespace) — discover what's been published
  Main block: emit 50 synthetic pipeline_records_processed metrics over simulated time,
    retrieve and print hourly average, show cost calculation for 10 custom metrics/month

02_log_groups_and_insights.py
  Purpose: CloudWatch Logs — structured logging, log groups, retention, Logs Insights queries
  Key concepts: log groups vs log streams, structured JSON logs, retention policies,
    Logs Insights query syntax, cost ($0.50/GB ingestion + $0.005/GB storage)
  Functions:
    - create_log_group(group_name, retention_days=30)
    - put_log_events(group_name, stream_name, messages: list[str]) — handle sequence token
    - put_structured_log(group_name, stream_name, event: dict) — JSON log entry
    - query_logs_insights(group_name, query_string, start, end, limit=100)
      — run CloudWatch Logs Insights, poll until complete, return results
    - common_queries() — return dict of useful pre-built queries:
        pipeline_errors: "filter @message like /ERROR/"
        slow_jobs: "filter duration_ms > 5000 | stats avg(duration_ms) by job_name"
        hourly_volume: "stats count() by bin(1h)"
    - set_retention_policy(group_name, days) — cost control via retention
  Main block: create log group, emit 20 structured JSON pipeline events (mix of INFO/ERROR),
    run 3 Insights queries, print results

03_alarms_and_composite_alarms.py
  Purpose: CloudWatch Alarms — metric alarms, anomaly detection, composite alarms
  Key concepts: threshold vs anomaly detection, alarm states (OK/ALARM/INSUFFICIENT_DATA),
    composite alarms for reducing alert noise, SNS notifications
  Functions:
    - create_metric_alarm(name, namespace, metric, dimensions, threshold,
        comparison, evaluation_periods, period_s, statistic, sns_arn=None)
    - create_anomaly_detector(namespace, metric_name, dimensions) — ML-based baseline
    - create_anomaly_detection_alarm(name, metric_name, namespace, dimensions, band_width=2)
    - create_composite_alarm(name, alarm_rule: str, sns_arn=None)
      — alarm_rule: "ALARM(cpu_high) AND ALARM(memory_high)"
    - get_alarm_history(alarm_name, days=7) — show state transitions
    - list_alarms_in_state(state="ALARM") — find firing alarms
    - delete_alarm(name)
  Main block: create 3 alarms (records_processed too low, error_rate too high, latency high),
    create composite alarm requiring 2-of-3, show history, cleanup

04_dashboards_and_embedded_metrics.py
  Purpose: CloudWatch Dashboards + Embedded Metric Format (EMF) for zero-cost structured metrics
  Key concepts: dashboard JSON widgets, EMF (emit metrics embedded in logs — free!),
    difference between CloudWatch agent and custom metrics
  Functions:
    - create_dashboard(name, widgets: list[dict]) — create from widget definitions
    - build_metric_widget(title, metrics: list, period_s, stat, width=12, height=6) → dict
    - build_text_widget(markdown: str, width=12, height=3) → dict
    - put_emf_metric(log_group, namespace, metrics: dict, dimensions: dict)
      — Embedded Metric Format: log-based metrics, zero extra cost
    - build_pipeline_dashboard(pipeline_name, namespace) — create standard DE dashboard:
        widgets: records/min, error rate, latency p50/p95/p99, active jobs count
    - get_dashboard_url(name, region) — return console URL
  Main block: emit 30 minutes of EMF pipeline metrics, build dashboard with 4 widgets, print URL

05_container_and_lambda_monitoring.py
  Purpose: Monitoring data pipelines in containers and Lambda — patterns for Toyota IoT stack
  Key concepts: Container Insights, Lambda metrics, log subscription filters, metric filters
  Functions:
    - create_metric_filter(log_group, filter_name, pattern, metric_namespace, metric_name)
      — extract metrics from log text (e.g., count ERROR lines → error_count metric)
    - create_subscription_filter(log_group, dest_arn, filter_pattern="")
      — stream logs to Lambda/Kinesis/Firehose
    - get_lambda_metrics(function_name, start, end) — Duration, Errors, Throttles, ConcurrentExecutions
    - build_ecs_monitoring_queries() — common Logs Insights for ECS Container Insights
    - calculate_cw_cost(custom_metrics, log_gb_month, dashboard_count, alarm_count) → dict
      — line-item cost breakdown
    - build_data_pipeline_runbook(pipeline_name, alarm_names) → str
      — generate markdown runbook: what each alarm means, how to investigate
  Main block: show metric filter creation for error extraction, print full cost breakdown
    for a realistic pipeline (50 custom metrics, 10GB logs/month, 2 dashboards, 10 alarms)

===== CAPSTONE PROJECT =====

capstone/brief.md
  Title: Pipeline Observability Stack
  Scenario: A Kinesis → Glue → S3 pipeline runs hourly. Build a complete CloudWatch
    observability layer that a data engineer can use to know: is the pipeline healthy?
    where is it slow? what broke and when?
  What to build:
    - emit_pipeline_metrics.py: simulate 24 hours of pipeline runs emitting custom metrics
        (records_in, records_out, error_count, duration_ms, lag_seconds)
        Use StatisticSets to batch efficiently
    - setup_alarms.py: create 5 alarms:
        - records_out drops below 1000 for 2 consecutive 5-min periods
        - error_count > 0 for any period
        - duration_ms p95 > 30000ms
        - lag_seconds > 300 (more than 5 min behind)
        - Composite: overall_pipeline_unhealthy = error OR lag
    - build_dashboard.py: dashboard with 5 widgets covering all key metrics
    - insights_queries.py: 4 saved Insights queries (slow runs, error patterns, daily volume, hourly lag)
    - cleanup.py: delete alarms, dashboard, log group

  Acceptance criteria:
    - Composite alarm definition is valid (test by checking describe_alarms output)
    - Dashboard URL prints and contains 5 widgets
    - At least one alarm transitions to ALARM state during simulated bad hour
    - Cost report shows estimated monthly cost < $20 for this setup

capstone/capstone.py — orchestration
capstone/test_capstone.py — test metric batching, alarm rule builder, cost calculator (no AWS)

===== INFRASTRUCTURE NOTES =====

AWS account required. CloudWatch free tier: 10 custom metrics, 5GB logs, 3 dashboards.
High-resolution metrics (1s) cost 3× standard. Use standard (60s) for tutorial files.
Logs Insights queries billed per GB scanned — keep query time windows short during testing.
Always set log group retention — unretained logs cost indefinitely.
CLEANUP RULES — MANDATORY:
- Every main() wraps demo code in try/finally — cleanup() is in the finally block
- Every file that creates a resource has its own cleanup() — do not rely on a separate file
- Cleanup functions catch "already deleted" errors and continue without crashing
- Print ⚠️ COST WARNING immediately after creating any billable resource
- Print ✅ Cleanup complete. No ongoing charges. at the end of every cleanup()
- capstone/cleanup.py deletes EVERYTHING and ends with that confirmation line

===== START =====

Acknowledge these instructions, then wait for me to say "generate file 01".

===
