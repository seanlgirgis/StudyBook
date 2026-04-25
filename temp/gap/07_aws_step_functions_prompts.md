# AWS Step Functions — ChatGPT Project Prompts

Priority: 🟠 Important — Toyota gap #7

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: AWS Step Functions
Slug: aws-step-functions

Extra coverage required:
- What Step Functions is — a serverless state machine orchestrator, not a scheduler; it coordinates services, not compute
- State types — Task (calls a service), Choice (branching), Parallel (fan-out), Map (iterate over array), Wait, Pass, Succeed, Fail
- Standard vs Express workflows — Standard: exactly-once, up to 1 year, audit history, priced per transition; Express: at-least-once, up to 5 min, high throughput, priced per execution duration
- Task state integrations — Lambda, ECS, Glue, EMR, DynamoDB, SQS, SNS, and 200+ AWS services via SDK integrations
- SDK integrations — optimistic (request-response) vs pessimistic (wait for task token) — how to call AWS services without a Lambda wrapper
- Error handling — Catch and Retry blocks on every Task state; exponential backoff config; ResultPath to preserve original input alongside error context
- Map state — dynamic parallel processing of an array input; inline mode vs distributed mode for datasets over 40MB
- Parallel state — fan out to concurrent independent branches and wait for all to complete before continuing
- Choice state — branching on input values using conditions; no code required, purely declarative
- Data pipeline patterns — chaining Glue crawlers, Glue ETL jobs, EMR steps, ECS tasks in sequence with error handling
- Step Functions vs Airflow — Step Functions wins for AWS-native event-driven workflows; Airflow wins for complex DAG dependencies and Python-heavy logic
- Monitoring — execution history in console, CloudWatch metrics for execution counts and durations, X-Ray tracing for latency breakdown
- Cost model — Standard: $0.025 per 1000 state transitions; Express: $1 per million executions plus duration; math matters at scale

SCOPE FENCE:
- Target 12–16 HOST/SEAN exchanges total
- Each bullet = at most one exchange
- SEAN answers: 3–5 sentences max, no monologues
- Merge the least distinct bullets if the list runs long
- Do NOT elaborate into a textbook — this feeds a reference audio script
```

Run pipeline after saving the script:
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

SCOPE FENCE:
- Create exactly these sections, in this order:
  1. What Step Functions Is — orchestrator, not scheduler
  2. State Types — Task, Choice, Parallel, Map, Wait, Pass
  3. Standard vs Express Workflows
  4. SDK Integrations — calling AWS without Lambda
  5. Error Handling — Catch, Retry, ResultPath
  6. Map & Parallel States — fan-out patterns
  7. Data Pipeline Orchestration Patterns
  8. Step Functions vs Airflow — decision guide
  9. Monitoring & Cost Model
  10. Interview Q&A — 6 realistic senior-level pairs
  11. Quick Reference — 12–15 rows
- Per section: 2–3 tight paragraphs, one code block max (20 lines)
- No step-by-step tutorials, no full worked examples
- Cheat sheet rows must each earn their place — no padding

Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\aws-step-functions.html
