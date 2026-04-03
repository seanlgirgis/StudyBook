"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 00-01 · Seed Lab Environment                                         ║
║  Creates Airflow Variables, Connections, and output path config.             ║
║  IDEMPOTENT — safe to run multiple times.                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Sets up everything the nuggets depend on:
  - Airflow Variables  (lab_airflow_*)
  - Airflow Connections  (lab_airflow_postgres, lab_airflow_filesystem)
  - Output path variable for DAG artifact outputs (runtime/container scoped)

USAGE
─────
    python 01_seed_lab.py          # Create/update lab objects
    python 01_seed_lab.py --reset  # Delete lab objects then recreate
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _airflow_connect import (
    LAB_VARIABLES, LAB_CONNECTIONS, LAB_PREFIX,
    set_variable, delete_variable, get_variables,
    upsert_connection, delete_connection, get_connections,
    check_airflow_reachable,
)


def check_ready(strict: bool = False):
    reachable = False
    ver = ""
    for attempt in range(1, 6):
        reachable, ver = check_airflow_reachable(timeout=8)
        if reachable:
            break
        if attempt < 5:
            time.sleep(3)

    if not reachable:
        tag = "FAIL" if strict else "SKIP"
        print(f"  [{tag}] Airflow not reachable: {ver}")
        print("  Fix: pwsh D:\\StudyBook\\_infra\\scripts\\infra_up.ps1 -Group pipeline")
        if strict:
            sys.exit(1)
        print("  [SKIP] Seed skipped because Airflow API is not reachable yet.")
        sys.exit(0)
    print(f"  [OK] Airflow {ver} reachable.")


def create_output_dir():
    """
    Document output dir semantics.
    Output path is container-side and configured via lab variable/connection.
    """
    out_dir = LAB_VARIABLES.get(f"{LAB_PREFIX}_output_dir", "/tmp/airflow_lab")
    print(f"    Output dir variable set to: {out_dir}  [OK]")
    print("    Note: this path is resolved inside Airflow runtime context.")


def delete_lab_variables():
    print("\n  Deleting lab variables...")
    existing = get_variables()
    for key in list(LAB_VARIABLES.keys()):
        if key in existing:
            delete_variable(key)
            print(f"    Deleted variable: {key}")


def create_lab_variables():
    print("\n  Creating lab variables...")
    existing = get_variables()
    for key, value in LAB_VARIABLES.items():
        set_variable(key, value)
        action = "updated" if key in existing else "created"
        print(f"    {action}: {key} = {value!r}")


def delete_lab_connections():
    print("\n  Deleting lab connections...")
    existing_ids = {c["connection_id"] for c in get_connections()}
    for conn_id in LAB_CONNECTIONS:
        if conn_id in existing_ids:
            delete_connection(conn_id)
            print(f"    Deleted connection: {conn_id}")


def create_lab_connections():
    print("\n  Creating lab connections...")
    existing_ids = {c["connection_id"] for c in get_connections()}
    for conn_id, conn_body in LAB_CONNECTIONS.items():
        upsert_connection(conn_id, conn_body)
        action = "updated" if conn_id in existing_ids else "created"
        print(f"    {action}: {conn_id}  (type={conn_body.get('conn_type')})")


def main():
    parser = argparse.ArgumentParser(description="Seed Airflow lab environment.")
    parser.add_argument("--reset", action="store_true", help="Delete lab objects then recreate.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero when Airflow API is unreachable.",
    )
    args = parser.parse_args()

    print("\n-- Seed Lab Environment ----------------------------------")

    check_ready(strict=args.strict)

    if args.reset:
        print("\n  Resetting lab environment...")
        delete_lab_variables()
        delete_lab_connections()

    create_lab_variables()
    create_lab_connections()
    create_output_dir()

    print(f"\n  Lab environment ready!  Prefix: {LAB_PREFIX}")
    print(f"  Variables: {len(LAB_VARIABLES)}")
    print(f"  Connections: {len(LAB_CONNECTIONS)}")
    print()


if __name__ == "__main__":
    main()
