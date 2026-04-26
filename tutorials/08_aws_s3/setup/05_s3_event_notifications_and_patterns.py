# ============================================================
# Topic   : AWS S3 for Data Engineers
# File    : 05_s3_event_notifications_and_patterns.py
# Covers  : S3 as event source — notifications, S3 Select, inventory, common DE patterns
# Prereqs : pip install boto3 | AWS credentials | S3 bucket
# Run     : python 05_s3_event_notifications_and_patterns.py
# ============================================================

import csv
import io
import json
import os
from datetime import datetime, date, timedelta, timezone
from pathlib import Path

import boto3
from botocore.exceptions import ClientError


AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_PROFILE = os.getenv("AWS_PROFILE")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
SQS_QUEUE_ARN = os.getenv("SQS_QUEUE_ARN")
S3_INVENTORY_DESTINATION_BUCKET = os.getenv("S3_INVENTORY_DESTINATION_BUCKET")


def get_s3_client():
    """
    Create an S3 client using the normal AWS credential chain.

    WHY:
    Local dev can use AWS_PROFILE. Production jobs should use IAM roles from
    Glue, Lambda, ECS, EC2, MWAA, or another managed runtime.
    """
    if AWS_PROFILE:
        session = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
    else:
        session = boto3.Session(region_name=AWS_REGION)

    return session.client("s3")


def configure_sqs_notification(bucket, queue_arn, events, prefix_filter=None):
    """
    Configure S3 event notifications to publish matching events to SQS.

    WHY:
    This is a common data engineering ingestion pattern:
    file lands in S3 -> event goes to SQS -> worker processes file.

    GOTCHA:
    S3 notifications are at-least-once. Your consumer must be idempotent because
    duplicate events can happen.
    """
    if not queue_arn:
        raise ValueError("queue_arn is required")

    s3 = get_s3_client()

    queue_config = {
        "Id": "s3-object-created-to-sqs",
        "QueueArn": queue_arn,
        "Events": events,
    }

    if prefix_filter:
        queue_config["Filter"] = {
            "Key": {
                "FilterRules": [
                    {
                        "Name": "prefix",
                        "Value": prefix_filter,
                    }
                ]
            }
        }

    config = {
        "QueueConfigurations": [queue_config]
    }

    s3.put_bucket_notification_configuration(
        Bucket=bucket,
        NotificationConfiguration=config,
    )

    print(f"Configured SQS notification on bucket: {bucket}")


