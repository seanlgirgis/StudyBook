"""Stage 1, Tiny Block 15: Store a routing decision in one object.

Functionality studied here:
    Keep the selected provider, model, and reason together.
"""


class RouteDecision:
    """Store one provider-routing decision."""

    def __init__(
        self,
        provider: str,
        model: str,
        reason: str,
    ) -> None:
        self.provider = provider
        self.model = model
        self.reason = reason


def choose_route(
    contains_private_data: bool,
    task_complexity: str,
) -> RouteDecision:
    """Choose a route and explain why it was selected."""

    if contains_private_data:
        return RouteDecision(
            provider="watsonx",
            model="approved-enterprise-model",
            reason="Private data requires an approved provider.",
        )

    if task_complexity == "simple":
        return RouteDecision(
            provider="openai",
            model="gpt-5.4-nano",
            reason="Simple public work can use the cheaper model.",
        )

    return RouteDecision(
        provider="openai",
        model="gpt-5.4-mini",
        reason="The task needs more judgment and explanation.",
    )


def main() -> None:
    decision = choose_route(
        contains_private_data=False,
        task_complexity="simple",
    )

    print("ROUTE DECISION")
    print("--------------")
    print(f"Provider: {decision.provider}")
    print(f"Model: {decision.model}")
    print(f"Reason: {decision.reason}")


if __name__ == "__main__":
    main()