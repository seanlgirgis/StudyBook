# Troubleshooting Notes

## `ModuleNotFoundError: langchain_core`

Install LangChain dependencies into the active virtual environment.

## OpenAI key missing

Set:

```powershell
$env:OPENAI_API_KEY = "your_key_here"
```

## Watsonx key or project missing

Set:

```powershell
$env:WATSONX_APIKEY = "your_key_here"
$env:WATSONX_PROJECT_ID = "your_project_id_here"
$env:WATSONX_URL = "https://eu-gb.ml.cloud.ibm.com"
```

## Watsonx model unsupported

Use a model supported in the selected IBM Cloud region. The tested working model was:

```text
mistralai/mistral-small-3-1-24b-instruct-2503
```

## LCEL interpreted incorrectly

Use the full phrase:

```text
LangChain Expression Language (LCEL)
```

instead of only the acronym.
