"""Stage 1, Brick 30: Represent chat state with a structured object.

New behavior proved here:
    Application state is no longer a loose dictionary.

    Python creates a ChatState object with:
    - known fields;
    - validation;
    - predictable attribute access.

No model call is needed in this brick.
"""


class ChatState:
    """Store and validate application-owned chat state.

    Args:
        topic:
            Current discussion topic.

        user_level:
            Current learner level.

        last_question:
            Most recent user question.
    """

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

    def to_dict(self) -> dict:
        """Return the state as a normal dictionary.

        This is useful when the state must be:
        - converted to JSON;
        - sent to a model;
        - logged;
        - stored.
        """
        return {
            "topic": self.topic,
            "user_level": self.user_level,
            "last_question": self.last_question,
        }


def main() -> None:
    state = ChatState(
        topic="vector embeddings",
        user_level="beginner",
        last_question="What is a vector embedding?",
    )

    print("STRUCTURED CHAT STATE")
    print("---------------------")
    print(f"Topic: {state.topic}")
    print(f"User level: {state.user_level}")
    print(f"Last question: {state.last_question}")

    print("\nDICTIONARY FORM")
    print("---------------")
    print(state.to_dict())


if __name__ == "__main__":
    main()