"""
00_prereq_check.py — Prerequisite checker for the dbt micro-nuggets lane.

Checks:
  1. Python version >= 3.9
  2. dbt-core is installed
  3. Adapter package for auto-detected backend is installed
  4. Backend connectivity (socket check or DuckDB import)
  5. profiles.yml can be written to lab_dbt_project/

Prints PASS/FAIL per check with exact pip install commands for failures.

Run:
    python 00_setup/00_prereq_check.py
"""
from __future__ import annotations

import socket
import sys
from pathlib import Path

# Add parent to path so we can import _dbt_lane_connect
sys.path.insert(0, str(Path(__file__).parent.parent))

from _dbt_lane_connect import (
    check_adapter_installed,
    check_dbt_installed,
    detect_backend,
    get_adapter_package,
    write_profiles_yml,
    DBT_PROJECT_DIR,
)


def check(label: str, ok: bool, fix: str = "") -> bool:
    """Print a labelled PASS/FAIL line and return the bool."""
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] {label}")
    if not ok and fix:
        print(f"         Fix: {fix}")
    return ok


def main() -> int:
    print("=" * 60)
    print("  dbt Lane — Prerequisite Check")
    print("=" * 60)

    results = []

    # 1. Python version
    py_ok = sys.version_info >= (3, 9)
    results.append(check(
        f"Python >= 3.9  (found {sys.version.split()[0]})",
        py_ok,
        "Upgrade Python: https://www.python.org/downloads/",
    ))

    # 2. dbt-core installed
    dbt_ok = check_dbt_installed()
    try:
        import dbt.version
        dbt_ver = dbt.version.__version__
    except Exception:
        dbt_ver = "not found"
    results.append(check(
        f"dbt-core installed (found: {dbt_ver})",
        dbt_ok,
        "pip install dbt-core",
    ))

    # 3. Backend detection + adapter
    backend, reason = detect_backend()
    print(f"\n  Auto-detected backend: {backend}")
    print(f"  Reason: {reason}\n")

    adapter_ok = check_adapter_installed(backend)
    adapter_pkg = get_adapter_package(backend)
    results.append(check(
        f"Adapter '{adapter_pkg}' installed",
        adapter_ok,
        f"pip install {adapter_pkg}",
    ))

    # 4. Backend connectivity
    if backend == "duckdb":
        try:
            import duckdb  # noqa: F401
            conn_ok = True
        except ImportError:
            conn_ok = False
        results.append(check(
            "DuckDB import available",
            conn_ok,
            "pip install duckdb  (usually installed with dbt-duckdb)",
        ))
    elif backend == "postgres":
        from _dbt_lane_connect import _env
        pg_host = _env("PG_HOST", "localhost")
        pg_port = int(_env("PG_PORT", "5432"))
        try:
            with socket.create_connection((pg_host, pg_port), timeout=2):
                conn_ok = True
        except OSError:
            conn_ok = False
        results.append(check(
            f"PostgreSQL reachable at {pg_host}:{pg_port}",
            conn_ok,
            f"Start Docker: cd D:\\StudyBook\\_infra && .\\scripts\\infra_up.ps1",
        ))
    elif backend == "snowflake":
        try:
            import snowflake.connector  # noqa: F401
            conn_ok = True
        except ImportError:
            conn_ok = False
        results.append(check(
            "Snowflake connector importable",
            conn_ok,
            "pip install dbt-snowflake",
        ))
    elif backend == "databricks":
        try:
            import databricks.sdk  # noqa: F401
            conn_ok = True
        except ImportError:
            # Databricks connector might not expose sdk but dbt adapter is enough
            conn_ok = adapter_ok
        results.append(check(
            "Databricks adapter importable",
            conn_ok,
            "pip install dbt-databricks",
        ))

    # 5. profiles.yml writeable
    try:
        profiles_path = write_profiles_yml()
        profiles_ok = profiles_path.exists()
    except Exception as e:
        profiles_ok = False
        print(f"         Error writing profiles.yml: {e}")
    results.append(check(
        f"profiles.yml writable to {DBT_PROJECT_DIR}",
        profiles_ok,
        f"Check write permissions on {DBT_PROJECT_DIR}",
    ))

    # 6. dbt debug (only if dbt + adapter both OK)
    print()
    if dbt_ok and adapter_ok and profiles_ok:
        print("  Running dbt debug...")
        from _dbt_lane_connect import run_dbt
        rc, stdout, stderr = run_dbt(["debug"], timeout=60)
        debug_ok = rc == 0
        # Print last 10 lines of dbt debug output
        lines = (stdout + "\n" + stderr).strip().splitlines()
        for line in lines[-12:]:
            print(f"    {line}")
        results.append(check(
            "dbt debug passes",
            debug_ok,
            "Review output above. Most common fix: correct profiles.yml backend/credentials.",
        ))
    else:
        print("  Skipping dbt debug (dbt-core or adapter not installed).")

    # Summary
    print()
    print("=" * 60)
    all_ok = all(results)
    passed = sum(results)
    total  = len(results)
    print(f"  Result: {passed}/{total} checks passed")
    if all_ok:
        print("  STATUS: READY — run 'python 00_setup/01_seed_lab.py' next")
        print("PASS")
    else:
        print("  STATUS: NOT READY — fix the FAIL items above")
        print("FAIL")
    print("=" * 60)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
