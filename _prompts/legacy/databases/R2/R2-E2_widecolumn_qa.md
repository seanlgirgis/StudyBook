SAVE AS: widecolumn_qa.md
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing Staff-level interview Q&A for wide-column databases.

TASK: Generate 25 Q&A pairs covering Cassandra internals, data modeling, and operational patterns. Group into sections: Architecture and Storage (Q1-7), Data Modeling (Q8-14), Consistency and Replication (Q15-20), Operations and Tuning (Q21-25).

Every answer ends with a Citi framing sentence.

DATASET CONTEXT — do not deviate:
- Cassandra: localhost:9042, keyspace=telemetry | metrics: ~1M rows
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

Include questions on: LSM tree vs B-tree write path, MemTable → SSTable flush mechanics, compaction purpose and strategy selection (STCS vs LCS vs TWCS), consistent hashing and vnode distribution, replication factor vs consistency level interaction, quorum math (RF=3, QUORUM = 2), why Cassandra has no joins (query-driven design), partition key design rules and wide partition risks, clustering key range query mechanics, tombstone accumulation and gc_grace_seconds, ALLOW FILTERING danger and when it's acceptable, Cassandra vs DynamoDB decision, Cassandra vs HBase comparison, Bigtable as the inspiration, when wide-column loses to relational.

CONSTRAINTS:
- Questions must be answerable from memory in a 45-minute Staff DE interview
- Answers: 3-6 sentences, precise, no filler
- Always end each answer with a Citi framing sentence
- Valid GitHub Flavored Markdown

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

