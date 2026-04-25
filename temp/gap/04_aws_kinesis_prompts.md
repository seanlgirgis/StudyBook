# AWS Kinesis — ChatGPT Project Prompts

Priority: 🔴 Critical — Toyota gap #4 (IoT / sensor data)

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: AWS Kinesis
Slug: aws-kinesis
Extra coverage required: Kinesis Data Streams — shards, partition keys, sequence numbers, retention period,
shard capacity math — 1 MB/s in, 2 MB/s out per shard — how to size for your throughput,
enhanced fan-out — dedicated throughput per consumer, when it justifies the cost,
Kinesis Data Firehose — fully managed delivery to S3, Redshift, OpenSearch, Splunk,
Firehose buffering — time and size buffering, format conversion to Parquet, compression,
Kinesis Data Analytics / Managed Apache Flink — stream processing SQL and stateful operators,
Kinesis vs Kafka / MSK — architectural differences, operational tradeoffs, when to choose each,
Kinesis vs SQS — when a queue is enough vs when you need a stream,
Lambda as Kinesis consumer — batch window, bisect on error, iterator age metric,
Kinesis for IoT and telemetry — ingesting high-frequency sensor data from manufacturing systems,
resharding — split and merge shards for scaling, the hot shard problem,
ordering guarantees — per-shard ordering, how partition key design affects order,
consumer group patterns — KCL (Kinesis Client Library) for stateful consumers,
monitoring — GetRecords.IteratorAgeMilliseconds as the key lag metric,
cost model — shard-hour pricing, extended retention, enhanced fan-out costs.

SCOPE FENCE: Target 12-16 HOST/SEAN exchanges total. Each bullet above = at most
one exchange. SEAN answers: 3-5 sentences maximum, no monologues. If the bullet list
has more items than exchanges, merge the least distinct ones. Do not elaborate into
a textbook - this feeds a reference audio script, not a lecture series.
```\r\n\r\nRun pipeline after saving the script:
```
run_mission_audio.ps1 -Slug aws-kinesis -ChunkSize 750
```

Upload final_aws-kinesis.mp3 to R2, then run Project 2.

---

## Project 2 — HTML Page

Run after `final_aws-kinesis.mp3` is live on R2.

```
Topic: AWS Kinesis
Slug: aws-kinesis
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_aws-kinesis.mp3
Today's date: 2026-04-25

Content sections — create exactly these, in this order:
Kinesis Data Streams | Shard Sizing & Capacity | Enhanced Fan-Out | Kinesis Firehose | Kinesis Analytics & Flink | Kinesis vs Kafka vs SQS | Lambda as Consumer | Ordering & Resharding | Cost Model
Then add: Interview Q&A (6 pairs) | Quick Reference (12-15 rows)
Size per section: 2-3 tight paragraphs, one code block max (20 lines). No tutorials.
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\aws-kinesis.html
