"""Stage 1, Tiny Block 14: Choose an allowed provider and model.

Functionality studied here:
    Provider routing should consider privacy before cost or model strength.

No API request is made in this lesson.
"""


def choose_route(
    contains_private_data: bool,
    task_complexity: str,
) -> tuple[str, str]:
    """Choose a provider and model using simple routing rules."""

    # Private data must stay with an approved provider.
    if contains_private_data:
        return "watsonx", "approved-enterprise-model"

    # Public, simple work can use the cheapest suitable model.
    if task_complexity == "simple":
        return "openai", "gpt-5.4-nano"

    # Public work needing more judgment uses a stronger model.
    return "openai", "gpt-5.4-mini"


def main() -> None:
    provider, model = choose_route(
        contains_private_data=True,
        task_complexity="simple",
    )

    print("SELECTED ROUTE")
    print("--------------")
    print(f"Provider: {provider}")
    print(f"Model: {model}")


if __name__ == "__main__":
    main()