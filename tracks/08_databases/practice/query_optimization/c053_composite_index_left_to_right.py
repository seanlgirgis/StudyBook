# Story:
# This file shows the left-to-right rule for composite indexes.
# It matters because the same index can be great for one query and weak for another.
# Expect index usage when the leftmost column is used.

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


def _setup_contacts():
    session = _open_connection()
    try:
        with session.cursor() as cur:
            # Step 1:
            # Reset the table so the demo is rerunnable.
            cur.execute("DROP TABLE IF EXISTS customer_contacts;")
            cur.execute(
                """
                CREATE TABLE customer_contacts (
                    id SERIAL PRIMARY KEY,
                    last_name TEXT NOT NULL,
                    first_name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    city TEXT NOT NULL
                );
                """
            )
            cur.execute(
                """
                CREATE INDEX customer_contacts_last_first_idx
                ON customer_contacts (last_name, first_name);
                """
            )

            last_names = [
                "Smith",
                "Johnson",
                "Lee",
                "Brown",
                "Garcia",
                "Davis",
                "Miller",
                "Wilson",
                "Martinez",
                "Taylor",
            ]
            first_names = [
                "Ava",
                "Noah",
                "Mia",
                "Liam",
                "Zoe",
                "Ethan",
                "Sofia",
                "Mason",
                "Chloe",
                "Lucas",
            ]
            cities = ["Austin", "Denver", "Chicago", "Seattle", "Boston"]

            rows = []
            for i in range(30000):
                last_name = last_names[i % len(last_names)]
                first_name = first_names[
                    (i // len(last_names)) % len(first_names)
                ]
                email = f"{first_name.lower()}.{last_name.lower()}{i}@example.com"
                city = cities[i % len(cities)]
                rows.append((last_name, first_name, email, city))

            cur.executemany(
                """
                INSERT INTO customer_contacts (last_name, first_name, email, city)
                VALUES (%s, %s, %s, %s);
                """,
                rows,
            )
            cur.execute("ANALYZE customer_contacts;")
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


def run_left_to_right_demo():
    # Step 0:
    # Reset data so the planner has correct stats.
    _setup_contacts()

    target_last = "Smith"
    target_first = "Ava"

    # Case A:
    # Leftmost column only: should use the composite index.
    _print_plan(
        "Case A - WHERE last_name = 'Smith' (expect Index Scan)",
        "SELECT * FROM customer_contacts WHERE last_name = %s;",
        (target_last,),
    )

    # Case B:
    # Left + right: best case for the composite index.
    _print_plan(
        "Case B - WHERE last_name = 'Smith' AND first_name = 'Ava' (expect Index Scan)",
        """
        SELECT * FROM customer_contacts
        WHERE last_name = %s AND first_name = %s;
        """,
        (target_last, target_first),
    )

    # Case C:
    # Rightmost column only: weak or unusable for the index.
    _print_plan(
        "Case C - WHERE first_name = 'Ava' (expect Seq Scan or poor index use)",
        "SELECT * FROM customer_contacts WHERE first_name = %s;",
        (target_first,),
    )


if __name__ == "__main__":
    # Step 3:
    # Run the left-to-right demo directly.
    run_left_to_right_demo()

# Takeaway:
# Composite indexes work left-to-right. Missing the leftmost column weakens the index.
