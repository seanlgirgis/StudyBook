# DataCamp Reuse Map

## Purpose

This file maps completed DataCamp learning into the local:

```text
RAG Application Builder Foundation
```

The goal is not to copy entire courses or duplicate their documentation.

The goal is to identify:

```text
existing concept
→ useful source artifact
→ foundation stage
→ reuse decision
→ adaptation needed
```

## Source preservation rule

The canonical DataCamp course folders remain unchanged.

```text
Do not move or rename original course files.
Do not duplicate full course packages.
Reference canonical paths.
Copy or adapt only small reusable code patterns when needed.
Preserve attribution to the original course.
```

---

## 1. Working with the OpenAI API

Canonical course folder:

```text
D:\Workarea\StudyBook\study_maps\DataCamp\courses\working_with_the_openai_api
```

Primary foundation value:

```text
direct model requests
message roles
temperature
few-shot prompting
multi-turn context
response inspection
```

### Known reusable source files

```text
lab\python\01_first_chat_request.py
lab\python\02_summarize_customer_chat.py
lab\python\03_temperature_comparison.py
lab\python\04_zero_vs_few_shot.py
lab\python\05_multi_turn_conversation.py
```

### Reuse mapping

| Existing concept | Foundation destination | Reuse decision | Adaptation |
|---|---|---|---|
| First chat request | Stage 1 — Application basics | Adapt | Make input, request, response, and metadata visible |
| System/user/assistant roles | Stage 1 | Adapt | Add explicit message-flow explanation |
| Temperature comparison | Stage 1 | Reference + adapt | Relate variability to application requirements |
| Zero-shot vs few-shot | Stage 2 — Prompt engineering | Adapt | Turn into a prompt-contract comparison |
| Multi-turn conversation | Stage 1 / Stage 2 | Adapt | Separate conversation state from model behavior |
| Response inspection | Stage 1 | Expand | Record model, tokens, latency, and finish behavior |
| API key environment setup | Lab bootstrap | Reuse pattern | Keep secrets in local `.env`, never in repository |

### Foundation scripts to create

```text
stage_01_application_basics\
  01_first_request.py
  02_system_and_user_messages.py
  03_prompt_variables.py
  04_response_metadata.py
  05_error_handling.py
```

### What should not be copied wholesale

```text
course index
chapter field guides
course-wide quick lookup
all exercises unchanged
DataCamp-specific customer-support scenarios unless useful
```

### Main learning upgrade

The DataCamp course taught how to make requests.

The foundation should extend this into:

```text
request
→ inspect
→ parse
→ validate
→ log
→ handle failure
→ return application-safe output
```

---

## 2. Prompt Engineering with the OpenAI API

Canonical course folder:

```text
D:\Workarea\StudyBook\study_maps\DataCamp\courses\prompt_engineering_with_the_openai_api
```

Primary foundation value:

```text
prompt structure
message roles
few-shot examples
classification
stateful interactions
structured state
validation
```

### Known reusable source areas

```text
lab\chapter_01\
lab\chapter_04\
lab\openai_support\
```

Known Chapter 1 exercises include:

```text
message roles
summarization
classification
few-shot prompting
support-ticket analysis
```

Known Chapter 4 files include:

```text
01_dual_prompt_chatbot.py
02_stateful_chatbot_context.py
03_answer_and_updated_state.py
04_structured_chat_state.py
```

The remaining Chapter 4 validation exercise should be inspected locally before
its exact filename is recorded here.

### Reuse mapping

| Existing concept | Foundation destination | Reuse decision | Adaptation |
|---|---|---|---|
| Clear task instructions | Stage 2 | Adapt | Express as an application contract |
| Context and delimiters | Stage 2 | Expand | Separate trusted instructions from untrusted content |
| Few-shot examples | Stage 2 | Adapt | Show when examples improve consistency |
| Classification prompts | Stage 2 | Adapt | Add explicit label validation |
| Structured output | Stage 2 | Strong reuse | Parse into a typed schema |
| Stateful chatbot context | Stage 2 | Adapt | Keep state local and inspect what is resent |
| Answer plus updated state | Stage 2 | Strong reuse | Use as bridge to agent/application state |
| Structured chat state | Stage 2 | Strong reuse | Validate before accepting state changes |
| Validation exercise | Stage 2 | Inspect and reuse | Add retry/fallback behavior |
| Reusable support classes | Later shared library | Selective reuse | Do not hide direct calls too early |

