# Amazon Redshift — ChatGPT Project Prompts

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Amazon Redshift
Slug: aws-redshift
Extra coverage required: columnar storage and why it matters for analytical workloads — compression and scan efficiency,
distribution styles — EVEN, KEY, and ALL — how to pick the right one and what happens when you get it wrong,
sort keys — compound vs interleaved — the tradeoffs and when interleaved stopped being worth it,
COPY command — bulk loading from S3, manifest files, COMPUPDATE, STATUPDATE,
WLM — workload management queues — concurrency scaling, manual vs auto WLM, queue hopping,
VACUUM and ANALYZE — why deleted rows stay, when to run VACUUM SORT, VACUUM DELETE, auto vacuum,
EXPLAIN plan reading — reading the query plan, spotting DS_DIST_INNER and DS_BCAST_INNER,
Redshift Spectrum — querying S3 directly from Redshift using external tables and the Glue Data Catalog,
materialized views — refresh strategies and when they help vs hurt,
Redshift Serverless vs provisioned — cost model differences, RPU pricing, when serverless saves money,
RA3 nodes and managed storage — decoupling compute and storage, cross-instance restore,
Redshift vs Athena — dedicated warehouse vs serverless SQL — when each wins,
data engineering patterns — loading from S3, transforming with SQL, sharing results via Spectrum,
common performance traps — missing sort key, skewed distribution, large COPY without ANALYZE.
```

Run pipeline after saving the script:
```
run_mission_audio.ps1 -Slug aws-redshift -ChunkSize 750
```

Upload final_aws-redshift.mp3 to R2, then run Project 2.

---

## Project 2 — HTML Page

Run after `final_aws-redshift.mp3` is live on R2.

```
Topic: Amazon Redshift
Slug: aws-redshift
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_aws-redshift.mp3
Today's date: 2026-04-25
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\aws-redshift.html
