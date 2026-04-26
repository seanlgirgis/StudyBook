# ChatGPT Prompt — AWS EMR Tutorial
# Paste everything between the === markers into ChatGPT

===

TOPIC: AWS EMR for Data Engineers
SLUG: aws-emr
PRIORITY: Toyota Interview Prep
INFRASTRUCTURE: AWS (boto3) — prefer EMR Serverless to avoid cluster costs

===== CODING STANDARDS =====

FILE HEADER:
# ============================================================
# Topic   : AWS EMR for Data Engineers
# File    : NN_filename.py
# Covers  : one-line description
# Prereqs : pip install boto3 | AWS credentials | S3 bucket for scripts/output
# Run     : python filename.py
# ============================================================

COMMENTS: Explain WHY. Always explain cost implications of EMR choices.
Always include cleanup() — running clusters are expensive.

Required env vars to document per file:
  AWS_REGION, AWS_PROFILE, EMR_S3_BUCKET, EMR_SUBNET_ID, EMR_EC2_KEY_PAIR (optional)

===== FILES TO GENERATE =====

01_emr_cluster_basics.py
  Purpose: Create, monitor, and terminate EMR clusters — instance types, configurations
  Key concepts: master/core/task nodes, instance types, EMR versions, bootstrap actions
  Functions:
    - create_emr_cluster(name, instance_type, core_count, emr_version, s3_bucket)
    - wait_for_cluster(cluster_id, target_state="WAITING", timeout=600)
    - describe_cluster(cluster_id) — show status, instance groups, timeline
    - list_steps(cluster_id) — show submitted and completed steps
    - terminate_cluster(cluster_id)
    - recommend_instance_type(data_size_gb, compute_vs_memory="balanced") — decision guide
  Main block: show cluster creation code (commented to avoid charges), describe existing cluster

02_spark_jobs_on_emr.py
  Purpose: Submit PySpark jobs to EMR — step submission, script upload, monitoring
  Key concepts: EMR steps, action-on-failure, S3 script storage, job arguments
  Functions:
    - upload_script_to_s3(script_path, bucket, prefix) — upload PySpark script before submit
    - submit_spark_step(cluster_id, script_s3_path, args, action_on_failure="CONTINUE")
    - wait_for_step(cluster_id, step_id, poll_interval=15)
    - get_step_logs(cluster_id, step_id, bucket) — find and read logs from S3
    - build_spark_submit_args(conf_overrides, py_files, jars) — construct --conf args
  Main block: upload sample script, submit, monitor, fetch logs

03_emr_serverless.py
  Purpose: EMR Serverless — no cluster management, pay per use, ideal for batch jobs
  Key concepts: Application, Job Run, pre-initialized capacity, worker configuration
  Functions:
    - create_serverless_application(name, emr_version, pre_init_capacity=None)
    - start_serverless_application(application_id)
    - submit_serverless_job(application_id, role_arn, script_s3, args, spark_conf)
    - wait_for_job(application_id, job_id, timeout=600)
    - get_job_details(application_id, job_id) — cost, duration, DPU-hours consumed
    - stop_and_delete_application(application_id)
  Main block: full EMR Serverless lifecycle demo with cost calculation

04_cost_optimization.py
  Purpose: Control EMR spend — Spot instances, auto-scaling, rightsizing, Serverless comparison
  Key concepts: Spot vs On-Demand, instance fleets, auto-scaling policies, Serverless cost model
  Functions:
    - calculate_cluster_cost(instance_type, core_count, hours, use_spot=True)
    - calculate_serverless_cost(dpu_hours, driver_hours)
    - compare_options(job_hours, data_size_gb) — print cost comparison table
    - build_instance_fleet_config(on_demand_capacity, spot_capacity, instance_types)
    - build_autoscaling_policy(min_instances, max_instances, scale_out_metric)
  Main block: cost comparison for 3 job profiles (small/medium/large)

05_monitoring_and_bootstrap.py
  Purpose: EMR monitoring, bootstrap actions, and debugging failed steps
  Key concepts: CloudWatch integration, YARN UI, bootstrap actions, step failure logs
  Functions:
    - create_bootstrap_action(name, script_s3_path, args) — install packages at launch
    - get_cluster_metrics(cluster_id, minutes=60) — YARN memory, containers, CPU
    - find_failed_step_logs(cluster_id, step_id, log_bucket) — locate stderr/stdout
    - parse_spark_log_for_errors(log_content) — extract OOM, shuffle, partition errors
    - setup_cloudwatch_alarms(cluster_id, sns_topic_arn) — memory/CPU alarms
  Main block: show bootstrap action setup, simulate log parsing with sample log content

===== CAPSTONE PROJECT =====

capstone/brief.md
  Title: Large-Scale Log Processing with EMR Serverless
  Scenario: Process one week of simulated web server access logs (1M records) using
    EMR Serverless PySpark. Aggregate by endpoint, status code, and hour.
    Write results as partitioned Parquet to S3.
  What to build:
    - generate_logs.py: generate 1M synthetic log records, upload to S3
    - process_logs.py: PySpark script for EMR (filter, parse, aggregate, write Parquet)
    - orchestrate.py: upload script, create EMR Serverless app, submit job, monitor, report cost
    - cleanup.py: remove S3 files, stop application
  Acceptance criteria:
    - EMR Serverless job completes successfully
    - Output Parquet partitioned by date/status_code
    - Cost report printed (DPU-hours, estimated $)

capstone/capstone.py — orchestration script
capstone/test_capstone.py — test log parsing and aggregation logic locally with pandas

===== INFRASTRUCTURE NOTES =====

AWS account required. EMR Serverless preferred — cheaper than clusters for testing.
Required: S3 bucket for scripts and output, IAM role with EMR Serverless permissions.
EMR Serverless pricing: ~$0.052/vCPU-hour, ~$0.0057/GB-hour (us-east-1)
Running clusters accidentally = significant cost. Always call cleanup() in finally blocks.

===== START =====

Acknowledge these instructions, then wait for me to say "generate file 01".

===
