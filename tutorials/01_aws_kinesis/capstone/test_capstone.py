# ============================================================
# Topic   : AWS Kinesis
# File    : capstone/test_capstone.py
# Covers  : pytest tests for Toyota IoT Kinesis capstone
# Prereqs : pip install pytest moto[kinesis,cloudwatch] boto3
# Run     : pytest test_capstone.py -v
# ============================================================

"""
pytest — tests using moto to mock AWS calls.

Run:
  cd capstone
  pytest test_capstone.py -v

Install:
  pip install pytest moto[kinesis,cloudwatch] boto3
"""

import json
import time

import boto3
import pytest
from moto import mock_aws

from sensor_pipeline import (
    ANOMALY_THRESHOLDS,
    SENSORS,
    SensorConsumer,
    SensorProducer,
    setup_stream,
    setup_alarms,
    cleanup,
)


@pytest.fixture
def kinesis_client():
    """Create mocked Kinesis client with a test stream."""
    with mock_aws():
        client = boto3.client("kinesis", region_name="us-east-1")
        client.create_stream(StreamName="test-stream", ShardCount=2)
        time.sleep(0.1)
        yield client


@pytest.fixture
def cloudwatch_client():
    """Create mocked CloudWatch client."""
    with mock_aws():
        yield boto3.client("cloudwatch", region_name="us-east-1")


def test_sensor_reading_has_required_fields():
    """generate_reading returns all required fields."""
    producer = SensorProducer()

    reading = producer.generate_reading(
        {
            "id": "sensor_001",
            "plant": "plant_1",
            "type": "temperature",
        }
    )

    required = {
        "sensor_id",
        "plant",
        "type",
        "value",
        "unit",
        "ts",
        "reading_id",
    }

    assert required.issubset(reading.keys())
    assert reading["sensor_id"] == "sensor_001"
    assert reading["plant"] == "plant_1"
    assert reading["type"] == "temperature"
    assert isinstance(reading["value"], float)
    assert reading["unit"] == "celsius"


def test_pressure_reading_has_psi_unit():
    """Pressure sensors should generate PSI readings."""
    producer = SensorProducer()

    reading = producer.generate_reading(
        {
            "id": "sensor_011",
            "plant": "plant_2",
            "type": "pressure",
        }
    )

    assert reading["type"] == "pressure"
    assert reading["unit"] == "psi"
    assert isinstance(reading["value"], float)


def test_anomaly_detection_flags_high_temp_and_pressure():
    """Values above thresholds are flagged as anomalies."""
    consumer = SensorConsumer()

    records = [
        {"type": "temperature", "value": 90.0, "sensor_id": "s1"},
        {"type": "temperature", "value": 70.0, "sensor_id": "s2"},
        {"type": "pressure", "value": 130.0, "sensor_id": "s3"},
        {"type": "pressure", "value": 100.0, "sensor_id": "s4"},
    ]

    anomalies = consumer.detect_anomalies(records)

    assert len(anomalies) == 2
    assert all(
        anomaly["value"] > ANOMALY_THRESHOLDS[anomaly["type"]]
        for anomaly in anomalies
    )


def test_anomaly_rate_calculation():
    """anomaly_rate returns correct percentage."""
    consumer = SensorConsumer()

    records = [
        {"type": "temperature", "value": 90.0},
        {"type": "temperature", "value": 70.0},
        {"type": "temperature", "value": 80.0},
        {"type": "temperature", "value": 95.0},
        {"type": "temperature", "value": 60.0},
    ]

    anomalies = consumer.detect_anomalies(records)
    rate = consumer.anomaly_rate(records, anomalies)

    assert rate == 40.0


def test_anomaly_rate_empty_records():
    """anomaly_rate should avoid divide-by-zero."""
    consumer = SensorConsumer()

    assert consumer.anomaly_rate([], []) == 0.0


