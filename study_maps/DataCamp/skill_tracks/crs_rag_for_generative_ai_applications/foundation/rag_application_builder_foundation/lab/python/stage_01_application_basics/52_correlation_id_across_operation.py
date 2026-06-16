"""Stage 1, Brick 52: Trace one logical request with a correlation ID.

Functionality studied:
    Create one correlation ID for a logical request and reuse it across:

    - retry attempts;
    - success or failure diagnostics;
    - the final user-facing result.

Reusable mechanics:
    - create_correlation_id()
    - validate_correlation_id()
    - RetryPolicy
    - run_with_retry()
    - build_success_diagnostic()
    - build_failure_diagnostic()
    - OpenAITextProvider
    - TextGenerationRequest

Important:
    A new correlation ID is created once per logical request, not once
    per retry attempt.
"""

from rag_foundation import (
    OpenAITextProvider,
    TextGenerationRequest,
)
from rag_foundation.correlation import (
    create_correlation_id,
    validate_correlation_id,
)
from rag_foundation.diagnostics import (
    build_failure_diagnostic,
    build_success_diagnostic,
)
from rag_foundation.retry import (
    RetryPolicy,
    run_with_retry,
)


MODEL = "gpt-5.4-nano"
SIMULATED_FAILURES = 2
MAX_ATTEMPTS = 3


def main() -> None:
    provider = OpenAITextProvider()

    correlation_id = create_correlation_id(
        prefix="rag",
    )

    correlation_id = validate_correlation_id(
        correlation_id
    )

    request = TextGenerationRequest(
        instructions=(
            "Use plain English. "
            "Return exactly one short sentence."
        ),
        prompt=(
            "Explain why a correlation ID is useful "
            "in an AI application."
        ),
        model=MODEL,
        temperature=0.0,
    )

    attempts = {"count": 0}

    print("LOGICAL REQUEST")
    print("---------------")
    print(f"Correlation ID: {correlation_id}")

    def generate_with_transient_failures():
        """Simulate failures before performing the real provider call."""

        attempts["count"] += 1

        print(
            f"Attempt {attempts['count']} "
            f"| correlation_id={correlation_id}"
        )

        if attempts["count"] <= SIMULATED_FAILURES:
            raise ConnectionError(
                "Simulated temporary provider failure."
            )

        return provider.generate(request)

    try:
        result = run_with_retry(
            generate_with_transient_failures,
            retry_on=(ConnectionError,),
            policy=RetryPolicy(
                max_attempts=MAX_ATTEMPTS,
                delay_seconds=0,
            ),
        )

        diagnostic = build_success_diagnostic(
            result
        ).to_dict()

        diagnostic["correlation_id"] = correlation_id

        print("\nMODEL ANSWER")
        print("------------")
        print(result.require_text())

        print("\nSAFE DIAGNOSTIC")
        print("---------------")
        print(diagnostic)

        print("\nUSER-FACING RESULT")
        print("------------------")
        print(result.require_text())
        print(f"Reference: {correlation_id}")

        final_status = "success"

    except ConnectionError as error:
        diagnostic = build_failure_diagnostic(
            error,
            provider="openai",
            model=MODEL,
        ).to_dict()

        diagnostic["correlation_id"] = correlation_id

        print("\nSAFE FAILURE DIAGNOSTIC")
        print("-----------------------")
        print(diagnostic)

        print("\nUSER-FACING RESULT")
        print("------------------")
        print(
            "The AI service is temporarily unavailable. "
            "Please try again later."
        )
        print(f"Reference: {correlation_id}")

        final_status = "fallback"

    print("\nTRACE SUMMARY")
    print("-------------")
    print(f"Correlation ID: {correlation_id}")
    print(f"Total attempts: {attempts['count']}")
    print(f"Final status: {final_status}")


if __name__ == "__main__":
    main()