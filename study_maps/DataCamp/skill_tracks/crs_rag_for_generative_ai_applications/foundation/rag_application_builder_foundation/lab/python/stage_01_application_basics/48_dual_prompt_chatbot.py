"""Stage 1, Brick 48: Use a dual-prompt chatbot pattern.

Functionality studied:
    Keep application-controlled behavior separate from the user's message.

    Application prompt:
        Defines the chatbot's role, rules, and response style.

    User prompt:
        Contains the user's current question.

Reusable mechanics:
    - ChatMessage
    - ConversationRequest
    - OpenAITextProvider
"""

from rag_foundation.models.chat import ChatMessage
from rag_foundation.models.requests import ConversationRequest
from rag_foundation.providers.openai_text import OpenAITextProvider


APPLICATION_PROMPT = """
You are a patient RAG application tutor.

Rules:
- Use plain English.
- Answer in exactly two short sentences.
- Explain only the concept asked about.
- Do not add headings, bullets, examples, or follow-up offers.
""".strip()


USER_PROMPT = """
What is semantic search?
""".strip()


def main() -> None:
    provider = OpenAITextProvider()

    request = ConversationRequest(
        messages=[
            ChatMessage(
                role="system",
                content=APPLICATION_PROMPT,
            ),
            ChatMessage(
                role="user",
                content=USER_PROMPT,
            ),
        ],
        model="gpt-5.4-nano",
        temperature=0.0,
    )

    result = provider.generate_conversation(request)

    print("APPLICATION PROMPT")
    print("------------------")
    print(APPLICATION_PROMPT)

    print("\nUSER PROMPT")
    print("-----------")
    print(USER_PROMPT)

    print("\nCHATBOT RESPONSE")
    print("----------------")
    print(result.require_text())

    print("\nMESSAGE ORDER")
    print("-------------")

    for number, message in enumerate(
        request.messages,
        start=1,
    ):
        print(f"{number}. {message.role}")


if __name__ == "__main__":
    main()