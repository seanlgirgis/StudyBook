# build_rag_shell.ps1
# Creates the ServiceCall AI / RAG learning project shell under:
# D:\Workarea\StudyBook\demos\rag
#
# Usage:
#   cd D:\Workarea\StudyBook\demos\rag
#   .\build_rag_shell.ps1
#
# Safe to re-run. It does not overwrite existing files with content.

$ErrorActionPreference = "Stop"

$Root = "D:\Workarea\StudyBook\demos\rag"

Write-Host "Creating RAG demo shell at: $Root" -ForegroundColor Cyan

# -------------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------------

function Ensure-Directory {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    if (-not (Test-Path $Path)) {
        New-Item -ItemType Directory -Path $Path | Out-Null
        Write-Host "Created directory: $Path" -ForegroundColor Green
    }
}

function Ensure-TextFile {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,

        [string]$Content = ""
    )

    $Parent = Split-Path $Path -Parent
    Ensure-Directory $Parent

    if (-not (Test-Path $Path)) {
        New-Item -ItemType File -Path $Path | Out-Null

        if ($Content -ne "") {
            Set-Content -Path $Path -Value $Content -Encoding UTF8
        }

        Write-Host "Created file: $Path" -ForegroundColor Yellow
    }
}

function Ensure-KeepFile {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Directory
    )

    Ensure-Directory $Directory
    $KeepPath = Join-Path $Directory "keepIt.keep"

    if (-not (Test-Path $KeepPath)) {
        New-Item -ItemType File -Path $KeepPath | Out-Null
        Write-Host "Created keep file: $KeepPath" -ForegroundColor DarkYellow
    }
}

# -------------------------------------------------------------------
# Root files
# -------------------------------------------------------------------

Ensure-Directory $Root

Ensure-TextFile "$Root\README.md" @"
# RAG Demo Workspace

This workspace contains a two-phase learning project for building RAG and AI intake assistant demos.

## Structure

- `pocs/` contains small proof-of-concepts used for learning and control.
- `integrated/` contains the assembled ServiceCall AI solution.
- `shared/` contains reusable prompts, schemas, diagrams, and sample questions.
- `docs/` contains manuals, architecture documents, runbooks, and learning notes.
- `archive/` stores old or broken experiments instead of deleting them.

## Main Rule

Nothing moves into `integrated/servicecall-ai/` until it has been understood in `pocs/`.
"@

Ensure-TextFile "$Root\00_RAG_DEMO_MASTER_PLAN.md" @"
# RAG Demo Master Plan

## Project

ServiceCall AI

## Goal

Build a learning-first RAG and AI intake assistant for home-service businesses.

The project should teach:

- RAG
- Pydantic schemas
- FastAPI
- website chat widget embedding
- intake classification
- guardrails
- escalation
- outcome logging
- Docker
- AWS ECS Fargate
- GitHub Actions CI/CD
- CloudWatch observability
- AWS cleanup

## Two-Phase Strategy

1. Build small proof-of-concepts in `pocs/`.
2. Assemble stable and understood pieces into `integrated/servicecall-ai/`.
"@

Ensure-TextFile "$Root\ENGINEERING_RULES.md" @"
# ServiceCall AI Engineering Rules

## Non-Negotiables

1. Use Pydantic models for all structured inputs, outputs, configs, logs, and AI responses.
2. Use type hints for all public functions.
3. No hardcoded secrets.
4. Every POC must have a README with commands and expected output.
5. Every POC must have at least one test or smoke check.
6. Every answer must include citations or use a fallback.
7. Every risky customer request must produce an escalation decision.
8. Every chat request must produce an outcome event.
9. Every AWS resource must have a cleanup path.
10. Nothing moves to `integrated/servicecall-ai/` until it is understood in `pocs/`.

## Main Principle

Schemas first. Implementation second.
"@

