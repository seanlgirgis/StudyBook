# CI/CD for Data Engineering — ChatGPT Project Prompts

Priority: 🔴 Critical — every senior DE role expects CI/CD discipline on pipeline code

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: CI/CD for Data Engineering
Slug: cicd-data-engineering
Extra coverage required: what CI/CD means for data pipelines — it's not just deploying code, it's validating data contracts, schemas, and logic before production,
GitLab CI / GitHub Actions anatomy — .gitlab-ci.yml or .github/workflows, stages, jobs, runners,
CI pipeline stages for a DE project — lint, unit test, integration test, schema validation, build artifact, deploy,
linting Python pipeline code — flake8, black, ruff — enforcing style in CI so reviewers focus on logic not formatting,
running pytest in CI — installing dependencies, running tests, failing the pipeline on test failure, coverage reports,
environment variables and secrets in CI — CI/CD secret stores, never hardcoding credentials, injecting at runtime,
testing database migrations in CI — running against a test database, validating schema changes don't break queries,
dbt CI — dbt test, dbt compile, slim CI (running only modified models and their dependents), dbt docs generate,
Airflow DAG validation in CI — checking DAGs load without errors, dag.test(), import validation before deploy,
artifact management — building a Docker image in CI, pushing to ECR, tagging with git commit SHA,
deployment strategies for data pipelines — blue/green, canary, rolling — what applies to scheduled pipelines vs streaming,
environment promotion — dev → staging → production, what must pass in each environment before promotion,
data pipeline versioning — semantic versioning for pipeline releases, pinning dependencies, reproducible builds,
rollback strategy — what rolling back a pipeline means when data has already been written, idempotency enables rollback,
infrastructure as code in the pipeline — Terraform plan in CI, Terraform apply gated on review approval,
monitoring CI pipeline health — flaky tests, slow jobs, notification on pipeline failure to Slack or Teams,
real scenario: GitLab CI/CD pipeline for the Citi ETL project — what runs on every merge request, what runs on merge to main.
```

Run pipeline after saving the script:
```
run_mission_audio.ps1 -Slug cicd-data-engineering -ChunkSize 750
```

Upload final_cicd-data-engineering.mp3 to R2, then run Project 2.

---

## Project 2 — HTML Page

Run after `final_cicd-data-engineering.mp3` is live on R2.

```
Topic: CI/CD for Data Engineering
Slug: cicd-data-engineering
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_cicd-data-engineering.mp3
Today's date: 2026-04-25
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\cicd-data-engineering.html
