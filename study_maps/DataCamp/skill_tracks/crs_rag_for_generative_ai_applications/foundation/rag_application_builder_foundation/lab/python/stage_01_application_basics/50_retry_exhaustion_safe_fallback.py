"""Stage 1, Brick 50: Handle retry exhaustion with a safe fallback.

Functionality studied:
    Attempt a retryable operation several times and return a controlled
    fallback response when every allowed attempt fails.

Reusable mechanics:
    - RetryPolicy
    - run_with_retry()

Application-specific behavior:
    - which exception types are retryable;
    - what fallback message should be returned;
    - what information may safely be shown to the user.
"""

from rag_foundation.retry import (
    RetryPolicy,
    run_with_retry,
)


MAX_ATTEMPTS = 3

SAFE_FALLBACK = (
    "The AI service is temporarily unavailable. "
    "Please try again later."
)


def main() -> None:
    attempts = {"count": 0}

    def always_failing_operation() -> str:
        """Simulate a provider operation that never recovers."""

        attempts["count"] += 1

        print(f"Attempt {attempts['count']}")

        raise ConnectionError(
            "Simulated provider connection failure."
        )

    try:
        answer = run_with_retry(
            always_failing_operation,
            retry_on=(ConnectionError,),
            policy=RetryPolicy(
                max_attempts=MAX_ATTEMPTS,
                delay_seconds=0,
            ),
        )

        status = "success"

    except ConnectionError as error:
        answer = SAFE_FALLBACK
        status = "fallback"

        print("\nINTERNAL ERROR")
        print("--------------")
        print(type(error).__name__)
        print(str(error))

    print("\nUSER-FACING RESULT")
    print("------------------")
    print(answer)

    print("\nEXECUTION SUMMARY")
    print("-----------------")
    print(f"Maximum attempts: {MAX_ATTEMPTS}")
    print(f"Actual attempts: {attempts['count']}")
    print(f"Final status: {status}")


if __name__ == "__main__":
    main()