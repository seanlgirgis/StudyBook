# Apache Kafka — ChatGPT Project Prompts

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Apache Kafka
Slug: apache-kafka
Extra coverage required: core concepts — topics, partitions, offsets, brokers, and the log-based storage model,
producers — batching, compression (lz4 vs snappy vs gzip), acks settings (0, 1, all), retries and idempotency,
consumers — the poll loop, offset commit strategies (auto vs manual), what happens on consumer crash,
consumer groups — partition assignment, group coordinator, rebalancing — triggered by join/leave/heartbeat timeout,
replication — ISR (in-sync replicas), leader election, min.insync.replicas and the durability-availability tradeoff,
delivery semantics — at-most-once, at-least-once, exactly-once — what each means in practice and what exactly-once actually costs,
Schema Registry — why schemas matter for stream consumers, Avro vs JSON schema, backward vs forward compatibility modes,
Kafka Connect — source and sink connectors, SMTs (Single Message Transforms), S3 sink connector pattern,
Kafka Streams — stateful stream processing inside the broker ecosystem, windowing, joins,
ksqlDB — streaming SQL over Kafka topics, pull queries vs push queries,
Kafka vs Kinesis — architectural differences, when to choose Kafka over AWS-native streaming,
retention and compaction — time-based vs size-based retention, log compaction for changelog topics,
consumer lag monitoring — what lag means, how to alert on it, CloudWatch metrics for MSK,
data engineering use cases — CDC ingestion, event-driven ETL trigger, real-time pipeline fan-out,
common production traps — hot partitions, rebalance storms, unclean leader election.
```

Run pipeline after saving the script:
```
run_mission_audio.ps1 -Slug apache-kafka -ChunkSize 750
```

Upload final_apache-kafka.mp3 to R2, then run Project 2.

---

## Project 2 — HTML Page

Run after `final_apache-kafka.mp3` is live on R2.

```
Topic: Apache Kafka
Slug: apache-kafka
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_apache-kafka.mp3
Today's date: 2026-04-25
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\apache-kafka.html
