"""Generate and parse a structured topic summary with a real OpenAI model."""

import os

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


class TopicSummary(BaseModel):
    """Structured explanation returned by the model."""

    topic: str = Field(
        description="The concept being explained."
    )
    explanation: str = Field(
        description="A short plain-English explanation."
    )


if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError(
        "OPENAI_API_KEY is not available."
    )


parser = JsonOutputParser(
    pydantic_object=TopicSummary
)


prompt = PromptTemplate(
    template=(
        "You are a patient technical tutor.\n"
        "Explain the following topic for a beginner.\n\n"
        "Topic: {topic}\n\n"
        "{format_instructions}\n\n"
        "Return only the requested JSON."
    ),
    input_variables=[
        "topic",
    ],
    partial_variables={
        "format_instructions": (
            parser.get_format_instructions()
        ),
    },
)


model = ChatOpenAI(
    model=os.getenv(
        "OPENAI_MODEL",
        "gpt-5.4-nano",
    ),
)


chain = (
    prompt
    | model
    | parser
)


result = chain.invoke(
    {
        "topic": "prompt templates",
    }
)


print("PARSED RESULT")
print("-------------")
print(result)

print("\nFIELD ACCESS")
print("------------")
print("Topic:", result["topic"])
print(
    "Explanation:",
    result["explanation"],
)

print("\nTYPE CHECK")
print("----------")
print(type(result).__name__)


if not isinstance(result, dict):
    raise RuntimeError(
        "Expected JsonOutputParser to return a dictionary."
    )

if set(result) != {
    "topic",
    "explanation",
}:
    raise RuntimeError(
        "The parsed result did not contain the expected fields."
    )


print("\nFINAL CHECK")
print("-----------")
print(
    "PASS: the model returned JSON and "
    "JsonOutputParser converted it into a Python dictionary."
)