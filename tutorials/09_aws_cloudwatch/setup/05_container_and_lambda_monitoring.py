# ============================================================
# Topic   : AWS CloudWatch for Data Engineers
# File    : 05_container_and_lambda_monitoring.py
# Covers  : Metric filters, Lambda metrics, ECS Insights queries, cost model, runbook
# Prereqs : pip install boto3 | AWS credentials | profile: study
# Run     : python 05_container_and_lambda_monitoring.py
# ============================================================

from __future__ import annotations

import json
import os
import time
from datetime import datetime, timedelta, timezone
from typing import Any

import boto3
from botocore.exceptions import ClientError


AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_PROFILE = os.getenv("AWS_PROFILE", "study")
CW_NAMESPACE = os.getenv("CW_NAMESPACE", "StudyBook/Pipeline")
CW_LOG_GROUP_NAME = os.getenv("CW_LOG_GROUP_NAME", "/studybook/pipeline")
LAMBDA_FUNCTION_NAME = os.getenv("LAMBDA_FUNCTION_NAME")  # optional


def get_cw_client() -> Any:
    session = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
    return session.client("cloudwatch")


def get_logs_client() -> Any:
    session = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
    return session.client("logs")


# ============================================================
# METRIC FILTERS
# ============================================================

def create_metric_filter(
    log_group: str,
    filter_name: str,
    pattern: str,
    metric_namespace: str,
    metric_name: str,
    metric_value: str = "1",
    default_value: float = 0,
) -> None:
    """
    Create a CloudWatch metric filter.

    WHY:
        Metric filters let you extract metrics from logs WITHOUT changing application code.
        This is huge in enterprise: ops teams can add observability retroactively.

    Args:
        log_group: Log group name
        filter_name: Filter name
        pattern: Filter pattern (e.g. "ERROR")
        metric_namespace: Namespace for generated metric
        metric_name: Metric name
        metric_value: Value to emit
        default_value: Default value if no match

    Returns:
        None
    """
    client = get_logs_client()

    try:
        client.put_metric_filter(
            logGroupName=log_group,
            filterName=filter_name,
            filterPattern=pattern,
            metricTransformations=[
                {
                    "metricName": metric_name,
                    "metricNamespace": metric_namespace,
                    "metricValue": metric_value,
                    "defaultValue": default_value,
                }
            ],
        )
        print(f"Created metric filter: {filter_name}")
    except ClientError as e:
        print(f"Metric filter failed: {e.response['Error']['Code']}")
        raise


def delete_metric_filter(log_group: str, filter_name: str) -> None:
    client = get_logs_client()

    try:
        client.delete_metric_filter(
            logGroupName=log_group,
            filterName=filter_name,
        )
        print(f"Deleted metric filter: {filter_name}")
    except ClientError as e:
        if e.response["Error"]["Code"] in ("ResourceNotFoundException", "ResourceNotFound"):
            return
        raise


# ============================================================
# LAMBDA METRICS
# ============================================================

def get_lambda_metrics(
    function_name: str,
    start: datetime,
    end: datetime,
    period_s: int = 300,
) -> dict[str, list[dict]]:
    """
    Get core Lambda metrics.

    WHY:
        These 4 metrics cover 90% of Lambda debugging:
        - Duration
        - Errors
        - Throttles
        - ConcurrentExecutions

    Args:
        function_name: Lambda function name
        start: Start time
        end: End time
        period_s: Period

    Returns:
        Dict of metric → datapoints
    """
    client = get_cw_client()

    metrics = ["Duration", "Errors", "Throttles", "ConcurrentExecutions"]
    results: dict[str, list[dict]] = {}

    for metric in metrics:
        try:
            response = client.get_metric_statistics(
                Namespace="AWS/Lambda",
                MetricName=metric,
                Dimensions=[{"Name": "FunctionName", "Value": function_name}],
                StartTime=start,
                EndTime=end,
                Period=period_s,
                Statistics=["Average"],
            )

            results[metric] = sorted(
                response.get("Datapoints", []),
                key=lambda x: x["Timestamp"],
            )

        except ClientError as e:
            print(f"Lambda metric failed: {metric}")
            raise

    return results


# ============================================================
# ECS / CONTAINER INSIGHTS
# ============================================================

def build_ecs_monitoring_queries() -> dict[str, str]:
    """
    Return Logs Insights queries for container monitoring.

    WHY:
        These are real-world queries used in ECS/Kubernetes environments.

    Returns:
        dict of query name → query string
    """
    return {
        "task_cpu": """
            stats avg(CpuUtilized) by TaskDefinitionFamily
        """,
        "task_memory": """
            stats avg(MemoryUtilized) by TaskDefinitionFamily
        """,
        "task_errors": """
            filter @message like /ERROR/
            | stats count(*) by TaskDefinitionFamily
        """,
    }


# ============================================================
# COST MODEL
# ============================================================