Ensure-TextFile "$Root\01_LEARNING_NOTES.md" "# Learning Notes`n`nUse this file to capture lessons learned while building the RAG demo.`n"
Ensure-TextFile "$Root\02_COMMANDS.md" "# Commands`n`nUse this file to collect repeatable PowerShell, Python, Docker, AWS, and Git commands.`n"
Ensure-TextFile "$Root\03_DECISIONS.md" "# Decisions`n`nUse this file to record architectural and product decisions.`n"

# -------------------------------------------------------------------
# Top-level directories
# -------------------------------------------------------------------

$TopDirs = @(
    "pocs",
    "integrated",
    "integrated\servicecall-ai",
    "shared",
    "archive",
    "docs"
)

foreach ($Dir in $TopDirs) {
    Ensure-KeepFile "$Root\$Dir"
}

Ensure-TextFile "$Root\pocs\README.md" @"
# POCs

This folder contains small proof-of-concepts.

Each POC should teach one thing clearly.

## Rule

Do not build giant apps here.

Each POC should include:

- README
- source code
- commands
- expected output
- common failures
- tests or smoke checks
- explanation of how it maps to the integrated solution
"@

Ensure-TextFile "$Root\integrated\README.md" @"
# Integrated Solutions

This folder contains assembled demo solutions.

Stable pieces from `pocs/` are integrated here after they are understood.
"@

Ensure-TextFile "$Root\integrated\servicecall-ai\README.md" @"
# ServiceCall AI

ServiceCall AI is a learning-first RAG and AI intake assistant for home-service businesses.

It will eventually include:

- synthetic website
- embedded chat widget
- FastAPI backend
- RAG retrieval
- citations
- intake classification
- guardrails
- escalation
- outcome logging
- Docker
- ECS Fargate deployment
- GitHub Actions CI/CD
- CloudWatch observability
"@

Ensure-TextFile "$Root\shared\README.md" @"
# Shared Assets

Reusable prompts, schemas, sample questions, and diagrams live here.
"@

Ensure-TextFile "$Root\archive\README.md" @"
# Archive

Use this folder for old experiments, failed attempts, and retired files.
"@

# -------------------------------------------------------------------
# POC structure
# -------------------------------------------------------------------

$PocDirs = @(
    "01_static_site_shell\website\assets",
    "01_static_site_shell\notes",

    "02_fake_business_docs\data\home_services_demo",
    "02_fake_business_docs\notes",

    "03_basic_retrieval\src",
    "03_basic_retrieval\data",
    "03_basic_retrieval\outputs",
    "03_basic_retrieval\notes",

    "04_answer_with_citations\src",
    "04_answer_with_citations\outputs",
    "04_answer_with_citations\tests",

    "05_intake_classifier\src",
    "05_intake_classifier\sample_inputs",
    "05_intake_classifier\outputs",
    "05_intake_classifier\tests",

    "06_guardrails_escalation\src",
    "06_guardrails_escalation\outputs",
    "06_guardrails_escalation\tests",

    "07_outcome_logging\src",
    "07_outcome_logging\outputs",
    "07_outcome_logging\tests",

    "08_fastapi_chat_api\app",
    "08_fastapi_chat_api\tests",
    "08_fastapi_chat_api\notes",

    "09_docker_fastapi\app",
    "09_docker_fastapi\notes",

    "10_aws_ecr_ecs_manual\deploy",
    "10_aws_ecr_ecs_manual\notes",

    "11_github_actions_cicd\.github\workflows",
    "11_github_actions_cicd\notes",

    "12_observability_cloudwatch\src",
    "12_observability_cloudwatch\deploy",
    "12_observability_cloudwatch\notes"
)

foreach ($Dir in $PocDirs) {
    Ensure-KeepFile "$Root\pocs\$Dir"
}

