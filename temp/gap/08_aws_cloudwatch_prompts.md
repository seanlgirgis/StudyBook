# AWS CloudWatch & CloudTrail — ChatGPT Project Prompts

Priority: 🟠 Important — Toyota gap #8

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: AWS CloudWatch and CloudTrail
Slug: aws-cloudwatch
Extra coverage required: CloudWatch Metrics — namespaces, dimensions, standard vs high-resolution metrics, custom metrics,
CloudWatch Alarms — static thresholds, anomaly detection, composite alarms, alarm actions,
CloudWatch Logs — log groups, log streams, retention policies, structured logging best practices,
CloudWatch Logs Insights — query syntax, common queries for pipeline debugging and error analysis,
CloudWatch Dashboards — building operational views for pipeline health,
metric math — creating derived metrics from raw CloudWatch data,
EMF — Embedded Metric Format — logging metrics directly from Lambda and ECS without PutMetricData calls,
CloudWatch Container Insights — task-level ECS and Kubernetes metrics,
CloudWatch for data pipelines — monitoring Glue job duration, Kinesis iterator age, Lambda error rate, ECS CPU,
setting meaningful SLO-based alarms — not just "CPU > 80%" but "consumer lag > 5 minutes",
CloudTrail — what it records, management events vs data events vs Insights events,
CloudTrail for security and compliance — who assumed which role, who deleted which S3 object,
querying CloudTrail with Athena — finding specific API calls across a time window,
CloudTrail Lake — managed CloudTrail query store without S3 and Athena setup,
cost control — high-resolution metrics cost, data events cost, log ingestion pricing.

SCOPE FENCE: Target 12-16 HOST/SEAN exchanges total. Each bullet above = at most
one exchange. SEAN answers: 3-5 sentences maximum, no monologues. If the bullet list
has more items than exchanges, merge the least distinct ones. Do not elaborate into
a textbook - this feeds a reference audio script, not a lecture series.
```\r\n\r\nRun pipeline after saving the script:
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

Content sections — create exactly these, in this order:
Metrics & Alarms | CloudWatch Logs | Logs Insights | Dashboards & Metric Math | EMF & Container Insights | Pipeline Monitoring Patterns | CloudTrail | Querying CloudTrail with Athena | Cost Control
Then add: Interview Q&A (6 pairs) | Quick Reference (12-15 rows)
Size per section: 2-3 tight paragraphs, one code block max (20 lines). No tutorials.
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\aws-cloudwatch.html
