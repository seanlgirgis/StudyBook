# Story:
# This file compares good vs bad query coverage for a composite index.
# It matters because the leftmost column determines whether the index helps.
# Expect the good query to use the index and the bad one to scan.

from pathlib import Path

import psycopg2


def _load_env_config():
    env_path = Path(__file__).resolve().parents[2] / "_setup" / "env"
    config = {}
    with env_path.open("r") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if not line.startswith("POSTGRES_"):
                continue
            key, value = line.split("=", 1)
            config[key] = value

    required = [
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
        "POSTGRES_DB",
        "POSTGRES_PORT",
    ]
    missing = [k for k in required if k not in config]
    if missing:
        raise ValueError(f"Missing keys in env file: {', '.join(missing)}")

    return {k: config[k] for k in required}


def _open_connection():
    config = _load_env_config()
    conn = psycopg2.connect(
        host="localhost",
        port=config["POSTGRES_PORT"],
        database=config["POSTGRES_DB"],
        user=config["POSTGRES_USER"],
        password=config["POSTGRES_PASSWORD"],
    )
    conn.autocommit = False
    return conn


def _setup_shipments():
    session = _open_connection()
    try:
        with session.cursor() as cur:
            # Step 1:
            # Reset the table so the demo is rerunnable.
            cur.execute("DROP TABLE IF EXISTS shipments;")
            cur.execute(
                """
                CREATE TABLE shipments (
                    id SERIAL PRIMARY KEY,
                    region TEXT NOT NULL,
                    shipped_at DATE NOT NULL,
                    total_cents INTEGER NOT NULL
                );
                """
            )
            cur.execute(
                "CREATE INDEX shipments_region_date_idx ON shipments (region, shipped_at);"
            )

            rows = []
            regions = ["US", "EU", "APAC"]
            for i in range(24000):
                region = regions[i % len(regions)]
                shipped_at = "2024-{:02d}-{:02d}".format(
                    (i % 12) + 1,
                    (i % 28) + 1,
                )
                total = 1000 + (i % 200) * 50
                rows.append((region, shipped_at, total))

            cur.executemany(
                """
                INSERT INTO shipments (region, shipped_at, total_cents)
                VALUES (%s, %s, %s);
                """,
                rows,
            )
            cur.execute("ANALYZE shipments;")
        session.commit()
    finally:
        session.close()


def _print_plan(label, sql, params=None):
    session = _open_connection()
    try:
        with session.cursor() as cur:
            cur.execute(f"EXPLAIN ANALYZE {sql}", params or ())
            rows = cur.fetchall()
        session.commit()
    finally:
        session.close()

    print(label)
    for (line,) in rows:
        print(line)


def run_good_vs_bad_queries_demo():
    # Step 0:
    # Reset data so the planner has correct stats.
    _setup_shipments()

    # Good coverage:
    # Leftmost column (region) is present, so the composite index helps.
    _print_plan(
        "Good - WHERE region = 'US' AND shipped_at >= '2024-06-01' (expect Index Scan)",
        """
        SELECT * FROM shipments
        WHERE region = %s AND shipped_at >= %s;
        """,
        ("US", "2024-06-01"),
    )

    # Bad coverage:
    # Missing the leftmost column makes the composite index weak.
    _print_plan(
        "Bad - WHERE shipped_at >= '2024-06-01' (expect Seq Scan)",
        "SELECT * FROM shipments WHERE shipped_at >= %s;",
        ("2024-06-01",),
    )


if __name__ == "__main__":
    # Step 2:
    # Run the good vs bad demo directly.
    run_good_vs_bad_queries_demo()

# Takeaway:
# Composite indexes only help when the leftmost column is included in the filter.
