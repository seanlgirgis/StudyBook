# build_curriculum_skeleton.ps1
# DE Curriculum Workspace Skeleton Builder
# Run from: PS D:\Workspace> .\scripts\build_curriculum_skeleton.ps1
# Never uses absolute paths — all paths relative to $PSScriptRoot\..\

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Force UTF-8 output — prevents em-dash and Unicode mangling on Windows console
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# ── ROOT is one level up from scripts/ ──────────────────────────────
$root = Split-Path $PSScriptRoot -Parent

function New-Folder {
    param([string]$rel)
    $full = Join-Path $root $rel
    if (-not (Test-Path $full)) {
        New-Item -ItemType Directory -Path $full | Out-Null
        Write-Host "  [+] $rel" -ForegroundColor Green
    } else {
        Write-Host "  [=] $rel (exists)" -ForegroundColor DarkGray
    }
}

function New-Readme {
    param([string]$rel, [string]$title, [string]$description, [string]$tier, [string[]]$notebooks)
    $full = Join-Path $root "$rel\README.md"
    if (Test-Path $full) {
        Write-Host "  [=] $rel\README.md (exists)" -ForegroundColor DarkGray
        return
    }
    $nbList = ($notebooks | ForEach-Object { "| $_ | ⬜ Not Started | |" }) -join "`n"
    $fence = '```'
    $content = @"
# $title

> $description

**Tier:** $tier  
**Mantra:** Simplicity and clarity is Gold.

---

## Notebooks

| File | Status | Notes |
|------|--------|-------|
$nbList

---

## How to generate a notebook

$fence
Read prompts/agent_rules.md and prompts/notebook_master_prompt.md — then read supplement_prompts/<file>.md and generate the notebook.
$fence

---

*Part of Sean's Staff/Principal DE Master Curriculum*
"@
    Set-Content -Path $full -Value $content -Encoding UTF8
    Write-Host "  [+] $rel\README.md" -ForegroundColor Cyan
}

function New-NotebookPlaceholder {
    param([string]$rel, [string]$topic, [string]$tier)
    $full = Join-Path $root $rel
    if (Test-Path $full) {
        Write-Host "  [=] $rel (exists)" -ForegroundColor DarkGray
        return
    }
    $safeTopic = $topic -replace '"', "'"
    $json = @"
{
 "nbformat": 4,
 "nbformat_minor": 5,
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.12.9"
  }
 },
 "cells": [
  {
   "cell_type": "markdown",
   "id": "cell-placeholder-title",
   "metadata": {},
   "source": [
    "# $safeTopic\n",
    "### *Placeholder — awaiting generation*\n",
    "\n",
    "**Tier:** $tier  \n",
    "**Status:** ⬜ Not Started  \n",
    "\n",
    "> Run the supplement prompt for this topic to generate the full master guide.\n",
    "\n",
    "---\n",
    "*Simplicity and clarity is Gold.*"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "cell-placeholder-code",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Placeholder — notebook not yet generated\n",
    "print('$safeTopic — pending generation')"
   ]
  }
 ]
}
"@
    Set-Content -Path $full -Value $json -Encoding UTF8
    Write-Host "  [+] $rel" -ForegroundColor Yellow
}

# ════════════════════════════════════════════════════════════════════
Write-Host ""
Write-Host "══════════════════════════════════════════" -ForegroundColor Magenta
Write-Host "  DE Curriculum Skeleton Builder" -ForegroundColor Magenta
Write-Host "  Root: $root" -ForegroundColor Magenta
Write-Host "══════════════════════════════════════════" -ForegroundColor Magenta
Write-Host ""

# ── 1. scripts/ folder (this script lives here) ─────────────────────
Write-Host "[1] scripts/" -ForegroundColor White
New-Folder "scripts"

# ── 2. supplement_prompts/ (already exists from Tiers 1-2 work) ─────
Write-Host "[2] supplement_prompts/" -ForegroundColor White
New-Folder "supplement_prompts"

# ── NOTE: Basics/ already exists at workspace root ──────────────────
# It is the root of all existing knowledge notebooks (Tiers 1-8).
# No changes made to Basics/ — new domains are siblings, not children.
Write-Host "[3] Basics\ — existing root, skipping" -ForegroundColor DarkGray

