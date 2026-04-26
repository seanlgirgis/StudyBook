# ============================================================
# Topic   : AWS CloudWatch for Data Engineers
# File    : capstone/capstone.py
# Covers  : Orchestrate the full Pipeline Observability Stack capstone
# Prereqs : pip install boto3 | AWS credentials | profile: study
# Run     : python capstone/capstone.py
# ============================================================

from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from typing import Any, Callable


NAMESPACE = os.getenv("CW_NAMESPACE", "StudyBook/CapstoneP")
LOG_GROUP = os.getenv("CW_LOG_GROUP_NAME", "/studybook/capstone/pipeline")
PIPELINE_NAME = "iot-ingest-hourly"
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_PROFILE = os.getenv("AWS_PROFILE", "study")


# Allow this file to import sibling capstone modules when run directly:
#   python capstone/capstone.py
CAPSTONE_DIR = Path(__file__).resolve().parent
if str(CAPSTONE_DIR) not in sys.path:
    sys.path.insert(0, str(CAPSTONE_DIR))


def run_step(step_name: str, fn: Callable[[], Any]) -> bool:
    """
    Run one capstone step and report success/failure.

    WHY:
        Real orchestration needs visible step boundaries. When a pipeline setup
        fails, operators need to know exactly which stage failed and how long it ran.

    Args:
        step_name (str): Human-readable step name.
        fn (Callable[[], Any]): Function to execute.

    Returns:
        bool: True if the step passed, False if it failed.

    Raises:
        None. Exceptions are caught and converted to FAIL output.
    """
    print(f"\n=== {step_name} ===")
    start = time.perf_counter()

    try:
        fn()
        elapsed = time.perf_counter() - start
        print(f"PASS: {step_name} completed in {elapsed:.2f}s")
        return True
    except Exception as exc:
        elapsed = time.perf_counter() - start
        print(f"FAIL: {step_name} failed in {elapsed:.2f}s")
        print(f"Reason: {type(exc).__name__}: {exc}")
        return False


def print_health_report(alarm_names: list[str], dashboard_url: str) -> None:
    """
    Print the final capstone health report.

    WHY:
        A good observability stack ends with an operator-facing summary:
        what was created, what failures were injected, and where to investigate.

    Args:
        alarm_names (list[str]): Created alarm names.
        dashboard_url (str): CloudWatch dashboard URL.

    Returns:
        None.

    Raises:
        None.
    """
    print("\nPIPELINE OBSERVABILITY STACK — HEALTH REPORT")
    print("============================================")
    print("Metrics emitted : 24 hourly runs (2 failures injected)")
    print(f"Alarms created  : {len(alarm_names)} (4 metric + 1 composite)")
    print(f"Dashboard       : {dashboard_url}")
    print("Failure hours   : -4h ago, -16h ago")
    print("Expected alarms : capstone-errors, capstone-lag-high, capstone-unhealthy → ALARM")
    print("Run insights_queries.py to investigate the failure windows.")


def main() -> None:
    """
    Run the full capstone workflow.

    WHY:
        This file ties together metrics, logs, alarms, dashboards, and Insights.
        That is the complete observability loop for a production data pipeline.

    Args:
        None.

    Returns:
        None.

    Raises:
        None. Step failures are reported without hiding cleanup instructions.
    """
    import emit_pipeline_metrics
    import setup_alarms
    import build_dashboard
    import insights_queries

    alarm_names: list[str] = []
    dashboard_url = ""

    try:
        run_step(
            "Emit 24 hours of pipeline metrics and logs",
            lambda: (
                emit_pipeline_metrics.create_log_group(retention_days=7),
                emit_pipeline_metrics.emit_24_hours(failure_hours=[4, 16]),
            ),
        )

        def create_alarms_step() -> None:
            nonlocal alarm_names
            alarm_names = setup_alarms.create_all_alarms()
            time.sleep(3)
            setup_alarms.print_alarm_states(alarm_names)

        run_step("Create CloudWatch alarms", create_alarms_step)

        def dashboard_step() -> None:
            nonlocal dashboard_url
            dashboard_url = build_dashboard.create_pipeline_dashboard(
                "capstone-pipeline-health"
            )

        run_step("Create CloudWatch dashboard", dashboard_step)

        run_step("Run Logs Insights investigation queries", insights_queries.run_all_queries)

        print_health_report(alarm_names, dashboard_url)

    finally:
        print("\nTo delete all resources run: python capstone/cleanup.py")


if __name__ == "__main__":
    main()