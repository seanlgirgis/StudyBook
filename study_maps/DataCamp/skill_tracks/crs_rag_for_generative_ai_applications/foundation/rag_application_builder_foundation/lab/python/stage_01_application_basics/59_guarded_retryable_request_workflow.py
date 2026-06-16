"""Stage 1, Brick 59: Compose one complete request workflow.

Functionality studied:
    Combine existing reusable mechanics into one application request:

    1. Create one correlation ID.
    2. Reserve projected budget for the whole logical request.
    3. Retry temporary failures using the same reservation.
    4. Call the model provider.
    5. Estimate and reconcile actual cost.
    6. Create a safe success or failure diagnostic.
    7. Return a user-facing result with a trace reference.

Reusable mechanics:
    - create_correlation_id()
    - BudgetReservationScope
    - CostBudgetTracker
    - RetryPolicy
    - run_with_retry()
    - build_success_diagnostic()
    - build_failure_diagnostic()
    - estimate_request_cost()
    - OpenAITextProvider
    - TextGenerationRequest

Application-specific behavior:
    - budget size;
    - projected request cost;
    - retry policy;
    - simulated temporary failures;
    - prompt;
    - fallback response.

Important:
    One logical request receives:

    - one correlation ID;
    - one budget reservation;
    - several possible retry attempts.

    Retries do not each reserve a separate amount.
"""

from decimal import Decimal

from rag_foundation import (
    OpenAITextProvider,
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
    build_failure_diagnostic,
    build_success_diagnostic,
)
from rag_foundation.retry import (
    RetryPolicy,
    run_with_retry,
)
from rag_foundation.operation_context import (
    OperationDiagnosticContext,
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

SAFE_FALLBACK = (
    "The AI service is temporarily unavailable. "
    "Please try again later."
)


def main() -> None:
    """Run one guarded and traceable generation request."""

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
            "Explain why combining retries, budget controls, "
            "diagnostics, and correlation IDs improves an AI application."
        ),
        model=MODEL,
        temperature=0.0,
    )

    attempts = {"count": 0}

    print("LOGICAL REQUEST")
    print("---------------")
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
            f"Reserved amount: "
            f"${tracker.amount_reserved:.10f}"
        )

        if not scope.allowed:
            print("\nUSER-FACING RESULT")
            print("------------------")
            print(
                "The request was not sent because its projected "
                "cost exceeds the available application budget."
            )
            print(f"Reference: {correlation_id}")

            return

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

        try:
            result = run_with_retry(
                generate_with_temporary_failures,
                retry_on=(ConnectionError,),
                policy=RetryPolicy(
                    max_attempts=MAX_ATTEMPTS,
                    delay_seconds=0,
                ),
            )

            actual_estimate = estimate_request_cost(
                result=result,
                rates=MODEL_RATES,
            )

            budget_status = scope.reconcile(
                actual_estimate
            )

            operation_context = OperationDiagnosticContext(
                correlation_id=correlation_id,
                attempt_count=attempts["count"],
            )

            diagnostic = build_success_diagnostic(
                result,
                context=operation_context,
            ).to_dict()


            print("\nMODEL ANSWER")
            print("------------")
            print(result.require_text())

            print("\nSAFE SUCCESS DIAGNOSTIC")
            print("-----------------------")
            print(diagnostic)

            print("\nBUDGET RECONCILIATION")
            print("---------------------")
            print(
                f"Projected reservation: "
                f"${PROJECTED_COST:.10f}"
            )
            print(
                f"Actual estimated cost: "
                f"${actual_estimate.total_cost:.10f}"
            )
            print(
                f"Recorded spending: "
                f"${budget_status.amount_spent:.10f}"
            )

            print("\nUSER-FACING RESULT")
            print("------------------")
            print(result.require_text())
            print(f"Reference: {correlation_id}")

            final_status = "success"

        except ConnectionError as error:
            # No manual reservation release is needed.
            # BudgetReservationScope releases it during __exit__.

            operation_context = OperationDiagnosticContext(
                correlation_id=correlation_id,
                attempt_count=attempts["count"],
            )

            diagnostic = build_failure_diagnostic(
                error,
                provider="openai",
                model=MODEL,
                context=operation_context,
            ).to_dict()

            print("\nSAFE FAILURE DIAGNOSTIC")
            print("-----------------------")
            print(diagnostic)

            print("\nUSER-FACING RESULT")
            print("------------------")
            print(SAFE_FALLBACK)
            print(f"Reference: {correlation_id}")

            final_status = "fallback"

    print("\nFINAL WORKFLOW STATE")
    print("--------------------")
    print(f"Correlation ID: {correlation_id}")
    print(f"Attempts: {attempts['count']}")
    print(f"Reserved: ${tracker.amount_reserved:.10f}")
    print(f"Spent: ${tracker.amount_spent:.10f}")
    print(f"Final status: {final_status}")


if __name__ == "__main__":
    main()