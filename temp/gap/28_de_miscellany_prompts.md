# Data Engineering Miscellany — ChatGPT Project Prompts

Priority: 🟠 Important — the "randoms" every DE gets asked that don't fit one neat category

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Data Engineering Miscellany — The Topics That Don't Fit Elsewhere
Slug: de-miscellany
Extra coverage required: Python virtual environments — venv vs conda vs poetry, requirements.txt vs pyproject.toml, pinning versions for reproducible pipeline runs,
environment variables and config management — os.environ, python-dotenv, never hardcoding credentials, twelve-factor app principles for data pipelines,
YAML for pipeline configuration — PyYAML, safe_load vs load, anchors and aliases for DRY config files, Pydantic-validated config,
regular expressions for data cleaning — re module, common patterns (emails, phone numbers, IP addresses, hostnames), re.sub for normalization,
REST API consumption patterns — requests library, pagination (offset, cursor, link header), rate limiting with backoff, retry logic with tenacity,
data profiling and EDA — pandas-profiling / ydata-profiling, value counts, null analysis, cardinality, distribution histograms before building a pipeline,
checksums and data integrity — MD5/SHA-256 for file transfer validation, row count reconciliation between source and target,
file formats beyond Parquet — JSON Lines (NDJSON) for streaming, Avro for schema evolution in Kafka, ORC in Hive ecosystems, CSV gotchas (encoding, quoting, BOM),
Python type hints for data engineering — type annotations, mypy, TypedDict for typed dicts, why type hints make pipeline code maintainable,
idempotency patterns in practice — natural keys for upsert, partition overwrite in Parquet, tombstone records for deletes,
data lineage concepts — knowing where data came from, what transformed it, where it went — why it matters for debugging and compliance,
the medallion architecture in plain terms — bronze/silver/gold, what belongs in each layer, why you never transform in-place on raw data,
SLAs for data pipelines — defining freshness SLAs, latency SLAs, completeness SLAs — and what happens when you miss them,
API versioning and schema evolution — backward vs forward compatibility, how to change a pipeline's output schema without breaking consumers,
the ten commandments of data quality — the mental checklist every DE should run before marking a pipeline production-ready.

SCOPE FENCE: Target 12-16 HOST/SEAN exchanges total. Each bullet above = at most
one exchange. SEAN answers: 3-5 sentences maximum, no monologues. If the bullet list
has more items than exchanges, merge the least distinct ones. Do not elaborate into
a textbook - this feeds a reference audio script, not a lecture series.
```\r\n\r\nRun pipeline after saving the script:
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

Content sections — create exactly these, in this order:
Virtual Environments & Packaging | Environment Variables & YAML Config | Regex for Data Cleaning | REST API Consumption Patterns | Data Profiling & EDA | Checksums & File Integrity | File Formats (JSON Lines / Avro / ORC) | Medallion Architecture | Data Lineage & Pipeline SLAs
Then add: Interview Q&A (6 pairs) | Quick Reference (12-15 rows)
Size per section: 2-3 tight paragraphs, one code block max (20 lines). No tutorials.
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\de-miscellany.html
