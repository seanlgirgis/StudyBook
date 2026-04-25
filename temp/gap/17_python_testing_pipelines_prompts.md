# Python Testing for Data Pipelines — ChatGPT Project Prompts

Priority: 🔴 Critical — asked in every senior data engineering interview

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Python Testing for Data Pipelines
Slug: python-testing-pipelines

Extra coverage required:
- Why pipeline testing is harder than app testing — non-determinism in data, external dependencies (databases, S3, APIs), large volumes you can't load in a test
- pytest fundamentals — test discovery (test_ prefix), plain assert statements, -v for verbose output, -k for filtering, --tb=short for readable failures
- Fixtures — setup and teardown via @pytest.fixture; scope (function/class/module/session); conftest.py for sharing fixtures across test files
- Parametrize — @pytest.mark.parametrize to run one test with multiple inputs; essential for covering edge cases without duplicating test code
- Mocking — unittest.mock.patch to replace database connections, S3 clients, API calls with controlled fakes; MagicMock for return values
- Testing ETL transformations — call the transform function directly with a small test DataFrame; assert output schema, row count, and specific cell values
- Testing data quality logic — verify that bad input (nulls in join key, zero rows, wrong schema) raises the correct exception or returns the right flag
- Testing enrichment joins — assert coverage rate is above threshold; assert no records are silently dropped; assert fallback logic fires correctly
- Testing idempotency — run the same pipeline stage twice on the same input; assert output is identical both times; catches append-only bugs
- Fixtures for PySpark — SparkSession fixture scoped to session; create test DataFrames with spark.createDataFrame; clean up after
- pytest-mock and monkeypatch — monkeypatch for replacing env vars and file paths in tests; pytest-mock as a cleaner mock.patch interface
- Coverage — pytest-cov; what 80% line coverage means and what it does not mean; branch coverage for conditional logic
- CI integration — running pytest in GitLab CI as a required stage; failing the merge request if tests fail; coverage report as artifact

SCOPE FENCE:
- Target 12–16 HOST/SEAN exchanges total
- Each bullet = at most one exchange
- SEAN answers: 3–5 sentences max, no monologues
- Merge the least distinct bullets if the list runs long
- Do NOT elaborate into a textbook — this feeds a reference audio script
```

Run pipeline after saving the script:
```
run_mission_audio.ps1 -Slug python-testing-pipelines -ChunkSize 750
```

Upload final_python-testing-pipelines.mp3 to R2, then run Project 2.

---

## Project 2 — HTML Page

Run after `final_python-testing-pipelines.mp3` is live on R2.

```
Topic: Python Testing for Data Pipelines
Slug: python-testing-pipelines
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_python-testing-pipelines.mp3
Today's date: 2026-04-25

SCOPE FENCE:
- Create exactly these sections, in this order:
  1. Why Pipeline Testing Is Hard
  2. pytest Fundamentals
  3. Fixtures & Parametrize
  4. Mocking — patch, MagicMock, monkeypatch
  5. Testing ETL Transformations
  6. Testing Data Quality & Enrichment Logic
  7. Testing Idempotency
  8. PySpark Test Fixtures
  9. Coverage & CI Integration
  10. Interview Q&A — 6 realistic senior-level pairs
  11. Quick Reference — 12–15 rows
- Per section: 2–3 tight paragraphs, one code block max (20 lines)
- No step-by-step tutorials, no full worked examples
- Cheat sheet rows must each earn their place — no padding

Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\python-testing-pipelines.html
