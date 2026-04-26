# ============================================================
# Topic   : AWS CloudWatch for Data Engineers
# File    : 02_log_groups_and_insights.py
# Covers  : CloudWatch Logs, structured JSON logs, retention, and Logs Insights queries
# Prereqs : pip install boto3 | AWS credentials | profile: study
# Run     : python 02_log_groups_and_insights.py
# ============================================================

from __future__ import annotations

import json
import os
import random
import time
from datetime import datetime, timedelta, timezone
from typing import Any

import boto3
from botocore.exceptions import ClientError


AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_PROFILE = os.getenv("AWS_PROFILE", "study")
CW_NAMESPACE = os.getenv("CW_NAMESPACE", "StudyBook/Pipeline")
CW_LOG_GROUP_NAME = os.getenv("CW_LOG_GROUP_NAME", "/studybook/pipeline")
CW_ALARM_SNS_ARN = os.getenv("CW_ALARM_SNS_ARN")


def get_logs_client() -> Any:
    """
    Create a CloudWatch Logs boto3 client.

    WHY:
        Centralized client creation makes scripts portable across local dev,
        CI, and production-like accounts because region/profile come from env.

    Args:
        None.

    Returns:
        Any: boto3 CloudWatch Logs client.

    Raises:
        botocore.exceptions.BotoCoreError: If boto3 cannot create the client.
    """
    session = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
    return session.client("logs")


def create_log_group(group_name: str, retention_days: int = 30) -> None:
    """
    Create a CloudWatch log group and set retention.

    WHY:
        Log groups without retention can store logs forever. For data pipelines,
        retention is a cost-control guardrail, not an afterthought.

    Args:
        group_name (str): CloudWatch log group name.
        retention_days (int): Number of days to retain logs.

    Returns:
        None.

    Raises:
        ClientError: If AWS returns an unexpected error.
    """
    client = get_logs_client()

    try:
        client.create_log_group(logGroupName=group_name)
        print(f"Created log group: {group_name}")
        print("⚠️  COST WARNING: CloudWatch Logs charges for ingestion and storage.")
    except ClientError as exc:
        code = exc.response["Error"]["Code"]
        if code == "ResourceAlreadyExistsException":
            print(f"Log group already exists: {group_name}")
        else:
            print(f"CreateLogGroup failed: {code}")
            raise

    set_retention_policy(group_name, retention_days)


def ensure_log_stream(group_name: str, stream_name: str) -> None:
    """
    Create a log stream if it does not already exist.

    WHY:
        CloudWatch Logs separates storage into log groups and log streams.
        A common pattern is one group per app and one stream per run/container.

    Args:
        group_name (str): CloudWatch log group name.
        stream_name (str): CloudWatch log stream name.

    Returns:
        None.

    Raises:
        ClientError: If AWS returns an unexpected error.
    """
    client = get_logs_client()

    try:
        client.create_log_stream(
            logGroupName=group_name,
            logStreamName=stream_name,
        )
        print(f"Created log stream: {stream_name}")
    except ClientError as exc:
        code = exc.response["Error"]["Code"]
        if code == "ResourceAlreadyExistsException":
            return
        if code == "ResourceNotFoundException":
            create_log_group(group_name, retention_days=7)
            client.create_log_stream(
                logGroupName=group_name,
                logStreamName=stream_name,
            )
            return

        print(f"CreateLogStream failed: {code}")
        raise


def _get_upload_sequence_token(group_name: str, stream_name: str) -> str | None:
    """
    Read the current upload sequence token for a log stream.

    WHY:
        Older CloudWatch Logs workflows require sequence tokens for repeated
        writes. Reading the token before writing makes this helper safe across
        repeated runs and avoids the classic InvalidSequenceTokenException trap.

    Args:
        group_name (str): CloudWatch log group name.
        stream_name (str): CloudWatch log stream name.

    Returns:
        str | None: Current upload sequence token, or None for a new stream.

    Raises:
        ClientError: If DescribeLogStreams fails unexpectedly.
    """
    client = get_logs_client()

    try:
        response = client.describe_log_streams(
            logGroupName=group_name,
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


def put_log_events(group_name: str, stream_name: str, messages: list[str]) -> None:
    """
    Put ordered log events into a CloudWatch log stream.

    WHY:
        CloudWatch requires log events in timestamp order and repeated writes may
        require a sequence token. This helper hides that operational gotcha.

    Args:
        group_name (str): CloudWatch log group name.
        stream_name (str): CloudWatch log stream name.
        messages (list[str]): Log message strings to write.

    Returns:
        None.

    Raises:
        ValueError: If messages is empty.
        ClientError: If PutLogEvents fails unexpectedly.
    """
    if not messages:
        raise ValueError("messages cannot be empty.")

    client = get_logs_client()
    ensure_log_stream(group_name, stream_name)

    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)

    events = [
        {
            "timestamp": now_ms + index,
            "message": message,
        }
        for index, message in enumerate(messages)
    ]

    request: dict[str, Any] = {
        "logGroupName": group_name,
        "logStreamName": stream_name,
        "logEvents": events,
    }

    token = _get_upload_sequence_token(group_name, stream_name)
    if token:
        request["sequenceToken"] = token

    try:
        client.put_log_events(**request)
    except ClientError as exc:
        code = exc.response["Error"]["Code"]

        if code in {"InvalidSequenceTokenException", "DataAlreadyAcceptedException"}:
            token = _get_upload_sequence_token(group_name, stream_name)
            retry_request = dict(request)
            if token:
                retry_request["sequenceToken"] = token
            elif "sequenceToken" in retry_request:
                del retry_request["sequenceToken"]

            client.put_log_events(**retry_request)
            return

        print(f"PutLogEvents failed: {code}")
        raise


