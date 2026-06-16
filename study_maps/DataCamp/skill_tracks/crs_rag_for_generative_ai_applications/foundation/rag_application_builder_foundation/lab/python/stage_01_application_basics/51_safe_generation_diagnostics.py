"""Stage 1, Brick 51: Record safe generation diagnostics.

Functionality studied:
    Build safe operational records for both successful and failed
    generation operations.

Reusable mechanics:
    - build_success_diagnostic()
    - build_failure_diagnostic()
    - GenerationDiagnostic
    - OpenAITextProvider
    - TextGenerationRequest

Safety rule:
    Diagnostics contain operational metadata, not prompts, generated
    content, credentials, raw responses, or exception messages.
"""

from rag_foundation import (
    OpenAITextProvider,
    TextGenerationRequest,
)
from rag_foundation.diagnostics import (
    build_failure_diagnostic,
    build_success_diagnostic,
)


MODEL = "gpt-5.4-nano"


def main() -> None:
    provider = OpenAITextProvider()

    request = TextGenerationRequest(
        instructions=(
            "Use plain English. "
            "Return exactly one short sentence."
        ),
        prompt=(
            "Explain why application diagnostics should avoid "
            "recording sensitive prompt content."
        ),
        model=MODEL,
        temperature=0.0,
    )

    result = provider.generate(request)

    success_diagnostic = build_success_diagnostic(
        result
    )

    simulated_error = ConnectionError(
        "API key secret-123 failed while sending "
        "private customer account information."
    )

    failure_diagnostic = build_failure_diagnostic(
        simulated_error,
        provider="openai",
        model=MODEL,
    )

    print("MODEL ANSWER")
    print("------------")
    print(result.require_text())

    print("\nSUCCESS DIAGNOSTIC")
    print("------------------")
    print(success_diagnostic.to_dict())

    print("\nFAILURE DIAGNOSTIC")
    print("------------------")
    print(failure_diagnostic.to_dict())

    combined_diagnostics = (
        str(success_diagnostic.to_dict())
        + str(failure_diagnostic.to_dict())
    )

    forbidden_values = [
        request.prompt,
        result.require_text(),
        "secret-123",
        "private customer account information",
        str(simulated_error),
    ]

    leaked_values = [
        value
        for value in forbidden_values
        if value in combined_diagnostics
    ]

    print("\nSAFETY CHECK")
    print("------------")
    print(f"Forbidden values found: {len(leaked_values)}")

    if leaked_values:
        print("Diagnostic safety check failed.")
    else:
        print("No prompt, answer, secret, or error message was recorded.")


if __name__ == "__main__":
    main()