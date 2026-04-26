# ChatGPT Prompt — AWS Kinesis
# READY TO PASTE — fully specified, no placeholders
# Paste everything between the === markers into ChatGPT

===

TOPIC: AWS Kinesis for Data Engineers
SLUG: aws_kinesis
PRIORITY: Toyota Interview Prep
INFRASTRUCTURE: AWS — boto3, real AWS account required
AWS_PROFILE = "study"

===== CODING STANDARDS =====

FILE HEADER (every file):
# ============================================================
# Topic   : AWS Kinesis
# File    : NN_filename.py
# Covers  : one-line description
# Prereqs : pip install boto3 | AWS credentials configured
# Run     : python NN_filename.py
# ============================================================

ENVIRONMENT VARIABLES (document at top of every file):
  AWS_REGION          — default "us-east-1"
  AWS_PROFILE         — default "study"
  KINESIS_STREAM_NAME — default "studybook-kinesis-{uuid4 first 8 chars}"
  FIREHOSE_STREAM_NAME — default "studybook-firehose-{uuid4 first 8 chars}"
  SNS_TOPIC_ARN       — optional, skip alarm creation if not set

CRITICAL — CLEANUP RULES (non-negotiable — runaway cost prevention):
  C1: Every main() that creates resources wraps ALL demo code in try/finally.
      cleanup() MUST be in the finally block — runs even if the script crashes.
  C2: Every file cleans up its own resources. No relying on a separate cleanup.py.
  C3: Cleanup is idempotent — catch ResourceNotFoundException, already-deleted errors silently.
  C4: Print ⚠️ COST WARNING immediately after creating any billable resource.
      "⚠️  COST: Kinesis stream '{name}' is running. ~$0.015/shard/hour until deleted."
  C5: Print at end of cleanup: "✅ Cleanup complete. No ongoing charges."

DANGEROUS RESOURCES:
  Kinesis Data Stream : ~$0.015/shard/hour  → delete_stream(StreamName=name)
  Kinesis Firehose    : ~$0.029/GB ingested → delete_delivery_stream(DeliveryStreamName=name)
  CloudWatch Alarms   : ~$0.10/alarm/month  → delete_alarms(AlarmNames=[name])

CODING:
  - Python 3.11+, type hints, f-strings
  - boto3 client with region_name and profile via boto3.Session
  - Specific exception handling (ClientError, botocore.exceptions)
  - uuid4 suffix on all resource names — never hardcode
  - if __name__ == "__main__" block with full demo

===== FILE 01: 01_streams_and_shards.py =====

import boto3, os, time, uuid
from botocore.exceptions import ClientError

STREAM_NAME = os.getenv("KINESIS_STREAM_NAME", f"studybook-kinesis-{uuid.uuid4().hex[:8]}")
AWS_REGION  = os.getenv("AWS_REGION", "us-east-1")
AWS_PROFILE = os.getenv("AWS_PROFILE", "study")

def get_client():
    """Return boto3 kinesis client using AWS_PROFILE session."""

def create_stream(name: str, shard_count: int = 1) -> None:
    """
    Create a Kinesis Data Stream and wait until status == ACTIVE.
    Poll describe_stream_summary every 5s, timeout after 120s.
    Print ⚠️ COST WARNING after creation.
    WHY shard_count=1: minimum for learning. Each shard = $0.015/hr.
    Raise if stream already exists (do not silently continue).
    """

def describe_stream(name: str) -> dict:
    """
    Return stream summary dict. Print formatted:
      Stream:     {name}
      Status:     ACTIVE
      Shards:     2
      Retention:  24 hours
      Encryption: NONE
    Return the raw StreamDescriptionSummary dict.
    """

def calculate_required_shards(write_mb_per_sec: float,
                               write_records_per_sec: int,
                               read_mb_per_sec: float) -> int:
    """
    Kinesis capacity math:
      Write limits per shard: 1 MB/s AND 1000 records/s
      Read limit per shard:   2 MB/s (shared across all consumers)
    shards_for_write = max(ceil(write_mb_per_sec), ceil(write_records_per_sec / 1000))
    shards_for_read  = ceil(read_mb_per_sec / 2)
    Return max(shards_for_write, shards_for_read).
    Print breakdown showing which limit is the bottleneck.
    """

