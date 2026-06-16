"""Stage 1, Brick 49: Retry a transient generation failure.

Functionality studied:
    Wrap a model-generation operation in a bounded retry policy.

Reusable mechanics:
    - RetryPolicy
    - run_with_retry()
    - OpenAITextProvider
    - TextGenerationRequest

Important:
    This brick simulates two temporary failures before making the real
    provider call. It does not intentionally send failed API requests.
"""

from rag_foundation import (
    OpenAITextProvider,
    TextGenerationRequest,
)
from rag_foundation.retry import (
    RetryPolicy,
    run_with_retry,
)


SIMULATED_FAILURES = 2


def main() -> None:
    provider = OpenAITextProvider()

    request = TextGenerationRequest(
        instructions=(
            "Use plain English. "
            "Return exactly one short sentence."
        ),
        prompt=(
            "Explain why bounded retries are useful "
            "in an AI application."
        ),
        model="gpt-5.4-nano",
        temperature=0.0,
    )

    attempts = {"count": 0}

    def generate_with_simulated_failure() -> str:
        """Fail temporarily, then perform the real generation call."""

        attempts["count"] += 1

        print(f"Attempt {attempts['count']}")

        if attempts["count"] <= SIMULATED_FAILURES:
            raise ConnectionError(
                "Simulated temporary connection failure."
            )

        result = provider.generate(request)

        return result.require_text()

    answer = run_with_retry(
        generate_with_simulated_failure,
        retry_on=(ConnectionError,),
        policy=RetryPolicy(
            max_attempts=3,
            delay_seconds=0,
        ),
    )

    print("\nFINAL ANSWER")
    print("------------")
    print(answer)

    print("\nRETRY SUMMARY")
    print("-------------")
    print(f"Total attempts: {attempts['count']}")
    print(f"Simulated failures: {SIMULATED_FAILURES}")
    print("Final status: success")


if __name__ == "__main__":
    main()