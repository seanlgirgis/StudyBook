"""
Shared Kafka connection helper for all micro-nuggets.

Kafka is a local Docker service (no cloud credentials required).
Default broker: localhost:9092

Service contract from streaming.yml:
  - Kafka host listener:     localhost:9092   (PLAINTEXT_HOST)
  - Kafka internal listener: kafka:29092      (PLAINTEXT, Docker-internal only)
  - Container name:          citi_kafka

Usage in any nugget:
    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
    from _kafka_connect import get_producer, get_consumer, BROKER, LAB_TOPICS

    producer = get_producer()
    producer.send("my_topic", value=b"hello")
    producer.flush()
    producer.close()

    consumer = get_consumer("my_topic", group_id="my_group")
    for msg in consumer:
        print(msg.value)

Kafka concepts:
  - Producer sends records to topics.
  - Consumer reads records from topics within a consumer group.
  - KafkaAdminClient creates/deletes/describes topics.
  - No URI needed -- just host:port. No TLS for local Docker setup.
"""
from __future__ import annotations

import json
import os
import socket
import sys
import time
from pathlib import Path
from typing import Any, List, Optional

# UTF-8 stdout for Windows console
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ── Broker config ─────────────────────────────────────────────────────────────
_ENV_FILE = Path(r"D:\StudyBook\_infra\env\.env.local")


def _load_env_file(path: Path) -> dict:
    out: dict = {}
    if not path.exists():
        return out
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def _resolve_broker() -> str:
    env_val = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    if env_val:
        return env_val
    file_map = _load_env_file(_ENV_FILE)
    port = file_map.get("KAFKA_PORT", "9092")
    return f"localhost:{port}"


BROKER: str = _resolve_broker()


def safe_json_deserializer(payload: bytes | None) -> dict[str, Any]:
    """
    Deserialize Kafka message bytes to a dict without raising.
    Returns a diagnostic dict when payload is non-UTF8 or invalid JSON.
    """
    if payload is None:
        return {"_decode_error": "empty_payload"}
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        return {"_decode_error": "unicode_decode_error", "_detail": str(exc)}
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as exc:
        return {"_decode_error": "json_decode_error", "_detail": str(exc)}
    if isinstance(parsed, dict):
        return parsed
    return {"_decoded_non_object": True, "value": parsed}

# ── Lab topic registry ────────────────────────────────────────────────────────
# All nuggets share this topic list -- seed script creates them all.
LAB_TOPICS: dict[str, dict] = {
    "lab.raw.events":        {"num_partitions": 3, "replication_factor": 1},
    "lab.clean.events":      {"num_partitions": 3, "replication_factor": 1},
    "lab.agg.gold":          {"num_partitions": 1, "replication_factor": 1},
    "lab.reliability.test":  {"num_partitions": 2, "replication_factor": 1},
    "lab.dlq":               {"num_partitions": 1, "replication_factor": 1},
    "lab.orders":            {"num_partitions": 4, "replication_factor": 1},
    "lab.clickstream":       {"num_partitions": 3, "replication_factor": 1},
    "lab.bronze":            {"num_partitions": 3, "replication_factor": 1},
    "lab.silver":            {"num_partitions": 3, "replication_factor": 1},
    "lab.gold":              {"num_partitions": 1, "replication_factor": 1},
}


# ── TCP probe ─────────────────────────────────────────────────────────────────
def probe_broker(broker: str = BROKER, timeout_s: float = 5.0) -> bool:
    """Return True if the broker TCP port is reachable."""
    host, port_str = broker.rsplit(":", 1)
    port = int(port_str)
    try:
        with socket.create_connection((host, port), timeout=timeout_s):
            return True
    except OSError:
        return False


def require_broker(broker: str = BROKER) -> None:
    """Raise with actionable message if broker is unreachable."""
    if not probe_broker(broker):
        raise ConnectionError(
            f"\n[X] Kafka broker unreachable at {broker}\n\n"
            "Fix:\n"
            "  1. Start the streaming stack:\n"
            "       pwsh D:\\StudyBook\\_infra\\scripts\\infra_up.ps1 -Group streaming\n"
            "  2. Wait ~30 s for broker to fully start, then re-run.\n"
            "  3. Check health:\n"
            "       pwsh D:\\StudyBook\\_infra\\scripts\\infra_health.ps1\n"
            "  4. Confirm Kafka UI at http://localhost:8080\n"
        )


