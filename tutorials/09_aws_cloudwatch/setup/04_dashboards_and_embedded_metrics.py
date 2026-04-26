# ============================================================
# Topic   : AWS CloudWatch for Data Engineers
# File    : 04_dashboards_and_embedded_metrics.py
# Covers  : CloudWatch Dashboards and Embedded Metric Format (EMF)
# Prereqs : pip install boto3 | AWS credentials | profile: study
# Run     : python 04_dashboards_and_embedded_metrics.py
# ============================================================

from __future__ import annotations

import json
import os
import random
import time
from datetime import datetime, timezone
from typing import Any
from urllib.parse import quote

import boto3
from botocore.exceptions import ClientError


AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_PROFILE = os.getenv("AWS_PROFILE", "study")
CW_NAMESPACE = os.getenv("CW_NAMESPACE", "StudyBook/Pipeline")
CW_LOG_GROUP_NAME = os.getenv("CW_LOG_GROUP_NAME", "/studybook/pipeline")
CW_ALARM_SNS_ARN = os.getenv("CW_ALARM_SNS_ARN")


def get_cw_client() -> Any:
    """
    Create a CloudWatch boto3 client.

    WHY:
        Centralized client creation keeps AWS profile and region handling
        consistent across scripts and environments.

    Args:
        None.

    Returns:
        Any: boto3 CloudWatch client.

    Raises:
        botocore.exceptions.BotoCoreError: If boto3 cannot create the client.
    """
    session = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
    return session.client("cloudwatch")


def get_logs_client() -> Any:
    """
    Create a CloudWatch Logs boto3 client.

    WHY:
        EMF metrics are written through CloudWatch Logs, so dashboard code often
        needs both the CloudWatch and Logs clients.

    Args:
        None.

    Returns:
        Any: boto3 CloudWatch Logs client.

    Raises:
        botocore.exceptions.BotoCoreError: If boto3 cannot create the client.
    """
    session = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
    return session.client("logs")


def ensure_log_group(log_group: str, retention_days: int = 7) -> None:
    """
    Create a log group and set retention.

    WHY:
        EMF is emitted through logs. Retention must be controlled because log
        ingestion and storage are billable.

    Args:
        log_group (str): CloudWatch log group name.
        retention_days (int): Retention period in days.

    Returns:
        None.

    Raises:
        ClientError: If AWS returns an unexpected error.
    """
    client = get_logs_client()

    try:
        client.create_log_group(logGroupName=log_group)
        print(f"Created log group: {log_group}")
        print("⚠️  COST WARNING: CloudWatch Logs charges for ingestion and storage.")
    except ClientError as exc:
        code = exc.response["Error"]["Code"]
        if code != "ResourceAlreadyExistsException":
            print(f"CreateLogGroup failed: {code}")
            raise

    try:
        client.put_retention_policy(
            logGroupName=log_group,
            retentionInDays=retention_days,
        )
        print(f"Retention set to {retention_days} days.")
    except ClientError as exc:
        code = exc.response["Error"]["Code"]
        print(f"PutRetentionPolicy failed: {code}")
        raise


def ensure_log_stream(log_group: str, stream_name: str) -> None:
    """
    Create a log stream if needed.

    WHY:
        A log stream is the append target for EMF JSON events. One stream per
        demo run keeps the tutorial output easy to inspect.

    Args:
        log_group (str): CloudWatch log group name.
        stream_name (str): CloudWatch log stream name.

    Returns:
        None.

    Raises:
        ClientError: If AWS returns an unexpected error.
    """
    client = get_logs_client()

    try:
        client.create_log_stream(
            logGroupName=log_group,
            logStreamName=stream_name,
        )
        print(f"Created log stream: {stream_name}")
    except ClientError as exc:
        code = exc.response["Error"]["Code"]
        if code == "ResourceAlreadyExistsException":
            return
        print(f"CreateLogStream failed: {code}")
        raise


def get_sequence_token(log_group: str, stream_name: str) -> str | None:
    """
    Return the current upload sequence token for a log stream.

    WHY:
        Repeated writes to CloudWatch Logs may require the latest sequence token.
        Pulling it before each write keeps the helper robust during demos.

    Args:
        log_group (str): CloudWatch log group name.
        stream_name (str): CloudWatch log stream name.

    Returns:
        str | None: Upload sequence token if present.

    Raises:
        ClientError: If DescribeLogStreams fails.
    """
    client = get_logs_client()

    try:
        response = client.describe_log_streams(
            logGroupName=log_group,
            logStreamNamePrefix=stream_name,
            limit=50,
        )
    except ClientError as exc:
        code = exc.response["Error"]["Code"]
        print(f"DescribeLogStreams failed: {code}")
        raise

    for stream in response.get("logStreams", []):
        if stream.get("logStreamName") == stream_name:
            return stream.get("uploadSequenceToken")

    return None