def query_object_with_s3_select(bucket, key, sql, input_format="CSV"):
    """
    Query part of an S3 object using S3 Select.

    WHY:
    S3 Select can reduce data transfer when you only need a subset of rows/columns.

    GOTCHA:
    S3 Select supports limited formats and SQL features. It is useful for targeted
    filtering, not a replacement for Athena, Spark, or a warehouse.
    """
    s3 = get_s3_client()

    if input_format.upper() != "CSV":
        raise ValueError("This tutorial function currently supports CSV only")

    try:
        response = s3.select_object_content(
            Bucket=bucket,
            Key=key,
            ExpressionType="SQL",
            Expression=sql,
            InputSerialization={
                "CSV": {
                    "FileHeaderInfo": "USE",
                    "RecordDelimiter": "\n",
                    "FieldDelimiter": ",",
                }
            },
            OutputSerialization={
                "CSV": {}
            },
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "MethodNotAllowed":
            print("WARNING: S3 Select is disabled on this bucket (deprecated). Skipping Select query.")
            return ""
        raise

    records = []

    for event in response["Payload"]:
        if "Records" in event:
            records.append(event["Records"]["Payload"].decode("utf-8"))

    return "".join(records)


def design_data_lake_prefix(environment, domain, date_value):
    """
    Return a consistent data lake prefix.

    WHY:
    Prefix design is not cosmetic. It controls discoverability, lifecycle rules,
    partition pruning, access policy boundaries, and operational clarity.

    Example:
    raw/iot/year=2026/month=04/day=25/
    """
    if isinstance(date_value, str):
        parsed_date = datetime.strptime(date_value, "%Y-%m-%d").date()
    elif isinstance(date_value, date):
        parsed_date = date_value
    else:
        raise TypeError("date_value must be a YYYY-MM-DD string or date object")

    return (
        f"{environment}/{domain}/"
        f"year={parsed_date.year:04d}/"
        f"month={parsed_date.month:02d}/"
        f"day={parsed_date.day:02d}/"
    )


def list_objects_by_date_range(bucket, prefix, start_date, end_date):
    """
    List objects under a prefix and filter by LastModified date.

    WHY:
    This is useful for operational checks, backfills, and finding recently landed
    files when event notifications are unavailable.

    GOTCHA:
    Filtering by LastModified happens client-side here. For large buckets, prefer
    partitioned prefixes, S3 Inventory, Athena, or object metadata catalogs.
    """
    s3 = get_s3_client()
    paginator = s3.get_paginator("list_objects_v2")

    if isinstance(start_date, str):
        start_date = datetime.fromisoformat(start_date).replace(tzinfo=timezone.utc)

    if isinstance(end_date, str):
        end_date = datetime.fromisoformat(end_date).replace(tzinfo=timezone.utc)

    matches = []

    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            last_modified = obj["LastModified"]

            if start_date <= last_modified <= end_date:
                matches.append(
                    {
                        "Key": obj["Key"],
                        "Size": obj["Size"],
                        "LastModified": last_modified.isoformat(),
                        "StorageClass": obj.get("StorageClass", "STANDARD"),
                    }
                )

    return matches


def create_inventory_config(bucket, destination_bucket, frequency="Weekly"):
    """
    Create an S3 Inventory configuration.

    WHY:
    S3 Inventory is better than listing huge buckets repeatedly. It produces
    scheduled object listings that can be queried by Athena or processed by Spark.

    COST NOTE:
    Inventory has a cost, but it can be cheaper and more reliable than scanning
    massive buckets with ListObjects calls.
    """
    if not destination_bucket:
        raise ValueError("destination_bucket is required")

    s3 = get_s3_client()

    account_id = boto3.client("sts").get_caller_identity()["Account"]

    config = {
        "Destination": {
            "S3BucketDestination": {
                "AccountId": account_id,
                "Bucket": f"arn:aws:s3:::{destination_bucket}",
                "Format": "CSV",
                "Prefix": f"inventory/{bucket}/",
            }
        },
        "IsEnabled": True,
        "Id": "weekly-inventory",
        "IncludedObjectVersions": "Current",
        "Schedule": {
            "Frequency": frequency
        },
        "OptionalFields": [
            "Size",
            "LastModifiedDate",
            "StorageClass",
            "ETag",
            "EncryptionStatus",
        ],
    }

    s3.put_bucket_inventory_configuration(
        Bucket=bucket,
        Id="weekly-inventory",
        InventoryConfiguration=config,
    )

    print(f"Created inventory config for bucket: {bucket}")


def demonstrate_copy_on_ingest(source_bucket, dest_bucket, key):
    """
    Copy an object from raw to bronze and add processing tags.

    WHY:
    Copy-on-ingest is a common lakehouse pattern:
    raw keeps the original landing file, bronze stores validated/accepted files.

    GOTCHA:
    S3 copy creates another object. That means more storage cost. Use it when the
    governance and recovery benefits are worth the extra copy.
    """
    s3 = get_s3_client()

    if not key.startswith("raw/"):
        raise ValueError("Expected source key to start with raw/")

    dest_key = key.replace("raw/", "bronze/", 1)

    s3.copy_object(
        Bucket=dest_bucket,
        Key=dest_key,
        CopySource={
            "Bucket": source_bucket,
            "Key": key,
        },
        MetadataDirective="COPY",
        TaggingDirective="REPLACE",
        Tagging=(
            "zone=bronze"
            "&ingestion_status=validated"
            "&data_classification=internal"
        ),
    )

    print(f"Copied s3://{source_bucket}/{key} -> s3://{dest_bucket}/{dest_key}")

    return dest_key


def upload_demo_csv(bucket, key):
    """
    Upload a small CSV file for S3 Select and copy-on-ingest demos.
    """
    s3 = get_s3_client()

    rows = [
        ["sensor_id", "plant", "metric_name", "value", "event_time"],
        ["s-001", "toyota-tx", "temperature", "70.5", "2026-04-25T10:00:00Z"],
        ["s-002", "toyota-tx", "pressure", "31.2", "2026-04-25T10:01:00Z"],
        ["s-003", "toyota-ky", "temperature", "85.1", "2026-04-25T10:02:00Z"],
        ["s-004", "toyota-ky", "vibration", "12.7", "2026-04-25T10:03:00Z"],
    ]

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerows(rows)

    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=buffer.getvalue().encode("utf-8"),
        ContentType="text/csv",
        Metadata={
            "source_system": "iot_sensor_demo",
            "data_classification": "internal",
        },
        Tagging="zone=raw&source_system=iot_sensor_demo",
    )

    print(f"Uploaded demo CSV: s3://{bucket}/{key}")


