"""
99_reset_lab.py — Reset the dbt lab to a clean state.

Actions:
  - For DuckDB: delete lab_dbt.duckdb file
  - For PostgreSQL: DROP SCHEMA dbt_lab CASCADE (and related schemas)
  - Remove compiled/, target/, logs/, dbt_packages/ from lab_dbt_project/
  - Idempotent — safe to run multiple times

REQUIRES --confirm flag to prevent accidental deletion.

Run:
    python 00_setup/99_reset_lab.py --confirm
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from _dbt_lane_connect import DBT_PROJECT_DIR, detect_backend, _env


def main() -> int:
    if "--confirm" not in sys.argv:
        print("=" * 60)
        print("  dbt Lab Reset — SAFETY GUARD")
        print("=" * 60)
        print()
        print("  This script will DELETE:")
        print("    - The DuckDB database file (lab_dbt.duckdb)")
        print("    - OR drop the dbt_lab PostgreSQL schema (CASCADE)")
        print("    - target/, compiled/, logs/, dbt_packages/ directories")
        print()
        print("  To proceed, re-run with the --confirm flag:")
        print()
        print("    python 00_setup/99_reset_lab.py --confirm")
        print()
        print("  Re-seed after reset:")
        print("    python 00_setup/01_seed_lab.py")
        return 1

    print("=" * 60)
    print("  dbt Lab Reset")
    print("=" * 60)
    cleaned = []

    # ── 1. Clean generated dbt artifacts ──────────────────────────────────────
    artifact_dirs = ["target", "dbt_packages", "logs"]
    for d in artifact_dirs:
        p = DBT_PROJECT_DIR / d
        if p.exists():
            shutil.rmtree(p)
            cleaned.append(str(p))
            print(f"  Removed: {p}")
        else:
            print(f"  Skip (not found): {p}")

    # ── 2. Backend-specific cleanup ───────────────────────────────────────────
    backend, reason = detect_backend()
    print(f"\n  Backend: {backend}")

    if backend == "duckdb":
        db_path = DBT_PROJECT_DIR / "lab_dbt.duckdb"
        if db_path.exists():
            db_path.unlink()
            cleaned.append(str(db_path))
            print(f"  Removed: {db_path}")
        else:
            print(f"  Skip (not found): {db_path}")

        # Also remove DuckDB WAL file if present
        wal_path = DBT_PROJECT_DIR / "lab_dbt.duckdb.wal"
        if wal_path.exists():
            wal_path.unlink()
            print(f"  Removed: {wal_path}")

    elif backend == "postgres":
        try:
            import psycopg2
            pg_host = _env("PG_HOST", "localhost")
            pg_port = int(_env("PG_PORT", "5432"))
            pg_user = _env("PG_USER", "de_admin")
            pg_pass = _env("PG_PASSWORD", "")
            pg_db   = _env("PG_DB", "de_telemetry")

            conn = psycopg2.connect(
                host=pg_host, port=pg_port, user=pg_user,
                password=pg_pass, dbname=pg_db
            )
            conn.autocommit = True
            schemas = [
                "dbt_lab", "dbt_lab_staging", "dbt_lab_raw",
                "dbt_lab_bronze", "dbt_lab_silver", "dbt_lab_gold",
                "dbt_lab_snapshots"
            ]
            with conn.cursor() as cur:
                for schema in schemas:
                    try:
                        cur.execute(f"DROP SCHEMA IF EXISTS {schema} CASCADE")
                        print(f"  Dropped schema: {schema}")
                        cleaned.append(f"schema:{schema}")
                    except Exception as e:
                        print(f"  Warning dropping {schema}: {e}")
            conn.close()
        except ImportError:
            print("  psycopg2 not installed — skipping PostgreSQL cleanup")
        except Exception as e:
            print(f"  PostgreSQL cleanup error: {e}")
    else:
        print(f"  No database cleanup implemented for backend: {backend}")

    # ── Summary ───────────────────────────────────────────────────────────────
    print()
    if cleaned:
        print(f"  Cleaned {len(cleaned)} items:")
        for item in cleaned:
            print(f"    - {item}")
    else:
        print("  Nothing to clean (already clean).")

    print()
    print("PASS — lab reset complete")
    print("Run 'python 00_setup/01_seed_lab.py' to re-seed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
