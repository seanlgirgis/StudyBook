"""Reuse one structured-output LCEL chain for multiple topics."""

import os

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


class TopicSummary(BaseModel):
    """Validated beginner-friendly explanation of one technical topic."""

    topic: str = Field(
        description="The technical concept being explained."
    )

    explanation: str = Field(
        description=(
            "A concise beginner-friendly explanation "
            "using no more than two sentences."
        )
    )


if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError(
        "OPENAI_API_KEY is not available."
    )


prompt = PromptTemplate.from_template(
    "You are a patient technical tutor.\n"
    "Explain the following topic for a beginner.\n"
    "Keep the explanation concise and practical.\n\n"
    "Topic: {topic}"
)


model = ChatOpenAI(
    model=os.getenv(
        "OPENAI_MODEL",
        "gpt-5.4-nano",
    ),
)


structured_model = model.with_structured_output(
    TopicSummary
)


chain = (
    prompt
    | structured_model
)


topics = [
    "prompt templates",
    "LangChain Expression Language",
    "RunnableParallel",
]


results: list[TopicSummary] = []


print("REUSABLE STRUCTURED-OUTPUT CHAIN")
print("--------------------------------")

for index, topic in enumerate(
    topics,
    start=1,
):
    print(
        f"\nRUN {index}"
    )
    print(
        "-" * 20
    )
    print(
        "Input topic:",
        topic,
    )

    result = chain.invoke(
        {
            "topic": topic,
        }
    )

    if not isinstance(
        result,
        TopicSummary,
    ):
        raise RuntimeError(
            "Expected a TopicSummary instance."
        )

    if result.topic.strip() == "":
        raise RuntimeError(
            "The topic field must not be blank."
        )

    if result.explanation.strip() == "":
        raise RuntimeError(
            "The explanation field must not be blank."
        )

    results.append(
        result
    )

    print(
        "Returned type:",
        type(result).__name__,
    )
    print(
        "Topic:",
        result.topic,
    )
    print(
        "Explanation:",
        result.explanation,
    )


print("\nCOLLECTED RESULTS")
print("-----------------")

for result in results:
    print(
        result.model_dump()
    )


print("\nFINAL CHECK")
print("-----------")

if len(results) != len(topics):
    raise RuntimeError(
        "Not every input produced a structured result."
    )

print(
    "PASS: one reusable LCEL chain processed "
    f"{len(results)} topics and returned a validated "
    "TopicSummary object for every invocation."
)