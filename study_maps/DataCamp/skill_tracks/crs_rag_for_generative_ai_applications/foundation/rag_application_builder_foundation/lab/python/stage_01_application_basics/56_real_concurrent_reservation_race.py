"""Stage 1, Brick 56: Test reservations with real concurrent threads.

Functionality studied:
    Start two application requests at nearly the same time and let both
    compete for the same local application budget.

Expected outcome:
    - exactly one request receives the reservation;
    - exactly one request is blocked;
    - total reserved cost never exceeds the budget.

Reusable mechanics:
    - CostBudgetTracker
    - reserve_projected_cost()

Application-specific behavior:
    - thread coordination;
    - projected request cost;
    - displayed results.

This brick does not make a provider call. It focuses only on the
concurrent reservation race.
"""

from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
from threading import Barrier

from rag_foundation.budget import (
    CostBudgetTracker,
    ReservationDecision,
)


APPLICATION_BUDGET = Decimal("1.00")
PROJECTED_COST = Decimal("0.70")
REQUEST_COUNT = 2


def attempt_reservation(
    request_name: str,
    *,
    tracker: CostBudgetTracker,
    start_barrier: Barrier,
) -> tuple[str, ReservationDecision]:
    """Wait for the other thread, then attempt one reservation."""

    print(f"{request_name} is ready.")

    start_barrier.wait()

    decision = tracker.reserve_projected_cost(
        PROJECTED_COST
    )

    return request_name, decision


def main() -> None:
    """Run two competing reservation attempts concurrently."""

    tracker = CostBudgetTracker(
        budget_limit=APPLICATION_BUDGET
    )

    start_barrier = Barrier(
        REQUEST_COUNT
    )

    print("CONCURRENT RESERVATION RACE")
    print("---------------------------")
    print(f"Budget limit: ${APPLICATION_BUDGET}")
    print(f"Each request wants: ${PROJECTED_COST}")

    with ThreadPoolExecutor(
        max_workers=REQUEST_COUNT
    ) as executor:
        futures = [
            executor.submit(
                attempt_reservation,
                request_name,
                tracker=tracker,
                start_barrier=start_barrier,
            )
            for request_name in (
                "Request A",
                "Request B",
            )
        ]

        results = [
            future.result()
            for future in futures
        ]

    print("\nRESULTS")
    print("-------")

    allowed_count = 0
    blocked_count = 0

    for request_name, decision in results:
        print(
            f"{request_name}: "
            f"allowed={decision.allowed}"
        )

        print(
            f"  reason={decision.reason}"
        )

        if decision.allowed:
            allowed_count += 1
        else:
            blocked_count += 1

    print("\nFINAL BUDGET STATE")
    print("------------------")
    print(
        f"Reserved: "
        f"${tracker.amount_reserved}"
    )
    print(
        f"Spent: "
        f"${tracker.amount_spent}"
    )

    print("\nCONCURRENCY CHECK")
    print("-----------------")
    print(f"Allowed requests: {allowed_count}")
    print(f"Blocked requests: {blocked_count}")

    if (
        allowed_count == 1
        and blocked_count == 1
        and tracker.amount_reserved == PROJECTED_COST
    ):
        print(
            "PASS: only one concurrent request claimed the budget."
        )
    else:
        print(
            "FAIL: the reservation guard did not behave as expected."
        )


if __name__ == "__main__":
    main()