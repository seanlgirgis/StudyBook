# Canonical Derived Prompt

> Source legacy: D:\StudyBook\_prompts\legacy\technologies\R1\\T1-J1_mlflow_intro.md

SAVE AS: mlflow_intro.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

ROLE: You are a senior Data Engineer writing a Jupyter notebook for an engineer learning
MLflow for the first time. You write production-quality, fully working code.
No placeholders. No TODO comments. Every cell must execute against the real running stack.

TASK: Generate mlflow_intro.ipynb — a Jupyter notebook covering the MLflow mental model,
experiment tracking, model registry, and a first anomaly detection experiment on the Citi telemetry data.

DATASET CONTEXT — do not deviate:
- Database: PostgreSQL on localhost:5432, db=de_telemetry, user=de_admin, password=DeAdmin2026!
- metrics table: 500,000 rows | endpoint_id (int FK), metric_name (varchar), value (float), timestamp (timestamptz)
- alerts table: 25,000 rows | alert_id (int PK), endpoint_id (int FK), severity (varchar), message (text), created_at (timestamptz)
- Citi narrative: detect anomalous endpoint behavior from metric patterns — high latency, error spikes

TECH STACK CONTEXT — do not deviate:
- MLflow: localhost:5000, ghcr.io/mlflow/mlflow:latest, SQLite backend
- MLflow tracking URI: http://localhost:5000
- Experiment name: "citi_telemetry_anomaly"

NOTEBOOK STRUCTURE — produce exactly these sections in order:

SECTION 1 — Title + Mental Model (markdown cell)
- H1: "MLflow — First Contact"
- 3-paragraph mental model: what MLflow is (ML lifecycle platform), 4 components
  (Tracking, Projects, Models, Registry), where DE meets ML (feature engineering, data pipelines feeding models)
- Citi framing: "A Staff DE at Citi is asked: 'Can we detect which endpoints are about to fail?'
  That's an ML problem. MLflow tracks every experiment, logs the winning model, and serves it via a REST endpoint."
- ASCII diagram: [Postgres metrics] → [Feature Engineering] → [MLflow Experiment] → [Model Registry] → [Serving]

SECTION 2 — Install + Imports (code cell)
- pip install mlflow scikit-learn psycopg2-binary pandas numpy
- imports: mlflow, mlflow.sklearn, sklearn (IsolationForest, StandardScaler, train_test_split, classification_report),
  pandas, numpy, psycopg2, json

SECTION 3 — MLflow Health Check (code cell + markdown)
- Markdown: "Verify MLflow tracking server is running"
- Code:
  - import requests; r = requests.get("http://localhost:5000/health")
  - mlflow.set_tracking_uri("http://localhost:5000")
  - Print: f"MLflow tracking URI: {mlflow.get_tracking_uri()}"
  - Print: f"MLflow version: {mlflow.__version__}"

SECTION 4 — Load + Engineer Features (code cell + markdown)
- Markdown: H2 "Feature Engineering from Telemetry Metrics"
  - Explain: raw metric rows are not ML-ready; we aggregate per endpoint into features
- Code:
  - psycopg2 connect, load metrics table into pandas DataFrame
  - Pivot/aggregate by endpoint_id: compute mean, std, max, min for each metric_name
    (use pivot_table with aggfunc=[mean,std,max,min])
  - Flatten column names: f"{metric_name}_{agg}"
  - Load alerts: count alerts per endpoint_id, add column "alert_count"
  - Join features + alert_count on endpoint_id
  - Fill NaN with 0
  - Print: f"Feature matrix: {features_df.shape[0]} endpoints × {features_df.shape[1]} features"
  - Print head(5)

SECTION 5 — First MLflow Experiment: Isolation Forest (code cell + markdown)
- Markdown: H2 "Experiment 1 — Isolation Forest Anomaly Detection"
  - Explain: Isolation Forest detects anomalies without labels, suitable when we don't have ground truth
  - MLflow experiment = container for runs; each run = one model training
