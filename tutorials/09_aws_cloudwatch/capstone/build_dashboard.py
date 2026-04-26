# ============================================================
# Topic   : AWS CloudWatch for Data Engineers
# File    : capstone/build_dashboard.py
# Covers  : Build a 5-widget CloudWatch pipeline health dashboard
# Prereqs : pip install boto3 | AWS credentials | profile: study
# Run     : python capstone/build_dashboard.py
# ============================================================

from __future__ import annotations

import json
import os
from typing import Any
from urllib.parse import quote

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
        Dashboards must be created in the same region as the metrics they display.
        Centralized client creation prevents confusing cross-region dashboard gaps.

    Args:
        None.

    Returns:
        Any: boto3 CloudWatch client.

    Raises:
        botocore.exceptions.BotoCoreError: If boto3 cannot create the client.
    """
    session = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
    return session.client("cloudwatch")


def build_widgets(namespace: str, pipeline_name: str) -> list[dict[str, Any]]:
    """
    Build exactly five dashboard widgets for the capstone pipeline.

    WHY:
        A useful pipeline dashboard should answer four questions fast:
        how much data arrived, how much was produced, how long it took, and
        whether failures or lag are present.

    Args:
        namespace (str): CloudWatch metric namespace.
        pipeline_name (str): PipelineName dimension value.

    Returns:
        list[dict[str, Any]]: Five CloudWatch dashboard widget definitions.

    Raises:
        None.
    """
    return [
        {
            "type": "text",
            "x": 0,
            "y": 0,
            "width": 24,
            "height": 2,
            "properties": {
                "markdown": "# IoT Ingest Pipeline — Health Dashboard",
            },
        },
        {
            "type": "metric",
            "x": 0,
            "y": 2,
            "width": 12,
            "height": 6,
            "properties": {
                "title": "Records In / Records Out — Last 24h",
                "region": AWS_REGION,
                "view": "timeSeries",
                "stacked": False,
                "period": 3600,
                "stat": "Average",
                "metrics": [
                    [
                        namespace,
                        "records_in",
                        "PipelineName",
                        pipeline_name,
                        {"label": "records_in"},
                    ],
                    [
                        ".",
                        "records_out",
                        ".",
                        ".",
                        {"label": "records_out"},
                    ],
                ],
            },
        },
        {
            "type": "metric",
            "x": 12,
            "y": 2,
            "width": 12,
            "height": 6,
            "properties": {
                "title": "Duration ms — Average and p90",
                "region": AWS_REGION,
                "view": "timeSeries",
                "stacked": False,
                "period": 3600,
                "metrics": [
                    [
                        namespace,
                        "duration_ms",
                        "PipelineName",
                        pipeline_name,
                        {"stat": "Average", "label": "duration_avg"},
                    ],
                    [
                        ".",
                        "duration_ms",
                        ".",
                        ".",
                        {"stat": "p90", "label": "duration_p90"},
                    ],
                ],
            },
        },
        {
            "type": "metric",
            "x": 0,
            "y": 8,
            "width": 12,
            "height": 6,
            "properties": {
                "title": "Error Count — Sum Last 24h",
                "region": AWS_REGION,
                "view": "bar",
                "stacked": False,
                "period": 3600,
                "stat": "Sum",
                "metrics": [
                    [
                        namespace,
                        "error_count",
                        "PipelineName",
                        pipeline_name,
                        {"label": "error_count"},
                    ],
                ],
            },
        },
        {
            "type": "metric",
            "x": 12,
            "y": 8,
            "width": 12,
            "height": 6,
            "properties": {
                "title": "Lag Seconds — Latest",
                "region": AWS_REGION,
                "view": "singleValue",
                "period": 3600,
                "stat": "Maximum",
                "metrics": [
                    [
                        namespace,
                        "lag_seconds",
                        "PipelineName",
                        pipeline_name,
                        {"label": "latest_lag_seconds"},
                    ],
                ],
            },
        },
    ]


def get_dashboard_url(name: str) -> str:
    """
    Build the AWS Console URL for the dashboard.

    WHY:
        Scripts should print direct console links so operators can move from
        automation output to visual investigation immediately.

    Args:
        name (str): Dashboard name.

    Returns:
        str: CloudWatch dashboard URL.

    Raises:
        None.
    """
    return (
        f"https://console.aws.amazon.com/cloudwatch/home"
        f"?region={AWS_REGION}#dashboards:name={quote(name)}"
    )


def create_pipeline_dashboard(name: str) -> str:
    """
    Create the capstone CloudWatch dashboard.

    WHY:
        Code-defined dashboards are reproducible. That matters for real data
        platforms where dev/stage/prod observability should look the same.

    Args:
        name (str): Dashboard name.

    Returns:
        str: Dashboard console URL.

    Raises:
        ClientError: If PutDashboard fails.
    """
    client = get_cw_client()
    widgets = build_widgets(NAMESPACE, PIPELINE_NAME)

    try:
        client.put_dashboard(
            DashboardName=name,
            DashboardBody=json.dumps({"widgets": widgets}),
        )
        print(f"Created dashboard: {name}")
        print("⚠️  COST WARNING: CloudWatch Dashboards cost about $3.00/month.")
        return get_dashboard_url(name)
    except ClientError as exc:
        code = exc.response["Error"]["Code"]
        print(f"PutDashboard failed: {code}")
        raise


def delete_dashboard(name: str) -> None:
    """
    Delete the capstone dashboard idempotently.

    WHY:
        Dashboards are billable monthly. Cleanup must be safe to run even when
        the dashboard was already removed.

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


def main() -> None:
    """
    Create the capstone dashboard and leave it for the full capstone flow.

    WHY:
        This file intentionally does not delete the dashboard in main because
        capstone.py and cleanup.py use it after creation.

    Args:
        None.

    Returns:
        None.

    Raises:
        ClientError: If AWS API calls fail unexpectedly.
    """
    url = create_pipeline_dashboard("capstone-pipeline-health")
    print(f"Dashboard created: {url}")
    print("Run capstone/cleanup.py to remove all resources.")


if __name__ == "__main__":
    main()