def put_log_line(log_group: str, stream_name: str, message: str) -> None:
    """
    Write one JSON line to CloudWatch Logs.

    WHY:
        EMF is just structured JSON written to logs. CloudWatch extracts metrics
        from the _aws.CloudWatchMetrics block asynchronously.

    Args:
        log_group (str): CloudWatch log group name.
        stream_name (str): CloudWatch log stream name.
        message (str): JSON log message.

    Returns:
        None.

    Raises:
        ClientError: If PutLogEvents fails unexpectedly.
    """
    client = get_logs_client()
    ensure_log_stream(log_group, stream_name)

    request: dict[str, Any] = {
        "logGroupName": log_group,
        "logStreamName": stream_name,
        "logEvents": [
            {
                "timestamp": int(datetime.now(timezone.utc).timestamp() * 1000),
                "message": message,
            }
        ],
    }

    token = get_sequence_token(log_group, stream_name)
    if token:
        request["sequenceToken"] = token

    try:
        client.put_log_events(**request)
    except ClientError as exc:
        code = exc.response["Error"]["Code"]

        if code in {"InvalidSequenceTokenException", "DataAlreadyAcceptedException"}:
            retry = dict(request)
            token = get_sequence_token(log_group, stream_name)

            if token:
                retry["sequenceToken"] = token
            elif "sequenceToken" in retry:
                del retry["sequenceToken"]

            client.put_log_events(**retry)
            return

        print(f"PutLogEvents failed: {code}")
        raise


def build_metric_widget(
    title: str,
    metrics: list[list[Any]],
    period_s: int,
    stat: str,
    width: int = 12,
    height: int = 6,
) -> dict[str, Any]:
    """
    Build a CloudWatch dashboard metric widget.

    WHY:
        Dashboards are JSON documents. Understanding the widget structure lets
        data engineers create monitoring views automatically with deployments.

    Args:
        title (str): Widget title.
        metrics (list[list[Any]]): CloudWatch dashboard metric array.
        period_s (int): Widget period in seconds.
        stat (str): Statistic such as Average, Sum, or p90.
        width (int): Widget width in grid units.
        height (int): Widget height in grid units.

    Returns:
        dict[str, Any]: Dashboard widget definition.

    Raises:
        None.
    """
    return {
        "type": "metric",
        "width": width,
        "height": height,
        "properties": {
            "metrics": metrics,
            "period": period_s,
            "stat": stat,
            "region": AWS_REGION,
            "title": title,
            "view": "timeSeries",
        },
    }


def build_text_widget(markdown: str, width: int = 12, height: int = 3) -> dict[str, Any]:
    """
    Build a CloudWatch dashboard text widget.

    WHY:
        Text widgets turn dashboards into runbooks by adding context, ownership,
        and expected behavior next to the charts.

    Args:
        markdown (str): Markdown text to display.
        width (int): Widget width in grid units.
        height (int): Widget height in grid units.

    Returns:
        dict[str, Any]: Dashboard text widget definition.

    Raises:
        None.
    """
    return {
        "type": "text",
        "width": width,
        "height": height,
        "properties": {
            "markdown": markdown,
        },
    }


def build_alarm_widget(
    alarm_arns: list[str],
    width: int = 12,
    height: int = 4,
) -> dict[str, Any]:
    """
    Build a CloudWatch dashboard alarm widget.

    WHY:
        Alarm widgets put alert state beside metric charts, which helps operators
        connect symptoms to alerting behavior during triage.

    Args:
        alarm_arns (list[str]): Alarm ARNs to display.
        width (int): Widget width in grid units.
        height (int): Widget height in grid units.

    Returns:
        dict[str, Any]: Dashboard alarm widget definition.

    Raises:
        None.
    """
    return {
        "type": "alarm",
        "width": width,
        "height": height,
        "properties": {
            "title": "Pipeline Alarm State",
            "alarms": alarm_arns,
        },
    }