def calculate_cw_cost(
    custom_metrics: int,
    log_gb_month: float,
    dashboard_count: int,
    alarm_count: int,
    insights_gb_scanned: float = 0,
) -> dict:
    """
    Calculate CloudWatch monthly cost.

    WHY:
        Cost awareness is critical. CloudWatch can silently become expensive
        at scale due to metric cardinality + logs volume.

    Returns:
        Cost breakdown dictionary
    """
    metrics_cost = max(0, custom_metrics - 10) * 0.30
    log_ingestion_cost = log_gb_month * 0.50
    log_storage_cost = log_gb_month * 0.005 * 30
    dashboard_cost = dashboard_count * 3.00
    alarm_cost = alarm_count * 0.10
    insights_cost = insights_gb_scanned * 0.005

    total = (
        metrics_cost
        + log_ingestion_cost
        + log_storage_cost
        + dashboard_cost
        + alarm_cost
        + insights_cost
    )

    return {
        "metrics_cost": metrics_cost,
        "log_ingestion_cost": log_ingestion_cost,
        "log_storage_cost": log_storage_cost,
        "dashboard_cost": dashboard_cost,
        "alarm_cost": alarm_cost,
        "insights_cost": insights_cost,
        "total_monthly_usd": total,
    }


# ============================================================
# RUNBOOK
# ============================================================

def build_data_pipeline_runbook(pipeline_name: str, alarm_names: list[str]) -> str:
    """
    Build markdown runbook.

    WHY:
        Runbooks convert alerts into action. Without them, alarms just create noise.

    Returns:
        Markdown string
    """
    lines = [f"# Runbook: {pipeline_name}", ""]

    for alarm in alarm_names:
        lines.append(f"## Alarm: {alarm}")

        if "errors" in alarm:
            lines.append("- Meaning: Errors detected in pipeline")
            lines.append("- Action: Check logs immediately")
        elif "lag" in alarm:
            lines.append("- Meaning: Pipeline delay building up")
            lines.append("- Action: Check downstream systems")
        else:
            lines.append("- Meaning: General pipeline issue")
            lines.append("- Action: Investigate metrics + logs")

        lines.append("- Escalation: Data Platform On-call")
        lines.append("")

    return "\n".join(lines)


# ============================================================
# LOG EMISSION
# ============================================================

def ensure_log_group(log_group: str) -> None:
    client = get_logs_client()
    try:
        client.create_log_group(logGroupName=log_group)
        print("Created log group")
    except ClientError:
        pass


def ensure_stream(log_group: str, stream: str) -> None:
    client = get_logs_client()
    try:
        client.create_log_stream(logGroupName=log_group, logStreamName=stream)
    except ClientError:
        pass


def put_log(log_group: str, stream: str, message: str) -> None:
    client = get_logs_client()

    token = None
    try:
        desc = client.describe_log_streams(logGroupName=log_group)
        token = desc["logStreams"][0].get("uploadSequenceToken")
    except Exception:
        pass

    kwargs = {
        "logGroupName": log_group,
        "logStreamName": stream,
        "logEvents": [
            {
                "timestamp": int(datetime.now(timezone.utc).timestamp() * 1000),
                "message": message,
            }
        ],
    }

    if token:
        kwargs["sequenceToken"] = token

    client.put_log_events(**kwargs)


# ============================================================
# MAIN
# ============================================================

def main() -> None:
    log_group = CW_LOG_GROUP_NAME
    stream = f"monitoring-{int(time.time())}"
    filter_name = "error_filter"

    try:
        ensure_log_group(log_group)
        ensure_stream(log_group, stream)

        print("⚠️ COST WARNING: Logs + metrics may incur charges")

        # emit logs
        for i in range(15):
            msg = "ERROR something failed" if i % 5 == 0 else "INFO normal"
            put_log(log_group, stream, msg)

        create_metric_filter(
            log_group,
            filter_name,
            "ERROR",
            CW_NAMESPACE,
            "error_count",
        )

        print("Waiting for metric filter...")
        time.sleep(5)

        # Lambda metrics
        if LAMBDA_FUNCTION_NAME:
            data = get_lambda_metrics(
                LAMBDA_FUNCTION_NAME,
                datetime.now(timezone.utc) - timedelta(hours=1),
                datetime.now(timezone.utc),
            )
            print("\nLambda Metrics:")
            print(data)
        else:
            print("\nSkipping Lambda metrics (env not set)")

        # ECS queries
        print("\nECS Queries:")
        print(build_ecs_monitoring_queries())

        # cost
        print("\nCost Example:")
        print(
            calculate_cw_cost(
                custom_metrics=50,
                log_gb_month=10,
                dashboard_count=2,
                alarm_count=10,
                insights_gb_scanned=5,
            )
        )

        # runbook
        print("\nRunbook:")
        print(
            build_data_pipeline_runbook(
                "iot-ingest",
                ["errors", "lag", "general"],
            )
        )

    finally:
        delete_metric_filter(log_group, filter_name)

        try:
            get_logs_client().delete_log_group(logGroupName=log_group)
        except ClientError:
            pass

        print("✅ Cleanup complete. No ongoing charges.")


if __name__ == "__main__":
    main()