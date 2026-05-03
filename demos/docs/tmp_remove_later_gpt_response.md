Yes — this is a good time to close both threads and start fresh for **03g_retrieval_decision**.

## 1. Codex closure prompt

Copy this into Codex first:

```markdown
We are closing the current Codex thread for:

D:\Workarea\StudyBook\demos\rag

Completed POC:
pocs/03f_hybrid_retrieval

Please do a final closure pass only.

Do NOT implement new code.
Do NOT start 03g.
Do NOT modify 03d or 03e artifacts.
Do NOT touch integrated/servicecall-ai.
Do NOT call any LLM.
Do NOT generate customer answers.

Please verify and record:

1. 03f status
- 03f_hybrid_retrieval is PASS / completed.
- Tests passed:
  pytest -v .\pocs\03f_hybrid_retrieval\tests
  Result: 16 passed
- Runner passed:
  python .\pocs\03f_hybrid_retrieval\src\run_hybrid_search.py
  Result: PASS, 6 queries run
- Sample output written:
  pocs/03f_hybrid_retrieval/outputs/sample_hybrid_search_results.json

2. 03f deliverables
Confirm these exist:
- pocs/03f_hybrid_retrieval/README.md
- pocs/03f_hybrid_retrieval/docs/DESIGN.md
- pocs/03f_hybrid_retrieval/docs/CONTRACT.md
- pocs/03f_hybrid_retrieval/docs/TEST_PLAN.md
- pocs/03f_hybrid_retrieval/requirements.txt
- pocs/03f_hybrid_retrieval/src/schemas.py
- pocs/03f_hybrid_retrieval/src/hybrid_retrieval.py
- pocs/03f_hybrid_retrieval/src/run_hybrid_search.py
- pocs/03f_hybrid_retrieval/tests/test_schemas.py
- pocs/03f_hybrid_retrieval/tests/test_hybrid_retrieval.py
- pocs/03f_hybrid_retrieval/outputs/sample_hybrid_search_results.json

3. Update tracking/control files if needed
Make sure these files clearly say 03f is closed as PASS:
- PROJECT_STATE.md
- TASK_BOARD.md
- HANDOFF.md
- DAILY_LOG.md
- CHANGELOG.md
- DECISIONS.md if appropriate

4. Record the next step
Next ladder step:
pocs/03g_retrieval_decision

But explicitly mark:
- 03g has not started yet.
- 03g should begin with design docs before code.
- 03g should decide retrieval quality/confidence only.
- 03g should not generate customer answers.
- 03g should not call an LLM.
- 03g should not move into integrated/servicecall-ai.

After closure:
- Report changed files only.
- Confirm no code was added.
- Confirm no new POC was started.
- Confirm the thread is safe to close.
```

## 2. Codex constitution update prompt

After closure, give Codex this:

```markdown
We are updating the project constitution / agent rules for:

D:\Workarea\StudyBook\demos\rag

Goal:
Make design documentation mandatory before implementation for every meaningful POC, feature, or project step.

Please update the appropriate project instruction/control files, likely including:
- AGENTS.md
- PROJECT_STATE.md if appropriate
- HANDOFF.md if appropriate
- DECISIONS.md if appropriate
- TASK_BOARD.md if appropriate

Add this standing rule:

## Design-First POC Rule

Every meaningful POC, feature, or project step must start with documentation before implementation.

Required documentation deliverables:
- README.md
- docs/DESIGN.md
- docs/CONTRACT.md
- docs/TEST_PLAN.md

Required implementation deliverables when code is approved:
- src/
- tests/
- outputs/

Acceptance gate:
A POC is not complete until:
1. README explains purpose, usage, inputs, outputs, and non-goals.
2. DESIGN.md explains problem, architecture, design decisions, boundaries, and future handoff.
3. CONTRACT.md defines input artifacts, output artifacts, data models, schemas, and required fields.
4. TEST_PLAN.md defines validation strategy, unit tests, integration checks, and acceptance checks.
5. Code exists only after design approval.
6. Tests pass.
7. Sample output exists if the POC produces artifacts.
8. Project tracking/control files are updated.

Important behavior rules:
- Do not implement code before design docs unless explicitly approved.
- Do not skip documentation for “small” but meaningful POCs.
- Keep documentation teaching-friendly and industry-style.
- Explain why the design exists, not only what files were changed.
- Keep each POC standalone, configurable, reusable, and chainable.
- Do not jump ahead to integrated/servicecall-ai until the POC ladder supports it.

After changes:
- Report changed files only.
- Summarize the constitution update.
- Confirm no feature code was implemented.
```

