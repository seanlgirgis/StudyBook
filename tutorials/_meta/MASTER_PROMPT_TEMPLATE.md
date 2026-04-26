# Master Prompt Template
# Copy this, fill in the {PLACEHOLDERS}, paste into ChatGPT

---

## HOW TO USE

1. Copy everything between the triple-dashes below
2. Fill in all {PLACEHOLDERS}
3. Paste into ChatGPT (Project 1 or a fresh conversation)
4. ChatGPT will generate files one at a time — save each before asking for the next
5. Ask: "Generate file 01", "Generate file 02", etc.
6. Save each file to the correct tutorial folder

---

```
You are generating educational Python tutorial files for a Senior Data Engineer
personal study system. Each file must be production-quality, heavily commented,
and runnable as-is.

TOPIC: {TOPIC NAME}
SLUG:  {topic-slug}
PRIORITY: {Toyota / Capital One / Fundamentals / Advanced}
INFRASTRUCTURE: {AWS / Docker-Postgres / Docker-Kafka / Pure Python}

===== CODING STANDARDS (follow exactly) =====

FILE HEADER — every file starts with:
# ============================================================
# Topic   : {TOPIC NAME}
# File    : NN_filename.py
# Covers  : one-line description
# Prereqs : what must be installed/running
# Run     : python filename.py
# ============================================================

COMMENTS:
- Explain WHY, not WHAT — the code shows what, comments show reasoning
- Every design decision, threshold, or non-obvious choice gets a comment
- Numbers and limits get comments citing their source (AWS docs, best practice, etc.)

DOCSTRINGS — every function must have:
- One-line summary
- WHY this approach (the senior insight — what separates this from a junior answer)
- Args with types
- Returns with type
- Raises if applicable
- One usage example

CODE:
- Python 3.11+, type hints on all signatures
- os.environ for ALL credentials and config — NEVER hardcode
- f-strings for formatting
- Specific exception handling — never bare except
- Every file ends with if __name__ == "__main__": that demos all functions
- No placeholder functions — everything must work when run

ENVIRONMENT VARIABLES — document at top of each file:
# Required environment variables:
#   VAR_NAME — description

===== FILES TO GENERATE =====

Generate these files one at a time. Wait for me to say "next" before generating
the following file. Name them exactly as shown.

{FILE_01_NAME}.py
  Purpose: {description}
  Key concepts: {concept1}, {concept2}, {concept3}
  Functions to include: {function list}

{FILE_02_NAME}.py
  Purpose: {description}
  Key concepts: {concept1}, {concept2}, {concept3}
  Functions to include: {function list}

{FILE_03_NAME}.py
  Purpose: {description}
  Key concepts: {concept1}, {concept2}, {concept3}
  Functions to include: {function list}

{FILE_04_NAME}.py
  Purpose: {description}
  Key concepts: {concept1}, {concept2}, {concept3}
  Functions to include: {function list}

{FILE_05_NAME}.py
  Purpose: {description}
  Key concepts: {concept1}, {concept2}, {concept3}
  Functions to include: {function list}

===== CAPSTONE PROJECT =====

After all 5 files, generate the capstone:

capstone/brief.md
  Title: {CAPSTONE TITLE}
  Scenario: {realistic real-world scenario}
  What to build: {concrete deliverable}
  Acceptance criteria:
    - {criterion 1}
    - {criterion 2}
    - {criterion 3}
  Concepts used: {list from tutorial files}
  Estimated time: {2-4 hours}

capstone/capstone.py
  Complete working solution to the brief above.
  Must use at least 3 concepts from the 5 tutorial files.
  Must be runnable against {INFRASTRUCTURE}.

capstone/test_capstone.py
  pytest tests validating the capstone solution.
  Mock external dependencies (AWS, DB) where appropriate.
  Minimum 5 test functions.

===== INFRASTRUCTURE NOTES =====

{INFRASTRUCTURE_NOTES}

===== START =====

Acknowledge these instructions, then wait for me to say "generate file 01".
```

---

## INFRASTRUCTURE NOTES SNIPPETS

Copy the appropriate block into {INFRASTRUCTURE_NOTES}:

### AWS
```
All AWS calls use boto3. The student has valid AWS credentials configured.
Use os.environ.get("AWS_REGION", "us-east-1") for region.
Use os.environ.get("AWS_PROFILE") for profile (may be None — use default).
Do not create real resources that cost money unless clearly commented.
Prefer describe/list operations in demos where possible.
When resources must be created, always include a cleanup function.
```

### Docker-Postgres
```
PostgreSQL runs locally via Docker:
  Host: localhost, Port: 5432
  Database: studybook, User: postgres, Password: from env POSTGRES_PASSWORD
  Start with: docker compose up -d (from _shared/docker/postgres/)
Use psycopg2 or SQLAlchemy. Include a setup/create_tables.sql file.
```

### Docker-Kafka
```
Kafka runs locally via Docker (single broker, no auth):
  Bootstrap: localhost:9092
  Start with: docker compose up -d (from _shared/docker/kafka/)
Use confluent-kafka-python. Include topic creation in setup.
```

### Pure Python
```
No external infrastructure required. Only pip-installable packages.
All data is generated synthetically within the scripts.
```
