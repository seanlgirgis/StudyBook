"""Smallest low-token IBM watsonx LangChain test."""

import os

from langchain_ibm import ChatWatsonx


required_variables = (
    "WATSONX_APIKEY",
    "WATSONX_PROJECT_ID",
    "WATSONX_URL",
)

missing = [
    name
    for name in required_variables
    if not os.getenv(name)
]

if missing:
    raise RuntimeError(
        "Missing environment variables: "
        + ", ".join(missing)
    )


model = ChatWatsonx(
    model_id="mistralai/mistral-small-3-1-24b-instruct-2503",
    apikey=os.environ["WATSONX_APIKEY"],
    project_id=os.environ["WATSONX_PROJECT_ID"],
    url=os.environ["WATSONX_URL"],
    params={
        "decoding_method": "greedy",
        "max_new_tokens": 10,
    },
)

response = model.invoke(
    "Reply with exactly two words: IBM OK"
)

print(response.content)