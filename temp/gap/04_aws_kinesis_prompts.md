# AWS Kinesis — ChatGPT Project Prompts

Priority: 🔴 Critical — Toyota gap #4 (IoT / sensor data)

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: AWS Kinesis
Slug: aws-kinesis

Extra coverage required:
- Kinesis Data Streams — shards, partition keys, sequence numbers, 24h default retention and how to extend it
- Shard capacity math — 1 MB/s in, 2 MB/s out per shard; how to calculate required shards from ingestion rate
- Enhanced fan-out — dedicated 2 MB/s throughput per registered consumer; when the cost is justified vs polling
- Kinesis Data Firehose — fully managed delivery to S3, Redshift, OpenSearch; no consumer code needed
- Firehose buffering — time-based and size-based buffering windows; format conversion to Parquet; Snappy compression
- Kinesis Data Analytics / Managed Flink — stream processing with SQL or Java/Python; stateful operators and windowing
- Kinesis vs Kafka / MSK — managed vs self-managed, replay semantics, ecosystem maturity, when each is the right call
- Kinesis vs SQS — stream vs queue; when ordering and replay matter vs when a queue is sufficient
- Lambda as Kinesis consumer — batch window, bisect-on-error for poison messages, iterator age as the key health metric
- Resharding — splitting and merging shards to scale; the hot shard problem and how partition key design causes it
- Ordering guarantees — ordering is per-shard only; how partition key choice determines co-location of related events
- Monitoring — GetRecords.IteratorAgeMilliseconds is the single most important Kinesis health metric; what threshold to alarm on
- Cost model — shard-hour pricing, extended retention add-on, enhanced fan-out per-consumer cost; how volume drives total spend

SCOPE FENCE:
- Target 12–16 HOST/SEAN exchanges total
- Each bullet = at most one exchange
- SEAN answers: 3–5 sentences max, no monologues
- Merge the least distinct bullets if the list runs long
- Do NOT elaborate into a textbook — this feeds a reference audio script
```

Run pipeline after saving the script:
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

SCOPE FENCE:
- Create exactly these sections, in this order:
  1. Kinesis Data Streams — shards, partition keys, retention
  2. Shard Sizing & Capacity Math
  3. Enhanced Fan-Out vs Standard Polling
  4. Kinesis Firehose — delivery, buffering, format conversion
  5. Kinesis Analytics & Managed Flink
  6. Kinesis vs Kafka vs SQS — decision guide
  7. Lambda as Consumer — patterns and gotchas
  8. Ordering, Resharding & Hot Shards
  9. Monitoring & Cost Model
  10. Interview Q&A — 6 realistic senior-level pairs
  11. Quick Reference — 12–15 rows
- Per section: 2–3 tight paragraphs, one code block max (20 lines)
- No step-by-step tutorials, no full worked examples
- Cheat sheet rows must each earn their place — no padding

Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\aws-kinesis.html
