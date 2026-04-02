SAVE AS: rds_aurora_setup.md
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing a cloud database setup guide.

TASK: Step-by-step guide to connect the Citi telemetry notebooks to AWS RDS PostgreSQL and Aurora Serverless v2. Every command is exact and executable — no "fill in your values" placeholders except for the specific values listed as variables at the top.

AWS CONTEXT — do not deviate:
- AWS profile: study
- AWS region: us-east-1
- AWS account: 357811130281
- Existing S3 bucket prefix: citi-telemetry-data-lake-dev

DATASET CONTEXT — do not deviate:
- PostgreSQL: localhost:5432, db=de_telemetry, user=de_admin, password=DeAdmin2026!
- endpoints: 10,000 rows | endpoint_id (int PK), name (varchar), region (varchar), status (varchar), category (varchar)
- metrics: 500,000 rows | endpoint_id (int FK), metric_name (varchar), value (float), timestamp (timestamptz)
- alerts: 25,000 rows | alert_id (int PK), endpoint_id (int FK), severity (varchar), message (text), created_at (timestamptz)
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

STRUCTURE:
1. Variables — define at top: RDS_ENDPOINT (to fill after creation), RDS_USER=de_admin, RDS_PASSWORD=DeAdmin2026!, RDS_DB=de_telemetry, AURORA_CLUSTER_ENDPOINT (to fill after creation)
2. Part 1 — RDS PostgreSQL 16: exact AWS CLI commands to create db subnet group, security group (allow port 5432 from your IP), RDS instance (db.t3.micro, 20GB gp2, Multi-AZ false); expected creation time; how to get the endpoint from `aws rds describe-db-instances`
3. Part 2 — Aurora Serverless v2: exact CLI commands to create Aurora PostgreSQL cluster (Serverless v2, min 0.5 ACU, max 2 ACU); why Serverless v2 vs provisioned for dev/test
4. Part 3 — Seed Data Migration: exact pg_dump command from localhost, pg_restore to RDS; expected time for 500K metrics; verify row counts match
5. Part 4 — Connect Notebooks: psycopg2 connection string for RDS; update notebooks to read from RDS_ENDPOINT env var; test query with timing comparison (local vs RDS)
6. Part 5 — Cost Estimation: RDS t3.micro $/month, Aurora Serverless v2 $/ACU-hour at 0.5 ACU; how to pause Aurora to zero cost when not in use; cleanup commands (delete instance, cluster, subnet group, security group)
7. Key Interview Points: 3 Q&A on RDS vs Aurora vs Aurora Serverless; when each fits a Citi workload

CONSTRAINTS:
- Valid GitHub Flavored Markdown
- Every AWS CLI command must include --profile study --region us-east-1
- Include expected output snippets for key commands

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