def arrange_widgets(widgets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Assign x/y positions to widgets in a 24-column grid.

    WHY:
        CloudWatch dashboards use a grid layout. Programmatic positioning avoids
        manual console edits and keeps dashboards reproducible.

    Args:
        widgets (list[dict[str, Any]]): Widgets without positions.

    Returns:
        list[dict[str, Any]]: Widgets with x and y positions.

    Raises:
        None.
    """
    arranged: list[dict[str, Any]] = []
    x = 0
    y = 0
    row_height = 0

    for widget in widgets:
        item = dict(widget)
        width = int(item.get("width", 12))
        height = int(item.get("height", 6))

        if x + width > 24:
            x = 0
            y += row_height
            row_height = 0

        item["x"] = x
        item["y"] = y

        arranged.append(item)

        x += width
        row_height = max(row_height, height)

    return arranged


def create_dashboard(name: str, widgets: list[dict[str, Any]]) -> str:
    """
    Create or replace a CloudWatch dashboard.

    WHY:
        Dashboards are billable and should be created deliberately from code,
        not by hand. Code-based dashboards are reproducible across accounts.

    Args:
        name (str): Dashboard name.
        widgets (list[dict[str, Any]]): Dashboard widget definitions.

    Returns:
        str: AWS Console dashboard URL.

    Raises:
        ClientError: If PutDashboard fails.
    """
    client = get_cw_client()
    body = {"widgets": arrange_widgets(widgets)}

    try:
        client.put_dashboard(
            DashboardName=name,
            DashboardBody=json.dumps(body),
        )
        print(f"Created dashboard: {name}")
        print("⚠️  COST WARNING: CloudWatch Dashboards cost about $3.00/month each.")
    except ClientError as exc:
        code = exc.response["Error"]["Code"]
        print(f"PutDashboard failed: {code}")
        raise

    return get_dashboard_url(name, AWS_REGION)


def get_dashboard_url(name: str, region: str) -> str:
    """
    Build the AWS Console URL for a CloudWatch dashboard.

    WHY:
        Returning the URL gives operators a direct handoff from automation to the
        console view used during incidents.

    Args:
        name (str): Dashboard name.
        region (str): AWS region.

    Returns:
        str: CloudWatch dashboard console URL.

    Raises:
        None.
    """
    return (
        f"https://console.aws.amazon.com/cloudwatch/home"
        f"?region={region}#dashboards:name={quote(name)}"
    )


def put_emf_metric(
    log_group: str,
    stream_name: str,
    namespace: str,
    metrics: dict[str, float],
    dimensions: dict[str, str],
) -> None:
    """
    Write a valid Embedded Metric Format log event.

    WHY:
        EMF lets applications emit metrics as structured logs. This avoids a
        separate PutMetricData call while still creating CloudWatch metrics from
        the log stream.

    Args:
        log_group (str): CloudWatch log group name.
        stream_name (str): CloudWatch log stream name.
        namespace (str): CloudWatch metric namespace.
        metrics (dict[str, float]): Metric name/value pairs.
        dimensions (dict[str, str]): Metric dimensions.

    Returns:
        None.

    Raises:
        ClientError: If CloudWatch Logs writing fails.
    """
    timestamp_ms = int(datetime.now(timezone.utc).timestamp() * 1000)

    metric_definitions = [
        {"Name": metric_name, "Unit": _infer_unit(metric_name)}
        for metric_name in metrics
    ]

    event: dict[str, Any] = {
        "_aws": {
            "Timestamp": timestamp_ms,
            "CloudWatchMetrics": [
                {
                    "Namespace": namespace,
                    "Dimensions": [list(dimensions.keys())],
                    "Metrics": metric_definitions,
                }
            ],
        },
        **dimensions,
        **metrics,
    }

    put_log_line(log_group, stream_name, json.dumps(event))


def _infer_unit(metric_name: str) -> str:
    """
    Infer a CloudWatch unit from a metric name.

    WHY:
        Units improve dashboard readability. In real systems, use explicit unit
        metadata; this small helper keeps the tutorial compact.

    Args:
        metric_name (str): Metric name.

    Returns:
        str: CloudWatch unit.

    Raises:
        None.
    """
    if metric_name.endswith("_ms") or "duration" in metric_name:
        return "Milliseconds"
    if metric_name.endswith("_count") or metric_name.startswith("records"):
        return "Count"
    return "None"


def delete_dashboard(name: str) -> None:
    """
    Delete a CloudWatch dashboard idempotently.

    WHY:
        Dashboards cost money monthly. Tutorial dashboards should always be
        removed after the demo.

    Args:
        name (str): Dashboard name.

    Returns:
        None.

    Raises:
        ClientError: If DeleteDashboards fails unexpectedly.
    """
    client = get_cw_client()

    try:
        client.delete_dashboards(DashboardNames=[name])
        print(f"Deleted dashboard if present: {name}")
    except ClientError as exc:
        code = exc.response["Error"]["Code"]
        if code in {"ResourceNotFoundException", "ResourceNotFound"}:
            return
        print(f"DeleteDashboards failed: {code}")
        raise


def delete_log_group(log_group: str) -> None:
    """
    Delete a CloudWatch log group idempotently.

    WHY:
        EMF events are stored as logs. Deleting the log group removes tutorial log
        storage and prevents ongoing storage charges.

    Args:
        log_group (str): CloudWatch log group name.

    Returns:
        None.

    Raises:
        ClientError: If DeleteLogGroup fails unexpectedly.
    """
    client = get_logs_client()

    try:
        client.delete_log_group(logGroupName=log_group)
        print(f"Deleted log group if present: {log_group}")
    except ClientError as exc:
        code = exc.response["Error"]["Code"]
        if code in {"ResourceNotFoundException", "ResourceNotFound"}:
            return
        print(f"DeleteLogGroup failed: {code}")
        raise


def cleanup(dashboard_name: str, log_group: str) -> None:
    """
    Clean up resources created by this file.

    WHY:
        This demo creates a dashboard and log group, both of which can generate
        cost. Cleanup keeps repeated study runs safe.

    Args:
        dashboard_name (str): Dashboard name.
        log_group (str): CloudWatch log group name.

    Returns:
        None.

    Raises:
        None.
    """
    try:
        delete_dashboard(dashboard_name)
    finally:
        try:
            delete_log_group(log_group)
        finally:
            print("✅  Cleanup complete. No ongoing charges.")


def build_demo_dashboard_widgets(namespace: str) -> list[dict[str, Any]]:
    """
    Build the four tutorial dashboard widgets.

    WHY:
        The dashboard shows common pipeline health dimensions: throughput,
        duration, errors, and a text/runbook-style header.

    Args:
        namespace (str): CloudWatch metric namespace.

    Returns:
        list[dict[str, Any]]: Dashboard widgets.

    Raises:
        None.
    """
    dimension_filter = {"pipeline_name": "studybook-emf", "environment": "dev"}

    records_widget = build_metric_widget(
        title="Records In / Out",
        metrics=[
            [
                namespace,
                "records_in",
                "pipeline_name",
                dimension_filter["pipeline_name"],
                "environment",
                dimension_filter["environment"],
            ],
            [
                ".",
                "records_out",
                ".",
                ".",
                ".",
                ".",
            ],
        ],
        period_s=60,
        stat="Average",
        width=12,
        height=6,
    )

    duration_widget = build_metric_widget(
        title="Duration Average",
        metrics=[
            [
                namespace,
                "duration_ms",
                "pipeline_name",
                dimension_filter["pipeline_name"],
                "environment",
                dimension_filter["environment"],
                {"stat": "Average"},
            ]
        ],
        period_s=60,
        stat="Average",
        width=12,
        height=6,
    )
    duration_widget["properties"]["view"] = "bar"

    error_widget = build_metric_widget(
        title="Error Count",
        metrics=[
            [
                namespace,
                "error_count",
                "pipeline_name",
                dimension_filter["pipeline_name"],
                "environment",
                dimension_filter["environment"],
                {"stat": "Sum"},
            ]
        ],
        period_s=60,
        stat="Sum",
        width=12,
        height=4,
    )

    text_widget = build_text_widget(
        markdown="# Pipeline Health — StudyBook Tutorial\n\nEMF metrics are emitted through structured logs.",
        width=24,
        height=3,
    )

    return [records_widget, duration_widget, error_widget, text_widget]


def main() -> None:
    """
    Run the CloudWatch dashboard and EMF demo.

    WHY:
        This demonstrates the operational pattern of emitting metrics through
        logs, then visualizing those metrics with a reproducible dashboard.

    Args:
        None.

    Returns:
        None.

    Raises:
        ClientError: If AWS API calls fail unexpectedly.
    """
    dashboard_name = "studybook-pipeline"
    stream_name = f"emf-demo-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"

    try:
        ensure_log_group(CW_LOG_GROUP_NAME, retention_days=7)
        ensure_log_stream(CW_LOG_GROUP_NAME, stream_name)

        random.seed(42)

        print("\nEmitting 20 EMF log entries...")
        for index in range(20):
            records_in = random.randint(8000, 12000)
            error_count = 1 if index in {7, 16} else 0
            records_out = records_in - random.randint(0, 300 if error_count else 80)

            put_emf_metric(
                log_group=CW_LOG_GROUP_NAME,
                stream_name=stream_name,
                namespace=CW_NAMESPACE,
                metrics={
                    "records_in": float(records_in),
                    "records_out": float(records_out),
                    "duration_ms": float(random.randint(7000, 28000)),
                    "error_count": float(error_count),
                },
                dimensions={
                    "pipeline_name": "studybook-emf",
                    "environment": "dev",
                },
            )

        print("Waiting briefly for EMF extraction...")
        time.sleep(5)

        widgets = build_demo_dashboard_widgets(CW_NAMESPACE)
        url = create_dashboard(dashboard_name, widgets)

        print(f"\nDashboard URL:\n{url}")

    finally:
        cleanup(dashboard_name, CW_LOG_GROUP_NAME)


if __name__ == "__main__":
    main()