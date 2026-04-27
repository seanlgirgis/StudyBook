

# Splunk — Core Concepts

## 1. Index

An index is the primary storage layer in Splunk where events are written, organized as a logical partition of data with shared retention policies, access controls, and storage settings. It is conceptually closest to a database table, but optimized for high-ingest, append-only, time-series and unstructured data rather than relational schemas. Splunk provides default indexes (like _internal, main) but production systems rely heavily on named indexes to isolate workloads and enforce governance. Index-level configuration determines data lifecycle, including hot, warm, cold, and frozen phases. Query performance and security boundaries are tightly coupled to how indexes are defined and accessed. All telemetry alerts live in index=citi_telemetry — ops team searches this index exclusively.

## 2. Sourcetype

Sourcetype defines the structure and format of incoming data and is the key mechanism Splunk uses to parse, segment, and extract fields from raw events. It is distinct from source, which identifies the origin (file path, HEC endpoint, syslog port), whereas sourcetype classifies the data format (JSON, CSV, syslog, or custom). Built-in sourcetypes handle common formats, but enterprises define custom ones for proprietary log schemas and enforce consistent parsing rules. Proper sourcetype assignment ensures correct timestamp extraction, field recognition, and downstream search usability. Misconfigured sourcetypes lead to broken parsing and unusable data at scale. Events from the HEC sender use sourcetype=citi:alert — colon convention namespaces custom sourcetypes.

## 3. Forwarder

A forwarder is a data collection agent responsible for monitoring sources and shipping events to Splunk indexers with minimal latency. The Universal Forwarder (UF) is lightweight, runs on hosts, and performs no indexing—only collection and forwarding—making it suitable for large-scale deployment. A Heavy Forwarder (HF) includes full Splunk parsing capabilities, allowing filtering, routing, and transformation before forwarding, at the cost of higher resource usage. Forwarders differ from HEC in that forwarders are persistent agents on infrastructure, while HEC allows applications to push events over HTTP. Forwarders ensure reliable, continuous ingestion from infrastructure-level sources. In the learning stack, the Python HEC sender replaces a forwarder — in production, Splunk UFs run on every Citi server and forward to a central indexer cluster.

## 4. Indexer

An indexer is the core Splunk component that receives incoming data, parses it into events, compresses, indexes, and stores it for search. It performs critical functions like timestamp recognition, metadata tagging, and indexing into inverted structures for fast retrieval. In enterprise deployments, indexers are deployed in clusters to distribute ingestion load and provide redundancy through replication factor and search factor configurations. The replication factor controls how many copies of data exist, while search factor ensures enough searchable copies are available. Indexers are analogous to Kafka brokers in their role of durable data storage and distributed processing. The learning stack runs a single Splunk indexer (the Docker container) — Citi production runs an indexer cluster with replication factor=3.

## 5. Search Head

A search head is the interface layer where users submit SPL queries, and it orchestrates distributed search execution across indexers. It parses queries, optimizes execution plans, dispatches them to indexers, and merges results before presenting them to users. Search heads also host Knowledge Objects such as dashboards, saved searches, and alerts, making them the control plane for analytics. In large deployments, Search Head Clusters provide high availability and workload distribution. Separation of search heads from indexers ensures scalability and independent tuning of compute and storage layers. [http://localhost:8000](http://localhost:8000) is the search head UI — it dispatches your SPL to the indexer and renders results.

## 6. SPL (Search Processing Language)

SPL is a pipe-based query language designed for streaming transformations over event data, where commands execute left-to-right in a data flow model. It operates in three phases: event retrieval (search), transformation (stats, eval, rex), and formatting (table, sort, output). Unlike SQL, SPL works on raw, unstructured events and applies schema-on-read, extracting fields dynamically at query time. This allows flexible exploration without predefined schemas but requires efficient query design for performance. SPL combines filtering, aggregation, and visualization in a single expression chain. index=citi_telemetry sourcetype=citi:alert | stats count by severity | sort -count — this single pipe retrieves, groups, and sorts 500 events in milliseconds.

## 7. HEC (HTTP Event Collector)

HEC is an HTTP-based ingestion interface that allows applications and services to send data directly to Splunk without installing agents. It uses token-based authentication and supports high-throughput ingestion via batched JSON events, typically newline-delimited for efficiency. Each event can specify metadata such as index, sourcetype, host, and timestamp, or inherit defaults from the HEC token configuration. HEC supports channels to distribute load and maintain ordering guarantees under high concurrency. It is commonly used in modern architectures where services emit logs or metrics programmatically. The Python notebook sends 500 events in 10 batches of 50 to HEC — at Citi scale, Kafka Connect → Splunk HEC handles millions of events per hour.

## 8. Knowledge Objects

Knowledge Objects are reusable configurations that enhance data usability and automate operational workflows in Splunk. They include saved searches (scheduled queries), alerts (trigger actions based on conditions), lookups (external enrichment via CSV or KV store), field extractions (regex-based parsing), and dashboards (visual aggregations). These objects enable abstraction and reuse, reducing duplication of logic across teams. Advanced features like report acceleration pre-compute summaries to optimize dashboard performance at scale. Knowledge Objects are central to turning raw telemetry into actionable insights. A saved search runs every 15 minutes: index=citi_telemetry severity=CRITICAL | stats count — if count > 100, trigger a PagerDuty alert to the Citi ops team.

---

## Quick Reference Table

| Concept           | One-line definition                         | Citi example                  |
| ----------------- | ------------------------------------------- | ----------------------------- |
| Index             | Storage partition for events                | index=citi_telemetry          |
| Sourcetype        | Event format classification                 | sourcetype=citi:alert         |
| Forwarder         | Agent that collects and ships data          | UF on every Citi server       |
| Indexer           | Server that stores and indexes events       | Single Docker container (dev) |
| Search Head       | Server that runs SPL queries                | localhost:8000                |
| SPL               | Pipe-based query language                   | search | stats | sort         |
| HEC               | HTTP endpoint for programmatic ingestion    | Python → HEC, 50 events/batch |
| Knowledge Objects | Saved searches, alerts, dashboards, lookups | 15-min CRITICAL alert         |

---

## Interview Flashcards

**Q: What is the difference between a source and a sourcetype?**
A: source is the origin of the data — a file path, HEC token name, or syslog port. sourcetype is the format classification — it tells Splunk how to parse the data (JSON, syslog, CSV, custom regex). One sourcetype can have many sources; one source always has one sourcetype.

**Q: What is schema-on-read and why does Splunk use it?**
A: Schema-on-read means field definitions are applied at query time, not at write time. Splunk indexes raw text and extracts fields when you search (via rex, spath, or auto field extraction). This allows ingesting data before you know what questions you'll ask — impossible with schema-on-write databases.

**Q: When would you use a Heavy Forwarder instead of a Universal Forwarder?**
A: When you need to filter, mask, or route events before they reach the indexer — for example, removing PII from log lines or routing security events to a separate index. The UF has minimal CPU/memory footprint; the HF runs a full Splunk engine and can process data in flight.

**Q: What is an accelerated report and when do you need one?**
A: Report acceleration pre-computes a summary index of expensive searches on a schedule, so dashboard loads are fast (milliseconds instead of minutes). Use it when a timechart or stats over millions of events is too slow for real-time dashboards. Trade-off: disk space for pre-computed summaries.
