# Kafka Streaming Micro-Nuggets Production Execution Master Prompt

Use this prompt with external code agents to build a complete, tested Kafka micro-nuggets lane for Data Engineering and interview preparation.

```text
You are a senior code agent working in this repo: D:\StudyBook

MISSION
Build a production-grade Kafka micro-nuggets system for Data Engineering fundamentals, reliability patterns, and interview readiness.
This must be runnable by a beginner on Windows PowerShell.

PRIMARY TARGET LOCATION
Create everything under:
D:\StudyBook\tracks\10_streaming\micro_nuggets\kafka

MANDATORY CONTEXT (READ FIRST)
- Existing Docker streaming stack is already defined in:
  - D:\StudyBook\_infra\docker\streaming.yml
- Existing startup scripts:
  - D:\StudyBook\_infra\scripts\infra_up.ps1
  - D:\StudyBook\_infra\scripts\infra_down.ps1
  - D:\StudyBook\_infra\scripts\infra_health.ps1
- Existing service contract:
  - Kafka: localhost:9092 (host), kafka:29092 (internal)
  - Zookeeper: localhost:2181
  - Kafka UI: http://localhost:8080
- Existing container names in compose:
  - citi_zookeeper
  - citi_kafka
  - citi_kafka_ui

MANDATORY PRE-WORK (DO THIS FIRST)
1) Discover and reuse repository conventions (env loading, diagnostics, runner style) from existing micro-nugget lanes.
2) Validate Docker streaming stack can be started with repo scripts (do not invent a second stack).
3) Create a preparatory setup stage to create topics and seed starter messages.
4) Build a deterministic run-all runner and execute it before claiming done.

NON-NEGOTIABLE REQUIREMENTS
- Production-grade code quality.
- Clear errors and actionable fixes for beginners.
- No hardcoded secrets.
- Windows-first command docs.
- Idempotent setup/reset behavior.
- Every nugget prints meaningful output and completion status.
- All scripts tested before delivery.
- No “done” claim without real command evidence.

PYTHON ENVIRONMENT REQUIREMENTS (MANDATORY)
Use this exact beginner-safe setup flow in README and in prereq checks:

1) Create and activate venv:
   powershell
   cd D:\StudyBook
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

2) Install dependencies:
   powershell
   pip install --upgrade pip
   pip install kafka-python requests

3) Optional high-performance client note:
   - If using confluent-kafka, include explicit install and fallback guidance.
   - If you choose kafka-python, keep implementation consistent throughout lane.

4) Verify dependencies in prereq script.

DOCKER STARTUP REQUIREMENTS (MANDATORY)
All docs and scripts must use existing infra commands:

- Start only streaming group:
  powershell
  pwsh D:\StudyBook\_infra\scripts\infra_up.ps1 -Group streaming

- Check health:
  powershell
  pwsh D:\StudyBook\_infra\scripts\infra_health.ps1

- Confirm Kafka UI:
  http://localhost:8080

- Stop streaming group:
  powershell
  pwsh D:\StudyBook\_infra\scripts\infra_down.ps1 -Group streaming

SCOPE TO IMPLEMENT

A) Folder structure
D:\StudyBook\tracks\10_streaming\micro_nuggets\kafka\
  00_setup\
  01_core_kafka\
  02_reliability\
  03_schema_and_contracts\
  04_stream_processing_patterns\
  05_operations\
  06_interview_drills\
  07_mini_capstone\
  _kafka_connect.py
  run_all_kafka_nuggets.py
  KAFKA_SPEEDY_STORY_AND_INTERVIEW.md
  KAFKA_GLOSSARY.md
  README.md

B) Setup stage (must be implemented and tested)
Create in 00_setup:
1) 00_prereq_check.py
   - Python version
   - dependency checks
   - Kafka broker TCP/connect probe
   - produce+consume smoke check
2) 01_seed_lab.py
   - create required topics with partition/replication settings
   - seed realistic event messages
   - idempotent behavior if topics already exist
3) 99_reset_lab.py
   - safe cleanup for lab topics only
   - requires explicit confirmation flag

C) Required concept coverage

01_core_kafka
- topic creation/listing/describing
- producer basics (keys, partitioning behavior)
- consumer basics (offsets, groups)
- ordering guarantees per partition

02_reliability
- at-least-once semantics demo
- idempotent producer concept and practical approximation
- retry/backoff patterns
- dead-letter topic pattern
- poison message handling

03_schema_and_contracts
- JSON event envelope standards
- versioned schema fields and backward-compat checks
- contract validation in code before produce/consume
- optional Avro section with graceful fallback if registry not configured

04_stream_processing_patterns
- tumbling/sliding window aggregation example
- watermark/late-event handling simulation
- dedup by event_id + event_time
- out-of-order event demonstration

05_operations
- consumer lag estimation basics
- rebalance behavior explanation + demo notes
- partition skew detection
- throughput and error counters
- troubleshooting guide scripts

06_interview_drills
- 10+ runnable scenario drills with concise model answers
- include ordering, exactly-once myths, offsets, retries, DLQ, partitions, consumer groups

07_mini_capstone
- end-to-end pipeline:
  - ingest raw events to bronze topic
  - consume/clean/dedup to silver topic
  - aggregate to gold topic or local analytical sink
- include one failure injection and recovery demonstration

RUNNER + VALIDATION (MANDATORY)
Implement:
D:\StudyBook\tracks\10_streaming\micro_nuggets\kafka\run_all_kafka_nuggets.py

Runner requirements:
- deterministic script order
- one-line PASS/FAIL per script
- timeout per script
- robust subprocess output capture
- Windows-safe console output encoding
- summary totals with failed-script list

Before delivery, you must run and report:
1) setup prereq check
2) seed script
3) full run-all
4) reset script (optional but preferred)

BEGINNER README (MANDATORY)
README must contain exact copy/paste blocks for:
1) activate venv
2) install dependencies
3) start Docker streaming stack
4) run prereq check
5) run seed
6) run single nugget
7) run all nuggets
8) reset lab
9) stop Docker stack
10) common errors and exact fixes

Required error-fix entries:
- Kafka broker unreachable on 9092
- Zookeeper not healthy
- Topic already exists
- Group already active/rebalance delays
- Message decode errors
- Windows execution policy issues for venv activation

GLOSSARY + STORY (MANDATORY)
Create:
- KAFKA_GLOSSARY.md
  - plain-English definitions
  - include: broker, topic, partition, offset, consumer group, rebalance, ISR, ACKs, idempotent producer, DLQ, watermark, exactly-once semantics
- KAFKA_SPEEDY_STORY_AND_INTERVIEW.md
  - guided storyline from beginner to DE-ready
  - 30+ interview Q&A with concise answers
  - link Q&A to runnable nuggets

QUALITY BAR
- No placeholders/TODOs.
- No fake successful output in docs.
- No absolute machine-specific paths in code except repo-root-safe references.
- Keep files ASCII unless unavoidable.
- Keep setup and runner idempotent.

DELIVERY FORMAT
At completion, provide:
1) full file tree created
2) module-by-module implementation summary
3) exact validation commands run
4) pass/fail table with totals
5) known constraints/blockers (if any)
6) next recommended phase after Kafka lane

WORK STYLE
- Make reasonable assumptions and proceed.
- Do not stop for optional clarifications.
- Finish end-to-end with tested artifacts.
```