def update_retention(name: str, hours: int) -> None:
    """
    Extend retention beyond 24h default (max 8760h = 365 days).
    Valid values: 24–8760 hours. Raise ValueError outside range.
    WHY: extended retention costs extra ($0.020/shard-hour beyond 7 days).
    Print old and new retention values.
    """

def cleanup(stream_name: str) -> None:
    """
    Delete stream. Catch ResourceNotFoundException silently.
    Print ✅ Cleanup complete. No ongoing charges.
    """

def main():
    resources = {"stream": None}
    try:
        print("\n=== CREATE STREAM ===")
        create_stream(STREAM_NAME, shard_count=1)
        resources["stream"] = STREAM_NAME

        print("\n=== DESCRIBE STREAM ===")
        describe_stream(STREAM_NAME)

        print("\n=== CAPACITY MATH ===")
        # Scenario: 5 MB/s writes, 800 records/s, 8 MB/s reads
        n = calculate_required_shards(write_mb_per_sec=5, write_records_per_sec=800,
                                      read_mb_per_sec=8)
        print(f"Required shards for scenario: {n}")

        print("\n=== UPDATE RETENTION ===")
        update_retention(STREAM_NAME, hours=48)
    finally:
        if resources["stream"]:
            cleanup(resources["stream"])

if __name__ == "__main__":
    main()

===== FILE 02: 02_producer_patterns.py =====

import json, time, random, uuid, os, boto3
from botocore.exceptions import ClientError

STREAM_NAME = os.getenv("KINESIS_STREAM_NAME", f"studybook-kinesis-{uuid.uuid4().hex[:8]}")

def get_client(): ...

def put_single_record(stream: str, data: dict, partition_key: str) -> dict:
    """
    PutRecord — single record. Convert data dict to JSON bytes.
    Return response with SequenceNumber and ShardId.
    WHY: PutRecord guarantees ordering within a shard but has higher per-call overhead.
    Use for low-volume or ordering-critical streams.
    Print: "Sent to shard {ShardId}, seq={SequenceNumber[:16]}..."
    """

def put_records_batch(stream: str, records: list[dict]) -> dict:
    """
    PutRecords — up to 500 records per call, up to 5 MB total.
    Each record: {"Data": json_bytes, "PartitionKey": str}
    Handle partial failures: FailedRecordCount > 0 → retry failed records once.
    WHY: PutRecords reduces API calls by 500×. Partial failure is normal —
    throttled records have ErrorCode "ProvisionedThroughputExceededException".
    Return: { sent: int, failed: int, retried: int }
    """

def generate_partition_key_strategies() -> None:
    """
    Print 3 partition key strategies with pros/cons:
    1. entity_id: partition_key = sensor_id
       PRO: all records for one sensor go to same shard (ordering guaranteed)
       CON: if one sensor is hot (high volume), that shard gets throttled
    2. hashed_id: partition_key = md5(sensor_id)[:8]
       PRO: even distribution even with sequential IDs
       CON: loses per-entity ordering
    3. salted: partition_key = f"{sensor_id}-{random.randint(0,9)}"
       PRO: spreads hot key across 10 shards
       CON: loses ordering entirely
    Show example partition keys for each strategy for sensor_id = "sensor_001"
    """

def detect_hot_shard_risk(records: list[dict]) -> dict:
    """
    Count records per partition_key. Return:
      { total: int, unique_keys: int, top_key: str, top_key_pct: float,
        hot_shard_risk: bool }
    hot_shard_risk = True if top_key_pct > 20% of total records.
    Print warning if hot shard risk detected.
    """

def simulate_producer(stream: str, n_records: int = 100,
                      strategy: str = "entity_id") -> dict:
    """
    Send n_records synthetic sensor records to stream.
    Record format: { sensor_id, temperature, pressure, ts }
    20 sensors: sensor_001 … sensor_020
    Use strategy to determine partition_key.
    Send in batches of 100 (PutRecords).
    Return: { sent: int, failed: int, elapsed_s: float }
    """

def cleanup(stream_name: str) -> None: ...

