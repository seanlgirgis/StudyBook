"""Stage 1, Brick 41: Observe repeated-call variability.

Functionality studied:
    Send the exact same request several times and compare the outputs.

Reusable mechanics:
    TextGenerationRequest, OpenAITextProvider, and TextGenerationResult
    are provided by rag_foundation.

Important:
    This brick does not change temperature or sampling controls.
    It only observes whether repeated calls naturally vary.
"""

from rag_foundation import (
    OpenAITextProvider,
    TextGenerationRequest,
)


NUMBER_OF_CALLS = 5

PROMPT = """
Write one short sentence explaining why good document chunking matters in RAG.
""".strip()

INSTRUCTIONS = """
Use plain English.
Return exactly one sentence.
Do not use bullets, headings, or follow-up offers.
""".strip()


def main() -> None:
    provider = OpenAITextProvider()

    request = TextGenerationRequest(
        prompt=PROMPT,
        instructions=INSTRUCTIONS,
        model="gpt-5.4-nano",
    )

    outputs: list[str] = []

    for call_number in range(1, NUMBER_OF_CALLS + 1):
        result = provider.generate(request)

        output = result.require_text().strip()
        outputs.append(output)

        print(f"CALL {call_number}")
        print("-" * 6)
        print(output)
        print(f"Output tokens: {result.output_tokens}")
        print()

    unique_outputs = set(outputs)

    print("SUMMARY")
    print("-------")
    print(f"Total calls: {len(outputs)}")
    print(f"Unique outputs: {len(unique_outputs)}")

    if len(unique_outputs) == 1:
        print("All calls returned identical text.")
    else:
        print("The repeated calls produced different wording.")


if __name__ == "__main__":
    main()