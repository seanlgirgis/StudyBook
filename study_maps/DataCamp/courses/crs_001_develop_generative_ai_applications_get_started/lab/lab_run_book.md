# Lab Run Book — Develop Generative AI Applications: Get Started

## Lab status

```text
Lab coverage: DEVELOPING → STRONG for Module 1 and Module 2 local patterns
Coursera Flask application lab: still to be completed and recorded
```

## Chapter-to-lab mapping

| Module | Lab files | What they prove |
|---|---|---|
| Module 1 | `01` to `04` | PromptTemplate, ChatPromptTemplate, few-shot prompting |
| Module 2 | `05` to `13` | LCEL, provider adapters, RunnableParallel, parsers, structured output, history |
| Module 3 | To be added | Model selection and Flask application delivery |

## Run order

### 1. Prompt template basics

```powershell
python .\01_prompt_template_one_variable.py
python .\02_prompt_template_multiple_variables.py
python .\03_chat_prompt_template.py
python .\04_few_shot_prompt_template.py
```

Memory rule:

```text
PromptTemplate → formatted text
ChatPromptTemplate → role-based messages
FewShotPromptTemplate → examples plus new input
```

### 2. LCEL basics

```powershell
python .\05_lcel_local_pipeline.py
python .\05b_lcel_openai_pipeline.py
```

Memory rule:

```text
prompt | model | parser
```

### 3. Provider switching

```powershell
python .\05d_watsonx_smallest_test.py
python .\05c_lcel_watsonx_pipeline.py
python .\05f_provider_switching_lcel_pipeline.py
```

What to verify:

```text
Same prompt + same parser + same input + same LCEL shape
Different model adapter
```

Provider abstraction does not guarantee identical wording or identical interpretation.

### 4. Runnables and parallel work

```powershell
python .\06_runnable_parallel.py
```

Memory rule:

```text
Dependent steps → sequence
Independent branches → RunnableParallel
```

### 5. Parsers and structured output

```powershell
python .\08_json_parser_shape.py
python .\09_provider_native_structured_output.py
```

Memory rule:

```text
JsonOutputParser → dict
with_structured_output(PydanticModel) → validated object
```

### 6. Conversation history

```powershell
python .\10_conversation_history_with_messages_placeholder.py
python .\11_update_conversation_history.py
python .\12_reusable_chat_function_with_history.py
python .\13_runnable_with_message_history.py
```

Memory rule:

```text
MessagesPlaceholder → where history goes
HumanMessage / AIMessage → what history contains
```

`13_runnable_with_message_history.py` is retained as legacy enrichment because it emitted a deprecation warning. The production direction is LangGraph persistence, but that is outside the core course path.

## Exact observed outputs to preserve

Record successful outputs in:

```text
lab/expected_outputs/
```

Suggested files:

```text
01_prompt_template_one_variable.txt
02_prompt_template_multiple_variables.txt
03_chat_prompt_template.txt
...
```

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `ModuleNotFoundError: langchain_core` | LangChain packages are missing | Install course requirements in the active venv |
| `OPENAI_API_KEY is not available` | OpenAI env var not set | Set `$env:OPENAI_API_KEY` |
| Watsonx model not supported | Wrong region or model ID | Use London endpoint and supported Mistral model |
| Watsonx explains liquid cooling for LCEL | Acronym ambiguity | Use full phrase `LangChain Expression Language (LCEL)` |
| `RunnableWithMessageHistory is deprecated` | Legacy LangChain pattern | Keep as enrichment; prefer LangGraph later |

## Completion standard

This lab is considered strong when:

1. all no-provider examples run;
2. OpenAI examples run with environment variables;
3. Watsonx examples run with environment variables;
4. outputs are saved under `expected_outputs/`;
5. the Flask Module 3 lab is added or explicitly marked as pending.
