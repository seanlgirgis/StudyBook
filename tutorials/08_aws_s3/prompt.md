# ChatGPT Prompt — AWS S3 Tutorial
# Paste everything between the === markers into ChatGPT

===

TOPIC: AWS S3 for Data Engineers
SLUG: aws-s3
PRIORITY: Toyota Interview Prep
INFRASTRUCTURE: AWS (boto3, real AWS account)

===== CODING STANDARDS =====

FILE HEADER:
# ============================================================
# Topic   : AWS S3 for Data Engineers
# File    : NN_filename.py
# Covers  : one-line description
# Prereqs : pip install boto3 | AWS credentials | S3 bucket
# Run     : python filename.py
# ============================================================

COMMENTS: Explain WHY. S3 has many gotchas (eventual consistency history, multipart,
presigned URLs, lifecycle, costs). Call them out. Explain pricing implications.
Env vars: AWS_REGION, AWS_PROFILE, S3_BUCKET_NAME

===== FILES TO GENERATE =====

01_s3_fundamentals.py
  Purpose: Core S3 operations — buckets, objects, metadata, tagging, versioning
  Key concepts: bucket naming rules, object key design, storage classes, versioning
  Functions:
    - create_bucket(name, region) — create with correct region handling (us-east-1 quirk)
    - upload_file(bucket, key, local_path, metadata=None, storage_class="STANDARD")
    - download_file(bucket, key, local_path)
    - list_objects(bucket, prefix="", page_size=100) — paginated listing
    - get_object_metadata(bucket, key) — head_object, show ContentType, ETag, metadata
    - enable_versioning(bucket) — turn on versioning, explain why it matters
    - tag_object(bucket, key, tags: dict) — add/replace tags
    - delete_object(bucket, key, version_id=None) — explain delete markers with versioning
  Main block: create bucket, upload 3 objects with different metadata, list, inspect, cleanup

02_s3_multipart_and_streaming.py
  Purpose: Large file uploads/downloads — multipart, streaming, transfer acceleration
  Key concepts: multipart threshold (100MB), part size, concurrent parts, streaming reads
  Functions:
    - upload_large_file(bucket, key, local_path, part_size_mb=100) — manual multipart
    - upload_with_transfer_config(bucket, key, local_path) — boto3 TransferConfig auto-multipart
    - stream_object_lines(bucket, key) — iterate S3 object line-by-line (no full download)
    - generate_synthetic_large_file(path, size_mb) — create test file for multipart demo
    - calculate_multipart_cost(file_size_gb, part_size_mb) — show part count and why it matters
    - download_range(bucket, key, byte_start, byte_end) — byte-range GET for partial reads
  Main block: generate 150MB test file, upload with manual multipart, stream first 100 lines, cleanup

03_s3_security_and_access.py
  Purpose: S3 security — bucket policies, ACLs, presigned URLs, encryption, Block Public Access
  Key concepts: bucket policy vs ACL vs IAM, presigned URL expiry, SSE-S3 vs SSE-KMS, public access block
  Functions:
    - block_all_public_access(bucket) — enable Block Public Access settings
    - apply_bucket_policy(bucket, policy_dict) — set resource-based policy
    - generate_presigned_url(bucket, key, expiry_seconds=3600) — time-limited GET URL
    - generate_presigned_post(bucket, key_prefix, max_size_bytes, expiry_seconds) — browser upload
    - enable_sse_s3(bucket) — server-side encryption with S3 managed keys
    - enable_sse_kms(bucket, kms_key_id) — SSE-KMS with customer managed key
    - check_bucket_security_posture(bucket) — report: public access, encryption, versioning, logging
  Main block: run security posture check on test bucket, fix all findings, verify

04_s3_lifecycle_and_cost.py
  Purpose: S3 cost optimization — lifecycle rules, storage classes, Intelligent-Tiering, cost calculator
  Key concepts: storage class ladder (Standard → IA → Glacier), lifecycle transitions, retrieval costs
  Functions:
    - create_lifecycle_rule(bucket, rule_id, prefix, transitions, expiration_days=None)
      — transitions: list of {"days": N, "storage_class": "STANDARD_IA"}
    - calculate_storage_cost(size_gb, storage_class, region="us-east-1") — monthly cost estimate
    - calculate_retrieval_cost(size_gb, storage_class, requests=1000) — GET + retrieval fees
    - recommend_storage_class(access_frequency_per_month, size_gb, min_storage_days) — decision
    - enable_intelligent_tiering(bucket, prefix) — auto-tiering for unknown access patterns
    - get_bucket_size_and_cost(bucket) — CloudWatch storage metrics + estimated monthly cost
  Main block: show lifecycle rule for log data (30d→IA, 90d→Glacier, 365d→delete), cost comparison

05_s3_event_notifications_and_patterns.py
  Purpose: S3 as event source — notifications, S3 Select, inventory, common DE patterns
  Key concepts: event notifications (Lambda/SQS/SNS), S3 Select SQL, data lake prefix design
  Functions:
    - configure_sqs_notification(bucket, queue_arn, events, prefix_filter=None)
      — trigger SQS on s3:ObjectCreated:*
    - query_object_with_s3_select(bucket, key, sql, input_format="CSV") — SQL on S3 object
    - design_data_lake_prefix(environment, domain, date) — return well-structured key prefix
    - list_objects_by_date_range(bucket, prefix, start_date, end_date) — filter by LastModified
    - create_inventory_config(bucket, destination_bucket, frequency="Weekly") — S3 Inventory setup
    - demonstrate_copy_on_ingest(source_bucket, dest_bucket, key) — copy + tag pattern for raw→bronze
  Main block: demo S3 Select on a CSV file, show prefix design for 3 real scenarios

===== CAPSTONE PROJECT =====

capstone/brief.md
  Title: S3 Data Lake Foundation
  Scenario: Build the S3 layer of a data lake for a manufacturing IoT system.
    Raw sensor files (CSV) land in a raw/ prefix. Build a pipeline that:
    validates file size → copies to bronze/ with metadata tags → applies lifecycle rules
    → generates presigned URLs for external data science team access → reports storage costs.
  What to build:
    - setup.py: create bucket, enable versioning + encryption + Block Public Access,
      create lifecycle rules (30d→IA, 180d→Glacier, 730d→delete for raw/; keep bronze/ forever)
    - ingest.py: simulate 10 sensor CSV files landing in raw/, copy to bronze/ with tags
      (source_system, ingestion_date, data_classification=internal)
    - access.py: generate presigned URLs for last 5 bronze/ files, print with expiry times
    - cost_report.py: calculate current storage cost + projected 12-month cost under lifecycle
    - cleanup.py: empty + delete bucket

  Acceptance criteria:
    - Bucket has versioning, encryption, Block Public Access all enabled
    - bronze/ objects have correct tags and metadata
    - Presigned URLs are valid for 1 hour and accessible
    - Cost report shows cost reduction from lifecycle vs keeping everything in Standard

capstone/capstone.py — orchestration
capstone/test_capstone.py — test lifecycle rule builder, cost calculator, prefix designer (no AWS needed)

===== INFRASTRUCTURE NOTES =====

AWS account required. S3 is nearly free at small scale but be careful with:
- Glacier retrieval fees (avoid in tutorial capstone — use STANDARD_IA instead)
- Versioning + delete markers accumulating — always cleanup with delete_bucket_contents()
- us-east-1 quirk: CreateBucket does NOT take LocationConstraint for us-east-1

===== START =====

Acknowledge these instructions, then wait for me to say "generate file 01".

===
