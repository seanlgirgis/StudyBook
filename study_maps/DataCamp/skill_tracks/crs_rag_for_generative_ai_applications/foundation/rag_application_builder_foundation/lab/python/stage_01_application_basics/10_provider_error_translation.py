"""Stage 1, Tiny Block 10: Translate a provider failure.

Functionality studied here:
    OpenAI-specific errors are converted into our library's ProviderError.

No real API request is made.
"""

from unittest.mock import Mock

from openai import OpenAIError

from rag_foundation import (
    OpenAITextProvider,
    ProviderError,
    TextGenerationRequest,
)


def main() -> None:
    # Build a fake OpenAI client.
    fake_client = Mock()

    # Make the fake API call fail deliberately.
    fake_client.responses.create.side_effect = OpenAIError(
        "Simulated OpenAI failure."
    )

    provider = OpenAITextProvider(
        client=fake_client,
        default_model="test-model",
    )

    request = TextGenerationRequest(
        prompt="Explain RAG.",
    )

    try:
        provider.generate(request)

    except ProviderError as error:
        print("PROVIDER ERROR CAUGHT")
        print("---------------------")
        print(f"Provider: {error.provider}")
        print(f"Message: {error}")
        print(f"Original error: {error.original_error}")


if __name__ == "__main__":
    main()