# Story:
# This file shows what an Index Only Scan looks like.
# It matters because coverage can avoid table reads.
# Expect Index Only Scan when visibility map allows it.

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


def _setup_inventory():
    session = _open_connection()
    try:
        with session.cursor() as cur:
            # Step 1:
            # Reset the table so the demo is rerunnable.
            cur.execute("DROP TABLE IF EXISTS inventory;")
            cur.execute(
                """
                CREATE TABLE inventory (
                    id SERIAL PRIMARY KEY,
                    sku TEXT NOT NULL,
                    warehouse TEXT NOT NULL,
                    on_hand INTEGER NOT NULL,
                    updated_at TIMESTAMP NOT NULL
                );
                """
            )
            cur.execute(
                """
                CREATE INDEX inventory_sku_cover_idx
                ON inventory (sku)
                INCLUDE (warehouse, on_hand);
                """
            )

            rows = []
            warehouses = ["A1", "B2", "C3", "D4"]
            for i in range(20000):
                sku = f"SKU-{i:05d}"
                warehouse = warehouses[i % len(warehouses)]
                on_hand = 10 + (i % 50)
                updated_at = "2024-06-{:02d} {:02d}:00:00".format(
                    (i % 28) + 1,
                    i % 24,
                )
                rows.append((sku, warehouse, on_hand, updated_at))

            cur.executemany(
                """
                INSERT INTO inventory (sku, warehouse, on_hand, updated_at)
                VALUES (%s, %s, %s, %s);
                """,
                rows,
            )
            cur.execute("ANALYZE inventory;")
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


def run_index_only_scan_demo():
    # Step 0:
    # Reset data and build the covering index.
    _setup_inventory()

    # Optional:
    # Index Only Scan depends on the visibility map.
    # If you see an Index Scan with heap fetches, run VACUUM and try again.
    _print_plan(
        "Index-only scan demo (look for Index Only Scan; heap fetches may appear)",
        """
        SELECT warehouse, on_hand
        FROM inventory
        WHERE sku = %s;
        """,
        ("SKU-15000",),
    )


if __name__ == "__main__":
    # Step 1:
    # Run the index-only scan demo directly.
    run_index_only_scan_demo()

# Takeaway:
# Index-only scans are possible when the index covers all needed columns and pages are visible.
