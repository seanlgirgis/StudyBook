"""Stage 1, Brick 55: Reserve projected cost for competing requests.

Functionality studied:
    Demonstrate how two requests competing for the same remaining budget
    are handled safely.

Flow:
    1. Request A reserves part of the budget.
    2. Request B attempts to reserve the same amount.
    3. Request B is blocked because Request A already holds the budget.
    4. Request A performs the real provider call.
    5. The reservation is replaced with the actual estimated cost.

Reusable mechanics:
    - CostBudgetTracker
    - BudgetReservation
    - reserve_projected_cost()
    - reconcile_reservation()
    - TokenRates
    - estimate_request_cost()
    - OpenAITextProvider
    - TextGenerationRequest

Application-specific behavior:
    - the application budget;
    - projected request costs;
    - the prompt being sent;
    - the user-facing blocked response.
"""

from decimal import Decimal

from rag_foundation import (
    OpenAITextProvider,
    TextGenerationRequest,
)
from rag_foundation.budget import CostBudgetTracker
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

REQUEST_A_PROJECTED_COST = Decimal("0.000070")
REQUEST_B_PROJECTED_COST = Decimal("0.000070")


def main() -> None:
    """Run the reservation and reconciliation demonstration."""

    provider = OpenAITextProvider()

    tracker = CostBudgetTracker(
        budget_limit=APPLICATION_BUDGET,
        warning_threshold_percentage=Decimal("80"),
    )

    print("APPLICATION BUDGET")
    print("------------------")
    print(f"Budget limit: ${APPLICATION_BUDGET:.10f}")
    print(f"Spent: ${tracker.amount_spent:.10f}")
    print(f"Reserved: ${tracker.amount_reserved:.10f}")

    request_a_decision = tracker.reserve_projected_cost(
        REQUEST_A_PROJECTED_COST
    )

    print("\nREQUEST A — RESERVATION")
    print("-----------------------")
    print(
        f"Projected cost: "
        f"${REQUEST_A_PROJECTED_COST:.10f}"
    )
    print(f"Allowed: {request_a_decision.allowed}")
    print(
        f"Reserved total: "
        f"${tracker.amount_reserved:.10f}"
    )
    print(
        f"Available after reservation: "
        f"${request_a_decision.available_budget:.10f}"
    )

    request_b_decision = tracker.reserve_projected_cost(
        REQUEST_B_PROJECTED_COST
    )

    print("\nREQUEST B — RESERVATION")
    print("-----------------------")
    print(
        f"Projected cost: "
        f"${REQUEST_B_PROJECTED_COST:.10f}"
    )
    print(f"Allowed: {request_b_decision.allowed}")
    print(f"Reason: {request_b_decision.reason}")
    print(
        f"Reserved total remains: "
        f"${tracker.amount_reserved:.10f}"
    )

    if not request_a_decision.allowed:
        print("\nRequest A could not reserve budget.")
        return

    reservation = request_a_decision.reservation

    if reservation is None:
        raise RuntimeError(
            "An allowed reservation decision must contain a reservation."
        )

    request = TextGenerationRequest(
        instructions=(
            "Use plain English. "
            "Return exactly one short sentence."
        ),
        prompt=(
            "Explain why reserving projected cost helps "
            "when several AI requests run at the same time."
        ),
        model=MODEL,
        temperature=0.0,
    )

    try:
        result = provider.generate(request)

    except Exception:
        tracker.release_reservation(
            reservation
        )

        print("\nREQUEST A — FAILURE")
        print("-------------------")
        print(
            "The provider call failed, so the reservation "
            "was released."
        )

        raise

    actual_estimate = estimate_request_cost(
        result=result,
        rates=MODEL_RATES,
    )

    final_status = tracker.reconcile_reservation(
        reservation=reservation,
        estimate=actual_estimate,
    )

    print("\nREQUEST A — PROVIDER RESULT")
    print("---------------------------")
    print(result.require_text())

    print("\nREQUEST A — RECONCILIATION")
    print("--------------------------")
    print(
        f"Projected reservation: "
        f"${REQUEST_A_PROJECTED_COST:.10f}"
    )
    print(
        f"Actual estimated cost: "
        f"${actual_estimate.total_cost:.10f}"
    )
    print(
        f"Reserved after reconciliation: "
        f"${tracker.amount_reserved:.10f}"
    )
    print(
        f"Recorded spending: "
        f"${final_status.amount_spent:.10f}"
    )
    print(
        f"Remaining budget: "
        f"${final_status.amount_remaining:.10f}"
    )

    print("\nREQUEST B — USER RESULT")
    print("-----------------------")

    if request_b_decision.allowed:
        print("Request B may proceed.")
    else:
        print(
            "Request B was not sent because another in-progress "
            "request had already reserved the available budget."
        )

    print("\nFINAL SUMMARY")
    print("-------------")
    print(f"Request A allowed: {request_a_decision.allowed}")
    print(f"Request B allowed: {request_b_decision.allowed}")
    print(f"Final reserved amount: ${tracker.amount_reserved:.10f}")
    print(f"Final spending: ${tracker.amount_spent:.10f}")


if __name__ == "__main__":
    main()