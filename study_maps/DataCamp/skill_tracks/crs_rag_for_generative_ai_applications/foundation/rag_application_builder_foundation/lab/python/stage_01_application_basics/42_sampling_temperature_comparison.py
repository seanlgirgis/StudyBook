"""Stage 1, Brick 42: Compare low and high sampling temperatures.

Functionality studied:
    Send the same prompt repeatedly with two temperature settings and
    compare the amount of wording variation.

Reusable mechanics:
    Temperature validation and provider translation are handled by
    rag_foundation.

Important:
    Temperature influences sampling behavior, but it does not guarantee
    identical output at low values or unique output at high values.
"""

from rag_foundation import (
    OpenAITextProvider,
    TextGenerationRequest,
)
from rag_foundation.exceptions import ProviderError


MODEL = "gpt-5.4-nano"

NUMBER_OF_CALLS = 4

LOW_TEMPERATURE = 0.0
HIGH_TEMPERATURE = 1.5

PROMPT = """
Write one short sentence explaining why retrieval matters in RAG.
""".strip()

INSTRUCTIONS = """
Use plain English.
Return exactly one sentence.
Do not use headings, bullets, or follow-up offers.
""".strip()


def run_temperature_group(
    provider: OpenAITextProvider,
    temperature: float,
) -> list[str]:
    """Run the same request several times at one temperature."""

    outputs: list[str] = []

    for call_number in range(
        1,
        NUMBER_OF_CALLS + 1,
    ):
        request = TextGenerationRequest(
            prompt=PROMPT,
            instructions=INSTRUCTIONS,
            model=MODEL,
            temperature=temperature,
        )

        result = provider.generate(request)

        output = result.require_text().strip()
        outputs.append(output)

        print(f"CALL {call_number}")
        print("-" * 6)
        print(output)
        print(f"Output tokens: {result.output_tokens}")
        print()

    return outputs


def print_summary(
    label: str,
    outputs: list[str],
) -> None:
    """Print a small variability summary."""

    unique_outputs = set(outputs)

    print(f"{label} SUMMARY")
    print("-" * (len(label) + 8))
    print(f"Total calls: {len(outputs)}")
    print(f"Unique outputs: {len(unique_outputs)}")

    if len(unique_outputs) == 1:
        print("All outputs were identical.")
    else:
        print("The outputs used different wording.")


def main() -> None:
    provider = OpenAITextProvider()

    try:
        print("LOW TEMPERATURE")
        print("===============")
        print(f"Temperature: {LOW_TEMPERATURE}\n")

        low_outputs = run_temperature_group(
            provider=provider,
            temperature=LOW_TEMPERATURE,
        )

        print_summary(
            label="LOW TEMPERATURE",
            outputs=low_outputs,
        )

        print("\nHIGH TEMPERATURE")
        print("================")
        print(f"Temperature: {HIGH_TEMPERATURE}\n")

        high_outputs = run_temperature_group(
            provider=provider,
            temperature=HIGH_TEMPERATURE,
        )

        print_summary(
            label="HIGH TEMPERATURE",
            outputs=high_outputs,
        )

        print("\nCOMPARISON")
        print("----------")
        print(
            "Low-temperature unique outputs: "
            f"{len(set(low_outputs))}"
        )
        print(
            "High-temperature unique outputs: "
            f"{len(set(high_outputs))}"
        )

    except ProviderError as error:
        print("SAMPLING CONTROL NOT ACCEPTED")
        print("-----------------------------")
        print(error)
        print(
            "\nThe shared library passed temperature correctly, "
            "but this provider/model combination rejected it."
        )


if __name__ == "__main__":
    main()