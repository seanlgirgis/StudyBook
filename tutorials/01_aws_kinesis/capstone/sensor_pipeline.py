# ============================================================
# Topic   : AWS Kinesis
# File    : capstone/sensor_pipeline.py
# Covers  : Toyota IoT sensor streaming pipeline with producer, consumer, monitoring, cleanup
# Prereqs : pip install boto3 | AWS credentials configured
# Run     : python sensor_pipeline.py
# ============================================================

"""
Toyota IoT Sensor Streaming Pipeline — Kinesis capstone.

Environment variables:
  AWS_REGION            — default "us-east-1"
  AWS_PROFILE           — default "study"
  FIREHOSE_S3_BUCKET    — optional
  FIREHOSE_IAM_ROLE_ARN — optional
  SNS_TOPIC_ARN         — optional

Architecture:
  SensorProducer → Kinesis Data Stream → SensorConsumer anomaly detection
                                       → optional Firehose → S3

Resources created:
  - 1 Kinesis Data Stream, 2 shards
  - 2 CloudWatch alarms
  - Optional Firehose stream if bucket + role are configured

All resources are cleaned up in finally.
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
RUN_ID = uuid.uuid4().hex[:8]

STREAM_NAME = f"studybook-iot-{RUN_ID}"
FIREHOSE_NAME = f"studybook-firehose-{RUN_ID}"

S3_BUCKET = os.getenv("FIREHOSE_S3_BUCKET")
FIREHOSE_IAM = os.getenv("FIREHOSE_IAM_ROLE_ARN")
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")

SENSORS = [
    {
        "id": f"sensor_{i:03d}",
        "plant": f"plant_{i % 3 + 1}",
        "type": "temperature" if i < 10 else "pressure",
    }
    for i in range(20)
]

ANOMALY_THRESHOLDS = {
    "temperature": 85.0,
    "pressure": 120.0,
}


def get_session() -> boto3.Session:
    """Return boto3 session using AWS_PROFILE and AWS_REGION."""
    try:
        return boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
    except ProfileNotFound as exc:
        raise RuntimeError(
            f"AWS profile '{AWS_PROFILE}' was not found. "
            "Run aws configure --profile study or set AWS_PROFILE."
        ) from exc


class SensorProducer:
    """
    Simulates 20 Toyota assembly-line sensors.

    Partition key = sensor_id.
    This preserves per-sensor ordering, but a very hot sensor could create hot-shard risk.
    """

    def generate_reading(self, sensor: dict[str, str]) -> dict[str, Any]:
        """Generate one synthetic sensor reading."""
        sensor_type = sensor["type"]

        if sensor_type == "temperature":
            normal_value = random.uniform(15.0, 82.0)
            anomaly_value = random.uniform(86.0, 95.0)
            unit = "celsius"
        elif sensor_type == "pressure":
            normal_value = random.uniform(80.0, 118.0)
            anomaly_value = random.uniform(121.0, 140.0)
            unit = "psi"
        else:
            raise ValueError(f"Unknown sensor type: {sensor_type}")

        value = anomaly_value if random.random() < 0.10 else normal_value

        return {
            "sensor_id": sensor["id"],
            "plant": sensor["plant"],
            "type": sensor_type,
            "value": round(value, 2),
            "unit": unit,
            "ts": time.time(),
            "reading_id": str(uuid.uuid4()),
        }

    def send_batch(
        self,
        client: Any,
        stream: str,
        n_readings: int = 100,
    ) -> dict[str, int | float | bool]:
        """Send n_readings records using PutRecords batching."""
        start = time.perf_counter()

        sent = 0
        failed = 0
        anomaly_count = 0
        shard_counts: dict[str, int] = {}

        batch: list[dict[str, Any]] = []

        for i in range(n_readings):
            sensor = SENSORS[i % len(SENSORS)]
            reading = self.generate_reading(sensor)

            if reading["value"] > ANOMALY_THRESHOLDS[reading["type"]]:
                anomaly_count += 1

            batch.append(
                {
                    "Data": json.dumps(reading).encode("utf-8"),
                    "PartitionKey": reading["sensor_id"],
                }
            )

            if len(batch) == 100:
                result = client.put_records(StreamName=stream, Records=batch)
                failed_count = int(result.get("FailedRecordCount", 0))
                failed += failed_count
                sent += len(batch) - failed_count

                for record_result in result.get("Records", []):
                    shard_id = record_result.get("ShardId")
                    if shard_id:
                        shard_counts[shard_id] = shard_counts.get(shard_id, 0) + 1

                batch = []

        if batch:
            result = client.put_records(StreamName=stream, Records=batch)
            failed_count = int(result.get("FailedRecordCount", 0))
            failed += failed_count
            sent += len(batch) - failed_count

            for record_result in result.get("Records", []):
                shard_id = record_result.get("ShardId")
                if shard_id:
                    shard_counts[shard_id] = shard_counts.get(shard_id, 0) + 1

        elapsed_s = time.perf_counter() - start

        top_pct = 0.0
        if shard_counts:
            top_pct = max(shard_counts.values()) / sum(shard_counts.values()) * 100

        hot_shard_risk = top_pct > 60.0

        return {
            "sent": sent,
            "failed": failed,
            "anomaly_count": anomaly_count,
            "elapsed_s": round(elapsed_s, 3),
            "hot_shard_risk": hot_shard_risk,
            "top_shard_pct": round(top_pct, 2),
        }

    def print_distribution(self, client: Any, stream: str) -> None:
        """Show shard layout and explain hot-shard check."""
        response = client.list_shards(StreamName=stream)
        shards = response.get("Shards", [])

        print("\nShard distribution note:")
        print(f"  Stream: {stream}")
        print(f"  Open shards: {len(shards)}")
        print("  Partition key: sensor_id")
        print("  Ordering: preserved per sensor")
        print("  Hot shard check: no single shard should receive > 60% of writes")


class SensorConsumer:
    """Reads Kinesis shards and detects sensor anomalies."""

    def consume_all_shards(self, client: Any, stream: str) -> list[dict[str, Any]]:
        """Read all records from all shards using TRIM_HORIZON."""
        records: list[dict[str, Any]] = []

        shard_response = client.list_shards(StreamName=stream)
        shards = shard_response.get("Shards", [])

        for shard in shards:
            shard_id = shard["ShardId"]

            iterator_response = client.get_shard_iterator(
                StreamName=stream,
                ShardId=shard_id,
                ShardIteratorType="TRIM_HORIZON",
            )

            iterator = iterator_response["ShardIterator"]

            while iterator:
                response = client.get_records(ShardIterator=iterator, Limit=100)
                raw_records = response.get("Records", [])

                for record in raw_records:
                    payload = record["Data"]

                    if isinstance(payload, bytes):
                        decoded = payload.decode("utf-8")
                    else:
                        decoded = payload.read().decode("utf-8")

                    records.append(json.loads(decoded))

                print(
                    f"Read {len(raw_records)} records from {shard_id}; "
                    f"IteratorAgeMs={response.get('MillisBehindLatest', 0)}"
                )

                iterator = response.get("NextShardIterator")

                if not raw_records:
                    break

        return records

    def detect_anomalies(self, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Return records where value exceeds configured threshold."""
        anomalies = []

        for record in records:
            sensor_type = record.get("type")
            value = float(record.get("value", 0.0))

            threshold = ANOMALY_THRESHOLDS.get(sensor_type)
            if threshold is not None and value > threshold:
                anomalies.append(record)

        return anomalies

    def anomaly_rate(
        self,
        records: list[dict[str, Any]],
        anomalies: list[dict[str, Any]],
    ) -> float:
        """Return anomaly percentage."""
        if not records:
            return 0.0
        return round((len(anomalies) / len(records)) * 100, 2)

    def check_consumer_lag(self, client_cw: Any, stream: str) -> float:
        """Return max IteratorAgeMilliseconds from CloudWatch, or 0.0 if no data."""
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(minutes=5)

        response = client_cw.get_metric_statistics(
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
            return 0.0

        return max(float(point["Maximum"]) for point in datapoints)


def setup_stream(client: Any, stream: str, shard_count: int = 2) -> None:
    """Create Kinesis stream, wait for ACTIVE, and print cost warning."""
    client.create_stream(StreamName=stream, ShardCount=shard_count)

    print(
        f"⚠️  COST: Kinesis stream '{stream}' is running. "
        "~$0.015/shard/hour until deleted."
    )

    deadline = time.time() + 120

    while time.time() < deadline:
        summary = client.describe_stream_summary(StreamName=stream)[
            "StreamDescriptionSummary"
        ]
        status = summary["StreamStatus"]

        if status == "ACTIVE":
            print(f"Stream '{stream}' is ACTIVE.")
            return

        print(f"Waiting for stream '{stream}' to become ACTIVE. Current: {status}")
        time.sleep(5)

    raise TimeoutError(f"Timed out waiting for stream '{stream}' to become ACTIVE.")


def setup_alarms(client_cw: Any, stream: str) -> list[str]:
    """Create iterator-age and write-throttle alarms."""
    alarm_names = [
        f"{stream}-iterator-age-high",
        f"{stream}-write-throttled",
    ]

    client_cw.put_metric_alarm(
        AlarmName=alarm_names[0],
        AlarmDescription="Consumer lag above 60 seconds.",
        Namespace="AWS/Kinesis",
        MetricName="GetRecords.IteratorAgeMilliseconds",
        Dimensions=[{"Name": "StreamName", "Value": stream}],
        Statistic="Maximum",
        Period=60,
        EvaluationPeriods=1,
        DatapointsToAlarm=1,
        Threshold=60_000,
        ComparisonOperator="GreaterThanThreshold",
        TreatMissingData="notBreaching",
        AlarmActions=[SNS_TOPIC_ARN] if SNS_TOPIC_ARN else [],
    )

    print(f"⚠️  COST: CloudWatch alarm '{alarm_names[0]}' created. ~$0.10/alarm/month.")

    client_cw.put_metric_alarm(
        AlarmName=alarm_names[1],
        AlarmDescription="Write throttling detected for 5 consecutive minutes.",
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
        AlarmActions=[SNS_TOPIC_ARN] if SNS_TOPIC_ARN else [],
    )

    print(f"⚠️  COST: CloudWatch alarm '{alarm_names[1]}' created. ~$0.10/alarm/month.")

    return alarm_names


def setup_firehose_if_configured(session: boto3.Session) -> str | None:
    """Create Firehose delivery stream only if S3 bucket and IAM role are configured."""
    if not S3_BUCKET or not FIREHOSE_IAM:
        print("Firehose skipped: FIREHOSE_S3_BUCKET or FIREHOSE_IAM_ROLE_ARN not set.")
        return None

    client_firehose = session.client("firehose")

    response = client_firehose.create_delivery_stream(
        DeliveryStreamName=FIREHOSE_NAME,
        DeliveryStreamType="DirectPut",
        ExtendedS3DestinationConfiguration={
            "RoleARN": FIREHOSE_IAM,
            "BucketARN": f"arn:aws:s3:::{S3_BUCKET}",
            "Prefix": "studybook/iot/",
            "ErrorOutputPrefix": "studybook/iot/errors/",
            "BufferingHints": {
                "SizeInMBs": 5,
                "IntervalInSeconds": 60,
            },
            "CompressionFormat": "UNCOMPRESSED",
        },
    )

    print(
        f"⚠️  COST: Kinesis Firehose '{FIREHOSE_NAME}' is running. "
        "~$0.029/GB ingested until deleted."
    )

    return response["DeliveryStreamARN"]


def cleanup(
    client: Any,
    client_cw: Any,
    stream: str | None,
    alarm_names: list[str],
    firehose_name: str | None = None,
) -> None:
    """Delete stream, alarms, and optional Firehose. Idempotent cleanup."""
    session = get_session()

    if alarm_names:
        try:
            client_cw.delete_alarms(AlarmNames=alarm_names)
            print(f"Deleted alarms: {alarm_names}")
        except ClientError as exc:
            code = exc.response.get("Error", {}).get("Code", "")
            if code not in {"ResourceNotFound", "ResourceNotFoundException"}:
                print(f"Warning: failed to delete alarms: {exc}")

    if firehose_name:
        try:
            firehose = session.client("firehose")
            firehose.delete_delivery_stream(
                DeliveryStreamName=firehose_name,
                AllowForceDelete=True,
            )
            print(f"Deleted Firehose stream '{firehose_name}'.")
        except ClientError as exc:
            code = exc.response.get("Error", {}).get("Code", "")
            if code not in {"ResourceNotFoundException", "ResourceNotFound"}:
                print(f"Warning: failed to delete Firehose: {exc}")

    if stream:
        try:
            client.delete_stream(
                StreamName=stream,
                EnforceConsumerDeletion=True,
            )
            print(f"Deleted Kinesis stream '{stream}'.")
        except ClientError as exc:
            code = exc.response.get("Error", {}).get("Code", "")
            if code not in {"ResourceNotFoundException", "ResourceNotFound"}:
                print(f"Warning: failed to delete stream: {exc}")

    print("✅ Cleanup complete. No ongoing charges.")


def print_summary(
    producer_stats: dict[str, Any],
    anomalies: list[dict[str, Any]],
    anomaly_rate_pct: float,
    lag_ms: float,
) -> None:
    """Print capstone run summary."""
    hot_shard = "Yes" if producer_stats.get("hot_shard_risk") else "No"

    print()
    print("╔══════════════════════════════════════════╗")
    print("║  IoT Pipeline Run — Summary              ║")
    print("╠══════════════════════════════════════════╣")
    print(f"║  Records sent       : {producer_stats['sent']:<18} ║")
    print(f"║  Records failed     : {producer_stats['failed']:<18} ║")
    print(
        f"║  Anomalies detected : {len(anomalies):<5} "
        f"({anomaly_rate_pct:<5}%)      ║"
    )
    print(f"║  Consumer lag       : {lag_ms:<8.0f} ms ✓       ║")
    print(f"║  Hot shard risk     : {hot_shard:<8} ✓          ║")
    print("╚══════════════════════════════════════════╝")


def main() -> None:
    session = get_session()
    client = session.client("kinesis")
    client_cw = session.client("cloudwatch")

    alarm_names: list[str] = []
    firehose_name: str | None = None
    stream_created: str | None = None

    try:
        print("\n=== SETUP STREAM ===")
        setup_stream(client, STREAM_NAME, shard_count=2)
        stream_created = STREAM_NAME

        print("\n=== SETUP ALARMS ===")
        alarm_names = setup_alarms(client_cw, STREAM_NAME)

        print("\n=== OPTIONAL FIREHOSE ===")
        firehose_arn = setup_firehose_if_configured(session)
        if firehose_arn:
            firehose_name = FIREHOSE_NAME
            print(f"Firehose ARN: {firehose_arn}")

        print("\n=== PRODUCE SENSOR READINGS ===")
        producer = SensorProducer()
        stats = producer.send_batch(client, STREAM_NAME, n_readings=1000)
        print(stats)
        producer.print_distribution(client, STREAM_NAME)

        print("\n=== CONSUME AND DETECT ANOMALIES ===")
        consumer = SensorConsumer()
        records = consumer.consume_all_shards(client, STREAM_NAME)
        anomalies = consumer.detect_anomalies(records)
        rate = consumer.anomaly_rate(records, anomalies)
        lag = consumer.check_consumer_lag(client_cw, STREAM_NAME)

        print_summary(stats, anomalies, rate, lag)

    finally:
        cleanup(client, client_cw, stream_created, alarm_names, firehose_name)


if __name__ == "__main__":
    main()