def put_structured_log(group_name: str, stream_name: str, event: dict[str, Any]) -> None:
    """
    Write one structured JSON log event.

    WHY:
        JSON logs turn raw text into queryable operational data. Logs Insights can
        query fields like duration_ms and records_out directly when logs are JSON.

    Args:
        group_name (str): CloudWatch log group name.
        stream_name (str): CloudWatch log stream name.
        event (dict[str, Any]): Structured event payload.

    Returns:
        None.

    Raises:
        ClientError: If CloudWatch Logs writing fails.
    """
    enriched = dict(event)
    enriched["timestamp"] = datetime.now(timezone.utc).isoformat()
    put_log_events(group_name, stream_name, [json.dumps(enriched, default=str)])


def query_logs_insights(
    group_name: str,
    query_string: str,
    start: datetime,
    end: datetime,
    limit: int = 100,
) -> list[dict[str, str]]:
    """
    Run a CloudWatch Logs Insights query and return rows.

    WHY:
        Logs Insights is asynchronous. Production scripts must start the query,
        poll for completion, and keep windows narrow because billing is based on
        GB scanned.

    Args:
        group_name (str): CloudWatch log group name.
        query_string (str): Logs Insights query string.
        start (datetime): Query start time.
        end (datetime): Query end time.
        limit (int): Max returned rows.

    Returns:
        list[dict[str, str]]: Query rows converted from field/value pairs.

    Raises:
        TimeoutError: If the query does not complete.
        ClientError: If Logs Insights API calls fail.
    """
    client = get_logs_client()

    try:
        response = client.start_query(
            logGroupName=group_name,
            startTime=int(start.timestamp()),
            endTime=int(end.timestamp()),
            queryString=query_string,
            limit=limit,
        )
        query_id = response["queryId"]
    except ClientError as exc:
        code = exc.response["Error"]["Code"]
        print(f"StartQuery failed: {code}")
        raise

    for _ in range(30):
        time.sleep(2)

        try:
            result = client.get_query_results(queryId=query_id)
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            print(f"GetQueryResults failed: {code}")
            raise

        status = result.get("status")

        if status == "Complete":
            rows: list[dict[str, str]] = []
            for raw_row in result.get("results", []):
                row = {
                    field["field"]: field.get("value", "")
                    for field in raw_row
                    if field.get("field") != "@ptr"
                }
                rows.append(row)
            return rows

        if status in {"Failed", "Cancelled", "Timeout"}:
            raise RuntimeError(f"Logs Insights query ended with status: {status}")

    raise TimeoutError("Logs Insights query did not complete within 60 seconds.")


def common_queries() -> dict[str, str]:
    """
    Return common CloudWatch Logs Insights queries for data pipelines.

    WHY:
        Senior engineers keep reusable query patterns around. During incidents,
        you do not want to invent syntax while a pipeline is failing.

    Args:
        None.

    Returns:
        dict[str, str]: Query name to Logs Insights query string.

    Raises:
        None.
    """
    return {
        "pipeline_errors": """
            filter @message like /ERROR/
            | sort @timestamp desc
            | limit 20
        """,
        "slow_jobs": """
            filter duration_ms > 5000
            | stats avg(duration_ms) as avg_duration_ms by job_name
            | sort avg_duration_ms desc
        """,
        "hourly_volume": """
            stats count(*) as events by bin(1h)
            | sort bin desc
        """,
        "error_rate": """
            stats sum(is_error) / count(*) * 100 as error_pct by bin(1h)
            | sort bin desc
        """,
    }


