"""Stage 1, Brick 70: Tiny guarded console AI application.

Functionality studied:
    Accept one user question, execute it through the reusable guarded
    workflow, display the safe result, and append compact audit metadata.

This is the Stage 1 end-to-end application.
"""

from decimal import Decimal
import os
from pathlib import Path

from rag_foundation import (
    ApplicationSettings,
    GuardedTextWorkflow,
    OpenAITextProvider,
    TextGenerationRequest,
)
from rag_foundation.costs import (
    TokenRates,
)


MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-5.4-nano",
)

AUDIT_FILE = (
    Path(__file__).resolve().parent
    / "output"
    / "70_console_application_audit.jsonl"
)


def main() -> None:
    """Run one guarded console question."""

    settings = ApplicationSettings.from_environment(
        model=MODEL,
        rates=TokenRates(
            input_per_million=Decimal("0.20"),
            output_per_million=Decimal("1.25"),
        ),
        budget_limit=Decimal("0.005000"),
        projected_request_cost=Decimal("0.000200"),
        warning_threshold_percentage=Decimal("80"),
        max_attempts=3,
        retry_delay_seconds=0,
    )

    workflow = GuardedTextWorkflow(
        OpenAITextProvider(),
        settings,
        audit_path=AUDIT_FILE,
    )

    print("GUARDED CONSOLE AI")
    print("------------------")

    question = input(
        "Enter one question: "
    ).strip()

    if question == "":
        print(
            "No question was entered. "
            "The provider was not called."
        )

        return

    request = TextGenerationRequest(
        instructions=(
            "You are a patient technical tutor. "
            "Use plain English and answer briefly."
        ),
        prompt=question,
        model=settings.model,
        temperature=0.0,
    )

    result = workflow.execute(
        request
    )

    print("\nANSWER")
    print("------")
    print(result.user_message)

    print("\nOPERATION")
    print("---------")
    print(f"Status: {result.status}")
    print(f"Reference: {result.correlation_id}")
    print(f"Attempts: {result.attempt_count}")

    if result.budget_status is not None:
        print(
            f"Estimated cost: "
            f"${result.budget_status.amount_spent}"
        )
        print(
            f"Remaining local budget: "
            f"${result.budget_status.amount_remaining}"
        )

    print(f"Safe audit file: {AUDIT_FILE}")

    print("\nFINAL CHECK")
    print("-----------")

    if (
        result.status
        in {
            "success",
            "fallback",
            "blocked",
        }
        and result.correlation_id
        == result.diagnostic.correlation_id
    ):
        print(
            "PASS: the console application returned "
            "one structured guarded result."
        )
    else:
        print(
            "FAIL: the console application result "
            "was inconsistent."
        )


if __name__ == "__main__":
    main()
