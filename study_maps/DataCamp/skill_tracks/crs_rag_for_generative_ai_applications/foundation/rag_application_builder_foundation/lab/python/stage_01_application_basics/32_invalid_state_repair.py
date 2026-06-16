"""Stage 1, Brick 32: Repair invalid chat state.

Mechanics:
    Generic JSON parsing and answer-plus-state extraction are supplied by
    rag_foundation.

Functionality studied here:
    Invalid application state is rejected, repaired by the model, and
    validated again before Python accepts it.
"""

import json

from rag_foundation import (
    OpenAITextProvider,
    TextGenerationRequest,
)
from rag_foundation.models.results import TextGenerationResult
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


def validate_local_state(state: dict) -> dict:
    """Run the same validator against local state."""
    return validate_state(dict(state))


def repair_state(
    provider: OpenAITextProvider,
    invalid_state: dict,
    validation_error: str,
) -> dict:
    """Ask the model for repaired state and validate it again."""

    request = TextGenerationRequest(
        instructions=(
            "Return valid JSON only with exactly two top-level fields: "
            "answer and updated_state. "
            "answer must briefly describe the repair. "
            "updated_state must contain topic, user_level, and last_question. "
            "user_level must be beginner, intermediate, or advanced."
        ),
        prompt=(
            "Repair this invalid application state while preserving meaning:\n"
            f"{json.dumps(invalid_state, indent=2)}\n\n"
            "Validation error:\n"
            f"{validation_error}"
        ),
        model="gpt-5.4-mini",
    )

    generation_result = provider.generate(request)

    repaired_turn = parse_stateful_turn(
        generation_result=generation_result,
        validate_state=validate_state,
    )

    return repaired_turn.updated_state


def main() -> None:
    provider = OpenAITextProvider()

    invalid_state = {
        "topic": "vector embeddings",
        "user_level": "expert",
        "last_question": "How are embeddings used in RAG?",
    }

    print("INVALID STATE")
    print("-------------")
    print(invalid_state)

    try:
        state = validate_local_state(invalid_state)

    except (TypeError, ValueError, KeyError) as error:
        print("\nVALIDATION FAILED")
        print("-----------------")
        print(error)

        state = repair_state(
            provider=provider,
            invalid_state=invalid_state,
            validation_error=str(error),
        )

    print("\nREPAIRED AND VALIDATED STATE")
    print("----------------------------")
    print(state)


if __name__ == "__main__":
    main()
