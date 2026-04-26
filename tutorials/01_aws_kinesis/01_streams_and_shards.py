# ============================================================
# Topic   : AWS Kinesis
# File    : 01_streams_and_shards.py
# Covers  : Create, describe, size, update retention, and clean up Kinesis streams
# Prereqs : pip install boto3 | AWS credentials configured
# Run     : python 01_streams_and_shards.py
# ============================================================

"""
Environment variables:
  AWS_REGION          — default "us-east-1"
  AWS_PROFILE         — default "study"
  KINESIS_STREAM_NAME — default "studybook-kinesis-{uuid4 first 8 chars}"
  SNS_TOPIC_ARN       — optional, unused in this file
"""

import math
import os
import time
import uuid
from typing import Any

import boto3
from botocore.exceptions import ClientError, ProfileNotFound


AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_PROFILE = os.getenv("AWS_PROFILE", "study")
STREAM_NAME = os.getenv(
    "KINESIS_STREAM_NAME",
    f"studybook-kinesis-{uuid.uuid4().hex[:8]}",
)


def get_client() -> Any:
    """Return boto3 Kinesis client using AWS_PROFILE session."""
    try:
        session = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
        return session.client("kinesis")
    except ProfileNotFound as exc:
        raise RuntimeError(
            f"AWS profile '{AWS_PROFILE}' was not found. "
            "Set AWS_PROFILE or configure the profile with aws configure."
        ) from exc


def create_stream(name: str, shard_count: int = 1) -> None:
    """
    Create a Kinesis Data Stream and wait until status == ACTIVE.

    Poll describe_stream_summary every 5s, timeout after 120s.
    Print cost warning after creation.

    WHY shard_count=1:
      Minimum for learning. Each shard costs about $0.015/hr.
    """
    client = get_client()

    try:
        client.create_stream(StreamName=name, ShardCount=shard_count)
        print(
            f"⚠️  COST: Kinesis stream '{name}' is running. "
            "~$0.015/shard/hour until deleted."
        )
    except ClientError as exc:
        code = exc.response.get("Error", {}).get("Code", "")
        if code == "ResourceInUseException":
            raise RuntimeError(
                f"Stream '{name}' already exists. Refusing to silently continue."
            ) from exc
        raise

    deadline = time.time() + 120

    while time.time() < deadline:
        summary = describe_stream(name)
        status = summary["StreamStatus"]

        if status == "ACTIVE":
            print(f"Stream '{name}' is ACTIVE.")
            return

        print(f"Waiting for stream '{name}' to become ACTIVE. Current: {status}")
        time.sleep(5)

    raise TimeoutError(f"Timed out waiting for stream '{name}' to become ACTIVE.")


def describe_stream(name: str) -> dict[str, Any]:
    """
    Return stream summary dict and print formatted stream details.
    """
    client = get_client()

    response = client.describe_stream_summary(StreamName=name)
    summary = response["StreamDescriptionSummary"]

    shard_count = summary.get("OpenShardCount")

    if shard_count is None:
        stream_response = client.describe_stream(StreamName=name)
        shard_count = len(stream_response["StreamDescription"]["Shards"])

    print(f"Stream:     {summary['StreamName']}")
    print(f"Status:     {summary['StreamStatus']}")
    print(f"Shards:     {shard_count}")
    print(f"Retention:  {summary['RetentionPeriodHours']} hours")
    print(f"Encryption: {summary.get('EncryptionType', 'NONE')}")

    return summary


def calculate_required_shards(
    write_mb_per_sec: float,
    write_records_per_sec: int,
    read_mb_per_sec: float,
) -> int:
    """
    Kinesis capacity math:
      Write limits per shard: 1 MB/s AND 1000 records/s
      Read limit per shard:   2 MB/s shared across all consumers
    """
    if write_mb_per_sec < 0:
        raise ValueError("write_mb_per_sec must be >= 0.")
    if write_records_per_sec < 0:
        raise ValueError("write_records_per_sec must be >= 0.")
    if read_mb_per_sec < 0:
        raise ValueError("read_mb_per_sec must be >= 0.")

    shards_for_write_mb = math.ceil(write_mb_per_sec)
    shards_for_write_records = math.ceil(write_records_per_sec / 1000)
    shards_for_write = max(shards_for_write_mb, shards_for_write_records)
    shards_for_read = math.ceil(read_mb_per_sec / 2)

    required = max(shards_for_write, shards_for_read)

    bottlenecks: list[str] = []
    if required == shards_for_write_mb:
        bottlenecks.append("write MB/s")
    if required == shards_for_write_records:
        bottlenecks.append("write records/s")
    if required == shards_for_read:
        bottlenecks.append("read MB/s")

    print("Shard capacity breakdown:")
    print(f"  Write MB/s needed      : {write_mb_per_sec} MB/s")
    print(f"  Shards for write MB/s  : {shards_for_write_mb}")
    print(f"  Write records needed   : {write_records_per_sec} records/s")
    print(f"  Shards for records/s   : {shards_for_write_records}")
    print(f"  Read MB/s needed       : {read_mb_per_sec} MB/s")
    print(f"  Shards for read MB/s   : {shards_for_read}")
    print(f"  Required shards        : {required}")
    print(f"  Bottleneck             : {', '.join(bottlenecks)}")

    return required


def update_retention(name: str, hours: int) -> None:
    """
    Extend retention beyond 24h default.

    Valid range: 24–8760 hours.
    WHY:
      Extended retention can cost extra, especially beyond 7 days.
    """
    if hours < 24 or hours > 8760:
        raise ValueError("Retention must be between 24 and 8760 hours.")

    client = get_client()
    before = describe_stream(name)["RetentionPeriodHours"]

    if hours == before:
        print(f"Retention already set to {hours} hours. No update needed.")
        return

    if hours > before:
        client.increase_stream_retention_period(
            StreamName=name,
            RetentionPeriodHours=hours,
        )
    else:
        client.decrease_stream_retention_period(
            StreamName=name,
            RetentionPeriodHours=hours,
        )

    print(f"Retention updated: {before} hours → {hours} hours")


def cleanup(stream_name: str) -> None:
    """
    Delete stream. Catch already-deleted errors silently.
    """
    client = get_client()

    try:
        client.delete_stream(
            StreamName=stream_name,
            EnforceConsumerDeletion=True,
        )
        print(f"Deleted stream '{stream_name}'.")
    except ClientError as exc:
        code = exc.response.get("Error", {}).get("Code", "")
        if code in {"ResourceNotFoundException", "ResourceInUseException"}:
            pass
        else:
            raise
    finally:
        print("✅ Cleanup complete. No ongoing charges.")


def main() -> None:
    resources: dict[str, str | None] = {"stream": None}

    try:
        print("\n=== CREATE STREAM ===")
        create_stream(STREAM_NAME, shard_count=1)
        resources["stream"] = STREAM_NAME

        print("\n=== DESCRIBE STREAM ===")
        describe_stream(STREAM_NAME)

        print("\n=== CAPACITY MATH ===")
        n = calculate_required_shards(
            write_mb_per_sec=5,
            write_records_per_sec=800,
            read_mb_per_sec=8,
        )
        print(f"Required shards for scenario: {n}")

        print("\n=== UPDATE RETENTION ===")
        update_retention(STREAM_NAME, hours=48)

    finally:
        if resources["stream"]:
            cleanup(resources["stream"])


if __name__ == "__main__":
    main()