# Story:
# This demo shows how Postgres uses cost estimates to pick a plan.
# The planner guesses row counts from stats and chooses the lowest-cost path.

import re
from pathlib import Path

import psycopg2


ROW_COUNT = 120000


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
            cur.execute("DROP TABLE IF EXISTS events_cost;")
            cur.execute(
                """
                CREATE TABLE events_cost (
                    id BIGSERIAL PRIMARY KEY,
                    category TEXT NOT NULL,
                    region TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    payload_text TEXT NOT NULL
                );
                """
            )
            cur.execute("ALTER TABLE events_cost SET (autovacuum_enabled = false);")

            rows = []
            regions = ["us", "eu", "apac", "latam"]
            payload_base = "x" * 300

            for i in range(ROW_COUNT):
                mod = i % 100
                if mod == 0:
                    category = "cold"
                elif mod < 10:
                    category = "warm"
                else:
                    category = "hot"

                region = regions[i % len(regions)]
                score = (i % 1000) - 500
                payload_text = f"{payload_base}{i % 1000}"
                rows.append((category, region, score, payload_text))

            cur.executemany(
                """
                INSERT INTO events_cost (
                    category,
                    region,
                    score,
                    payload_text
                )
                VALUES (%s, %s, %s, %s);
                """,
                rows,
            )

            cur.execute("CREATE INDEX events_cost_category_idx ON events_cost (category);")
        session.commit()
    finally:
        session.close()


def _analyze():
    session = _open_connection()
    try:
        with session.cursor() as cur:
            cur.execute("ANALYZE events_cost;")
        session.commit()
    finally:
        session.close()


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


def _extract_scan_stats(plan_lines):
    for line in plan_lines:
        if "events_cost" not in line or "Scan" not in line:
            continue
        matches = re.findall(r"rows=(\d+)", line)
        if len(matches) >= 2:
            return int(matches[0]), int(matches[1]), line.strip()
        if len(matches) == 1:
            return int(matches[0]), None, line.strip()
    return None, None, None


def _run_scenario(label, sql, params=None):
    plan_lines = _explain(sql, params)
    est_rows, actual_rows, node = _extract_scan_stats(plan_lines)

    print("=" * 72)
    print(label)
    for line in plan_lines:
        print(line)

    if node:
        print("Plan node:", node)
    if est_rows is not None:
        print("Estimated rows:", est_rows)
    if actual_rows is not None:
        print("Actual rows:", actual_rows)

    return {
        "node": node,
        "est_rows": est_rows,
        "actual_rows": actual_rows,
    }


def _estimate_error(summary):
    est = summary.get("est_rows")
    actual = summary.get("actual_rows")
    if est is None or actual is None:
        return None
    return abs(est - actual)


def run_cost_model_demo():
    _setup_table()

    print("Cost model demo: skewed data + index on category.")

    print("\nBefore ANALYZE (stats are default)")
    scenario_a_before = _run_scenario(
        "Scenario A - selective predicate (category = cold)",
        "SELECT count(*) FROM events_cost WHERE category = %s;",
        ("cold",),
    )
    scenario_b_before = _run_scenario(
        "Scenario B - non-selective predicate (category = hot)",
        "SELECT count(*) FROM events_cost WHERE category = %s;",
        ("hot",),
    )

    print("\nRunning ANALYZE...")
    _analyze()

    print("\nAfter ANALYZE (stats refreshed)")
    scenario_a_after = _run_scenario(
        "Scenario A - selective predicate (category = cold)",
        "SELECT count(*) FROM events_cost WHERE category = %s;",
        ("cold",),
    )
    scenario_b_after = _run_scenario(
        "Scenario B - non-selective predicate (category = hot)",
        "SELECT count(*) FROM events_cost WHERE category = %s;",
        ("hot",),
    )

    print("=" * 72)
    print("Summary")
    print("Scenario A plan before:", scenario_a_before["node"])
    print("Scenario A plan after:", scenario_a_after["node"])
    print("Scenario B plan before:", scenario_b_before["node"])
    print("Scenario B plan after:", scenario_b_after["node"])

    error_a_before = _estimate_error(scenario_a_before)
    error_a_after = _estimate_error(scenario_a_after)
    error_b_before = _estimate_error(scenario_b_before)
    error_b_after = _estimate_error(scenario_b_after)

    print("Scenario A estimate error before:", error_a_before)
    print("Scenario A estimate error after:", error_a_after)
    print("Scenario B estimate error before:", error_b_before)
    print("Scenario B estimate error after:", error_b_after)

    if error_a_before is not None and error_a_after is not None:
        if error_a_after < error_a_before:
            print("Scenario A: ANALYZE improved the estimate.")
        else:
            print("Scenario A: estimate did not improve much.")

    if error_b_before is not None and error_b_after is not None:
        if error_b_after < error_b_before:
            print("Scenario B: ANALYZE improved the estimate.")
        else:
            print("Scenario B: estimate did not improve much.")

    if scenario_a_after["node"] and scenario_b_after["node"]:
        if "Index" in scenario_a_after["node"] and "Seq Scan" in scenario_b_after["node"]:
            print("Planner chose different paths for selective vs broad predicates.")


if __name__ == "__main__":
    run_cost_model_demo()

# Takeaway:
# The planner is guessing the cheapest path. Stats decide how good the guess is.
