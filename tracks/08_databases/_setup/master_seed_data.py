"""
master_seed_data.py
-------------------
Generates and loads the Citi telemetry dataset into all 6 live databases.
Idempotent — safe to run multiple times (checks before inserting).

Dataset:
  endpoints  10,000 rows
  metrics   500,000 rows
  alerts     25,000 rows
  events     50,000 rows
"""

import os
import random
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

from dotenv import load_dotenv
from faker import Faker
from tqdm import tqdm

load_dotenv(Path(__file__).parent / "env", override=True)

fake = Faker()
random.seed(42)
Faker.seed(42)

NOW = datetime.now(timezone.utc)

# ── Lookup tables ──────────────────────────────────────────────────────────────
DATACENTERS   = ["NYC1", "NYC2", "LON1", "SNG1"]
ENVIRONMENTS  = ["prod", "staging", "dev"]
SERVICE_TYPES = ["web", "db", "cache", "worker", "monitor"]
OS_TYPES      = ["linux", "windows"]
METRIC_NAMES  = ["cpu_percent", "memory_percent", "disk_io", "network_in", "network_out"]
METRIC_UNITS  = {
    "cpu_percent":    "percent",
    "memory_percent": "percent",
    "disk_io":        "iops",
    "network_in":     "mbps",
    "network_out":    "mbps",
}
SEVERITIES    = ["critical", "high", "medium", "low"]
ALERT_CATS    = ["cpu", "memory", "disk", "network", "process"]
ALERT_STATUSES = ["open", "acknowledged", "resolved"]
EVENT_TYPES   = ["deploy", "restart", "config_change", "patch", "incident"]
ALERT_MESSAGES = [
    "CPU utilization exceeded 90% threshold for 5 minutes",
    "Memory usage at 95% — potential OOM imminent",
    "Disk I/O latency spike detected: 450ms avg",
    "Network throughput dropped below SLA threshold",
    "Process {proc} exited unexpectedly — restart triggered",
    "TCP connection pool exhausted on port 5432",
    "Health check failed: HTTP 503 from {host}",
    "Swap usage exceeded 80% on {host}",
    "Load average exceeded 4x CPU count",
    "SSL certificate expires in 7 days",
]


# ── Data generators ────────────────────────────────────────────────────────────
def gen_endpoints(n=10_000):
    endpoints = []
    for i in range(n):
        dc = random.choice(DATACENTERS)
        svc = random.choice(SERVICE_TYPES)
        endpoints.append({
            "endpoint_id": str(uuid.uuid4()),
            "hostname":    f"srv-{i+1:05d}.citi.internal",
            "datacenter":  dc,
            "environment": random.choice(ENVIRONMENTS),
            "service_type": svc,
            "ip_address":  fake.ipv4_private(),
            "os":          random.choice(OS_TYPES),
            "status":      random.choices(["active", "inactive"], weights=[90, 10])[0],
            "created_at":  NOW - timedelta(days=random.randint(0, 730)),
        })
    return endpoints


def gen_metrics(endpoints, n=500_000):
    ep_ids = [e["endpoint_id"] for e in endpoints]
    metrics = []
    for _ in range(n):
        mname = random.choice(METRIC_NAMES)
        if mname in ("cpu_percent", "memory_percent"):
            value = round(random.uniform(5.0, 99.9), 2)
        elif mname == "disk_io":
            value = round(random.uniform(10.0, 5000.0), 2)
        else:
            value = round(random.uniform(0.1, 1000.0), 2)
        metrics.append({
            "metric_id":   str(uuid.uuid4()),
            "endpoint_id": random.choice(ep_ids),
            "metric_name": mname,
            "value":       value,
            "unit":        METRIC_UNITS[mname],
            "recorded_at": NOW - timedelta(
                seconds=random.randint(0, 90 * 24 * 3600)
            ),
        })
    return metrics


