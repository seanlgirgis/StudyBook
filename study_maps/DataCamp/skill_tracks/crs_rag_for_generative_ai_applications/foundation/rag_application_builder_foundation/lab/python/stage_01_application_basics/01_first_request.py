"""
Stage 1, Tiny Block 1: Make one visible OpenAI request.

Input:
    A short prompt stored in PROMPT.

What local Python does:
    1. Creates a TextGenerationRequest.
    2. Sends it through OpenAITextProvider.
    3. Prints the normalized result.

What the shared library does:
    1. Reads the API key and model from the environment.
    2. Creates the OpenAI client.
    3. Sends the request.
    4. Extracts text, request ID, and token usage.

What the model does:
    Generates the response text.
"""

from __future__ import annotations

from rag_foundation import (
    OpenAITextProvider,
    TextGenerationRequest,
)


PROMPT = """
In one plain-English sentence, explain what an AI application is.
""".strip()


def main() -> None:
    """Create one request, send it, and display the result."""

    request = TextGenerationRequest(
        prompt=PROMPT,
    )

    provider = OpenAITextProvider()

    print("INPUT")
    print("-----")
    print(request.prompt)

    print("\nLOCAL PYTHON")
    print("------------")
    print(f"Provider: {provider.PROVIDER_NAME}")
    print(f"Default model: {provider.default_model}")
    print("Sending one request...")

    result = provider.generate(request)

    print("\nMODEL OUTPUT")
    print("------------")
    print(result.text)

    print("\nREQUEST ID")
    print("----------")
    print(result.request_id)

    print("\nTOKEN USAGE")
    print("-----------")
    print(f"Input tokens: {result.input_tokens}")
    print(f"Output tokens: {result.output_tokens}")
    print(f"Total tokens: {result.total_tokens}")


if __name__ == "__main__":
    main()