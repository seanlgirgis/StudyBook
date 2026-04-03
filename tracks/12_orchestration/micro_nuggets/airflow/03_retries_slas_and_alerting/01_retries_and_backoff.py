"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 03-01 · Retries, Backoff, and Failure Callbacks                      ║
║  Production-grade error handling and alerting patterns                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Transient failures (API timeouts, DB blips, network hiccups) are inevitable.
Airflow's retry system gives tasks multiple chances before declaring failure,
and callbacks let you alert or take recovery actions.

KEY CONCEPTS
────────────
  retries              — how many retry attempts (default: 0 in config)
  retry_delay          — timedelta between retries
  retry_exponential_backoff — double the delay on each retry
  max_retry_delay      — cap for exponential backoff
  on_failure_callback  — called when task fails all retries
  on_success_callback  — called when task succeeds
  on_retry_callback    — called on each retry attempt
  execution_timeout    — kill the task if it runs too long
  SLA                  — Service Level Agreement; alert if task is late

RETRY BACKOFF MATH
──────────────────
  retry 1:  retry_delay * 2^0 = base delay
  retry 2:  retry_delay * 2^1 = 2x base
  retry 3:  retry_delay * 2^2 = 4x base
  (capped at max_retry_delay)

INTERVIEW RELEVANCE
───────────────────
  "How do you handle transient failures in Airflow?"
  "What is exponential backoff and why is it better than fixed retry?"
  "How do you send a Slack alert when a task fails?"
  "What is on_failure_callback and what does the context dict contain?"
"""
from __future__ import annotations

import sys
from pathlib import Path
from datetime import timedelta

print("\n-- Nugget 03-01 : Retries and Failure Callbacks ------------")

RETRY_DAG_CODE = '''
from airflow.decorators import dag, task
from datetime import datetime, timedelta

# ── Reusable callback functions ───────────────────────────────────────────────

def on_task_failure(context: dict) -> None:
    """
    Called when a task exhausts all retries.
    In production: send Slack/PagerDuty/email alert here.
    context keys: dag, task, run_id, execution_date, exception, log_url, etc.
    """
    dag_id   = context["dag"].dag_id
    task_id  = context["task"].task_id
    exc      = context.get("exception", "unknown")
    run_id   = context["run_id"]
    print(f"[ALERT] Task FAILED: {dag_id}.{task_id} | run={run_id} | err={exc}")
    # Real implementation:
    # send_slack_message(channel="#data-alerts", text=f"DAG {dag_id} failed: {exc}")


def on_task_retry(context: dict) -> None:
    """Called on each retry attempt."""
    attempt = context["task_instance"].try_number
    task_id = context["task"].task_id
    print(f"[RETRY] {task_id} — attempt #{attempt}")


def on_task_success(context: dict) -> None:
    """Called when task succeeds (even after retries)."""
    task_id = context["task"].task_id
    print(f"[OK] {task_id} succeeded")


@dag(
    dag_id="lab_airflow_retries_demo",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    default_args={
        "retries": 3,
        "retry_delay": timedelta(seconds=10),
        "retry_exponential_backoff": True,
        "max_retry_delay": timedelta(minutes=5),
        "on_failure_callback": on_task_failure,
        "on_retry_callback": on_task_retry,
    },
    tags=["lab", "retries"],
)
def retries_demo():
    """
    Demonstrates retry patterns:
      - global default_args: retries + exponential backoff
      - per-task override with different retry settings
      - execution_timeout to kill stalled tasks
      - on_failure_callback for alerting
    """

    @task(
        retries=5,                              # override default_args
        retry_delay=timedelta(seconds=5),
        execution_timeout=timedelta(minutes=2), # kill if still running after 2m
        on_success_callback=on_task_success,
    )
    def flaky_api_call() -> str:
        """Simulates a task that may fail transiently."""
        import random
        if random.random() < 0.3:  # 30% failure rate
            raise ConnectionError("API timeout (simulated)")
        return "api_response_ok"

    @task(
        retries=0,               # no retries — must succeed first time
        on_failure_callback=on_task_failure,
    )
    def critical_validation(api_result: str) -> None:
        """Validation that must not be retried (idempotency concern)."""
        if api_result != "api_response_ok":
            raise ValueError(f"Invalid API response: {api_result}")
        print(f"Validation passed: {api_result}")

    result = flaky_api_call()
    critical_validation(result)


dag_instance = retries_demo()
'''

namespace: dict = {}
try:
    exec(RETRY_DAG_CODE, namespace)  # noqa: S102
    dag_obj = namespace["dag_instance"]

    print(f"  [OK] DAG parsed: {dag_obj.dag_id}")

    # Verify default_args retries
    assert dag_obj.default_args["retries"] == 3
    assert dag_obj.default_args["retry_exponential_backoff"] is True
    print("  [OK] default_args: retries=3, exponential_backoff=True")

    # Verify per-task override
    flaky = dag_obj.get_task("flaky_api_call")
    assert flaky.retries == 5, f"Expected 5 retries, got {flaky.retries}"
    print(f"  [OK] flaky_api_call overrides retries=5")

    # Verify execution_timeout
    assert flaky.execution_timeout == timedelta(minutes=2)
    print("  [OK] execution_timeout=2min on flaky_api_call")

    # Verify critical task has 0 retries
    crit = dag_obj.get_task("critical_validation")
    assert crit.retries == 0
    print("  [OK] critical_validation retries=0 (no retry on validation)")

    # Verify callbacks are set
    assert dag_obj.default_args.get("on_failure_callback") is not None
    print("  [OK] on_failure_callback configured globally")

except ImportError as e:
    print(f"  [SKIP] apache-airflow not installed: {e}")
    sys.exit(0)
except Exception as e:
    print(f"  [FAIL] {e}")
    sys.exit(1)

# ── Backoff math illustration ─────────────────────────────────────────────────
print()
print("  EXPONENTIAL BACKOFF EXAMPLE (base=10s, max=300s)")
print("  --------------------------------------------------")
base = 10
max_delay = 300
for attempt in range(1, 6):
    delay = min(base * (2 ** (attempt - 1)), max_delay)
    print(f"  Retry {attempt}: wait {delay}s before next attempt")

print()
print("  CALLBACK CONTEXT KEYS")
print("  ----------------------")
ctx_keys = [
    ("dag",            "DAG object"),
    ("task",           "Task object"),
    ("task_instance",  "TaskInstance with try_number, xcom_pull, etc."),
    ("run_id",         "DAG run identifier"),
    ("execution_date", "Pendulum datetime of the run"),
    ("exception",      "The exception that caused failure"),
    ("log_url",        "Link to the task log in the Airflow UI"),
]
for k, desc in ctx_keys:
    print(f"  context['{k}']   {desc}")

print()
print("  KEY TAKEAWAYS")
print("  -------------")
print("  - Use default_args retries for global policy; override per task")
print("  - retry_exponential_backoff=True is best practice for external calls")
print("  - execution_timeout prevents zombie tasks from blocking workers")
print("  - on_failure_callback receives the full context dict for rich alerts")
print("  - Set retries=0 on validation tasks to avoid repeating side effects")
print()
