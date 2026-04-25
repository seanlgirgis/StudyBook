# AWS Lambda — ChatGPT Project Prompts

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: AWS Lambda
Slug: aws-lambda
Extra coverage required: execution model — init phase, invoke phase, and shutdown — what happens inside the runtime,
cold starts — what causes them, how long they actually take, and how to mitigate with provisioned concurrency and SnapStart,
invocation types — synchronous, asynchronous, and stream-based — error handling differences between each,
event sources — S3, SQS, SNS, EventBridge, Kinesis, DynamoDB Streams, API Gateway — push vs pull model,
concurrency — reserved concurrency, provisioned concurrency, account-level limits, throttling behavior,
memory and timeout — the memory-CPU coupling, cost math, how to right-size,
Lambda layers — shared libraries, size limits, version pinning,
container image support — up to 10 GB images, when to use vs zip deployment,
VPC networking — ENI creation, cold start penalty, when Lambda actually needs VPC access,
Lambda destinations — async success and failure routing to SQS, SNS, EventBridge, or another Lambda,
Lambda + S3 event notifications — the event-driven ETL pattern,
Lambda for data engineering — trigger-based CDC, lightweight transformation, API backends for data products,
Lambda vs Fargate vs Glue — choosing the right compute for event-driven vs batch vs heavy ETL,
common traps — function timeout on large payloads, missing DLQ on async, hitting concurrency limits silently.
```

Run pipeline after saving the script:
```
run_mission_audio.ps1 -Slug aws-lambda -ChunkSize 750
```

Upload final_aws-lambda.mp3 to R2, then run Project 2.

---

## Project 2 — HTML Page

Run after `final_aws-lambda.mp3` is live on R2.

```
Topic: AWS Lambda
Slug: aws-lambda
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_aws-lambda.mp3
Today's date: 2026-04-25
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\aws-lambda.html