# ── 4. Basics\Databases\ ────────────────────────────────────────────
Write-Host "[4] Basics\Databases\" -ForegroundColor White
New-Folder "Basics\Databases"
New-Folder "Basics\Databases\supplement_prompts"
New-Readme `
    -rel "Basics\Databases" `
    -title "Databases — SQL, NoSQL, and Beyond" `
    -description "Full database landscape: SQL internals, transactions, indexing, NoSQL patterns, graph, time-series, vector, and query engines." `
    -tier "Tier A" `
    -notebooks @(
        "sql_advanced_postgres.ipynb",
        "sql_transactions_isolation.ipynb",
        "sql_indexing_deep_dive.ipynb",
        "nosql_mongo_dynamodb.ipynb",
        "nosql_cassandra_wide_column.ipynb",
        "nosql_redis_patterns.ipynb",
        "graph_db_neo4j_cypher.ipynb",
        "timeseries_influx_timescale.ipynb",
        "vector_db_pgvector_pinecone.ipynb",
        "newsql_cockroach_spanner.ipynb",
        "query_engines_duckdb_trino.ipynb",
        "db_decision_framework.ipynb"
    )

$sqlNotebooks = @{
    "Basics\Databases\sql_advanced_postgres.ipynb"       = "SQL Advanced — PostgreSQL Internals"
    "Basics\Databases\sql_transactions_isolation.ipynb"  = "SQL Transactions — ACID and Isolation Levels"
    "Basics\Databases\sql_indexing_deep_dive.ipynb"      = "SQL Indexing — B-Tree, Hash, GIN, Partial"
    "Basics\Databases\nosql_mongo_dynamodb.ipynb"        = "NoSQL — MongoDB and DynamoDB"
    "Basics\Databases\nosql_cassandra_wide_column.ipynb" = "NoSQL — Cassandra and Wide Column"
    "Basics\Databases\nosql_redis_patterns.ipynb"        = "NoSQL — Redis Patterns for DE"
    "Basics\Databases\graph_db_neo4j_cypher.ipynb"       = "Graph DB — Neo4j and Cypher"
    "Basics\Databases\timeseries_influx_timescale.ipynb" = "Time-Series — InfluxDB and TimescaleDB"
    "Basics\Databases\vector_db_pgvector_pinecone.ipynb" = "Vector DB — pgvector and Pinecone"
    "Basics\Databases\newsql_cockroach_spanner.ipynb"    = "NewSQL — CockroachDB and Spanner"
    "Basics\Databases\query_engines_duckdb_trino.ipynb"  = "Query Engines — DuckDB, Trino, Presto"
    "Basics\Databases\db_decision_framework.ipynb"       = "Database Decision Framework — When to Use What"
}
foreach ($nb in $sqlNotebooks.GetEnumerator()) {
    New-NotebookPlaceholder -rel $nb.Key -topic $nb.Value -tier "Tier A"
}

# ── 5. Basics\Python_Data\ ───────────────────────────────────────────
Write-Host "[5] Basics\Python_Data\" -ForegroundColor White
New-Folder "Basics\Python_Data"
New-Folder "Basics\Python_Data\supplement_prompts"
New-Readme `
    -rel "Basics\Python_Data" `
    -title "Python Data — Analytics and Visualization" `
    -description "Pandas, NumPy, PySpark, Polars, plotting libraries, and statistical analysis. Daily DE tools." `
    -tier "Tier B" `
    -notebooks @(
        "pandas_advanced.ipynb",
        "numpy_broadcast_vectorize.ipynb",
        "pyspark_dataframes.ipynb",
        "polars_guide.ipynb",
        "matplotlib_seaborn.ipynb",
        "plotly_dash_interactive.ipynb",
        "scipy_statsmodels.ipynb"
    )

$pyNotebooks = @{
    "Basics\Python_Data\pandas_advanced.ipynb"           = "Pandas Advanced — Performance and Patterns"
    "Basics\Python_Data\numpy_broadcast_vectorize.ipynb" = "NumPy — Broadcasting and Vectorization"
    "Basics\Python_Data\pyspark_dataframes.ipynb"        = "PySpark DataFrames — DE Patterns"
    "Basics\Python_Data\polars_guide.ipynb"              = "Polars — Modern Pandas Alternative"
    "Basics\Python_Data\matplotlib_seaborn.ipynb"        = "Matplotlib and Seaborn — Static Viz"
    "Basics\Python_Data\plotly_dash_interactive.ipynb"   = "Plotly and Dash — Interactive Viz"
    "Basics\Python_Data\scipy_statsmodels.ipynb"         = "SciPy and Statsmodels — Statistical Analysis"
}
foreach ($nb in $pyNotebooks.GetEnumerator()) {
    New-NotebookPlaceholder -rel $nb.Key -topic $nb.Value -tier "Tier B"
}

