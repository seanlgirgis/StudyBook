# Story:
# This file compares a normal index vs a covering index.
# It matters because covering indexes can avoid extra table reads.
# Expect fewer table hits when the index covers all selected columns.

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
            cur.execute("DROP TABLE IF EXISTS support_orders;")
            cur.execute(
                """
                CREATE TABLE support_orders (
                    id SERIAL PRIMARY KEY,
                    customer_email TEXT NOT NULL,
                    status TEXT NOT NULL,
                    total_cents INTEGER NOT NULL,
                    created_at TIMESTAMP NOT NULL
                );
                """
            )
            cur.execute(
                "CREATE INDEX support_orders_email_idx ON support_orders (customer_email);"
            )

            rows = []
            statuses = ["new", "processing", "shipped", "refunded"]
            for i in range(30000):
                email = f"user{i:05d}@example.com"
                status = statuses[i % len(statuses)]
                total = 1000 + (i % 200) * 50
                created_at = "2024-06-{:02d} {:02d}:00:00".format(
                    (i % 28) + 1,
                    i % 24,
                )
                rows.append((email, status, total, created_at))

            cur.executemany(
                """
                INSERT INTO support_orders (customer_email, status, total_cents, created_at)
                VALUES (%s, %s, %s, %s);
                """,
                rows,
            )
            cur.execute("ANALYZE support_orders;")
        session.commit()
    finally:
        session.close()


def _add_covering_index():
    session = _open_connection()
    try:
        with session.cursor() as cur:
            cur.execute("DROP INDEX IF EXISTS support_orders_email_cover_idx;")
            cur.execute(
                """
                CREATE INDEX support_orders_email_cover_idx
                ON support_orders (customer_email)
                INCLUDE (status, total_cents);
                """
            )
            cur.execute("ANALYZE support_orders;")
        session.commit()
    finally:
        session.close()


def _drop_normal_index():
    session = _open_connection()
    try:
        with session.cursor() as cur:
            cur.execute("DROP INDEX IF EXISTS support_orders_email_idx;")
            cur.execute("ANALYZE support_orders;")
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


def run_covering_vs_normal_demo():
    # Step 0:
    # Reset data and add a normal index.
    _setup_orders()

    target_email = "user15000@example.com"

    # Case A:
    # Normal index finds the row, but still needs table data for status and total.
    # Plan type can be Index Scan (not Index Only Scan) since coverage is missing.
    _print_plan(
        "Case A - normal index (expect Index Scan + heap fetch)",
        """
        SELECT status, total_cents
        FROM support_orders
        WHERE customer_email = %s;
        """,
        (target_email,),
    )

    # Step 1:
    # Add a covering index that includes the needed columns.
    _add_covering_index()

    # Case B:
    # Drop the normal index so the planner must consider the covering index.
    _drop_normal_index()

    # Covering index can answer from the index alone.
    # Plan type may be Index Scan or Index Only Scan depending on visibility,
    # but the index name in the plan should be the covering index.
    _print_plan(
        "Case B - covering index (check index name in plan)",
        """
        SELECT status, total_cents
        FROM support_orders
        WHERE customer_email = %s;
        """,
        (target_email,),
    )


if __name__ == "__main__":
    # Step 2:
    # Run the coverage comparison directly.
    run_covering_vs_normal_demo()

# Takeaway:
# Covering indexes can remove table lookups when the index already has what you need.
