#!/usr/bin/env python3
"""
Run all Databricks Bridge micro-nuggets and report PASS/FAIL.

Usage:
    python run_all_databricks_bridge_nuggets.py

Options (positional-style env vars for simplicity):
    BRIDGE_STOP_ON_FAIL=1  -- stop after first failure
    BRIDGE_TIMEOUT=120     -- per-script timeout in seconds (default 120)

Windows PowerShell:
    $env:BRIDGE_STOP_ON_FAIL=1
    python run_all_databricks_bridge_nuggets.py
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

NUGGET_DIR = Path(__file__).parent
TIMEOUT = int(os.getenv("BRIDGE_TIMEOUT", "120"))
STOP_ON_FAIL = os.getenv("BRIDGE_STOP_ON_FAIL", "0") == "1"

# Deterministic script order: setup first, then modules, capstone last
SCRIPTS = [
    # ── Setup and seeding ──────────────────────────────────────────────
    "00_setup/00_prereq_check.py",
    "00_setup/01_seed_lab.py",
    # ── SQL Foundations ────────────────────────────────────────────────
    "01_sql_foundations/01_joins.py",
    "01_sql_foundations/02_aggregation_and_having.py",
    "01_sql_foundations/03_subqueries.py",
    # ── CTE and Windowing ──────────────────────────────────────────────
    "02_cte_and_windowing/01_ctes.py",
    "02_cte_and_windowing/02_window_functions.py",
    "02_cte_and_windowing/03_advanced_analytics.py",
    # ── Delta Core ────────────────────────────────────────────────────
    "03_delta_core/01_acid_and_transactions.py",
    "03_delta_core/02_schema_enforcement_evolution.py",
    "03_delta_core/03_time_travel.py",
    "03_delta_core/04_optimize_and_zorder.py",
    # ── DE Patterns ───────────────────────────────────────────────────
    "04_de_patterns/01_deduplication.py",
    "04_de_patterns/02_merge_upsert.py",
    "04_de_patterns/03_scd_type2.py",
    "04_de_patterns/04_incremental_and_late_events.py",
    # ── Performance ───────────────────────────────────────────────────
    "05_performance_and_optimization/01_explain_and_profiling.py",
    "05_performance_and_optimization/02_partitioning_strategy.py",
    # ── Governance ────────────────────────────────────────────────────
    "06_governance_and_security/01_unity_catalog_and_grants.py",
    # ── Data Quality ──────────────────────────────────────────────────
    "07_data_quality_and_testing/01_data_quality_checks.py",
    # ── Interview Drills ──────────────────────────────────────────────
    "08_interview_drills/01_interview_drills.py",
    # ── Capstone (always last) ─────────────────────────────────────────
    "09_mini_capstone/01_mini_capstone.py",
]


def safe_print(text: str) -> None:
    """Print safely on Windows consoles with non-UTF8 encodings."""
    encoding = sys.stdout.encoding or "utf-8"
    try:
        print(text.encode(encoding, errors="replace").decode(encoding, errors="replace"))
    except Exception:
        print(text.encode("ascii", errors="replace").decode("ascii"))


def run_script(script_path: Path) -> tuple[bool, str, float]:
    """
    Run a single nugget script as a subprocess.
    Returns (passed, output_snippet, elapsed_seconds).
    """
    start = time.perf_counter()
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=False,
            timeout=TIMEOUT,
            cwd=str(script_path.parent),
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        elapsed = time.perf_counter() - start
        passed = result.returncode == 0

        stdout_text = (result.stdout or b"").decode("utf-8", errors="replace")
        stderr_text = (result.stderr or b"").decode("utf-8", errors="replace")

        # Build output snippet for the report
        lines = stdout_text.strip().splitlines()
        snippet = " | ".join(lines[-2:]) if lines else "(no output)"

        # For failures, prefer the last stderr line (usually the error message)
        if not passed and stderr_text.strip():
            err_lines = stderr_text.strip().splitlines()
            # Find the most informative line (avoid boilerplate traceback lines)
            for line in reversed(err_lines):
                line = line.strip()
                if line and not line.startswith("Traceback") and not line.startswith("File "):
                    snippet = line[:100]
                    break

        return passed, snippet, elapsed

    except subprocess.TimeoutExpired:
        elapsed = time.perf_counter() - start
        return False, f"TIMEOUT after {TIMEOUT}s", elapsed
    except Exception as exc:
        elapsed = time.perf_counter() - start
        return False, str(exc)[:100], elapsed


def main() -> None:
    safe_print("")
    safe_print("=" * 72)
    safe_print("  Databricks Bridge -- Full Nugget Validation Run")
    safe_print(f"  Scripts: {len(SCRIPTS)}  |  Timeout per script: {TIMEOUT}s")
    safe_print("=" * 72)

    row_data: list[tuple[str, bool, str, float]] = []

    for script_rel in SCRIPTS:
        script_path = NUGGET_DIR / script_rel

        if not script_path.exists():
            row_data.append((script_rel, False, "FILE NOT FOUND", 0.0))
            safe_print(f"  FAIL  {script_rel}")
            safe_print(f"    -> FILE NOT FOUND")
            if STOP_ON_FAIL:
                break
            continue

        safe_print(f"  RUN   {script_rel} ...")
        passed, snippet, elapsed = run_script(script_path)
        row_data.append((script_rel, passed, snippet, elapsed))

        status = "PASS" if passed else "FAIL"
        safe_print(f"  {status:<4}  {script_rel:<55} {elapsed:>5.1f}s")
        if not passed:
            safe_print(f"    -> {snippet}")
            if STOP_ON_FAIL:
                safe_print("")
                safe_print("  BRIDGE_STOP_ON_FAIL=1: stopping after first failure.")
                break

    # ── Final report ──────────────────────────────────────────────────────
    safe_print("")
    safe_print("-" * 72)
    safe_print(f"  {'Script':<55} {'Status':<6} {'Time':>6}")
    safe_print("-" * 72)

    passed_count = 0
    failed_scripts: list[str] = []

    for script_rel, passed, snippet, elapsed in row_data:
        status = "PASS" if passed else "FAIL"
        if passed:
            passed_count += 1
        else:
            failed_scripts.append(script_rel)
        safe_print(f"  {script_rel:<55} {status:<6} {elapsed:>5.1f}s")
        if not passed:
            safe_print(f"    -> {snippet}")

    total = len(row_data)
    safe_print("-" * 72)
    safe_print(f"  Total: {total}  |  Passed: {passed_count}  |  Failed: {len(failed_scripts)}")
    safe_print("=" * 72)
    safe_print("")

    if failed_scripts:
        safe_print("  Failed scripts:")
        for f in failed_scripts:
            safe_print(f"    - {f}")
        safe_print("")
        sys.exit(1)
    else:
        safe_print("  All nuggets passed! [OK]")
        safe_print("")
        sys.exit(0)


if __name__ == "__main__":
    main()