# ── 6. Technologies/ ────────────────────────────────────────────────
Write-Host "[6] Technologies\" -ForegroundColor White
New-Folder "Technologies"
New-Folder "Technologies\supplement_prompts"
New-Readme `
    -rel "Technologies" `
    -title "DE Technologies Stack" `
    -description "Apache Spark, Kafka, dbt, AWS deep-dive, Databricks, Snowflake, Docker/K8s, Terraform." `
    -tier "Tier C" `
    -notebooks @(
        "spark_internals_tuning.ipynb",
        "kafka_patterns_internals.ipynb",
        "dbt_models_tests_lineage.ipynb",
        "aws_glue_emr_athena_lakeformation.ipynb",
        "databricks_delta_lake.ipynb",
        "snowflake_architecture.ipynb",
        "docker_k8s_for_de.ipynb",
        "terraform_iac_basics.ipynb"
    )

$techNotebooks = @{
    "Technologies\spark_internals_tuning.ipynb"          = "Apache Spark — Internals and Tuning"
    "Technologies\kafka_patterns_internals.ipynb"         = "Apache Kafka — Patterns and Internals"
    "Technologies\dbt_models_tests_lineage.ipynb"         = "dbt — Models, Tests, and Lineage"
    "Technologies\aws_glue_emr_athena_lakeformation.ipynb"= "AWS Deep — Glue, EMR, Athena, Lake Formation"
    "Technologies\databricks_delta_lake.ipynb"            = "Databricks and Delta Lake"
    "Technologies\snowflake_architecture.ipynb"           = "Snowflake Architecture and Patterns"
    "Technologies\docker_k8s_for_de.ipynb"                = "Docker and Kubernetes for Data Engineers"
    "Technologies\terraform_iac_basics.ipynb"             = "Terraform and IaC for DE"
}
foreach ($nb in $techNotebooks.GetEnumerator()) {
    New-NotebookPlaceholder -rel $nb.Key -topic $nb.Value -tier "Tier C"
}

# ── 7. ML_AI/ with three sub-tracks ─────────────────────────────────
Write-Host "[7] ML_AI\ (3 sub-tracks)" -ForegroundColor White
New-Folder "ML_AI"
New-Folder "ML_AI\Classical"
New-Folder "ML_AI\DeepLearning"
New-Folder "ML_AI\GenAI_MLOps"
New-Folder "ML_AI\supplement_prompts"

New-Readme `
    -rel "ML_AI" `
    -title "AI / ML for Data Engineers" `
    -description "Three sub-tracks: Classical ML, Deep Learning, and GenAI/MLOps. Staff DE depth — not research, production." `
    -tier "Tier D" `
    -notebooks @("Classical/", "DeepLearning/", "GenAI_MLOps/")

New-Readme `
    -rel "ML_AI\Classical" `
    -title "Classical ML" `
    -description "Regression, trees, ensembles, clustering, dimensionality reduction, sklearn pipeline API." `
    -tier "Tier D1" `
    -notebooks @(
        "linear_logistic_regression.ipynb",
        "tree_ensemble_xgboost.ipynb",
        "clustering_kmeans_dbscan.ipynb",
        "dimensionality_pca_umap.ipynb",
        "evaluation_metrics_auc.ipynb",
        "feature_engineering_patterns.ipynb",
        "sklearn_pipeline_api.ipynb"
    )

$classicalNotebooks = @{
    "ML_AI\Classical\linear_logistic_regression.ipynb" = "Linear and Logistic Regression"
    "ML_AI\Classical\tree_ensemble_xgboost.ipynb"      = "Decision Trees, Random Forest, XGBoost"
    "ML_AI\Classical\clustering_kmeans_dbscan.ipynb"   = "Clustering — K-Means and DBSCAN"
    "ML_AI\Classical\dimensionality_pca_umap.ipynb"    = "Dimensionality Reduction — PCA and UMAP"
    "ML_AI\Classical\evaluation_metrics_auc.ipynb"     = "Evaluation Metrics — AUC, Precision, Recall"
    "ML_AI\Classical\feature_engineering_patterns.ipynb"= "Feature Engineering Patterns"
    "ML_AI\Classical\sklearn_pipeline_api.ipynb"       = "scikit-learn Pipeline API"
}
foreach ($nb in $classicalNotebooks.GetEnumerator()) {
    New-NotebookPlaceholder -rel $nb.Key -topic $nb.Value -tier "Tier D1"
}

New-Readme `
    -rel "ML_AI\DeepLearning" `
    -title "Deep Learning" `
    -description "Neural nets, CNNs, RNNs, Transformers, embeddings, PyTorch basics, transfer learning." `
    -tier "Tier D2" `
    -notebooks @(
        "neural_net_fundamentals.ipynb",
        "cnns_image_tabular.ipynb",
        "rnns_lstms_sequence.ipynb",
        "transformers_attention_bert.ipynb",
        "embeddings_dense_vectors.ipynb",
        "pytorch_basics.ipynb",
        "transfer_learning_finetuning.ipynb"
    )