### Foundation scripts to create

```text
stage_02_prompt_engineering\
  01_clear_task_contract.py
  02_context_delimiters.py
  03_few_shot_examples.py
  04_structured_output.py
  05_validate_output.py
  06_retry_invalid_output.py
  07_prompt_injection_boundary.py
```

### Main learning upgrade

Prompting should be treated as application engineering:

```text
task definition
+ allowed context
+ examples
+ output schema
+ validation rule
+ fallback behavior
```

The goal is not clever wording. The goal is repeatable application behavior.

---

## 3. Working with Hugging Face

Canonical course folder:

```text
D:\Workarea\StudyBook\study_maps\DataCamp\courses\working_with_hugging_face
```

Primary foundation value:

```text
model pipelines
local inference
question answering
document extraction
PDF question answering
model/task selection
```

### Known reusable source file

```text
lab\python\15_pdf_document_qa.py
```

Validated behavior already observed:

```text
PDF pages extracted
→ question passed to a QA pipeline
→ answer span returned
→ answer displayed
```

### Reuse mapping

| Existing concept | Foundation destination | Reuse decision | Adaptation |
|---|---|---|---|
| Pipeline abstraction | Stage 1 / framework comparison | Reference | Explain what the pipeline hides |
| Task-specific models | Stage 1 | Reference | Compare task model vs general chat model |
| Extractive QA | Stage 3 — Document processing | Strong reference | Contrast extracted answer span with generated answer |
| PDF text extraction | Stage 3 | Strong reuse | Separate extraction from QA |
| Page-level processing | Stage 3 | Adapt | Preserve page metadata for later citations |
| Document question answering | Stage 3 / Stage 6 | Adapt | Use as bridge from QA to grounded generation |
| CPU model execution | Provider/model comparison | Reference | Record local latency and resource behavior |

### Foundation scripts to create

```text
stage_03_document_processing\
  01_load_text_file.py
  02_extract_pdf_text.py
  03_clean_extracted_text.py
  04_split_text_into_chunks.py
  05_attach_chunk_metadata.py
  06_compare_extractive_and_generative_qa.py
```

### Main learning upgrade

The Hugging Face exercise answered questions from extracted text.

The foundation should expose the larger document pipeline:

```text
document
→ extraction
→ cleaning
→ chunking
→ metadata
→ retrieval
→ grounded generation
→ source citation
```

---

## 4. AI Ethics

Canonical course folder:

```text
D:\Workarea\StudyBook\study_maps\DataCamp\courses\ai_ethics
```

Primary foundation value:

```text
fairness
accountability
explainability
human oversight
monitoring
risk assessment
complaint and feedback channels
```

### Reuse mapping

| Existing concept | Foundation destination | Reuse decision |
|---|---|---|
| Human-in-the-loop | Stage 8 — Evaluation and observability | Selective reuse |
| Monitoring after deployment | Stage 8 | Strong reuse |
| Bias and group-level performance | Stage 8 | Reference when evaluating applications |
| Explainability and transparency | Stage 6 / Stage 8 | Adapt to source display and limitations |
| Feedback and complaint channel | Stage 8 | Adapt to user feedback capture |
| Risk varies by context | Stage 8 | Use in application release checklist |
| Cross-functional accountability | Documentation | Use in production-readiness notes |

### Main learning upgrade

Do not repeat the ethics course as a separate theory block.

Apply it inside concrete application questions:

```text
Can the answer be verified?
Were sources shown?
Could sensitive information be exposed?
Can a human override the result?
Are failures and complaints recorded?
Does performance differ across important groups or use cases?
```

---

## 5. Introduction to Data Privacy

Canonical course folder:

```text
D:\Workarea\StudyBook\study_maps\DataCamp\courses\introduction_to_data_privacy
```

Primary foundation value:

```text
purpose limitation
data minimization
retention
jurisdiction
third-party risk
sensitive inference
privacy by design
```

