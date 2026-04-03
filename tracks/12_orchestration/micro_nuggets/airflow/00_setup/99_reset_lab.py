"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 00-99 · Reset Lab Environment                                        ║
║  Removes all lab-created Variables and Connections.                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Cleans up everything created by 01_seed_lab.py:
  - Removes all lab_airflow_* Variables
  - Removes all lab_airflow_* Connections

Requires --confirm flag to prevent accidental deletion.

USAGE
─────
    python 99_reset_lab.py --confirm
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _airflow_connect import (
    LAB_VARIABLES, LAB_CONNECTIONS, LAB_PREFIX,
    delete_variable, get_variables,
    delete_connection, get_connections,
    check_airflow_reachable,
)


def main():
    parser = argparse.ArgumentParser(description="Reset Airflow lab environment.")
    parser.add_argument(
        "--confirm", action="store_true",
        help="Required to actually delete lab objects.",
    )
    args = parser.parse_args()

    if not args.confirm:
        print("\n  Usage: python 99_reset_lab.py --confirm")
        print("  This will delete all lab_airflow_* Variables and Connections.")
        sys.exit(0)

    print("\n-- Reset Lab Environment ---------------------------------")

    reachable, ver = check_airflow_reachable(timeout=8)
    if not reachable:
        print(f"  [FAIL] Airflow not reachable: {ver}")
        print("  Skipping API cleanup (Airflow offline).")
    else:
        print(f"  [OK] Airflow {ver} reachable.")

        # Delete lab variables
        print("\n  Deleting lab variables...")
        existing_vars = get_variables()
        deleted = 0
        for key in list(LAB_VARIABLES.keys()):
            if key in existing_vars:
                delete_variable(key)
                print(f"    Deleted: {key}")
                deleted += 1
            else:
                print(f"    Not found (skipped): {key}")
        print(f"    Variables deleted: {deleted}")

        # Delete lab connections
        print("\n  Deleting lab connections...")
        existing_conns = {c["connection_id"] for c in get_connections()}
        deleted_c = 0
        for conn_id in LAB_CONNECTIONS:
            if conn_id in existing_conns:
                delete_connection(conn_id)
                print(f"    Deleted: {conn_id}")
                deleted_c += 1
            else:
                print(f"    Not found (skipped): {conn_id}")
        print(f"    Connections deleted: {deleted_c}")

    print("\n  Lab reset complete.")
    print(f"  To recreate: python 01_seed_lab.py")
    print()


if __name__ == "__main__":
    main()
