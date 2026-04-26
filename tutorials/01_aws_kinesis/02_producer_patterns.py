# ============================================================
# Topic   : AWS Kinesis
# File    : 02_producer_patterns.py
# Covers  : PutRecord, PutRecords batching, partition keys, and hot shard risk
# Prereqs : pip install boto3 | AWS credentials configured
# Run     : python 02_producer_patterns.py
# ============================================================

"""
Environment variables:
  AWS_REGION          — default "us-east-1"
  AWS_PROFILE         — default "study"
  KINESIS_STREAM_NAME — default "studybook-kinesis-{uuid4 first 8 chars}"
  SNS_TOPIC_ARN       — optional, unused in this file
"""

import hashlib
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


def wait_for_stream_active(stream: str, timeout_s: int = 120) -> None:
    """Poll stream status until ACTIVE."""
    client = get_client()
    deadline = time.time() + timeout_s

    while time.time() < deadline:
        response = client.describe_stream_summary(StreamName=stream)
        status = response["StreamDescriptionSummary"]["StreamStatus"]

        if status == "ACTIVE":
            print(f"Stream '{stream}' is ACTIVE.")
            return

        print(f"Waiting for stream '{stream}' to become ACTIVE. Current: {status}")
        time.sleep(5)

    raise TimeoutError(f"Timed out waiting for stream '{stream}' to become ACTIVE.")


def put_single_record(stream: str, data: dict[str, Any], partition_key: str) -> dict[str, Any]:
    """
    PutRecord — single record.

    WHY:
      PutRecord guarantees ordering within a shard but has higher per-call overhead.
      Use it for low-volume or ordering-critical streams.
    """
    client = get_client()

    response = client.put_record(
        StreamName=stream,
        Data=json.dumps(data).encode("utf-8"),
        PartitionKey=partition_key,
    )

    shard_id = response["ShardId"]
    sequence_number = response["SequenceNumber"]

    print(f"Sent to shard {shard_id}, seq={sequence_number[:16]}...")

    return response


def put_records_batch(stream: str, records: list[dict[str, Any]]) -> dict[str, int]:
    """
    PutRecords — up to 500 records per call, up to 5 MB total.

    Handles partial failures:
      FailedRecordCount > 0 means some records failed while others succeeded.
      This is normal under throttling. Failed records are retried once.
    """
    if not records:
        return {"sent": 0, "failed": 0, "retried": 0}

    if len(records) > 500:
        raise ValueError("PutRecords accepts at most 500 records per call.")

    client = get_client()

    entries = []
    for record in records:
        if "partition_key" not in record:
            raise ValueError("Each record must include 'partition_key'.")

        payload = {k: v for k, v in record.items() if k != "partition_key"}

        entries.append(
            {
                "Data": json.dumps(payload).encode("utf-8"),
                "PartitionKey": str(record["partition_key"]),
            }
        )

    response = client.put_records(StreamName=stream, Records=entries)
    failed_count = response.get("FailedRecordCount", 0)

    retried = 0
    retry_failed = 0

    if failed_count > 0:
        failed_entries = []

        for original_entry, result in zip(entries, response["Records"]):
            if "ErrorCode" in result:
                failed_entries.append(original_entry)

        print(f"Partial failure: {failed_count} records failed. Retrying once...")

        retry_response = client.put_records(StreamName=stream, Records=failed_entries)
        retry_failed = retry_response.get("FailedRecordCount", 0)
        retried = len(failed_entries)

    sent = len(records) - retry_failed
    failed = retry_failed

    return {"sent": sent, "failed": failed, "retried": retried}


def generate_partition_key_strategies() -> None:
    """
    Print 3 partition key strategies with pros/cons.
    """
    sensor_id = "sensor_001"
    hashed = hashlib.md5(sensor_id.encode("utf-8")).hexdigest()[:8]
    salted = f"{sensor_id}-{random.randint(0, 9)}"

    print("1. entity_id")
    print(f"   partition_key = sensor_id → {sensor_id}")
    print("   PRO: all records for one sensor go to same shard; ordering guaranteed")
    print("   CON: if one sensor is hot, that shard can get throttled")

    print("\n2. hashed_id")
    print(f"   partition_key = md5(sensor_id)[:8] → {hashed}")
    print("   PRO: even distribution even with sequential IDs")
    print("   CON: loses per-entity ordering")

    print("\n3. salted")
    print(f"   partition_key = f'{sensor_id}-{{0..9}}' → {salted}")
    print("   PRO: spreads a hot key across 10 logical keys")
    print("   CON: loses ordering entirely")


