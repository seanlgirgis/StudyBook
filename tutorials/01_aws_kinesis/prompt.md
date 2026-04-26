# ChatGPT Prompt — AWS Kinesis Tutorial
# Paste everything between the === markers into ChatGPT

===

You are generating educational Python tutorial files for a Senior Data Engineer
personal study system. Each file must be production-quality, heavily commented,
and fully runnable.

TOPIC: AWS Kinesis
SLUG: aws-kinesis
PRIORITY: Toyota Interview Prep
INFRASTRUCTURE: AWS (boto3, real AWS account)

===== CODING STANDARDS =====

FILE HEADER — every file starts with:
# ============================================================
# Topic   : AWS Kinesis
# File    : NN_filename.py
# Covers  : one-line description
# Prereqs : pip install boto3 | AWS credentials configured
# Run     : python filename.py
# ============================================================

COMMENTS: Explain WHY, not WHAT. Every design decision gets a comment.
Numbers and limits get comments citing AWS docs (e.g. "1 MB/s per shard write limit").

DOCSTRINGS — every function must have:
- One-line summary
- WHY this approach (the senior insight)
- Args with types, Returns with type, Raises, one Example

CODE: Python 3.11+, type hints, os.environ for all config, f-strings,
specific exception handling, if __name__ == "__main__" block that demos everything.

ENVIRONMENT VARIABLES — document at top of each file:
# Required environment variables:
#   AWS_REGION           — e.g. us-east-1
#   AWS_PROFILE          — optional
#   KINESIS_STREAM_NAME  — target stream name

===== FILES TO GENERATE =====

Generate one file at a time. Wait for "next" before proceeding.

01_streams_and_shards.py
  Purpose: Understand Kinesis Data Streams fundamentals — create, describe, list, delete streams
  Key concepts: shards, partition keys, sequence numbers, retention, shard capacity math
  Functions:
    - create_stream(name, shard_count) — create and wait for ACTIVE status
    - describe_stream(name) — show shard count, retention, status
    - calculate_required_shards(write_mb_per_sec, write_records_per_sec, read_mb_per_sec) — capacity math
    - update_retention(name, hours) — extend beyond 24h default
    - delete_stream(name) — cleanup with confirmation
  Main block: create a 2-shard test stream, describe it, show capacity math for 5 MB/s scenario

02_producer_patterns.py
  Purpose: Write records to Kinesis — single record vs batch, partition key strategies, error handling
  Key concepts: PutRecord vs PutRecords, partial failure, partition key design, hot shards
  Functions:
    - put_single_record(stream, data, partition_key) — single put with sequence number returned
    - put_records_batch(stream, records) — PutRecords with partial failure handling
    - generate_partition_key_strategies() — show entity-id, hashed, salted strategies
    - detect_hot_shard_risk(records) — warn if one key dominates
    - simulate_producer(stream, n_records, strategy) — send n records with chosen strategy
  Main block: send 100 records with different partition key strategies, compare distribution

03_consumer_patterns.py
  Purpose: Read records from Kinesis — iterator types, polling loop, checkpointing
  Key concepts: iterator types (TRIM_HORIZON, LATEST, AT_SEQUENCE_NUMBER), polling, iterator age
  Functions:
    - get_shard_iterator(stream, shard_id, iterator_type, sequence_number=None)
    - read_shard(stream, shard_id, max_records=100) — polling loop with iterator refresh
    - get_all_shards(stream) — list shards for fan-out consumer
    - check_iterator_age(stream) — calculate consumer lag in seconds
    - consume_stream(stream, from_beginning=True) — complete consumer with lag monitoring
  Main block: consume from test stream, show records and iterator age metric

04_firehose_delivery.py
  Purpose: Kinesis Firehose for managed S3 delivery — create, configure buffering, send records
  Key concepts: delivery streams, buffering (time/size), format conversion to Parquet, S3 prefix
  Functions:
    - create_firehose_to_s3(name, bucket, prefix, buffer_seconds, buffer_mb)
    - describe_firehose(name) — show config, destination, buffering settings
    - put_firehose_record(stream, data) — single record delivery
    - put_firehose_batch(stream, records) — batch up to 500 records
    - calculate_buffer_tradeoffs(records_per_sec, record_size_bytes) — show latency vs file size
  Main block: show buffer tradeoff calculation, send 50 records, describe delivery stream

05_monitoring_and_alarms.py
  Purpose: Observe Kinesis health — key metrics, CloudWatch alarms, iterator age monitoring
  Key concepts: GetRecords.IteratorAgeMilliseconds, WriteProvisionedThroughputExceeded, alarms
  Functions:
    - get_stream_metrics(stream, minutes=60) — pull key CloudWatch metrics for the stream
    - create_iterator_age_alarm(stream, threshold_ms, sns_topic_arn) — alarm on consumer lag
    - create_throttle_alarm(stream, sns_topic_arn) — alarm on write throttling
    - get_shard_utilization(stream) — estimate % capacity used per shard
    - print_health_report(stream) — full health summary
  Main block: pull metrics for existing stream, show health report

===== CAPSTONE PROJECT =====

After all 5 files, generate:

capstone/brief.md
  Title: IoT Sensor Streaming Pipeline
  Scenario: A Toyota manufacturing plant has 20 assembly-line sensors reporting
    temperature and pressure readings every second. Build a streaming pipeline
    that ingests sensor data into Kinesis, processes records via Lambda logic
    (simulated in Python), delivers to S3 via Firehose, and monitors health.
  What to build:
    - SensorProducer class: simulates 20 sensors, sends to Kinesis with sensor_id as partition key
    - SensorConsumer class: reads from all shards, detects anomalies (temp > 85°C)
    - Delivery pipeline: Firehose stream delivering to S3 with 60s/5MB buffering
    - Health monitor: check iterator age, throttling, alert on anomaly rate > 5%
  Acceptance criteria:
    - 1000 sensor readings sent with even shard distribution (no hot shards)
    - Anomaly detection correctly flags readings where temp > 85 or pressure > 120
    - Iterator age stays under 5000ms during normal operation
    - Cleanup function removes all created resources
  Concepts used: PutRecords, partition key design, consumer polling, Firehose, CloudWatch metrics

capstone/capstone.py
  Complete working solution. Must be runnable. Include cleanup().

capstone/test_capstone.py
  pytest tests. Mock boto3 calls with moto or unittest.mock.
  Test: producer distributes records evenly, anomaly detection logic, cleanup called on error.

===== INFRASTRUCTURE NOTES =====

All AWS calls use boto3. Real AWS account with credentials configured.
Use os.environ.get("AWS_REGION", "us-east-1") for region.
When creating real resources (streams, Firehose), always include a cleanup() function.
Prefer us-east-1 as default region — cheapest for testing.
Kinesis stream costs ~$0.015/shard-hour — always delete test streams in cleanup.
CLEANUP RULES — MANDATORY:
- Every main() wraps demo code in try/finally — cleanup() is in the finally block
- Every file that creates a resource has its own cleanup() — do not rely on a separate file
- Cleanup functions catch "already deleted" errors and continue without crashing
- Print ⚠️ COST WARNING immediately after creating any billable resource
- Print ✅ Cleanup complete. No ongoing charges. at the end of every cleanup()
- capstone/cleanup.py deletes EVERYTHING and ends with that confirmation line

===== START =====

Acknowledge these instructions, then wait for me to say "generate file 01".

===
