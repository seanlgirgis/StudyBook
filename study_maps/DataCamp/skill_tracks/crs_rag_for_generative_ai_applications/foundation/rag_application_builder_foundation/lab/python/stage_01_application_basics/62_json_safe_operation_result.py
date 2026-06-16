"""Stage 1, Brick 62: Serialize a real OperationResult to JSON.

Functionality studied:
    Execute one guarded AI request and serialize its final structured
    OperationResult into formatted JSON.

Workflow:
    1. Create one correlation ID.
    2. Reserve projected application budget.
    3. Retry simulated temporary failures.
    4. Call the provider.
    5. Estimate actual request cost.
    6. Reconcile the reservation.
    7. Build structured diagnostic context.
    8. Build a safe generation diagnostic.
    9. Return one OperationResult.
    10. Convert it to a JSON-safe dictionary.
    11. Encode and print formatted JSON.

Reusable mechanics:
    - OperationResult
    - OperationDiagnosticContext
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
    - projected request cost;
    - retry policy;
    - simulated transient failures;
    - prompt;
    - output formatting.

Important:
    ``OperationResult.to_dict()`` keeps Decimal objects.

    ``OperationResult.to_json_dict()`` converts Decimal values to strings
    so the result can be passed safely to ``json.dumps()`` without losing
    financial precision.
"""

from decimal import Decimal
import json
from typing import Any

from rag_foundation import (
    OpenAITextProvider,
    OperationDiagnosticContext,
    OperationResult,
    TextGenerationRequest,
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


def contains_decimal(
    value: Any,
) -> bool:
    """Return whether a nested value contains any Decimal object."""

    if isinstance(value, Decimal):
        return True

    if isinstance(value, dict):
        return any(
            contains_decimal(item)
            for item in value.values()
        )

    if isinstance(
        value,
        (
            list,
            tuple,
        ),
    ):
        return any(
            contains_decimal(item)
            for item in value
        )

    return False


def execute_operation() -> OperationResult:
    """Execute one real guarded request and return OperationResult."""

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
        prompt=(
            "Explain why JSON-safe serialization matters "
            "for structured AI application results."
        ),
        model=MODEL,
        temperature=0.0,
    )

    attempts = {"count": 0}

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
            """Simulate transient failures before the real call."""

            attempts["count"] += 1

            print(
                f"Attempt {attempts['count']} "
                f"| correlation_id={correlation_id}"
            )

            if attempts["count"] <= SIMULATED_FAILURES:
                raise ConnectionError(
                    "Simulated temporary provider failure."
                )

            return provider.generate(request)

        provider_result = run_with_retry(
            generate_with_temporary_failures,
            retry_on=(ConnectionError,),
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


def display_serialization(
    result: OperationResult,
) -> None:
    """Display Python-native and JSON-safe representations."""

    python_native = result.to_dict()
    json_safe = result.to_json_dict()

    formatted_json = json.dumps(
        json_safe,
        indent=2,
    )

    print("\nSTRUCTURED RESULT")
    print("-----------------")
    print(f"Status: {result.status}")
    print(f"Correlation ID: {result.correlation_id}")
    print(f"Attempts: {result.attempt_count}")
    print(f"User message: {result.user_message}")

    print("\nPYTHON-NATIVE SERIALIZATION")
    print("---------------------------")
    print(python_native)

    print("\nJSON-SAFE SERIALIZATION")
    print("-----------------------")
    print(json_safe)

    print("\nFORMATTED JSON")
    print("--------------")
    print(formatted_json)

    python_native_has_decimal = contains_decimal(
        python_native
    )

    json_safe_has_decimal = contains_decimal(
        json_safe
    )

    print("\nSERIALIZATION CHECKS")
    print("--------------------")
    print(
        "Python-native result contains Decimal: "
        f"{python_native_has_decimal}"
    )
    print(
        "JSON-safe result contains Decimal: "
        f"{json_safe_has_decimal}"
    )
    print(
        "JSON budget amount_spent type: "
        f"{type(json_safe['budget_status']['amount_spent']).__name__}"
    )

    correlation_matches = (
        result.correlation_id
        == result.diagnostic.correlation_id
        == json_safe["correlation_id"]
        == json_safe["diagnostic"]["correlation_id"]
    )

    attempts_match = (
        result.attempt_count
        == result.diagnostic.attempt_count
        == json_safe["attempt_count"]
        == json_safe["diagnostic"]["attempt_count"]
    )

    print(
        "Correlation IDs aligned: "
        f"{correlation_matches}"
    )
    print(
        "Attempt counts aligned: "
        f"{attempts_match}"
    )

    print("\nFINAL CHECK")
    print("-----------")

    if (
        result.status == "success"
        and python_native_has_decimal
        and not json_safe_has_decimal
        and isinstance(
            json_safe["budget_status"]["amount_spent"],
            str,
        )
        and correlation_matches
        and attempts_match
    ):
        print(
            "PASS: the real OperationResult was serialized "
            "to precise, JSON-safe formatted output."
        )
    else:
        print(
            "FAIL: the serialized operation result did not "
            "meet the expected safety or consistency rules."
        )


def main() -> None:
    """Execute the workflow and display formatted JSON."""

    result = execute_operation()

    display_serialization(result)


if __name__ == "__main__":
    main()