def detect_hot_shard_risk(records: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Count records per partition_key and flag hot shard risk.

    hot_shard_risk = True if the most frequent key is > 20% of total records.
    """
    total = len(records)

    if total == 0:
        return {
            "total": 0,
            "unique_keys": 0,
            "top_key": "",
            "top_key_pct": 0.0,
            "hot_shard_risk": False,
        }

    counts: dict[str, int] = {}

    for record in records:
        key = str(record.get("partition_key", ""))
        counts[key] = counts.get(key, 0) + 1

    top_key = max(counts, key=counts.get)
    top_count = counts[top_key]
    top_key_pct = (top_count / total) * 100
    hot_shard_risk = top_key_pct > 20

    if hot_shard_risk:
        print(
            f"⚠️  HOT SHARD RISK: partition key '{top_key}' is "
            f"{top_key_pct:.1f}% of records."
        )
    else:
        print(f"Hot shard risk: OK. Top key is {top_key_pct:.1f}% of records.")

    return {
        "total": total,
        "unique_keys": len(counts),
        "top_key": top_key,
        "top_key_pct": round(top_key_pct, 2),
        "hot_shard_risk": hot_shard_risk,
    }


def choose_partition_key(sensor_id: str, strategy: str) -> str:
    """Return partition key based on selected strategy."""
    if strategy == "entity_id":
        return sensor_id

    if strategy == "hashed_id":
        return hashlib.md5(sensor_id.encode("utf-8")).hexdigest()[:8]

    if strategy == "salted":
        return f"{sensor_id}-{random.randint(0, 9)}"

    raise ValueError("strategy must be one of: entity_id, hashed_id, salted")


def simulate_producer(
    stream: str,
    n_records: int = 100,
    strategy: str = "entity_id",
) -> dict[str, float | int]:
    """
    Send synthetic sensor records to Kinesis.

    Record format:
      { sensor_id, temperature, pressure, ts }

    Uses 20 sensors:
      sensor_001 … sensor_020
    """
    start = time.perf_counter()

    sent_total = 0
    failed_total = 0

    batch: list[dict[str, Any]] = []

    for i in range(n_records):
        sensor_num = (i % 20) + 1
        sensor_id = f"sensor_{sensor_num:03d}"
        partition_key = choose_partition_key(sensor_id, strategy)

        batch.append(
            {
                "sensor_id": sensor_id,
                "temperature": round(random.uniform(20.0, 90.0), 2),
                "pressure": round(random.uniform(80.0, 140.0), 2),
                "ts": time.time(),
                "partition_key": partition_key,
            }
        )

        if len(batch) == 100:
            result = put_records_batch(stream, batch)
            sent_total += result["sent"]
            failed_total += result["failed"]
            batch = []

    if batch:
        result = put_records_batch(stream, batch)
        sent_total += result["sent"]
        failed_total += result["failed"]

    elapsed_s = time.perf_counter() - start

    return {
        "sent": sent_total,
        "failed": failed_total,
        "elapsed_s": round(elapsed_s, 3),
    }


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
        client = get_client()

        client.create_stream(StreamName=STREAM_NAME, ShardCount=1)
        resources["stream"] = STREAM_NAME

        print(
            f"⚠️  COST: Kinesis stream '{STREAM_NAME}' is running. "
            "~$0.015/shard/hour until deleted."
        )

        wait_for_stream_active(STREAM_NAME)

        print("\n=== PUT SINGLE RECORD ===")
        single = {
            "sensor_id": "sensor_001",
            "temperature": 72.4,
            "pressure": 101.7,
            "ts": time.time(),
        }
        put_single_record(STREAM_NAME, single, partition_key="sensor_001")

        print("\n=== PARTITION KEY STRATEGIES ===")
        generate_partition_key_strategies()

        print("\n=== SIMULATE PRODUCER (entity_id strategy) ===")
        result = simulate_producer(STREAM_NAME, n_records=100, strategy="entity_id")
        print(result)

        print("\n=== HOT SHARD RISK CHECK ===")
        skewed = [
            {"partition_key": "sensor_001" if i < 80 else f"sensor_{i:03d}"}
            for i in range(100)
        ]
        risk = detect_hot_shard_risk(skewed)
        print(risk)

    finally:
        if resources["stream"]:
            cleanup(resources["stream"])


if __name__ == "__main__":
    main()