SAVE AS: graph_nuggets.md
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing gotcha nuggets for graph databases.

TASK: Generate 10 Neo4j gotcha nuggets. Cover: supernode problem (a node with millions of relationships causes traversal to pull all adjacent edges into memory), relationship direction ignored in undirected match causing 2× result rows, MERGE creating duplicate nodes when label or property case differs, variable-length path query without upper bound causing full graph traversal and OOM, missing index on lookup property causing full node scan before relationship traversal, DETACH DELETE on a supernode timing out (delete relationships first in batches), Cypher query planner choosing wrong start node when multiple MATCH patterns exist (use USING INDEX hint), graph not ACID by default for multi-statement transactions in older Neo4j versions, Neo4j browser query result limit hiding incomplete data (browser caps at 1000 nodes), importing from CSV with periodic commit not supported in Neo4j 5 (use CALL IN TRANSACTIONS instead).

DATASET CONTEXT — do not deviate:
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

CONSTRAINTS:
- Each nugget: title + 2-sentence setup + 1-sentence fix/lesson
- Gotcha framing — something that bites engineers who think they know Neo4j
- Citi framing woven naturally into setup or fix sentence
- Valid GitHub Flavored Markdown

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