# POC README files
$PocNames = @(
    "01_static_site_shell",
    "02_fake_business_docs",
    "03_basic_retrieval",
    "04_answer_with_citations",
    "05_intake_classifier",
    "06_guardrails_escalation",
    "07_outcome_logging",
    "08_fastapi_chat_api",
    "09_docker_fastapi",
    "10_aws_ecr_ecs_manual",
    "11_github_actions_cicd",
    "12_observability_cloudwatch"
)

foreach ($Poc in $PocNames) {
    Ensure-TextFile "$Root\pocs\$Poc\README.md" @"
# $Poc

## Purpose

Describe what this POC teaches.

## Commands

Add commands here.

## Expected Output

Add expected output here.

## Common Failures

Add troubleshooting notes here.

## How This Maps to Integrated Solution

Explain how this POC later moves into `integrated/servicecall-ai`.
"@
}

# POC starter files
Ensure-TextFile "$Root\pocs\01_static_site_shell\website\index.html"
Ensure-TextFile "$Root\pocs\01_static_site_shell\website\assets\styles.css"
Ensure-TextFile "$Root\pocs\01_static_site_shell\website\assets\chat-widget.js"
Ensure-TextFile "$Root\pocs\01_static_site_shell\notes\what_this_teaches.md"
Ensure-TextFile "$Root\pocs\01_static_site_shell\notes\questions.md"

Ensure-TextFile "$Root\pocs\02_fake_business_docs\notes\retrieval_questions.md"
Ensure-TextFile "$Root\pocs\02_fake_business_docs\notes\what_good_answers_should_include.md"

$BusinessDocs = @(
    "company_profile.md",
    "service_area.md",
    "business_hours.md",
    "hvac_repair_policy.md",
    "ac_replacement_estimates.md",
    "plumbing_services.md",
    "water_heater_policy.md",
    "appliance_repair_policy.md",
    "maintenance_plan.md",
    "coupon_policy.md",
    "scheduling_policy.md",
    "financing_policy.md",
    "warranty_policy.md",
    "escalation_rules.md",
    "intake_script.md",
    "faq.md"
)

foreach ($Doc in $BusinessDocs) {
    Ensure-TextFile "$Root\pocs\02_fake_business_docs\data\home_services_demo\$Doc"
}

Ensure-TextFile "$Root\pocs\03_basic_retrieval\requirements.txt"
Ensure-TextFile "$Root\pocs\03_basic_retrieval\src\load_docs.py"
Ensure-TextFile "$Root\pocs\03_basic_retrieval\src\chunk_docs.py"
Ensure-TextFile "$Root\pocs\03_basic_retrieval\src\search_docs.py"
Ensure-TextFile "$Root\pocs\03_basic_retrieval\outputs\retrieval_results.json"
Ensure-TextFile "$Root\pocs\03_basic_retrieval\notes\what_this_teaches.md"
Ensure-TextFile "$Root\pocs\03_basic_retrieval\notes\common_failures.md"

Ensure-TextFile "$Root\pocs\04_answer_with_citations\requirements.txt"
Ensure-TextFile "$Root\pocs\04_answer_with_citations\src\answer.py"
Ensure-TextFile "$Root\pocs\04_answer_with_citations\src\citations.py"
Ensure-TextFile "$Root\pocs\04_answer_with_citations\src\prompt_template.md"
Ensure-TextFile "$Root\pocs\04_answer_with_citations\outputs\sample_answers.md"
Ensure-TextFile "$Root\pocs\04_answer_with_citations\tests\test_citations.py"

Ensure-TextFile "$Root\pocs\05_intake_classifier\requirements.txt"
Ensure-TextFile "$Root\pocs\05_intake_classifier\src\classify_intake.py"
Ensure-TextFile "$Root\pocs\05_intake_classifier\src\schemas.py"
Ensure-TextFile "$Root\pocs\05_intake_classifier\sample_inputs\ac_not_cooling.txt"
Ensure-TextFile "$Root\pocs\05_intake_classifier\sample_inputs\replacement_estimate.txt"
Ensure-TextFile "$Root\pocs\05_intake_classifier\sample_inputs\waive_fee_request.txt"
Ensure-TextFile "$Root\pocs\05_intake_classifier\outputs\intake_results.jsonl"
Ensure-TextFile "$Root\pocs\05_intake_classifier\tests\test_intake_classifier.py"

