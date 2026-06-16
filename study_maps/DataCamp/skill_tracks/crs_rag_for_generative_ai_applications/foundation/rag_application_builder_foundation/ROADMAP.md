# RAG Application Builder Foundation Roadmap

## Stage 0 — Inventory and alignment

Goal: identify what Sean already learned and what still needs to be built.

Artifacts:

- `docs/DATACAMP_REUSE_MAP.md`
- `docs/COURSE_ALIGNMENT_MATRIX.md`
- `source_material/coursera/COURSE_RECONNAISSANCE.md`

## Stage 1 — AI application basics

Build:

```text
input
→ messages
→ model request
→ response
→ validation
→ usable output
```

Tiny scripts:

```text
01_first_request.py
02_system_and_user_messages.py
03_prompt_variables.py
04_response_metadata.py
05_error_handling.py
```

## Stage 2 — Prompt engineering as application engineering

Focus:

- instruction hierarchy
- context boundaries
- few-shot examples
- structured output
- validation
- retry and fallback
- prompt injection awareness

Tiny scripts:

```text
01_clear_task_contract.py
02_context_delimiters.py
03_few_shot_examples.py
04_structured_output.py
05_validate_output.py
06_retry_invalid_output.py
07_prompt_injection_boundary.py
```

## Stage 3 — Document processing

Build:

```text
file
→ extracted text
→ cleaned text
→ chunks
→ metadata
```

## Stage 4 — Embeddings and vectors

Build:

```text
text
→ embedding model
→ vector
→ similarity
```

## Stage 5 — Retrieval

Build:

```text
question
→ query embedding
→ vector search
→ ranked chunks
→ metadata filters
```

## Stage 6 — Grounded generation

Build:

```text
retrieved chunks
+ question
+ answer contract
→ grounded prompt
→ answer with sources
```

## Stage 7 — Complete transparent RAG pipeline

Build one small end-to-end application without a large framework first.

## Stage 8 — Evaluation and observability

Track:

- request count
- model
- tokens
- estimated local cost
- latency
- retries
- failures
- embedding use
- retrieval latency
- retrieved chunk scores
- source coverage
- groundedness notes

## Stage 9 — watsonx.ai comparison

Repeat selected concepts using watsonx.ai only where useful:

- one chat request
- one structured response
- one embedding or retrieval comparison when supported
- model behavior and metadata comparison
- authentication and project configuration

## Completion gate

The foundation is ready when Sean can explain:

```text
what local Python does
what the generation model does
what the embedding model does
what the vector store does
what the retriever does
what the prompt does
what validation does
what monitoring measures
```