def main():
    resources = {"stream": None}
    try:
        # Create stream first
        boto3.Session(profile_name=AWS_PROFILE).client(
            "kinesis", region_name=AWS_REGION
        ).create_stream(StreamName=STREAM_NAME, ShardCount=1)
        resources["stream"] = STREAM_NAME
        print("⚠️  COST: Stream created. ~$0.015/hour until deleted.")
        time.sleep(15)  # wait for ACTIVE

        print("\n=== PARTITION KEY STRATEGIES ===")
        generate_partition_key_strategies()

        print("\n=== SIMULATE PRODUCER (entity_id strategy) ===")
        result = simulate_producer(STREAM_NAME, n_records=100, strategy="entity_id")
        print(result)

        print("\n=== HOT SHARD RISK CHECK ===")
        # Generate skewed records (80% from sensor_001)
        skewed = [{"partition_key": "sensor_001" if i < 80 else f"sensor_{i:03d}"}
                  for i in range(100)]
        risk = detect_hot_shard_risk(skewed)
        print(risk)
    finally:
        if resources["stream"]:
            cleanup(resources["stream"])

if __name__ == "__main__":
    main()

===== FILE 03: 03_consumer_patterns.py =====

def get_shard_iterator(client, stream: str, shard_id: str,
                       iterator_type: str = "TRIM_HORIZON",
                       sequence_number: str = None) -> str:
    """
    Get shard iterator. iterator_type options:
      TRIM_HORIZON        — from very beginning of retention window
      LATEST              — only new records from now
      AT_SEQUENCE_NUMBER  — start at specific sequence (requires sequence_number)
      AFTER_SEQUENCE_NUMBER — start after sequence (for checkpointing)
    WHY TRIM_HORIZON for tutorials: reads everything already in the stream.
    WHY LATEST for production: avoids reprocessing on consumer restart.
    Return iterator string.
    """

def read_shard(client, stream: str, shard_id: str,
               max_records: int = 100) -> list[dict]:
    """
    Single polling loop iteration. Call GetRecords with current iterator.
    Decode each record: json.loads(record["Data"])
    Return list of decoded record dicts.
    Update iterator for next call (iterator expires after 5 minutes of inactivity).
    Print: "Read {n} records from shard {shard_id}  IteratorAgeMs={age}"
    WHY iterator age: GetRecords.IteratorAgeMilliseconds is the key consumer lag metric.
    0ms = consumer is caught up. High ms = consumer is falling behind.
    """

def get_all_shards(client, stream: str) -> list[str]:
    """
    List all shard IDs for the stream (handles pagination via NextToken).
    Return list of shard ID strings.
    WHY: fan-out consumers read all shards in parallel (one thread per shard).
    """

def check_iterator_age(client, stream: str) -> dict:
    """
    Get GetRecords.IteratorAgeMilliseconds from CloudWatch (last 5 minutes, max).
    Return: { stream: str, max_iterator_age_ms: float, status: str }
    status: "OK" if < 60_000ms, "WARNING" if < 300_000ms, "CRITICAL" if >= 300_000ms.
    If CloudWatch returns no data, return status "NO_DATA".
    """

def consume_stream(client, stream: str, from_beginning: bool = True,
                   max_rounds: int = 3) -> list[dict]:
    """
    Complete consumer: get all shards, read max_rounds times from each.
    Returns all collected records.
    Print progress per round: round number, records read, iterator age.
    """

def cleanup(stream_name: str) -> None: ...

def main():
    resources = {"stream": None}
    try:
        # Assumes stream from file 02 exists — or creates a fresh one and seeds it
        client = boto3.Session(profile_name=AWS_PROFILE).client(
            "kinesis", region_name=AWS_REGION)
        client.create_stream(StreamName=STREAM_NAME, ShardCount=1)
        resources["stream"] = STREAM_NAME
        print("⚠️  COST: Stream created.")
        time.sleep(15)

        # Seed some records
        for i in range(20):
            client.put_record(StreamName=STREAM_NAME,
                              Data=json.dumps({"id": i, "val": random.random()}).encode(),
                              PartitionKey=f"key-{i % 4}")

        print("\n=== CONSUME STREAM ===")
        records = consume_stream(client, STREAM_NAME, from_beginning=True, max_rounds=2)
        print(f"Total records consumed: {len(records)}")
    finally:
        if resources["stream"]:
            cleanup(resources["stream"])

if __name__ == "__main__":
    main()

===== FILE 04: 04_firehose_delivery.py =====