def delete_object_if_exists(bucket, key):
    """
    Best-effort cleanup for tutorial objects.
    """
    s3 = get_s3_client()

    try:
        s3.delete_object(Bucket=bucket, Key=key)
        print(f"Deleted: s3://{bucket}/{key}")
    except ClientError as e:
        code = e.response["Error"]["Code"]
        if code not in ("NoSuchKey", "404"):
            raise


def main():
    if not S3_BUCKET_NAME:
        raise RuntimeError(
            "Missing S3_BUCKET_NAME environment variable. "
            "Example: set S3_BUCKET_NAME=my-unique-bucket-name"
        )

    bucket = S3_BUCKET_NAME
    raw_key = "raw/iot/year=2026/month=04/day=25/sensor_sample.csv"

    print("\nData lake prefix examples:")
    scenarios = [
        ("raw", "iot", "2026-04-25"),
        ("bronze", "manufacturing_quality", "2026-04-25"),
        ("curated", "supply_chain", "2026-04-25"),
    ]

    for environment, domain, date_value in scenarios:
        prefix = design_data_lake_prefix(environment, domain, date_value)
        print(f"{environment}/{domain}: {prefix}")

    print("\nUpload demo CSV:")
    upload_demo_csv(bucket, raw_key)

    print("\nS3 Select query:")
    sql = """
    SELECT s.sensor_id, s.plant, s.metric_name, s.value
    FROM S3Object s
    WHERE CAST(s.value AS FLOAT) > 50
    """
    result = query_object_with_s3_select(bucket, raw_key, sql)
    print(result)

    print("\nCopy raw object to bronze:")
    bronze_key = demonstrate_copy_on_ingest(bucket, bucket, raw_key)

    print("\nList objects modified today under raw/:")
    now = datetime.now(timezone.utc)
    start = now - timedelta(days=1)
    matches = list_objects_by_date_range(bucket, "raw/", start, now)
    print(json.dumps(matches, indent=2))

    if SQS_QUEUE_ARN:
        print("\nConfigure SQS notification:")
        configure_sqs_notification(
            bucket=bucket,
            queue_arn=SQS_QUEUE_ARN,
            events=["s3:ObjectCreated:*"],
            prefix_filter="raw/",
        )
    else:
        print("\nSkipping SQS notification: SQS_QUEUE_ARN is not set.")

    if S3_INVENTORY_DESTINATION_BUCKET:
        print("\nCreate S3 Inventory config:")
        create_inventory_config(
            bucket=bucket,
            destination_bucket=S3_INVENTORY_DESTINATION_BUCKET,
            frequency="Weekly",
        )
    else:
        print("\nSkipping inventory config: S3_INVENTORY_DESTINATION_BUCKET is not set.")

    print("\nCleanup demo objects:")
    delete_object_if_exists(bucket, raw_key)
    delete_object_if_exists(bucket, bronze_key)

    print("\nNOTE:")
    print("S3 event notifications are at-least-once, so downstream processing must be idempotent.")
    print("For big lakes, prefer partitioned prefixes + Inventory/Athena over brute-force listing.")


if __name__ == "__main__":
    main()