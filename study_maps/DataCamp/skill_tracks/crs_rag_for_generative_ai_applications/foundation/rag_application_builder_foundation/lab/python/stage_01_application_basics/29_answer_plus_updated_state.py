"""Stage 1, Brick 29: Answer plus updated state across two calls.

Mechanics:
    Generic JSON parsing and answer-plus-state extraction are supplied by
    rag_foundation.

Functionality studied here:
    Python stores application state, validates the model's proposed update,
    and sends the trusted updated state into a second call.
"""

import json

from rag_foundation import (
    OpenAITextProvider,
    TextGenerationRequest,
)
from rag_foundation.stateful import parse_stateful_turn


def validate_state(state: dict) -> dict:
    """Validate this application's teaching-state fields."""

    required_fields = [
        "topic",
        "user_level",
        "last_question",
    ]

    for field_name in required_fields:
        if field_name not in state:
            raise ValueError(
                f"Missing state field: {field_name}"
            )

        if not isinstance(state[field_name], str):
            raise TypeError(
                f"{field_name} must be a string."
            )

        state[field_name] = state[field_name].strip()

        if state[field_name] == "":
            raise ValueError(
                f"{field_name} must not be blank."
            )

    allowed_levels = [
        "beginner",
        "intermediate",
        "advanced",
    ]

    if state["user_level"] not in allowed_levels:
        raise ValueError(
            "user_level must be beginner, intermediate, or advanced."
        )

    return state


def run_turn(
    provider: OpenAITextProvider,
    state: dict,
    user_message: str,
):
    """Send one stateful turn and return the shared result object."""

    request = TextGenerationRequest(

        instructions = """
        Return valid JSON only.

        Use exactly this structure:

        {
        "answer": "answer for the user",
        "updated_state": {
            "topic": "the specific current subject of the latest user message",
            "user_level": "beginner, intermediate, or advanced",
            "last_question": "the user's latest question"
        }
        }

        Rules for updated_state:

        1. Update topic to reflect the most specific subject discussed in the latest
        user message.

        2. Do not leave topic unchanged when the conversation moves from a broad
        subject to a more specific subject.

        3. Preserve user_level unless the conversation provides strong evidence that
        the learner level changed.

        4. Set last_question to the latest user message.

        Examples:

        If the old topic is:
        "general AI concepts"

        and the user asks:
        "What is a vector embedding?"

        then the new topic should be:
        "vector embeddings"

        If the old topic is:
        "vector embeddings"

        and the user asks:
        "How is it used in RAG?"

        then the new topic should be:
        "vector embeddings in RAG"

        Do not add markdown or explanations outside the JSON.
        """.strip(),


        prompt=(
            "Current application state:\n"
            f"{json.dumps(state, indent=2)}\n\n"
            "New user message:\n"
            f"{user_message}"
        ),
        model="gpt-5.4-mini",
    )

    generation_result = provider.generate(request)

    return parse_stateful_turn(
        generation_result=generation_result,
        validate_state=validate_state,
    )


def main() -> None:
    provider = OpenAITextProvider()

    state = {
        "topic": "general AI concepts",
        "user_level": "beginner",
        "last_question": "none",
    }

    print("INITIAL STATE")
    print("-------------")
    print(state)

    first_turn = run_turn(
        provider=provider,
        state=state,
        user_message="What is a vector embedding?",
    )

    state = first_turn.updated_state

    print("\nTURN 1 ANSWER")
    print("-------------")
    print(first_turn.answer)

    print("\nSTATE AFTER TURN 1")
    print("------------------")
    print(state)

    second_turn = run_turn(
        provider=provider,
        state=state,
        user_message="How is it used in RAG?",
    )

    state = second_turn.updated_state

    print("\nTURN 2 ANSWER")
    print("-------------")
    print(second_turn.answer)

    print("\nSTATE AFTER TURN 2")
    print("------------------")
    print(state)


if __name__ == "__main__":
    main()
