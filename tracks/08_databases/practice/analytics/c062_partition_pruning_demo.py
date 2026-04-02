# Story:
# This demo shows partition pruning in Postgres.
# Partitioning splits one table into labeled chunks by date.
# Pruning skips entire partitions before reading rows.

import re
from pathlib import Path

import psycopg2


PARTITION_MONTHS = [
    ("2024-01-01", "2024-02-01"),
    ("2024-02-01", "2024-03-01"),
    ("2024-03-01", "2024-04-01"),
    ("2024-04-01", "2024-05-01"),
    ("2024-05-01", "2024-06-01"),
    ("2024-06-01", "2024-07-01"),
]


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


def _setup_partitioned_table():
    session = _open_connection()
    try:
        with session.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS events_partitioned CASCADE;")
            cur.execute(
                """
                DO $$
                BEGIN
                    IF EXISTS (SELECT 1 FROM pg_type WHERE typname = 'events_partitioned') THEN
                        DROP TYPE events_partitioned;
                    END IF;
                END $$;
                """
            )
            cur.execute(
                """
                CREATE TABLE events_partitioned (
                    id BIGSERIAL NOT NULL,
                    user_id INTEGER NOT NULL,
                    event_type TEXT NOT NULL,
                    ts TIMESTAMP NOT NULL,
                    value INTEGER NOT NULL
                )
                PARTITION BY RANGE (ts);
                """
            )

            partitions = []
            for start, end in PARTITION_MONTHS:
                month_label = start[:7].replace("-", "_")
                name = f"events_partitioned_{month_label}"
                partitions.append(name)
                cur.execute(
                    f"""
                    CREATE TABLE {name}
                    PARTITION OF events_partitioned
                    FOR VALUES FROM ('{start}') TO ('{end}');
                    """
                )

            rows = []
            event_types = ["page_view", "purchase", "signup", "support_ticket"]
            rows_per_month = 12000
            for month_index, (start, _) in enumerate(PARTITION_MONTHS):
                year, month, _ = start.split("-")
                for i in range(rows_per_month):
                    user_id = (i % 5000) + 1 + (month_index * 3)
                    event_type = event_types[i % len(event_types)]
                    day = (i % 28) + 1
                    hour = i % 24
                    ts = f"{year}-{month}-{day:02d} {hour:02d}:00:00"
                    value = (i % 1000) * 3
                    rows.append((user_id, event_type, ts, value))

            cur.executemany(
                """
                INSERT INTO events_partitioned (
                    user_id,
                    event_type,
                    ts,
                    value
                )
                VALUES (%s, %s, %s, %s);
                """,
                rows,
            )

            cur.execute("ANALYZE events_partitioned;")
        session.commit()
    finally:
        session.close()

    return partitions


def _explain(sql, params=None):
    session = _open_connection()
    try:
        with session.cursor() as cur:
            cur.execute(f"EXPLAIN (ANALYZE, BUFFERS) {sql}", params or ())
            rows = cur.fetchall()
        session.commit()
    finally:
        session.close()

    return [line for (line,) in rows]


def _extract_partitions(plan_lines):
    pattern = re.compile(r"on (events_partitioned_\d{4}_\d{2})")
    found = []
    for line in plan_lines:
        match = pattern.search(line)
        if match:
            found.append(match.group(1))
    return sorted(set(found))


def _print_plan(label, sql, params=None, total_partitions=None):
    plan_lines = _explain(sql, params)
    partitions = _extract_partitions(plan_lines)

    print("=" * 72)
    print(label)
    for line in plan_lines:
        print(line)

    if total_partitions is not None:
        print("Partitions touched:", len(partitions), "of", total_partitions)
        if partitions:
            print("Touched list:", ", ".join(partitions))
        else:
            print("Touched list: none (unexpected)")

    return partitions


def run_partition_pruning_demo():
    partitions = _setup_partitioned_table()
    total_partitions = len(partitions)

    print("Partition pruning demo: partitioned by ts (monthly).")

    scenario_a = _print_plan(
        "Scenario A - filter on partition key (March 2024)",
        "SELECT count(*) FROM events_partitioned WHERE ts >= %s AND ts < %s;",
        ("2024-03-01", "2024-04-01"),
        total_partitions,
    )

    scenario_b = _print_plan(
        "Scenario B - no partition filter (user_id only)",
        "SELECT count(*) FROM events_partitioned WHERE user_id < %s;",
        (2000,),
        total_partitions,
    )

    scenario_c = _print_plan(
        "Scenario C - partition key hidden in a function",
        "SELECT count(*) FROM events_partitioned WHERE to_char(ts, 'YYYY-MM') = %s;",
        ("2024-03",),
        total_partitions,
    )

    print("=" * 72)
    print("Summary")
    print("Scenario A partitions:", len(scenario_a))
    print("Scenario B partitions:", len(scenario_b))
    print("Scenario C partitions:", len(scenario_c))

    if len(scenario_a) < len(scenario_b):
        print("Pruning benefit: Scenario A touched fewer partitions than B.")
    else:
        print("Pruning benefit: not observed (check plan output).")

    if len(scenario_c) >= len(scenario_b):
        print("Scenario C: pruning likely failed due to hidden key.")
    elif len(scenario_c) == len(scenario_a):
        print("Scenario C: planner still pruned (engine was smarter this time).")
    else:
        print("Scenario C: partial pruning observed.")


if __name__ == "__main__":
    run_partition_pruning_demo()

# Takeaway:
# Filter on the partition key to let the engine skip entire partitions.