### Reuse mapping

| Existing concept | Foundation destination | Reuse decision |
|---|---|---|
| Purpose limitation | Stage 3 / Stage 8 | Apply to document ingestion |
| Data minimization | Stage 3 | Apply before sending text to a model |
| Retention controls | Stage 8 | Apply to prompts, logs, and vector stores |
| Sensitive inference | Stage 8 | Include in evaluation checklist |
| Jurisdiction and sovereignty | Architecture notes | Record provider/data-location concerns |
| Third-party governance | Provider strategy | Apply to OpenAI, IBM, and other services |
| Shift-left privacy | All stages | Add checks during design, not after release |
| Deletion/correction difficulty | Vector storage | Record reindexing and deletion requirements |

### Main learning upgrade

Privacy should be visible in the data flow:

```text
source document
→ classify sensitivity
→ minimize content
→ decide local vs external processing
→ control storage
→ control logs
→ support deletion/reindexing
```

---

## 6. Consolidated foundation mapping

| Foundation stage | Primary DataCamp source | Supporting source |
|---|---|---|
| Stage 1 — Application basics | Working with the OpenAI API | Hugging Face pipelines |
| Stage 2 — Prompt engineering | Prompt Engineering with the OpenAI API | Working with the OpenAI API |
| Stage 3 — Document processing | Working with Hugging Face | Introduction to Data Privacy |
| Stage 4 — Embeddings and vectors | New material required | Hugging Face model concepts |
| Stage 5 — Retrieval | New material required | Database and SQL experience |
| Stage 6 — Grounded generation | Prompt Engineering + Hugging Face | AI Ethics |
| Stage 7 — Complete RAG | New integration work | All three technical courses |
| Stage 8 — Evaluation/observability | AI Ethics + Data Privacy | OpenAI response metadata |
| Stage 9 — watsonx.ai comparison | IBM Coursera reconnaissance | OpenAI foundation scripts |

---

## 7. Reusable code promotion rule

A pattern should move into:

```text
lab\src\rag_foundation\
```

only after Sean has:

```text
1. built it visibly in a tiny script;
2. run it successfully;
3. inspected its input and output;
4. explained what each component did;
5. used it in at least two small exercises.
```

Possible later modules:

```text
providers\
validation\
retrieval\
monitoring\
```

Do not create a large abstraction layer during the first pass.

---

## 8. Immediate build order

### First build cluster

Use the completed OpenAI API course to create:

```text
stage_01_application_basics\
  01_first_request.py
  02_system_and_user_messages.py
  03_prompt_variables.py
  04_response_metadata.py
  05_error_handling.py
```

### Second build cluster

Use the prompt-engineering course to create:

```text
stage_02_prompt_engineering\
  01_clear_task_contract.py
  02_context_delimiters.py
  03_few_shot_examples.py
  04_structured_output.py
  05_validate_output.py
  06_retry_invalid_output.py
  07_prompt_injection_boundary.py
```

### Third build cluster

Use the Hugging Face course to create:

```text
stage_03_document_processing\
  01_load_text_file.py
  02_extract_pdf_text.py
  03_clean_extracted_text.py
  04_split_text_into_chunks.py
  05_attach_chunk_metadata.py
  06_compare_extractive_and_generative_qa.py
```

Then pause and reconcile against IBM Course 1 reconnaissance before building
Stages 4–9 in detail.

---

## 9. Current status

```text
Working with the OpenAI API mapping: READY FOR LOCAL INSPECTION
Prompt Engineering mapping: READY FOR LOCAL INSPECTION
Working with Hugging Face mapping: READY FOR LOCAL INSPECTION
AI Ethics mapping: CONCEPTUALLY MAPPED
Data Privacy mapping: CONCEPTUALLY MAPPED
Stage 1 scripts: NOT STARTED
Stage 2 scripts: NOT STARTED
Stage 3 scripts: NOT STARTED
```

## 10. Next action

Inspect the canonical source folders locally and confirm the exact reusable file
names for Stages 1 and 2.

Then create only:

```text
stage_01_application_basics\01_first_request.py
```

Run it, inspect its output, and record the result in:

```text
lab\lab_run_book.md
```