# ── Producer factory ──────────────────────────────────────────────────────────
def get_producer(broker: str = BROKER, **kwargs):
    """
    Return a KafkaProducer connected to the lab broker.

    Default settings:
      - value_serializer: raw bytes (callers JSON-encode before passing)
      - acks="all": wait for leader + all ISR replicas to acknowledge
      - retries=3: automatic retry on transient errors
      - linger_ms=5: small batching window for throughput
      - compression_type="gzip": reduce network bytes

    Callers must call producer.flush() then producer.close() when done.
    """
    from kafka import KafkaProducer  # type: ignore
    defaults = dict(
        bootstrap_servers=broker,
        acks="all",
        retries=3,
        linger_ms=5,
        compression_type="gzip",
        request_timeout_ms=15_000,
        **kwargs,
    )
    return KafkaProducer(**defaults)


# ── Consumer factory ──────────────────────────────────────────────────────────
def get_consumer(
    *topics: str,
    group_id: str = "lab_default_group",
    broker: str = BROKER,
    auto_offset_reset: str = "earliest",
    enable_auto_commit: bool = True,
    timeout_ms: int = 5_000,
    **kwargs,
):
    """
    Return a KafkaConsumer subscribed to one or more topics.

    auto_offset_reset="earliest": start from the beginning when no committed
      offset exists for this group -- important for lab reruns.

    Consumer groups:
      - All consumers sharing a group_id split partitions between them.
      - Each partition is owned by exactly one consumer in the group.
      - Use unique group_id per nugget to avoid offset interference.

    Callers must call consumer.close() when done.
    """
    from kafka import KafkaConsumer  # type: ignore
    defaults = dict(
        bootstrap_servers=broker,
        group_id=group_id,
        auto_offset_reset=auto_offset_reset,
        enable_auto_commit=enable_auto_commit,
        consumer_timeout_ms=timeout_ms,
        **kwargs,
    )
    return KafkaConsumer(*topics, **defaults)


# ── Admin client factory ───────────────────────────────────────────────────────
def get_admin(broker: str = BROKER):
    """Return a KafkaAdminClient for topic management."""
    from kafka import KafkaAdminClient  # type: ignore
    return KafkaAdminClient(
        bootstrap_servers=broker,
        request_timeout_ms=15_000,
    )


# ── Topic helpers ─────────────────────────────────────────────────────────────
def list_topics(broker: str = BROKER) -> List[str]:
    """Return sorted list of topics visible on the broker."""
    from kafka import KafkaConsumer  # type: ignore
    c = KafkaConsumer(bootstrap_servers=broker, consumer_timeout_ms=3_000)
    topics = sorted(c.topics())
    c.close()
    return topics


def ensure_topics(
    topic_specs: Optional[dict] = None,
    broker: str = BROKER,
) -> None:
    """
    Create topics that do not yet exist (idempotent).
    topic_specs: {name: {"num_partitions": N, "replication_factor": R}}
    Defaults to LAB_TOPICS if not provided.
    """
    from kafka import KafkaAdminClient  # type: ignore
    from kafka.admin import NewTopic  # type: ignore
    from kafka.errors import TopicAlreadyExistsError  # type: ignore

    if topic_specs is None:
        topic_specs = LAB_TOPICS

    admin = get_admin(broker)
    existing = set(list_topics(broker))
    to_create = [
        NewTopic(
            name=name,
            num_partitions=cfg["num_partitions"],
            replication_factor=cfg["replication_factor"],
        )
        for name, cfg in topic_specs.items()
        if name not in existing
    ]
    if to_create:
        try:
            admin.create_topics(to_create, validate_only=False)
        except TopicAlreadyExistsError:
            pass  # race condition with auto-create -- safe to ignore
    admin.close()