Ensure-TextFile "$Root\pocs\06_guardrails_escalation\requirements.txt"
Ensure-TextFile "$Root\pocs\06_guardrails_escalation\src\guardrails.py"
Ensure-TextFile "$Root\pocs\06_guardrails_escalation\src\escalation.py"
Ensure-TextFile "$Root\pocs\06_guardrails_escalation\src\escalation_rules.json"
Ensure-TextFile "$Root\pocs\06_guardrails_escalation\outputs\escalation_queue.jsonl"
Ensure-TextFile "$Root\pocs\06_guardrails_escalation\tests\test_guardrails.py"
Ensure-TextFile "$Root\pocs\06_guardrails_escalation\tests\test_escalation.py"

Ensure-TextFile "$Root\pocs\07_outcome_logging\requirements.txt"
Ensure-TextFile "$Root\pocs\07_outcome_logging\src\outcome_logger.py"
Ensure-TextFile "$Root\pocs\07_outcome_logging\src\outcome_report.py"
Ensure-TextFile "$Root\pocs\07_outcome_logging\outputs\interactions.jsonl"
Ensure-TextFile "$Root\pocs\07_outcome_logging\outputs\outcome_report.md"
Ensure-TextFile "$Root\pocs\07_outcome_logging\tests\test_outcome_logger.py"

Ensure-TextFile "$Root\pocs\08_fastapi_chat_api\requirements.txt"
Ensure-TextFile "$Root\pocs\08_fastapi_chat_api\app\main.py"
Ensure-TextFile "$Root\pocs\08_fastapi_chat_api\app\schemas.py"
Ensure-TextFile "$Root\pocs\08_fastapi_chat_api\app\service.py"
Ensure-TextFile "$Root\pocs\08_fastapi_chat_api\tests\test_api.py"
Ensure-TextFile "$Root\pocs\08_fastapi_chat_api\notes\endpoints.md"
Ensure-TextFile "$Root\pocs\08_fastapi_chat_api\notes\api_test_commands.md"

Ensure-TextFile "$Root\pocs\09_docker_fastapi\Dockerfile"
Ensure-TextFile "$Root\pocs\09_docker_fastapi\.dockerignore"
Ensure-TextFile "$Root\pocs\09_docker_fastapi\docker-compose.yml"
Ensure-TextFile "$Root\pocs\09_docker_fastapi\notes\docker_commands.md"
Ensure-TextFile "$Root\pocs\09_docker_fastapi\notes\troubleshooting.md"

Ensure-TextFile "$Root\pocs\10_aws_ecr_ecs_manual\deploy\task-definition.json"
Ensure-TextFile "$Root\pocs\10_aws_ecr_ecs_manual\deploy\ecs-service-notes.md"
Ensure-TextFile "$Root\pocs\10_aws_ecr_ecs_manual\deploy\cleanup.ps1"
Ensure-TextFile "$Root\pocs\10_aws_ecr_ecs_manual\notes\ecr_commands.md"
Ensure-TextFile "$Root\pocs\10_aws_ecr_ecs_manual\notes\ecs_commands.md"
Ensure-TextFile "$Root\pocs\10_aws_ecr_ecs_manual\notes\iam_notes.md"
Ensure-TextFile "$Root\pocs\10_aws_ecr_ecs_manual\notes\cost_controls.md"

Ensure-TextFile "$Root\pocs\11_github_actions_cicd\.github\workflows\deploy-ecs.yml"
Ensure-TextFile "$Root\pocs\11_github_actions_cicd\notes\cicd_flow.md"
Ensure-TextFile "$Root\pocs\11_github_actions_cicd\notes\required_secrets.md"
Ensure-TextFile "$Root\pocs\11_github_actions_cicd\notes\rollback.md"

