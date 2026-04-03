#!/usr/bin/env python3
"""
Run all Airflow micro-nuggets and report PASS/FAIL.

Usage:
    python run_all_airflow_nuggets.py

Environment variables:
    AIRFLOW_TIMEOUT       seconds per script (default: 60)
    AIRFLOW_STOP_ON_FAIL  set to "1" to stop on first failure
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

NUGGET_DIR = Path(__file__).parent
TIMEOUT = int(os.getenv("AIRFLOW_TIMEOUT", "60"))
STOP_ON_FAIL = os.getenv("AIRFLOW_STOP_ON_FAIL", "0") == "1"
AIRFLOW_HOME_DIR = NUGGET_DIR / "_lab" / "airflow_home"

# Order matters — setup first, then modules
SCRIPTS = [
    # Setup
    "00_setup/00_prereq_check.py",
    "00_setup/01_seed_lab.py",
    # DAG Basics
    "01_dag_basics/01_taskflow_api.py",
    "01_dag_basics/02_python_bash_operators.py",
    "01_dag_basics/03_dag_params_and_templating.py",
    "01_dag_basics/04_xcom_fundamentals.py",
    # Dependencies & Scheduling
    "02_dependencies_and_scheduling/01_dependency_graphs.py",
    "02_dependencies_and_scheduling/02_scheduling_and_catchup.py",
    "02_dependencies_and_scheduling/03_sensors.py",
    # Retries, SLAs, Alerting
    "03_retries_slas_and_alerting/01_retries_and_backoff.py",
    "03_retries_slas_and_alerting/02_sla_and_timeouts.py",
    # Data Pipeline Patterns
    "04_data_pipeline_patterns/01_etl_pattern.py",
    "04_data_pipeline_patterns/02_branching_and_shortcircuit.py",
    # Operations & Observability
    "05_operations_and_observability/01_dag_run_lifecycle.py",
    # Interview Drills
    "06_interview_drills/01_interview_drills.py",
    # Mini Capstone
    "07_mini_capstone/01_mini_capstone.py",
]


def safe_print(text: str) -> None:
    """Print safely on Windows consoles with non-UTF8 encodings."""
    encoding = sys.stdout.encoding or "utf-8"
    print(text.encode(encoding, errors="replace").decode(encoding, errors="replace"))


def run_script(script_path: Path) -> tuple[str, str, float]:
    """
    Run a single nugget script.
    Returns (status, output_snippet, elapsed) where status is PASS|FAIL|SKIP.
    """
    start = time.perf_counter()
    try:
        AIRFLOW_HOME_DIR.mkdir(parents=True, exist_ok=True)
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True, text=False, timeout=TIMEOUT,
            cwd=str(script_path.parent),
            env={
                **os.environ,
                "PYTHONIOENCODING": "utf-8",
                # Avoid warnings promoted to errors by inherited shell flags.
                "PYTHONWARNINGS": "default",
                # Avoid permission issues from default %USERPROFILE%\\airflow.
                "AIRFLOW_HOME": str(AIRFLOW_HOME_DIR),
            },
        )
        elapsed = time.perf_counter() - start
        passed = result.returncode == 0
        stdout_text = (result.stdout or b"").decode("utf-8", errors="replace")
        stderr_text = (result.stderr or b"").decode("utf-8", errors="replace")
        output = stdout_text.strip()
        lines = output.splitlines()
        snippet = " | ".join(lines[-2:]) if lines else "(no output)"
        if "[SKIP]" in stdout_text or "[SKIP]" in stderr_text:
            return "SKIP", snippet, elapsed
        if stderr_text and not passed:
            err_lines = stderr_text.strip().splitlines()
            snippet = err_lines[-1][:120] if err_lines else stderr_text[:120]
        return ("PASS" if passed else "FAIL"), snippet, elapsed
    except subprocess.TimeoutExpired:
        elapsed = time.perf_counter() - start
        return "FAIL", f"TIMEOUT ({TIMEOUT}s)", elapsed
    except Exception as e:
        elapsed = time.perf_counter() - start
        return "FAIL", str(e)[:120], elapsed


def main():
    safe_print("=" * 70)
    safe_print("  Airflow Micro-Nuggets - Full Validation")
    safe_print("=" * 70)
    safe_print(f"  Nugget dir : {NUGGET_DIR}")
    safe_print(f"  Scripts    : {len(SCRIPTS)}")
    safe_print(f"  Timeout    : {TIMEOUT}s per script")
    safe_print(f"  Stop-on-fail: {STOP_ON_FAIL}")
    safe_print("")

    results = []
    for script_rel in SCRIPTS:
        script_path = NUGGET_DIR / script_rel
        if not script_path.exists():
            results.append((script_rel, "FAIL", "FILE NOT FOUND", 0.0))
            if STOP_ON_FAIL:
                break
            continue

        safe_print(f"  Running: {script_rel}")
        status, snippet, elapsed = run_script(script_path)
        results.append((script_rel, status, snippet, elapsed))

        if status == "FAIL" and STOP_ON_FAIL:
            safe_print(f"    FAILED — stopping (AIRFLOW_STOP_ON_FAIL=1)")
            break

    # Report
    safe_print("")
    safe_print("-" * 70)
    safe_print(f"  {'Script':<52} {'Result':<6} {'Time':>6}")
    safe_print("-" * 70)

    passed_count = 0
    skipped_count = 0
    failed: list[str] = []

    for script_rel, status, snippet, elapsed in results:
        is_skip = status == "SKIP"
        if status == "PASS":
            passed_count += 1
        elif is_skip:
            skipped_count += 1
        else:
            failed.append(script_rel)
        safe_print(f"  {script_rel:<52} {status:<6} {elapsed:>5.1f}s")
        if status == "FAIL":
            # Show error snippet (truncated)
            safe_print(f"    -> {snippet[:100]}")

    safe_print("-" * 70)
    safe_print(
        f"  Total: {len(results)}"
        f"  |  Passed: {passed_count}"
        f"  |  Skipped: {skipped_count}"
        f"  |  Failed: {len(failed)}"
    )
    safe_print("=" * 70)

    if failed:
        safe_print("")
        safe_print("  Failed scripts:")
        for f in failed:
            safe_print(f"    - {f}")
        safe_print("")
        safe_print("  Tip: Run a single script for details:")
        safe_print(f"    python {NUGGET_DIR / failed[0]}")
        sys.exit(1)
    elif skipped_count > 0:
        safe_print("")
        safe_print("  Validation completed with skips. [PARTIAL]")
        safe_print("  Install to run full validation: pip install apache-airflow")
        sys.exit(2)
    else:
        safe_print("")
        safe_print("  All nuggets passed! [OK]")
        sys.exit(0)


if __name__ == "__main__":
    main()
