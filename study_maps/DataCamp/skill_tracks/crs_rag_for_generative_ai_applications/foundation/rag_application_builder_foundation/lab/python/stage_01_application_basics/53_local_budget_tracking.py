"""Stage 1, Brick 53: Track cumulative request cost against a budget.

Functionality studied:
    - make several real model requests;
    - calculate the estimated cost of each request;
    - accumulate those costs locally;
    - report warning and exhaustion thresholds.

Reusable mechanics:
    - OpenAITextProvider
    - TextGenerationRequest
    - TokenRates
    - estimate_request_cost()
    - CostBudgetTracker
    - BudgetStatus

Important:
    This tracks only costs recorded by this application run.
    It does not query the authoritative OpenAI account balance.
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

# Small learning budget so the percentage is visible.
APPLICATION_BUDGET = Decimal("0.0010")
WARNING_THRESHOLD = Decimal("50")


PROMPTS = [
    "Explain vector embeddings in one short sentence.",
    "Explain semantic search in one short sentence.",
    "Explain why chunking matters in RAG in one short sentence.",
]


def main() -> None:
    provider = OpenAITextProvider()

    budget_tracker = CostBudgetTracker(
        budget_limit=APPLICATION_BUDGET,
        warning_threshold_percentage=WARNING_THRESHOLD,
    )

    print("LOCAL APPLICATION BUDGET")
    print("------------------------")
    print(f"Budget limit: ${APPLICATION_BUDGET}")
    print(f"Warning threshold: {WARNING_THRESHOLD}%")

    for request_number, prompt in enumerate(
        PROMPTS,
        start=1,
    ):
        request = TextGenerationRequest(
            instructions=(
                "Use plain English. "
                "Return exactly one short sentence."
            ),
            prompt=prompt,
            model=MODEL,
            temperature=0.0,
        )

        result = provider.generate(request)

        estimate = estimate_request_cost(
            result=result,
            rates=MODEL_RATES,
        )

        budget_status = budget_tracker.record_cost(
            estimate
        )

        print(f"\nREQUEST {request_number}")
        print("-" * (8 + len(str(request_number))))
        print(result.require_text())

        print("\nREQUEST COST")
        print("------------")
        print(f"Input tokens: {estimate.input_tokens}")
        print(f"Output tokens: {estimate.output_tokens}")
        print(f"Estimated cost: ${estimate.total_cost:.10f}")

        print("\nBUDGET STATUS")
        print("-------------")
        print(
            f"Amount spent: "
            f"${budget_status.amount_spent:.10f}"
        )
        print(
            f"Amount remaining: "
            f"${budget_status.amount_remaining:.10f}"
        )
        print(
            f"Usage percentage: "
            f"{budget_status.usage_percentage:.2f}%"
        )
        print(
            f"Warning reached: "
            f"{budget_status.warning_reached}"
        )
        print(
            f"Budget exhausted: "
            f"{budget_status.budget_exhausted}"
        )

    final_status = budget_tracker.status()

    print("\nFINAL BUDGET SUMMARY")
    print("--------------------")
    print(f"Requests recorded: {len(PROMPTS)}")
    print(f"Total spent: ${final_status.amount_spent:.10f}")
    print(
        f"Remaining budget: "
        f"${final_status.amount_remaining:.10f}"
    )
    print(
        f"Budget usage: "
        f"{final_status.usage_percentage:.2f}%"
    )

    if final_status.budget_exhausted:
        print("Final state: budget exhausted")
    elif final_status.warning_reached:
        print("Final state: warning threshold reached")
    else:
        print("Final state: within budget")


if __name__ == "__main__":
    main()