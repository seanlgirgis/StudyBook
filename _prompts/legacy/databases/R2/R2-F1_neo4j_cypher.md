SAVE AS: neo4j_cypher.ipynb
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a deep Neo4j and Cypher guide notebook.

TASK: Cover Cypher query patterns, graph algorithms, fraud detection patterns, and APOC — all running live against the Citi telemetry Neo4j instance with endpoint dependency graphs.

DATASET CONTEXT — do not deviate:
- Neo4j: localhost:7687 (Bolt), user=neo4j, password=DeNeo4j2026!
- Neo4j Browser: localhost:7474
- 10,000 endpoint nodes seeded with DEPENDS_ON relationships (endpoint dependency graph)
- Node label: Endpoint | Properties: endpoint_id (int), name (str), region (str), status (str), category (str)
- Relationship: DEPENDS_ON (source endpoint depends on target endpoint)
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

SECTIONS:
1. Title + Mental Model — "Neo4j — Property Graph, Cypher, Graph Algorithms"; explain nodes, relationships, properties, labels; why graph wins for connected data (O(1) relationship traversal vs O(log n) join); ASCII diagram of endpoint dependency graph; when graph databases lose to relational
2. Imports + setup (neo4j driver, no pip install); driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "DeNeo4j2026!")); verify with MATCH (n) RETURN count(n); print "Neo4j connected — {count} nodes"
3. Basic Cypher Patterns — 5 queries: (1) MATCH (e:Endpoint) RETURN e LIMIT 5; (2) MATCH (e:Endpoint {region: 'APAC'}) RETURN count(e); (3) MATCH (a:Endpoint)-[:DEPENDS_ON]->(b:Endpoint) RETURN a.name, b.name LIMIT 10; (4) CREATE relationship; (5) MERGE pattern for idempotent upsert; print results for each
4. Path Queries — shortestPath between two endpoints; allShortestPaths; variable-length path MATCH (a)-[:DEPENDS_ON*1..3]->(b); explain graph traversal vs SQL recursive CTE; Citi use case: "which upstream endpoints does endpoint X depend on — 3 hops out?"
5. Fraud / Cascade Detection — find all endpoints that would be affected if endpoint X goes down (transitive dependencies); MATCH (root:Endpoint {endpoint_id: 1})<-[:DEPENDS_ON*]-(affected) RETURN affected.name, count(*); print "X endpoints affected by outage cascade"
6. Graph Algorithms (APOC or built-in) — use CALL apoc.algo.pageRank or db.stats for centrality; find top 5 most depended-upon endpoints; explain PageRank applied to infrastructure: highly connected nodes are blast-radius multipliers; Citi framing
7. Graph vs Relational — same "find all transitive dependencies" query in both Cypher and recursive SQL CTE; time both; show Cypher is simpler for >2 hops; explain when to use each
8. What Just Happened — Neo4j vs Neptune vs TigerGraph decision table; 4 interview Q&A; cleanup: MATCH (n) DETACH DELETE n only for test nodes created in session

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed
- No placeholder credentials — use real values (bolt://localhost:7687, neo4j/DeNeo4j2026!)
- Every code cell must execute top-to-bottom without error

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

