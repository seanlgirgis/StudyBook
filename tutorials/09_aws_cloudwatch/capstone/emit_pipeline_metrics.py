# ============================================================
# Topic   : AWS CloudWatch for Data Engineers
# File    : capstone/emit_pipeline_metrics.py
# Covers  : Simulate 24 hours of hourly pipeline metrics and structured logs
# Prereqs : pip install boto3 | AWS credentials | profile: study
# Run     : python capstone/emit_pipeline_metrics.py
# ============================================================

from __future__ import annotations

import json
import os
import random
from datetime import datetime, timedelta, timezone
from typing import Any

import boto3
from botocore.exceptions import ClientError


NAMESPACE = os.getenv("CW_NAMESPACE", "StudyBook/CapstoneP")
LOG_GROUP = os.getenv("CW_LOG_GROUP_NAME", "/studybook/capstone/pipeline")
PIPELINE_NAME = "iot-ingest-hourly"
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_PROFILE = os.getenv("AWS_PROFILE", "study")


def get_cw_client() -> Any:
    """
    Create a CloudWatch client.

    WHY:
        CloudWatch metrics are the first layer of the observability stack.
        Centralized client creation keeps profile and region behavior consistent.

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
    Create a CloudWatch Logs client.

    WHY:
        Metrics show symptoms, but logs explain what happened. This capstone emits
        both so the pipeline can be investigated from CloudWatch end to end.

    Args:
        None.

    Returns:
        Any: boto3 CloudWatch Logs client.

    Raises:
        botocore.exceptions.BotoCoreError: If boto3 cannot create the client.
    """
    session = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
    return session.client("logs")


def create_log_group(retention_days: int = 7) -> None:
    """
    Create the capstone log group and set retention.

    WHY:
        Always set retention. Infinite retention is how tutorial logs become
        surprise bills. Seven days is enough for this capstone investigation.

    Args:
        retention_days (int): Number of days to retain logs.

    Returns:
        None.

    Raises:
        ClientError: If AWS returns an unexpected error.
    """
    logs = get_logs_client()

    try:
        logs.create_log_group(logGroupName=LOG_GROUP)
        print(f"Created log group: {LOG_GROUP}")
        print("⚠️  COST WARNING: CloudWatch Logs charge for ingestion and storage.")
    except ClientError as exc:
        code = exc.response["Error"]["Code"]
        if code != "ResourceAlreadyExistsException":
            print(f"CreateLogGroup failed: {code}")
            raise

    try:
        logs.put_retention_policy(
            logGroupName=LOG_GROUP,
            retentionInDays=retention_days,
        )
        print(f"Retention set to {retention_days} days for {LOG_GROUP}")
    except ClientError as exc:
        code = exc.response["Error"]["Code"]
        print(f"PutRetentionPolicy failed: {code}")
        raise


def create_log_stream(stream_name: str) -> None:
    """
    Create a CloudWatch log stream for this capstone run.

    WHY:
        A stream per run makes troubleshooting easier because the run's structured
        events are grouped together inside the shared pipeline log group.

    Args:
        stream_name (str): Log stream name.

    Returns:
        None.

    Raises:
        ClientError: If AWS returns an unexpected error.
    """
    logs = get_logs_client()

    try:
        logs.create_log_stream(
            logGroupName=LOG_GROUP,
            logStreamName=stream_name,
        )
    except ClientError as exc:
        code = exc.response["Error"]["Code"]
        if code == "ResourceAlreadyExistsException":
            return
        print(f"CreateLogStream failed: {code}")
        raise