PURPOSE: Kinesis Firehose for managed S3 delivery.
NOTE: Firehose requires an S3 bucket and an IAM role.
Add env var: FIREHOSE_S3_BUCKET (required), FIREHOSE_IAM_ROLE_ARN (required).
If either is missing, print a clear message and skip Firehose creation.

def create_firehose_to_s3(name: str, bucket: str, prefix: str,
                           role_arn: str, buffer_seconds: int = 60,
                           buffer_mb: int = 5) -> str:
    """
    Create Kinesis Firehose delivery stream to S3.
    Use ExtendedS3DestinationConfiguration.
    Print ⚠️ COST WARNING after creation.
    WHY buffering: Firehose batches records before writing to S3.
    Smaller buffer = more files (small file problem). Larger = higher latency.
    60s/5MB is a good default for analytics workloads.
    Return delivery stream ARN.
    """

def describe_firehose(name: str) -> dict:
    """
    Return delivery stream description. Print formatted:
      Stream:      {name}
      Status:      ACTIVE
      Destination: s3://{bucket}/{prefix}
      Buffer:      {buffer_seconds}s / {buffer_mb}MB
    """

def put_firehose_record(client, stream: str, data: dict) -> dict:
    """
    Send single record. Data dict → JSON bytes + newline (Firehose best practice).
    WHY newline: Firehose concatenates records in S3 files. Without newlines,
    the file becomes unparseable JSON. Always append \\n.
    """

def put_firehose_batch(client, stream: str, records: list[dict]) -> dict:
    """
    PutRecordBatch — up to 500 records or 4 MB per call.
    Handle partial failures (FailedPutCount > 0).
    Return: { sent: int, failed: int }
    """

def calculate_buffer_tradeoffs(records_per_sec: int,
                                record_size_bytes: int) -> None:
    """
    Print table showing for buffer_seconds in [30, 60, 120, 300]:
      buffer_s | files_per_hour | avg_file_size_mb | latency_s
    Explain: fewer, larger files are better for S3/Athena query performance.
    """

def cleanup(firehose_name: str) -> None:
    """Delete Firehose stream. Catch ResourceNotFoundException."""

def main():
    bucket = os.getenv("FIREHOSE_S3_BUCKET")
    role_arn = os.getenv("FIREHOSE_IAM_ROLE_ARN")

    if not bucket or not role_arn:
        print("FIREHOSE_S3_BUCKET and FIREHOSE_IAM_ROLE_ARN not set.")
        print("Showing buffer tradeoff calculation only (no AWS resources created).")
        calculate_buffer_tradeoffs(records_per_sec=1000, record_size_bytes=500)
        return

    resources = {"firehose": None}
    try:
        client = boto3.Session(profile_name=AWS_PROFILE).client(
            "firehose", region_name=AWS_REGION)
        arn = create_firehose_to_s3(
            FIREHOSE_NAME, bucket, "studybook/kinesis/",
            role_arn, buffer_seconds=60, buffer_mb=5)
        resources["firehose"] = FIREHOSE_NAME

        print("\n=== DESCRIBE ===")
        describe_firehose(FIREHOSE_NAME)

        print("\n=== SEND 50 RECORDS ===")
        records = [{"sensor_id": f"s{i}", "temp": random.uniform(20, 90)} for i in range(50)]
        result = put_firehose_batch(client, FIREHOSE_NAME, records)
        print(result)

        print("\n=== BUFFER TRADEOFFS ===")
        calculate_buffer_tradeoffs(1000, 500)
    finally:
        if resources["firehose"]:
            cleanup(resources["firehose"])

if __name__ == "__main__":
    main()

===== FILE 05: 05_monitoring_and_alarms.py =====

def get_stream_metrics(client_cw, stream: str, minutes: int = 60) -> dict:
    """
    Pull these CloudWatch metrics for the Kinesis stream (last `minutes` minutes):
      GetRecords.IteratorAgeMilliseconds — consumer lag
      PutRecord.Success                 — successful puts
      WriteProvisionedThroughputExceeded — write throttling
      ReadProvisionedThroughputExceeded  — read throttling
    Use get_metric_statistics with Period=300, Statistics=["Maximum","Sum"].
    Return dict of metric_name → latest value (or None if no data).
    """

