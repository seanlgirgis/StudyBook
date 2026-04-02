# Story:
# This file shows how a small query becomes slow at scale.
# It matters because the same logic can be fast or painfully slow.
# Expect the "bad" query to take longer than the "good" query.

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


def _setup_orders():
    session = _open_connection()
    try:
        with session.cursor() as cur:
            # Step 1:
            # Reset the table so the demo is rerunnable.
            cur.execute("DROP TABLE IF EXISTS customer_orders;")
            cur.execute(
                """
                CREATE TABLE customer_orders (
                    id SERIAL PRIMARY KEY,
                    customer_email TEXT NOT NULL,
                    total_cents INTEGER NOT NULL
                );
                """
            )
            cur.execute(
                "CREATE INDEX customer_orders_email_idx ON customer_orders (customer_email);"
            )

            # Step 2:
            # Seed enough rows so the scan cost shows up.
            rows = []
            for i in range(20000):
                email = f"user{i:05d}@example.com"
                total = (i % 200) * 100
                rows.append((email, total))
            cur.executemany(
                "INSERT INTO customer_orders (customer_email, total_cents) VALUES (%s, %s);",
                rows,
            )
            cur.execute("ANALYZE customer_orders;")
        session.commit()
    finally:
        session.close()


def _time_query(label, sql, params):
    session = _open_connection()
    try:
        with session.cursor() as cur:
            start = time.perf_counter()
            cur.execute(sql, params)
            cur.fetchall()
            elapsed = time.perf_counter() - start
        session.commit()
    finally:
        session.close()
    print(f"{label}: {elapsed:.4f}s")


def run_bad_vs_good_demo():
    # Step 0:
    # Reset the data so the comparison is fair.
    _setup_orders()

    target_email = "user15000@example.com"

    # Step 3:
    # Bad pattern: wrap the column in LOWER(), which blocks the index.
    _time_query(
        "Bad query (seq scan likely)",
        "SELECT * FROM customer_orders WHERE LOWER(customer_email) = LOWER(%s);",
        (target_email,),
    )

    # Step 4:
    # Good pattern: direct equality can use the index.
    _time_query(
        "Good query (index scan likely)",
        "SELECT * FROM customer_orders WHERE customer_email = %s;",
        (target_email,),
    )


if __name__ == "__main__":
    # Step 5:
    # Run the timing comparison directly.
    run_bad_vs_good_demo()

# Takeaway:
# Optimization is about helping the database do less work per query.
