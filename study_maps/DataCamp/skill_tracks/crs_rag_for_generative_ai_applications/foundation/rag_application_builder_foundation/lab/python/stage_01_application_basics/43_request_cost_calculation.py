"""Stage 1, Brick 43: Calculate the estimated cost of one request.

Functionality studied:
    Use normalized token usage to estimate the input, output, and total
    cost of a real model request.

Reusable mechanics:
    TokenRates, RequestCostEstimate, and estimate_request_cost()
    are provided by rag_foundation.

Pricing note:
    Model prices are supplied by the application rather than hard-coded
    into the shared library because provider prices can change.
"""

from decimal import Decimal

from rag_foundation import (
    OpenAITextProvider,
    TextGenerationRequest,
)
from rag_foundation.costs import (
    TokenRates,
    estimate_request_cost,
)


MODEL = "gpt-5.4-nano"

# Current pricing used for this learning run:
# dollars per one million tokens.
MODEL_RATES = TokenRates(
    input_per_million=Decimal("0.20"),
    output_per_million=Decimal("1.25"),
)


def main() -> None:
    provider = OpenAITextProvider()

    request = TextGenerationRequest(
        instructions=(
            "Use plain English. "
            "Answer in exactly two short sentences."
        ),
        prompt=(
            "Explain why token usage matters when designing "
            "a cost-conscious RAG application."
        ),
        model=MODEL,
    )

    result = provider.generate(request)

    estimate = estimate_request_cost(
        result=result,
        rates=MODEL_RATES,
    )

    print("MODEL RESULT")
    print("------------")
    print(result.require_text())

    print("\nTOKEN USAGE")
    print("-----------")
    print(f"Input tokens: {estimate.input_tokens}")
    print(f"Output tokens: {estimate.output_tokens}")

    print("\nPRICING USED")
    print("------------")
    print(
        "Input price per 1M tokens: "
        f"${MODEL_RATES.input_per_million}"
    )
    print(
        "Output price per 1M tokens: "
        f"${MODEL_RATES.output_per_million}"
    )

    print("\nESTIMATED COST")
    print("--------------")
    print(f"Input cost:  ${estimate.input_cost:.10f}")
    print(f"Output cost: ${estimate.output_cost:.10f}")
    print(f"Total cost:  ${estimate.total_cost:.10f}")


if __name__ == "__main__":
    main()