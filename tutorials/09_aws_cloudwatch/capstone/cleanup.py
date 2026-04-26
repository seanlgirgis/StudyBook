# ============================================================
# Topic   : AWS CloudWatch for Data Engineers
# File    : capstone/cleanup.py
# Covers  : Delete all capstone CloudWatch resources safely
# Prereqs : pip install boto3 | AWS credentials | profile: study
# Run     : python capstone/cleanup.py
# ============================================================

from __future__ import annotations

import os
import time
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
        Cleanup must run against the same AWS profile and region used by the
        capstone build scripts.

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
        The capstone creates a log group, and log groups can keep generating
        storage charges if left behind.

    Args:
        None.

    Returns:
        Any: boto3 CloudWatch Logs client.

    Raises:
        botocore.exceptions.BotoCoreError: If boto3 cannot create the client.
    """
    session = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
    return session.client("logs")


def delete_alarms() -> None:
    """
    Delete all capstone alarms idempotently.

    WHY:
        Composite alarms depend on metric alarms. AWS rejects deleting metric
        alarms first, so delete the composite alarm before deleting its children.

    Args:
        None.

    Returns:
        None.

    Raises:
        ClientError: If AWS returns an unexpected delete failure.
    """
    client = get_cw_client()

    composite_alarms = ["capstone-unhealthy"]
    metric_alarms = [
        "capstone-records-low",
        "capstone-errors",
        "capstone-duration-high",
        "capstone-lag-high",
    ]

    for batch in [composite_alarms, metric_alarms]:
        try:
            client.delete_alarms(AlarmNames=batch)
            for alarm in batch:
                print(f"Deleted alarm or already gone: {alarm}")
            time.sleep(2)
        except ClientError as exc:
            code = exc.response["Error"]["Code"]

            if code in {"ResourceNotFoundException", "ResourceNotFound"}:
                for alarm in batch:
                    print(f"Alarm already gone: {alarm}")
                continue

            print(f"DeleteAlarms failed: {code}")
            raise


def delete_dashboard() -> None:
    """
    Delete the capstone dashboard idempotently.

    WHY:
        CloudWatch dashboards cost about $3/month. Removing the dashboard is the
        most important cleanup step after alarm deletion.

    Args:
        None.

    Returns:
        None.

    Raises:
        ClientError: If AWS returns an unexpected delete failure.
    """
    client = get_cw_client()
    dashboard_name = "capstone-pipeline-health"

    try:
        client.delete_dashboards(DashboardNames=[dashboard_name])
        print(f"Deleted dashboard or already gone: {dashboard_name}")
    except ClientError as exc:
        code = exc.response["Error"]["Code"]

        if code in {"ResourceNotFoundException", "ResourceNotFound"}:
            print(f"Dashboard already gone: {dashboard_name}")
            return

        print(f"DeleteDashboards failed: {code}")
        raise


def delete_log_group() -> None:
    """
    Delete the capstone log group idempotently.

    WHY:
        Logs are billable through ingestion and storage. Deleting the capstone log
        group removes all tutorial log streams and stored events.

    Args:
        None.

    Returns:
        None.

    Raises:
        ClientError: If AWS returns an unexpected delete failure.
    """
    client = get_logs_client()

    try:
        client.delete_log_group(logGroupName=LOG_GROUP)
        print(f"Deleted log group: {LOG_GROUP}")
    except ClientError as exc:
        code = exc.response["Error"]["Code"]

        if code in {"ResourceNotFoundException", "ResourceNotFound"}:
            print(f"Log group already gone: {LOG_GROUP}")
            return

        print(f"DeleteLogGroup failed: {code}")
        raise


def cleanup_all() -> None:
    """
    Delete every persistent resource created by the capstone.

    WHY:
        This is the safety valve for the full lab. Metrics naturally age out, but
        alarms, dashboards, and log groups should be explicitly deleted.

    Args:
        None.

    Returns:
        None.

    Raises:
        ClientError: If AWS cleanup fails unexpectedly.
    """
    delete_alarms()
    delete_dashboard()
    delete_log_group()
    print("✅ Cleanup complete. No ongoing charges.")


def main() -> None:
    """
    Run capstone cleanup.

    WHY:
        Keeping cleanup executable as its own script lets you remove resources
        after running individual capstone files or the full orchestrator.

    Args:
        None.

    Returns:
        None.

    Raises:
        ClientError: If AWS cleanup fails unexpectedly.
    """
    cleanup_all()


if __name__ == "__main__":
    main()