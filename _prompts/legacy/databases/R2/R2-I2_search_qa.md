SAVE AS: search_qa.md
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing Staff-level interview Q&A for search databases.

TASK: Generate 20 Q&A pairs covering Elasticsearch internals, query design, and operational patterns. Group into sections: Inverted Index and Storage (Q1-6), Query Design (Q7-12), Aggregations and Performance (Q13-16), Operations and Decision (Q17-20).

Every answer ends with a Citi framing sentence.

DATASET CONTEXT — do not deviate:
- Elasticsearch: localhost:9200 | citi-alerts index: 25,000 documents
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

Include questions on: inverted index mechanics and why it beats SQL LIKE for full-text, BM25 scoring vs TF-IDF, keyword vs text mapping difference and when each applies, dynamic mapping and mapping explosion risk, filter context vs query context (scoring vs no-scoring), bool query structure (must/should/filter/must_not), aggregation bucket vs metric vs pipeline types, shard count selection and oversharding consequences, replica shard read routing, near-real-time search (1 second refresh interval), index lifecycle management (ILM) for log rotation, Elasticsearch vs Splunk for observability use cases, segment merging and forcemerge cost, hot-warm-cold architecture for logs, scroll API vs search_after for deep pagination.

CONSTRAINTS:
- Questions must be answerable from memory in a 45-minute Staff DE interview
- Answers: 3-6 sentences, precise, no filler
- Always end each answer with a Citi framing sentence
- Valid GitHub Flavored Markdown

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

