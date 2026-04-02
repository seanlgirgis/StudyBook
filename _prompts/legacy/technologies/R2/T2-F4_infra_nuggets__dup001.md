SAVE AS: infra_nuggets.md
PLACE IN: D:\Workspace\Technologies\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing gotcha nuggets.

TASK: Generate 10 infrastructure gotcha nuggets. Cover: Terraform state drift (resource changed outside Terraform), K8s OOM kill from missing resource limits, Docker layer cache invalidation from COPY order, K8s ImagePullBackOff from wrong registry credentials, Terraform destroy on a module deletes all child resources (including stateful ones), K8s pending pods from resource quota exhaustion (no error, just hangs), Docker build context sending node_modules / .git causing slow builds, Terraform provider version not pinned causing breaking changes on init, K8s CrashLoopBackOff vs Error distinction, Secret stored as base64 (not encrypted) — many teams think it is encrypted.

DATASET CONTEXT — do not deviate:
- Database: PostgreSQL on localhost:5432, db=de_telemetry, user=de_admin, password=DeAdmin2026!
- endpoints table: 10,000 rows | endpoint_id (int PK), name (varchar), region (varchar), status (varchar), category (varchar)
- metrics table: 500,000 rows | endpoint_id (int FK), metric_name (varchar), value (float), timestamp (timestamptz)
- alerts table: 25,000 rows | alert_id (int PK), endpoint_id (int FK), severity (varchar), message (text), created_at (timestamptz)
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

CONSTRAINTS:
- Each nugget: title + 2-sentence setup + 1-sentence fix/lesson
- Gotcha framing — something that bites engineers who think they know the tool
- Citi framing woven naturally into setup or fix sentence
- Valid GitHub Flavored Markdown

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.
