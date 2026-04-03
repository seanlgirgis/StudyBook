"""
Shared Spark Structured Streaming connection helper for all micro-nuggets.

Provides:
  - SparkSession builder with Kafka packages
  - Kafka broker configuration
  - Checkpoint and output path management
  - Topic creation via kafka-python

Usage in any nugget:
    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
    from _spark_stream_connect import get_spark, LAB_CHECKPOINT, LAB_OUTPUT

    spark = get_spark("my-nugget")
    ...
    spark.stop()
"""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

# ── Windows Hadoop workaround ─────────────────────────────────────────────────
# Spark on Windows needs winutils.exe for file operations. We work around this
# by setting spark.local.dir to a simple path and using file-based checkpoints.
if os.name == "nt" and not os.getenv("HADOOP_HOME"):
    # Point to PySpark's own bundled Hadoop (comes with pyspark package)
    pyspark_home = Path(__file__).parent.parent.parent.parent.parent / ".venv" / "Lib" / "site-packages" / "pyspark"
    if not pyspark_home.exists():
        # Try the canonical venv
        pyspark_home = Path(r"C:\py_venv\proj_educate\Lib\site-packages\pyspark")
    if pyspark_home.exists():
        os.environ["HADOOP_HOME"] = str(pyspark_home)

# ── Lab paths ─────────────────────────────────────────────────────────────────
LAB_BASE = Path(__file__).parent / "_lab"
LAB_CHECKPOINT = LAB_BASE / "checkpoint"
LAB_OUTPUT = LAB_BASE / "output"
LAB_DATA = LAB_BASE / "data"

# ── Kafka config ──────────────────────────────────────────────────────────────
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")

# Lab topics
TOPICS = {
    "raw_events": 3,
    "bronze_events": 3,
    "silver_orders": 3,
    "gold_metrics": 3,
    "lab_input": 1,
}


def ensure_lab_dirs():
    """Create lab directories idempotently."""
    for d in [LAB_CHECKPOINT, LAB_OUTPUT, LAB_DATA]:
        d.mkdir(parents=True, exist_ok=True)


def clean_lab():
    """Remove all lab data (checkpoints, outputs, seeded data)."""
    if LAB_BASE.exists():
        shutil.rmtree(LAB_BASE)
    ensure_lab_dirs()


def get_spark(app_name: str = "spark-streaming-lab", **kwargs):
    """
    Create a SparkSession configured for Structured Streaming with Kafka.

    Args:
        app_name: Spark application name
        **kwargs: Extra SparkConf key-value pairs

    Returns:
        pyspark.sql.SparkSession
    """
    try:
        from pyspark.sql import SparkSession
    except ImportError:
        raise EnvironmentError(
            "Missing dependency: pyspark\n"
            "Fix: pip install pyspark"
        )

    builder = (
        SparkSession.builder
        .appName(app_name)
        .master(os.getenv("SPARK_MASTER", "local[*]"))
        .config("spark.sql.shuffle.partitions", 4)
        .config("spark.sql.streaming.forceDeleteTempCheckpointLocation", True)
        .config("spark.local.dir", str(LAB_BASE / "spark_local"))
    )

    for key, value in kwargs.items():
        builder = builder.config(key, value)

    return builder.getOrCreate()


def create_kafka_topics():
    """
    Create required Kafka topics using kafka-python admin client.
    Idempotent — skips topics that already exist.
    """
    try:
        from kafka.admin import KafkaAdminClient, NewTopic
        from kafka.errors import TopicAlreadyExistsError
    except ImportError:
        raise EnvironmentError(
            "Missing dependency: kafka-python\n"
            "Fix: pip install kafka-python"
        )

    admin = KafkaAdminClient(bootstrap_servers=KAFKA_BOOTSTRAP)
    existing = set(admin.list_topics())

    to_create = []
    for name, partitions in TOPICS.items():
        if name not in existing:
            to_create.append(NewTopic(name=name, num_partitions=partitions, replication_factor=1))

    if to_create:
        try:
            admin.create_topics(to_create)
            return len(to_create)
        except Exception:
            # Some topics may have been created by another process
            return len(to_create)
    return 0


def produce_kafka_messages(topic: str, messages: list[bytes], key: Optional[bytes] = None):
    """
    Produce messages to a Kafka topic.

    Args:
        topic: Topic name
        messages: List of message payloads (bytes)
        key: Optional message key (applied to all messages)
    """
    try:
        from kafka import KafkaProducer
    except ImportError:
        raise EnvironmentError("pip install kafka-python")

    producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP)
    for msg in messages:
        producer.send(topic, value=msg, key=key)
    producer.flush()
    producer.close()


def check_kafka_broker(timeout: float = 5.0) -> bool:
    """Check if Kafka broker is reachable."""
    try:
        from kafka import KafkaConsumer
        consumer = KafkaConsumer(
            bootstrap_servers=KAFKA_BOOTSTRAP,
            consumer_timeout_ms=int(timeout * 1000),
        )
        consumer.close()
        return True
    except Exception:
        return False
