SAVE AS: graph_qa.md
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing Staff-level interview Q&A for graph databases.

TASK: Generate 20 Q&A pairs covering Neo4j internals, Cypher, graph algorithms, and when to use graph vs relational. Group into sections: Graph Model and Internals (Q1-6), Cypher and Query Patterns (Q7-12), Graph Algorithms and Use Cases (Q13-17), Decision and Trade-offs (Q18-20).

Every answer ends with a Citi framing sentence.

DATASET CONTEXT — do not deviate:
- Neo4j: localhost:7687, 10,000 endpoint nodes with DEPENDS_ON relationships
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

Include questions on: property graph model vs RDF, native graph storage vs graph on top of relational, index-free adjacency and O(1) relationship traversal, Cypher MATCH vs SQL JOIN for multi-hop paths, variable-length path query performance, MERGE for idempotent upsert, graph algorithms (PageRank, betweenness centrality, community detection) and their DE use cases, fraud detection pattern (shared identity, circular dependency), Neo4j ACID transactions, Neo4j vs Neptune trade-offs, when graph database loses to relational (simple lookups, no relationship traversal needed), supernode problem and mitigation.

CONSTRAINTS:
- Questions must be answerable from memory in a 45-minute Staff DE interview
- Answers: 3-6 sentences, precise, no filler
- Always end each answer with a Citi framing sentence
- Valid GitHub Flavored Markdown

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

