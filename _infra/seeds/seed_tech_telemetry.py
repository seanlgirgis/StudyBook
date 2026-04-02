"""
seed_tech_telemetry.py

Idempotent seed for StudyBook Technologies-style `public.*` tables.
These tables intentionally differ from `telemetry.*` to support simplified learning notebooks.

Usage:
  python _infra/seeds/seed_tech_telemetry.py
"""

from __future__ import annotations

import os
import random
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


def _ddl(cur) -> None:
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS public.endpoints (
            endpoint_id INTEGER PRIMARY KEY,
            name VARCHAR(80) NOT NULL,
            region VARCHAR(10) NOT NULL,
            status VARCHAR(20) NOT NULL,
            category VARCHAR(20) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS public.metrics (
            metric_id BIGSERIAL PRIMARY KEY,
            endpoint_id INTEGER NOT NULL REFERENCES public.endpoints(endpoint_id),
            metric_name VARCHAR(40) NOT NULL,
            value DOUBLE PRECISION NOT NULL,
            timestamp TIMESTAMPTZ NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_public_metrics_endpoint ON public.metrics(endpoint_id);
        CREATE INDEX IF NOT EXISTS idx_public_metrics_ts ON public.metrics(timestamp DESC);

        CREATE TABLE IF NOT EXISTS public.alerts (
            alert_id INTEGER PRIMARY KEY,
            endpoint_id INTEGER NOT NULL REFERENCES public.endpoints(endpoint_id),
            severity VARCHAR(10) NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMPTZ NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_public_alerts_endpoint ON public.alerts(endpoint_id);
        CREATE INDEX IF NOT EXISTS idx_public_alerts_severity ON public.alerts(severity);
        CREATE INDEX IF NOT EXISTS idx_public_alerts_created ON public.alerts(created_at DESC);
        """
    )


def _gen_endpoints(rng: random.Random, n: int):
    regions = ["NYC1", "SNG1", "LDN1", "TKY1", "SYD1"]
    statuses = ["active", "active", "active", "inactive", "degraded"]
    categories = ["web", "api", "grpc", "streaming", "batch"]
    rows = []
    for i in range(1, n + 1):
        rows.append((i, f"citi-api-{i:05d}.internal", rng.choice(regions), rng.choice(statuses), rng.choice(categories)))
    return rows


def _iter_metrics(rng: random.Random, now: datetime, endpoint_ids, n: int):
    metric_names = ["latency_ms", "error_rate", "throughput_rps", "cpu_percent", "memory_percent"]
    for _ in range(n):
        ep_id = rng.choice(endpoint_ids)
        metric_name = rng.choice(metric_names)
        if metric_name == "latency_ms":
            value = round(rng.uniform(5.0, 2000.0), 2)
        elif metric_name == "error_rate":
            value = round(rng.uniform(0.0, 0.25), 4)
        elif metric_name == "throughput_rps":
            value = round(rng.uniform(1.0, 5000.0), 1)
        else:
            value = round(rng.uniform(0.0, 100.0), 2)
        ts = now - timedelta(seconds=rng.randint(0, 30 * 86400))
        yield (ep_id, metric_name, value, ts)


def _iter_alerts(rng: random.Random, now: datetime, endpoint_ids, n: int):
    severities = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
    sev_weights = [0.05, 0.15, 0.35, 0.45]
    templates = {
        "CRITICAL": [
            "Service unavailable — connection timeout exceeded",
            "Error rate spike — circuit breaker triggered",
            "CPU saturation detected for endpoint",
        ],
        "HIGH": [
            "Latency P99 exceeded threshold",
            "Throughput drop detected",
            "Disk queue depth increasing",
        ],
        "MEDIUM": [
            "Latency elevated but within tolerance",
            "CPU trend increasing",
            "Connection pool near limit",
        ],
        "LOW": [
            "Scheduled maintenance window",
            "Config reload completed",
            "Certificate expiry warning",
        ],
    }

    for alert_id in range(1, n + 1):
        severity = rng.choices(severities, weights=sev_weights)[0]
        created = now - timedelta(seconds=rng.randint(0, 30 * 86400))
        message = rng.choice(templates[severity])
        yield (alert_id, rng.choice(endpoint_ids), severity, message, created)


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

    seed = _env_int("SEED_TECH", 42)
    n_endpoints = _env_int("SEED_ENDPOINTS", 10_000)
    n_metrics = _env_int("SEED_METRICS", 500_000)
    n_alerts = _env_int("SEED_ALERTS", 25_000)

    rng = random.Random(seed)
    now = datetime.now(timezone.utc)

    with _conn() as conn:
        with conn.cursor() as cur:
            _ddl(cur)
            conn.commit()

            cur.execute("SELECT COUNT(*) FROM public.endpoints")
            existing = cur.fetchone()[0]
            if existing >= n_endpoints:
                print(f"seed_tech_telemetry: already seeded ({existing:,} endpoints). Skipping.")
                return

            endpoint_rows = _gen_endpoints(rng, n_endpoints)
            psycopg2.extras.execute_batch(
                cur,
                "INSERT INTO public.endpoints VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING",
                endpoint_rows,
                page_size=1000,
            )
            conn.commit()

            endpoint_ids = [row[0] for row in endpoint_rows]

            metrics_inserted = _insert_batches(
                cur,
                "INSERT INTO public.metrics (endpoint_id, metric_name, value, timestamp) VALUES (%s,%s,%s,%s)",
                _iter_metrics(rng, now, endpoint_ids, n_metrics),
                chunk_size=5000,
            )
            conn.commit()

            alerts_inserted = _insert_batches(
                cur,
                "INSERT INTO public.alerts VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING",
                _iter_alerts(rng, now, endpoint_ids, n_alerts),
                chunk_size=3000,
            )
            conn.commit()

            cur.execute("SELECT COUNT(*) FROM public.endpoints")
            ep_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM public.metrics")
            m_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM public.alerts")
            a_count = cur.fetchone()[0]

    print("seed_tech_telemetry: complete")
    print(f"  endpoints: {ep_count:,}")
    print(f"  metrics:   {m_count:,} (insert attempted: {metrics_inserted:,})")
    print(f"  alerts:    {a_count:,} (insert attempted: {alerts_inserted:,})")


if __name__ == "__main__":
    main()