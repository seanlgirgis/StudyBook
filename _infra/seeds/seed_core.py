"""
seed_core.py

Idempotent seed for the StudyBook core telemetry schema (`telemetry.*`) in PostgreSQL.
Designed for reproducible local infra bootstrap with deterministic synthetic data.

Usage:
  python _infra/seeds/seed_core.py
"""

from __future__ import annotations

import os
import random
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

import psycopg2
import psycopg2.extras


def _load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        raw = line.strip()
        if not raw or raw.startswith("#") or "=" not in raw:
            continue
        key, value = raw.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def _load_env() -> None:
    infra_root = Path(__file__).resolve().parents[1]
    env_dir = infra_root / "env"
    _load_env_file(env_dir / ".env.example")
    _load_env_file(env_dir / ".env.local")


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default


def _conn():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=_env_int("POSTGRES_PORT", 5432),
        dbname=os.getenv("POSTGRES_DB", "de_telemetry"),
        user=os.getenv("POSTGRES_USER", "de_admin"),
        password=os.getenv("POSTGRES_PASSWORD", "change_me"),
        connect_timeout=10,
    )


def _create_tables(cur) -> None:
    cur.execute(
        """
        CREATE SCHEMA IF NOT EXISTS telemetry;

        CREATE TABLE IF NOT EXISTS telemetry.endpoints (
            endpoint_id UUID PRIMARY KEY,
            hostname TEXT NOT NULL,
            datacenter TEXT NOT NULL,
            environment TEXT NOT NULL,
            service_type TEXT NOT NULL,
            ip_address TEXT NOT NULL,
            os TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TIMESTAMPTZ NOT NULL
        );

        CREATE TABLE IF NOT EXISTS telemetry.metrics (
            metric_id UUID PRIMARY KEY,
            endpoint_id UUID NOT NULL REFERENCES telemetry.endpoints(endpoint_id),
            metric_name TEXT NOT NULL,
            value DOUBLE PRECISION NOT NULL,
            unit TEXT NOT NULL,
            recorded_at TIMESTAMPTZ NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_metrics_endpoint ON telemetry.metrics(endpoint_id);
        CREATE INDEX IF NOT EXISTS idx_metrics_recorded_at ON telemetry.metrics(recorded_at DESC);

        CREATE TABLE IF NOT EXISTS telemetry.alerts (
            alert_id UUID PRIMARY KEY,
            endpoint_id UUID NOT NULL REFERENCES telemetry.endpoints(endpoint_id),
            severity TEXT NOT NULL,
            message TEXT NOT NULL,
            category TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TIMESTAMPTZ NOT NULL,
            resolved_at TIMESTAMPTZ NULL
        );

        CREATE INDEX IF NOT EXISTS idx_alerts_endpoint ON telemetry.alerts(endpoint_id);
        CREATE INDEX IF NOT EXISTS idx_alerts_created_at ON telemetry.alerts(created_at DESC);

        CREATE TABLE IF NOT EXISTS telemetry.events (
            event_id UUID PRIMARY KEY,
            endpoint_id UUID NOT NULL REFERENCES telemetry.endpoints(endpoint_id),
            event_type TEXT NOT NULL,
            description TEXT NOT NULL,
            performed_by TEXT NOT NULL,
            created_at TIMESTAMPTZ NOT NULL
        );
        """
    )


def _build_endpoints(rng: random.Random, now: datetime, count: int):
    datacenters = ["NYC1", "NYC2", "LON1", "SNG1"]
    environments = ["prod", "staging", "dev"]
    service_types = ["web", "db", "cache", "worker", "monitor"]
    os_types = ["linux", "windows"]

    rows = []
    for i in range(count):
        endpoint_id = uuid.UUID(int=rng.getrandbits(128))
        rows.append(
            (
                str(endpoint_id),
                f"srv-{i + 1:05d}.studybook.internal",
                rng.choice(datacenters),
                rng.choice(environments),
                rng.choice(service_types),
                f"10.{rng.randint(0,255)}.{rng.randint(0,255)}.{rng.randint(1,254)}",
                rng.choice(os_types),
                rng.choices(["active", "inactive"], weights=[90, 10])[0],
                now - timedelta(days=rng.randint(0, 730)),
            )
        )
    return rows


def _iter_metrics(rng: random.Random, now: datetime, endpoint_ids, count: int):
    metric_names = ["cpu_percent", "memory_percent", "disk_io", "network_in", "network_out"]
    metric_units = {
        "cpu_percent": "percent",
        "memory_percent": "percent",
        "disk_io": "iops",
        "network_in": "mbps",
        "network_out": "mbps",
    }

    for _ in range(count):
        metric_name = rng.choice(metric_names)
        if metric_name in ("cpu_percent", "memory_percent"):
            value = round(rng.uniform(5.0, 99.9), 2)
        elif metric_name == "disk_io":
            value = round(rng.uniform(10.0, 5000.0), 2)
        else:
            value = round(rng.uniform(0.1, 1000.0), 2)

        yield (
            str(uuid.UUID(int=rng.getrandbits(128))),
            rng.choice(endpoint_ids),
            metric_name,
            value,
            metric_units[metric_name],
            now - timedelta(seconds=rng.randint(0, 90 * 24 * 3600)),
        )