- Code:
  - mlflow.set_experiment("citi_telemetry_anomaly")
  - with mlflow.start_run(run_name="isolation_forest_v1") as run:
    - Log params: contamination=0.05, n_estimators=100, random_state=42
    - Scale features: StandardScaler
    - Fit IsolationForest(contamination=0.05, n_estimators=100, random_state=42)
    - Predict: -1 = anomaly, 1 = normal; convert to 0/1 binary
    - Log metrics:
      - anomaly_count: int(sum(predictions == 1))
      - anomaly_rate: float(mean(predictions == 1))
      - n_features: features_df.shape[1]
    - Log the scaler and model: mlflow.sklearn.log_model(scaler, "scaler"); mlflow.sklearn.log_model(model, "model")
    - Log feature names as artifact: mlflow.log_dict({"features": list(feature_cols)}, "features.json")
    - run_id = run.info.run_id
    - Print: f"Run ID: {run_id}"
    - Print anomaly_count, anomaly_rate

SECTION 6 — Second Run: Tuned Parameters (code cell + markdown)
- Markdown: "Track a second run with different contamination — MLflow makes comparison trivial"
- Code:
  - with mlflow.start_run(run_name="isolation_forest_v2"):
    - Same structure but contamination=0.1, n_estimators=200
    - Log same params/metrics/model
    - Print comparison note

SECTION 7 — Compare Runs (code cell + markdown)
- Markdown: H2 "Compare Experiments in MLflow"
- Code:
  - client = mlflow.tracking.MlflowClient()
  - experiment = client.get_experiment_by_name("citi_telemetry_anomaly")
  - runs = client.search_runs(experiment.experiment_id, order_by=["metrics.anomaly_rate ASC"])
  - Print a formatted table: run_name | contamination | n_estimators | anomaly_count | anomaly_rate
  - Print: "View all runs at http://localhost:5000"

SECTION 8 — Register the Best Model (code cell + markdown)
- Markdown: H2 "Model Registry — Promote the Best Model"
  - Explain: Registry = versioned model store, stages: None → Staging → Production → Archived
- Code:
  - Identify best run (lowest anomaly_rate)
  - Register: mlflow.register_model(f"runs:/{best_run_id}/model", "citi_endpoint_anomaly_detector")
  - client.transition_model_version_stage("citi_endpoint_anomaly_detector", version=1, stage="Staging")
  - Print: "Model registered as 'citi_endpoint_anomaly_detector' version 1, stage: Staging"

SECTION 9 — Load + Score from Registry (code cell + markdown)
- Markdown: "Load the Staging model and score new data — this is how an API would serve predictions"
- Code:
  - loaded_model = mlflow.sklearn.load_model("models:/citi_endpoint_anomaly_detector/Staging")
  - sample = features_df.sample(10, random_state=1)
  - preds = loaded_model.predict(scaler.transform(sample[feature_cols]))
  - anomalies = sample[preds == -1]
  - Print: f"Scored 10 endpoints — {len(anomalies)} flagged as anomalous"
  - Print anomaly endpoint_ids

SECTION 10 — MLflow UI Tour (markdown cell)
- H2: "MLflow UI — Where to Find Things"
- Bullet list:
  - http://localhost:5000 — MLflow Web UI
  - Experiments tab → citi_telemetry_anomaly → see all runs
  - Click a run → Parameters, Metrics, Artifacts (model files, features.json)
  - Compare runs: select 2 runs → Compare → side-by-side metrics chart
  - Models tab → citi_endpoint_anomaly_detector → version history, stage transitions

SECTION 11 — Summary (markdown cell)
- H2: "What Just Happened"
- Bullets: feature engineering from 500k metric rows, 2 Isolation Forest runs tracked, parameters/metrics/models logged,
  comparison via MlflowClient, best model registered, served from registry
- Citi tie-in: "This is the Staff DE interview answer: 'ML is just another data pipeline.
  The DE builds features in Spark, logs experiments in MLflow, promotes the model to Production stage,
  and the scoring API loads it from the registry — no manual model file management.'"
- Next: "Run ml_platform_concepts.md for vocabulary, then Round 2 for feature stores and SageMaker."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4
- mlflow.set_tracking_uri("http://localhost:5000") must be called before any mlflow operations
- feature_cols must be defined before Sections 6-9 reference them (define in Section 4 code cell)
- Section 9 uses the scaler defined in Section 5 — note this requires running cells in order
- No placeholder values

ACCEPTANCE: Every code cell executes. Section 8 shows model registered in MLflow registry.

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.


