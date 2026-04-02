SAVE AS: ml_platform_concepts.md
PLACE IN: D:\Workspace\Technologies\
TOOL: Either (ChatGPT or Gemini)

---

ROLE: You are a senior Data Engineer writing a reference guide for an engineer preparing
for Staff DE interviews at a financial institution. Precise, dense, no filler.

TASK: Generate ml_platform_concepts.md — a concept reference covering the ML platform landscape:
experiment tracking, model registry, feature stores, and model serving — from a DE perspective.

DATASET CONTEXT — do not deviate:
- Citi narrative: endpoint anomaly detector model, features engineered from 500k metric rows in Postgres

STRUCTURE — produce exactly these sections in order:

# ML Platform — Core Concepts (Data Engineer Perspective)

## 1. Experiment Tracking
One paragraph. Cover: logging parameters, metrics, and artifacts for each training run,
reproducibility (given run_id, reproduce exact model), comparison across runs, MLflow Tracking as
the open-source standard, managed alternatives (W&B, Neptune, SageMaker Experiments, Vertex Experiments),
why DEs care: the training data pipeline is an input to every run.
End with: "Every Isolation Forest run on citi_telemetry_anomaly is logged — contamination, n_estimators, anomaly_rate, and the model artifact — all retrievable by run_id."

## 2. Model Registry
One paragraph. Cover: versioned store of promoted models, stages (Staging/Production/Archived),
aliased model names decouple serving code from run IDs, registry enables A/B testing
(serve v1 to 10% of traffic, v2 to 90%), MLflow Model Registry vs SageMaker Model Registry vs
Vertex AI Model Registry.
End with: "models:/citi_endpoint_anomaly_detector/Production loads whatever version is currently in Production — promoting v2 requires no code change in the scoring API."

## 3. Feature Store
One paragraph. Cover: centralized repository of reusable ML features, offline store (historical
features for training — S3/Parquet), online store (low-latency feature lookup at inference — Redis/DynamoDB),
point-in-time joins prevent training/serving skew (feature value at prediction time, not current value),
open-source: Feast, commercial: Tecton, managed: SageMaker Feature Store, Vertex Feature Store.
End with: "Without a feature store, 'avg_latency_24h' is computed differently in the training pipeline and the scoring API — training/serving skew makes the model worse in production."

## 4. Training/Serving Skew
One paragraph. Cover: the most dangerous ML production bug — model trained on features computed
one way, served with features computed differently, causes: different code paths, missing data
at inference, time window mismatch, feature store solves this by computing features once and
reusing for both training and serving.
End with: "Training the anomaly detector on avg_latency_7d but scoring on avg_latency_24h is training/serving skew — the model performs worse than offline metrics suggested."

## 5. MLOps Maturity
One paragraph. Cover: Level 0 = manual notebooks, no tracking; Level 1 = training pipeline automated,
experiment tracking in MLflow; Level 2 = full CI/CD for ML (retraining triggers, automated model evaluation,
shadow deployment, rollback); most teams are at Level 1; Level 2 is achievable with GitHub Actions + MLflow.
End with: "The citi_telemetry stack is targeting Level 1: automated Airflow DAG trains the model nightly, MLflow tracks every run, best model promoted to Staging automatically."

## 6. Feature Engineering as a DE Responsibility
One paragraph. Cover: 80% of ML time is feature engineering (data cleaning, joins, aggregations,
window functions), this is core DE work, Spark is the standard tool for feature engineering at scale,
features must be point-in-time correct (no data leakage — don't use future data to predict the past),
data leakage is the most common cause of inflated offline metrics.
End with: "The DE builds: endpoint features from 500k metric rows (Spark aggregations) → loaded to feature store → ML engineer trains on offline store → model served from online store."

## 7. Model Serving Patterns
One paragraph. Cover: batch scoring (Airflow DAG scores all endpoints nightly, writes predictions to Postgres),
real-time serving (Flask/FastAPI wraps the model, reads features from online store, returns prediction in <100ms),
model as microservice (Docker container, Kubernetes Deployment), MLflow models serve command for dev,
managed serving: SageMaker endpoints, Vertex AI endpoints, Azure ML endpoints.
End with: "Citi's anomaly detector: batch mode — nightly Airflow DAG loads model from MLflow registry, scores all endpoints, writes anomaly_score to de_telemetry.endpoint_scores."

## 8. SageMaker + Vertex AI — Managed ML Platforms
One paragraph. Cover: SageMaker = AWS managed ML platform (training jobs, endpoints, pipelines, Feature Store),
Vertex AI = GCP equivalent (Workbench, Training, Endpoints, Feature Store, Pipelines),
both provide managed Jupyter (SageMaker Studio, Vertex Workbench), both include experiment tracking and
model registry, DEs use them for managed training infrastructure not for notebook work.
End with: "Staff DE answer: 'We use MLflow locally for experiment tracking — when moving to production, SageMaker Training Jobs replace local training, SageMaker Endpoints serve the model, S3 Feature Store replaces Feast.'"

---

## Quick Reference Table

| Concept | What it is | Tool(s) |
|---------|-----------|---------|
| Experiment Tracking | Log params/metrics/artifacts per run | MLflow, W&B, Neptune |
| Model Registry | Versioned model store with stages | MLflow, SageMaker, Vertex |
| Feature Store | Reusable features, offline + online | Feast, Tecton, SageMaker FS |
| Training/Serving Skew | Different feature computation at train vs serve | Prevented by feature store |
| MLOps Level | Maturity of ML automation | Level 0-2 |
| Batch Scoring | Score all records on schedule | Airflow + MLflow |
| Real-time Serving | Low-latency inference API | FastAPI + MLflow serve |
| Managed Platform | Cloud-hosted full ML lifecycle | SageMaker, Vertex AI |

---

## Interview Flashcards

**Q: What is training/serving skew and how do you prevent it?**
A: Skew occurs when features are computed differently during training vs serving — for example,
training uses 7-day average latency but serving computes 24-hour average. The model performs worse
in production than offline metrics suggest. Prevention: compute features once in a feature store,
use the same code path for both training (offline store) and serving (online store).

**Q: What is a feature store and when do you need one?**
A: A feature store centrally computes, stores, and serves ML features. The offline store holds
historical features for training (point-in-time correct joins). The online store serves features
at inference time with millisecond latency. You need one when: multiple models reuse the same
features, or when training/serving skew is causing production degradation.

**Q: What does a DE own in the ML pipeline?**
A: The data side: source data pipelines, feature engineering code (Spark jobs), feature store
loading, batch scoring pipelines (Airflow DAGs), monitoring data quality. The ML engineer owns:
model architecture, hyperparameters, training logic, serving API. The line is feature store output
= DE handoff point to ML engineer.

**Q: What is MLOps Level 2?**
A: Full CI/CD for ML. A new batch of training data triggers automatic model retraining (Airflow DAG),
the new model is evaluated against the current production model (automated metrics comparison),
if better: promoted to Staging, shadow deployed (runs alongside Production, no traffic),
A/B tested, then promoted to Production. Failed model triggers rollback. No human in the loop.

CONSTRAINTS:
- Each concept: exactly one paragraph, 4-6 sentences, no bullets inside
- Citi tie-in is the last sentence of each paragraph
- Table: valid GFM pipe table
- No filler phrases

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.