$dlNotebooks = @{
    "ML_AI\DeepLearning\neural_net_fundamentals.ipynb"    = "Neural Network Fundamentals"
    "ML_AI\DeepLearning\cnns_image_tabular.ipynb"         = "CNNs — Image and Tabular"
    "ML_AI\DeepLearning\rnns_lstms_sequence.ipynb"        = "RNNs and LSTMs — Sequence Modeling"
    "ML_AI\DeepLearning\transformers_attention_bert.ipynb" = "Transformers and Attention — BERT"
    "ML_AI\DeepLearning\embeddings_dense_vectors.ipynb"   = "Embeddings and Dense Vectors"
    "ML_AI\DeepLearning\pytorch_basics.ipynb"             = "PyTorch Basics for DE"
    "ML_AI\DeepLearning\transfer_learning_finetuning.ipynb"= "Transfer Learning and Fine-Tuning"
}
foreach ($nb in $dlNotebooks.GetEnumerator()) {
    New-NotebookPlaceholder -rel $nb.Key -topic $nb.Value -tier "Tier D2"
}

New-Readme `
    -rel "ML_AI\GenAI_MLOps" `
    -title "GenAI + MLOps" `
    -description "LLM internals, RAG pipelines, prompt engineering, LoRA fine-tuning, MLflow, feature stores, model serving." `
    -tier "Tier D3" `
    -notebooks @(
        "llm_internals_tokens_context.ipynb",
        "rag_pipeline_design.ipynb",
        "prompt_engineering_patterns.ipynb",
        "finetuning_lora_peft.ipynb",
        "mlflow_experiment_tracking.ipynb",
        "feature_stores_feast_tecton.ipynb",
        "model_serving_ray_bentoml.ipynb",
        "evaluation_ragas_benchmarks.ipynb"
    )

$genaiNotebooks = @{
    "ML_AI\GenAI_MLOps\llm_internals_tokens_context.ipynb" = "LLM Internals — Tokens and Context"
    "ML_AI\GenAI_MLOps\rag_pipeline_design.ipynb"           = "RAG Pipeline Design"
    "ML_AI\GenAI_MLOps\prompt_engineering_patterns.ipynb"   = "Prompt Engineering Patterns"
    "ML_AI\GenAI_MLOps\finetuning_lora_peft.ipynb"          = "Fine-Tuning — LoRA and PEFT"
    "ML_AI\GenAI_MLOps\mlflow_experiment_tracking.ipynb"    = "MLflow — Experiment Tracking"
    "ML_AI\GenAI_MLOps\feature_stores_feast_tecton.ipynb"   = "Feature Stores — Feast and Tecton"
    "ML_AI\GenAI_MLOps\model_serving_ray_bentoml.ipynb"     = "Model Serving — Ray and BentoML"
    "ML_AI\GenAI_MLOps\evaluation_ragas_benchmarks.ipynb"   = "Evaluation — RAGAS and Benchmarks"
}
foreach ($nb in $genaiNotebooks.GetEnumerator()) {
    New-NotebookPlaceholder -rel $nb.Key -topic $nb.Value -tier "Tier D3"
}

# ── 8. Governance/ ──────────────────────────────────────────────────
Write-Host "[8] Governance\" -ForegroundColor White
New-Folder "Governance"
New-Folder "Governance\supplement_prompts"
New-Readme `
    -rel "Governance" `
    -title "Data Governance + Quality" `
    -description "Data contracts, schema evolution, lineage, cataloging, PII handling, GDPR/CCPA, SLA monitoring." `
    -tier "Tier E" `
    -notebooks @(
        "data_contracts_schema_evolution.ipynb",
        "lineage_openlineage_marquez.ipynb",
        "cataloging_datahub_amundsen.ipynb",
        "pii_masking_tokenization.ipynb",
        "gdpr_ccpa_pipeline_patterns.ipynb",
        "data_sla_monitoring_alerting.ipynb"
    )

