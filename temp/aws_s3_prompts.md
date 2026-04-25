# Amazon S3 — ChatGPT Project Prompts

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Amazon S3
Slug: aws-s3
Extra coverage required: object model — keys, buckets, metadata, ETags, and how S3 is not a filesystem,
storage classes — Standard, Standard-IA, One Zone-IA, Glacier Instant, Glacier Flexible, Deep Archive — cost vs retrieval tradeoff,
Intelligent-Tiering — how it monitors and moves objects automatically, when it saves money and when it does not,
three-zone data lake pattern — raw, processed, curated zones and access patterns per zone,
Hive-style partitioning — year/month/day folder structure, how Athena and Glue use it for partition pruning,
security model — bucket policies, block public access settings, ACLs (and why to disable them), SSE-KMS vs SSE-S3,
VPC endpoints for S3 — Gateway endpoint, access from private subnets without NAT, bucket policy enforcement,
S3 event notifications — Lambda, SQS, SNS triggers for event-driven pipelines,
strong consistency — how S3 became strongly consistent in 2020 and what that means for pipelines,
lifecycle policies — transition rules, expiration, noncurrent version management,
multipart upload — when S3 requires it, how to handle incomplete uploads with lifecycle rules,
S3 Select and S3 Object Lambda — filtering and transforming data server-side before it leaves S3,
replication — same-region and cross-region, use cases for compliance and disaster recovery,
cost model — storage per GB, request pricing, data transfer, and the retrieval cost trap with Glacier,
data engineering patterns — S3 as the source of truth, landing zone for Firehose, trigger for Glue and Lambda.
```

Run pipeline after saving the script:
```
run_mission_audio.ps1 -Slug aws-s3 -ChunkSize 750
```

Upload final_aws-s3.mp3 to R2, then run Project 2.

---

## Project 2 — HTML Page

Run after `final_aws-s3.mp3` is live on R2.

```
Topic: Amazon S3
Slug: aws-s3
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_aws-s3.mp3
Today's date: 2026-04-25
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\aws-s3.html
