# CI/CD for Data Engineering — ChatGPT Project Prompts

Priority: 🔴 Critical — every senior DE role expects CI/CD discipline on pipeline code

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: CI/CD for Data Engineering
Slug: cicd-data-engineering

Extra coverage required:
- What CI/CD means for data pipelines — continuous integration validates code, schema, and data contracts on every commit; continuous delivery automates promotion to production
- GitLab CI / GitHub Actions anatomy — .gitlab-ci.yml or .github/workflows; stages run sequentially; jobs within a stage run in parallel; runners execute on VMs or containers
- CI stages for a DE project — lint → unit test → integration test → schema validation → build artifact → deploy; each stage gates the next
- Linting Python pipeline code — flake8, black, ruff; enforcing style in CI so code review focuses on logic not formatting; fast to run, catches obvious errors early
- Running pytest in CI — install dependencies from requirements.txt, run pytest --tb=short, fail the pipeline on any test failure, publish coverage report as artifact
- Secrets in CI — CI/CD variable stores (GitLab CI variables, GitHub secrets); inject as environment variables at runtime; never appear in logs or artifacts
- dbt CI — dbt test on modified models only (slim CI with --select state:modified+); dbt compile to validate SQL; dbt docs generate for updated lineage
- Airflow DAG validation in CI — import each DAG file and check it loads without errors; dag.test() for logic validation; catches syntax errors before deployment
- Docker image build in CI — docker build in CI, push tagged image (git SHA + branch) to ECR; downstream deploy step pulls the exact image SHA
- Environment promotion — dev → staging → production; each environment requires all prior stage tests to pass; staging mirrors production data volume
- Deployment strategies — blue/green (swap load balancer after validation), canary (route 5% of traffic to new version); rolling update for scheduled pipeline containers
- Rollback strategy — idempotent pipelines enable safe reruns from any checkpoint; rollback means rerunning the previous pinned image version, not undoing data writes
- Terraform in CI — terraform plan in CI produces a diff artifact for review; terraform apply runs only on merge to main with approval; prevents infrastructure drift
- Monitoring CI health — alert on flaky tests (intermittent failures), slow jobs that block developers, pipeline failure notifications to Slack or Teams

SCOPE FENCE:
- Target 12–16 HOST/SEAN exchanges total
- Each bullet = at most one exchange
- SEAN answers: 3–5 sentences max, no monologues
- Merge the least distinct bullets if the list runs long
- Do NOT elaborate into a textbook — this feeds a reference audio script
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

SCOPE FENCE:
- Create exactly these sections, in this order:
  1. What CI/CD Means for Data Pipelines
  2. GitLab CI / GitHub Actions Anatomy
  3. CI Stage Pipeline — lint, test, build, deploy
  4. Secrets Management in CI
  5. dbt CI & Airflow DAG Validation
  6. Docker Build & ECR Artifact Management
  7. Environment Promotion — dev → staging → production
  8. Deployment Strategies & Rollback
  9. Terraform in CI & Monitoring Pipeline Health
  10. Interview Q&A — 6 realistic senior-level pairs
  11. Quick Reference — 12–15 rows
- Per section: 2–3 tight paragraphs; include a code block where it adds value (20 lines max)
- No step-by-step tutorials, no full worked examples
- Cheat sheet rows must each earn their place — no padding

Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\cicd-data-engineering.html
