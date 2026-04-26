# Pydantic for Data Engineers — ChatGPT Project Prompts

Priority: 🟠 Important — data validation and schema enforcement, increasingly standard in pipelines

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Pydantic for Data Engineers
Slug: pydantic

Extra coverage required:
- What Pydantic is — runtime data validation using Python type annotations; validates at instantiation, not just type-hints which are ignored at runtime
- BaseModel — define a class inheriting BaseModel; each class attribute is a typed field; Pydantic validates types and constraints when you call MyModel(**data)
- Field types — str, int, float, bool, datetime, Optional[T], List[T], Dict[str, T], Literal['a','b'] — what each validates and coerces
- Field() — setting defaults, aliases (for JSON keys that differ from Python names), constraints: ge/le (numeric bounds), min_length/max_length, pattern (regex)
- Validators — @field_validator for single-field custom logic; @model_validator for cross-field validation (e.g. end_date must be after start_date)
- model_dump() and model_json() — serializing a model instance to dict or JSON string; exclude_none=True to strip null fields from output
- model_validate() — parsing a raw dict into a validated model instance; raises ValidationError with per-field details if anything fails
- Using Pydantic as a data contract — define input and output schemas for each pipeline stage; catch bad data at stage boundaries, not silently downstream
- Pipeline config validation — parse YAML or JSON config files through a Pydantic model; type errors in config surface immediately with a clear message
- Nested models — compose models for nested JSON structures (e.g. an API response with an embedded address object); validation is recursive
- Strict vs lax mode — lax (default) coerces compatible types ("1" to 1); strict rejects any type mismatch; use strict for untrusted external data
- Error handling — ValidationError contains a list of errors per field; iterate .errors() to log field name, error type, and value for debugging
- Pydantic v1 vs v2 — v2 is 5–50x faster (Rust core); API differences: .dict() became .model_dump(), @validator became @field_validator; migration matters

SCOPE FENCE:
- Target 12–16 HOST/SEAN exchanges total
- Each bullet = at most one exchange
- SEAN answers: 3–5 sentences max, no monologues
- Merge the least distinct bullets if the list runs long
- Do NOT elaborate into a textbook — this feeds a reference audio script
```

Run pipeline after saving the script:
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

SCOPE FENCE:
- Create exactly these sections, in this order:
  1. What Pydantic Is — runtime validation, not just type hints
  2. BaseModel & Core Field Types
  3. Field() — defaults, aliases, constraints
  4. Validators — field and model level
  5. Serialization — model_dump & model_json
  6. Pydantic as a Data Contract
  7. Pipeline Config Validation
  8. Nested Models, Strict Mode & Error Handling
  9. Pydantic v1 vs v2 — migration essentials
  10. Interview Q&A — 6 realistic senior-level pairs
  11. Quick Reference — 12–15 rows
- Per section: 2–3 tight paragraphs; include a code block where it adds value (20 lines max)
- No step-by-step tutorials, no full worked examples
- Cheat sheet rows must each earn their place — no padding

Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\pydantic.html