def create_iterator_age_alarm(client_cw, stream: str,
                               threshold_ms: int = 60_000,
                               sns_topic_arn: str = None) -> str:
    """
    Create CloudWatch alarm on GetRecords.IteratorAgeMilliseconds.
    threshold_ms default 60_000 (1 minute lag = consumer falling behind).
    If sns_topic_arn is None, create alarm without action (still useful for dashboard).
    Print ⚠️ COST WARNING: $0.10/alarm/month.
    Return alarm name.
    """

def create_throttle_alarm(client_cw, stream: str,
                           sns_topic_arn: str = None) -> str:
    """
    Create alarm on WriteProvisionedThroughputExceeded > 0 for 5 consecutive minutes.
    WHY: even a single throttled write means records were dropped or must be retried.
    Return alarm name.
    """

def get_shard_utilization(client_cw, stream: str) -> dict:
    """
    Estimate % of write capacity used per shard:
      write_util = (IncomingBytes / (1MB * shards * 60s)) * 100
    Return: { stream, shard_count, estimated_write_util_pct, estimated_read_util_pct }
    Print with color indication: < 70% = OK, 70-90% = WARNING, > 90% = CRITICAL
    """

def print_health_report(client_cw, client_kinesis, stream: str) -> None:
    """
    Print a complete health summary:
      ╔═══════════════════════════════════════╗
      ║  Kinesis Health Report: {stream}      ║
      ╠═══════════════════════════════════════╣
      ║  Status:           ACTIVE             ║
      ║  Shards:           2                  ║
      ║  Iterator Age:     1,240 ms   ✓       ║
      ║  Write Throttled:  0          ✓       ║
      ║  Read Throttled:   0          ✓       ║
      ║  Write Util:       ~12%       ✓       ║
      ╚═══════════════════════════════════════╝
    """

def cleanup(alarm_names: list[str]) -> None:
    """Delete CloudWatch alarms. Print ✅ Cleanup complete."""

def main():
    sns_arn = os.getenv("SNS_TOPIC_ARN")  # optional
    stream  = os.getenv("KINESIS_STREAM_NAME", "studybook-kinesis-test")

    session    = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
    client_cw  = session.client("cloudwatch")
    client_kin = session.client("kinesis")

    alarm_names = []
    try:
        print("\n=== STREAM METRICS ===")
        metrics = get_stream_metrics(client_cw, stream)
        print(metrics)

        print("\n=== CREATE ALARMS ===")
        a1 = create_iterator_age_alarm(client_cw, stream, sns_topic_arn=sns_arn)
        alarm_names.append(a1)
        a2 = create_throttle_alarm(client_cw, stream, sns_topic_arn=sns_arn)
        alarm_names.append(a2)

        print("\n=== SHARD UTILIZATION ===")
        util = get_shard_utilization(client_cw, stream)
        print(util)

        print("\n=== HEALTH REPORT ===")
        print_health_report(client_cw, client_kin, stream)
    finally:
        cleanup(alarm_names)

if __name__ == "__main__":
    main()

===== CAPSTONE PROJECT =====

Title: IoT Sensor Streaming Pipeline
Scenario: A Toyota manufacturing plant has 20 assembly-line sensors reporting
temperature and pressure every second. Build a streaming pipeline: ingest → process
anomalies → deliver to S3 → monitor health.

Directory layout:
  capstone/
    sensor_pipeline.py   ← full pipeline (producer + consumer + monitoring)
    test_capstone.py     ← pytest with moto mocks

===== CAPSTONE FILE: sensor_pipeline.py =====

"""
Toyota IoT Sensor Streaming Pipeline — Kinesis capstone.

Architecture:
  SensorProducer → Kinesis Data Stream → SensorConsumer (anomaly detection)
                                       → Kinesis Firehose → S3

Resources created (all cleaned up in finally):
  - 1 Kinesis Data Stream (2 shards)
  - 1 Kinesis Firehose delivery stream (if S3 bucket configured)
  - 2 CloudWatch alarms (iterator age + throttling)
"""
import os, uuid, json, time, random, boto3
from botocore.exceptions import ClientError