$govNotebooks = @{
    "Governance\data_contracts_schema_evolution.ipynb" = "Data Contracts and Schema Evolution"
    "Governance\lineage_openlineage_marquez.ipynb"     = "Data Lineage — OpenLineage and Marquez"
    "Governance\cataloging_datahub_amundsen.ipynb"     = "Data Cataloging — DataHub and Amundsen"
    "Governance\pii_masking_tokenization.ipynb"        = "PII Handling — Masking and Tokenization"
    "Governance\gdpr_ccpa_pipeline_patterns.ipynb"     = "GDPR and CCPA Pipeline Patterns"
    "Governance\data_sla_monitoring_alerting.ipynb"    = "Data SLA Monitoring and Alerting"
}
foreach ($nb in $govNotebooks.GetEnumerator()) {
    New-NotebookPlaceholder -rel $nb.Key -topic $nb.Value -tier "Tier E"
}

# ── 9. Staff_Craft/ ─────────────────────────────────────────────────
Write-Host "[9] Staff_Craft\" -ForegroundColor White
New-Folder "Staff_Craft"
New-Folder "Staff_Craft\supplement_prompts"
New-Readme `
    -rel "Staff_Craft" `
    -title "Staff Craft" `
    -description "RFC writing, influence without authority, tech debt frameworks, cloud cost optimization, mentoring." `
    -tier "Tier F" `
    -notebooks @(
        "rfc_design_doc_writing.ipynb",
        "influence_without_authority.ipynb",
        "tech_debt_prioritization.ipynb",
        "cloud_cost_optimization.ipynb",
        "oncall_incident_runbooks.ipynb",
        "mentoring_patterns.ipynb"
    )

$staffNotebooks = @{
    "Staff_Craft\rfc_design_doc_writing.ipynb"      = "RFC and Design Doc Writing"
    "Staff_Craft\influence_without_authority.ipynb"  = "Influence Without Authority"
    "Staff_Craft\tech_debt_prioritization.ipynb"     = "Tech Debt Prioritization Frameworks"
    "Staff_Craft\cloud_cost_optimization.ipynb"      = "Cloud Cost Optimization Narratives"
    "Staff_Craft\oncall_incident_runbooks.ipynb"     = "On-Call and Incident Runbooks"
    "Staff_Craft\mentoring_patterns.ipynb"           = "Mentoring Patterns for Staff Engineers"
}
foreach ($nb in $staffNotebooks.GetEnumerator()) {
    New-NotebookPlaceholder -rel $nb.Key -topic $nb.Value -tier "Tier F"
}

# ════════════════════════════════════════════════════════════════════
# SUMMARY
# ════════════════════════════════════════════════════════════════════
Write-Host ""
Write-Host "══════════════════════════════════════════" -ForegroundColor Magenta
Write-Host "  Done. Workspace structure:" -ForegroundColor Magenta
Write-Host "══════════════════════════════════════════" -ForegroundColor Magenta
Write-Host ""

$folders = @(
    "scripts/                     (this script)",
    "supplement_prompts/          (existing + future prompt files)",
    "Basics/                      (existing — untouched)",
    "Basics/Databases/            (new — SQL, NoSQL, all DB types)",
    "Basics/Python_Data/          (new — Pandas, NumPy, PySpark)",
    "Technologies/                (new)",
    "ML_AI/Classical/             (new)",
    "ML_AI/DeepLearning/          (new)",
    "ML_AI/GenAI_MLOps/           (new)",
    "Governance/                  (new)",
    "Staff_Craft/                 (new)"
)
foreach ($f in $folders) {
    Write-Host "  $f" -ForegroundColor Cyan
}

Write-Host ""
$nbCount = ($sqlNotebooks.Count + $pyNotebooks.Count + $techNotebooks.Count +
            $classicalNotebooks.Count + $dlNotebooks.Count + $genaiNotebooks.Count +
            $govNotebooks.Count + $staffNotebooks.Count)
# Note: Basics/ notebooks already exist — not counted here
Write-Host "  Placeholder notebooks created : $nbCount" -ForegroundColor Yellow
Write-Host "  README.md files created       : 9" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Next: run gitq to commit the skeleton." -ForegroundColor Green
Write-Host ""

# ── gitq ────────────────────────────────────────────────────────────
Write-Host "  Running gitq..." -ForegroundColor White
try {
    powershell.exe -Command "gitq"
    Write-Host "  Skeleton committed." -ForegroundColor Green
} catch {
    Write-Host "  gitq failed — commit manually: git add -A && git commit -m 'skeleton' && git push" -ForegroundColor Red
}
