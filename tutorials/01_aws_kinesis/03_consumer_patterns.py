# ============================================================
# Topic   : AWS Kinesis
# File    : 03_consumer_patterns.py
# Covers  : Shard iterators, polling consumers, iterator age, and stream consumption
# Prereqs : pip install boto3 | AWS credentials configured
# Run     : python 03_consumer_patterns.py
# ============================================================

"""
Environment variables:
  AWS_REGION          — default "us-east-1"
  AWS_PROFILE         — default "study"
  KINESIS_STREAM_NAME — default "studybook-kinesis-{uuid4 first 8 chars}"
  SNS_TOPIC_ARN       — optional, unused in this file
"""

import json
import os
import random
import time
import uuid
from datetime import datetime, timedelta, timezone
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


def get_cloudwatch_client() -> Any:
    """Return boto3 CloudWatch client using AWS_PROFILE session."""
    try:
        session = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
        return session.client("cloudwatch")
    except ProfileNotFound as exc:
        raise RuntimeError(
            f"AWS profile '{AWS_PROFILE}' was not found. "
            "Set AWS_PROFILE or configure the profile with aws configure."
        ) from exc


def wait_for_stream_active(client: Any, stream: str, timeout_s: int = 120) -> None:
    """Poll stream status until ACTIVE."""
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


def get_shard_iterator(
    client: Any,
    stream: str,
    shard_id: str,
    iterator_type: str = "TRIM_HORIZON",
    sequence_number: str | None = None,
) -> str:
    """
    Get shard iterator.

    Iterator type options:
      TRIM_HORIZON           — from beginning of retention window
      LATEST                 — only new records from now
      AT_SEQUENCE_NUMBER     — start at specific sequence
      AFTER_SEQUENCE_NUMBER  — start after sequence, useful for checkpointing

    WHY TRIM_HORIZON for tutorials:
      Reads everything already in the stream.

    WHY LATEST for production:
      Avoids reprocessing on consumer restart.
    """
    valid_types = {
        "TRIM_HORIZON",
        "LATEST",
        "AT_SEQUENCE_NUMBER",
        "AFTER_SEQUENCE_NUMBER",
    }

    if iterator_type not in valid_types:
        raise ValueError(f"iterator_type must be one of {sorted(valid_types)}")

    kwargs: dict[str, Any] = {
        "StreamName": stream,
        "ShardId": shard_id,
        "ShardIteratorType": iterator_type,
    }

    if iterator_type in {"AT_SEQUENCE_NUMBER", "AFTER_SEQUENCE_NUMBER"}:
        if not sequence_number:
            raise ValueError(f"{iterator_type} requires sequence_number.")
        kwargs["StartingSequenceNumber"] = sequence_number

    response = client.get_shard_iterator(**kwargs)
    return response["ShardIterator"]


def read_shard(
    client: Any,
    stream: str,
    shard_id: str,
    max_records: int = 100,
    shard_iterator: str | None = None,
) -> tuple[list[dict[str, Any]], str | None, int]:
    """
    Single polling loop iteration.

    Calls GetRecords with current iterator, decodes JSON payloads,
    and returns:
      (decoded_records, next_shard_iterator, iterator_age_ms)

    WHY iterator age:
      GetRecords.IteratorAgeMilliseconds is the key consumer lag metric.
      0ms = consumer is caught up.
      High ms = consumer is falling behind.
    """
    if shard_iterator is None:
        shard_iterator = get_shard_iterator(
            client=client,
            stream=stream,
            shard_id=shard_id,
            iterator_type="TRIM_HORIZON",
        )

    response = client.get_records(
        ShardIterator=shard_iterator,
        Limit=max_records,
    )

    decoded_records: list[dict[str, Any]] = []

    for record in response.get("Records", []):
        raw = record["Data"]

        if isinstance(raw, bytes):
            payload = raw.decode("utf-8")
        else:
            payload = raw.read().decode("utf-8")

        decoded_records.append(json.loads(payload))

    next_iterator = response.get("NextShardIterator")
    iterator_age_ms = int(response.get("MillisBehindLatest", 0))

    print(
        f"Read {len(decoded_records)} records from shard {shard_id}  "
        f"IteratorAgeMs={iterator_age_ms}"
    )

    return decoded_records, next_iterator, iterator_age_ms


