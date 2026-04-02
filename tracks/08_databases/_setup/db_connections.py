"""
db_connections.py
-----------------
Connection helpers for all 7 databases in the DE mastery stack.
Loads credentials from the env file using python-dotenv.

Usage:
    from db_connections import get_postgres_conn, test_all_connections
    conn = get_postgres_conn()
"""

import os
import time
from pathlib import Path
from dotenv import load_dotenv

# Load credentials from the non-dot-prefixed env file in the same directory
_env_path = Path(__file__).parent / "env"
load_dotenv(_env_path, override=True)  # override=True ensures shell env vars don't shadow the file


# ── PostgreSQL ──────────────────────────────────────────────────────────────────
def get_postgres_conn():
    """Return a psycopg2 connection to PostgreSQL."""
    import psycopg2
    return psycopg2.connect(
        host="localhost",
        port=int(os.getenv("POSTGRES_PORT", 5432)),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        dbname=os.getenv("POSTGRES_DB"),
    )


def test_postgres():
    """Ping PostgreSQL. Returns (success: bool, latency_ms: float)."""
    try:
        t0 = time.perf_counter()
        conn = get_postgres_conn()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.fetchone()
        conn.close()
        return True, (time.perf_counter() - t0) * 1000
    except Exception as e:
        print(f"  [PostgreSQL] {e}")
        return False, 0.0


# ── Redis ───────────────────────────────────────────────────────────────────────
def get_redis_conn():
    """Return a redis.Redis client."""
    import redis
    return redis.Redis(
        host="localhost",
        port=int(os.getenv("REDIS_PORT", 6379)),
        password=os.getenv("REDIS_PASSWORD"),
        decode_responses=True,
    )


def test_redis():
    """Ping Redis. Returns (success: bool, latency_ms: float)."""
    try:
        t0 = time.perf_counter()
        r = get_redis_conn()
        r.ping()
        return True, (time.perf_counter() - t0) * 1000
    except Exception as e:
        print(f"  [Redis] {e}")
        return False, 0.0


# ── Cassandra ───────────────────────────────────────────────────────────────────
def get_cassandra_session():
    """Return a Cassandra Session connected to the local cluster."""
    import asyncore  # pyasyncore package restores this module removed in Python 3.12
    from cassandra.cluster import Cluster
    from cassandra.policies import ConstantReconnectionPolicy

    cluster = Cluster(
        ["127.0.0.1"],
        port=int(os.getenv("CASSANDRA_PORT", 9042)),
        connect_timeout=10,
        control_connection_timeout=10,
        reconnection_policy=ConstantReconnectionPolicy(delay=2, max_attempts=3),
        protocol_version=4,
    )
    return cluster.connect()


def test_cassandra():
    """Ping Cassandra. Returns (success: bool, latency_ms: float)."""
    try:
        t0 = time.perf_counter()
        session = get_cassandra_session()
        session.execute("SELECT release_version FROM system.local")
        session.cluster.shutdown()
        return True, (time.perf_counter() - t0) * 1000
    except Exception as e:
        print(f"  [Cassandra] {e}")
        return False, 0.0


# ── Neo4j ───────────────────────────────────────────────────────────────────────
def get_neo4j_driver():
    """Return a neo4j Driver connected to the local instance."""
    from neo4j import GraphDatabase

    uri = f"bolt://localhost:{os.getenv('NEO4J_BOLT_PORT', 7687)}"
    return GraphDatabase.driver(
        uri,
        auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD")),
    )


def test_neo4j():
    """Ping Neo4j. Returns (success: bool, latency_ms: float)."""
    try:
        t0 = time.perf_counter()
        driver = get_neo4j_driver()
        with driver.session() as session:
            session.run("RETURN 1").single()
        driver.close()
        return True, (time.perf_counter() - t0) * 1000
    except Exception as e:
        print(f"  [Neo4j] {e}")
        return False, 0.0


# ── InfluxDB ────────────────────────────────────────────────────────────────────
def get_influxdb_client():
    """Return an InfluxDBClient connected to the local instance."""
    from influxdb_client import InfluxDBClient as _InfluxDBClient

    return _InfluxDBClient(
        url=f"http://localhost:{os.getenv('INFLUXDB_PORT', 8086)}",
        token=os.getenv("INFLUXDB_TOKEN"),
        org=os.getenv("INFLUXDB_ORG"),
    )


def test_influxdb():
    """Ping InfluxDB. Returns (success: bool, latency_ms: float)."""
    try:
        t0 = time.perf_counter()
        client = get_influxdb_client()
        health = client.health()
        client.close()
        ok = health.status == "pass"
        return ok, (time.perf_counter() - t0) * 1000
    except Exception as e:
        print(f"  [InfluxDB] {e}")
        return False, 0.0


