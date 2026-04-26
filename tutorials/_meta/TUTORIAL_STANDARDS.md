# Tutorial Standards
# StudyBook — Senior Data Engineer Learning System

All tutorial files generated for this system must follow these standards exactly.
ChatGPT prompts reference this document. Every generated file is judged against it.

---

## FILE HEADER — required on every .py file

```python
# ============================================================
# Topic   : {TOPIC NAME}
# File    : {NN}_{filename}.py
# Covers  : {one-line description of what this file demos}
# Prereqs : {what must be set up / installed first}
# Run     : python {filename}.py
# ============================================================
```

---

## COMMENT PHILOSOPHY

Comments explain WHY, not WHAT. The code shows what. The comment shows the reasoning.

BAD:
```python
# loop through records
for record in records:
```

GOOD:
```python
# Process records one-at-a-time rather than in bulk because the downstream
# API enforces a per-record rate limit of 100 req/s. Bulk inserts would
# require client-side batching logic that obscures the core concept here.
for record in records:
```

Every non-trivial block gets a comment. Every design decision gets a comment.
Numbers and thresholds get a comment explaining where they come from.

---

## FUNCTION / CLASS DOCSTRINGS

Every function must have a docstring with:
- What it does (one line)
- WHY this approach was chosen (the senior insight)
- Args with types and meaning
- Returns with type and meaning
- Raises if applicable
- Example usage

```python
def put_records_batch(stream_name: str, records: list[dict]) -> dict:
    """
    Write a batch of records to a Kinesis Data Stream.

    Uses PutRecords (batch API) instead of PutRecord (single) because
    PutRecords reduces API call overhead by up to 5x for high-throughput
    producers. The tradeoff is partial failure handling — PutRecords can
    succeed partially, so we must check FailedRecordCount in the response.

    Args:
        stream_name: Kinesis stream name (not ARN — the SDK resolves it)
        records: list of dicts with 'Data' (bytes) and 'PartitionKey' (str)

    Returns:
        dict: PutRecords response including FailedRecordCount and per-record Results

    Raises:
        ClientError: if the stream does not exist or throughput is exceeded

    Example:
        records = [{"Data": b"hello", "PartitionKey": "sensor-01"}]
        response = put_records_batch("my-stream", records)
    """
```

---

## CODE STANDARDS

- Python 3.11+
- Type hints on all function signatures
- f-strings for string formatting (not .format() or %)
- os.environ for all credentials and config — NEVER hardcode
- Use the shared logger from `_shared/logger.py`
- Use the shared AWS session from `_shared/aws_session.py`
- `if __name__ == "__main__":` block on every file that demonstrates all functions
- No placeholder code — every function must work when run
- Error handling: catch specific exceptions, log with context, re-raise or handle explicitly

---

## ENVIRONMENT VARIABLES

All config comes from environment variables. Every file that needs them
must document them at the top:

```python
# Required environment variables:
#   AWS_REGION          — e.g. us-east-1
#   AWS_PROFILE         — optional, uses default if not set
#   KINESIS_STREAM_NAME — the stream to read/write
```

---

## MAIN BLOCK STANDARD

The `if __name__ == "__main__":` block must:
1. Print a clear header showing what is being demonstrated
2. Call every major function defined in the file
3. Print results in a readable format
4. Catch and log top-level errors gracefully

```python
if __name__ == "__main__":
    print("=" * 60)
    print("DEMO: Kinesis Producer Patterns")
    print("=" * 60)

    logger.info("Starting producer demo", stream=STREAM_NAME)
    # ... demo calls ...
```

---

## CAPSTONE STANDARDS

Every capstone folder contains:

| File | Purpose |
|---|---|
| `brief.md` | Problem statement, acceptance criteria, what to build |
| `capstone.py` | The complete working solution |
| `test_capstone.py` | pytest tests validating the solution |
| `setup/` | Any DB scripts, docker-compose, sample data needed |

The capstone must:
- Be a realistic mini-project (not a toy)
- Use at least 3 concepts from the tutorial files
- Be completable in 2-4 hours
- Have clear acceptance criteria in brief.md

---

## INFRASTRUCTURE CATEGORIES

| Category | What it uses | Setup required |
|---|---|---|
| AWS | boto3 + real AWS account | AWS credentials in env |
| Docker-DB | `_shared/docker/postgres/` | `docker compose up -d` |
| Docker-Kafka | `_shared/docker/kafka/` | `docker compose up -d` |
| Docker-Search | `_shared/docker/opensearch/` | `docker compose up -d` |
| Pure Python | pip install only | `pip install -r setup/requirements.txt` |

---

## REQUIREMENTS.TXT FORMAT

Every `setup/requirements.txt` pins major versions:

```
boto3>=1.34,<2.0
python-json-logger>=2.0,<3.0
```

Include a comment on non-obvious dependencies explaining why they are needed.
