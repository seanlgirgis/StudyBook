"""LCEL pipeline using local functions, so no API key is required."""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

prompt = PromptTemplate.from_template(
    "Topic: {topic}\nReturn one concise explanation."
)


def local_model(prompt_value):
    """Stand in for a model while demonstrating the pipeline shape."""

    prompt_text = prompt_value.to_string()

    return (
        "LOCAL MODEL RESULT: "
        + prompt_text.replace("\n", " | ")
    )


chain = (
    prompt
    | RunnableLambda(local_model)
    | StrOutputParser()
)

result = chain.invoke(
    {"topic": "LCEL"}
)

print(result)