def gen_alerts(endpoints, n=25_000):
    ep_ids = [e["endpoint_id"] for e in endpoints]
    alerts = []
    for _ in range(n):
        created = NOW - timedelta(seconds=random.randint(0, 90 * 24 * 3600))
        status = random.choice(ALERT_STATUSES)
        resolved_at = None
        if status == "resolved":
            resolved_at = created + timedelta(minutes=random.randint(5, 480))
        msg_tmpl = random.choice(ALERT_MESSAGES)
        message = msg_tmpl.format(
            proc=fake.user_name(),
            host=fake.hostname(),
        )
        alerts.append({
            "alert_id":    str(uuid.uuid4()),
            "endpoint_id": random.choice(ep_ids),
            "severity":    random.choice(SEVERITIES),
            "message":     message,
            "category":    random.choice(ALERT_CATS),
            "status":      status,
            "created_at":  created,
            "resolved_at": resolved_at,
        })
    return alerts


def gen_events(endpoints, n=50_000):
    ep_ids = [e["endpoint_id"] for e in endpoints]
    events = []
    for _ in range(n):
        events.append({
            "event_id":     str(uuid.uuid4()),
            "endpoint_id":  random.choice(ep_ids),
            "event_type":   random.choice(EVENT_TYPES),
            "description":  fake.sentence(nb_words=10),
            "performed_by": fake.user_name(),
            "created_at":   NOW - timedelta(
                seconds=random.randint(0, 90 * 24 * 3600)
            ),
        })
    return events


# ── PostgreSQL ─────────────────────────────────────────────────────────────────
def seed_postgres(endpoints, metrics, alerts, events):
    from db_connections import get_postgres_conn
    import psycopg2.extras

    print("\n[PostgreSQL] Seeding...")
    conn = get_postgres_conn()
    cur = conn.cursor()

    # Schema
    cur.execute("CREATE SCHEMA IF NOT EXISTS telemetry;")

    # Endpoints table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS telemetry.endpoints (
            endpoint_id  UUID PRIMARY KEY,
            hostname     TEXT NOT NULL,
            datacenter   TEXT,
            environment  TEXT,
            service_type TEXT,
            ip_address   TEXT,
            os           TEXT,
            status       TEXT,
            created_at   TIMESTAMPTZ
        );
    """)

    # Metrics table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS telemetry.metrics (
            metric_id    UUID PRIMARY KEY,
            endpoint_id  UUID REFERENCES telemetry.endpoints(endpoint_id),
            metric_name  TEXT,
            value        DOUBLE PRECISION,
            unit         TEXT,
            recorded_at  TIMESTAMPTZ
        );
    """)

    # Alerts table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS telemetry.alerts (
            alert_id     UUID PRIMARY KEY,
            endpoint_id  UUID REFERENCES telemetry.endpoints(endpoint_id),
            severity     TEXT,
            message      TEXT,
            category     TEXT,
            status       TEXT,
            created_at   TIMESTAMPTZ,
            resolved_at  TIMESTAMPTZ
        );
    """)

    # Events table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS telemetry.events (
            event_id     UUID PRIMARY KEY,
            endpoint_id  UUID REFERENCES telemetry.endpoints(endpoint_id),
            event_type   TEXT,
            description  TEXT,
            performed_by TEXT,
            created_at   TIMESTAMPTZ
        );
    """)
    conn.commit()

    # Check idempotency
    cur.execute("SELECT COUNT(*) FROM telemetry.endpoints;")
    existing = cur.fetchone()[0]
    if existing >= len(endpoints):
        print(f"  [PostgreSQL] Already seeded ({existing} endpoints). Skipping.")
        conn.close()
        return

    # Batch insert endpoints
    ep_rows = [(
        e["endpoint_id"], e["hostname"], e["datacenter"], e["environment"],
        e["service_type"], e["ip_address"], e["os"], e["status"], e["created_at"]
    ) for e in endpoints]
    psycopg2.extras.execute_batch(
        cur,
        """INSERT INTO telemetry.endpoints VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
           ON CONFLICT DO NOTHING""",
        ep_rows, page_size=1000
    )
    conn.commit()
    print(f"  endpoints: {len(endpoints):,}")

    # Metrics in chunks
    chunk = 5000
    for i in tqdm(range(0, len(metrics), chunk), desc="  metrics"):
        rows = [(
            m["metric_id"], m["endpoint_id"], m["metric_name"],
            m["value"], m["unit"], m["recorded_at"]
        ) for m in metrics[i:i+chunk]]
        psycopg2.extras.execute_batch(
            cur,
            """INSERT INTO telemetry.metrics VALUES (%s,%s,%s,%s,%s,%s)
               ON CONFLICT DO NOTHING""",
            rows, page_size=1000
        )
        conn.commit()
    print(f"  metrics: {len(metrics):,}")

    # Alerts
    al_rows = [(
        a["alert_id"], a["endpoint_id"], a["severity"], a["message"],
        a["category"], a["status"], a["created_at"], a["resolved_at"]
    ) for a in alerts]
    psycopg2.extras.execute_batch(
        cur,
        """INSERT INTO telemetry.alerts VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
           ON CONFLICT DO NOTHING""",
        al_rows, page_size=1000
    )
    conn.commit()
    print(f"  alerts: {len(alerts):,}")

    # Events
    ev_rows = [(
        e["event_id"], e["endpoint_id"], e["event_type"],
        e["description"], e["performed_by"], e["created_at"]
    ) for e in events]
    psycopg2.extras.execute_batch(
        cur,
        """INSERT INTO telemetry.events VALUES (%s,%s,%s,%s,%s,%s)
           ON CONFLICT DO NOTHING""",
        ev_rows, page_size=1000
    )
    conn.commit()
    print(f"  events: {len(events):,}")
    conn.close()
    print("  [PostgreSQL] Done.")


