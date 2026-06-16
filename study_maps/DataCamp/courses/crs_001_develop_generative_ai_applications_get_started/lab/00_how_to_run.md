# How to Run the Python Lab

Target folder:

```powershell
cd D:\Workarea\StudyBook\study_maps\DataCamp\courses\crs_001_develop_generative_ai_applications_get_started\lab\python
```

Activate the course environment first:

```powershell
D:\py_venv\rag_application_builder_foundation\Scripts\activate
```

## No-provider examples

These do not require model API keys:

```powershell
python .\01_prompt_template_one_variable.py
python .\02_prompt_template_multiple_variables.py
python .\03_chat_prompt_template.py
python .\04_few_shot_prompt_template.py
python .\05_lcel_local_pipeline.py
python .\06_runnable_parallel.py
python .\07_messages_placeholder.py
```

## OpenAI examples

These require `OPENAI_API_KEY`:

```powershell
$env:OPENAI_API_KEY = "your_key_here"
$env:OPENAI_MODEL = "gpt-5.4-nano"

python .\05b_lcel_openai_pipeline.py
python .\08_json_parser_shape.py
python .\09_provider_native_structured_output.py
python .\10_conversation_history_with_messages_placeholder.py
python .\11_update_conversation_history.py
python .\12_reusable_chat_function_with_history.py
python .\13_runnable_with_message_history.py
```

## IBM watsonx examples

These require IBM watsonx variables:

```powershell
$env:WATSONX_APIKEY = "your_watsonx_key_here"
$env:WATSONX_PROJECT_ID = "your_project_id_here"
$env:WATSONX_URL = "https://eu-gb.ml.cloud.ibm.com"
$env:WATSONX_MODEL_ID = "mistralai/mistral-small-3-1-24b-instruct-2503"

python .\05d_watsonx_smallest_test.py
python .\05c_lcel_watsonx_pipeline.py
python .\05f_provider_switching_lcel_pipeline.py
```

## Safety notes

Do not hard-code API keys inside Python files.

Use environment variables only.