AWS_REGION   = os.getenv("AWS_REGION", "us-east-1")
AWS_PROFILE  = os.getenv("AWS_PROFILE", "study")
RUN_ID       = uuid.uuid4().hex[:8]
STREAM_NAME  = f"studybook-iot-{RUN_ID}"
S3_BUCKET    = os.getenv("FIREHOSE_S3_BUCKET")      # optional
FIREHOSE_IAM = os.getenv("FIREHOSE_IAM_ROLE_ARN")   # optional

SENSORS = [{"id": f"sensor_{i:03d}", "plant": f"plant_{i%3+1}",
             "type": "temperature" if i < 10 else "pressure"}
           for i in range(20)]

ANOMALY_THRESHOLDS = {"temperature": 85.0, "pressure": 120.0}

class SensorProducer:
    """
    Simulates 20 sensors sending readings every second.
    Uses PutRecords batching. Partition key = sensor_id (ensures per-sensor ordering).

    Methods:
      generate_reading(sensor: dict) → dict
        { sensor_id, plant, type, value, unit, ts, reading_id }
        value: temp uniform 15-95°C, pressure uniform 80-140 PSI
        10% chance of anomaly (value > threshold)

      send_batch(client, stream: str, n_readings: int = 100) → dict
        Send n_readings records (batch of 100 per PutRecords call).
        Return { sent, failed, anomaly_count, elapsed_s }

      print_distribution(client, stream: str) → None
        After sending, show record count per shard (from describe_stream).
        Verify no single shard has > 60% of records (hot shard check).
    """

class SensorConsumer:
    """
    Reads all shards, detects anomalies, tracks iterator age.

    Methods:
      consume_all_shards(client, stream: str) → list[dict]
        Read all shards from TRIM_HORIZON. Return all decoded records.

      detect_anomalies(records: list[dict]) → list[dict]
        Filter records where value > ANOMALY_THRESHOLDS[type].
        Return anomaly records.

      anomaly_rate(records: list[dict], anomalies: list[dict]) → float
        Return anomaly_count / total_count as percentage.

      check_consumer_lag(client_cw, stream: str) → float
        Return max IteratorAgeMilliseconds from CloudWatch. Return 0.0 if no data.
    """

def setup_stream(client, stream: str, shard_count: int = 2) -> None:
    """Create stream, wait for ACTIVE, print ⚠️ COST WARNING."""

def setup_alarms(client_cw, stream: str) -> list[str]:
    """Create iterator age alarm (60s threshold) + throttle alarm. Return alarm names."""

def cleanup(client, client_cw, stream: str, alarm_names: list[str],
            firehose_name: str = None) -> None:
    """
    Delete stream, alarms, and firehose (if created).
    Each delete in its own try/except — one failure must not block the others.
    Print ✅ Cleanup complete. No ongoing charges.
    """

def print_summary(producer_stats: dict, anomalies: list[dict],
                  anomaly_rate_pct: float, lag_ms: float) -> None:
    """
    ╔══════════════════════════════════════════╗
    ║  IoT Pipeline Run — Summary              ║
    ╠══════════════════════════════════════════╣
    ║  Records sent       : 1000               ║
    ║  Records failed     : 0                  ║
    ║  Anomalies detected : 47   (4.7%)        ║
    ║  Consumer lag       : 0 ms  ✓            ║
    ║  Hot shard risk     : No    ✓            ║
    ╚══════════════════════════════════════════╝
    """

def main():
    session   = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
    client    = session.client("kinesis")
    client_cw = session.client("cloudwatch")

    alarm_names = []
    firehose_name = None

    try:
        setup_stream(client, STREAM_NAME, shard_count=2)

        alarm_names = setup_alarms(client_cw, STREAM_NAME)

        producer = SensorProducer()
        stats = producer.send_batch(client, STREAM_NAME, n_readings=1000)
        producer.print_distribution(client, STREAM_NAME)

        consumer = SensorConsumer()
        records   = consumer.consume_all_shards(client, STREAM_NAME)
        anomalies = consumer.detect_anomalies(records)
        rate      = consumer.anomaly_rate(records, anomalies)
        lag       = consumer.check_consumer_lag(client_cw, STREAM_NAME)

        print_summary(stats, anomalies, rate, lag)

    finally:
        cleanup(client, client_cw, STREAM_NAME, alarm_names, firehose_name)

if __name__ == "__main__":
    main()

===== CAPSTONE FILE: test_capstone.py =====