Ensure-TextFile "$Root\pocs\12_observability_cloudwatch\src\structured_logging.py"
Ensure-TextFile "$Root\pocs\12_observability_cloudwatch\src\metrics_examples.py"
Ensure-TextFile "$Root\pocs\12_observability_cloudwatch\deploy\cloudwatch_alarms.md"
Ensure-TextFile "$Root\pocs\12_observability_cloudwatch\notes\what_to_monitor.md"
Ensure-TextFile "$Root\pocs\12_observability_cloudwatch\notes\failure_modes.md"

# -------------------------------------------------------------------
# Integrated solution structure
# -------------------------------------------------------------------

$IntegratedDirs = @(
    "website\assets",

    "backend\app\rag",
    "backend\app\intake",
    "backend\app\safety",
    "backend\app\outcomes",
    "backend\app\observability",

    "data\home_services_demo",

    "tests",
    "outputs",
    "docker",
    "deploy\aws",
    "deploy\cloudflare",
    ".github\workflows"
)

foreach ($Dir in $IntegratedDirs) {
    Ensure-KeepFile "$Root\integrated\servicecall-ai\$Dir"
}

$IntegratedFiles = @(
    "00_ARCHITECTURE.md",
    "01_DEMO_SCRIPT.md",
    "02_RUNBOOK.md",
    "03_INTERVIEW_QA.md",
    "04_CLEANUP.md",

    "website\index.html",
    "website\assets\styles.css",
    "website\assets\chat-widget.js",

    "backend\requirements.txt",
    "backend\app\main.py",
    "backend\app\config.py",
    "backend\app\schemas.py",

    "backend\app\rag\ingest.py",
    "backend\app\rag\chunking.py",
    "backend\app\rag\retriever.py",
    "backend\app\rag\answerer.py",

    "backend\app\intake\classifier.py",
    "backend\app\intake\lead_scoring.py",

    "backend\app\safety\guardrails.py",
    "backend\app\safety\escalation.py",

    "backend\app\outcomes\logger.py",
    "backend\app\outcomes\reports.py",

    "backend\app\observability\logging_config.py",
    "backend\app\observability\metrics.py",

    "tests\test_api.py",
    "tests\test_retrieval.py",
    "tests\test_citations.py",
    "tests\test_intake.py",
    "tests\test_guardrails.py",
    "tests\test_outcomes.py",

    "outputs\interactions.jsonl",
    "outputs\escalation_queue.jsonl",
    "outputs\outcome_report.md",

    "docker\Dockerfile",
    "docker\.dockerignore",
    "docker\docker-compose.yml",

    "deploy\aws\README_ECS_FARGATE.md",
    "deploy\aws\task-definition.json",
    "deploy\aws\service-definition.json",
    "deploy\aws\github-actions-notes.md",
    "deploy\aws\cleanup.ps1",

    "deploy\cloudflare\README_CLOUDFLARE_PAGES.md",
    "deploy\cloudflare\pages-notes.md",

    ".github\workflows\ci.yml",
    ".github\workflows\deploy-ecs.yml"
)

foreach ($File in $IntegratedFiles) {
    Ensure-TextFile "$Root\integrated\servicecall-ai\$File"
}

foreach ($Doc in $BusinessDocs) {
    Ensure-TextFile "$Root\integrated\servicecall-ai\data\home_services_demo\$Doc"
}

# -------------------------------------------------------------------
# Shared assets
# -------------------------------------------------------------------

$SharedDirs = @(
    "prompts",
    "schemas",
    "sample_questions",
    "diagrams"
)

foreach ($Dir in $SharedDirs) {
    Ensure-KeepFile "$Root\shared\$Dir"
}

