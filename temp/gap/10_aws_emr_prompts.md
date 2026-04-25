# AWS EMR — ChatGPT Project Prompts

Priority: 🟡 Good to have — Toyota gap #10

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: AWS EMR
Slug: aws-emr

Extra coverage required:
- What EMR is — managed Hadoop and Spark on EC2; AWS handles cluster provisioning, Hadoop config, and patching
- Cluster anatomy — primary node (driver, YARN ResourceManager), core nodes (HDFS + executors), task nodes (executors only, no HDFS, safe to lose)
- EMR on EC2 vs EMR Serverless vs EMR on EKS — persistent cluster vs auto-scaling serverless vs Kubernetes-based; cost and control tradeoffs
- EMR Serverless — no cluster management, auto-scaling vCPUs and memory, pay-per-second, cold start adds ~1 min to first job
- Instance fleet vs instance group — fleet uses multiple instance types for Spot diversification; group locks to one type, simpler but higher interruption risk
- Spot instances on EMR — 60–90% cost savings; task nodes are the safest Spot target; graceful decommission handles interruptions
- Bootstrap actions — shell scripts that run on every node at launch; used to install Python packages, set Hadoop properties, configure logging
- EMR steps — submitting Spark jobs as managed steps; step concurrency up to 256; step failure modes: CONTINUE vs TERMINATE_CLUSTER
- EMRFS — the S3-compatible filesystem for EMR; replaces HDFS for persistent storage; consistent view handles S3 eventual consistency
- EMR and Glue Data Catalog — using Glue as the shared Hive metastore; tables defined once, queryable from EMR, Athena, and Glue ETL jobs
- Performance tuning — right-sizing instance types, YARN memory vs executor memory, dynamic allocation, spark.sql.shuffle.partitions
- EMR vs Glue — EMR: full control, longer startup, lower cost at scale; Glue: managed, faster to start, higher cost per DPU, 2.5 DPU minimum
- Cost optimization — auto-termination after idle time, Reserved Instances for persistent clusters, Spot for task nodes, S3 instead of HDFS

SCOPE FENCE:
- Target 12–16 HOST/SEAN exchanges total
- Each bullet = at most one exchange
- SEAN answers: 3–5 sentences max, no monologues
- Merge the least distinct bullets if the list runs long
- Do NOT elaborate into a textbook — this feeds a reference audio script
```

Run pipeline after saving the script:
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

SCOPE FENCE:
- Create exactly these sections, in this order:
  1. What EMR Is — managed Hadoop/Spark on EC2
  2. Cluster Anatomy — primary, core, task nodes
  3. EMR Variants — EC2 vs Serverless vs EKS
  4. Instance Fleets & Spot Strategy
  5. Bootstrap Actions & EMR Steps
  6. EMRFS & Glue Data Catalog Integration
  7. Performance Tuning
  8. EMR vs Glue — decision guide
  9. Cost Optimization
  10. Interview Q&A — 6 realistic senior-level pairs
  11. Quick Reference — 12–15 rows
- Per section: 2–3 tight paragraphs, one code block max (20 lines)
- No step-by-step tutorials, no full worked examples
- Cheat sheet rows must each earn their place — no padding

Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\aws-emr.html
