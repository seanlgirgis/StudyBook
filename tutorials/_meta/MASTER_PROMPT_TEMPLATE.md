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

CLEANUP — MANDATORY FOR ALL AWS FILES (runaway cost prevention):
- Every function that creates an AWS resource MUST have a corresponding delete/cleanup call
- Every main() that creates resources MUST wrap the demo in try/finally with cleanup in the finally block
- Cleanup functions MUST be idempotent — catch "already deleted" errors and continue silently
- Print a ⚠️ COST WARNING immediately after creating any resource that charges by the hour
- Print "✅ Cleanup complete. No ongoing charges." at the end of every cleanup function
- NEVER leave a Kinesis stream, EMR cluster, Glue job, CloudWatch alarm, or log group
  running at the end of a script — they charge money even when idle

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

===== README =====

After file 05, generate a README.md for the topic directory with:
- Prerequisites block (exact PowerShell commands to set env vars and load env_setter.ps1)
- Phase 1 section: one entry per setup file with the run command, what it does, and the key takeaway
- Phase 2 section: capstone run order with exact commands
- Cleanup note: how to emergency-cleanup if a run is interrupted mid-way

===== CAPSTONE PROJECT =====

After the README, generate the capstone:

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
Use os.environ.get("AWS_PROFILE", "study") for profile — local profile is "study".
Do not create real resources that cost money unless clearly commented.
Prefer describe/list operations in demos where possible.
When resources must be created, always include a cleanup() function.

REQUIRED RULES (learned from real execution — follow exactly):
1. S3 Select is deprecated — wrap select_object_content in try/except, catch MethodNotAllowed,
   print a warning and return gracefully instead of crashing.
2. Versioned bucket cleanup — NEVER use a plain delete loop. Use:
     s3_resource = boto3.resource("s3")
     s3_resource.Bucket(BUCKET_NAME).object_versions.delete()
     s3_client.delete_bucket(Bucket=BUCKET_NAME)
3. Multipart file size — use 15 MB synthetic files, not 150 MB. Set TransferConfig:
     multipart_threshold=5*1024*1024, multipart_chunksize=5*1024*1024
4. Resource names — always read from env vars with uuid fallback, never hardcode.
5. us-east-1 CreateBucket — do NOT pass LocationConstraint for us-east-1.
6. Optional env vars — gate optional features (SQS, SNS, etc.) with an if-check,
   print "Skipping — ENV_VAR not set" instead of crashing.
```

### Docker-Postgres
```
PostgreSQL runs locally via Docker (studybook_core stack — already running, do NOT spin up new):
  Host: localhost, Port: 5432
  Database: studybook, User: studybook, Password: studybook
Use psycopg2-binary or SQLAlchemy. Read all connection params from env vars with
the above values as defaults.
```

### Docker-Kafka
```
Kafka runs locally via Docker (studybook_core stack — already running, do NOT spin up new):
  Bootstrap: localhost:29092  ← NOTE: external listener is 29092, NOT 9092
  Kafka UI: http://localhost:8080
Use confluent-kafka-python or kafka-python. Read bootstrap from env var
KAFKA_BOOTSTRAP_SERVERS with default "localhost:29092".
```

### Pure Python
```
No external infrastructure required. Only pip-installable packages.
All data is generated synthetically within the scripts.
Output goes to OUTPUT_DIR env var or /tmp/studybook/{topic}/ by default.
```