# ── Elasticsearch ───────────────────────────────────────────────────────────────
def get_elasticsearch_client():
    """Return an Elasticsearch client connected to the local instance."""
    from elasticsearch import Elasticsearch

    return Elasticsearch(
        f"http://localhost:{os.getenv('ELASTIC_PORT', 9200)}",
        basic_auth=("elastic", os.getenv("ELASTIC_PASSWORD")),
        verify_certs=False,
        ssl_show_warn=False,
    )


def test_elasticsearch():
    """Ping Elasticsearch. Returns (success: bool, latency_ms: float)."""
    try:
        t0 = time.perf_counter()
        es = get_elasticsearch_client()
        ok = es.ping()
        return ok, (time.perf_counter() - t0) * 1000
    except Exception as e:
        print(f"  [Elasticsearch] {e}")
        return False, 0.0


# ── DuckDB ──────────────────────────────────────────────────────────────────────
def get_duckdb_conn():
    """Return an in-memory DuckDB connection (with Postgres attached)."""
    import duckdb

    conn = duckdb.connect(":memory:")
    # Attach Postgres via duckdb postgres extension for live querying
    try:
        conn.execute("INSTALL postgres; LOAD postgres;")
        pg_dsn = (
            f"host=localhost "
            f"port={os.getenv('POSTGRES_PORT', 5432)} "
            f"user={os.getenv('POSTGRES_USER')} "
            f"password={os.getenv('POSTGRES_PASSWORD')} "
            f"dbname={os.getenv('POSTGRES_DB')}"
        )
        conn.execute(f"ATTACH '{pg_dsn}' AS pg (TYPE POSTGRES, READ_ONLY);")
    except Exception:
        pass  # attachment is optional; base DuckDB always works
    return conn


def test_duckdb():
    """Ping DuckDB. Returns (success: bool, latency_ms: float)."""
    try:
        t0 = time.perf_counter()
        conn = get_duckdb_conn()
        conn.execute("SELECT 42").fetchone()
        conn.close()
        return True, (time.perf_counter() - t0) * 1000
    except Exception as e:
        print(f"  [DuckDB] {e}")
        return False, 0.0


# ── MongoDB Atlas ───────────────────────────────────────────────────────────────
def get_mongo_client():
    """Return a pymongo MongoClient connected to MongoDB Atlas."""
    from pymongo import MongoClient
    uri = os.getenv("MONGO_URI")
    return MongoClient(uri)


def get_mongo_db():
    """Return the MongoDB database object."""
    client = get_mongo_client()
    db_name = os.getenv("MONGO_DB", "de_telemetry")
    return client[db_name]


def test_mongo():
    """Ping MongoDB Atlas. Returns (success: bool, latency_ms: float)."""
    try:
        t0 = time.perf_counter()
        db = get_mongo_db()
        db.command("ping")
        return True, round((time.perf_counter() - t0) * 1000, 1)
    except Exception as e:
        print(f"  [MongoDB] {e}")
        return False, 0.0


# ── test_all_connections ─────────────────────────────────────────────────────────
def test_all_connections() -> bool:
    """
    Test all 7 database connections.
    Prints a formatted table. Returns True if all pass, False if any fail.
    """
    tests = [
        ("PostgreSQL",     test_postgres),
        ("Redis",          test_redis),
        ("Cassandra",      test_cassandra),
        ("Neo4j",          test_neo4j),
        ("InfluxDB",       test_influxdb),
        ("Elasticsearch",  test_elasticsearch),
        ("DuckDB",         test_duckdb),
        ("MongoDB Atlas",  test_mongo),
    ]

    results = []
    print("\nTesting connections...")
    for name, fn in tests:
        ok, ms = fn()
        results.append((name, ok, ms))

    # Print table
    header = f"\n  {'DATABASE':<20} {'STATUS':<12} {'LATENCY':>10}"
    print(header)
    print("  " + "-" * 44)
    all_pass = True
    for name, ok, ms in results:
        status = "PASS" if ok else "FAIL"
        latency = f"{ms:.1f}ms" if ok else "---"
        print(f"  {name:<20} {status:<12} {latency:>10}")
        if not ok:
            all_pass = False
    print("  " + "-" * 44)
    print(f"  {'Result:':<20} {'ALL PASS' if all_pass else 'FAILURES DETECTED'}")
    return all_pass


if __name__ == "__main__":
    import sys
    ok = test_all_connections()
    sys.exit(0 if ok else 1)
