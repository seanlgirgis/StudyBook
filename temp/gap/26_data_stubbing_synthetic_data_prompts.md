# Data Stubbing & Synthetic Test Data — ChatGPT Project Prompts

Priority: 🟠 Important — testing pipelines without production data, interview signal for test maturity

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Data Stubbing and Synthetic Test Data for Data Engineers
Slug: data-stubbing-synthetic

Extra coverage required:
- What data stubbing is — replacing real external data sources (databases, S3, APIs) with controlled fake data so tests run fast, deterministically, and without production access
- Why synthetic data is required — production PII cannot go into dev/test environments; external systems are unavailable in CI; real data has non-deterministic edge cases
- Faker library — generating realistic names, addresses, emails, phone numbers, dates, company names, IP addresses; locale-aware; seed for reproducibility
- Structurally valid vs semantically valid test data — a valid email format is not the same as a deliverable email; valid SSN format is not a real SSN; the distinction matters for contract testing
- Building test DataFrames — small (10–100 rows), covering edge cases: nulls in join key, duplicates, boundary values, encoding oddities, empty strings vs null
- Factory pattern for test data — TestDataFactory class generates consistent reusable records; parametrize tests with factory output; avoids duplicating raw dict literals across test files
- Edge case coverage checklist — null join keys, duplicate identifiers, records in one source but not the other, zero rows, maximum-length strings, negative numbers
- S3 stubs with moto — @mock_aws decorator replaces boto3 S3 calls with an in-memory fake; no real AWS credentials needed; test upload/download/list without network calls
- Database stubs — SQLite in-memory as a drop-in for Oracle/SQL Server in unit tests; create_engine("sqlite:///:memory:"); load test fixtures with to_sql()
- API response stubs — responses library patches requests.get/post; returns pre-defined JSON; unittest.mock.patch for async HTTP clients
- Data contract testing — assert that a pipeline's output DataFrame matches the schema the downstream consumer declared; catches breaking changes before deployment
- Snapshot testing — capture the expected output of a transformation and store it; future test runs diff against the snapshot; pytest-snapshot library
- Volume testing with synthetic data — generate 1M+ rows with Faker or numpy; test pipeline memory behavior, chunk processing, and performance at scale

SCOPE FENCE:
- Target 12–16 HOST/SEAN exchanges total
- Each bullet = at most one exchange
- SEAN answers: 3–5 sentences max, no monologues
- Merge the least distinct bullets if the list runs long
- Do NOT elaborate into a textbook — this feeds a reference audio script
```

Run pipeline after saving the script:
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

SCOPE FENCE:
- Create exactly these sections, in this order:
  1. What Data Stubbing Is & Why It Matters
  2. Faker Library — generating realistic fake data
  3. Building Test DataFrames & Edge Case Coverage
  4. TestDataFactory Pattern
  5. S3 Stubs with moto
  6. Database Stubs — SQLite in-memory
  7. API Response Stubs
  8. Data Contract Testing & Snapshot Testing
  9. Volume Testing with Synthetic Data
  10. Interview Q&A — 6 realistic senior-level pairs
  11. Quick Reference — 12–15 rows
- Per section: 2–3 tight paragraphs, one code block max (20 lines)
- No step-by-step tutorials, no full worked examples
- Cheat sheet rows must each earn their place — no padding

Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\data-stubbing-synthetic.html
