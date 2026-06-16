"""Run the same LCEL pipeline with OpenAI and IBM watsonx."""

import os
import warnings

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ibm import ChatWatsonx
from langchain_openai import ChatOpenAI


warnings.filterwarnings(
    "ignore",
    message=r"This model is a Non-IBM Product.*",
)


required_environment_variables = (
    "OPENAI_API_KEY",
    "WATSONX_APIKEY",
    "WATSONX_PROJECT_ID",
)

missing_environment_variables = [
    variable_name
    for variable_name in required_environment_variables
    if not os.getenv(variable_name)
]

if missing_environment_variables:
    raise RuntimeError(
        "Missing required environment variables: "
        + ", ".join(missing_environment_variables)
    )


prompt = PromptTemplate.from_template(
    "You are a technical tutor explaining LangChain concepts.\n"
    "Topic: {topic}\n"
    "Explain it to a beginner in one short sentence "
    "using no more than 25 words."
)

parser = StrOutputParser()


openai_model = ChatOpenAI(
    model=os.getenv(
        "OPENAI_MODEL",
        "gpt-5.4-nano",
    ),
)


watsonx_model = ChatWatsonx(
    model_id=os.getenv(
        "WATSONX_MODEL_ID",
        "mistralai/mistral-small-3-1-24b-instruct-2503",
    ),
    url=os.getenv(
        "WATSONX_URL",
        "https://eu-gb.ml.cloud.ibm.com",
    ),
    project_id=os.environ[
        "WATSONX_PROJECT_ID"
    ],
    apikey=os.environ[
        "WATSONX_APIKEY"
    ],
    params={
        "temperature": 0,
        "max_tokens": 40,
    },
)


openai_chain = (
    prompt
    | openai_model
    | parser
)

watsonx_chain = (
    prompt
    | watsonx_model
    | parser
)


input_data = {
    "topic": "LangChain Expression Language (LCEL)",
}


print("OPENAI RESULT")
print("-------------")

openai_result = openai_chain.invoke(
    input_data
)

print(openai_result)


print("\nWATSONX RESULT")
print("--------------")

watsonx_result = watsonx_chain.invoke(
    input_data
)

print(watsonx_result)


print("\nFINAL CHECK")
print("-----------")

if not openai_result.strip():
    raise RuntimeError(
        "OpenAI returned an empty result."
    )

if not watsonx_result.strip():
    raise RuntimeError(
        "Watsonx returned an empty result."
    )

print(
    "PASS: the same prompt, parser, input, and LCEL "
    "shape ran successfully against two model providers."
)