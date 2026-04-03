#!/usr/bin/env python3
"""
Run all PostgreSQL micro-nuggets and report PASS/FAIL.

Usage:
    python run_all_postgresql_nuggets.py
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

NUGGET_DIR = Path(__file__).parent
TIMEOUT = 60  # seconds per script

# Order matters — setup first, then modules
SCRIPTS = [
    # Setup
    "00_setup/00_prereq_check.py",
    "00_setup/01_seed_lab.py",
    # SQL Core
    "01_sql_core/01_joins.py",
    "01_sql_core/02_aggregation.py",
    "01_sql_core/03_subqueries.py",
    # CTEs & Windowing
    "02_cte_and_windowing/01_ctes.py",
    "02_cte_and_windowing/02_window_functions.py",
    "02_cte_and_windowing/03_advanced_analytics.py",
    # Data Modeling
    "03_data_modeling/01_keys_and_constraints.py",
    "03_data_modeling/02_normalization.py",
    # DE Patterns
    "04_de_patterns/01_de_patterns.py",
    # Performance
    "05_performance_tuning/01_explain_and_indexes.py",
    # Transactions
    "06_transactions_and_concurrency/01_transactions.py",
    # Data Quality
    "07_data_quality_and_testing/01_data_quality.py",
    # Interview
    "08_interview_drills/01_interview_drills.py",
    # Capstone
    "09_mini_capstone/01_mini_capstone.py",
]


def safe_print(text: str) -> None:
    """Print safely on Windows consoles with non-UTF8 encodings."""
    encoding = sys.stdout.encoding or "utf-8"
    print(text.encode(encoding, errors="replace").decode(encoding, errors="replace"))


def run_script(script_path: Path) -> tuple[bool, str, float]:
    """Run a single nugget script. Returns (passed, output_snippet, elapsed)."""
    start = time.perf_counter()
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True, text=False, timeout=TIMEOUT,
            cwd=str(script_path.parent),
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        elapsed = time.perf_counter() - start
        passed = result.returncode == 0
        stdout_text = (result.stdout or b"").decode("utf-8", errors="replace")
        stderr_text = (result.stderr or b"").decode("utf-8", errors="replace")
        # Grab last 2 lines of output for the report
        output = stdout_text.strip()
        lines = output.splitlines()
        snippet = " | ".join(lines[-2:]) if lines else "(no output)"
        if stderr_text and not passed:
            err_lines = stderr_text.strip().splitlines()
            snippet = err_lines[-1][:100] if err_lines else stderr_text[:100]
        return passed, snippet, elapsed
    except subprocess.TimeoutExpired:
        elapsed = time.perf_counter() - start
        return False, f"TIMEOUT ({TIMEOUT}s)", elapsed
    except Exception as e:
        elapsed = time.perf_counter() - start
        return False, str(e)[:100], elapsed


def main():
    safe_print("=" * 70)
    safe_print("  PostgreSQL Micro-Nuggets - Full Validation")
    safe_print("=" * 70)

    results = []
    for script_rel in SCRIPTS:
        script_path = NUGGET_DIR / script_rel
        if not script_path.exists():
            results.append((script_rel, False, "FILE NOT FOUND", 0))
            continue

        passed, snippet, elapsed = run_script(script_path)
        results.append((script_rel, passed, snippet, elapsed))

    # Report
    safe_print("\n" + "-" * 70)
    safe_print(f"  {'Script':<55} {'Result':<6} {'Time':>6}")
    safe_print("-" * 70)

    passed_count = 0
    failed = []
    for script_rel, passed, snippet, elapsed in results:
        status = "PASS" if passed else "FAIL"
        if passed:
            passed_count += 1
        else:
            failed.append(script_rel)
        safe_print(f"  {script_rel:<55} {status:<6} {elapsed:>5.1f}s")
        if not passed:
            safe_print(f"    -> {snippet}")

    safe_print("-" * 70)
    safe_print(f"  Total: {len(results)}  |  Passed: {passed_count}  |  Failed: {len(failed)}")
    safe_print("=" * 70)

    if failed:
        safe_print("\n  Failed scripts:")
        for f in failed:
            safe_print(f"    - {f}")
        sys.exit(1)
    else:
        safe_print("\n  All nuggets passed! [OK]")
        sys.exit(0)


if __name__ == "__main__":
    main()
