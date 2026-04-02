# Story:
# This file compares row-style vs column-style access on the same data.
# It matters because analytics often needs a few columns across many rows.
# Expect the column-style query to read fewer buffers and run faster.

import time
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


def _setup_events():
    session = _open_connection()
    try:
        with session.cursor() as cur:
            # Step 1:
            # Reset the table so the demo is rerunnable.
            cur.execute("DROP TABLE IF EXISTS events;")
            cur.execute(
                """
                CREATE TABLE events (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    event_type TEXT NOT NULL,
                    device TEXT NOT NULL,
                    country TEXT NOT NULL,
                    ts TIMESTAMP NOT NULL,
                    value INTEGER NOT NULL,
                    payload_text TEXT NOT NULL
                );
                """
            )

            rows = []
            event_types = ["page_view", "purchase", "signup", "support_ticket"]
            devices = [
                "mobile-android-v2",
                "mobile-ios-v3",
                "desktop-chrome-v120",
                "desktop-firefox-v118",
            ]
            countries = [
                "United-States",
                "United-Kingdom",
                "Germany",
                "Brazil",
                "India",
            ]
            payload_base = "x" * 1200
            for i in range(100000):
                user_id = (i % 5000) + 1
                event_type = event_types[i % len(event_types)]
                device = devices[i % len(devices)]
                country = countries[i % len(countries)]
                ts = "2024-06-{:02d} {:02d}:00:00".format(
                    (i % 28) + 1,
                    i % 24,
                )
                value = (i % 1000) * 3
                payload_text = f"{payload_base}{i % 1000}"
                rows.append(
                    (
                        user_id,
                        event_type,
                        device,
                        country,
                        ts,
                        value,
                        payload_text,
                    )
                )

            cur.executemany(
                """
                INSERT INTO events (
                    user_id,
                    event_type,
                    device,
                    country,
                    ts,
                    value,
                    payload_text
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s);
                """,
                rows,
            )

            cur.execute("CREATE INDEX events_user_idx ON events (user_id);")
            cur.execute("ANALYZE events;")
        session.commit()
    finally:
        session.close()


def _add_covering_index():
    session = _open_connection()
    try:
        with session.cursor() as cur:
            cur.execute("DROP INDEX IF EXISTS events_user_cover_idx;")
            cur.execute(
                """
                CREATE INDEX events_user_cover_idx
                ON events (user_id)
                INCLUDE (value);
                """
            )
            cur.execute("ANALYZE events;")
        session.commit()
    finally:
        session.close()


def _drop_normal_index():
    session = _open_connection()
    try:
        with session.cursor() as cur:
            cur.execute("DROP INDEX IF EXISTS events_user_idx;")
            cur.execute("ANALYZE events;")
        session.commit()
    finally:
        session.close()


def _print_plan(label, sql, params=None):
    session = _open_connection()
    try:
        with session.cursor() as cur:
            cur.execute(f"EXPLAIN (ANALYZE, BUFFERS) {sql}", params or ())
            rows = cur.fetchall()
        session.commit()
    finally:
        session.close()

    print(label)
    for (line,) in rows:
        print(line)


def _time_query(label, sql, params=None):
    session = _open_connection()
    try:
        with session.cursor() as cur:
            start = time.perf_counter()
            cur.execute(sql, params or ())
            cur.fetchall()
            elapsed = time.perf_counter() - start
        session.commit()
    finally:
        session.close()
    print(f"{label}: {elapsed:.4f}s")


def run_row_vs_column_demo():
    # Step 0:
    # Load data and build a normal index.
    _setup_events()

    threshold = 500

    # Scenario A:
    # Row-style access pulls full rows.
    # Note: Postgres is a row store; this is a row-store simulation of column benefit.
    _print_plan(
        "Scenario A - row-style (SELECT *)",
        "SELECT * FROM events WHERE user_id < %s;",
        (threshold,),
    )
    _time_query(
        "Scenario A runtime",
        "SELECT * FROM events WHERE user_id < %s;",
        (threshold,),
    )

    # Step 1:
    # Add a covering index and remove the normal index so the planner uses coverage.
    _add_covering_index()
    _drop_normal_index()

    # Scenario B:
    # Column-style access reads only the needed columns.
    # Plan type may be Index Scan or Index Only Scan, but buffers should drop.
    # This is still a row-store engine; we're showing the benefit of narrow projection.
    _print_plan(
        "Scenario B - column-style (SELECT user_id, value)",
        "SELECT user_id, value FROM events WHERE user_id < %s;",
        (threshold,),
    )
    _time_query(
        "Scenario B runtime",
        "SELECT user_id, value FROM events WHERE user_id < %s;",
        (threshold,),
    )


if __name__ == "__main__":
    # Step 2:
    # Run the demo directly.
    run_row_vs_column_demo()

# Takeaway:
# Column-style access avoids reading unnecessary data.
