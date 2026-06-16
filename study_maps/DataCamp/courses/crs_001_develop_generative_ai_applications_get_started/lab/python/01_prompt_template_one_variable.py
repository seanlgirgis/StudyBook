"""Smallest PromptTemplate example: one changing value."""

from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "Explain {topic} in two plain-English sentences."
)

formatted = prompt.invoke(
    {"topic": "semantic search"}
)

print(formatted.to_string())