## 3. ChatGPT project constitution note

For the **ChatGPT project instructions / sources**, add something like this to your project source file or instructions:

```markdown
## Design-First Rule for demos/RAG

For every meaningful POC, feature, or serious project step, ChatGPT and Codex must follow a design-first workflow.

Standard POC deliverables:
- README.md
- docs/DESIGN.md
- docs/CONTRACT.md
- docs/TEST_PLAN.md
- src/
- tests/
- outputs/

Workflow:
1. Discuss and teach the concept first.
2. Create design documentation before code.
3. Review design boundaries and non-goals.
4. Implement only after explicit approval.
5. Keep implementation standalone, configurable, reusable, and chainable.
6. Produce sample outputs where applicable.
7. Run tests.
8. Update project tracking files.
9. Close the POC before starting the next one.

Acceptance gate:
A POC is not complete until documentation, code, tests, sample outputs, and tracking updates are all done.

Behavior rules:
- Do not jump ahead to LLM answers, FastAPI, Docker, AWS, or integrated/servicecall-ai.
- Do not implement without explicit approval.
- Do not duplicate logic from earlier POCs.
- Reuse existing artifacts and contracts where possible.
- Keep documentation teaching-friendly and industry-style.
```

## 4. New ChatGPT discussion starter

Use this as the first message in the new ChatGPT thread:

```markdown
We are continuing the demos / RAG project.

Please read the project sources first:
- CHATGPT_PROJECT_CONTEXT.md
- CHATGPT_RAG_CONTEXT.md

Local project:
D:\Workarea\StudyBook\demos\rag

Demo:
ServiceCall AI, a learning-first RAG demo for a synthetic home-services business.

New discussion name:
RAG 03g Retrieval Decision POC

Completed ladder:
- 03a_load_documents: PASS
- 03b_chunk_documents: PASS
- 03c_text_normalization: PASS
- 03d_word_tfidf_index: PASS
- 03e_char_tfidf_typo_search: PASS
- 03f_hybrid_retrieval: PASS

03f completed deliverables:
- reusable schemas
- reusable hybrid retrieval engine
- runner script
- sample_hybrid_search_results.json
- design docs
- tests passing: 16 passed
- runner passing: 6 sample queries
- scoring: 0.65 word / 0.35 char

Important standing rule:
Every meaningful POC must be design-first.

Required POC deliverables:
- README.md
- docs/DESIGN.md
- docs/CONTRACT.md
- docs/TEST_PLAN.md
- src/
- tests/
- outputs/

Workflow:
- Teach first.
- Discuss boundaries.
- Produce design docs before code.
- Do not implement without explicit approval.
- Move one element at a time.
- Keep each POC standalone, configurable, reusable, and chainable.

Current next task:
Discuss and later build only:

pocs/03g_retrieval_decision

Do not give Codex prompt yet unless I ask.

Start by explaining one question at a time:
1. What retrieval decision means.
2. Why it comes after 03f.
3. What signals it should inspect.
4. How confidence / ambiguity / weak-match decisions might work.
5. What 03g should read/write.
6. What 03g should NOT do.
```

## 5. New Codex thread starter

Use this in a fresh Codex chat later:

```markdown
We are starting a new Codex thread for:

D:\Workarea\StudyBook\demos\rag

POC:
pocs/03g_retrieval_decision

Current ladder status:
- 03a_load_documents: PASS
- 03b_chunk_documents: PASS
- 03c_text_normalization: PASS
- 03d_word_tfidf_index: PASS
- 03e_char_tfidf_typo_search: PASS
- 03f_hybrid_retrieval: PASS

Important:
Do not implement yet unless explicitly asked.

Standing project rule:
Every meaningful POC must be design-first.

Required docs before code:
- README.md
- docs/DESIGN.md
- docs/CONTRACT.md
- docs/TEST_PLAN.md

03g purpose:
03g_retrieval_decision should inspect hybrid retrieval results and decide retrieval quality/confidence.

It should eventually classify retrieval outcomes such as:
- strong_match
- ambiguous_match
- weak_match
- no_match
- needs_clarification

But for the first step, create design docs only if asked.

03g must NOT:
- generate customer answers
- call an LLM
- decide final business response
- ask live clarification questions
- move anything into integrated/servicecall-ai
- rebuild 03d, 03e, or 03f artifacts

Wait for my next instruction before changing files.
```

Suggested new ChatGPT discussion name:

```text
RAG 03g Retrieval Decision POC
```