$SharedFiles = @(
    "prompts\rag_answer_prompt.md",
    "prompts\intake_classifier_prompt.md",
    "prompts\escalation_prompt.md",

    "schemas\chat_request.schema.json",
    "schemas\chat_response.schema.json",
    "schemas\intake_summary.schema.json",
    "schemas\outcome_event.schema.json",

    "sample_questions\hvac_questions.md",
    "sample_questions\plumbing_questions.md",
    "sample_questions\appliance_questions.md",
    "sample_questions\tricky_questions.md",

    "diagrams\local_architecture.mmd",
    "diagrams\aws_ecs_architecture.mmd",
    "diagrams\cicd_flow.mmd"
)

foreach ($File in $SharedFiles) {
    Ensure-TextFile "$Root\shared\$File"
}

# -------------------------------------------------------------------
# Documentation layer
# -------------------------------------------------------------------

$DocDirs = @(
    "product",
    "architecture",
    "manuals",
    "learning",
    "runbooks",
    "diagrams"
)

foreach ($Dir in $DocDirs) {
    Ensure-KeepFile "$Root\docs\$Dir"
}

Ensure-TextFile "$Root\docs\README.md" @"
# Documentation

This folder contains the manuals, architecture documents, learning notes, runbooks, and diagrams for ServiceCall AI.
"@

$DocFiles = @(
    "product\PRODUCT_VISION.md",
    "product\DEMO_SCRIPT.md",
    "product\BUSINESS_USE_CASES.md",
    "product\SUCCESS_METRICS.md",

    "architecture\ARCHITECTURE_OVERVIEW.md",
    "architecture\DATA_FLOW.md",
    "architecture\LOCAL_ARCHITECTURE.md",
    "architecture\AWS_ECS_FARGATE_ARCHITECTURE.md",
    "architecture\CICD_ARCHITECTURE.md",
    "architecture\OBSERVABILITY_ARCHITECTURE.md",
    "architecture\SECURITY_ARCHITECTURE.md",

    "manuals\DEVELOPER_MANUAL.md",
    "manuals\DEPLOYMENT_MANUAL.md",
    "manuals\TROUBLESHOOTING_MANUAL.md",
    "manuals\AWS_CLEANUP_MANUAL.md",
    "manuals\DEMO_PRESENTER_MANUAL.md",

    "learning\RAG_CONCEPTS.md",
    "learning\PYDANTIC_CONTRACTS.md",
    "learning\FASTAPI_CONCEPTS.md",
    "learning\DOCKER_CONCEPTS.md",
    "learning\ECS_FARGATE_CONCEPTS.md",
    "learning\GITHUB_ACTIONS_CICD.md",
    "learning\CLOUDWATCH_CONCEPTS.md",
    "learning\INTERVIEW_QA.md",

    "runbooks\LOCAL_RUNBOOK.md",
    "runbooks\DOCKER_RUNBOOK.md",
    "runbooks\ECS_DEPLOYMENT_RUNBOOK.md",
    "runbooks\CICD_RUNBOOK.md",
    "runbooks\INCIDENT_RUNBOOK.md",
    "runbooks\ROLLBACK_RUNBOOK.md",

    "diagrams\local-rag-flow.mmd",
    "diagrams\website-chat-widget-flow.mmd",
    "diagrams\fastapi-backend-flow.mmd",
    "diagrams\aws-ecs-fargate-flow.mmd",
    "diagrams\cicd-flow.mmd",
    "diagrams\observability-flow.mmd"
)

foreach ($File in $DocFiles) {
    Ensure-TextFile "$Root\docs\$File" @"
# $File

## Purpose

Starter documentation file for ServiceCall AI.

## Notes

Fill this in as the project grows.
"@
}

Write-Host ""
Write-Host "ServiceCall AI shell created successfully." -ForegroundColor Cyan
Write-Host "Root: $Root" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next commands:" -ForegroundColor White
Write-Host "  cd $Root" -ForegroundColor Gray
Write-Host "  tree /F" -ForegroundColor Gray
Write-Host "  git status" -ForegroundColor Gray