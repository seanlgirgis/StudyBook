# Splunk + Citi Telemetry Interview Narrative

## 1) The Problem

At Citi, the operational challenge was monitoring a large, business-critical API estate with **6,000+ endpoints** spread across multiple regions and service categories. The environment generated telemetry for core signals such as **latency, error rate, and throughput**, and the system had to support both real-time operational visibility and long-term regulatory traceability.

A practical way to describe the scale in interviews is this:

- **6,000+ API endpoints**
- Roughly **10 telemetry events per second per endpoint**
- Around **60,000 events per second** sustained at peak
- Multi-tier alerting based on severity
- Need for **real-time alerting**
- Need for **7-year retention**
- Need for **regulatory auditability**

For prep purposes, I map the interview story to the sample telemetry model below so I can explain it consistently:

- **PostgreSQL**
- `endpoints` table: **10,000 rows**
  - `endpoint_id` (int PK)
  - `name` (varchar)
  - `region` (varchar)
  - `status` (varchar)
  - `category` (varchar)
- `metrics` table: **500,000 rows**
  - `endpoint_id` (int FK)
  - `metric_name` (varchar)
  - `value` (float)
  - `timestamp` (timestamptz)
- `alerts` table: **25,000 rows**
  - `alert_id` (int PK)
  - `endpoint_id` (int FK)
  - `severity` (varchar)
  - `message` (text)
  - `created_at` (timestamptz)

The core business problem was not just collecting logs. It was building a system that could:

1. Ingest high-volume telemetry with low latency.
2. Detect incidents fast enough for operations teams to act.
3. Preserve searchable history for audits and regulatory reviews.
4. Provide reliable dashboards for engineering, operations, and leadership.
5. Scale without turning every investigation into a slow, manual search exercise.

That is the framing I use in interviews: **this was an observability and compliance system, not just a logging tool**.

---

## 2) The Architecture

The architecture centered on **HTTP Event Collector (HEC)** for ingest, a **3-node indexer cluster** for scalable storage and search, and a **Search Head cluster** for dashboards, scheduled alerts, and operational investigations.

### High-Level Flow

```text
                +---------------------------+
                |   API Services / Probes   |
                |  latency, errors, volume  |
                +-------------+-------------+
                              |
                              | JSON telemetry over HTTPS
                              v
                    +----------------------+
                    |   Splunk HEC Layer   |
                    |  tokenized ingest    |
                    +----------+-----------+
                               |
                               v
        +--------------------------------------------------+
        |            Splunk Indexer Cluster                |
        |--------------------------------------------------|
        | Indexer 1      Indexer 2       Indexer 3         |
        | hot/warm       hot/warm        hot/warm          |
        | bucket mgmt    replication     searchable store   |
        +--------------------+-----------------------------+
                             |
                             v
              +--------------------------------------+
              |        Search Head Cluster           |
              |--------------------------------------|
              | Dashboards | Scheduled Searches      |
              | Alerts     | Incident Investigation  |
              +----------------+---------------------+
                               |
               +---------------+------------------+
               |                                  |
               v                                  v
    +-----------------------+          +------------------------+
    | Ops / SRE Dashboards  |          | Alert Routing / Tiers  |
    | SLA, regions, storms  |          | Sev1 / Sev2 / Sev3     |
    +-----------------------+          +------------------------+

Retention Strategy:
- Hot: 7 days
- Warm: 90 days
- Cold: 7 years on S3
```

### Architectural Narrative

**Ingest:**  
Telemetry events were pushed over HTTPS into Splunk using **HEC**. That gave us a lightweight, low-latency ingestion model and avoided the extra operational overhead of managing large fleets of forwarders for this use case.

**Storage and search:**  
The **3-node indexer cluster** handled indexing, bucket management, and distributed search. This gave the platform enough parallelism to absorb sustained event volume while keeping operational searches responsive.

**Consumption:**  
A **Search Head cluster** exposed dashboards for service health, latency trends, regional failure patterns, and alert volume. It also ran scheduled searches to detect SLA breaches, storm conditions, and correlated incidents across endpoint groups.

**Retention:**  
The system used retention tiers aligned to operational and regulatory needs:

- **Hot:** 7 days for fastest access during active incidents
- **Warm:** 90 days for near-term troubleshooting and trend analysis
- **Cold:** 7 years on S3 for long-term auditability

