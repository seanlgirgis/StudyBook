# ============================================================
# Topic   : AWS EMR for Data Engineers
# File    : cleanup_tutorial_resources.py
# Covers  : Cleanup resources created by tutorials 01-05
# Prereqs : pip install boto3 | AWS credentials configured | S3 bucket
# Run     : python cleanup_tutorial_resources.py
# ============================================================

from __future__ import annotations

import os
import time
from typing import Any

import boto3
from botocore.exceptions import ClientError


AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
AWS_PROFILE = os.environ.get("AWS_PROFILE")
EMR_S3_BUCKET = os.environ.get("EMR_S3_BUCKET")

S3_PREFIXES = [
    "emr-scripts/",
    "emr-logs/",
    "emr-serverless-logs/",
    "sample/category_output/",
]

SERVERLESS_NAME_PREFIXES = [
    "studybook-emr-serverless-",
]

CLUSTER_NAME_PREFIXES = [
    "studybook-emr-basics-",
]

CLOUDWATCH_ALARM_PREFIXES = [
    "emr-",
]


def get_boto3_session() -> boto3.session.Session:
    if AWS_PROFILE:
        return boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
    return boto3.Session(region_name=AWS_REGION)


def get_emr_client() -> Any:
    return get_boto3_session().client("emr")


def get_emr_serverless_client() -> Any:
    return get_boto3_session().client("emr-serverless")


def get_s3_client() -> Any:
    return get_boto3_session().client("s3")


def get_cloudwatch_client() -> Any:
    return get_boto3_session().client("cloudwatch")


def delete_s3_prefix(bucket: str, prefix: str) -> int:
    s3 = get_s3_client()
    paginator = s3.get_paginator("list_objects_v2")
    deleted = 0

    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        objects = [{"Key": item["Key"]} for item in page.get("Contents", [])]

        if not objects:
            continue

        s3.delete_objects(
            Bucket=bucket,
            Delete={"Objects": objects},
        )
        deleted += len(objects)

    return deleted


def cleanup_s3() -> int:
    if not EMR_S3_BUCKET:
        print("EMR_S3_BUCKET is not set. Skipping S3 cleanup.")
        return 0

    total = 0

    for prefix in S3_PREFIXES:
        count = delete_s3_prefix(EMR_S3_BUCKET, prefix)
        total += count
        print(f"Deleted {count} objects from s3://{EMR_S3_BUCKET}/{prefix}")

    return total


def terminate_matching_emr_clusters() -> int:
    emr = get_emr_client()
    terminated = 0

    active_states = [
        "STARTING",
        "BOOTSTRAPPING",
        "RUNNING",
        "WAITING",
    ]

    response = emr.list_clusters(ClusterStates=active_states)

    for cluster in response.get("Clusters", []):
        cluster_id = cluster["Id"]
        cluster_name = cluster["Name"]

        if not any(cluster_name.startswith(prefix) for prefix in CLUSTER_NAME_PREFIXES):
            continue

        print(f"Terminating EMR cluster: {cluster_name} ({cluster_id})")

        try:
            emr.terminate_job_flows(JobFlowIds=[cluster_id])
            terminated += 1
        except ClientError as exc:
            message = exc.response.get("Error", {}).get("Message", "").lower()
            if "already terminated" not in message:
                raise

    return terminated


def stop_and_delete_serverless_app(application_id: str) -> None:
    client = get_emr_serverless_client()

    try:
        response = client.get_application(applicationId=application_id)
        state = response["application"]["state"]

        if state not in {"STOPPED", "CREATED"}:
            client.stop_application(applicationId=application_id)

            start = time.time()
            while time.time() - start < 300:
                response = client.get_application(applicationId=application_id)
                state = response["application"]["state"]
                print(f"Stopping EMR Serverless app {application_id}: {state}")

                if state == "STOPPED":
                    break

                time.sleep(10)

        client.delete_application(applicationId=application_id)
        print(f"Deleted EMR Serverless app: {application_id}")

    except ClientError as exc:
        code = exc.response.get("Error", {}).get("Code", "")
        if code in {"ResourceNotFoundException", "ValidationException"}:
            return
        raise


def cleanup_serverless_apps() -> int:
    client = get_emr_serverless_client()
    paginator = client.get_paginator("list_applications")
    deleted = 0

    for page in paginator.paginate():
        for app in page.get("applications", []):
            app_name = app.get("name", "")
            app_id = app.get("id")

            if any(app_name.startswith(prefix) for prefix in SERVERLESS_NAME_PREFIXES):
                print(f"Cleaning EMR Serverless app: {app_name} ({app_id})")
                stop_and_delete_serverless_app(app_id)
                deleted += 1

    return deleted


def cleanup_cloudwatch_alarms() -> int:
    cloudwatch = get_cloudwatch_client()
    paginator = cloudwatch.get_paginator("describe_alarms")
    alarm_names: list[str] = []

    for page in paginator.paginate():
        for alarm in page.get("MetricAlarms", []):
            name = alarm.get("AlarmName", "")

            is_emr_alarm = (
                name.startswith("emr-")
                and (
                    name.endswith("-low-memory")
                    or name.endswith("-high-pending")
                )
            )

            if is_emr_alarm:
                alarm_names.append(name)

    deleted = 0

    for index in range(0, len(alarm_names), 100):
        batch = alarm_names[index:index + 100]
        if batch:
            cloudwatch.delete_alarms(AlarmNames=batch)
            deleted += len(batch)

    if deleted:
        print(f"Deleted CloudWatch alarms: {deleted}")
    else:
        print("Deleted CloudWatch alarms: 0")

    return deleted


def main() -> None:
    print("AWS EMR Tutorial Cleanup")
    print("=" * 72)

    total_s3 = cleanup_s3()
    total_clusters = terminate_matching_emr_clusters()
    total_apps = cleanup_serverless_apps()
    total_alarms = cleanup_cloudwatch_alarms()

    print("=" * 72)
    print(f"S3 objects deleted              : {total_s3}")
    print(f"EMR clusters termination started: {total_clusters}")
    print(f"EMR Serverless apps deleted     : {total_apps}")
    print(f"CloudWatch alarms deleted       : {total_alarms}")
    print("✅ Cleanup complete. No ongoing charges.")


if __name__ == "__main__":
    main()