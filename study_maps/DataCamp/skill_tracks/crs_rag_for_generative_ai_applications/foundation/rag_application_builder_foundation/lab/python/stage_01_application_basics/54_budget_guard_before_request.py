"""Stage 1, Brick 54: Guard a request before calling the provider.

Functionality studied:
    Check a projected request cost against the remaining local application
    budget before sending anything to the model provider.

Reusable mechanics:
    - CostBudgetTracker
    - BudgetDecision
    - TokenRates
    - estimate_request_cost()
    - OpenAITextProvider
    - TextGenerationRequest

Important:
    The projected cost is a conservative reservation used before the call.

    After an allowed request completes, the application records the actual
    estimated cost from the returned token usage.

    A blocked request is never sent and does not change amount_spent.
"""

from decimal import Decimal

from rag_foundation import (
    OpenAITextProvider,
    TextGenerationRequest,
)
from rag_foundation.budget import CostBudgetTracker
from rag_foundation.costs import (
    RequestCostEstimate,
    TokenRates,
    estimate_request_cost,
)


MODEL = "gpt-5.4-nano"

MODEL_RATES = TokenRates(
    input_per_million=Decimal("0.20"),
    output_per_million=Decimal("1.25"),
)

APPLICATION_BUDGET = Decimal("0.000100")
WARNING_THRESHOLD = Decimal("50")

# Conservative pre-call estimates.
FIRST_PROJECTED_COST = Decimal("0.000050")
SECOND_PROJECTED_COST = Decimal("0.000100")


def make_existing_cost(
    total_cost: Decimal,
) -> RequestCostEstimate:
    """Create a prior-cost record for the demonstration."""

    return RequestCostEstimate(
        input_tokens=0,
        output_tokens=0,
        input_cost=Decimal("0"),
        output_cost=total_cost,
        total_cost=total_cost,
    )


def print_decision(
    request_number: int,
    projected_cost: Decimal,
    decision,
) -> None:
    """Display one pre-call budget decision."""

    print(f"\nREQUEST {request_number} — PRE-CALL CHECK")
    print("--------------------------------")
    print(f"Amount already spent: ${decision.amount_spent:.10f}")
    print(f"Projected request cost: ${projected_cost:.10f}")
    print(f"Projected total: ${decision.projected_total:.10f}")
    print(
        f"Projected remaining: "
        f"${decision.projected_remaining:.10f}"
    )
    print(f"Allowed: {decision.allowed}")
    print(f"Reason: {decision.reason}")


def main() -> None:
    provider = OpenAITextProvider()

    tracker = CostBudgetTracker(
        budget_limit=APPLICATION_BUDGET,
        warning_threshold_percentage=WARNING_THRESHOLD,
    )

    print("LOCAL APPLICATION BUDGET")
    print("------------------------")
    print(f"Budget limit: ${APPLICATION_BUDGET}")
    print(f"Warning threshold: {WARNING_THRESHOLD}%")

    first_decision = tracker.check_projected_cost(
        FIRST_PROJECTED_COST
    )

    print_decision(
        request_number=1,
        projected_cost=FIRST_PROJECTED_COST,
        decision=first_decision,
    )

    if first_decision.allowed:
        request = TextGenerationRequest(
            instructions=(
                "Use plain English. "
                "Return exactly one short sentence."
            ),
            prompt=(
                "Explain why checking a budget before an AI call "
                "is useful."
            ),
            model=MODEL,
            temperature=0.0,
        )

        result = provider.generate(request)

        actual_estimate = estimate_request_cost(
            result=result,
            rates=MODEL_RATES,
        )

        status = tracker.record_cost(
            actual_estimate
        )

        print("\nREQUEST 1 — PROVIDER RESULT")
        print("---------------------------")
        print(result.require_text())

        print("\nREQUEST 1 — ACTUAL COST")
        print("-----------------------")
        print(
            f"Reserved projected cost: "
            f"${FIRST_PROJECTED_COST:.10f}"
        )
        print(
            f"Actual estimated cost: "
            f"${actual_estimate.total_cost:.10f}"
        )
        print(
            f"Cumulative spending: "
            f"${status.amount_spent:.10f}"
        )

    else:
        print("\nRequest 1 was blocked before the provider call.")

    # Add prior local spending so the next request is predictably blocked.
    #
    # This represents other work performed by the application. It is only
    # used to make the blocked path deterministic in this learning brick.
    current_spending = tracker.amount_spent

    target_spending = Decimal("0.000075")

    if current_spending < target_spending:
        tracker.record_cost(
            make_existing_cost(
                target_spending - current_spending
            )
        )

    second_decision = tracker.check_projected_cost(
        SECOND_PROJECTED_COST
    )

    print_decision(
        request_number=2,
        projected_cost=SECOND_PROJECTED_COST,
        decision=second_decision,
    )

    provider_called_for_request_2 = False

    if second_decision.allowed:
        provider_called_for_request_2 = True

        request = TextGenerationRequest(
            prompt="This request should normally be blocked.",
            model=MODEL,
            temperature=0.0,
        )

        result = provider.generate(request)

        actual_estimate = estimate_request_cost(
            result=result,
            rates=MODEL_RATES,
        )

        tracker.record_cost(actual_estimate)

        print("\nREQUEST 2 — PROVIDER RESULT")
        print("---------------------------")
        print(result.require_text())

    else:
        print("\nREQUEST 2 — SAFE APPLICATION RESULT")
        print("-----------------------------------")
        print(
            "This request was not sent because its projected cost "
            "would exceed the local application budget."
        )

    final_status = tracker.status()

    print("\nFINAL SUMMARY")
    print("-------------")
    print(
        f"Provider called for request 2: "
        f"{provider_called_for_request_2}"
    )
    print(
        f"Final recorded spending: "
        f"${final_status.amount_spent:.10f}"
    )
    print(
        f"Remaining budget: "
        f"${final_status.amount_remaining:.10f}"
    )
    print(
        f"Budget exhausted: "
        f"{final_status.budget_exhausted}"
    )


if __name__ == "__main__":
    main()