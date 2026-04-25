# AWS EMR — ChatGPT Project Prompts

Priority: 🟡 Good to have — Toyota gap #10

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: AWS EMR
Slug: aws-emr
Extra coverage required: what EMR is — managed Hadoop and Spark on EC2, the control plane for big data jobs,
EMR cluster anatomy — master node, core nodes, task nodes — roles and failure behavior,
EMR on EC2 vs EMR Serverless vs EMR on EKS — when to choose each and the cost model differences,
EMR Serverless — no cluster management, auto-scaling, pay-per-vCPU-second, cold start tradeoff,
instance fleet vs instance group — spot diversification strategy to reduce interruption risk,
Spot instances on EMR — cost savings of 60-90%, handling spot interruption gracefully,
bootstrap actions — installing Python packages, configuring Hadoop properties at cluster launch,
EMR steps — submitting Spark jobs as steps, step concurrency, step failure handling,
EMRFS — the S3-compatible filesystem layer, consistency view, how it differs from HDFS,
EMR and the Glue Data Catalog — using Glue as the shared Hive metastore for EMR Spark jobs,
performance tuning on EMR — instance type selection, dynamic allocation, YARN memory settings,
EMR vs Glue — the real tradeoffs — control, flexibility, cost at scale, startup time,
EMR for large-scale manufacturing data — processing terabytes of historical sensor data with PySpark,
cost optimization — right-sizing clusters, auto-termination, reserved instances for persistent clusters,
monitoring — CloudWatch EMR metrics, Spark History Server, YARN Resource Manager UI.

SCOPE FENCE: Target 12-16 HOST/SEAN exchanges total. Each bullet above = at most
one exchange. SEAN answers: 3-5 sentences maximum, no monologues. If the bullet list
has more items than exchanges, merge the least distinct ones. Do not elaborate into
a textbook - this feeds a reference audio script, not a lecture series.
```\r\n\r\nRun pipeline after saving the script:
```
run_mission_audio.ps1 -Slug aws-emr -ChunkSize 750
```

Upload final_aws-emr.mp3 to R2, then run Project 2.

---

## Project 2 — HTML Page

Run after `final_aws-emr.mp3` is live on R2.

```
Topic: AWS EMR
Slug: aws-emr
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_aws-emr.mp3
Today's date: 2026-04-25

SCOPE FENCE: 8-10 sections maximum. 2-3 tight paragraphs per section.
One code block per section, 20 lines max. Cheat sheet: 12-15 rows.
Reference page only - no step-by-step tutorials or full worked examples.
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\aws-emr.html
