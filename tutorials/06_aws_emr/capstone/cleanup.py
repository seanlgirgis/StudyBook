# ============================================================
# Topic   : AWS EMR for Data Engineers
# File    : capstone/cleanup.py
# Covers  : Delete S3 data and EMR Serverless applications created by the capstone
# Prereqs : pip install boto3 | AWS credentials configured | S3 bucket
# Run     : python capstone/cleanup.py
# ============================================================

from __future__ import annotations

import os
import time
from typing import Any

import boto3
from botocore.exceptions import ClientError


# Environment variables used by this file:
# - AWS_REGION: AWS region for S3 and EMR Serverless.
# - AWS_PROFILE: Optional AWS profile.
# - EMR_S3_BUCKET: Bucket containing capstone data.
#
# Cost note:
# This script deletes all generated data and applications to stop storage and compute charges.

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
AWS_PROFILE = os.environ.get("AWS_PROFILE")
EMR_S3_BUCKET = os.environ.get("EMR_S3_BUCKET")

PREFIXES = [
    "raw/weblogs/",
    "processed/weblogs/",
    "emr-scripts/",
    "emr-serverless-logs/",
]


def get_boto3_session() -> boto3.session.Session:
    if AWS_PROFILE:
        return boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
    return boto3.Session(region_name=AWS_REGION)


def get_s3_client() -> Any:
    return get_boto3_session().client("s3")


def get_emr_serverless_client() -> Any:
    return get_boto3_session().client("emr-serverless")


def delete_s3_prefix(bucket: str, prefix: str) -> int:
    """
    Delete all objects under a prefix. Return number of deleted objects.
    """
    s3 = get_s3_client()
    paginator = s3.get_paginator("list_objects_v2")

    total_deleted = 0

    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        contents = page.get("Contents", [])
        if not contents:
            continue

        objects = [{"Key": obj["Key"]} for obj in contents]

        s3.delete_objects(Bucket=bucket, Delete={"Objects": objects})
        total_deleted += len(objects)

    return total_deleted


def stop_and_delete_application(application_id: str) -> None:
    """
    Stop and delete an EMR Serverless application.
    """
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
                print(f"Stopping application {application_id}: {state}")

                if state == "STOPPED":
                    break

                time.sleep(10)

        client.delete_application(applicationId=application_id)
        print(f"Deleted EMR Serverless application: {application_id}")

    except ClientError as exc:
        code = exc.response.get("Error", {}).get("Code", "")
        if code in {"ResourceNotFoundException", "ValidationException"}:
            return
        raise


def cleanup_serverless_apps() -> int:
    """
    Delete all EMR Serverless applications with prefix studybook-log-processor-
    """
    client = get_emr_serverless_client()

    deleted_count = 0

    paginator = client.get_paginator("list_applications")

    for page in paginator.paginate():
        apps = page.get("applications", [])
        for app in apps:
            name = app.get("name", "")
            app_id = app.get("id")

            if name.startswith("studybook-log-processor-"):
                print(f"Cleaning up application: {name} ({app_id})")
                stop_and_delete_application(app_id)
                deleted_count += 1

    return deleted_count


def main() -> None:
    if not EMR_S3_BUCKET:
        print("Set EMR_S3_BUCKET before running cleanup.")
        return

    print("Starting capstone cleanup")
    print("=" * 72)

    try:
        total_deleted = 0

        for prefix in PREFIXES:
            count = delete_s3_prefix(EMR_S3_BUCKET, prefix)
            print(f"Deleted {count} objects from s3://{EMR_S3_BUCKET}/{prefix}")
            total_deleted += count

        app_count = cleanup_serverless_apps()
        print(f"Deleted {app_count} EMR Serverless applications")

        print("=" * 72)
        print(f"Total S3 objects deleted: {total_deleted}")
        print("✅ Cleanup complete. No ongoing charges.")

    finally:
        pass


if __name__ == "__main__":
    main()