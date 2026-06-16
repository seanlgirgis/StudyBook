"""Stage 1, Tiny Block 9: Reject invalid provider configuration.

Mechanics:
    Handled by rag_foundation.

Functionality studied here:
    The provider validates its configuration before sending an API request.
"""

from rag_foundation import (
    ConfigurationError,
    OpenAITextProvider,
)


def main() -> None:
    try:
        provider = OpenAITextProvider(
            default_model="   ",
        )

        print(provider.default_model)

    except ConfigurationError as error:
        print("PROVIDER CONFIGURATION REJECTED")
        print("-------------------------------")
        print(error)


if __name__ == "__main__":
    main()