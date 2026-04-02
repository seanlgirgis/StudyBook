SAVE AS: spark_qa.md
PLACE IN: D:\Workspace\Technologies\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing Staff-level interview Q&A.

TASK: Generate 30 Q&A pairs. Sections: DAG and Execution Model (Q1-7), Shuffle and Performance (Q8-14), Memory Management (Q15-20), Structured Streaming (Q21-25), Tuning Decisions (Q26-30).

Cover: RDD vs DataFrame vs Dataset, lazy evaluation, action vs transformation, wide vs narrow dependency, shuffle write/read, spill to disk, executor memory config, GC pressure, broadcast join threshold, AQE, coalesce vs repartition, watermarking, output modes, checkpointing, Spark vs Flink, when to use Spark vs pandas.

Every answer ends with a Citi framing sentence.

DATASET CONTEXT — do not deviate:
- Database: PostgreSQL on localhost:5432, db=de_telemetry, user=de_admin, password=DeAdmin2026!
- endpoints table: 10,000 rows | endpoint_id (int PK), name (varchar), region (varchar), status (varchar), category (varchar)
- metrics table: 500,000 rows | endpoint_id (int FK), metric_name (varchar), value (float), timestamp (timestamptz)
- alerts table: 25,000 rows | alert_id (int PK), endpoint_id (int FK), severity (varchar), message (text), created_at (timestamptz)
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

CONSTRAINTS:
- Questions must be answerable from memory in a 45-minute Staff DE interview
- Answers: 3-6 sentences, precise, no filler
- Always end each answer with a Citi framing sentence
- Valid GitHub Flavored Markdown

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.
