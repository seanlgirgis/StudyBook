# Pydantic for Data Engineers — ChatGPT Project Prompts

Priority: 🟠 Important — data validation, schema enforcement, increasingly standard in modern pipelines

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Pydantic for Data Engineers
Slug: pydantic
Extra coverage required: what Pydantic is — data validation using Python type annotations, not just type hints,
BaseModel — defining a model, field types, how validation happens at instantiation,
field types — str, int, float, bool, datetime, Optional, List, Dict, Literal — and what each validates,
Field() — default values, aliases, validation constraints (ge, le, min_length, pattern),
validators — @field_validator, @model_validator — custom validation logic with real pipeline examples,
model_dump() and model_json() — serializing to dict and JSON, exclude_none, include patterns,
model_validate() and model_validate_json() — parsing dicts and JSON strings into validated models,
Pydantic v1 vs v2 — the breaking changes, the new API, performance improvements in v2,
using Pydantic as a data contract — defining the expected schema for pipeline stage inputs and outputs,
validating pipeline configuration — using Pydantic to parse YAML or JSON config files with type safety,
Pydantic with FastAPI — how it powers automatic request/response validation and OpenAPI docs,
schema export — model.schema(), JSON Schema generation for documentation and contract sharing,
nested models — composing models, validating nested JSON structures from API responses,
strict mode vs lax mode — coercion vs rejection of type mismatches,
error handling — ValidationError, accessing error details per field, surfacing errors in pipeline logging,
real scenario: defining a validated config model for a data pipeline with required S3 paths, thresholds, and region settings.

SCOPE FENCE: Target 12-16 HOST/SEAN exchanges total. Each bullet above = at most
one exchange. SEAN answers: 3-5 sentences maximum, no monologues. If the bullet list
has more items than exchanges, merge the least distinct ones. Do not elaborate into
a textbook - this feeds a reference audio script, not a lecture series.
```\r\n\r\nRun pipeline after saving the script:
```
run_mission_audio.ps1 -Slug pydantic -ChunkSize 750
```

Upload final_pydantic.mp3 to R2, then run Project 2.

---

## Project 2 — HTML Page

Run after `final_pydantic.mp3` is live on R2.

```
Topic: Pydantic for Data Engineers
Slug: pydantic
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_pydantic.mp3
Today's date: 2026-04-25

SCOPE FENCE: 8-10 sections maximum. 2-3 tight paragraphs per section.
One code block per section, 20 lines max. Cheat sheet: 12-15 rows.
Reference page only - no step-by-step tutorials or full worked examples.
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\pydantic.html
