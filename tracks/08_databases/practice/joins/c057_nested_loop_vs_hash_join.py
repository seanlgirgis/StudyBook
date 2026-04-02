# Story:
# This file shows how the planner chooses Nested Loop vs Hash Join.
# It matters because indexes can flip the join strategy.
# Expect Nested Loop with an index, Hash Join without one.

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


def _setup_tables():
    session = _open_connection()
    try:
        with session.cursor() as cur:
            # Step 1:
            # Reset tables so the demo is rerunnable.
            cur.execute("DROP TABLE IF EXISTS orders;")
            cur.execute("DROP TABLE IF EXISTS customers;")
            cur.execute(
                """
                CREATE TABLE customers (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    region TEXT NOT NULL
                );
                """
            )
            cur.execute(
                """
                CREATE TABLE orders (
                    id SERIAL PRIMARY KEY,
                    customer_id INTEGER NOT NULL,
                    total_cents INTEGER NOT NULL,
                    created_at TIMESTAMP NOT NULL
                );
                """
            )

            customer_rows = []
            regions = ["EU", "APAC"]
            for i in range(1000):
                if i < 10:
                    region = "US"
                else:
                    region = regions[(i - 10) % len(regions)]
                customer_rows.append((f"Customer {i:04d}", region))
            cur.executemany(
                "INSERT INTO customers (name, region) VALUES (%s, %s);",
                customer_rows,
            )

            order_rows = []
            for i in range(30000):
                customer_id = (i % 1000) + 1
                total = 1000 + (i % 200) * 50
                created_at = "2024-06-{:02d} {:02d}:00:00".format(
                    (i % 28) + 1,
                    i % 24,
                )
                order_rows.append((customer_id, total, created_at))
            cur.executemany(
                """
                INSERT INTO orders (customer_id, total_cents, created_at)
                VALUES (%s, %s, %s);
                """,
                order_rows,
            )
            cur.execute("ANALYZE customers;")
            cur.execute("ANALYZE orders;")
        session.commit()
    finally:
        session.close()


def _add_index_on_orders():
    session = _open_connection()
    try:
        with session.cursor() as cur:
            cur.execute("DROP INDEX IF EXISTS orders_customer_idx;")
            cur.execute("CREATE INDEX orders_customer_idx ON orders (customer_id);")
            cur.execute("ANALYZE orders;")
        session.commit()
    finally:
        session.close()


def _drop_index_on_orders():
    session = _open_connection()
    try:
        with session.cursor() as cur:
            cur.execute("DROP INDEX IF EXISTS orders_customer_idx;")
            cur.execute("ANALYZE orders;")
        session.commit()
    finally:
        session.close()


def _print_plan(label, sql):
    session = _open_connection()
    try:
        with session.cursor() as cur:
            cur.execute(f"EXPLAIN ANALYZE {sql}")
            rows = cur.fetchall()
        session.commit()
    finally:
        session.close()

    print(label)
    for (line,) in rows:
        print(line)


def run_join_strategy_demo():
    # Step 0:
    # Reset data and stats.
    _setup_tables()

    join_sql_small = """
        SELECT c.name, o.total_cents
        FROM customers c
        JOIN orders o ON o.customer_id = c.id
        WHERE c.region = 'US';
    """
    join_sql_large = """
        SELECT c.name, o.total_cents
        FROM customers c
        JOIN orders o ON o.customer_id = c.id;
    """

    # Scenario A:
    # With index on orders.customer_id and a tiny outer set, planner can do Nested Loop.
    _add_index_on_orders()
    _print_plan(
        "Scenario A - small outer set + index (expect Nested Loop)",
        join_sql_small,
    )

    # Scenario B:
    # Without index and a broad join, planner will likely choose Hash Join.
    _drop_index_on_orders()
    _print_plan(
        "Scenario B - broad join without index (expect Hash Join)",
        join_sql_large,
    )


if __name__ == "__main__":
    # Step 1:
    # Run the join strategy demo directly.
    run_join_strategy_demo()

# Takeaway:
# Indexes often shift joins from Hash Join to Nested Loop.
