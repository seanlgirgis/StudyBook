"""Stage 1, Brick 28: Keep application state outside the model.

Functionality studied here:
    Python owns the state.
    The model receives only the state needed for the current response.

Mechanics:
    Handled by rag_foundation.
"""

from rag_foundation import (
    OpenAITextProvider,
    TextGenerationRequest,
)


def main() -> None:
    provider = OpenAITextProvider()

    # The application owns this state.
    state = {
        "topic": "vector embeddings",
        "user_level": "beginner",
        "preferred_style": "plain English",
    }

    prompt = f"""
Current topic:
{state["topic"]}

User level:
{state["user_level"]}

Preferred style:
{state["preferred_style"]}

Explain why this topic matters in RAG.
""".strip()

    request = TextGenerationRequest(
        prompt=prompt,
    )

    result = provider.generate(request)

    print("APPLICATION STATE")
    print("-----------------")
    print(state)

    print("\nMODEL RESULT")
    print("------------")
    print(result.text)


if __name__ == "__main__":
    main()