def _iter_alerts(rng: random.Random, now: datetime, endpoint_ids, count: int):
    severities = ["critical", "high", "medium", "low"]
    categories = ["cpu", "memory", "disk", "network", "process"]
    statuses = ["open", "acknowledged", "resolved"]
    templates = [
        "CPU utilization exceeded threshold",
        "Memory usage spike detected",
        "Disk latency increased above SLA",
        "Network throughput dropped below baseline",
        "Process restart triggered by watchdog",
    ]

    for _ in range(count):
        created_at = now - timedelta(seconds=rng.randint(0, 90 * 24 * 3600))
        status = rng.choice(statuses)
        resolved_at = None
        if status == "resolved":
            resolved_at = created_at + timedelta(minutes=rng.randint(5, 480))

        yield (
            str(uuid.UUID(int=rng.getrandbits(128))),
            rng.choice(endpoint_ids),
            rng.choice(severities),
            rng.choice(templates),
            rng.choice(categories),
            status,
            created_at,
            resolved_at,
        )


def _iter_events(rng: random.Random, now: datetime, endpoint_ids, count: int):
    event_types = ["deploy", "restart", "config_change", "patch", "incident"]
    users = ["ops_bot", "de_admin", "svc_airflow", "svc_spark", "svc_monitor"]

    for _ in range(count):
        event_type = rng.choice(event_types)
        yield (
            str(uuid.UUID(int=rng.getrandbits(128))),
            rng.choice(endpoint_ids),
            event_type,
            f"{event_type} executed on endpoint",
            rng.choice(users),
            now - timedelta(seconds=rng.randint(0, 90 * 24 * 3600)),
        )


def _insert_batches(cur, sql: str, rows, chunk_size: int = 5000) -> int:
    total = 0
    batch = []
    for row in rows:
        batch.append(row)
        if len(batch) >= chunk_size:
            psycopg2.extras.execute_batch(cur, sql, batch, page_size=1000)
            total += len(batch)
            batch = []
    if batch:
        psycopg2.extras.execute_batch(cur, sql, batch, page_size=1000)
        total += len(batch)
    return total


def main() -> None:
    _load_env()

    seed = _env_int("SEED_CORE", 42)
    n_endpoints = _env_int("SEED_ENDPOINTS", 10_000)
    n_metrics = _env_int("SEED_METRICS", 500_000)
    n_alerts = _env_int("SEED_ALERTS", 25_000)
    n_events = _env_int("SEED_EVENTS", 50_000)

    rng = random.Random(seed)
    now = datetime.now(timezone.utc)

    with _conn() as conn:
        with conn.cursor() as cur:
            _create_tables(cur)
            conn.commit()

            cur.execute("SELECT COUNT(*) FROM telemetry.endpoints")
            existing = cur.fetchone()[0]
            if existing >= n_endpoints:
                print(f"seed_core: telemetry already seeded ({existing:,} endpoints). Skipping.")
                return

            endpoints = _build_endpoints(rng, now, n_endpoints)
            endpoint_ids = [row[0] for row in endpoints]

            psycopg2.extras.execute_batch(
                cur,
                """
                INSERT INTO telemetry.endpoints
                (endpoint_id, hostname, datacenter, environment, service_type, ip_address, os, status, created_at)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT DO NOTHING
                """,
                endpoints,
                page_size=1000,
            )
            conn.commit()

            metrics_inserted = _insert_batches(
                cur,
                """
                INSERT INTO telemetry.metrics
                (metric_id, endpoint_id, metric_name, value, unit, recorded_at)
                VALUES (%s,%s,%s,%s,%s,%s)
                ON CONFLICT DO NOTHING
                """,
                _iter_metrics(rng, now, endpoint_ids, n_metrics),
                chunk_size=5000,
            )
            conn.commit()

            alerts_inserted = _insert_batches(
                cur,
                """
                INSERT INTO telemetry.alerts
                (alert_id, endpoint_id, severity, message, category, status, created_at, resolved_at)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT DO NOTHING
                """,
                _iter_alerts(rng, now, endpoint_ids, n_alerts),
                chunk_size=3000,
            )
            conn.commit()

            events_inserted = _insert_batches(
                cur,
                """
                INSERT INTO telemetry.events
                (event_id, endpoint_id, event_type, description, performed_by, created_at)
                VALUES (%s,%s,%s,%s,%s,%s)
                ON CONFLICT DO NOTHING
                """,
                _iter_events(rng, now, endpoint_ids, n_events),
                chunk_size=3000,
            )
            conn.commit()

            cur.execute("SELECT COUNT(*) FROM telemetry.endpoints")
            ep_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM telemetry.metrics")
            m_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM telemetry.alerts")
            a_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM telemetry.events")
            e_count = cur.fetchone()[0]

    print("seed_core: complete")
    print(f"  endpoints: {ep_count:,}")
    print(f"  metrics:   {m_count:,} (insert attempted: {metrics_inserted:,})")
    print(f"  alerts:    {a_count:,} (insert attempted: {alerts_inserted:,})")
    print(f"  events:    {e_count:,} (insert attempted: {events_inserted:,})")


if __name__ == "__main__":
    main()