def get_all_shards(client: Any, stream: str) -> list[str]:
    """
    List all shard IDs for the stream.

    Handles pagination via NextToken.

    WHY:
      Fan-out consumers read all shards in parallel, commonly one worker/thread per shard.
    """
    shard_ids: list[str] = []

    response = client.list_shards(StreamName=stream)

    while True:
        for shard in response.get("Shards", []):
            shard_ids.append(shard["ShardId"])

        next_token = response.get("NextToken")
        if not next_token:
            break

        response = client.list_shards(NextToken=next_token)

    return shard_ids


def check_iterator_age(client: Any, stream: str) -> dict[str, Any]:
    """
    Get GetRecords.IteratorAgeMilliseconds from CloudWatch.

    Uses last 5 minutes, Maximum statistic.

    Returns:
      {
        stream,
        max_iterator_age_ms,
        status
      }

    Status:
      OK       < 60,000 ms
      WARNING  < 300,000 ms
      CRITICAL >= 300,000 ms
      NO_DATA  no CloudWatch datapoints yet
    """
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=5)

    response = client.get_metric_statistics(
        Namespace="AWS/Kinesis",
        MetricName="GetRecords.IteratorAgeMilliseconds",
        Dimensions=[{"Name": "StreamName", "Value": stream}],
        StartTime=start_time,
        EndTime=end_time,
        Period=60,
        Statistics=["Maximum"],
    )

    datapoints = response.get("Datapoints", [])

    if not datapoints:
        return {
            "stream": stream,
            "max_iterator_age_ms": None,
            "status": "NO_DATA",
        }

    max_age = max(float(point["Maximum"]) for point in datapoints)

    if max_age < 60_000:
        status = "OK"
    elif max_age < 300_000:
        status = "WARNING"
    else:
        status = "CRITICAL"

    return {
        "stream": stream,
        "max_iterator_age_ms": max_age,
        "status": status,
    }


def consume_stream(
    client: Any,
    stream: str,
    from_beginning: bool = True,
    max_rounds: int = 3,
) -> list[dict[str, Any]]:
    """
    Complete consumer:
      1. Get all shards
      2. Create one iterator per shard
      3. Read max_rounds times from each shard

    Returns all collected decoded records.
    """
    iterator_type = "TRIM_HORIZON" if from_beginning else "LATEST"
    shard_ids = get_all_shards(client, stream)

    if not shard_ids:
        print(f"No shards found for stream '{stream}'.")
        return []

    iterators: dict[str, str | None] = {
        shard_id: get_shard_iterator(
            client=client,
            stream=stream,
            shard_id=shard_id,
            iterator_type=iterator_type,
        )
        for shard_id in shard_ids
    }

    all_records: list[dict[str, Any]] = []

    for round_num in range(1, max_rounds + 1):
        print(f"\nConsumer round {round_num}/{max_rounds}")

        round_records = 0
        max_age = 0

        for shard_id in shard_ids:
            iterator = iterators[shard_id]

            if iterator is None:
                print(f"Shard {shard_id} has no active iterator.")
                continue

            records, next_iterator, age_ms = read_shard(
                client=client,
                stream=stream,
                shard_id=shard_id,
                max_records=100,
                shard_iterator=iterator,
            )

            iterators[shard_id] = next_iterator
            all_records.extend(records)
            round_records += len(records)
            max_age = max(max_age, age_ms)

        print(
            f"Round {round_num}: records_read={round_records}, "
            f"max_iterator_age_ms={max_age}"
        )

        time.sleep(1)

    return all_records


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

        wait_for_stream_active(client, STREAM_NAME)

        print("\n=== SEED RECORDS ===")
        for i in range(20):
            payload = {
                "id": i,
                "val": round(random.random(), 4),
                "ts": time.time(),
            }

            client.put_record(
                StreamName=STREAM_NAME,
                Data=json.dumps(payload).encode("utf-8"),
                PartitionKey=f"key-{i % 4}",
            )

        print("Seeded 20 records.")

        print("\n=== LIST SHARDS ===")
        shard_ids = get_all_shards(client, STREAM_NAME)
        print(f"Shards: {shard_ids}")

        print("\n=== CONSUME STREAM ===")
        records = consume_stream(
            client=client,
            stream=STREAM_NAME,
            from_beginning=True,
            max_rounds=2,
        )
        print(f"Total records consumed: {len(records)}")

        print("\n=== CLOUDWATCH ITERATOR AGE CHECK ===")
        cloudwatch = get_cloudwatch_client()
        lag = check_iterator_age(cloudwatch, STREAM_NAME)
        print(lag)

    finally:
        if resources["stream"]:
            cleanup(resources["stream"])


if __name__ == "__main__":
    main()