# ── Redis ──────────────────────────────────────────────────────────────────────
def seed_redis(endpoints, alerts):
    from db_connections import get_redis_conn

    print("\n[Redis] Seeding...")
    r = get_redis_conn()

    # Idempotency check
    existing = r.exists("endpoint:seeded")
    if existing:
        count = r.zcard("alert_counts")
        print(f"  [Redis] Already seeded ({count} alert_counts entries). Skipping.")
        return

    # Store each endpoint as a hash: endpoint:{id}
    pipe = r.pipeline(transaction=False)
    for i, ep in enumerate(tqdm(endpoints, desc="  endpoints")):
        key = f"endpoint:{ep['endpoint_id']}"
        pipe.hset(key, mapping={
            "hostname":     ep["hostname"],
            "datacenter":   ep["datacenter"],
            "environment":  ep["environment"],
            "service_type": ep["service_type"],
            "ip_address":   ep["ip_address"],
            "os":           ep["os"],
            "status":       ep["status"],
        })
        if i % 500 == 0:
            pipe.execute()
    pipe.execute()

    # Alert count per endpoint as a sorted set: key = alert_counts, member = endpoint_id, score = count
    alert_counts: dict = {}
    for a in alerts:
        alert_counts[a["endpoint_id"]] = alert_counts.get(a["endpoint_id"], 0) + 1

    pipe = r.pipeline(transaction=False)
    for ep_id, count in tqdm(alert_counts.items(), desc="  alert_counts"):
        pipe.zadd("alert_counts", {ep_id: count})
    pipe.execute()

    r.set("endpoint:seeded", "1")
    print(f"  endpoints: {len(endpoints):,} hashes")
    print(f"  alert_counts sorted set: {len(alert_counts):,} members")
    print("  [Redis] Done.")


