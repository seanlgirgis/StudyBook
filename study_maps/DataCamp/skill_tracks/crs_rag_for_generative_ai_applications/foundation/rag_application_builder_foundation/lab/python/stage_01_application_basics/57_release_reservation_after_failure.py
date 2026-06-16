"""Stage 1, Brick 57: Release a budget reservation after failure.

Functionality studied:
    Demonstrate that an in-progress request must release its projected
    budget reservation when the provider operation fails.

Flow:
    1. Request A reserves budget.
    2. Request A fails before producing a result.
    3. The application releases Request A's reservation.
    4. Request B can then reserve the recovered budget.

Reusable mechanics:
    - CostBudgetTracker
    - BudgetReservation
    - reserve_projected_cost()
    - release_reservation()

Application-specific behavior:
    - simulated provider failure;
    - projected request costs;
    - user-facing status messages.
"""

from decimal import Decimal

from rag_foundation.budget import CostBudgetTracker


APPLICATION_BUDGET = Decimal("1.00")
PROJECTED_COST = Decimal("0.70")


def simulated_provider_call() -> str:
    """Simulate a provider operation that fails."""

    raise ConnectionError(
        "Simulated provider connection failure."
    )


def main() -> None:
    """Reserve, fail, release, and retry with another request."""

    tracker = CostBudgetTracker(
        budget_limit=APPLICATION_BUDGET
    )

    print("INITIAL BUDGET")
    print("--------------")
    print(f"Budget limit: ${APPLICATION_BUDGET}")
    print(f"Spent: ${tracker.amount_spent}")
    print(f"Reserved: ${tracker.amount_reserved}")

    request_a = tracker.reserve_projected_cost(
        PROJECTED_COST
    )

    print("\nREQUEST A — RESERVATION")
    print("-----------------------")
    print(f"Allowed: {request_a.allowed}")
    print(f"Reserved: ${tracker.amount_reserved}")

    if not request_a.allowed:
        print("Request A could not reserve budget.")
        return

    reservation = request_a.reservation

    if reservation is None:
        raise RuntimeError(
            "Allowed reservation decision did not contain "
            "a reservation."
        )

    try:
        simulated_provider_call()

    except ConnectionError as error:
        print("\nREQUEST A — PROVIDER FAILURE")
        print("----------------------------")
        print(type(error).__name__)
        print("The provider operation failed.")

        tracker.release_reservation(
            reservation
        )

        print("\nREQUEST A — CLEANUP")
        print("-------------------")
        print("Reservation released.")
        print(
            f"Reserved after cleanup: "
            f"${tracker.amount_reserved}"
        )
        print(
            f"Spent after cleanup: "
            f"${tracker.amount_spent}"
        )

    request_b = tracker.reserve_projected_cost(
        PROJECTED_COST
    )

    print("\nREQUEST B — RESERVATION")
    print("-----------------------")
    print(f"Allowed: {request_b.allowed}")
    print(f"Reason: {request_b.reason}")
    print(f"Reserved: ${tracker.amount_reserved}")

    print("\nFINAL CHECK")
    print("-----------")

    if (
        request_b.allowed
        and tracker.amount_reserved == PROJECTED_COST
        and tracker.amount_spent == Decimal("0")
    ):
        print(
            "PASS: failed work released its reservation, "
            "and another request could proceed."
        )
    else:
        print(
            "FAIL: reservation cleanup did not behave as expected."
        )


if __name__ == "__main__":
    main()