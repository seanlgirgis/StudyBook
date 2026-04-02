# Story:
# This file shows when indexes are ignored.
# It matters because "index exists" does not mean "index used."
# Expect Seq Scans in each case, for different reasons.

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


def _setup_table():
    session = _open_connection()
    try:
        with session.cursor() as cur:
            # Step 1:
            # Reset the table so the demo is deterministic.
            cur.execute("DROP TABLE IF EXISTS product_events;")
            cur.execute(
                """
                CREATE TABLE product_events (
                    id SERIAL PRIMARY KEY,
                    event_type TEXT NOT NULL,
                    user_email TEXT NOT NULL
                );
                """
            )
            cur.execute(
                "CREATE INDEX product_events_email_idx ON product_events (user_email);"
            )
            cur.execute(
                "CREATE INDEX product_events_type_idx ON product_events (event_type);"
            )

            rows = []
            for i in range(30000):
                email = f"user{i:05d}@example.com"
                event_type = "click" if i % 10 else "purchase"
                rows.append((event_type, email))
            cur.executemany(
                "INSERT INTO product_events (event_type, user_email) VALUES (%s, %s);",
                rows,
            )
            cur.execute("ANALYZE product_events;")
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


def run_index_not_used_demo():
    # Step 0:
    # Reset data so each case is fair.
    _setup_table()

    target_email = "user15000@example.com"

    # Case A:
    # Function breaks index usage on the column.
    _print_plan(
        "Case A - LOWER(column) blocks index (expect Seq Scan)",
        "SELECT * FROM product_events WHERE LOWER(user_email) = LOWER(%s);",
        (target_email,),
    )

    # Case B:
    # Low selectivity: most rows match, so scan can be cheaper.
    _print_plan(
        "Case B - low selectivity (expect Seq Scan)",
        "SELECT * FROM product_events WHERE event_type = 'click';",
    )

    # Case C:
    # Small table: scan is cheap, index overhead not worth it.
    small_session = _open_connection()
    try:
        with small_session.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS product_events_tiny;")
            cur.execute(
                """
                CREATE TABLE product_events_tiny (
                    id SERIAL PRIMARY KEY,
                    event_type TEXT NOT NULL,
                    user_email TEXT NOT NULL
                );
                """
            )
            cur.execute(
                "CREATE INDEX product_events_tiny_email_idx ON product_events_tiny (user_email);"
            )
            cur.executemany(
                "INSERT INTO product_events_tiny (event_type, user_email) VALUES (%s, %s);",
                [
                    ("click", "tiny1@example.com"),
                    ("click", "tiny2@example.com"),
                    ("purchase", "tiny3@example.com"),
                    ("click", "tiny4@example.com"),
                ],
            )
            cur.execute("ANALYZE product_events_tiny;")
        small_session.commit()
    finally:
        small_session.close()
    _print_plan(
        "Case C - tiny table with index (expect Seq Scan)",
        "SELECT * FROM product_events_tiny WHERE user_email = %s;",
        ("tiny3@example.com",),
    )


if __name__ == "__main__":
    # Step 2:
    # Run the index-not-used cases directly.
    run_index_not_used_demo()

# Takeaway:
# The planner skips indexes when they are not the cheapest path.
