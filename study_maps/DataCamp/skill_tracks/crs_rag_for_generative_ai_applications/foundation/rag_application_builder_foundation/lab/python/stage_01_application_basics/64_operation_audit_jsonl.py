"""Stage 1, Brick 64: Append safe operation metadata to JSON Lines.

Functionality studied:
    Execute one real AI operation, reduce its structured result to a compact
    safe audit record, and append that record to a JSON Lines file.

Workflow:
    1. Create one correlation ID.
    2. Reserve projected application budget.
    3. Retry simulated transient failures.
    4. Make the real provider request.
    5. Reconcile actual estimated cost.
    6. Build safe operation diagnostics.
    7. Return one validated OperationResult.
    8. Build one compact OperationAuditRecord.
    9. Convert the audit record to JSON-safe values.
    10. Append exactly one compact JSON object to the audit file.
    11. Reload the latest audit line.
    12. Verify that no prompt, answer, secret, or raw response was saved.

Reusable mechanics:
    - OperationResult
    - OperationDiagnosticContext
    - OperationAuditRecord
    - build_operation_audit_record()
    - append_json_line()
    - BudgetReservationScope
    - CostBudgetTracker
    - RetryPolicy
    - run_with_retry()
    - build_success_diagnostic()
    - create_correlation_id()
    - estimate_request_cost()
    - OpenAITextProvider
    - TextGenerationRequest

Application-specific behavior:
    - budget size;
    - projected cost;
    - retry count;
    - simulated failures;
    - model prompt;
    - audit-file location;
    - displayed validation.

Important:
    The JSON Lines audit file stores operational metadata only.

    It does not store prompts, generated answers, API keys, exception
    messages, or raw provider responses.
"""

from decimal import Decimal
import json
from pathlib import Path
from typing import Any

from rag_foundation import (
    OpenAITextProvider,
    OperationDiagnosticContext,
    OperationResult,
    TextGenerationRequest,
    append_json_line,
    build_operation_audit_record,
)
from rag_foundation.budget import (
    BudgetReservationScope,
    CostBudgetTracker,
)
from rag_foundation.correlation import (
    create_correlation_id,
)
from rag_foundation.costs import (
    TokenRates,
    estimate_request_cost,
)
from rag_foundation.diagnostics import (
    build_success_diagnostic,
)
from rag_foundation.retry import (
    RetryPolicy,
    run_with_retry,
)


MODEL = "gpt-5.4-nano"

MODEL_RATES = TokenRates(
    input_per_million=Decimal("0.20"),
    output_per_million=Decimal("1.25"),
)

APPLICATION_BUDGET = Decimal("0.000100")
PROJECTED_COST = Decimal("0.000070")

MAX_ATTEMPTS = 3
SIMULATED_FAILURES = 2

REQUEST_PROMPT = (
    "Explain why an AI audit log should store operational "
    "metadata instead of prompts and generated answers."
)

OUTPUT_DIRECTORY = (
    Path(__file__).resolve().parent
    / "output"
)

AUDIT_FILE = (
    OUTPUT_DIRECTORY
    / "64_operation_audit.jsonl"
)

FORBIDDEN_KEYS = {
    "prompt",
    "instructions",
    "user_message",
    "generated_text",
    "answer",
    "raw_response",
    "api_key",
    "secret",
    "exception_message",
}


def read_audit_lines(
    path: Path,
) -> list[dict[str, Any]]:
    """Read every nonblank JSON object from an audit file."""

    if not path.exists():
        return []

    records: list[dict[str, Any]] = []

    for line in path.read_text(
        encoding="utf-8"
    ).splitlines():
        if line.strip() == "":
            continue

        loaded = json.loads(
            line
        )

        if not isinstance(loaded, dict):
            raise RuntimeError(
                "Each audit line must contain a JSON object."
            )

        records.append(
            loaded
        )

    return records


