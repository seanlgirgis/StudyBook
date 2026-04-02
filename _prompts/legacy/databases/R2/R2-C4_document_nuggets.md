SAVE AS: document_nuggets.md
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing gotcha nuggets for document databases.

TASK: Generate 10 document database gotcha nuggets covering MongoDB and DynamoDB. Cover: DynamoDB hot partition from sequential auto-increment PK (use UUID or hash prefix instead), MongoDB unbounded array growth causing document to exceed 16MB limit, MongoDB $lookup (join) doing collection scan when foreign field has no index, DynamoDB GSI consuming double write capacity on every item update (WCU × number of GSIs), MongoDB aggregation $group stage materializing entire result set in memory (100MB default limit), DynamoDB on-demand capacity spiky cost vs provisioned + auto-scaling for predictable workloads, MongoDB missing index on sort field causing in-memory sort with 32MB limit, DynamoDB single-table design breaking on new access pattern not modeled in PK/SK, MongoDB transactions locking multiple documents across collections causing contention at scale, DynamoDB Streams shard iterator expiring after 4 hours causing missed records.

DATASET CONTEXT — do not deviate:
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

CONSTRAINTS:
- Each nugget: title + 2-sentence setup + 1-sentence fix/lesson
- Gotcha framing — something that bites engineers who think they know the tool
- Citi framing woven naturally into setup or fix sentence
- Valid GitHub Flavored Markdown

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

