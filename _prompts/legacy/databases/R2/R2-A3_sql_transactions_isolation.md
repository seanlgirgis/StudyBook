SAVE AS: sql_transactions_isolation.ipynb
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a deep PostgreSQL transactions and isolation notebook.

TASK: Cover MVCC internals, all four isolation levels, deadlock simulation and prevention, and advisory locks — all running live against the Citi telemetry database.

DATASET CONTEXT — do not deviate:
- PostgreSQL: localhost:5432, db=de_telemetry, user=de_admin, password=DeAdmin2026!
- endpoints: 10,000 rows | endpoint_id (int PK), name (varchar), region (varchar), status (varchar), category (varchar)
- metrics: 500,000 rows | endpoint_id (int FK), metric_name (varchar), value (float), timestamp (timestamptz)
- alerts: 25,000 rows | alert_id (int PK), endpoint_id (int FK), severity (varchar), message (text), created_at (timestamptz)
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

SECTIONS:
1. Title + Mental Model — "PostgreSQL Transactions — MVCC, Isolation, Deadlocks"; explain MVCC: each row has xmin/xmax, readers never block writers; ASCII diagram of two concurrent transactions seeing different snapshots
2. Imports + connection setup (psycopg2, real credentials, no pip install)
3. MVCC Internals — query pg_stat_activity while running a long transaction; show xmin/xmax on a rows; demonstrate that a SELECT in a second connection does NOT block during an UPDATE in the first; print "MVCC confirmed — reader not blocked"
4. Isolation Level Demo — run 4 pairs of transactions (one writer, one reader) for: READ UNCOMMITTED (Postgres treats as READ COMMITTED — show this), READ COMMITTED, REPEATABLE READ, SERIALIZABLE; for each level show what the reader sees mid-transaction; print a summary table
5. Deadlock Simulation — open two connections; transaction A locks endpoint_id=1 then tries endpoint_id=2; transaction B does the reverse; use threading to run both; catch psycopg2.errors.DeadlockDetected; print "Deadlock detected and resolved by Postgres — victim transaction rolled back"
6. Deadlock Prevention — same scenario but with consistent lock ordering (always lock lower endpoint_id first); confirm no deadlock; explain Citi pattern: "all alert writes lock by alert_id ascending to prevent deadlock in concurrent severity escalation"
7. Advisory Locks — use pg_try_advisory_lock(key) to implement application-level mutex; demonstrate two workers competing for same lock; show only one proceeds; pg_advisory_unlock; Citi use case: distributed cron job protection
8. What Just Happened — summary table: isolation level vs anomaly prevented vs Postgres behavior; Citi framing: "Citi's alert escalation pipeline runs REPEATABLE READ — prevents phantom alerts from appearing mid-escalation"

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error
- Use threading for deadlock simulation — both threads must start before either locks

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

