SAVE AS: document_qa.md
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing Staff-level interview Q&A for document databases.

TASK: Generate 30 Q&A pairs covering MongoDB and DynamoDB internals, design patterns, and operational decisions. Group into sections: MongoDB Internals (Q1-8), MongoDB Design Patterns (Q9-14), DynamoDB Fundamentals (Q15-22), DynamoDB Design Patterns (Q23-28), Decision Scenarios (Q29-30).

Every answer ends with a Citi framing sentence.

DATASET CONTEXT — do not deviate:
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

Include questions on: MongoDB embedding vs referencing (16MB limit, unbounded arrays), aggregation pipeline vs SQL, BSON vs JSON storage, WiredTiger storage engine and MVCC, MongoDB atlas search vs Elasticsearch, DynamoDB partition key design for even distribution, RCU/WCU calculation, hot partition detection and write sharding, GSI vs LSI trade-offs, single-table design overloaded keys, DynamoDB Streams and Lambda integration, on-demand vs provisioned capacity mode selection, DynamoDB global tables and conflict resolution, MongoDB multi-document transactions cost, time-to-live (TTL) in both MongoDB and DynamoDB.

CONSTRAINTS:
- Questions must be answerable from memory in a 45-minute Staff DE interview
- Answers: 3-6 sentences, precise, no filler
- Always end each answer with a Citi framing sentence
- Valid GitHub Flavored Markdown

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