@mock_aws
def test_producer_send_batch_returns_stats():
    """send_batch returns sent/failed/anomaly_count stats."""
    client = boto3.client("kinesis", region_name="us-east-1")
    client.create_stream(StreamName="test-stream", ShardCount=1)
    time.sleep(0.1)

    producer = SensorProducer()
    stats = producer.send_batch(client, "test-stream", n_readings=10)

    assert "sent" in stats
    assert "failed" in stats
    assert "anomaly_count" in stats
    assert "elapsed_s" in stats
    assert stats["sent"] + stats["failed"] == 10
    assert 0 <= stats["anomaly_count"] <= 10


@mock_aws
def test_consumer_reads_all_records():
    """consume_all_shards returns all records put into stream."""
    client = boto3.client("kinesis", region_name="us-east-1")
    client.create_stream(StreamName="test-stream", ShardCount=1)
    time.sleep(0.1)

    for i in range(5):
        client.put_record(
            StreamName="test-stream",
            Data=json.dumps(
                {
                    "sensor_id": f"s{i}",
                    "type": "temperature",
                    "value": 50.0,
                }
            ).encode("utf-8"),
            PartitionKey=f"key-{i}",
        )

    consumer = SensorConsumer()
    records = consumer.consume_all_shards(client, "test-stream")

    assert len(records) == 5
    assert all(record["type"] == "temperature" for record in records)


@mock_aws
def test_setup_stream_creates_active_stream():
    """setup_stream creates a Kinesis stream."""
    client = boto3.client("kinesis", region_name="us-east-1")

    setup_stream(client, "test-stream", shard_count=2)

    summary = client.describe_stream_summary(StreamName="test-stream")[
        "StreamDescriptionSummary"
    ]

    assert summary["StreamName"] == "test-stream"
    assert summary["StreamStatus"] in {"ACTIVE", "CREATING"}
    assert summary["OpenShardCount"] == 2


@mock_aws
def test_setup_alarms_creates_two_alarms():
    """setup_alarms creates iterator-age and throttle alarms."""
    client_cw = boto3.client("cloudwatch", region_name="us-east-1")

    alarm_names = setup_alarms(client_cw, "test-stream")

    response = client_cw.describe_alarms(AlarmNames=alarm_names)
    alarms = response["MetricAlarms"]

    assert len(alarm_names) == 2
    assert len(alarms) == 2
    assert any("iterator-age-high" in alarm["AlarmName"] for alarm in alarms)
    assert any("write-throttled" in alarm["AlarmName"] for alarm in alarms)


@mock_aws
def test_cleanup_removes_stream_and_alarms():
    """cleanup deletes both Kinesis stream and CloudWatch alarms."""
    client = boto3.client("kinesis", region_name="us-east-1")
    client_cw = boto3.client("cloudwatch", region_name="us-east-1")

    client.create_stream(StreamName="test-stream", ShardCount=1)
    time.sleep(0.1)

    alarm_names = setup_alarms(client_cw, "test-stream")

    cleanup(
        client=client,
        client_cw=client_cw,
        stream="test-stream",
        alarm_names=alarm_names,
        firehose_name=None,
    )

    alarms = client_cw.describe_alarms(AlarmNames=alarm_names)["MetricAlarms"]
    assert alarms == []


@mock_aws
def test_no_hot_shard_smoke_test_with_entity_partition_key():
    """
    With 20 sensors and 2 shards, send should complete without error.

    This is a smoke test because moto does not perfectly model real AWS shard
    hash distribution behavior.
    """
    client = boto3.client("kinesis", region_name="us-east-1")
    client.create_stream(StreamName="test-stream", ShardCount=2)
    time.sleep(0.1)

    producer = SensorProducer()
    stats = producer.send_batch(client, "test-stream", n_readings=100)

    assert stats["sent"] + stats["failed"] == 100
    assert isinstance(stats["hot_shard_risk"], bool)


def test_sensor_catalog_has_20_sensors():
    """Capstone should simulate exactly 20 sensors."""
    assert len(SENSORS) == 20

    sensor_ids = {sensor["id"] for sensor in SENSORS}

    assert len(sensor_ids) == 20
    assert "sensor_000" in sensor_ids
    assert "sensor_019" in sensor_ids