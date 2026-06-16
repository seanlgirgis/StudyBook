# Bill of Materials — Developing AI Systems with the OpenAI API

## Identity

- Canonical slug: `developing_ai_systems_with_the_openai_api`
- Track: Developing AI Applications
- Track position: 6
- Level: Intermediate
- DataCamp update shown: April 2026
- Estimated duration: 3 hours
- Curriculum size: 3 chapters, 11 videos, 36 exercises

## Source inventory

| Source | Status | Notes |
|---|---|---|
| Course overview screenshot | AVAILABLE | Supplies title, metadata, chapters, and lesson names |
| Chapter videos | MISSING | Supply chapter by chapter |
| Transcripts | MISSING | `source_material/transcript_raw_combined.md` is still a shell |
| Exercise notes | MISSING | Capture during the live course pass |
| Local Python code | NOT STARTED | Store under `lab/python/` |
| Expected outputs | NOT STARTED | Record only after execution |

## Planned study artifacts

- `study_pages/field_guide.html`
- `study_pages/field_guide.md`
- `study_pages/openai_api_quick_lookup.html`
- Three chapter field guides
- `lab/lab_run_book.md`
- Python chapter workspaces under `lab/python/`

## Core topic inventory

### Chapter 1

API request structure, response decoding, JSON output, errors, exceptions, batching, retry behavior, rate limits, and token limits.

### Chapter 2

Tool definitions, the `tools` parameter, tool-call extraction, function dictionaries, multiple and parallel functions, forced tool selection, external API execution, and returning tool results.

### Chapter 3

Moderation, prompt-injection mitigation, guardrails, validation, model-error handling, adversarial testing, safety practices, risk reduction, and end-user identifiers.

## Fast-review priorities

- Request-to-response lifecycle
- Structured outputs and validation
- Retry versus batching
- Tool-calling lifecycle
- Separation between model selection and application execution
- Moderation and prompt-injection defenses

## Open items

- Populate chapter pages only from supplied chapter sources and completed exercises.
- Validate examples against the OpenAI API version taught by the course.
- Record actual local run evidence before marking the lab complete.