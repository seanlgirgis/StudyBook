# ============================================================
# Topic   : AWS CloudWatch for Data Engineers
# File    : capstone/test_capstone.py
# Covers  : Pure logic tests for the CloudWatch capstone
# Prereqs : pip install boto3 pytest | AWS credentials | profile: study
# Run     : pytest capstone/test_capstone.py
# ============================================================

from __future__ import annotations

import importlib
import sys
from pathlib import Path


CAPSTONE_DIR = Path(__file__).resolve().parent
ROOT_DIR = CAPSTONE_DIR.parent
SETUP_DIR = ROOT_DIR / "setup"

if str(CAPSTONE_DIR) not in sys.path:
    sys.path.insert(0, str(CAPSTONE_DIR))

if str(SETUP_DIR) not in sys.path:
    sys.path.insert(0, str(SETUP_DIR))


from emit_pipeline_metrics import simulate_pipeline_run
from build_dashboard import build_widgets


def test_simulate_pipeline_run_normal() -> None:
    """
    Verify normal simulated runs stay inside healthy ranges.

    WHY:
        This validates the capstone's baseline behavior without calling AWS.
        Good unit tests isolate pure logic from cloud dependencies.
    """
    run = simulate_pipeline_run(hour_offset=1, inject_failure=False)

    assert 8000 <= run["records_in"] <= 12000
    assert run["error_count"] == 0
    assert run["duration_ms"] < 30000
    assert run["lag_seconds"] < 300


def test_simulate_pipeline_run_failure() -> None:
    """
    Verify failure runs produce unhealthy signals.

    WHY:
        The capstone depends on injected failures to exercise dashboards, alarms,
        and investigation queries.
    """
    run = simulate_pipeline_run(hour_offset=1, inject_failure=True)

    assert run["error_count"] > 0
    assert run["duration_ms"] > 30000 or run["lag_seconds"] > 300


def test_build_widgets_returns_five() -> None:
    """
    Verify dashboard builder returns exactly five widgets.

    WHY:
        Dashboard tests catch accidental layout or widget-count drift before the
        script writes dashboard JSON to AWS.
    """
    widgets = build_widgets("MyNamespace", "my-pipeline")

    assert len(widgets) == 5

    types = [widget["type"] for widget in widgets]

    assert "text" in types
    assert types.count("metric") == 4


def test_calculate_cw_cost_free_tier() -> None:
    """
    Verify CloudWatch metric free-tier cost behavior.

    WHY:
        Cost math is pure logic and should be tested without AWS calls.
    """
    monitoring_module = importlib.import_module("05_container_and_lambda_monitoring")

    cost = monitoring_module.calculate_cw_cost(
        custom_metrics=5,
        log_gb_month=1,
        dashboard_count=1,
        alarm_count=3,
    )

    assert cost["metrics_cost"] == 0.0
    assert cost["dashboard_cost"] == 3.0
    assert cost["total_monthly_usd"] > 0


def test_calculate_cw_cost_over_free_tier() -> None:
    """
    Verify CloudWatch cost calculation after custom metric free tier.

    WHY:
        Custom metric cardinality is one of the most common hidden CloudWatch
        cost traps in data platforms.
    """
    monitoring_module = importlib.import_module("05_container_and_lambda_monitoring")

    cost = monitoring_module.calculate_cw_cost(
        custom_metrics=50,
        log_gb_month=10,
        dashboard_count=2,
        alarm_count=10,
    )

    assert cost["metrics_cost"] == 40 * 0.30
    assert cost["alarm_cost"] == 10 * 0.10


def test_alarm_rule_composite_format() -> None:
    """
    Verify composite alarm rule string format.

    WHY:
        Composite alarm rules are string-based. A tiny formatting mistake can
        create a broken alarm or fail AWS validation.
    """
    name1 = "capstone-errors"
    name2 = "capstone-lag-high"
    alarm_rule = f'ALARM("{name1}") OR ALARM("{name2}")'

    assert alarm_rule == 'ALARM("capstone-errors") OR ALARM("capstone-lag-high")'
    assert alarm_rule.startswith('ALARM("')
    assert '") OR ALARM("' in alarm_rule
    assert alarm_rule.endswith('")')