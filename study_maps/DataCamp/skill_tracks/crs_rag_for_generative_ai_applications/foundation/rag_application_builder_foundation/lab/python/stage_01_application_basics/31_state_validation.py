"""Stage 1, Brick 31: Reject invalid structured chat state.

New behavior proved here:
    ChatState validates its fields when Python creates the object.

No model call is made.
"""


class ChatState:
    """Store and validate application-owned chat state."""

    ALLOWED_USER_LEVELS = [
        "beginner",
        "intermediate",
        "advanced",
    ]

    def __init__(
        self,
        topic: str,
        user_level: str,
        last_question: str,
    ) -> None:
        self.topic = ChatState._clean_required_text(
            topic,
            "topic",
        )

        self.user_level = ChatState._clean_user_level(
            user_level
        )

        self.last_question = ChatState._clean_required_text(
            last_question,
            "last_question",
        )

    @staticmethod
    def _clean_required_text(
        value: str,
        field_name: str,
    ) -> str:
        """Return cleaned required text."""
        if not isinstance(value, str):
            raise TypeError(
                f"{field_name} must be a string."
            )

        cleaned_value = value.strip()

        if cleaned_value == "":
            raise ValueError(
                f"{field_name} must not be blank."
            )

        return cleaned_value

    @staticmethod
    def _clean_user_level(
        user_level: str,
    ) -> str:
        """Return a valid normalized user level."""
        cleaned_level = ChatState._clean_required_text(
            user_level,
            "user_level",
        ).lower()

        if cleaned_level not in ChatState.ALLOWED_USER_LEVELS:
            raise ValueError(
                "user_level must be beginner, "
                "intermediate, or advanced."
            )

        return cleaned_level


def main() -> None:
    try:
        state = ChatState(
            topic="vector embeddings",
            user_level="expert",
            last_question="How are embeddings used in RAG?",
        )

        print(state.user_level)

    except ValueError as error:
        print("STATE REJECTED")
        print("--------------")
        print(error)


if __name__ == "__main__":
    main()