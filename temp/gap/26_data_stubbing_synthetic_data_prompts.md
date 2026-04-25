# Data Stubbing & Synthetic Test Data — ChatGPT Project Prompts

Priority: 🟠 Important — testing pipelines without production data, interview signal for test maturity

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Data Stubbing and Synthetic Test Data for Data Engineers
Slug: data-stubbing-synthetic
Extra coverage required: what data stubbing is — replacing real external data sources with controlled fake data for testing,
why you need synthetic data — can't use production PII in dev/test, can't rely on external systems being available in CI,
Faker library — generating realistic names, addresses, emails, phone numbers, dates, company names, IPs,
structurally valid vs semantically valid test data — a valid email format is not the same as a deliverable email,
building test DataFrames — small, representative, covering edge cases (nulls, duplicates, boundary values, encoding issues),
factory patterns — TestDataFactory classes that generate consistent, reusable test records for pipeline unit tests,
fixtures vs inline data — when to define test data in conftest.py fixtures vs inline in the test function,
covering edge cases systematically — null join keys, duplicate identifiers, records in one source but not another, zero rows,
statistically representative synthetic data — matching the distribution, cardinality, and skew of production data for performance testing,
time series test data — generating periodic data with realistic seasonality, trends, and anomalies for forecasting pipeline tests,
database stubs — SQLite in-memory database as a drop-in for Oracle/SQL Server in unit tests, loading test fixtures,
S3 stubs — moto library for mocking AWS S3 in Python tests, no real AWS calls needed in CI,
API response stubs — responses library, unittest.mock for patching HTTP clients, recording and replaying real responses,
data contract testing — testing that a pipeline's output matches the schema contract the downstream consumer expects,
volume testing with synthetic data — generating 1M+ rows to test pipeline performance and memory behavior,
snapshot testing — capturing the expected output of a transformation and asserting it hasn't changed.

SCOPE FENCE: Target 12-16 HOST/SEAN exchanges total. Each bullet above = at most
one exchange. SEAN answers: 3-5 sentences maximum, no monologues. If the bullet list
has more items than exchanges, merge the least distinct ones. Do not elaborate into
a textbook - this feeds a reference audio script, not a lecture series.
```\r\n\r\nRun pipeline after saving the script:
```
run_mission_audio.ps1 -Slug data-stubbing-synthetic -ChunkSize 750
```

Upload final_data-stubbing-synthetic.mp3 to R2, then run Project 2.

---

## Project 2 — HTML Page

Run after `final_data-stubbing-synthetic.mp3` is live on R2.

```
Topic: Data Stubbing and Synthetic Test Data for Data Engineers
Slug: data-stubbing-synthetic
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_data-stubbing-synthetic.mp3
Today's date: 2026-04-25

Content sections — create exactly these, in this order:
What Data Stubbing Is & Why | Faker Library | Test DataFrame Factories | Edge Case Coverage | Statistically Representative Data | Time Series Test Data | S3 Stubs with moto | API Response Stubs | Data Contract & Snapshot Testing
Then add: Interview Q&A (6 pairs) | Quick Reference (12-15 rows)
Size per section: 2-3 tight paragraphs, one code block max (20 lines). No tutorials.
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\data-stubbing-synthetic.html
