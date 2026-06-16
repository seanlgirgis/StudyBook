from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)


class TemporaryServiceError(Exception):
    """Represents a failure that may succeed when retried."""


attempt_number = 0


@retry(
    retry=retry_if_exception_type(TemporaryServiceError),
    stop=stop_after_attempt(4),
    wait=wait_exponential(
        multiplier=1,
        min=1,
        max=4,
    ),
    reraise=True,
)
def call_temporary_service() -> str:
    global attempt_number
    attempt_number += 1

    print(f"Attempt {attempt_number}")

    if attempt_number < 3:
        raise TemporaryServiceError(
            "Temporary failure. Please retry."
        )

    return "Service call succeeded."


try:
    result = call_temporary_service()
    print(result)

except TemporaryServiceError as exc:
    print("The service failed after all retry attempts.")
    print(exc)