def get_sequence_token(stream_name: str) -> str | None:
    """
    Get the current upload sequence token for a stream.

    WHY:
        CloudWatch Logs can require a sequence token for repeated writes. Reading
        the token keeps log emission stable across reruns and retries.

    Args:
        stream_name (str): Log stream name.

    Returns:
        str | None: Upload sequence token if one exists.

    Raises:
        ClientError: If DescribeLogStreams fails.
    """
    logs = get_logs_client()

    try:
        response = logs.describe_log_streams(
            logGroupName=LOG_GROUP,
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


def put_structured_log(stream_name: str, event: dict[str, Any], event_time: datetime) -> None:
    """
    Write one structured pipeline log event.

    WHY:
        Structured JSON logs make Logs Insights useful. Fields like duration_ms,
        error_count, lag_seconds, and job_name become directly queryable.

    Args:
        stream_name (str): CloudWatch log stream name.
        event (dict[str, Any]): Structured event payload.
        event_time (datetime): Event timestamp.

    Returns:
        None.

    Raises:
        ClientError: If PutLogEvents fails unexpectedly.
    """
    logs = get_logs_client()
    create_log_stream(stream_name)

    request: dict[str, Any] = {
        "logGroupName": LOG_GROUP,
        "logStreamName": stream_name,
        "logEvents": [
            {
                "timestamp": int(event_time.timestamp() * 1000),
                "message": json.dumps(event, default=str),
            }
        ],
    }

    token = get_sequence_token(stream_name)
    if token:
        request["sequenceToken"] = token

    try:
        logs.put_log_events(**request)
    except ClientError as exc:
        code = exc.response["Error"]["Code"]

        if code in {"InvalidSequenceTokenException", "DataAlreadyAcceptedException"}:
            retry = dict(request)
            token = get_sequence_token(stream_name)
            if token:
                retry["sequenceToken"] = token
            else:
                retry.pop("sequenceToken", None)

            logs.put_log_events(**retry)
            return

        print(f"PutLogEvents failed: {code}")
        raise


def simulate_pipeline_run(hour_offset: int, inject_failure: bool = False) -> dict[str, Any]:
    """
    Simulate one hourly pipeline run.

    WHY:
        Real observability needs realistic metric shape: throughput, output count,
        error count, latency, and lag. These five signals cover most pipeline
        health discussions in senior data engineering interviews.

    Args:
        hour_offset (int): Number of hours ago this run occurred.
        inject_failure (bool): Whether to simulate a failed/degraded run.

    Returns:
        dict[str, Any]: Pipeline run metrics and metadata.

    Raises:
        ValueError: If hour_offset is negative.
    """
    if hour_offset < 0:
        raise ValueError("hour_offset cannot be negative.")

    records_in = random.randint(8000, 12000)

    if inject_failure:
        records_out = int(records_in * random.uniform(0.80, 0.94))
        error_count = random.randint(1, 10)
        duration_ms = random.randint(35000, 60000)
        lag_seconds = random.randint(400, 900)
        level = "ERROR"
        status = "FAILED"
        error_msg = "Simulated Kinesis-to-Glue processing delay with partial output."
    else:
        records_out = int(records_in * random.uniform(0.97, 1.0))
        error_count = 0
        duration_ms = random.randint(8000, 25000)
        lag_seconds = random.randint(10, 60)
        level = "INFO"
        status = "SUCCEEDED"
        error_msg = ""

    run_time = datetime.now(timezone.utc) - timedelta(hours=hour_offset)

    return {
        "pipeline_name": PIPELINE_NAME,
        "job_name": PIPELINE_NAME,
        "hour_offset": hour_offset,
        "run_time": run_time.isoformat(),
        "level": level,
        "status": status,
        "records_in": records_in,
        "records_out": records_out,
        "error_count": error_count,
        "duration_ms": duration_ms,
        "lag_seconds": lag_seconds,
        "error_msg": error_msg,
    }


def emit_run_metrics(run: dict[str, Any], hour_offset: int) -> None:
    """
    Emit all metrics and one structured log for a pipeline run.

    WHY:
        Emitting all five metrics in one PutMetricData call is cheaper and cleaner
        than separate API calls. The matching log event gives investigation context.

    Args:
        run (dict[str, Any]): Pipeline run payload from simulate_pipeline_run.
        hour_offset (int): Number of hours ago this metric should be timestamped.

    Returns:
        None.

    Raises:
        ClientError: If CloudWatch metric or log emission fails.
    """
    cw = get_cw_client()
    event_time = datetime.now(timezone.utc) - timedelta(hours=hour_offset)

    dimensions = [
        {"Name": "PipelineName", "Value": PIPELINE_NAME},
    ]

    metric_data = [
        {
            "MetricName": "records_in",
            "Value": float(run["records_in"]),
            "Unit": "Count",
            "Dimensions": dimensions,
            "Timestamp": event_time,
            "StorageResolution": 60,
        },
        {
            "MetricName": "records_out",
            "Value": float(run["records_out"]),
            "Unit": "Count",
            "Dimensions": dimensions,
            "Timestamp": event_time,
            "StorageResolution": 60,
        },
        {
            "MetricName": "error_count",
            "Value": float(run["error_count"]),
            "Unit": "Count",
            "Dimensions": dimensions,
            "Timestamp": event_time,
            "StorageResolution": 60,
        },
        {
            "MetricName": "duration_ms",
            "Value": float(run["duration_ms"]),
            "Unit": "Milliseconds",
            "Dimensions": dimensions,
            "Timestamp": event_time,
            "StorageResolution": 60,
        },
        {
            "MetricName": "lag_seconds",
            "Value": float(run["lag_seconds"]),
            "Unit": "Seconds",
            "Dimensions": dimensions,
            "Timestamp": event_time,
            "StorageResolution": 60,
        },
    ]

    try:
        cw.put_metric_data(Namespace=NAMESPACE, MetricData=metric_data)
    except ClientError as exc:
        code = exc.response["Error"]["Code"]
        print(f"PutMetricData failed: {code}")
        raise

    stream_name = f"{PIPELINE_NAME}-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
    log_event = dict(run)
    log_event["timestamp"] = event_time.isoformat()

    put_structured_log(stream_name=stream_name, event=log_event, event_time=event_time)


def emit_24_hours(failure_hours: list[int] | None = None) -> None:
    """
    Emit 24 hours of hourly pipeline metrics.

    WHY:
        A 24-hour window gives dashboards and Insights queries enough history to
        show normal behavior plus failure windows without requiring real pipeline runs.

    Args:
        failure_hours (list[int] | None): Hour offsets where failures are injected.

    Returns:
        None.

    Raises:
        ClientError: If AWS metric or log emission fails.
    """
    if failure_hours is None:
        failure_hours = [6, 18]

    random.seed(42)

    print("⚠️  COST WARNING: Custom metrics cost $0.30/metric/month after the free tier.")
    print("⚠️  COST WARNING: CloudWatch Logs charge for ingestion and storage.")

    for hour in range(23, -1, -1):
        inject_failure = hour in failure_hours
        run = simulate_pipeline_run(hour_offset=hour, inject_failure=inject_failure)
        emit_run_metrics(run=run, hour_offset=hour)

        print(
            f"Hour -{hour}: "
            f"records_in={run['records_in']}, "
            f"errors={run['error_count']}, "
            f"lag={run['lag_seconds']}s"
        )


def main() -> None:
    """
    Run the capstone metric emission demo.

    WHY:
        This creates the data foundation for the capstone: metrics for alarms and
        dashboards, plus structured logs for Logs Insights investigation.

    Args:
        None.

    Returns:
        None.

    Raises:
        ClientError: If AWS API calls fail unexpectedly.
    """
    create_log_group(retention_days=7)
    emit_24_hours(failure_hours=[4, 16])
    print("Emitted 24 hours of pipeline metrics. 2 failure hours injected (4h ago, 16h ago).")


if __name__ == "__main__":
    main()