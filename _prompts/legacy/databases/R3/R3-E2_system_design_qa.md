SAVE AS: system_design_qa.md
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing Staff-level database system design interview questions.

TASK: Generate 20 system design Q&A pairs for database-focused system design interviews. Each answer is a structured design walkthrough (not just a list of bullet points). Group into sections: Monitoring & Observability Systems (Q1-5), Transactional Systems (Q6-10), Analytical & Reporting Systems (Q11-15), Multi-Tier & Hybrid Systems (Q16-20).

Every answer ends with a Citi framing sentence.

DATASET CONTEXT — do not deviate:
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

Questions must include: Design the data layer for an API monitoring platform (10K endpoints, 500K metrics/hour), Design a real-time leaderboard system (Redis sorted sets, write path, cache invalidation), Design a notification/alert system that guarantees at-least-once delivery with deduplication, Design the storage layer for a financial transaction system (ACID, audit log, compliance retention), Design a search system over 100M log messages (Elasticsearch vs Solr, index design, shard sizing), Design a data warehouse ingestion pipeline from 20 OLTP sources into Redshift (CDC vs batch, schema registry), Design a time-series storage system for IoT sensor data at 1M events/second, Design a URL shortener (Redis + Postgres, cache-aside, TTL strategy), Design a recommendation engine data layer (graph DB for relationships, vector DB for similarity, Redis for serving), Design a multi-region active-active database setup for a trading platform (conflict resolution, CRDT, eventual vs strong consistency), Design a data lakehouse architecture (S3 + Delta Lake + Redshift Spectrum + dbt), Design a session store for a banking app (Redis Cluster, session serialization, eviction policy), Design a full audit log system (append-only, tamper-evident, queryable), Design a feature store for ML models (online store=Redis, offline store=S3/Parquet, point-in-time correctness), Design the database tier for a multi-tenant SaaS platform (schema-per-tenant vs shared schema), Design a GDPR-compliant data deletion system across a polyglot stack.

CONSTRAINTS:
- Each answer: 6-10 sentences covering data model, DB choice, access pattern, consistency requirement, and scaling consideration
- No single-line bullet-point answers — must read as a design walkthrough
- Always end with a Citi framing sentence
- Valid GitHub Flavored Markdown

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

