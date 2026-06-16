"""LCEL pipeline using an IBM watsonx chat model."""

import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ibm import ChatWatsonx


required_variables = (
    "WATSONX_APIKEY",
    "WATSONX_PROJECT_ID",
)

missing_variables = [
    variable_name
    for variable_name in required_variables
    if not os.getenv(variable_name)
]

if missing_variables:
    raise RuntimeError(
        "Missing required environment variables: "
        + ", ".join(missing_variables)
    )


model_id = os.getenv(
    "WATSONX_MODEL_ID",
    "mistralai/mistral-small-3-1-24b-instruct-2503",
)

watsonx_url = os.getenv(
    "WATSONX_URL",
    "https://eu-gb.ml.cloud.ibm.com",
)


prompt = PromptTemplate.from_template(
    "Topic: {topic}\n"
    "Explain it to a beginner in one short sentence "
    "of no more than 20 words."
)


model = ChatWatsonx(
    model_id=model_id,
    url=watsonx_url,
    project_id=os.environ["WATSONX_PROJECT_ID"],
    apikey=os.environ["WATSONX_APIKEY"],
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


print("MODEL")
print("-----")
print(model_id)

print("\nRESULT")
print("------")
print(result)