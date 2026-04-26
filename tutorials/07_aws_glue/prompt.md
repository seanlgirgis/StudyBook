# ChatGPT Prompt — AWS Glue Tutorial
# Paste everything between the === markers into ChatGPT

===

TOPIC: AWS Glue for Data Engineers
SLUG: aws-glue
PRIORITY: Toyota Interview Prep
INFRASTRUCTURE: AWS (boto3 for control plane; Glue scripts run in AWS)

===== CODING STANDARDS =====

FILE HEADER:
# ============================================================
# Topic   : AWS Glue
# File    : NN_filename.py
# Covers  : one-line description
# Prereqs : pip install boto3 | AWS credentials | S3 bucket
# Run     : python filename.py
# ============================================================

COMMENTS: Explain WHY. Glue has many gotchas — always call them out.
Env vars: AWS_REGION, AWS_PROFILE, GLUE_S3_BUCKET, GLUE_IAM_ROLE_ARN

===== FILES TO GENERATE =====

01_glue_catalog.py
  Purpose: Glue Data Catalog — databases, tables, crawlers, schema discovery
  Key concepts: Catalog as Hive metastore, crawlers, classifiers, partition projection
  Functions:
    - create_catalog_database(name, description)
    - create_catalog_table(database, name, s3_location, schema_cols, partition_keys)
    - create_crawler(name, role_arn, s3_targets, database, schedule=None)
    - run_crawler_and_wait(name, timeout=300)
    - get_table_details(database, table) — show columns, partitions, location
    - list_partitions(database, table) — show discovered partitions
  Main block: create database, table, crawler; run crawler; inspect results

02_glue_etl_jobs.py
  Purpose: Create and run Glue ETL jobs — DynamicFrame, transforms, bookmarks
  Key concepts: DynamicFrame vs DataFrame, job bookmarks, resolveChoice, ApplyMapping
  Functions:
    - create_glue_job(name, role_arn, script_s3_path, glue_version="4.0", workers=2)
    - start_job_run(job_name, arguments)
    - wait_for_job_run(job_name, run_id, poll_interval=15)
    - get_job_run_metrics(job_name, run_id) — DPU-hours, duration, error message
    - enable_job_bookmark(job_name) — configure incremental processing
    - generate_sample_etl_script(source_bucket, target_bucket) — return PySpark+Glue script string
  Main block: create job, start run with sample script, monitor, show metrics

03_glue_triggers_and_workflows.py
  Purpose: Automate Glue — scheduled triggers, event triggers, Glue Workflows
  Key concepts: trigger types (SCHEDULED, CONDITIONAL, ON_DEMAND), Workflow, crawl-then-transform
  Functions:
    - create_scheduled_trigger(name, job_name, cron_expression)
    - create_conditional_trigger(name, watch_job, then_run_job, watch_state="SUCCEEDED")
    - create_workflow(name, jobs_sequence) — crawler → job chain
    - start_workflow_run(workflow_name)
    - get_workflow_run_status(workflow_name, run_id) — node-by-node status
  Main block: build a crawler → ETL job workflow definition

04_glue_data_quality.py
  Purpose: Glue Data Quality — define rules, evaluate, act on failures
  Key concepts: DQDL rules, Evaluate Data Quality transform, rulesets, outcomes
  Functions:
    - build_ruleset(rules) — construct DQDL ruleset string
    - create_data_quality_ruleset(name, database, table, ruleset_string)
    - start_data_quality_run(ruleset_name, database, table, role_arn)
    - get_data_quality_results(run_id) — pass/fail per rule, overall outcome
    - common_rules_for_etl_output() — generate standard rules: completeness, uniqueness, freshness
  Main block: create ruleset with 5 common ETL rules, run evaluation, show results

05_glue_vs_emr_vs_lambda.py
  Purpose: Decision guide — Glue vs EMR vs Lambda for ETL, with concrete scenarios
  Key concepts: managed vs configurable, DPU pricing, cold start, use-case matrix
  Functions:
    - calculate_glue_cost(dpu_count, hours, glue_version="4.0")
    - calculate_emr_cost(instance_type, core_count, hours, spot=True)
    - calculate_lambda_cost(invocations, avg_duration_ms, memory_mb)
    - recommend_service(data_size_gb, frequency, latency_req_s, team_spark_expertise)
    - print_decision_matrix() — formatted table of all 3 services across key dimensions
  Main block: run 4 real-world scenario recommendations

===== CAPSTONE PROJECT =====

capstone/brief.md
  Title: Automated Data Lake ETL Pipeline
  Scenario: Raw JSON files land daily in S3 raw/ prefix. Build a Glue pipeline that:
    crawls new files → validates with Data Quality rules → transforms JSON to Parquet
    in silver/ → updates catalog partitions → reports metrics.
  What to build:
    - setup.py: create catalog database, S3 structure, upload sample JSON files
    - pipeline.py: create crawler, data quality ruleset, ETL job; wire them with a workflow
    - monitor.py: check workflow run status, pull DQ results, print cost report
    - cleanup.py: remove all created Glue resources

  Acceptance criteria:
    - Crawler discovers JSON files and creates catalog table
    - DQ rules catch a deliberately bad file (null key column)
    - ETL job converts valid files to Parquet with correct schema
    - Cost report shows DPU-hours consumed

capstone/capstone.py — orchestration
capstone/test_capstone.py — test DQ rule builder, cost calculator, mock boto3

===== INFRASTRUCTURE NOTES =====

AWS account required. Glue needs an IAM role with S3 and Glue permissions.
Glue 4.0 pricing: $0.44/DPU-hour (2 DPU minimum = $0.88/hour minimum).
Job bookmarks require job to be run with --job-bookmark-option job-bookmark-enable.
Glue scripts must be uploaded to S3 before job creation.

===== START =====

Acknowledge these instructions, then wait for me to say "generate file 01".

===