That retention story matters in interviews because it shows I was balancing **performance, cost, and compliance** instead of treating storage as infinite.

---

## 3) The Key Decisions

## Why Splunk over ELK

The decision was driven primarily by **regulatory and operational concerns**.

Splunk was the better fit because:

- It gave us a more mature path for **enterprise governance and auditability**
- It reduced operational complexity for teams that needed **stable, supportable search and alerting**
- It aligned better with a regulated environment where **retention controls, access patterns, and traceability** mattered as much as raw ingestion capability

In an interview, I usually summarize it this way:

> ELK can be a strong platform, but in this case Splunk was the stronger enterprise choice because we needed faster time to value for regulated operations, predictable search behavior, and clearer long-term retention governance.

## Why HEC over forwarders

We chose **HEC** instead of universal/heavy forwarders because the telemetry was already structured and generated by services that could post JSON directly.

HEC gave us:

- Lower end-to-end ingest latency
- Simpler integration for API telemetry producers
- Less agent management overhead
- Cleaner tokenized authentication model
- Better fit for centralized service-generated events

In short: **forwarders are great when you need host-based collection; HEC was better for high-volume API telemetry generated directly by applications and probes**.

## Index design choices

We evaluated whether to keep everything in a single logical telemetry index or split by region.

### Option A: Single index
- `citi_telemetry`

### Option B: Multiple regional indexes
- `citi_telemetry_us`
- `citi_telemetry_eu`
- `citi_telemetry_apac`

The design bias was toward a primary index pattern like **`citi_telemetry`** with strong metadata fields such as:

- `region`
- `severity`
- `endpoint_id`
- `category`
- `metric_name`

Why that was attractive:

- Easier cross-region queries
- Simpler dashboard maintenance
- Fewer duplicated saved searches
- Cleaner operational model

Why we still considered splitting:

- Better data isolation by geography
- Possible retention or permission segmentation
- Potential search scoping advantages for region-specific teams

The interview-ready answer is:

> My default preference was a unified telemetry index with disciplined fielding, unless compliance or access boundaries forced regional separation. That kept the search model simpler and the dashboards more reusable.

## Retention tiers

We explicitly designed retention by access pattern:

- **Hot: 7 days**  
  For rapid incident investigation and high-frequency dashboard access.

- **Warm: 90 days**  
  For trend analysis, root cause follow-up, and recurring incident review.

- **Cold: 7 years on S3**  
  For audit, compliance, and historical review.

That was a business decision as much as a technical one. The platform had to support **fast operational response today** and **provable historical traceability years later**.

---

## 4) The SPL Queries

Below are five production-style SPL queries I use in interview prep. They are grounded in the Citi telemetry story and are easy to explain live.

## 4.1 Severity distribution

Used to understand current alert mix and whether the environment is drifting toward higher-severity incidents.

```spl
index=citi_telemetry sourcetype=alerts earliest=-15m
| stats count by severity
| sort - count
```

**What it shows:**  
How many alerts are hitting each severity bucket in the last 15 minutes.

**Why it matters:**  
It is a fast health indicator. A spike in Sev1 or Sev2 often tells leadership and operations that the issue is systemic, not isolated.

## 4.2 Endpoint storm detection

Used to identify endpoints generating abnormal alert volume in a short window.

```spl
index=citi_telemetry sourcetype=alerts earliest=-10m
| stats count as alert_count by endpoint_id
| where alert_count > 100
| sort - alert_count
```

**What it shows:**  
Endpoints that are generating alert storms.

**Why it matters:**  
Storms can hide the true root cause, overwhelm responders, and create noisy escalation paths.

## 4.3 Regional failure rate

Used to compare stability by region and quickly isolate geographic blast radius.

```spl
index=citi_telemetry sourcetype=metrics metric_name=error_rate earliest=-15m
| stats avg(value) as avg_error_rate by region
| eval avg_error_rate=round(avg_error_rate,4)
| sort - avg_error_rate
```

**What it shows:**  
Average error rate by region over the last 15 minutes.

**Why it matters:**  
This is one of the fastest ways to answer, “Is this local, regional, or global?”

## 4.4 SLA breach detection

Used to detect endpoints violating latency targets.

```spl
index=citi_telemetry sourcetype=metrics metric_name=latency_ms earliest=-5m
| stats p95(value) as p95_latency by endpoint_id, region
| where p95_latency > 300
| sort - p95_latency
```

