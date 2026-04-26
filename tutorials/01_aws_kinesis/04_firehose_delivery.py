# ============================================================
# Topic   : AWS Kinesis
# File    : 04_firehose_delivery.py
# Covers  : Kinesis Firehose delivery to S3, batching, buffering, and cleanup
# Prereqs : pip install boto3 | AWS credentials configured
# Run     : python 04_firehose_delivery.py
# ============================================================

"""
Environment variables:
  AWS_REGION            — default "us-east-1"
  AWS_PROFILE           — default "study"
  FIREHOSE_STREAM_NAME  — default "studybook-firehose-{uuid4 first 8 chars}"
  FIREHOSE_S3_BUCKET    — required for Firehose creation
  FIREHOSE_IAM_ROLE_ARN — required for Firehose creation
  SNS_TOPIC_ARN         — optional, unused in this file
"""

import json
import os
import random
import time
import uuid
from typing import Any

import boto3
from botocore.exceptions import ClientError, ProfileNotFound


AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_PROFILE = os.getenv("AWS_PROFILE", "study")
FIREHOSE_NAME = os.getenv(
    "FIREHOSE_STREAM_NAME",
    f"studybook-firehose-{uuid.uuid4().hex[:8]}",
)


def get_client() -> Any:
    """Return boto3 Firehose client using AWS_PROFILE session."""
    try:
        session = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
        return session.client("firehose")
    except ProfileNotFound as exc:
        raise RuntimeError(
            f"AWS profile '{AWS_PROFILE}' was not found. "
            "Set AWS_PROFILE or configure the profile with aws configure."
        ) from exc


def wait_for_firehose_active(name: str, timeout_s: int = 180) -> None:
    """Poll Firehose status until ACTIVE."""
    client = get_client()
    deadline = time.time() + timeout_s

    while time.time() < deadline:
        response = client.describe_delivery_stream(DeliveryStreamName=name)
        status = response["DeliveryStreamDescription"]["DeliveryStreamStatus"]

        if status == "ACTIVE":
            print(f"Firehose delivery stream '{name}' is ACTIVE.")
            return

        print(f"Waiting for Firehose '{name}' to become ACTIVE. Current: {status}")
        time.sleep(5)

    raise TimeoutError(f"Timed out waiting for Firehose '{name}' to become ACTIVE.")


def create_firehose_to_s3(
    name: str,
    bucket: str,
    prefix: str,
    role_arn: str,
    buffer_seconds: int = 60,
    buffer_mb: int = 5,
) -> str:
    """
    Create Kinesis Firehose delivery stream to S3.

    Uses ExtendedS3DestinationConfiguration.

    WHY buffering:
      Firehose batches records before writing to S3.
      Smaller buffer = more files and possible small-file problem.
      Larger buffer = fewer files but higher delivery latency.
      60s/5MB is a good default for analytics workloads.
    """
    client = get_client()

    if not bucket:
        raise ValueError("bucket is required.")
    if not role_arn:
        raise ValueError("role_arn is required.")
    if buffer_seconds < 60 or buffer_seconds > 900:
        raise ValueError("buffer_seconds must be between 60 and 900.")
    if buffer_mb < 1 or buffer_mb > 128:
        raise ValueError("buffer_mb must be between 1 and 128.")

    try:
        response = client.create_delivery_stream(
            DeliveryStreamName=name,
            DeliveryStreamType="DirectPut",
            ExtendedS3DestinationConfiguration={
                "RoleARN": role_arn,
                "BucketARN": f"arn:aws:s3:::{bucket}",
                "Prefix": prefix,
                "ErrorOutputPrefix": f"{prefix.rstrip('/')}/errors/",
                "BufferingHints": {
                    "SizeInMBs": buffer_mb,
                    "IntervalInSeconds": buffer_seconds,
                },
                "CompressionFormat": "UNCOMPRESSED",
            },
        )
    except ClientError as exc:
        code = exc.response.get("Error", {}).get("Code", "")
        if code == "ResourceInUseException":
            raise RuntimeError(
                f"Firehose delivery stream '{name}' already exists. "
                "Refusing to silently continue."
            ) from exc
        raise

    print(
        f"⚠️  COST: Kinesis Firehose '{name}' is running. "
        "~$0.029/GB ingested until deleted."
    )

    wait_for_firehose_active(name)

    return response["DeliveryStreamARN"]


def describe_firehose(name: str) -> dict[str, Any]:
    """
    Return delivery stream description and print formatted details.
    """
    client = get_client()
    response = client.describe_delivery_stream(DeliveryStreamName=name)
    desc = response["DeliveryStreamDescription"]

    destination = desc["Destinations"][0]
    extended_s3 = destination.get("ExtendedS3DestinationDescription", {})

    bucket_arn = extended_s3.get("BucketARN", "unknown")
    bucket = bucket_arn.replace("arn:aws:s3:::", "")
    prefix = extended_s3.get("Prefix", "")
    buffering = extended_s3.get("BufferingHints", {})

    print(f"Stream:      {desc['DeliveryStreamName']}")
    print(f"Status:      {desc['DeliveryStreamStatus']}")
    print(f"Destination: s3://{bucket}/{prefix}")
    print(
        "Buffer:      "
        f"{buffering.get('IntervalInSeconds', 'unknown')}s / "
        f"{buffering.get('SizeInMBs', 'unknown')}MB"
    )

    return desc


