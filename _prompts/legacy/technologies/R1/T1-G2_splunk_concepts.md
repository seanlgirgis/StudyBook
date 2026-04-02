SAVE AS: splunk_concepts.md
PLACE IN: D:\Workspace\Technologies\
TOOL: Either (ChatGPT or Gemini)

---

ROLE: You are a senior Data Engineer writing a reference guide for an engineer preparing
for Staff DE interviews at a financial institution. Precise, dense, no filler.

TASK: Generate splunk_concepts.md — a concept reference covering 8 core Splunk abstractions,
each in one tight paragraph, with Citi narrative tie-ins throughout.

DATASET CONTEXT — do not deviate:
- Citi narrative: 6,000+ API endpoints, alerts ingested into Splunk index citi_telemetry,
  ops team runs SPL searches for anomaly detection and dashboards

STRUCTURE — produce exactly these sections in order:

# Splunk — Core Concepts

## 1. Index
One paragraph. Cover: the storage layer where events live, logical partition of data,
events in an index share retention policy and access control, default index vs named indexes,
index = closest analogy is a database table (but optimized for unstructured/time-series data).
End with: "All telemetry alerts live in index=citi_telemetry — ops team searches this index exclusively."

## 2. Sourcetype
One paragraph. Cover: classification of data format, Splunk uses sourcetype to determine how to
parse and extract fields, built-in sourcetypes (syslog, json, csv), custom sourcetypes for
proprietary formats, sourcetype ≠ source (source = where the data came from, sourcetype = what format it is).
End with: "Events from the HEC sender use sourcetype=citi:alert — colon convention namespaces custom sourcetypes."

## 3. Forwarder
One paragraph. Cover: lightweight agent that collects data and forwards to indexers,
Universal Forwarder (UF) = minimal footprint, monitors files/syslog/WMI, no indexing,
Heavy Forwarder = parses and filters before forwarding (higher resource cost), forwarder vs HEC
(forwarder = persistent agent on host, HEC = application pushes events via HTTP).
End with: "In the learning stack, the Python HEC sender replaces a forwarder — in production, Splunk UFs run on every Citi server and forward to a central indexer cluster."

## 4. Indexer
One paragraph. Cover: server that indexes incoming data (parses, compresses, stores), indexer
cluster = multiple indexers for replication and search distribution, search factor (replicated
copies) vs replication factor, indexer is to Splunk what a broker is to Kafka.
End with: "The learning stack runs a single Splunk indexer (the Docker container) — Citi production runs an indexer cluster with replication factor=3."

## 5. Search Head
One paragraph. Cover: server that accepts SPL queries from users, distributes searches to indexers,
merges and presents results, Search Head Cluster for HA, search head is separate from indexers
in enterprise deployments, Knowledge Objects (saved searches, lookups, dashboards) live on search heads.
End with: "http://localhost:8000 is the search head UI — it dispatches your SPL to the indexer and renders results."

## 6. SPL (Search Processing Language)
One paragraph. Cover: pipe-based query language, left-to-right data flow (search | transform | format),
three phases (event retrieval, reporting commands, output), SPL is not SQL — it operates on
unstructured events and extracts fields at search time (schema-on-read vs schema-on-write).
End with: "index=citi_telemetry sourcetype=citi:alert | stats count by severity | sort -count — this single pipe retrieves, groups, and sorts 500 events in milliseconds."

## 7. HEC (HTTP Event Collector)
One paragraph. Cover: HTTP endpoint for pushing events programmatically (no agent needed),
token-based authentication, supports JSON batch posting (newline-delimited), channels for
load distribution, timestamps in epoch format (time field), index/sourcetype/host set per event or
via HEC token defaults.
End with: "The Python notebook sends 500 events in 10 batches of 50 to HEC — at Citi scale, Kafka Connect → Splunk HEC handles millions of events per hour."

## 8. Knowledge Objects
One paragraph. Cover: saved searches (run on schedule), alerts (trigger action when search returns results),
lookups (CSV/KV store to enrich events with external data), field extractions (regex to create
fields at search time), dashboards (panels of SPL visualizations), report acceleration (pre-compute
expensive searches for dashboard performance).
End with: "A saved search runs every 15 minutes: index=citi_telemetry severity=CRITICAL | stats count — if count > 100, trigger a PagerDuty alert to the Citi ops team."

---

## Quick Reference Table

| Concept | One-line definition | Citi example |
|---------|---------------------|--------------|
| Index | Storage partition for events | index=citi_telemetry |
| Sourcetype | Event format classification | sourcetype=citi:alert |
| Forwarder | Agent that collects and ships data | UF on every Citi server |
| Indexer | Server that stores and indexes events | Single Docker container (dev) |
| Search Head | Server that runs SPL queries | localhost:8000 |
| SPL | Pipe-based query language | search | stats | sort |
| HEC | HTTP endpoint for programmatic ingestion | Python → HEC, 50 events/batch |
| Knowledge Objects | Saved searches, alerts, dashboards, lookups | 15-min CRITICAL alert |

---

## Interview Flashcards

**Q: What is the difference between a source and a sourcetype?**
A: source is the origin of the data — a file path, HEC token name, or syslog port. sourcetype is
the format classification — it tells Splunk how to parse the data (JSON, syslog, CSV, custom regex).
One sourcetype can have many sources; one source always has one sourcetype.

**Q: What is schema-on-read and why does Splunk use it?**
A: Schema-on-read means field definitions are applied at query time, not at write time. Splunk
indexes raw text and extracts fields when you search (via rex, spath, or auto field extraction).
This allows ingesting data before you know what questions you'll ask — impossible with schema-on-write databases.

**Q: When would you use a Heavy Forwarder instead of a Universal Forwarder?**
A: When you need to filter, mask, or route events before they reach the indexer — for example,
removing PII from log lines or routing security events to a separate index. The UF has minimal
CPU/memory footprint; the HF runs a full Splunk engine and can process data in flight.

**Q: What is an accelerated report and when do you need one?**
A: Report acceleration pre-computes a summary index of expensive searches on a schedule, so
dashboard loads are fast (milliseconds instead of minutes). Use it when a timechart or stats
over millions of events is too slow for real-time dashboards. Trade-off: disk space for pre-computed summaries.

CONSTRAINTS:
- Each concept: exactly one paragraph, 4-6 sentences, no bullets inside
- Citi tie-in is the last sentence of each paragraph
- Table: valid GFM pipe table
- No filler phrases

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