**What it shows:**  
Endpoints whose p95 latency exceeds a 300 ms SLA threshold.

**Why it matters:**  
This turns raw telemetry into an operationally meaningful business signal.

## 4.5 Alert correlation

Used to correlate latency, error, and throughput degradation on the same endpoint.

```spl
index=citi_telemetry sourcetype=metrics earliest=-10m
| search metric_name IN ("latency_ms","error_rate","throughput")
| stats latest(value) as current_value by endpoint_id, metric_name
| xyseries endpoint_id metric_name current_value
| where latency_ms > 300 AND error_rate > 0.05 AND throughput < 100
| sort - latency_ms
```

**What it shows:**  
Endpoints where multiple failure signals line up at the same time.

**Why it matters:**  
This is closer to true incident detection than any single metric alone.

---

## 5) The Interview Answers

These are concise, ready-to-deliver versions I would use in interviews.

## 5.1 “Tell me about a monitoring system you built.”

I built a large-scale telemetry and alerting system for an environment with more than 6,000 API endpoints. The platform was designed to ingest around 60,000 telemetry events per second covering latency, error rate, throughput, and alert conditions. We used Splunk as the operational search and alerting layer, with HEC for low-latency ingest, a 3-node indexer cluster for scalable storage and search, and a Search Head cluster for dashboards and scheduled detections. The key design challenge was balancing real-time visibility with long-term regulatory retention, so we implemented tiered retention: 7 days hot, 90 days warm, and 7 years cold on S3. The result was a system that gave operations teams rapid incident detection while also supporting auditability and historical investigations.

## 5.2 “How do you handle 60K events per second?”

I handle that in layers. First, I make sure the ingest path is simple and low-latency, which is why HEC was the right fit for structured API telemetry. Second, I design indexes and fields so searches stay focused and efficient instead of forcing broad scans. Third, I separate operational retention from archival retention so high-speed storage is reserved for the data that needs fast access. Fourth, I invest in detection logic that summarizes the right signals — like p95 latency, regional error rate, and storm detection — instead of relying on raw event review for every incident. So the answer is not just scale out the cluster; it is also simplify ingest, design the data model correctly, and search only what matters.

## 5.3 “What would you do differently?”

If I were evolving the system further, I would push harder on two things. First, I would expand correlation and noise-reduction logic so the alerting system produced fewer symptom alerts and more incident-level signals. Second, I would tighten the bridge between Splunk and downstream analytical storage so long-horizon trend analysis and capacity forecasting became easier without overloading the operational search layer. In other words, the next step would be making the system not just observable, but more predictive and more cost-efficient over time.

---

## 6) The Numbers

These are the numbers I would memorize before an interview.

| Category | Number | Why it matters |
|---|---:|---|
| API endpoints monitored | 6,000+ | Core scale of the story |
| Events per endpoint per second | ~10 | Basis for throughput estimate |
| Total event rate | ~60,000 events/sec | Main scale number interviewers remember |
| `endpoints` table size | 10,000 rows | Describes modeled service inventory |
| `metrics` table size | 500,000 rows | Shows telemetry volume in the prep dataset |
| `alerts` table size | 25,000 rows | Shows alert history scale |
| Indexer cluster size | 3 nodes | Core storage/search architecture detail |
| Hot retention | 7 days | Fast incident response window |
| Warm retention | 90 days | Short- to medium-term investigation window |
| Cold retention | 7 years on S3 | Regulatory retention and auditability |
| Typical search latency target | < 5 seconds for operational dashboards | Shows performance expectation |
| Alert response target | < 1 minute from event to routed alert | Shows operational responsiveness |

---

## Final Interview Framing

The strongest way to tell this story is to keep it simple:

- **Problem:** massive API telemetry volume in a regulated environment
- **Architecture:** HEC ingest, indexer cluster, search heads, dashboards, alerts
- **Decisions:** Splunk for enterprise/regulatory fit, HEC for low-latency telemetry ingest, tiered retention for cost and compliance
- **Operations:** real-time dashboards, storm detection, SLA monitoring, correlation searches
- **Outcome:** fast incident detection plus long-term auditability

That framing consistently lands well because it shows scale, architecture, tradeoffs, and business impact in one narrative.
