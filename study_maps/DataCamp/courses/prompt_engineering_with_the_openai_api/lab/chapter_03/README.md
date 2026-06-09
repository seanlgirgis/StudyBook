# Chapter 3 Lab — Prompt Engineering for Business Applications

This folder preserves Chapter 3 as a small, replayable sequence of business-focused prompt engineering exercises.

## Run order

1. `01_business_summary.py` — Summarize a business report into exactly three bullets.
2. `02_business_expansion.py` — Expand notes into professional prose without inventing facts.
3. `03_tone_adjustment.py` — Improve tone while preserving facts and avoiding false promises.
4. `04_business_translation.py` — Translate while preserving meaning, timing, and professional tone.
5. `05_proofreading.py` — Correct grammar and punctuation without broad rewriting.
6. `06_ticket_classification_and_extraction.py` — Classify a ticket and extract named business fields.
7. `07_json_entity_extraction.py` — Return fixed-key JSON suitable for downstream code.
8. `08_parse_and_validate_json.py` — Parse JSON and validate allowed values and data types.
9. `09_safe_json_validation.py` — Accept or reject model output safely with `try / except / else`.

## Chapter decision map

```text
Need a shorter business message
→ summarization

Need polished prose from notes
→ expansion with no-invention rules

Need the same facts for a different audience
→ tone adjustment or rewriting

Need another language
→ translation with meaning and tone preservation

Need grammar correction only
→ proofreading

Need a business category
→ classification with an allowed label set

Need fields from unstructured text
→ entity extraction with a fixed schema

Need downstream processing
→ JSON output followed by deterministic validation
```

## Core business rules

```text
Improve wording
≠ invent facts

Professional tone
≠ create promises

Valid JSON
≠ correct data

LLM generates
→ Python validates
→ pipeline accepts or rejects
```

## Data-engineering pattern

```text
unstructured text
→ constrained prompt
→ structured JSON
→ json.loads()
→ key / type / allowed-value validation
→ database, queue, API, retry, or human review
```

For production use, also validate exact keys, required fields, null handling, ranges, date formats, currency, units, source fidelity, privacy, retries, and human-review behavior.

## How to run

From the course `lab` folder:

```powershell
$env:PYTHONPATH = (Get-Location).Path
python .\chapter_03\01_business_summary.py
```

Run the remaining files in numerical order.

## Completion standard

You can turn a business objective into a bounded prompt, preserve source meaning, produce predictable structured output, parse JSON, validate it with Python, and reject unsafe or invalid records without crashing the pipeline.