# ── Cassandra ─────────────────────────────────────────────────────────────────
def seed_cassandra(metrics):
    from db_connections import get_cassandra_session

    print("\n[Cassandra] Seeding...")
    session = get_cassandra_session()

    # Keyspace
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS telemetry
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
    """)
    session.set_keyspace("telemetry")

    # Metrics table — partition by endpoint_id, cluster by recorded_at DESC
    session.execute("""
        CREATE TABLE IF NOT EXISTS metrics (
            endpoint_id  UUID,
            recorded_at  TIMESTAMP,
            metric_id    UUID,
            metric_name  TEXT,
            value        DOUBLE,
            unit         TEXT,
            PRIMARY KEY (endpoint_id, recorded_at, metric_id)
        ) WITH CLUSTERING ORDER BY (recorded_at DESC);
    """)

    # Idempotency — count a sample partition
    sample_ep = metrics[0]["endpoint_id"]
    rows = session.execute(
        "SELECT COUNT(*) FROM metrics WHERE endpoint_id = %s", (uuid.UUID(sample_ep),)
    )
    if rows.one()[0] > 0:
        total = session.execute("SELECT COUNT(*) FROM metrics").one()[0]
        print(f"  [Cassandra] Already seeded (~{total:,} rows). Skipping.")
        session.cluster.shutdown()
        return

    from cassandra.query import BatchStatement
    from cassandra import ConsistencyLevel

    insert_stmt = session.prepare("""
        INSERT INTO metrics (endpoint_id, recorded_at, metric_id, metric_name, value, unit)
        VALUES (?, ?, ?, ?, ?, ?)
    """)

    chunk_size = 50  # Cassandra batch limit
    for i in tqdm(range(0, len(metrics), chunk_size), desc="  metrics"):
        batch = BatchStatement(consistency_level=ConsistencyLevel.ONE)
        for m in metrics[i:i+chunk_size]:
            batch.add(insert_stmt, (
                uuid.UUID(m["endpoint_id"]),
                m["recorded_at"],
                uuid.UUID(m["metric_id"]),
                m["metric_name"],
                m["value"],
                m["unit"],
            ))
        session.execute(batch)

    print(f"  metrics: {len(metrics):,}")
    session.cluster.shutdown()
    print("  [Cassandra] Done.")


# ── Neo4j ──────────────────────────────────────────────────────────────────────
def seed_neo4j(endpoints):
    from db_connections import get_neo4j_driver

    print("\n[Neo4j] Seeding...")
    driver = get_neo4j_driver()

    with driver.session() as session:
        # Idempotency
        count = session.run("MATCH (e:Endpoint) RETURN COUNT(e) AS c").single()["c"]
        if count >= len(endpoints):
            print(f"  [Neo4j] Already seeded ({count} nodes). Skipping.")
            driver.close()
            return

        # Constraint for uniqueness
        session.run("""
            CREATE CONSTRAINT endpoint_id IF NOT EXISTS
            FOR (e:Endpoint) REQUIRE e.endpoint_id IS UNIQUE
        """)

        # Insert endpoints as nodes in chunks
        chunk_size = 500
        ep_list = [{
            "endpoint_id": e["endpoint_id"],
            "hostname":    e["hostname"],
            "datacenter":  e["datacenter"],
            "environment": e["environment"],
            "service_type": e["service_type"],
            "status":      e["status"],
        } for e in endpoints]

        for i in tqdm(range(0, len(ep_list), chunk_size), desc="  nodes"):
            session.run("""
                UNWIND $batch AS ep
                MERGE (e:Endpoint {endpoint_id: ep.endpoint_id})
                SET e.hostname     = ep.hostname,
                    e.datacenter   = ep.datacenter,
                    e.environment  = ep.environment,
                    e.service_type = ep.service_type,
                    e.status       = ep.status
            """, batch=ep_list[i:i+chunk_size])

        # Create DEPENDS_ON relationships (1-3 random deps per endpoint)
        ep_ids = [e["endpoint_id"] for e in endpoints]
        dep_pairs = []
        for ep in endpoints:
            n_deps = random.randint(1, 3)
            targets = random.sample([x for x in ep_ids if x != ep["endpoint_id"]], n_deps)
            for t in targets:
                dep_pairs.append({"src": ep["endpoint_id"], "dst": t})

        for i in tqdm(range(0, len(dep_pairs), 500), desc="  relationships"):
            session.run("""
                UNWIND $pairs AS pair
                MATCH (a:Endpoint {endpoint_id: pair.src})
                MATCH (b:Endpoint {endpoint_id: pair.dst})
                MERGE (a)-[:DEPENDS_ON]->(b)
            """, pairs=dep_pairs[i:i+500])

    print(f"  endpoints: {len(endpoints):,} nodes")
    print(f"  relationships: {len(dep_pairs):,} DEPENDS_ON edges")
    driver.close()
    print("  [Neo4j] Done.")


# ── InfluxDB ───────────────────────────────────────────────────────────────────
def seed_influxdb(metrics):
    from db_connections import get_influxdb_client
    from influxdb_client import Point
    from influxdb_client.client.write_api import SYNCHRONOUS

    print("\n[InfluxDB] Seeding...")
    client = get_influxdb_client()
    bucket = os.getenv("INFLUXDB_BUCKET", "telemetry")
    org    = os.getenv("INFLUXDB_ORG", "de_org")

    # Idempotency — query count
    query_api = client.query_api()
    try:
        result = query_api.query(
            f'from(bucket:"{bucket}") |> range(start: -91d) |> count() |> limit(n:1)',
            org=org
        )
        if result and any(True for _ in result):
            print("  [InfluxDB] Already seeded. Skipping.")
            client.close()
            return
    except Exception:
        pass  # bucket may be empty — proceed

    write_api = client.write_api(write_options=SYNCHRONOUS)
    chunk_size = 5000
    for i in tqdm(range(0, len(metrics), chunk_size), desc="  metrics"):
        points = []
        for m in metrics[i:i+chunk_size]:
            p = (
                Point("metrics")
                .tag("endpoint_id", m["endpoint_id"])
                .tag("metric_name", m["metric_name"])
                .tag("unit", m["unit"])
                .field("value", float(m["value"]))
                .time(m["recorded_at"])
            )
            points.append(p)
        write_api.write(bucket=bucket, org=org, record=points)

    print(f"  metrics: {len(metrics):,} points")
    client.close()
    print("  [InfluxDB] Done.")


# ── Elasticsearch ──────────────────────────────────────────────────────────────
def seed_elasticsearch(alerts):
    from db_connections import get_elasticsearch_client
    from elasticsearch.helpers import bulk

    print("\n[Elasticsearch] Seeding...")
    es = get_elasticsearch_client()
    index = "telemetry_alerts"

    # Idempotency
    if es.indices.exists(index=index):
        count = es.count(index=index)["count"]
        if count >= len(alerts):
            print(f"  [Elasticsearch] Already seeded ({count:,} docs). Skipping.")
            return

    # Create index with mapping
    es.indices.create(index=index, ignore=400, body={
        "mappings": {
            "properties": {
                "alert_id":    {"type": "keyword"},
                "endpoint_id": {"type": "keyword"},
                "severity":    {"type": "keyword"},
                "message":     {"type": "text"},
                "category":    {"type": "keyword"},
                "status":      {"type": "keyword"},
                "created_at":  {"type": "date"},
                "resolved_at": {"type": "date"},
            }
        }
    })

    def _actions():
        for a in alerts:
            doc = dict(a)
            doc["created_at"]  = a["created_at"].isoformat()
            doc["resolved_at"] = a["resolved_at"].isoformat() if a["resolved_at"] else None
            yield {"_index": index, "_id": a["alert_id"], "_source": doc}

    chunk_size = 1000
    alert_list = list(_actions())
    for i in tqdm(range(0, len(alert_list), chunk_size), desc="  alerts"):
        bulk(es, alert_list[i:i+chunk_size])

    print(f"  alerts: {len(alerts):,} documents")
    print("  [Elasticsearch] Done.")


# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("Citi Telemetry Seed — generating data...")
    print("=" * 60)

    print("Generating endpoints (10,000)...")
    endpoints = gen_endpoints(10_000)

    print("Generating metrics (500,000)...")
    metrics = gen_metrics(endpoints, 500_000)

    print("Generating alerts (25,000)...")
    alerts = gen_alerts(endpoints, 25_000)

    print("Generating events (50,000)...")
    events = gen_events(endpoints, 50_000)

    print(f"\nDataset ready:")
    print(f"  endpoints : {len(endpoints):>10,}")
    print(f"  metrics   : {len(metrics):>10,}")
    print(f"  alerts    : {len(alerts):>10,}")
    print(f"  events    : {len(events):>10,}")

    seed_postgres(endpoints, metrics, alerts, events)
    seed_redis(endpoints, alerts)
    seed_cassandra(metrics)
    seed_neo4j(endpoints)
    seed_influxdb(metrics)
    seed_elasticsearch(alerts)

    print("\n" + "=" * 60)
    print("Seed complete.")
    print("  PostgreSQL  : endpoints, metrics, alerts, events")
    print("  Redis       : endpoint hashes + alert_counts sorted set")
    print("  Cassandra   : metrics (partition by endpoint_id)")
    print("  Neo4j       : Endpoint nodes + DEPENDS_ON relationships")
    print("  InfluxDB    : metrics time-series points")
    print("  Elasticsearch: alerts documents")
    print("=" * 60)
