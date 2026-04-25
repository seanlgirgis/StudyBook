# AWS CloudWatch & CloudTrail — ChatGPT Project Prompts

Priority: 🟠 Important — Toyota gap #8

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: AWS CloudWatch and CloudTrail
Slug: aws-cloudwatch

Extra coverage required:
- CloudWatch Metrics — namespaces, dimensions, standard (1-min) vs high-resolution (1-sec) metrics, publishing custom metrics via PutMetricData
- CloudWatch Alarms — static thresholds vs anomaly detection bands; composite alarms combining multiple conditions; alarm actions: SNS, Auto Scaling, EC2
- CloudWatch Logs — log groups and log streams; retention policies (1 day to 10 years); why structured JSON logs are better than plain text
- CloudWatch Logs Insights — query syntax: fields, filter, stats, sort, limit; common queries for finding pipeline errors and slow stages
- CloudWatch Dashboards — building operational views for pipeline health; combining metrics from multiple services in one view
- Metric math — creating derived metrics (e.g. error rate = errors / requests) from raw CloudWatch data without storing a new metric
- EMF (Embedded Metric Format) — logging metrics as structured JSON from Lambda and ECS; avoids PutMetricData API calls and cost
- Container Insights — task-level CPU, memory, and network metrics for ECS and Kubernetes; not enabled by default
- Data pipeline monitoring patterns — Glue job duration and DPU usage, Kinesis IteratorAgeMilliseconds, Lambda error rate, ECS task failures
- Meaningful alarm design — alarm on business-level SLOs ("consumer lag > 5 min") not just resource thresholds ("CPU > 80%")
- CloudTrail — captures every AWS API call; management events (default) vs data events (S3 object access, Lambda invocations — extra cost)
- CloudTrail for compliance — who assumed which IAM role, who deleted which S3 object, what changed in a security group
- Querying CloudTrail with Athena — partition the trail logs in S3 by date; query with standard SQL for audit investigations
- Cost control — high-resolution metrics cost 3x standard; data events in CloudTrail add up fast on busy S3 buckets; log ingestion pricing per GB

SCOPE FENCE:
- Target 12–16 HOST/SEAN exchanges total
- Each bullet = at most one exchange
- SEAN answers: 3–5 sentences max, no monologues
- Merge the least distinct bullets if the list runs long
- Do NOT elaborate into a textbook — this feeds a reference audio script
```

Run pipeline after saving the script:
```
run_mission_audio.ps1 -Slug aws-cloudwatch -ChunkSize 750
```

Upload final_aws-cloudwatch.mp3 to R2, then run Project 2.

---

## Project 2 — HTML Page

Run after `final_aws-cloudwatch.mp3` is live on R2.

```
Topic: AWS CloudWatch and CloudTrail
Slug: aws-cloudwatch
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_aws-cloudwatch.mp3
Today's date: 2026-04-25

SCOPE FENCE:
- Create exactly these sections, in this order:
  1. Metrics — namespaces, dimensions, standard vs high-resolution
  2. Alarms — static, anomaly detection, composite
  3. CloudWatch Logs — groups, streams, retention
  4. Logs Insights — query syntax and pipeline debugging patterns
  5. Dashboards & Metric Math
  6. EMF & Container Insights
  7. Data Pipeline Monitoring Patterns
  8. CloudTrail — API audit trail and compliance
  9. Querying CloudTrail with Athena & Cost Control
  10. Interview Q&A — 6 realistic senior-level pairs
  11. Quick Reference — 12–15 rows
- Per section: 2–3 tight paragraphs; include a code block where it adds value (20 lines max)
- No step-by-step tutorials, no full worked examples
- Cheat sheet rows must each earn their place — no padding

Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\aws-cloudwatch.html