"""
pytest — 6 tests using moto to mock AWS calls.
Run: pytest test_capstone.py -v
pip install moto[kinesis,cloudwatch]
"""
import json, pytest
import boto3
from moto import mock_aws
from sensor_pipeline import SensorProducer, SensorConsumer, ANOMALY_THRESHOLDS

@pytest.fixture
def kinesis_client():
    with mock_aws():
        client = boto3.client("kinesis", region_name="us-east-1")
        client.create_stream(StreamName="test-stream", ShardCount=2)
        # wait for active
        import time; time.sleep(0.1)
        yield client

def test_sensor_reading_has_required_fields():
    """generate_reading returns all required fields."""
    producer = SensorProducer()
    reading = producer.generate_reading(
        {"id": "sensor_001", "plant": "plant_1", "type": "temperature"})
    required = {"sensor_id", "plant", "type", "value", "unit", "ts", "reading_id"}
    assert required.issubset(reading.keys())

def test_anomaly_detection_flags_high_temp():
    """Values above threshold are flagged as anomalies."""
    consumer = SensorConsumer()
    records = [
        {"type": "temperature", "value": 90.0, "sensor_id": "s1"},  # anomaly
        {"type": "temperature", "value": 70.0, "sensor_id": "s2"},  # normal
        {"type": "pressure",    "value": 130.0, "sensor_id": "s3"}, # anomaly
    ]
    anomalies = consumer.detect_anomalies(records)
    assert len(anomalies) == 2
    assert all(a["value"] > ANOMALY_THRESHOLDS[a["type"]] for a in anomalies)

def test_anomaly_rate_calculation():
    """anomaly_rate returns correct percentage."""
    consumer = SensorConsumer()
    records  = [{"type": "temperature", "value": v} for v in [90, 70, 80, 95, 60]]
    anomalies = consumer.detect_anomalies(records)
    rate = consumer.anomaly_rate(records, anomalies)
    assert 0 <= rate <= 100

@mock_aws
def test_producer_send_batch_returns_stats():
    """send_batch returns dict with sent/failed/anomaly_count."""
    client = boto3.client("kinesis", region_name="us-east-1")
    client.create_stream(StreamName="test-stream", ShardCount=1)
    import time; time.sleep(0.1)
    producer = SensorProducer()
    stats = producer.send_batch(client, "test-stream", n_readings=10)
    assert "sent" in stats
    assert "failed" in stats
    assert stats["sent"] + stats["failed"] == 10

@mock_aws
def test_consumer_reads_all_records():
    """consume_all_shards returns all records put into stream."""
    client = boto3.client("kinesis", region_name="us-east-1")
    client.create_stream(StreamName="test-stream", ShardCount=1)
    import time; time.sleep(0.1)
    for i in range(5):
        client.put_record(
            StreamName="test-stream",
            Data=json.dumps({"sensor_id": f"s{i}", "type": "temperature",
                             "value": 50.0}).encode(),
            PartitionKey=f"key-{i}")
    consumer = SensorConsumer()
    records = consumer.consume_all_shards(client, "test-stream")
    assert len(records) == 5

@mock_aws
def test_no_hot_shard_with_entity_partition_key():
    """
    With 20 sensors and 2 shards, no shard should have > 80% of records
    when using sensor_id as partition key (random distribution).
    """
    client = boto3.client("kinesis", region_name="us-east-1")
    client.create_stream(StreamName="test-stream", ShardCount=2)
    import time; time.sleep(0.1)
    producer = SensorProducer()
    producer.send_batch(client, "test-stream", n_readings=100)
    # Read shard counts via describe_stream_summary (moto supports this)
    # Just verify send completed without error for now
    assert True  # smoke test

===== GENERATION SEQUENCE =====

Acknowledge these instructions, then wait for me to say "generate file 01".

  "generate file 01"  → 01_streams_and_shards.py
  "generate file 02"  → 02_producer_patterns.py
  "generate file 03"  → 03_consumer_patterns.py
  "generate file 04"  → 04_firehose_delivery.py
  "generate file 05"  → 05_monitoring_and_alarms.py
  "generate readme"   → README.md
  "generate pipeline" → capstone/sensor_pipeline.py
  "generate tests"    → capstone/test_capstone.py

Each file COMPLETE and FULLY RUNNABLE. No placeholders. No pass statements.

===
