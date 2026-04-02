# Story:
# This file shows how to read an execution plan.
# It matters because the plan explains where time is spent.
# Expect a Seq Scan for the bad query and an Index Scan for the good one.

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


def _print_plan(label, sql, params):
    session = _open_connection()
    try:
        with session.cursor() as cur:
            cur.execute(f"EXPLAIN ANALYZE {sql}", params)
            rows = cur.fetchall()
        session.commit()
    finally:
        session.close()

    print(label)
    for (line,) in rows:
        print(line)


def run_explain_demo():
    # Step 0:
    # Reset data so the plan is predictable.
    _setup_orders()

    target_email = "user15000@example.com"

    # Step 1:
    # Bad query plan: look for Seq Scan and high rows read.
    # Plan cost = estimated work; rows = estimated row count.
    # Actual rows/time show what really happened.
    _print_plan(
        "Bad query plan (look for Seq Scan, high actual rows)",
        "SELECT * FROM customer_orders WHERE LOWER(customer_email) = LOWER(%s);",
        (target_email,),
    )

    # Step 2:
    # Good query plan: look for Index Scan and low rows read.
    # Big gaps between estimated rows and actual rows mean stats are off.
    # If actual time is high, the plan is expensive or the estimate is wrong.
    _print_plan(
        "Good query plan (look for Index Scan, low actual rows)",
        "SELECT * FROM customer_orders WHERE customer_email = %s;",
        (target_email,),
    )


if __name__ == "__main__":
    # Step 3:
    # Run the explain demo directly.
    run_explain_demo()

# Takeaway:
# Execution plans reveal whether the database scanned everything or jumped to the row.
