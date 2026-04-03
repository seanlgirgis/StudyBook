# Spark Structured Streaming Micro-Nuggets Production Execution Master Prompt

Use this prompt with external code agents to build a complete, tested Spark Structured Streaming micro-nuggets lane for Data Engineering and interview preparation.

```text
You are a senior code agent working in this repo: D:\StudyBook

MISSION
Build a production-grade Spark Structured Streaming micro-nuggets lane for Data Engineering.
Goal: teach practical streaming processing (from Kafka to curated outputs), reliability patterns, and interview readiness.
This must be runnable by a beginner on Windows PowerShell.

PRIMARY TARGET LOCATION
Create everything under:
D:\StudyBook\tracks\10_streaming\micro_nuggets\spark_structured_streaming

MANDATORY CONTEXT (READ FIRST)
- Existing Docker stacks:
  - Kafka/Zookeeper/UI: D:\StudyBook\_infra\docker\streaming.yml
  - Spark master/worker: D:\StudyBook\_infra\docker\pipeline.yml
- Existing infra scripts:
  - D:\StudyBook\_infra\scripts\infra_up.ps1
  - D:\StudyBook\_infra\scripts\infra_down.ps1
  - D:\StudyBook\_infra\scripts\infra_health.ps1
- Existing service ports:
  - Kafka host listener: localhost:9092
  - Spark master: localhost:7077
  - Spark master UI: http://localhost:8081
  - Spark worker UI: http://localhost:8085

MANDATORY PRE-WORK (DO THIS FIRST)
1) Reuse existing repo conventions for setup scripts, run-all runners, and beginner docs.
2) Start/validate required Docker groups using repo scripts (do not invent parallel infra):
   - streaming + pipeline
3) Build setup stage that creates topics and seed data used by all nuggets.
4) Implement and execute full run-all validation before claiming completion.

NON-NEGOTIABLE REQUIREMENTS
- Production-grade code quality.
- Idempotent setup/reset behavior.
- Every nugget runnable and outputs clear status.
- No hardcoded secrets.
- Windows-first instructions.
- No fake success claims.
- Must include real validation evidence.

PYTHON ENVIRONMENT REQUIREMENTS (MANDATORY)
Use this exact flow in README and prereq checks:
1) powershell
   cd D:\StudyBook
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
2) powershell
   pip install --upgrade pip
   pip install pyspark kafka-python requests
3) Verify versions in prereq script.
4) If Java is required, detect JAVA_HOME and provide explicit fix instructions.

DOCKER STARTUP REQUIREMENTS (MANDATORY)
Use existing infra scripts only:
1) Start both groups:
   powershell
   pwsh D:\StudyBook\_infra\scripts\infra_up.ps1 -Group streaming
   pwsh D:\StudyBook\_infra\scripts\infra_up.ps1 -Group pipeline
2) Health:
   powershell
   pwsh D:\StudyBook\_infra\scripts\infra_health.ps1
3) Stop:
   powershell
   pwsh D:\StudyBook\_infra\scripts\infra_down.ps1 -Group pipeline
   pwsh D:\StudyBook\_infra\scripts\infra_down.ps1 -Group streaming

SCOPE TO IMPLEMENT

A) Folder structure
D:\StudyBook\tracks\10_streaming\micro_nuggets\spark_structured_streaming\
  00_setup\
  01_streaming_basics\
  02_event_time_and_windows\
  03_stateful_processing\
  04_reliability_and_recovery\
  05_kafka_to_lake_patterns\
  06_operations_and_tuning\
  07_interview_drills\
  08_mini_capstone\
  _spark_stream_connect.py
  run_all_spark_streaming_nuggets.py
  SPARK_STREAMING_SPEEDY_STORY_AND_INTERVIEW.md
  SPARK_STREAMING_GLOSSARY.md
  README.md

B) Setup stage (must be implemented and tested)
Create:
1) 00_setup/00_prereq_check.py
   - Python, pyspark, kafka-python, Java, Spark session creation
   - Kafka broker probe + topic probe
2) 00_setup/01_seed_lab.py
   - create required Kafka topics
   - seed deterministic events for stream tests
   - idempotent behavior
3) 00_setup/99_reset_lab.py
   - cleanup only lab topics/checkpoints/output paths
   - requires explicit confirmation flag

C) Required concept coverage

01_streaming_basics
- readStream from Kafka
- parse JSON payload
- writeStream modes (append/update/complete)
- output sinks: console + parquet/delta-like file sink
- checkpoint basics

02_event_time_and_windows
- event-time column handling
- watermark
- tumbling/sliding windows
- late data behavior

03_stateful_processing
- dedup with event_id + watermark
- stateful aggregations
- handling out-of-order records

04_reliability_and_recovery
- checkpoint recovery after restart
- idempotent writes pattern
- exactly-once discussion (practical limits)
- failure injection and replay behavior

05_kafka_to_lake_patterns
- bronze stream write (raw)
- silver transformation stream
- gold aggregation stream
- schema evolution handling in stream parsing

06_operations_and_tuning
- trigger intervals
- micro-batch metrics interpretation
- backpressure concepts
- partitioning and throughput tuning basics
- troubleshooting slow/lagging streams

07_interview_drills
- 10+ runnable streaming interview scenarios:
  - watermark vs processing time
  - late events
  - checkpoint semantics
  - at-least-once vs exactly-once
  - idempotency in sink design

08_mini_capstone
- end-to-end:
  - ingest click/order events from Kafka
  - bronze -> silver -> gold streaming pipeline
  - intentional bad batch + recovery
  - validation query/output report

RUNNER + VALIDATION (MANDATORY)
Implement:
D:\StudyBook\tracks\10_streaming\micro_nuggets\spark_structured_streaming\run_all_spark_streaming_nuggets.py

Runner must:
- use deterministic order
- print one-line PASS/FAIL per script
- have per-script timeout
- support Windows-safe output encoding
- show summary totals + failed list

Mandatory validation before delivery:
1) prereq check
2) seed setup
3) full run-all
4) reset check (preferred)

BEGINNER README (MANDATORY)
Include exact copy/paste blocks for:
1) venv setup
2) dependency install
3) start Docker services
4) prereq check
5) seed data
6) run one nugget
7) run all nuggets
8) reset lab
9) stop services
10) common errors and fixes

Required error-fix entries:
- Java/JAVA_HOME missing
- Spark session fails to start
- Kafka broker unreachable
- topic missing
- checkpoint permission/path issues
- stream query already active
- Windows execution policy issue

GLOSSARY + STORY (MANDATORY)
Create:
- SPARK_STREAMING_GLOSSARY.md
  - plain-English definitions:
    micro-batch, watermark, trigger, checkpoint, state store, exactly-once, late data, event-time, processing-time, output mode
- SPARK_STREAMING_SPEEDY_STORY_AND_INTERVIEW.md
  - beginner-to-practitioner narrative
  - 30+ concise interview Q&A
  - links to runnable nuggets

QUALITY BAR
- No TODO placeholders.
- No hardcoded machine-specific secrets.
- Idempotent setup/reset.
- Deterministic testable behavior.
- Keep files ASCII unless unavoidable.

DELIVERY FORMAT
At completion provide:
1) full file tree created
2) module-by-module summary
3) exact validation commands run
4) pass/fail table with totals
5) known constraints/blockers (if any)
6) next recommended phase after Spark streaming lane

WORK STYLE
- Make reasonable assumptions and proceed.
- Do not stop for optional clarifications.
- Finish with tested artifacts.
```
