SAVE AS: technologies_nuggets_master.md
PLACE IN: D:\Workspace\Technologies\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing the master gotcha nuggets reference document.

TASK: Consolidate the highest-signal gotcha nuggets across all 11 technology categories into one master reference. This is the document to read when something breaks in production and you need to know what bit you. Prioritize nuggets that are non-obvious, have caused real production incidents, and distinguish Staff-level awareness from senior-level.

DATASET CONTEXT — do not deviate:
- Database: PostgreSQL on localhost:5432, db=de_telemetry, user=de_admin, password=DeAdmin2026!
- endpoints table: 10,000 rows | endpoint_id (int PK), name (varchar), region (varchar), status (varchar), category (varchar)
- metrics table: 500,000 rows | endpoint_id (int FK), metric_name (varchar), value (float), timestamp (timestamptz)
- alerts table: 25,000 rows | alert_id (int PK), endpoint_id (int FK), severity (varchar), message (text), created_at (timestamptz)
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

STRUCTURE:
1. Header — "Technologies Master Nuggets — Production Gotchas Reference"; note: "4 gotchas per category = 44 total; each nugget: title + 2-sentence setup + 1-sentence fix; Citi framing woven into setup or fix"
2. Section A — Kafka (4 nuggets): consumer group rebalance storm under partition pressure, acks=all + min.insync.replicas deadlock under broker failure, auto.offset.reset=latest silently dropping events on first deploy, partition count can never decrease — only increase
3. Section B — Spark (4 nuggets): shuffle file explosion when numPartitions > executors × cores, broadcast join threshold breach causing driver OOM, AQE coalesce reducing parallelism below optimal post-shuffle, checkpointing to local filesystem causing silent data loss on executor restart
4. Section C — Airflow (4 nuggets): zombie task holding slot while scheduler thinks it finished, DAG import error silently preventing all downstream DAGs from loading, XCom size limit (48KB default) causing silent truncation of large payloads, catchup=True + missed runs triggering flood of concurrent DAG runs
5. Section D — dbt (4 nuggets): full refresh on an incremental model in production dropping all history, late-arriving data older than incremental filter silently excluded forever, dbt test failure not blocking downstream models without explicit on-run-end hook, macro side effects persisting across runs when state is stored in vars
6. Section E — Databricks / Lakehouse (4 nuggets): VACUUM running during time travel query causing FileNotFoundException, Z-order on high-cardinality column producing no pruning benefit, small file explosion from streaming writes without OPTIMIZE scheduled job, Delta log retention shorter than time travel window causing history gap
7. Section F — Infrastructure (4 nuggets): Terraform state lock not released after interrupted apply — requires manual unlock, K8s OOM kill on Spark executor with no log — only visible in node events, persistent volume claims not deleted after pod eviction consuming storage quota, Terraform workspace not isolating provider credentials causing cross-env resource creation
8. Section G — Splunk (4 nuggets): HEC token disabled after license throttle without explicit re-enable, summary index not populated because search head and indexer clocks differ by >1 second, spath command silently returning null for nested JSON fields deeper than 2 levels, sourcetype misconfiguration sending events to wrong index — no error, silent loss
9. Section H — AWS DE (4 nuggets): Glue DPU autoscaling to max on small jobs — set maxCapacity explicitly, Athena query scanning full partition on predicate not matching partition column type (int vs string), Lake Formation tag-based access silently overriding IAM policy in unexpected order, EMR bootstrap action failure leaving cluster in WAITING state with no visible error
10. Section I — GCP + Azure DE (4 nuggets): Dataflow worker autoscale lag causing backlog spike during burst before new workers provision, BigQuery slot contention on shared reservation silently throttling interactive queries, Pub/Sub undelivered message quota hitting 10GB cap and silently dropping new messages, Azure Event Hubs capture producing Avro files with schema version mismatch after schema update
11. Section J — ML Platform (4 nuggets): training-serving skew from feature store serving stale values during refresh window, MLflow artifact store path not version-pinned — re-running experiment overwrites artifacts, model registry transition to Production silently triggering serving infrastructure refresh in some configs, point-in-time join in feature store using wrong entity timestamp timezone causing label leakage
12. Section K — CI/CD for Data (4 nuggets): Great Expectations checkpoint silently passing when datasource returns 0 rows (empty DataFrame), dbt CI run using production target instead of dev schema — modifying live tables, GitHub Actions secret not available in fork PRs — CI silently skips credential-dependent steps, data contract schema evolution breaking downstream consumers when no version negotiation in place

CONSTRAINTS:
- Each nugget: title + 2-sentence setup + 1-sentence fix/lesson
- Gotcha framing — something that bites engineers who think they know the tool
- Citi framing woven naturally into setup or fix sentence
- Valid GitHub Flavored Markdown
- Each section must have exactly 4 nuggets

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

