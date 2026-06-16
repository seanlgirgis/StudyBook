"""PromptTemplate with several runtime variables."""

from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "Explain {topic} to a {audience} using {tone} language."
)

formatted = prompt.invoke(
    {
        "topic": "vector embeddings",
        "audience": "beginner",
        "tone": "friendly",
    }
)

print(formatted.to_string())