def set_retention_policy(group_name: str, days: int) -> None:
    """
    Set retention policy for a CloudWatch log group.

    WHY:
        Retention policies prevent log storage from becoming a silent monthly
        bill. For tutorial and dev logs, short retention is usually best.

    Args:
        group_name (str): CloudWatch log group name.
        days (int): Retention period in days.

    Returns:
        None.

    Raises:
        ClientError: If PutRetentionPolicy fails unexpectedly.
    """
    client = get_logs_client()

    try:
        client.put_retention_policy(
            logGroupName=group_name,
            retentionInDays=days,
        )
        print(f"Retention set to {days} days for {group_name}")
    except ClientError as exc:
        code = exc.response["Error"]["Code"]
        print(f"PutRetentionPolicy failed: {code}")
        raise


def delete_log_group(group_name: str) -> None:
    """
    Delete a CloudWatch log group idempotently.

    WHY:
        Deleting tutorial log groups prevents ongoing storage costs. Idempotent
        cleanup means the script is safe to rerun after partial failures.

    Args:
        group_name (str): CloudWatch log group name.

    Returns:
        None.

    Raises:
        None.
    """
    client = get_logs_client()

    try:
        client.delete_log_group(logGroupName=group_name)
        print(f"Deleted log group: {group_name}")
    except ClientError as exc:
        code = exc.response["Error"]["Code"]
        if code in {"ResourceNotFoundException", "ResourceNotFound"}:
            return

        print(f"DeleteLogGroup failed: {code}")
        raise


def cleanup(group_name: str) -> None:
    """
    Clean up resources created by this file.

    WHY:
        CloudWatch log groups are billable through ingestion and storage.
        Cleanup keeps learning labs safe to run repeatedly.

    Args:
        group_name (str): CloudWatch log group name.

    Returns:
        None.

    Raises:
        None.
    """
    try:
        delete_log_group(group_name)
    finally:
        print("✅  Cleanup complete. No ongoing charges.")


def build_demo_events() -> list[dict[str, Any]]:
    """
    Build synthetic structured log events for a data pipeline.

    WHY:
        Good observability examples need realistic fields: job_name, stage,
        duration, records in/out, and an error flag. These are the fields used
        in real pipeline dashboards and incident queries.

    Args:
        None.

    Returns:
        list[dict[str, Any]]: Synthetic structured events.

    Raises:
        None.
    """
    random.seed(42)

    stages = ["extract", "validate", "transform", "load"]
    jobs = ["iot-ingest", "quality-check", "bronze-writer"]

    events: list[dict[str, Any]] = []

    for index in range(30):
        is_error = 1 if index in {6, 14, 23} else 0
        level = "ERROR" if is_error else "INFO"
        records_in = random.randint(8000, 12000)
        records_out = records_in - random.randint(0, 100)

        if is_error:
            duration_ms = random.randint(7000, 13000)
            error_msg = "ERROR simulated downstream write failure"
        else:
            duration_ms = random.randint(800, 4500)
            error_msg = ""

        events.append(
            {
                "level": level,
                "job_name": random.choice(jobs),
                "stage": random.choice(stages),
                "duration_ms": duration_ms,
                "records_in": records_in,
                "records_out": records_out,
                "is_error": is_error,
                "error_msg": error_msg,
            }
        )

    return events


def print_query_results(title: str, rows: list[dict[str, str]]) -> None:
    """
    Print Logs Insights query results.

    WHY:
        CLI demos should make cloud output visible without forcing the user to
        open the console for every validation step.

    Args:
        title (str): Query title.
        rows (list[dict[str, str]]): Query result rows.

    Returns:
        None.

    Raises:
        None.
    """
    print(f"\n{title}")
    print("-" * len(title))

    if not rows:
        print("No rows returned. Logs Insights can take a short time to index events.")
        return

    for row in rows[:10]:
        print(row)


def main() -> None:
    """
    Run the CloudWatch Logs and Logs Insights demo.

    WHY:
        This demonstrates the operational loop for logs: create group, set
        retention, emit structured events, query them, and delete the resource.

    Args:
        None.

    Returns:
        None.

    Raises:
        ClientError: If AWS API calls fail unexpectedly.
    """
    group_name = CW_LOG_GROUP_NAME
    stream_name = f"demo-run-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"

    try:
        create_log_group(group_name, retention_days=7)
        ensure_log_stream(group_name, stream_name)

        print("\nEmitting 30 structured JSON log events...")
        events = build_demo_events()
        messages = [json.dumps(event, default=str) for event in events]
        put_log_events(group_name, stream_name, messages)

        print("Waiting briefly for CloudWatch Logs indexing...")
        time.sleep(8)

        end = datetime.now(timezone.utc) + timedelta(minutes=2)
        start = end - timedelta(hours=1)

        for name, query in common_queries().items():
            rows = query_logs_insights(
                group_name=group_name,
                query_string=query,
                start=start,
                end=end,
                limit=100,
            )
            print_query_results(name, rows)

    finally:
        cleanup(group_name)


if __name__ == "__main__":
    main()