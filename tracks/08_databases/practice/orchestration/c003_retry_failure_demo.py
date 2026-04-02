# Story:
# A pipeline breaks at 2 AM. Do you retry, stop, or block downstream tasks?


def _run_with_retry(task_name, max_retries, outcome_fn):
    attempts = 0
    while True:
        attempts += 1
        print(f"[ATTEMPT {attempts}] {task_name}")
        outcome = outcome_fn(attempts)
        if outcome == "success":
            print(f"[SUCCESS] {task_name} after {attempts} attempt(s)")
            return "success"
        if outcome == "non_retryable":
            print(f"[FAILED - NON-RETRYABLE] {task_name} (stop immediately)")
            return "failed_final"

        print(f"[FAILED - RETRYABLE] {task_name}")
        if attempts > max_retries:
            print(f"[FAILED - FINAL] {task_name} exhausted retries (max {max_retries})")
            return "failed_final"
        print(f"[RETRY] {task_name} will retry (retry {attempts} of {max_retries})")


def _block_if_failed(task_name, deps, state):
    missing = [dep for dep in deps if state.get(dep) != "success"]
    if missing:
        print(f"[BLOCKED] {task_name} waits on {missing}")
        return True
    return False


def run_retry_failure_demo():
    print("=" * 72)
    print("Scenario: nightly finance pipeline with retries")
    print("Retryable failure = likely temporary. Non-retryable = stop now.")
    print("Final failed state = retries exhausted or non-retryable error.")

    state = {}

    print("=" * 72)
    print("Case A: transient failure that succeeds on retry")

    def transient_outcome(attempt):
        return "success" if attempt >= 2 else "retryable"

    state["extract_api"] = _run_with_retry("extract_api", max_retries=3, outcome_fn=transient_outcome)
    if not _block_if_failed("transform_sales", ["extract_api"], state):
        state["transform_sales"] = "success"
        print("[RUN] transform_sales -> success (upstream recovered)")

    print("=" * 72)
    print("Case B: persistent failure that keeps failing and eventually stops")

    def persistent_outcome(attempt):
        return "retryable"

    state["apply_fraud_rules"] = _run_with_retry(
        "apply_fraud_rules", max_retries=2, outcome_fn=persistent_outcome
    )
    if _block_if_failed("publish_metrics", ["apply_fraud_rules"], state):
        state["publish_metrics"] = "blocked"

    print("=" * 72)
    print("Case C: blind retries are dangerous")
    print("Charging a customer twice is worse than failing once.")

    def payment_outcome(_attempt):
        return "non_retryable"

    state["capture_payment"] = _run_with_retry(
        "capture_payment", max_retries=0, outcome_fn=payment_outcome
    )
    print("- Retrying this task could duplicate charges, so we do not retry.")

    print("=" * 72)
    print("Summary:")
    print("- Retryable failures can recover (transient glitches).")
    print("- Persistent failures exhaust retries and end in a final failed state.")
    print("- Non-retryable failures should stop immediately.")
    print("- Downstream tasks are blocked when upstream tasks fail.")


if __name__ == "__main__":
    run_retry_failure_demo()

# Takeaway: Retries are a tool, not a reflex.
