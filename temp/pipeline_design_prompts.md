# Data Pipeline Architecture & Design — ChatGPT Project Prompts

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Data Pipeline Architecture and Design
Slug: pipeline-design
Extra coverage required: how to architect a new pipeline from scratch — starting from consumers not sources,
batch vs streaming — the decision framework before you touch any tool,
designing for idempotency — why it is the first constraint not an afterthought,
microservices boundaries for data engineering — how to decide when one service becomes two,
service communication — sync vs async, REST vs event-driven, and what coupling really costs,
data contracts and schema evolution — who breaks when a field changes, backward vs forward compatibility,
the testing pyramid for data pipelines — unit, integration, contract, end-to-end, and data quality tests,
testing a transformation that runs on 500 GB — sampling, local test datasets, schema-only validation,
testing idempotency — run it twice and compare,
data quality validation — row count reconciliation, null propagation, deduplication, freshness checks,
observability and SLAs — pipeline health metrics, consumer lag, freshness SLOs, alerting thresholds,
late-arriving data — watermarking, grace periods, when to close a window vs reprocess,
backfill strategy — how to reprocess 2 years of history without blocking production,
replay design — immutable source, idempotent sinks, offset-based replay,
failure modes and recovery — transient vs fatal errors, dead letter queues, compensating transactions,
build vs buy — honest cost of ownership when choosing managed services vs custom builds,
how to handle technical debt when the right architecture takes longer than the deadline,
interview framing — how to structure answers to architecture questions to show senior-level thinking.
```

Run pipeline after saving the script:
```
run_mission_audio.ps1 -Slug pipeline-design -ChunkSize 750
```

Upload final_pipeline-design.mp3 to R2, then run Project 2.

---

## Project 2 — HTML Page

Run after `final_pipeline-design.mp3` is live on R2.

```
Topic: Data Pipeline Architecture and Design
Slug: pipeline-design
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_pipeline-design.mp3
Today's date: 2026-04-25
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\pipeline-design.html
