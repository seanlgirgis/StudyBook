# AWS Step Functions — ChatGPT Project Prompts

Priority: 🟠 Important — Toyota gap #7

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: AWS Step Functions
Slug: aws-step-functions
Extra coverage required: what Step Functions is — a serverless state machine orchestrator, not a scheduler,
state machine concepts — states, transitions, input/output processing, state types,
state types — Task, Choice, Parallel, Map, Wait, Pass, Succeed, Fail,
Standard vs Express workflows — execution duration limits, pricing model, exactly-once vs at-least-once,
Task state — integrating Lambda, ECS, Glue, EMR, DynamoDB, SQS, SNS, and 200+ AWS services,
SDK integrations — optimistic vs pessimistic — calling AWS services directly without Lambda wrappers,
error handling — Catch and Retry blocks, exponential backoff, ResultPath for error context,
Map state — dynamic parallel processing of arrays — inline vs distributed mode for large datasets,
Parallel state — fanning out to concurrent branches and waiting for all to complete,
Choice state — branching logic based on input values without code,
Step Functions for data pipelines — orchestrating Glue crawlers, Glue ETL jobs, EMR steps, ECS tasks,
Step Functions vs Airflow — when to choose each for pipeline orchestration,
Express Workflows for high-frequency event processing — IoT sensor pipelines,
monitoring — execution history, CloudWatch metrics, X-Ray tracing,
cost model — state transitions pricing, Standard vs Express math at scale.

SCOPE FENCE: Target 12-16 HOST/SEAN exchanges total. Each bullet above = at most
one exchange. SEAN answers: 3-5 sentences maximum, no monologues. If the bullet list
has more items than exchanges, merge the least distinct ones. Do not elaborate into
a textbook - this feeds a reference audio script, not a lecture series.
```\r\n\r\nRun pipeline after saving the script:
```
run_mission_audio.ps1 -Slug aws-step-functions -ChunkSize 750
```

Upload final_aws-step-functions.mp3 to R2, then run Project 2.

---

## Project 2 — HTML Page

Run after `final_aws-step-functions.mp3` is live on R2.

```
Topic: AWS Step Functions
Slug: aws-step-functions
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_aws-step-functions.mp3
Today's date: 2026-04-25

Content sections — create exactly these, in this order:
What Step Functions Is | State Types | Standard vs Express Workflows | SDK Integrations | Error Handling | Map & Parallel States | Data Pipeline Patterns | Step Functions vs Airflow | Monitoring & Cost
Then add: Interview Q&A (6 pairs) | Quick Reference (12-15 rows)
Size per section: 2-3 tight paragraphs, one code block max (20 lines). No tutorials.
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\aws-step-functions.html
