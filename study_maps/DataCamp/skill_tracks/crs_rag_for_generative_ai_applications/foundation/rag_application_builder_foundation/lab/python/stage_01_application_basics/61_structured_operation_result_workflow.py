"""Stage 1, Brick 61: Return one structured operation result.

Functionality studied:
    Compose the existing request mechanics and return one validated
    ``OperationResult`` instead of exposing unrelated loose values.

Workflow:
    1. Create one correlation ID.
    2. Reserve projected cost.
    3. Retry temporary failures.
    4. Call the provider.
    5. Reconcile actual cost.
    6. Build structured diagnostic context.
    7. Build a safe generation diagnostic.
    8. Return one immutable OperationResult.

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
    - prompt;
    - simulated temporary failures.

This brick demonstrates the successful result path.
"""

from decimal import Decimal

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


def execute_operation() -> OperationResult:
    """Execute one logical AI request and return its structured result."""

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
            "Explain why returning one structured operation result "
            "is better than returning several unrelated values."
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
                "The demonstration budget unexpectedly blocked "
                "the operation."
            )

        def generate_with_temporary_failures():
            """Simulate temporary failures before the real provider call."""

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


def display_operation_result(
    result: OperationResult,
) -> None:
    """Display one completed structured operation result."""

    print("\nSTRUCTURED OPERATION RESULT")
    print("---------------------------")
    print(f"Status: {result.status}")
    print(f"Correlation ID: {result.correlation_id}")
    print(f"Attempts: {result.attempt_count}")

    print("\nUSER MESSAGE")
    print("------------")
    print(result.user_message)

    print("\nSAFE DIAGNOSTIC")
    print("---------------")
    print(result.diagnostic.to_dict())

    print("\nBUDGET RESULT")
    print("-------------")

    if result.budget_status is None:
        print("No completed budget status was returned.")
    else:
        print(
            f"Spent: "
            f"${result.budget_status.amount_spent:.10f}"
        )
        print(
            f"Remaining: "
            f"${result.budget_status.amount_remaining:.10f}"
        )
        print(
            f"Warning reached: "
            f"{result.budget_status.warning_reached}"
        )
        print(
            f"Budget exhausted: "
            f"{result.budget_status.budget_exhausted}"
        )

    print("\nSERIALIZED RESULT")
    print("-----------------")
    print(result.to_dict())


def main() -> None:
    """Execute the workflow and display its structured result."""

    result = execute_operation()

    display_operation_result(result)

    print("\nFINAL CHECK")
    print("-----------")

    if (
        result.status == "success"
        and result.correlation_id
        == result.diagnostic.correlation_id
        and result.attempt_count
        == result.diagnostic.attempt_count
        and result.budget_status is not None
    ):
        print(
            "PASS: one validated OperationResult contains "
            "the complete safe workflow outcome."
        )
    else:
        print(
            "FAIL: the structured result is incomplete "
            "or internally inconsistent."
        )


if __name__ == "__main__":
    main()