def put_firehose_record(client: Any, stream: str, data: dict[str, Any]) -> dict[str, Any]:
    """
    Send one record to Firehose.

    Data dict → JSON bytes + newline.

    WHY newline:
      Firehose concatenates records in S3 files.
      Without newlines, the output can become unparseable JSON.
    """
    payload = json.dumps(data).encode("utf-8") + b"\n"

    response = client.put_record(
        DeliveryStreamName=stream,
        Record={"Data": payload},
    )

    print(f"Sent Firehose record: {response['RecordId'][:16]}...")
    return response


def put_firehose_batch(
    client: Any,
    stream: str,
    records: list[dict[str, Any]],
) -> dict[str, int]:
    """
    PutRecordBatch — up to 500 records or 4 MB per call.

    Handles partial failures.
    """
    if not records:
        return {"sent": 0, "failed": 0}

    if len(records) > 500:
        raise ValueError("Firehose PutRecordBatch accepts at most 500 records.")

    entries = [
        {"Data": json.dumps(record).encode("utf-8") + b"\n"}
        for record in records
    ]

    response = client.put_record_batch(
        DeliveryStreamName=stream,
        Records=entries,
    )

    failed = int(response.get("FailedPutCount", 0))
    sent = len(records) - failed

    if failed > 0:
        print(f"⚠️  Firehose partial failure: {failed} records failed.")

        for result in response.get("RequestResponses", []):
            if "ErrorCode" in result:
                print(
                    f"  ErrorCode={result.get('ErrorCode')} "
                    f"ErrorMessage={result.get('ErrorMessage')}"
                )

    return {"sent": sent, "failed": failed}


def calculate_buffer_tradeoffs(records_per_sec: int, record_size_bytes: int) -> None:
    """
    Print table showing buffering tradeoffs.

    Fewer, larger files are generally better for S3/Athena query performance.
    """
    if records_per_sec <= 0:
        raise ValueError("records_per_sec must be > 0.")
    if record_size_bytes <= 0:
        raise ValueError("record_size_bytes must be > 0.")

    print("buffer_s | files_per_hour | avg_file_size_mb | latency_s")
    print("---------|----------------|------------------|----------")

    for buffer_seconds in [30, 60, 120, 300]:
        bytes_per_buffer = records_per_sec * record_size_bytes * buffer_seconds
        avg_file_size_mb = bytes_per_buffer / (1024 * 1024)
        files_per_hour = 3600 / buffer_seconds

        print(
            f"{buffer_seconds:8d} | "
            f"{files_per_hour:14.1f} | "
            f"{avg_file_size_mb:16.2f} | "
            f"{buffer_seconds:9d}"
        )

    print()
    print("Interpretation:")
    print("- Smaller buffers reduce latency but create more S3 files.")
    print("- More files can slow Athena/Spark queries due to small-file overhead.")
    print("- Larger buffers improve file size but increase delivery latency.")


def cleanup(firehose_name: str) -> None:
    """
    Delete Firehose stream. Catch already-deleted errors silently.
    """
    client = get_client()

    try:
        client.delete_delivery_stream(
            DeliveryStreamName=firehose_name,
            AllowForceDelete=True,
        )
        print(f"Deleted Firehose delivery stream '{firehose_name}'.")
    except ClientError as exc:
        code = exc.response.get("Error", {}).get("Code", "")
        if code in {"ResourceNotFoundException", "ResourceNotFound"}:
            pass
        else:
            raise
    finally:
        print("✅ Cleanup complete. No ongoing charges.")


def main() -> None:
    bucket = os.getenv("FIREHOSE_S3_BUCKET")
    role_arn = os.getenv("FIREHOSE_IAM_ROLE_ARN")

    if not bucket or not role_arn:
        print("FIREHOSE_S3_BUCKET and FIREHOSE_IAM_ROLE_ARN not set.")
        print("Showing buffer tradeoff calculation only (no AWS resources created).")
        print()
        calculate_buffer_tradeoffs(records_per_sec=1000, record_size_bytes=500)
        return

    resources: dict[str, str | None] = {"firehose": None}

    try:
        client = get_client()

        print("\n=== CREATE FIREHOSE TO S3 ===")
        arn = create_firehose_to_s3(
            name=FIREHOSE_NAME,
            bucket=bucket,
            prefix="studybook/kinesis/",
            role_arn=role_arn,
            buffer_seconds=60,
            buffer_mb=5,
        )
        resources["firehose"] = FIREHOSE_NAME
        print(f"Firehose ARN: {arn}")

        print("\n=== DESCRIBE ===")
        describe_firehose(FIREHOSE_NAME)

        print("\n=== SEND SINGLE RECORD ===")
        put_firehose_record(
            client,
            FIREHOSE_NAME,
            {
                "sensor_id": "sensor_single",
                "temp": round(random.uniform(20, 90), 2),
                "ts": time.time(),
            },
        )

        print("\n=== SEND 50 RECORDS ===")
        records = [
            {
                "sensor_id": f"s{i}",
                "temp": round(random.uniform(20, 90), 2),
                "ts": time.time(),
            }
            for i in range(50)
        ]
        result = put_firehose_batch(client, FIREHOSE_NAME, records)
        print(result)

        print("\n=== BUFFER TRADEOFFS ===")
        calculate_buffer_tradeoffs(records_per_sec=1000, record_size_bytes=500)

    finally:
        if resources["firehose"]:
            cleanup(resources["firehose"])


if __name__ == "__main__":
    main()