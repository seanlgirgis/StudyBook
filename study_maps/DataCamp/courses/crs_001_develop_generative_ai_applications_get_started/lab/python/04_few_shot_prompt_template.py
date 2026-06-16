"""Small few-shot classification prompt without a provider call."""

from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

example_prompt = PromptTemplate.from_template(
    "Text: {text}\nCategory: {category}"
)

examples = [
    {
        "text": "I was charged twice.",
        "category": "billing",
    },
    {
        "text": "The application will not start.",
        "category": "technical",
    },
]

prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="Classify the support request using the examples.",
    suffix="Text: {request}\nCategory:",
    input_variables=["request"],
)

print(
    prompt.invoke(
        {"request": "My invoice has the wrong amount."}
    ).to_string()
)
