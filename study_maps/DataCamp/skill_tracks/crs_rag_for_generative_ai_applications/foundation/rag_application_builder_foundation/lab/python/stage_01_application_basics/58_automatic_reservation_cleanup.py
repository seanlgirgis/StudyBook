"""Stage 1, Brick 58: Automatically manage a budget reservation.

Functionality studied:
    Use a context manager so application code cannot accidentally leave
    projected budget reserved after a provider failure.

Reusable mechanics:
    - BudgetReservationScope
    - CostBudgetTracker
    - TokenRates
    - estimate_request_cost()
    - OpenAITextProvider
    - TextGenerationRequest

Application-specific behavior:
    - budget size;
    - projected request cost;
    - prompt;
    - user-facing success or failure message.
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
from rag_foundation.costs import (
    TokenRates,
    estimate_request_cost,
)


MODEL = "gpt-5.4-nano"

MODEL_RATES = TokenRates(
    input_per_million=Decimal("0.20"),
    output_per_million=Decimal("1.25"),
)

APPLICATION_BUDGET = Decimal("0.000100")
PROJECTED_COST = Decimal("0.000070")


def main() -> None:
    """Reserve, call the provider, and reconcile automatically."""

    provider = OpenAITextProvider()

    tracker = CostBudgetTracker(
        budget_limit=APPLICATION_BUDGET,
        warning_threshold_percentage=Decimal("80"),
    )

    request = TextGenerationRequest(
        instructions=(
            "Use plain English. "
            "Return exactly one short sentence."
        ),
        prompt=(
            "Explain why a context manager is useful "
            "for cleaning up reserved resources."
        ),
        model=MODEL,
        temperature=0.0,
    )

    print("INITIAL BUDGET")
    print("--------------")
    print(f"Budget limit: ${APPLICATION_BUDGET:.10f}")
    print(f"Spent: ${tracker.amount_spent:.10f}")
    print(f"Reserved: ${tracker.amount_reserved:.10f}")

    with BudgetReservationScope(
        tracker,
        PROJECTED_COST,
    ) as scope:
        print("\nRESERVATION DECISION")
        print("--------------------")
        print(f"Allowed: {scope.allowed}")
        print(f"Reason: {scope.decision.reason}")
        print(
            f"Reserved inside scope: "
            f"${tracker.amount_reserved:.10f}"
        )

        if not scope.allowed:
            print("\nUSER-FACING RESULT")
            print("------------------")
            print(
                "The request was not sent because its projected "
                "cost exceeds the available application budget."
            )
            return

        result = provider.generate(request)

        actual_estimate = estimate_request_cost(
            result=result,
            rates=MODEL_RATES,
        )

        status = scope.reconcile(
            actual_estimate
        )

        print("\nMODEL ANSWER")
        print("------------")
        print(result.require_text())

        print("\nRECONCILIATION")
        print("--------------")
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
            f"${status.amount_spent:.10f}"
        )

    print("\nAFTER SCOPE")
    print("-----------")
    print(
        f"Reserved: "
        f"${tracker.amount_reserved:.10f}"
    )
    print(
        f"Spent: "
        f"${tracker.amount_spent:.10f}"
    )

    if (
        tracker.amount_reserved == Decimal("0")
        and tracker.amount_spent > Decimal("0")
    ):
        print(
            "PASS: the reservation was finalized into "
            "actual spending."
        )
    else:
        print(
            "FAIL: the reservation lifecycle was not completed."
        )


if __name__ == "__main__":
    main()