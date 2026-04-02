SAVE AS: search_nuggets.md
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing gotcha nuggets for search databases.

TASK: Generate 10 Elasticsearch gotcha nuggets. Cover: mapping explosion from dynamic mapping on JSON with unpredictable keys (index hits 1000-field limit and rejects new documents), near-real-time 1-second delay meaning freshly indexed docs not immediately searchable (use ?refresh=true for tests only), deep pagination with from/size causing coordinator to collect and sort offset+size hits from all shards (use search_after instead), shard count cannot be changed after index creation without reindex (plan upfront), forcemerge on hot index causing I/O saturation and indexing pause, aggregation on text field returning error (use keyword sub-field), fielddata enabled on text field loading entire inverted index into heap causing OOM, delete-by-query not immediately freeing disk space (tombstones until segment merge), index template not applied to existing index (only new indexes match a template), Kibana Discover query returning partial results because shard timeout hit during coordination.

DATASET CONTEXT — do not deviate:
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

CONSTRAINTS:
- Each nugget: title + 2-sentence setup + 1-sentence fix/lesson
- Gotcha framing — something that bites engineers who think they know Elasticsearch
- Citi framing woven naturally into setup or fix sentence
- Valid GitHub Flavored Markdown

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

