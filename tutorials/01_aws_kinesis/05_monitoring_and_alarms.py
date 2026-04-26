# ============================================================
# Topic   : AWS Kinesis
# File    : 05_monitoring_and_alarms.py
# Covers  : CloudWatch metrics, iterator lag alarms, throttle alarms, and health reports
# Prereqs : pip install boto3 | AWS credentials configured
# Run     : python 05_monitoring_and_alarms.py
# ============================================================

"""
Environment variables:
  AWS_REGION          — default "us-east-1"
  AWS_PROFILE         — default "study"
  KINESIS_STREAM_NAME — default "studybook-kinesis-{uuid4 first 8 chars}"
  SNS_TOPIC_ARN       — optional, skip alarm actions if not set
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


def get_session() -> boto3.Session:
    """Return boto3 session using AWS_PROFILE and AWS_REGION."""
    try:
        return boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
    except ProfileNotFound as exc:
        raise RuntimeError(
            f"AWS profile '{AWS_PROFILE}' was not found. "
            "Set AWS_PROFILE or configure the profile with aws configure."
        ) from exc


def create_demo_stream(client_kinesis: Any, stream: str, shard_count: int = 1) -> None:
    """Create demo stream and wait until ACTIVE."""
    try:
        client_kinesis.create_stream(StreamName=stream, ShardCount=shard_count)
    except ClientError as exc:
        code = exc.response.get("Error", {}).get("Code", "")
        if code == "ResourceInUseException":
            raise RuntimeError(
                f"Stream '{stream}' already exists. Refusing to silently continue."
            ) from exc
        raise

    print(
        f"⚠️  COST: Kinesis stream '{stream}' is running. "
        "~$0.015/shard/hour until deleted."
    )

    deadline = time.time() + 120

    while time.time() < deadline:
        summary = client_kinesis.describe_stream_summary(StreamName=stream)[
            "StreamDescriptionSummary"
        ]
        status = summary["StreamStatus"]

        if status == "ACTIVE":
            print(f"Stream '{stream}' is ACTIVE.")
            return

        print(f"Waiting for stream '{stream}' to become ACTIVE. Current: {status}")
        time.sleep(5)

    raise TimeoutError(f"Timed out waiting for stream '{stream}' to become ACTIVE.")


def seed_records(client_kinesis: Any, stream: str, count: int = 50) -> None:
    """Put demo records into Kinesis so metrics and health report have activity."""
    records = []

    for i in range(count):
        payload = {
            "sensor_id": f"sensor_{i % 10:03d}",
            "temperature": round(random.uniform(20, 90), 2),
            "pressure": round(random.uniform(80, 140), 2),
            "ts": time.time(),
        }

        records.append(
            {
                "Data": json.dumps(payload).encode("utf-8"),
                "PartitionKey": payload["sensor_id"],
            }
        )

    response = client_kinesis.put_records(StreamName=stream, Records=records)
    failed = response.get("FailedRecordCount", 0)
    sent = count - failed

    print(f"Seeded records: sent={sent}, failed={failed}")


def consume_some_records(client_kinesis: Any, stream: str) -> None:
    """Read records once so IteratorAge-related consumer metrics can exist."""
    shard_response = client_kinesis.list_shards(StreamName=stream)
    shards = shard_response.get("Shards", [])

    total_read = 0

    for shard in shards:
        shard_id = shard["ShardId"]

        iterator_response = client_kinesis.get_shard_iterator(
            StreamName=stream,
            ShardId=shard_id,
            ShardIteratorType="TRIM_HORIZON",
        )

        records_response = client_kinesis.get_records(
            ShardIterator=iterator_response["ShardIterator"],
            Limit=100,
        )

        total_read += len(records_response.get("Records", []))
        age = records_response.get("MillisBehindLatest", 0)

        print(f"Read {len(records_response.get('Records', []))} records from {shard_id}; IteratorAgeMs={age}")

    print(f"Total records consumed for demo: {total_read}")


def get_latest_metric_value(
    client_cw: Any,
    stream: str,
    metric_name: str,
    minutes: int,
    statistic: str,
) -> float | None:
    """Fetch latest CloudWatch datapoint value for one Kinesis metric."""
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)

    response = client_cw.get_metric_statistics(
        Namespace="AWS/Kinesis",
        MetricName=metric_name,
        Dimensions=[{"Name": "StreamName", "Value": stream}],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=[statistic],
    )

    datapoints = response.get("Datapoints", [])
    if not datapoints:
        return None

    latest = max(datapoints, key=lambda p: p["Timestamp"])
    return float(latest.get(statistic, 0.0))


def get_stream_metrics(client_cw: Any, stream: str, minutes: int = 60) -> dict[str, float | None]:
    """Pull key CloudWatch metrics for the Kinesis stream."""
    metric_specs = {
        "GetRecords.IteratorAgeMilliseconds": "Maximum",
        "PutRecord.Success": "Sum",
        "PutRecords.Success": "Sum",
        "IncomingBytes": "Sum",
        "IncomingRecords": "Sum",
        "WriteProvisionedThroughputExceeded": "Sum",
        "ReadProvisionedThroughputExceeded": "Sum",
    }

    return {
        metric_name: get_latest_metric_value(
            client_cw=client_cw,
            stream=stream,
            metric_name=metric_name,
            minutes=minutes,
            statistic=statistic,
        )
        for metric_name, statistic in metric_specs.items()
    }


def create_iterator_age_alarm(
    client_cw: Any,
    stream: str,
    threshold_ms: int = 60_000,
    sns_topic_arn: str | None = None,
) -> str:
    """Create CloudWatch alarm on GetRecords.IteratorAgeMilliseconds."""
    alarm_name = f"{stream}-iterator-age-high"
    alarm_actions = [sns_topic_arn] if sns_topic_arn else []

    client_cw.put_metric_alarm(
        AlarmName=alarm_name,
        AlarmDescription="Kinesis consumer lag is high.",
        Namespace="AWS/Kinesis",
        MetricName="GetRecords.IteratorAgeMilliseconds",
        Dimensions=[{"Name": "StreamName", "Value": stream}],
        Statistic="Maximum",
        Period=60,
        EvaluationPeriods=1,
        DatapointsToAlarm=1,
        Threshold=threshold_ms,
        ComparisonOperator="GreaterThanThreshold",
        TreatMissingData="notBreaching",
        AlarmActions=alarm_actions,
    )

    print(f"⚠️  COST: CloudWatch alarm '{alarm_name}' created. ~$0.10/alarm/month.")
    return alarm_name


def create_throttle_alarm(
    client_cw: Any,
    stream: str,
    sns_topic_arn: str | None = None,
) -> str:
    """Create alarm on WriteProvisionedThroughputExceeded > 0 for 5 consecutive minutes."""
    alarm_name = f"{stream}-write-throttled"
    alarm_actions = [sns_topic_arn] if sns_topic_arn else []

    client_cw.put_metric_alarm(
        AlarmName=alarm_name,
        AlarmDescription="Kinesis write throttling detected.",
        Namespace="AWS/Kinesis",
        MetricName="WriteProvisionedThroughputExceeded",
        Dimensions=[{"Name": "StreamName", "Value": stream}],
        Statistic="Sum",
        Period=60,
        EvaluationPeriods=5,
        DatapointsToAlarm=5,
        Threshold=0,
        ComparisonOperator="GreaterThanThreshold",
        TreatMissingData="notBreaching",
        AlarmActions=alarm_actions,
    )

    print(f"⚠️  COST: CloudWatch alarm '{alarm_name}' created. ~$0.10/alarm/month.")
    return alarm_name


def get_stream_status_and_shards(client_kinesis: Any, stream: str) -> tuple[str, int]:
    """Return stream status and open shard count."""
    summary = client_kinesis.describe_stream_summary(StreamName=stream)[
        "StreamDescriptionSummary"
    ]

    status = summary["StreamStatus"]
    shard_count = summary.get("OpenShardCount")

    if shard_count is None:
        response = client_kinesis.describe_stream(StreamName=stream)
        shard_count = len(response["StreamDescription"].get("Shards", []))

    return status, int(shard_count)


def get_shard_utilization(
    client_cw: Any,
    client_kinesis: Any,
    stream: str,
) -> dict[str, Any]:
    """Estimate write/read capacity used."""
    _, shard_count = get_stream_status_and_shards(client_kinesis, stream)

    incoming_bytes = get_latest_metric_value(
        client_cw,
        stream,
        "IncomingBytes",
        minutes=15,
        statistic="Sum",
    )

    get_records_bytes = get_latest_metric_value(
        client_cw,
        stream,
        "GetRecords.Bytes",
        minutes=15,
        statistic="Sum",
    )

    write_capacity_bytes_per_min = 1 * 1024 * 1024 * shard_count * 60
    read_capacity_bytes_per_min = 2 * 1024 * 1024 * shard_count * 60

    write_util = ((incoming_bytes or 0.0) / write_capacity_bytes_per_min) * 100
    read_util = ((get_records_bytes or 0.0) / read_capacity_bytes_per_min) * 100

    if write_util < 70:
        status = "OK"
        symbol = "✓"
    elif write_util <= 90:
        status = "WARNING"
        symbol = "!"
    else:
        status = "CRITICAL"
        symbol = "✗"

    print(f"Write Util: ~{write_util:.2f}% {symbol} ({status})")
    print(f"Read Util:  ~{read_util:.2f}%")

    return {
        "stream": stream,
        "shard_count": shard_count,
        "estimated_write_util_pct": round(write_util, 2),
        "estimated_read_util_pct": round(read_util, 2),
        "status": status,
    }


def fmt_metric(value: float | None, suffix: str = "") -> str:
    """Format metric value for reports."""
    if value is None:
        return "NO_DATA"
    if suffix:
        return f"{value:,.0f} {suffix}"
    return f"{value:,.0f}"


def print_health_report(client_cw: Any, client_kinesis: Any, stream: str) -> None:
    """Print a complete Kinesis health summary."""
    status, shard_count = get_stream_status_and_shards(client_kinesis, stream)
    metrics = get_stream_metrics(client_cw, stream)
    util = get_shard_utilization(client_cw, client_kinesis, stream)

    iterator_age = metrics["GetRecords.IteratorAgeMilliseconds"]
    write_throttled = metrics["WriteProvisionedThroughputExceeded"]
    read_throttled = metrics["ReadProvisionedThroughputExceeded"]

    iterator_ok = iterator_age is None or iterator_age < 60_000
    write_ok = write_throttled is None or write_throttled == 0
    read_ok = read_throttled is None or read_throttled == 0
    write_util_ok = util["estimated_write_util_pct"] < 70

    print()
    print("╔══════════════════════════════════════════════╗")
    print(f"║  Kinesis Health Report: {stream[:20]:<20} ║")
    print("╠══════════════════════════════════════════════╣")
    print(f"║  Status:           {status:<18} ║")
    print(f"║  Shards:           {shard_count:<18} ║")
    print(
        f"║  Iterator Age:     {fmt_metric(iterator_age, 'ms'):<12} "
        f"{'✓' if iterator_ok else '✗':<5} ║"
    )
    print(
        f"║  Write Throttled:  {fmt_metric(write_throttled):<12} "
        f"{'✓' if write_ok else '✗':<5} ║"
    )
    print(
        f"║  Read Throttled:   {fmt_metric(read_throttled):<12} "
        f"{'✓' if read_ok else '✗':<5} ║"
    )
    print(
        f"║  Write Util:       ~{util['estimated_write_util_pct']:<10}% "
        f"{'✓' if write_util_ok else '!':<5} ║"
    )
    print("╚══════════════════════════════════════════════╝")


def cleanup(
    client_kinesis: Any,
    client_cw: Any,
    stream_name: str | None,
    alarm_names: list[str],
) -> None:
    """Delete CloudWatch alarms and Kinesis stream. Idempotent cleanup."""
    if alarm_names:
        try:
            client_cw.delete_alarms(AlarmNames=alarm_names)
            print(f"Deleted alarms: {alarm_names}")
        except ClientError as exc:
            code = exc.response.get("Error", {}).get("Code", "")
            if code not in {"ResourceNotFound", "ResourceNotFoundException"}:
                print(f"Warning: failed to delete alarms: {exc}")

    if stream_name:
        try:
            client_kinesis.delete_stream(
                StreamName=stream_name,
                EnforceConsumerDeletion=True,
            )
            print(f"Deleted stream '{stream_name}'.")
        except ClientError as exc:
            code = exc.response.get("Error", {}).get("Code", "")
            if code not in {"ResourceNotFoundException", "ResourceNotFound"}:
                print(f"Warning: failed to delete stream: {exc}")

    print("✅ Cleanup complete. No ongoing charges.")


def main() -> None:
    sns_arn = os.getenv("SNS_TOPIC_ARN")

    session = get_session()
    client_cw = session.client("cloudwatch")
    client_kin = session.client("kinesis")

    alarm_names: list[str] = []
    created_stream: str | None = None

    try:
        print("\n=== CREATE DEMO STREAM ===")
        create_demo_stream(client_kin, STREAM_NAME, shard_count=1)
        created_stream = STREAM_NAME

        print("\n=== SEED DEMO RECORDS ===")
        seed_records(client_kin, STREAM_NAME, count=50)

        print("\n=== CONSUME DEMO RECORDS ===")
        consume_some_records(client_kin, STREAM_NAME)

        print("\n=== STREAM METRICS ===")
        print("Note: CloudWatch metrics often take several minutes to appear.")
        metrics = get_stream_metrics(client_cw, STREAM_NAME)
        print(metrics)

        print("\n=== CREATE ALARMS ===")
        alarm_names.append(
            create_iterator_age_alarm(client_cw, STREAM_NAME, sns_topic_arn=sns_arn)
        )
        alarm_names.append(
            create_throttle_alarm(client_cw, STREAM_NAME, sns_topic_arn=sns_arn)
        )

        print("\n=== SHARD UTILIZATION ===")
        util = get_shard_utilization(client_cw, client_kin, STREAM_NAME)
        print(util)

        print("\n=== HEALTH REPORT ===")
        print_health_report(client_cw, client_kin, STREAM_NAME)

    finally:
        cleanup(client_kin, client_cw, created_stream, alarm_names)


if __name__ == "__main__":
    main()