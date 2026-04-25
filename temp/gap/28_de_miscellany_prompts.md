# Data Engineering Miscellany — ChatGPT Project Prompts

Priority: 🟠 Important — the "randoms" every DE gets asked that don't fit one neat category

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Data Engineering Miscellany — The Topics That Don't Fit Elsewhere
Slug: de-miscellany

Extra coverage required:
- Python virtual environments — venv (stdlib), conda (data science), poetry (dependency locking); requirements.txt vs pyproject.toml; why pinning versions matters for reproducible pipeline runs
- Environment variables and config management — os.environ, python-dotenv, twelve-factor app principle: config belongs in the environment, not in the code
- YAML for pipeline configuration — PyYAML safe_load vs load (load is unsafe, never use it on untrusted input); anchors and aliases for DRY config; validate with Pydantic at startup
- Regular expressions for data cleaning — re module; patterns for emails, phone numbers, IP addresses, hostnames; re.sub for normalization; compile patterns once outside loops
- REST API consumption patterns — requests library; pagination (offset-based, cursor-based, link header); tenacity for retry with exponential backoff; session reuse for connection pooling
- Data profiling before building a pipeline — ydata-profiling for automated EDA; value_counts, null counts, cardinality, distribution histograms; know your data before writing transforms
- Checksums and data integrity — MD5/SHA-256 hash of files to verify transfer integrity; row count reconciliation between source and target; common ETL completeness check pattern
- File formats beyond Parquet — JSON Lines (NDJSON) for streaming and logs; Avro for schema-evolving Kafka messages; ORC in legacy Hive; CSV gotchas: encoding, BOM, quoting, delimiter collisions
- Python type hints for pipeline maintainability — type annotations in function signatures; TypedDict for typed dicts; mypy for static checking; makes code reviewable and self-documenting
- Idempotency patterns — natural key upsert for row-level idempotency; partition overwrite for batch idempotency; tombstone records for deletes in append-only systems
- Data lineage concepts — knowing where data came from, what transformed it, where it went; essential for debugging root causes and for compliance audit trails
- Medallion architecture — bronze (raw, immutable), silver (cleaned, validated), gold (aggregated, business-ready); never transform in-place on raw data; each layer is queryable independently
- SLAs for data pipelines — freshness SLA (data must be available by X time), completeness SLA (≥99% of expected records), latency SLA (end-to-end processing time); alerting when SLAs are missed

SCOPE FENCE:
- Target 12–16 HOST/SEAN exchanges total
- Each bullet = at most one exchange
- SEAN answers: 3–5 sentences max, no monologues
- Merge the least distinct bullets if the list runs long
- Do NOT elaborate into a textbook — this feeds a reference audio script
```

Run pipeline after saving the script:
```
run_mission_audio.ps1 -Slug de-miscellany -ChunkSize 750
```

Upload final_de-miscellany.mp3 to R2, then run Project 2.

---

## Project 2 — HTML Page

Run after `final_de-miscellany.mp3` is live on R2.

```
Topic: Data Engineering Miscellany — The Topics That Don't Fit Elsewhere
Slug: de-miscellany
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_de-miscellany.mp3
Today's date: 2026-04-25

SCOPE FENCE:
- Create exactly these sections, in this order:
  1. Virtual Environments & Dependency Management
  2. Environment Variables & YAML Config
  3. Regex for Data Cleaning
  4. REST API Consumption Patterns
  5. Data Profiling & EDA Before You Build
  6. Checksums, File Integrity & Row Reconciliation
  7. File Formats Beyond Parquet
  8. Idempotency Patterns & Medallion Architecture
  9. Data Lineage, SLAs & Type Hints
  10. Interview Q&A — 6 realistic senior-level pairs
  11. Quick Reference — 12–15 rows
- Per section: 2–3 tight paragraphs, one code block max (20 lines)
- No step-by-step tutorials, no full worked examples
- Cheat sheet rows must each earn their place — no padding

Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\de-miscellany.html
