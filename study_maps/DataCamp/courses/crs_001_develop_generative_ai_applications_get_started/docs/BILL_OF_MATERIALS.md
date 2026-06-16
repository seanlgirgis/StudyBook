# Bill of Materials — Develop Generative AI Applications: Get Started

## Identity

- Platform: Coursera
- Provider: IBM
- Program: RAG for Generative AI Applications Specialization
- Position: Course 1 of 4
- Canonical library ID: `crs_001`
- Canonical slug: `crs_001_develop_generative_ai_applications_get_started`
- Canonical path:

```text
D:\Workarea\StudyBook\study_maps\DataCamp\courses\crs_001_develop_generative_ai_applications_get_started
```

## Course modules

1. **Generative AI, Prompt Engineering, and Prompt Templates**
2. **Introduction to LangChain in Generative AI Applications**
3. **Build a Generative AI Application with LangChain**

## Source inventory

### Available

- [x] Course scaffold ZIP
- [x] Earlier reinforced course ZIP
- [x] Existing `study_pages` ZIP
- [x] Starter-code ZIP
- [x] Local command outputs from completed Python examples
- [x] RemNote study-card project bundle
- [x] Approved HTML templates
- [x] Course root `index.html`
- [x] Course root `README.md`
- [x] Existing Bill of Materials
- [x] Existing Setup Audit

### Still incomplete or not yet reconciled

- [ ] Full official Coursera curriculum screenshot captured in `source_material`
- [ ] Complete lesson/video title inventory
- [ ] Full transcript set
- [ ] Official readings inventory
- [ ] Official quiz inventory
- [ ] Official notebook inventory
- [ ] Official Module 3 Flask lab evidence
- [ ] Final platform-completion evidence

## Study artifacts

### Core guides

- [x] `study_pages\field_guide.html`
- [x] `study_pages\field_guide.md`
- [x] `study_pages\chapter_01_generative_ai_prompt_engineering_and_prompt_templates_field_guide.html`
- [x] `study_pages\chapter_02_introduction_to_langchain_in_generative_ai_applications_field_guide.html`
- [x] `study_pages\chapter_03_build_a_generative_ai_application_with_langchain_field_guide.html`

### Supporting study files

- [x] `study_pages\concept_and_code_quick_lookup.html`
- [x] `study_pages\langchain_code_patterns.html`
- [x] `study_pages\langchain_code_patterns.md`
- [x] `study_pages\chapter_01_learning_evidence.md`
- [x] `study_pages\certification_review_digest.html`
- [x] `study_pages\certification_self_test.html`
- [x] `study_pages\README.md`

### Reinforcement artifacts

- [x] RemNote comprehensive learning-mode cards
- [x] RemNote coding-pattern cards
- [x] Selective reinforcement cards
- [x] Theory reinforcement material
- [x] Confusion-focused reinforcement for:
  - `prompt.invoke()` vs `model.invoke()` vs `chain.invoke()`
  - sequence vs parallel
  - RunnableLambda vs automatic coercion
  - JSON dictionary vs Pydantic object
  - provider abstraction vs provider behavior
  - self-consistency
  - conversation-history flow

## Lab artifacts

### Lab support files

- [x] `lab\README.md`
- [x] `lab\00_how_to_run.md`
- [x] `lab\lab_run_book.md`
- [x] `lab\lab_guide.html`
- [x] `lab\notes\troubleshooting.md`
- [x] `lab\notes\python_syntax_validation.md`
- [x] `lab\expected_outputs\README.md`
- [x] `lab\source_archive\starter_code.zip`

### Runnable Python files

- [x] `01_prompt_template_one_variable.py`
- [x] `02_prompt_template_multiple_variables.py`
- [x] `03_chat_prompt_template.py`
- [x] `04_few_shot_prompt_template.py`
- [x] `05_lcel_local_pipeline.py`
- [x] `05b_lcel_openai_pipeline.py`
- [x] `05c_lcel_watsonx_pipeline.py`
- [x] `05d_watsonx_smallest_test.py`
- [x] `05f_provider_switching_lcel_pipeline.py`
- [x] `06_runnable_parallel.py`
- [x] `07_messages_placeholder.py`
- [x] `08_json_parser_shape.py`
- [x] `09_provider_native_structured_output.py`
- [x] `10_conversation_history_with_messages_placeholder.py`
- [x] `11_update_conversation_history.py`
- [x] `12_reusable_chat_function_with_history.py`
- [x] `13_runnable_with_message_history.py`

### Lab validation

- [x] All 17 Python files passed syntax compilation
- [x] Prompt-template examples executed
- [x] OpenAI examples executed
- [x] IBM watsonx examples executed
- [x] Provider-switching comparison executed
- [x] RunnableParallel executed
- [x] JSON parser example executed
- [x] Structured-output example executed
- [x] Conversation-history examples executed
- [ ] Representative output files saved under `lab\expected_outputs`
- [ ] Flask application lab completed

## Concept inventory

### AI foundations

- generative AI
- discriminative AI
- foundation models
- large language models
- model adaptation
- prompting versus fine-tuning

### Prompt engineering

- zero-shot prompting
- one-shot prompting
- few-shot prompting
- step-by-step prompting
- self-consistency
- prompt variables
- system and human roles
- prompt templates

### LangChain

- PromptTemplate
- ChatPromptTemplate
- FewShotPromptTemplate
- LCEL
- runnables
- RunnableLambda
- automatic coercion
- RunnableParallel
- StrOutputParser
- JsonOutputParser
- provider-native structured output
- Pydantic models
- MessagesPlaceholder
- HumanMessage
- AIMessage
- conversation history
- provider adapters

### Application development

- model selection
- evaluation criteria
- multimodel design
- Flask routes
- request validation
- HTTP status codes
- structured JSON responses
- monitoring
- cost and latency
- governance and responsible deployment

## Code-pattern inventory

```text
PromptTemplate.from_template(...)
ChatPromptTemplate.from_messages(...)
FewShotPromptTemplate(...)
prompt.invoke(...)
model.invoke(...)
chain.invoke(...)
prompt | model | parser
RunnableLambda(...)
RunnableParallel(...)
JsonOutputParser(...)
model.with_structured_output(...)
MessagesPlaceholder(...)
HumanMessage(...)
AIMessage(...)
result.model_dump()
```

## Fast-review topics

- foundation model versus LLM
- generative versus discriminative AI
- zero-shot versus few-shot
- PromptTemplate versus ChatPromptTemplate
- `prompt.invoke()` versus `model.invoke()` versus `chain.invoke()`
- sequence versus parallel
- JsonOutputParser versus structured output
- dictionary access versus Pydantic attribute access
- provider-neutral structure versus provider-specific behavior

## Slow-down topics

- self-consistency
- automatic coercion versus explicit RunnableLambda
- conversation-history lifecycle
- provider switching and model-region availability
- structured-output validation
- model-selection trade-offs
- prototype-to-production controls

## Interview-important topics

- What is a foundation model?
- What is an LLM?
- What problem does LangChain solve?
- What is LCEL?
- Why use structured output?
- When should RunnableParallel be used?
- What is provider abstraction?
- How would you select an LLM for an application?
- What changes when moving from prototype to production?

## Open items

1. Capture the official lesson inventory.
2. Complete the remaining Coursera course work.
3. Build and record the Module 3 Flask lab.
4. Save representative successful outputs.
5. Update specialization navigation.
6. Update the Course Library landing page.
7. Reconcile final status after platform completion.
