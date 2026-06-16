"""Stage 1, Brick 47: Validate and repair a generated summary.

Functionality studied:
    1. Generate a compact summary.
    2. Check whether required facts were preserved.
    3. Repair the summary once when facts are missing.
    4. Validate the repaired summary again.
    5. Accept only a complete summary.

Reusable mechanics:
    - TextGenerationRequest
    - OpenAITextProvider
    - validate_summary_facts()

Application-specific behavior:
    - which facts must be preserved;
    - how the repair prompt is written;
    - how many repair attempts are allowed.
"""

from rag_foundation import (
    OpenAITextProvider,
    TextGenerationRequest,
)
from rag_foundation.summary_validation import (
    SummaryValidationResult,
    validate_summary_facts,
)


SOURCE_CONVERSATION = """
user: For this project, split documents into chunks of 400 words.
assistant: Understood: chunk size is 400 words.
user: Use an overlap of 50 words between chunks.
assistant: Understood: overlap is 50 words.
user: Store the source filename and page number with every chunk.
assistant: Understood: preserve source filename and page number.
""".strip()


REQUIRED_FACTS = [
    "400 words",
    "50 words",
    "source filename",
    "page number",
]


def generate_summary(
    provider: OpenAITextProvider,
) -> str:
    """Generate an intentionally compressed first summary."""

    request = TextGenerationRequest(
        instructions=(
            "Summarize the conversation in exactly one short sentence. "
            "Preserve the most important project decisions. "
            "Do not add information."
        ),
        prompt=SOURCE_CONVERSATION,
        model="gpt-5.4-nano",
        temperature=0.0,
    )

    result = provider.generate(request)

    return result.require_text().strip()


def repair_summary(
    provider: OpenAITextProvider,
    summary: str,
    validation: SummaryValidationResult,
) -> str:
    """Ask the model to restore facts missing from the summary."""

    missing_facts_text = "\n".join(
        f"- {fact}"
        for fact in validation.missing_facts
    )

    request = TextGenerationRequest(
        instructions=(
            "Repair the summary so it preserves every required fact. "
            "Return exactly one concise sentence. "
            "Do not add facts that are not in the source conversation."
        ),
        prompt=f"""
Source conversation:
{SOURCE_CONVERSATION}

Current incomplete summary:
{summary}

Missing required facts:
{missing_facts_text}
""".strip(),
        model="gpt-5.4-nano",
        temperature=0.0,
    )

    result = provider.generate(request)

    return result.require_text().strip()


def print_validation(
    title: str,
    validation: SummaryValidationResult,
) -> None:
    """Display preserved and missing summary facts."""

    print(title)
    print("-" * len(title))
    print(f"Valid: {validation.is_valid}")
    print(
        "Preserved facts: "
        f"{list(validation.preserved_facts)}"
    )
    print(
        "Missing facts: "
        f"{list(validation.missing_facts)}"
    )


def main() -> None:
    provider = OpenAITextProvider()

    summary = generate_summary(provider)

    first_validation = validate_summary_facts(
        summary=summary,
        required_facts=REQUIRED_FACTS,
    )

    print("INITIAL SUMMARY")
    print("---------------")
    print(summary)

    print()
    print_validation(
        "INITIAL VALIDATION",
        first_validation,
    )

    if first_validation.is_valid:
        final_summary = summary
        final_validation = first_validation

        print("\nREPAIR")
        print("------")
        print("No repair was needed.")

    else:
        final_summary = repair_summary(
            provider=provider,
            summary=summary,
            validation=first_validation,
        )

        final_validation = validate_summary_facts(
            summary=final_summary,
            required_facts=REQUIRED_FACTS,
        )

        print("\nREPAIRED SUMMARY")
        print("----------------")
        print(final_summary)

        print()
        print_validation(
            "FINAL VALIDATION",
            final_validation,
        )

    print("\nFINAL RESULT")
    print("------------")

    if final_validation.is_valid:
        print("Summary accepted.")
        print(final_summary)
    else:
        print("Summary rejected after one repair attempt.")


if __name__ == "__main__":
    main()