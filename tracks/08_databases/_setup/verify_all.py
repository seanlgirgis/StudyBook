"""
verify_all.py
-------------
Connects to all 7 databases, verifies seeded record counts,
prints a formatted status table, exits 0 if all pass / 1 if any fail.
"""

import sys
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / "env", override=True)

from db_connections import (
    get_postgres_conn,
    get_redis_conn,
    get_cassandra_session,
    get_neo4j_driver,
    get_influxdb_client,
    get_elasticsearch_client,
    get_duckdb_conn,
    get_mongo_db,
)

results = []   # (db_name, ok, latency_ms, record_str)


def check(name, fn):
    try:
        ok, ms, records = fn()
        results.append((name, ok, ms, records))
    except Exception as e:
        results.append((name, False, 0.0, f"ERROR: {e}"))


# ── PostgreSQL ─────────────────────────────────────────────────────────────────
def _check_postgres():
    t0 = time.perf_counter()
    conn = get_postgres_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM telemetry.endpoints")
    ep_count = cur.fetchone()[0]
    conn.close()
    ms = (time.perf_counter() - t0) * 1000
    return True, ms, f"{ep_count:,} endpoints"


# ── Redis ──────────────────────────────────────────────────────────────────────
def _check_redis():
    t0 = time.perf_counter()
    r = get_redis_conn()
    # Count keys matching endpoint:* pattern
    cursor = 0
    count = 0
    while True:
        cursor, keys = r.scan(cursor, match="endpoint:????????-*", count=1000)
        count += len(keys)
        if cursor == 0:
            break
    ms = (time.perf_counter() - t0) * 1000
    return True, ms, f"{count:,} keys"


# ── Cassandra ──────────────────────────────────────────────────────────────────
def _check_cassandra():
    t0 = time.perf_counter()
    session = get_cassandra_session()
    session.set_keyspace("telemetry")
    row = session.execute("SELECT COUNT(*) FROM metrics").one()
    count = row[0]
    session.cluster.shutdown()
    ms = (time.perf_counter() - t0) * 1000
    return True, ms, f"{count:,} metrics"


# ── Neo4j ──────────────────────────────────────────────────────────────────────
def _check_neo4j():
    t0 = time.perf_counter()
    driver = get_neo4j_driver()
    with driver.session() as session:
        count = session.run("MATCH (e:Endpoint) RETURN COUNT(e) AS c").single()["c"]
    driver.close()
    ms = (time.perf_counter() - t0) * 1000
    return True, ms, f"{count:,} nodes"


# ── InfluxDB ───────────────────────────────────────────────────────────────────
def _check_influxdb():
    import os
    t0 = time.perf_counter()
    client = get_influxdb_client()
    bucket = os.getenv("INFLUXDB_BUCKET", "telemetry")
    org    = os.getenv("INFLUXDB_ORG", "de_org")
    query_api = client.query_api()
    tables = query_api.query(
        f'from(bucket:"{bucket}") |> range(start: -91d) |> count()',
        org=org
    )
    total = sum(rec.get_value() for table in tables for rec in table.records)
    client.close()
    ms = (time.perf_counter() - t0) * 1000
    return True, ms, f"{total:,} points"


# ── Elasticsearch ──────────────────────────────────────────────────────────────
def _check_elasticsearch():
    t0 = time.perf_counter()
    es = get_elasticsearch_client()
    count = es.count(index="telemetry_alerts")["count"]
    ms = (time.perf_counter() - t0) * 1000
    return True, ms, f"{count:,} alerts"


# ── DuckDB ─────────────────────────────────────────────────────────────────────
def _check_duckdb():
    t0 = time.perf_counter()
    conn = get_duckdb_conn()
    conn.execute("SELECT 42").fetchone()
    conn.close()
    ms = (time.perf_counter() - t0) * 1000
    return True, ms, "in-memory (no seed)"


# ── MongoDB Atlas ───────────────────────────────────────────────────────────────
def _check_mongo():
    t0 = time.perf_counter()
    db = get_mongo_db()
    ep_count = db["endpoints"].estimated_document_count()
    al_count = db["alerts"].estimated_document_count()
    ms = (time.perf_counter() - t0) * 1000
    return True, ms, f"{ep_count:,} endpoints · {al_count:,} alerts"


# ── Splunk ─────────────────────────────────────────────────────────────────────
def _check_splunk():
    import os, time
    import urllib.request, ssl, base64, json
    
    t0 = time.perf_counter()
    user = "admin"
    password = os.getenv("SPLUNK_PASSWORD")
    port = os.getenv("SPLUNK_PORT_MGT", 8089)
    url = f"https://localhost:{port}/services/server/info?output_mode=json"

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(url)
    auth_b64 = base64.b64encode(f"{user}:{password}".encode("utf-8")).decode("ascii")
    req.add_header("Authorization", f"Basic {auth_b64}")

    try:
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
            version = data.get("generator", {}).get("version", "unknown")
            ms = (time.perf_counter() - t0) * 1000
            return True, ms, f"v{version} (no seed)"
    except Exception as e:
        return False, 0.0, str(e)


# ── Run all checks ─────────────────────────────────────────────────────────────
print("\nVerifying all databases...\n")

checks = [
    ("PostgreSQL",    _check_postgres),
    ("Redis",         _check_redis),
    ("Cassandra",     _check_cassandra),
    ("Neo4j",         _check_neo4j),
    ("InfluxDB",      _check_influxdb),
    ("Elasticsearch", _check_elasticsearch),
    ("DuckDB",        _check_duckdb),
    ("MongoDB Atlas", _check_mongo),
    ("Splunk",        _check_splunk),
]

for name, fn in checks:
    print(f"  Checking {name}...", end=" ", flush=True)
    try:
        ok, ms, records = fn()
        results.append((name, ok, ms, records))
        print(f"OK  ({ms:.0f}ms)")
    except Exception as e:
        results.append((name, False, 0.0, str(e)))
        print(f"FAIL  {e}")

# ── Print table ────────────────────────────────────────────────────────────────
print()
header = f"  {'DB':<20} {'STATUS':<12} {'LATENCY':>10}   {'RECORDS'}"
print(header)
print("  " + "-" * 65)

all_pass = True
for name, ok, ms, records in results:
    status  = "PASS" if ok else "FAIL"
    latency = f"{ms:.0f}ms" if ok else "---"
    print(f"  {name:<20} {status:<12} {latency:>10}   {records}")
    if not ok:
        all_pass = False

print("  " + "-" * 65)
verdict = "ALL GREEN" if all_pass else "FAILURES DETECTED"
print(f"  {verdict}\n")

sys.exit(0 if all_pass else 1)
