# ============================================================
# Topic   : AWS CloudWatch for Data Engineers
# File    : capstone/insights_queries.py
# Covers  : Run Logs Insights queries against emitted pipeline logs
# Prereqs : pip install boto3 | AWS credentials | profile: study
# Run     : python capstone/insights_queries.py
# ============================================================

from __future__ import annotations

import os
import time
from datetime import datetime, timedelta, timezone
from typing import Any

import boto3
from botocore.exceptions import ClientError


NAMESPACE = os.getenv("CW_NAMESPACE", "StudyBook/CapstoneP")
LOG_GROUP = os.getenv("CW_LOG_GROUP_NAME", "/studybook/capstone/pipeline")
PIPELINE_NAME = "iot-ingest-hourly"
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_PROFILE = os.getenv("AWS_PROFILE", "study")


def get_logs_client() -> Any:
    """
    Create a CloudWatch Logs client.

    WHY:
        Logs Insights runs through the CloudWatch Logs API, not the CloudWatch
        metrics API. Keeping the client factory explicit avoids mixing services.

    Args:
        None.

    Returns:
        Any: boto3 CloudWatch Logs client.

    Raises:
        botocore.exceptions.BotoCoreError: If boto3 cannot create the client.
    """
    session = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
    return session.client("logs")


def run_query(log_group: str, query: str, hours_back: int = 24) -> list[dict[str, str]]:
    """
    Run one CloudWatch Logs Insights query.

    WHY:
        Logs Insights is asynchronous and billed by data scanned. Production code
        should use tight time windows, poll carefully, and format results clearly.

    Args:
        log_group (str): CloudWatch log group name.
        query (str): Logs Insights query string.
        hours_back (int): Number of hours back from now to query.

    Returns:
        list[dict[str, str]]: Query results as dictionaries.

    Raises:
        RuntimeError: If the query fails, times out, or is cancelled.
        ClientError: If AWS API calls fail unexpectedly.
    """
    client = get_logs_client()

    end = datetime.now(timezone.utc) + timedelta(minutes=5)
    start = end - timedelta(hours=hours_back)

    try:
        response = client.start_query(
            logGroupName=log_group,
            startTime=int(start.timestamp()),
            endTime=int(end.timestamp()),
            queryString=query,
            limit=100,
        )
        query_id = response["queryId"]
    except ClientError as exc:
        code = exc.response["Error"]["Code"]
        print(f"StartQuery failed: {code}")
        raise

    for _ in range(45):
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

            if not rows:
                print("Note: query completed but returned no rows.")
            return rows

        if status in {"Failed", "Cancelled", "Timeout"}:
            raise RuntimeError(f"Logs Insights query ended with status: {status}")

    raise RuntimeError("Logs Insights query did not complete within 90 seconds.")


def print_results(title: str, results: list[dict[str, str]]) -> None:
    """
    Print query results as a small table.

    WHY:
        During incidents, operators need fast readable output. A compact table
        makes script output useful without opening the AWS console.

    Args:
        title (str): Query title.
        results (list[dict[str, str]]): Query result rows.

    Returns:
        None.

    Raises:
        None.
    """
    print(f"\n{title}")
    print("=" * len(title))

    if not results:
        print("No rows returned.")
        return

    columns = list(results[0].keys())

    for row in results[1:]:
        for key in row:
            if key not in columns:
                columns.append(key)

    widths = {
        col: min(
            max(len(col), *(len(str(row.get(col, ""))) for row in results[:10])),
            32,
        )
        for col in columns
    }

    header = " | ".join(f"{col:<{widths[col]}}" for col in columns)
    divider = "-+-".join("-" * widths[col] for col in columns)

    print(header)
    print(divider)

    for row in results[:10]:
        print(
            " | ".join(
                f"{str(row.get(col, ''))[:widths[col]]:<{widths[col]}}"
                for col in columns
            )
        )


def run_all_queries() -> None:
    """
    Run all capstone Logs Insights queries.

    WHY:
        These four queries represent the incident workflow: find slow runs, summarize
        errors, measure throughput, and inspect lag trend.

    Args:
        None.

    Returns:
        None.

    Raises:
        ClientError: If Logs Insights API calls fail unexpectedly.
    """
    queries = {
        "Slow pipeline runs (>25s)": """
            filter duration_ms > 25000
            | fields @timestamp, job_name, duration_ms, records_in
            | sort duration_ms desc
            | limit 10
        """,
        "Error summary by hour": """
            filter level = "ERROR"
            | stats count(*) as error_count by bin(1h)
            | sort bin desc
        """,
        "Daily throughput": """
            stats sum(records_out) as total_out,
                  avg(records_in) as avg_in,
                  count(*) as runs by bin(24h)
        """,
        "Lag trend (1-hour buckets)": """
            filter ispresent(lag_seconds)
            | stats avg(lag_seconds) as avg_lag,
                    max(lag_seconds) as peak_lag
              by bin(1h)
            | sort bin asc
        """,
    }

    for title, query in queries.items():
        rows = run_query(LOG_GROUP, query, hours_back=24)
        print_results(title, rows)


def main() -> None:
    """
    Run the capstone Logs Insights query demo.

    WHY:
        Metrics and dashboards identify symptoms; Logs Insights explains the
        failure windows with structured event fields.

    Args:
        None.

    Returns:
        None.

    Raises:
        ClientError: If AWS API calls fail unexpectedly.
    """
    run_all_queries()
    print("\nInsights queries complete.")


if __name__ == "__main__":
    main()