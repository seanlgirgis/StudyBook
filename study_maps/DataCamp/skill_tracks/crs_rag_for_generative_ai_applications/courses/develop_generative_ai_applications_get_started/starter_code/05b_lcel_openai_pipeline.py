"""LCEL pipeline using a real OpenAI chat model."""

import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

model_name = os.getenv(
    "OPENAI_MODEL",
    "gpt-5.4-nano",
)

prompt = PromptTemplate.from_template(
    "Topic: {topic}\n"
    "Return one concise beginner-friendly explanation."
)

model = ChatOpenAI(
    model=model_name,
)

chain = (
    prompt
    | model
    | StrOutputParser()
)

result = chain.invoke(
    {
        "topic": "LCEL",
    }
)

print(result)