"""Stage 1, Brick 69: Use one reusable guarded request workflow.

Functionality studied:
    Configure one GuardedTextWorkflow and use it to execute a real provider
    request without manually wiring retries, budget control, diagnostics,
    structured results, and audit persistence in the application script.
"""

from decimal import Decimal
import json
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
    / "69_guarded_workflow_audit.jsonl"
)


def main() -> None:
    """Execute one real guarded request."""

    settings = ApplicationSettings.from_environment(
        model=MODEL,
        rates=TokenRates(
            input_per_million=Decimal("0.20"),
            output_per_million=Decimal("1.25"),
        ),
        budget_limit=Decimal("0.001000"),
        projected_request_cost=Decimal("0.000100"),
        warning_threshold_percentage=Decimal("80"),
        max_attempts=3,
        retry_delay_seconds=0,
    )

    workflow = GuardedTextWorkflow(
        OpenAITextProvider(),
        settings,
        audit_path=AUDIT_FILE,
    )

    request = TextGenerationRequest(
        instructions=(
            "Use plain English. "
            "Return exactly one short sentence."
        ),
        prompt=(
            "Explain why an application should call one reusable "
            "guarded workflow instead of wiring every reliability "
            "mechanic separately."
        ),
        model=settings.model,
        temperature=0.0,
    )

    result = workflow.execute(
        request
    )

    print("GUARDED WORKFLOW RESULT")
    print("-----------------------")
    print(f"Status: {result.status}")
    print(f"Correlation ID: {result.correlation_id}")
    print(f"Attempts: {result.attempt_count}")
    print(f"User message: {result.user_message}")
    print(f"Audit file: {AUDIT_FILE}")

    if result.budget_status is not None:
        print(
            f"Amount spent: "
            f"${result.budget_status.amount_spent}"
        )
        print(
            f"Amount remaining: "
            f"${result.budget_status.amount_remaining}"
        )

    print("\nJSON-SAFE RESULT")
    print("----------------")
    print(
        json.dumps(
            result.to_json_dict(),
            indent=2,
        )
    )

    print("\nFINAL CHECK")
    print("-----------")

    if (
        result.status == "success"
        and result.attempt_count >= 1
        and result.correlation_id
        == result.diagnostic.correlation_id
        and AUDIT_FILE.exists()
    ):
        print(
            "PASS: the reusable workflow completed "
            "the guarded request."
        )
    else:
        print(
            "FAIL: the guarded workflow did not "
            "complete successfully."
        )


if __name__ == "__main__":
    main()
