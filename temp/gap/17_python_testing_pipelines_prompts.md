# Python Testing for Data Pipelines — ChatGPT Project Prompts

Priority: 🔴 Critical — asked in every senior data engineering interview

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Python Testing for Data Pipelines
Slug: python-testing-pipelines
Extra coverage required: why testing data pipelines is harder than testing application code — non-determinism, external dependencies, large data volumes,
pytest fundamentals — test discovery, assert statements, running with -v, -k, --tb=short,
fixtures — what they are, scope (function/class/session), conftest.py, why they replace setUp/tearDown,
parametrize — running the same test against multiple inputs, testing edge cases systematically,
mocking — unittest.mock, patch, MagicMock — mocking database connections, S3 clients, API calls without hitting real services,
testing ETL transformations — unit testing individual transform functions with small DataFrames,
testing data quality logic — the validate_extract pattern, testing that bad data raises the right exception,
testing enrichment joins — verifying coverage rates, testing fallback logic, asserting no silent nulls,
integration tests vs unit tests — where the boundary sits for pipeline code,
testing idempotency — running the same pipeline stage twice and asserting the output is identical,
pytest-mock vs monkeypatch — when each is appropriate,
fixtures for Pandas and PySpark — creating test DataFrames, SparkSession fixtures for PySpark tests,
conftest.py patterns — shared fixtures for database connections, test data factories,
coverage — pytest-cov, what 80% coverage means and what it doesn't mean,
CI integration — running pytest in GitLab CI, failing the pipeline on test failure,
real scenario: testing the hostname normalization logic and enrichment join coverage gate from the Citi pipeline.
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
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\python-testing-pipelines.html