def execute_operation() -> OperationResult:
    """Execute one guarded request and return OperationResult."""

    provider = OpenAITextProvider()

    tracker = CostBudgetTracker(
        budget_limit=APPLICATION_BUDGET,
        warning_threshold_percentage=Decimal("80"),
    )

    correlation_id = create_correlation_id(
        prefix="rag"
    )

    request = TextGenerationRequest(
        instructions=(
            "Use plain English. "
            "Return exactly one short sentence."
        ),
        prompt=REQUEST_PROMPT,
        model=MODEL,
        temperature=0.0,
    )

    attempts = {
        "count": 0,
    }

    print("WORKFLOW START")
    print("--------------")
    print(f"Correlation ID: {correlation_id}")
    print(f"Budget limit: ${APPLICATION_BUDGET:.10f}")
    print(f"Projected cost: ${PROJECTED_COST:.10f}")

    with BudgetReservationScope(
        tracker,
        PROJECTED_COST,
    ) as scope:
        print("\nBUDGET RESERVATION")
        print("------------------")
        print(f"Allowed: {scope.allowed}")
        print(f"Reason: {scope.decision.reason}")
        print(
            f"Reserved: "
            f"${tracker.amount_reserved:.10f}"
        )

        if not scope.allowed:
            raise RuntimeError(
                "The demonstration budget unexpectedly "
                "blocked the operation."
            )

        def generate_with_temporary_failures():
            """Simulate failures before the real provider request."""

            attempts["count"] += 1

            print(
                f"Attempt {attempts['count']} "
                f"| correlation_id={correlation_id}"
            )

            if attempts["count"] <= SIMULATED_FAILURES:
                raise ConnectionError(
                    "Simulated temporary provider failure."
                )

            return provider.generate(
                request
            )

        provider_result = run_with_retry(
            generate_with_temporary_failures,
            retry_on=(
                ConnectionError,
            ),
            policy=RetryPolicy(
                max_attempts=MAX_ATTEMPTS,
                delay_seconds=0,
            ),
        )

        actual_cost = estimate_request_cost(
            result=provider_result,
            rates=MODEL_RATES,
        )

        budget_status = scope.reconcile(
            actual_cost
        )

        operation_context = OperationDiagnosticContext(
            correlation_id=correlation_id,
            attempt_count=attempts["count"],
        )

        diagnostic = build_success_diagnostic(
            provider_result,
            context=operation_context,
        )

        return OperationResult(
            status="success",
            user_message=provider_result.require_text(),
            correlation_id=correlation_id,
            attempt_count=attempts["count"],
            diagnostic=diagnostic,
            budget_status=budget_status,
        )


def main() -> None:
    """Execute, audit, reload, and validate one operation."""

    records_before = read_audit_lines(
        AUDIT_FILE
    )

    result = execute_operation()

    audit_record = build_operation_audit_record(
        result
    )

    json_safe_record = audit_record.to_json_dict()

    saved_path = append_json_line(
        json_safe_record,
        AUDIT_FILE,
        ensure_ascii=False,
    )

    records_after = read_audit_lines(
        saved_path
    )

    latest_record = records_after[-1]

    latest_line = saved_path.read_text(
        encoding="utf-8"
    ).splitlines()[-1]

    appended_count = (
        len(records_after)
        - len(records_before)
    )

    unsafe_keys_found = (
        FORBIDDEN_KEYS
        & latest_record.keys()
    )

    user_message_found = (
        result.user_message
        in latest_line
    )

    request_prompt_found = (
        REQUEST_PROMPT
        in latest_line
    )

    correlation_matches = (
        result.correlation_id
        == audit_record.correlation_id
        == latest_record["correlation_id"]
    )

    attempts_match = (
        result.attempt_count
        == audit_record.attempt_count
        == latest_record["attempt_count"]
    )

    amount_spent_is_string = isinstance(
        latest_record["amount_spent"],
        str,
    )

    print("\nMODEL RESULT")
    print("------------")
    print(result.user_message)

    print("\nAUDIT APPEND")
    print("------------")
    print(f"Audit file: {saved_path}")
    print(f"Records before: {len(records_before)}")
    print(f"Records after: {len(records_after)}")
    print(f"Records appended: {appended_count}")

    print("\nLATEST AUDIT RECORD")
    print("-------------------")
    print(
        json.dumps(
            latest_record,
            indent=2,
            ensure_ascii=False,
        )
    )

    print("\nAUDIT SAFETY CHECKS")
    print("-------------------")
    print(
        f"Forbidden keys found: "
        f"{len(unsafe_keys_found)}"
    )
    print(
        f"Generated answer found: "
        f"{user_message_found}"
    )
    print(
        f"Prompt found: "
        f"{request_prompt_found}"
    )
    print(
        f"Correlation IDs aligned: "
        f"{correlation_matches}"
    )
    print(
        f"Attempt counts aligned: "
        f"{attempts_match}"
    )
    print(
        f"amount_spent type: "
        f"{type(latest_record['amount_spent']).__name__}"
    )

    print("\nFINAL CHECK")
    print("-----------")

    if (
        result.status == "success"
        and saved_path.exists()
        and appended_count == 1
        and len(unsafe_keys_found) == 0
        and not user_message_found
        and not request_prompt_found
        and correlation_matches
        and attempts_match
        and amount_spent_is_string
    ):
        print(
            "PASS: one compact safe operation summary was "
            "appended to the JSON Lines audit file."
        )
    else:
        print(
            "FAIL: the JSON Lines audit record did not meet "
            "the expected safety or consistency rules."
        )


if __name__ == "__main__":
    main()
