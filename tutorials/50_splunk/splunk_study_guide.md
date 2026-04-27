# Study Guide - splunk

## 1. Module Mission

Production log pipelines fail in ways that are invisible until money or trust is lost. When raw events are not parsed and indexed, teams cannot find the error that caused a payment to fail, and the incident report turns into guesswork. When search scope is uncontrolled, a simple query grinds the whole cluster, masking the real outage. This module exists to prevent that quiet failure mode: logs that exist but cannot be searched fast enough to protect the system.

The scenario is an order platform with checkout and payments services emitting events and a logging team trying to make sense of them. You see raw log lines for order creation and card declines, then you watch those lines become searchable events. You also step into a control room view where dashboards display service health and alerts ring only when thresholds are crossed. The actors are engineers who need to spot a failing payment flow before it cascades into lost revenue.

The progression starts with **ingestion**, **parsing**, and **indexing**, and ends with cross-platform reasoning about Splunk and Elasticsearch. You begin by turning raw text into fields, then learn how an **SPL** pipeline narrows a search and produces aggregates. Next the module adds dashboards and alerts, then moves to anomaly detection where baselines and spikes become the signal. It finishes by contrasting storage, query, and ingestion models so you can choose the right toolchain.

After finishing this module, when you see a rising error rate with no obvious trace, you will know to check index scope, verify field extraction, and build a targeted SPL pipeline before you panic. When a dashboard goes stale, you will know to validate the ingestion path and confirm that events are actually landing in the expected index. When an alert fires, you will know to compare it to baseline windows rather than assume the alert itself is the truth. When a platform choice debate appears in production planning, you will know how ingestion, query language, and storage tiers change both cost and speed.

---

## 2. File Map

| File | One-line description |
|------|----------------------|
| `d00_log_ingestion_story.md` | Sets up the mailroom metaphor that maps raw logs to parsed, indexed events. |
| `d01_spl_basics_story.md` | Frames SPL as a search-to-stats pipeline that narrows signal from an index. |
| `d02_dashboards_alerts_story.md` | Establishes dashboards as state summaries and alerts as threshold triggers. |
| `d03_log_anomaly_detection_story.md` | Teaches baseline comparisons for throughput drops and error spikes. |
| `d04_splunk_vs_elastic_story.md` | Contrasts ingestion, query, and storage models across Splunk and Elastic. |
| `c001_log_ingestion_demo.py` | Proves how raw lines become searchable events with extracted fields. |
| `c002_spl_basics_demo.py` | Demonstrates search, filter, and aggregation in an SPL-like flow. |
| `c003_dashboards_alerts_demo.py` | Shows dashboard rollups and alert thresholds on latency and errors. |
| `c004_log_anomaly_detection_demo.py` | Detects anomalies by comparing windows to simple baselines. |
| `c005_splunk_vs_elastic_demo.py` | Prints a side-by-side comparison of Splunk and Elastic capabilities. |
| `INTERVIEW.md` | Provides scenario-based questions and answers for mastery checks. |

---

## 3. Story Files

### d00_log_ingestion_story.md - Mailroom Sorting for Logs

**Part A: The Problem Being Solved**
When logs arrive as raw text without structure, the system becomes a pile of unlabelled letters. Engineers cannot filter by `level` or `service`, so every incident search becomes a manual scan of raw lines. The failure mode is slow or missed detection: a payment failure is buried under thousands of unrelated INFO events, and no one can slice the data fast enough. Without indexing, even simple questions like "show me all ERRORs in checkout" require reading every event, which collapses response time during outages. This story exists to show that observability is not about collecting logs, it is about structuring them so you can act under pressure.

**Part B: The Scenario**
The narrative uses a mailroom metaphor to make the mechanics concrete. It starts with "Letters arrive as raw text." and shows a mailroom that must read addresses, sort bins, and store everything for fast lookup. The same steps are mapped to logs: ingestion brings the letters in, parsing reads the address, and indexing puts the letters into shelves you can query. You can see the goal in the phrase "Splunk turns raw logs into searchable events by parsing and indexing." which signals the end state of the pipeline. The scenario is deliberately simple so the reader focuses on the transformation from raw to searchable rather than on the service domain itself.

**Part C: The Core Concept**
The point of this story is that ingestion, parsing, and indexing are the minimum steps required to turn raw logs into searchable events.

**Part D: What to Watch For in the Code**
- Notice how `parse_log` preserves `_raw` while adding fields, because Splunk keeps the raw event alongside extracted fields.
- Follow how `index_events` adds an `index` field, mirroring how Splunk assigns events to named indexes for search scope.
- Track the `search` function filtering on `index` and `level`, which matches the `index=orders level=ERROR` search pattern.
### d01_spl_basics_story.md - The Toolbox Search Pipeline

**Part A: The Problem Being Solved**
When engineers do not narrow search scope early, they query everything and drown in noise. A single incident search can scan all indexes, slow the system, and still fail to isolate the events that matter. Without a disciplined pipeline, teams jump straight to aggregation and miss the detail needed to explain why a metric moved. The failure is twofold: performance collapses from wide searches, and the analyst loses the thread of the investigation because the search is not staged. This story makes it clear that you must start with a precise dataset, apply filters, and only then compute statistics.

**Part B: The Scenario**
The story uses a toolbox metaphor to show how the search pipeline should feel. You first "You open the toolbox (index), filter by tool type, then count how many of each you have." Each step is a concrete action: select the index, filter by `level=ERROR`, then summarize with a count by field. The line "SPL is a pipeline: search ? filter ? stats." provides the exact arc that the demo later follows. By stepping through the toolbox, the scenario teaches the order of operations, not just the commands themselves.

**Part C: The Core Concept**
The point of this story is that SPL is an ordered pipeline where index selection and filtering must come before aggregation.

**Part D: What to Watch For in the Code**
- Identify how `search` is called first with `index=orders`, which mirrors the recommended SPL habit of scoping early.
- Watch the second `search` call filtering by `level=ERROR`, showing how filter stages build on prior results.
- Inspect `stats_count_by` and how it builds a count map, reflecting `stats count by service` in SPL.

### d02_dashboards_alerts_story.md - Control Room Dashboards

**Part A: The Problem Being Solved**
When teams rely on raw logs alone, they miss the state of the system at a glance. Operators need a single view that summarizes total events, error volume, and latency, otherwise they only discover issues after customers complain. Without alerting thresholds, every spike requires manual detection, which means outages grow before anyone reacts. The failure mode is delayed response: a high latency incident sits undetected because no one is watching for it, or because the signal is buried in individual events. Dashboards and alerts exist to compress raw event streams into actionable signals that trigger fast response.

**Part B: The Scenario**
The scene is a control room with gauges and alarms. You can almost see the wall of charts as the story says, "A control room shows key gauges on a wall." It then narrows the idea of an alert to a simple trigger: "Alarms ring only when a gauge crosses a limit." The scenario makes it clear that dashboards summarize ongoing state, while alerts are discrete actions that wake people up. This framing sets up the demo to produce a metric rollup and then check for thresholds in the same run.

**Part C: The Core Concept**
The point of this story is that dashboards summarize current health while alerts activate only when a defined threshold or spike occurs.

**Part D: What to Watch For in the Code**
- See how `dashboard_metrics` computes totals and averages, mirroring a dashboard panel calculation.
- Look at the `ERROR_THRESHOLD` and `LATENCY_THRESHOLD` constants, which define the alert trigger boundaries.
- Follow `alert_checks` as it evaluates thresholds and emits alert labels, a direct stand-in for saved searches.

### d03_log_anomaly_detection_story.md - Traffic Monitor Baselines

**Part A: The Problem Being Solved**
Monitoring by simple point-in-time checks fails when the system is normally noisy or when failures are silent. A service can stop serving traffic without throwing errors, and a naive alert that checks only error counts will miss the outage. Without baselines, operators cannot distinguish normal variation from true anomalies, so they either ignore alerts or chase false positives. The failure mode is either missed downtime or alert fatigue, both of which make the log pipeline untrustworthy. This story introduces baseline comparison as the minimum viable method for detecting volume drops and error spikes.

**Part B: The Scenario**
The story uses a traffic camera that expects a steady flow. The line "A traffic camera expects a steady flow. If cars suddenly drop or pile up, something is wrong." captures both the baseline and the deviation. The narrative then names the specific deviations: "Throughput drop" and "Error spike" as the two anomaly types to watch. The detection pattern compares windows to baseline thresholds, which maps directly onto the demo's `BASELINE_REQUESTS` and `BASELINE_ERRORS`. The scenario is deliberately short so the reader can map it one-to-one with the code that follows.

**Part C: The Core Concept**
The point of this story is that anomalies are defined by deviations from a baseline, not by absolute counts alone.

**Part D: What to Watch For in the Code**
- Track how `BASELINE_REQUESTS` and `BASELINE_ERRORS` are used as multipliers, not as single hard limits.
- Observe the 0.6 and 3.0 multipliers in `detect_anomalies`, which implement drop and spike thresholds.
- Notice the `anomalies` list with `type` values, which mirrors how Splunk would tag events for later analysis.

### d04_splunk_vs_elastic_story.md - Two Toolkits for Logs

**Part A: The Problem Being Solved**
Teams often argue about log platforms without a shared frame for what actually differs. When you treat Splunk and Elastic as interchangeable, you miss the operational costs that come from ingestion pipelines, query models, and storage tiers. The failure mode is an expensive migration or a platform choice that optimizes for the wrong thing, such as choosing a query language without considering storage lifecycle. This story prevents that by mapping the differences into concrete categories so a decision is grounded in how the system will be run. Without this clarity, platform debates are opinion-driven and lead to avoidable rework.

**Part B: The Scenario**
The narrative compares two teams using different toolkits to solve the same observability problem. It states, "Two teams solve the same observability problem with different toolkits." and then enumerates ingestion, query, and storage differences. The line "Splunk uses forwarders/HEC into indexes; Elastic uses Beats/Logstash into indices." puts concrete components on each side. It then contrasts query language and storage models to show how user experience and retention costs change. The close, "Different stacks, similar goals: search, monitoring, and analytics." defines the common end state despite the implementation differences.

**Part C: The Core Concept**
The point of this story is that Splunk and Elastic reach similar observability outcomes through different ingestion, query, and storage models.

**Part D: What to Watch For in the Code**
- Look at the `COMPARISON` rows to see the categories used for side-by-side evaluation.
- Notice how ingestion and indexing are separated, which mirrors the architectural split in each platform.
- Pay attention to the query language row, which drives user workflow and performance trade-offs.

---

## 4. Demo Files

### c001_log_ingestion_demo.py - From Raw Lines to Indexed Events

**Part A: What This Demo Proves**
This demo proves that the difference between unusable logs and searchable events is a concrete, mechanical pipeline. Without the parsing step, the raw lines are opaque strings, and no search can reliably match `level` or `service`. By extracting key=value pairs and then tagging each record with an `index`, the output shows a stable structure that can be filtered with deterministic criteria. The evidence is visible in the printed events and in the filtered search results that return only the `level=ERROR` record. Seeing the search return a single error event is the proof that parsing and indexing enable precise questions to be answered fast.

**Part B: The Key Code**
```python
# NOTE: Parsing turns raw text into searchable fields before indexing.
def parse_log(line):  # <-- defines the extraction boundary between raw text and fields
    parts = line.split(" ")  # <-- splits tokens so key=value pairs can be isolated
    record = {"_raw": line, "timestamp": parts[0]}  # <-- preserves raw event and captures time
    for token in parts[1:]:  # <-- iterates over all remaining tokens for extraction
        if "=" in token:  # <-- guards to avoid malformed segments
            key, value = token.split("=", 1)  # <-- splits once to keep values intact
            record[key] = value  # <-- stores extracted fields for later search
    return record  # <-- returns a structured event ready for indexing
```

**Part C: How the Mechanism Works**
When `run_splunk_ingest_demo` runs, it first prints raw lines so you can see the unstructured input. Each line is then passed to `parse_log`, which splits on spaces and converts every `key=value` pair into a dictionary entry. The `_raw` field is stored so the original event text remains available, just like Splunk retains the raw event even after extraction. Next, `index_events` appends an `index` value to every record, simulating how Splunk assigns events to a named index for fast scoping. Finally, the `search` function filters the list by matching all criteria, which mimics how SPL narrows a dataset by indexed fields. The key mechanic is that extraction happens once, before search, so the search step operates on structured fields rather than on raw text scans.

**Part D: Expected Output**
```text
========================================================================
Scenario: log ingestion and indexing concepts

Ingest raw logs
  2026-03-27T12:00:01Z level=INFO service=checkout msg=order_created order_id=o100
  2026-03-27T12:00:05Z level=ERROR service=payments msg=card_declined order_id=o101
  2026-03-27T12:00:09Z level=INFO service=checkout msg=order_paid order_id=o100

Parsed + indexed events
  {'_raw': '2026-03-27T12:00:01Z level=INFO service=checkout msg=order_created order_id=o100', 'timestamp': '2026-03-27T12:00:01Z', 'level': 'INFO', 'service': 'checkout', 'msg': 'order_created', 'order_id': 'o100', 'index': 'orders'}
  {'_raw': '2026-03-27T12:00:05Z level=ERROR service=payments msg=card_declined order_id=o101', 'timestamp': '2026-03-27T12:00:05Z', 'level': 'ERROR', 'service': 'payments', 'msg': 'card_declined', 'order_id': 'o101', 'index': 'orders'}
  {'_raw': '2026-03-27T12:00:09Z level=INFO service=checkout msg=order_paid order_id=o100', 'timestamp': '2026-03-27T12:00:09Z', 'level': 'INFO', 'service': 'checkout', 'msg': 'order_paid', 'order_id': 'o100', 'index': 'orders'}

Search: index=orders level=ERROR
  {'_raw': '2026-03-27T12:00:05Z level=ERROR service=payments msg=card_declined order_id=o101', 'timestamp': '2026-03-27T12:00:05Z', 'level': 'ERROR', 'service': 'payments', 'msg': 'card_declined', 'order_id': 'o101', 'index': 'orders'}

Summary
- Ingestion takes raw logs into the system.
- Parsing extracts fields for search.
- Indexing assigns events to an index for fast queries.
```

**Part E: The One Rule**
> Every searchable event is born from raw text plus explicit field extraction.

### c002_spl_basics_demo.py - Search, Filter, Stats

**Part A: What This Demo Proves**
This demo proves that an SPL search is a staged pipeline, not a single opaque query. The observable evidence is the stepwise output: a full index scan first, a filtered subset next, and a final aggregate map last. Without seeing each stage printed, it is easy to believe that stats somehow happen directly on raw data, but the demo makes the intermediate datasets visible. The count by service only makes sense after the filter and the index selection have narrowed the set of events. By printing each stage, the demo makes the pipeline order tangible and confirms that each step builds on the last.

**Part B: The Key Code**
```python
def search(events, **criteria):  # <-- models the SPL search command as a filter
    results = []  # <-- collects only matching events
    for event in events:  # <-- streams through the dataset
        if all(event.get(k) == v for k, v in criteria.items()):  # <-- applies exact-match predicates
            results.append(event)  # <-- keeps events that pass every filter
    return results  # <-- returns the narrowed dataset for the next stage

def stats_count_by(events, field):  # <-- simulates SPL stats count by <field>
    counts = {}  # <-- aggregation map keyed by field value
    for event in events:  # <-- iterates through filtered events
        key = event.get(field, "(missing)")  # <-- handles absent fields deterministically
        counts[key] = counts.get(key, 0) + 1  # <-- increments the group count
    return counts  # <-- returns the final aggregation result
```

**Part C: How the Mechanism Works**
The demo starts by calling `search(EVENTS, index="orders")`, which scans each event and keeps only those with the matching index. This mirrors how a Splunk search head constrains the search to a specific index before doing any heavier work. The filtered list is then passed into a second `search` call with `level="ERROR"`, narrowing the dataset further to the single failing payment event. After filtering, `stats_count_by` iterates over the now-scoped events and builds a dictionary keyed by the selected field. The function uses `counts.get(key, 0)` to accumulate counts, which is the in-memory equivalent of a `stats count by service` aggregation. Because each stage returns a concrete list, you can see how the pipeline composes: each stage works on the output of the previous stage rather than on the original raw list.

**Part D: Expected Output**
```text
========================================================================
Scenario: SPL basics

Step 1: Select index=orders
  {'index': 'orders', 'level': 'INFO', 'service': 'checkout', 'status': 'created'}
  {'index': 'orders', 'level': 'ERROR', 'service': 'payments', 'status': 'declined'}
  {'index': 'orders', 'level': 'INFO', 'service': 'checkout', 'status': 'paid'}
  {'index': 'orders', 'level': 'WARN', 'service': 'payments', 'status': 'retry'}

Step 2: Filter level=ERROR
  {'index': 'orders', 'level': 'ERROR', 'service': 'payments', 'status': 'declined'}

Step 3: Stats count by service
{'checkout': 2, 'payments': 2}

Summary
- SPL starts with index selection.
- Filters narrow to events of interest.
- Stats summarize counts by a field.
```

**Part E: The One Rule**
> Always scope the index and filters before you aggregate.
### c003_dashboards_alerts_demo.py - Metrics and Thresholds

**Part A: What This Demo Proves**
This demo proves that dashboards and alerts are two distinct computations over the same event stream. The dashboard is a rollup that compresses the whole list into totals and averages, while the alert logic checks for thresholds and spikes. Without seeing both outputs side by side, it is easy to confuse a summary metric with an alerting condition, which leads to noisy or missed notifications. The printed metrics show the system state, and the printed alert list shows the action triggers. By emitting both, the demo shows the difference between descriptive monitoring and reactive alerting.

**Part B: The Key Code**
```python
def dashboard_metrics(events):  # <-- aggregates events into dashboard-ready KPIs
    total = len(events)  # <-- counts total events for volume context
    errors = sum(1 for e in events if e["level"] == "ERROR")  # <-- counts error events
    avg_latency = sum(e["latency_ms"] for e in events) / total  # <-- computes mean latency
    return {"total_events": total, "error_count": errors, "avg_latency_ms": round(avg_latency, 1)}  # <-- formats dashboard summary

def alert_checks(events):  # <-- evaluates alert conditions against thresholds
    errors = sum(1 for e in events if e["level"] == "ERROR")  # <-- reuses the error count for alerting
    high_latency = [e for e in events if e["latency_ms"] > LATENCY_THRESHOLD]  # <-- identifies spike candidates
    alerts = []  # <-- collects triggered alert labels
    if errors >= ERROR_THRESHOLD:  # <-- fires error count alert when threshold crossed
        alerts.append(f"ERROR_COUNT >= {ERROR_THRESHOLD}")  # <-- records error alert trigger
    if high_latency:  # <-- fires latency alert if any spike exists
        alerts.append(f"LATENCY_SPIKE > {LATENCY_THRESHOLD}ms")  # <-- records latency alert trigger
    return alerts, high_latency  # <-- returns alerts and the offending events
```

**Part C: How the Mechanism Works**
`run_dashboards_alerts_demo` calls `dashboard_metrics` first, which turns raw events into a compact dictionary of totals and averages. The `total` and `errors` counts are computed with `len` and a generator expression, then `avg_latency` is computed by summing the `latency_ms` values and dividing by `total`. This mirrors how a Splunk dashboard panel uses `stats` or `timechart` to render a summary value. Next, `alert_checks` is run on the same events but applies thresholds: it compares `errors` to `ERROR_THRESHOLD` and selects events above `LATENCY_THRESHOLD`. The function builds a list of alert labels, which is analogous to a saved search that triggers an alert action in Splunk. The output demonstrates two parallel computations: one descriptive for monitoring and one prescriptive for alerting.

**Part D: Expected Output**
```text
========================================================================
Scenario: dashboards and alerting patterns

Dashboard summary
{'total_events': 4, 'error_count': 1, 'avg_latency_ms': 415.0}

Alert evaluation
Alerts: ['ERROR_COUNT >= 1', 'LATENCY_SPIKE > 400ms']
High latency events:
  {'service': 'payments', 'level': 'ERROR', 'latency_ms': 900}
  {'service': 'payments', 'level': 'WARN', 'latency_ms': 500}

Summary
- Dashboards roll up signals for quick health checks.
- Alerts trigger on thresholds or spikes.
```

**Part E: The One Rule**
> Dashboards describe state; alerts demand action.

### c004_log_anomaly_detection_demo.py - Baselines and Deviations

**Part A: What This Demo Proves**
This demo proves that anomaly detection can be expressed as a comparison against baselines, not just as absolute rules. The output shows normal windows alongside windows that trigger a throughput drop or an error spike, making the anomaly criteria explicit. Without the printed windows and anomalies, it is easy to believe a single threshold is enough, but the demo shows two separate rules applied to the same data. The evidence is the anomaly list containing two different types, which demonstrates that the same event stream can yield different anomaly classes. By inspecting the anomaly types, you see how a simple baseline can catch both silent drops and loud error spikes.

**Part B: The Key Code**
```python
def detect_anomalies(windows):  # <-- evaluates each time window against baselines
    anomalies = []  # <-- collects detected anomaly records
    for w in windows:  # <-- iterates through each time window
        if w["requests"] < BASELINE_REQUESTS * 0.6:  # <-- flags throughput drops below 60 percent
            anomalies.append({"window": w["window"], "type": "throughput_drop"})  # <-- records drop anomaly
        if w["errors"] > BASELINE_ERRORS * 3:  # <-- flags error spikes above 3x baseline
            anomalies.append({"window": w["window"], "type": "error_spike"})  # <-- records spike anomaly
    return anomalies  # <-- returns all anomalies for reporting
```

**Part C: How the Mechanism Works**
`run_log_anomaly_demo` prints the baseline values first so the reader can see the reference point for every decision. It then iterates over the `WINDOWS` list and prints each time window with its request and error counts. `detect_anomalies` compares each window to two baseline-derived thresholds: a 60 percent drop for throughput and a 3x spike for errors. If a window crosses either threshold, a small anomaly record is appended with the window label and the anomaly type. The final printed anomalies list is a concrete signal list that a dashboard or alert system could consume. This mechanical flow mirrors a Splunk search that uses `eval` and `where` clauses to tag anomaly windows before indexing them into a summary store.

**Part D: Expected Output**
```text
========================================================================
Scenario: log-based anomaly detection

Baseline
{'requests': 100, 'errors': 2}

Windows
  {'window': '10:00', 'requests': 105, 'errors': 1}
  {'window': '10:05', 'requests': 98, 'errors': 2}
  {'window': '10:10', 'requests': 40, 'errors': 1}
  {'window': '10:15', 'requests': 120, 'errors': 9}

Anomalies
  {'window': '10:10', 'type': 'throughput_drop'}
  {'window': '10:15', 'type': 'error_spike'}

Summary
- Drops in throughput and spikes in errors are anomalies.
- Thresholds catch unusual log patterns.
```

**Part E: The One Rule**
> An anomaly is a meaningful deviation from baseline, not just a big number.

### c005_splunk_vs_elastic_demo.py - Side-by-Side Platform View

**Part A: What This Demo Proves**
This demo proves that platform comparison can be grounded in specific operational categories rather than opinion. The output prints ingestion, indexing, query, storage, and use case differences so the reader can evaluate trade-offs directly. Without such a list, engineers often compare tooling only by query syntax or by brand recognition, which misses core cost and performance implications. The evidence is the structured comparison printed under each category, which makes the contrast explicit and easy to discuss in architecture reviews. By seeing the categories side by side, you can map requirements to the platform features that actually deliver them.

**Part B: The Key Code**
```python
def run_splunk_vs_elastic_demo():  # <-- prints a category-based comparison report
    print("=" * 72)  # <-- standard header line to separate scenarios
    print("Scenario: Splunk vs Elasticsearch comparison")  # <-- declares the comparison context

    for row in COMPARISON:  # <-- iterates over comparison categories
        print(f"\n{row['category']}")  # <-- prints the category title
        print(f"  Splunk: {row['splunk']}")  # <-- prints the Splunk side of the category
        print(f"  Elastic: {row['elastic']}")  # <-- prints the Elastic side of the category

    print("\nSummary")  # <-- introduces the closing summary
    print("- Splunk emphasizes SPL pipelines over indexed events.")  # <-- summarizes Splunk strength
    print("- Elasticsearch uses document indices and DSL queries.")  # <-- summarizes Elastic model
    print("- Both support observability and log analytics.")  # <-- states the shared outcome
```

**Part C: How the Mechanism Works**
The function prints a separator line, then a scenario label so the output is easy to parse in a run log. It iterates through the `COMPARISON` list, which is a list of dictionaries where each dictionary has a `category` and a `splunk` and `elastic` entry. For each category, it prints a blank line followed by the category name, then prints two indented lines that show Splunk and Elastic descriptions. This is a direct structural analog of a slide in an architecture review, where each category is evaluated in turn. After the loop, it prints a summary section to reinforce the key distinctions: pipeline-based SPL, document-based DSL, and shared observability use cases. Because the data is encoded as a list, the comparison is easy to extend with new categories without changing the printing logic.

**Part D: Expected Output**
```text
========================================================================
Scenario: Splunk vs Elasticsearch comparison

Ingestion
  Splunk: Forwarders/HEC send raw logs; indexing happens automatically.
  Elastic: Beats/Logstash ship data; pipelines enrich before indexing.

Indexing
  Splunk: Events go into indexes with metadata + raw text.
  Elastic: Documents indexed into shards with mappings.

Query
  Splunk: SPL search | filter | stats pipeline.
  Elastic: DSL/Query APIs with aggregations.

Storage
  Splunk: Hot/warm/cold buckets with time-based retention.
  Elastic: Indices/data streams with tiered storage.

Use Cases
  Splunk: Ops monitoring, SIEM, log analytics dashboards.
  Elastic: Search, observability, log analytics, APM.

Summary
- Splunk emphasizes SPL pipelines over indexed events.
- Elasticsearch uses document indices and DSL queries.
- Both support observability and log analytics.
```

**Part E: The One Rule**
> Compare platforms by ingestion, query, and storage mechanics before brand or cost.

---

## 5. Study Questions

These questions test the scenarios covered in this module.
# Interview Questions — Splunk

> Topics covered: log ingestion and indexing · SPL basics · dashboards and alerting · log-based anomaly detection · Splunk vs Elasticsearch
> Levels: Starter | Mid | Senior | Architect

---

## Log Ingestion and Indexing

### Level 1 — Starter

**Q1: In `c001_log_ingestion_demo.py`, the `parse_log` function splits a raw log line and extracts key=value pairs into a dictionary. What Splunk concept does this simulate, and what is that process called during indexing?**
What a good answer covers:
- Field extraction at index time — Splunk parses raw event text into named fields stored alongside the `_raw` event
- The demo mimics Splunk's transform/EXTRACT stanza behavior using regex or delimiters
- The `_raw` field is always preserved so you can re-extract fields at search time if the schema changes
Why this is asked: Confirms the candidate understands the separation between raw storage and extracted fields.

**Q2: The demo stores events in a list after calling `index_events`, tagging each record with an `index` field. Why does Splunk organize data into named indexes, and what is the primary benefit?**
What a good answer covers:
- Indexes act as data silos that isolate retention policies, access controls, and search scope
- Keeping noisy or high-volume sources in a separate index prevents them from flooding searches across other data
- Each index has its own hot/warm/cold bucket lifecycle for cost management
Why this is asked: Tests understanding of multi-tenancy, RBAC, and storage tiering — common in real deployments.

**Q3: `c001_log_ingestion_demo.py` uses structured key=value log lines (e.g., `level=INFO service=checkout`). How does Splunk handle logs that are NOT in a structured format, and what role does `props.conf` play?**
What a good answer covers:
- Splunk uses `props.conf` to define source types and bind regex-based field extraction rules
- Unstructured logs require custom `EXTRACT` or `TRANSFORM` stanzas to produce usable fields
- Without structured fields, many SPL stats commands would fail or return inaccurate results
Why this is asked: Probes whether the candidate can operationalize Splunk beyond pre-formatted logs.

**Q4: The demo's `search` function filters indexed records by matching field values. What is the difference between searching at index time versus search time in Splunk, and when does each apply?**
What a good answer covers:
- Index-time extraction creates persistent fields written to disk; search-time extraction runs on demand via `REPORT` or `EVAL`
- Index-time fields are faster to query but less flexible; search-time fields allow schema-on-read without re-indexing
- The choice affects storage overhead and the ability to backfill field definitions across historical data
Why this is asked: Distinguishes candidates who understand Splunk's architecture from those who only know basic searches.

### Level 2 — Mid

**Q5: `c001_log_ingestion_demo.py` represents a single node ingesting three log lines. In a production Splunk deployment, how does the Universal Forwarder differ from a Heavy Forwarder, and when would you choose each?**
What a good answer covers:
- Universal Forwarder is lightweight, forwards raw data with minimal processing — suitable for most endpoints
- Heavy Forwarder can parse, mask, route, and filter before forwarding — used when field extraction or routing logic must happen close to the source
- Heavy Forwarders are resource-intensive and typically deployed for compliance masking or network-edge aggregation
Why this is asked: Evaluates practical deployment architecture knowledge beyond the conceptual demo.

**Q6: The demo assigns every event to a single `index_name`. In production, how would you design an index strategy for a multi-service platform (checkout, payments, auth) to balance search performance and retention cost?**
What a good answer covers:
- Per-service or per-criticality indexes allow different retention windows (e.g., payments logs kept 1 year vs. debug logs 7 days)
- Summary indexes can store pre-aggregated metrics to avoid re-scanning raw data for dashboards
- Too many small indexes increase management overhead; too few create noisy searches — right-sizing requires volume profiling
Why this is asked: Tests the candidate's ability to translate demo concepts into real architecture decisions.

**Q7: After parsing, the demo stores events in memory as Python dicts. How does Splunk's hot/warm/cold bucket model work, and what triggers a bucket to roll from hot to warm to cold?**
What a good answer covers:
- Hot buckets are open for writing and kept on fast SSD storage; warm buckets are closed but still on fast disk
- A bucket rolls to warm when it reaches the configured max size or age; cold buckets move to cheaper, slower storage
- Frozen buckets are archived or deleted based on retention policy — relevant for compliance and cost optimization
Why this is asked: Verifies understanding of Splunk's storage lifecycle, which is critical for capacity planning.

**Q8: The demo's `parse_log` function splits on spaces. What are common pitfalls when log lines contain quoted strings, multi-word values, or embedded JSON, and how does Splunk address them?**
What a good answer covers:
- Space-delimited parsing breaks when field values contain spaces (e.g., error messages); `QUOTE` and `SEDCMD` settings in `props.conf` handle this
- Embedded JSON fields require `spath` or `KV_MODE = json` to navigate nested structures
- Multi-format logs in the same source type can cause extraction failures — separate source types or conditional extractions are the fix
Why this is asked: Surfaces real-world log parsing pain points that any production Splunk admin encounters.

### Level 3 — Senior

**Q9: At scale, `c001_log_ingestion_demo.py`'s linear scan over indexed records becomes a bottleneck. How does Splunk's indexer clustering and search head clustering distribute search load, and what are the trade-offs?**
What a good answer covers:
- Indexer clusters replicate data across peers (RF/SF settings); search heads fan out queries to all indexers in parallel and merge results
- Adding indexers scales ingest throughput and parallel search; adding search heads scales concurrent user load
- Replication factor increases storage cost and network bandwidth; over-sharding can make small time-range searches slower due to coordination overhead
Why this is asked: Distinguishes engineers who have operated distributed Splunk from those with single-instance experience.

**Q10: The demo preserves `_raw` alongside extracted fields. In a high-volume environment (e.g., 500 GB/day), what strategies exist to reduce index storage without losing critical observability?**
What a good answer covers:
- Selective indexing: route verbose debug logs to a summary-only pipeline using `nullQueue` for raw storage while retaining aggregated metrics
- Indexed fields extraction with `INDEXED_EXTRACTIONS` reduces repeated parsing cost but not storage
- Using summary indexes and report acceleration materializes common query patterns, reducing full raw scan frequency
- SmartStore offloads warm/cold buckets to object storage (S3/GCS), decoupling compute from storage cost
Why this is asked: Tests cost-aware engineering judgment on a core Splunk operational challenge.

**Q11: The demo's `parse_log` function is deterministic and stateless. In production, what issues arise from event boundary detection (multi-line events, broken lines) during ingestion, and how does Splunk handle them?**
What a good answer covers:
- Java stack traces and multi-line JSON span multiple raw lines — Splunk uses `BREAK_ONLY_BEFORE`, `MUST_BREAK_AFTER`, or `LINE_BREAKER` in `props.conf` to stitch them
- Broken lines from buffered writes or network splits can create partial events that corrupt field extraction
- `TIME_PREFIX` and `MAX_TIMESTAMP_LOOKAHEAD` settings ensure Splunk timestamps events correctly even when the timestamp is mid-line
Why this is asked: Multi-line event handling is one of the most common production issues for Splunk operators.

### Level 4 — Architect

**Q12: The demo models a synchronous ingest-then-search flow. How would you integrate Splunk HEC (HTTP Event Collector) with a Kafka-based streaming pipeline to achieve real-time log ingestion, and what delivery semantics trade-offs apply?**
What a good answer covers:
- A Kafka consumer reads from the log topic and POSTs batches to HEC endpoints; HEC acknowledgment tokens provide at-least-once delivery confirmation
- HEC does not natively support exactly-once — deduplication must be implemented upstream (e.g., using Kafka transactional producers + idempotent HEC token tracking)
- Batch size vs. latency trade-off: larger HEC batches improve throughput but increase end-to-end lag visible in dashboards
- Connecting to the streaming track: Kafka consumer group lag monitoring in Splunk can itself become an observability feedback loop
Why this is asked: Tests the ability to bridge Splunk with modern streaming infrastructure and reason about delivery guarantees.

**Q13: If a data quality incident corrupts field extractions for 24 hours of indexed events in `c001_log_ingestion_demo.py`'s scenario, what is the recovery path in Splunk, and how would you design ingestion pipelines to prevent silent extraction failures?**
What a good answer covers:
- Splunk does not re-index in place — recovery requires deleting the affected time-range buckets and re-ingesting from the original source (requires raw log retention upstream)
- Prevention: enforce a data contract schema at the forwarder or HEC pre-processing layer; use Splunk's `metrics.log` and `health.conf` to alert on extraction error rates
- Connecting to the data quality track: schema validation before HEC POST (e.g., JSON schema checks on the producer side) prevents malformed events from entering the index
- An immutable raw log archive (S3, GCS) upstream of Splunk provides a guaranteed replay source for re-ingestion after corruption
Why this is asked: Tests recovery planning, upstream data contract thinking, and cross-track architectural awareness.

---

## SPL Basics

### Level 1 — Starter

**Q1: In `c002_spl_basics_demo.py`, the search pipeline starts by selecting `index=orders`, then filters by `level=ERROR`. How does this translate to SPL syntax, and why does Splunk recommend specifying the index first in every search?**
What a good answer covers:
- SPL equivalent: `index=orders level=ERROR`
- Specifying the index first limits the search scope to one bucket set, avoiding full-cluster scans
- Without an index filter, Splunk searches all indexes the user has access to, dramatically increasing search time and cost
Why this is asked: Reinforces the single most important SPL performance habit from day one.

**Q2: The demo's `stats_count_by` function counts events grouped by a field. What is the SPL equivalent using `stats`, and what other aggregation functions does `stats` support beyond `count`?**
What a good answer covers:
- SPL: `index=orders | stats count by service` — directly mirrors the demo's `stats_count_by(events, "service")`
- `stats` also supports `sum`, `avg`, `max`, `min`, `dc` (distinct count), `values`, `list`, `stdev`
- Unlike SQL GROUP BY, SPL `stats` can aggregate multiple fields and functions in one command
Why this is asked: Tests foundational SPL aggregation knowledge, the most common operation after filtering.

**Q3: `c002_spl_basics_demo.py` demonstrates filtering on exact field values. How do SPL wildcard searches, comparison operators, and the `IN` operator extend this, and what are their performance implications?**
What a good answer covers:
- Wildcards (`level=ERR*`) trigger a linear scan of bloom filters; exact-match searches use the TSIDX index for fast lookup
- `IN` operator (`status IN (declined, retry)`) is syntactic sugar for OR conditions — use it for readability but be aware it does not use term indexes more efficiently than OR
- Comparison operators (`latency_ms > 500`) require numeric field extraction and cannot use string-based term indexes
Why this is asked: Shows whether the candidate understands when SPL searches are fast versus when they degrade.

**Q4: The demo searches a static in-memory list. In Splunk, what is the difference between a `search` command and a `tstats` command, and when should you use each?**
What a good answer covers:
- `search` reads raw `_raw` text and extracted fields from full index buckets; `tstats` reads only the TSIDX metadata (indexed fields), bypassing raw event data
- `tstats` is 10-100x faster for high-level aggregations over long time ranges but only works on fields indexed at ingest time
- Use `search` when you need non-indexed fields or full event content; use `tstats` for dashboard summary panels over 30+ day windows
Why this is asked: `tstats` is a critical performance optimization that many mid-level Splunk users are unaware of.

### Level 2 — Mid

**Q5: `c002_spl_basics_demo.py` uses a simple filter-then-count pipeline. How does SPL's pipe `|` model differ from SQL's declarative model, and what are the implications for query optimization?**
What a good answer covers:
- SPL is an ordered pipeline — each command receives the output of the previous one; SQL is declarative and the optimizer chooses execution order
- In SPL, you control optimization manually: push filters early, use `fields` to drop unneeded columns before expensive transformations
- SPL's pipeline model makes it easy to reason about data flow but means the user bears more responsibility for performance than in a SQL planner
Why this is asked: Addresses a fundamental conceptual difference that affects how engineers write efficient queries.

**Q6: The demo counts events per service. How would you extend this in SPL to compute a percentage of errors per service over a time window, and what SPL commands would you chain?**
What a good answer covers:
- `index=orders earliest=-1h | stats count as total, count(eval(level="ERROR")) as errors by service | eval error_rate=round(errors/total*100,2)`
- `timechart` could replace `stats` if the goal is a time-series percentage rather than a single aggregate
- The `eval` command is the SPL equivalent of a computed column and is essential for derived metrics
Why this is asked: Tests the ability to compose multi-step SPL pipelines, a common dashboard requirement.

**Q7: `c002_spl_basics_demo.py` shows filtering on a known field. In Splunk, what is the role of field aliases, calculated fields, and lookups in enriching events beyond what was ingested?**
What a good answer covers:
- Field aliases (`FIELDALIAS`) map one field name to another for unified searching without re-ingestion
- Calculated fields (`EVAL-`) add derived fields available at search time, similar to `eval` but pre-computed in the pipeline
- Lookups join external reference data (e.g., a CSV of service owners) to events, enabling enrichment without re-indexing
Why this is asked: Enrichment techniques are central to building useful dashboards and alerts from raw logs.

**Q8: The demo pipeline runs sequentially. How does Splunk's job scheduler prioritize concurrent searches, and what mechanisms exist to prevent a long-running SPL query from degrading dashboard performance for other users?**
What a good answer covers:
- Splunk uses a scheduler that assigns search priority based on user role and search type (real-time vs. historical)
- `max_searches_per_cpu` and `base_max_searches` in `limits.conf` cap concurrent searches per search head
- Report acceleration and summary indexes pre-compute expensive queries so dashboard panels read from summaries rather than triggering raw scans
Why this is asked: Operational awareness of resource management distinguishes senior Splunk users from power users.

### Level 3 — Senior

**Q9: `c002_spl_basics_demo.py` operates on a small static dataset. How does Splunk handle SPL searches that return millions of events, and what are the memory and disk spill behaviors to be aware of?**
What a good answer covers:
- Splunk streams events through the pipeline rather than loading all into memory; intermediate results are spilled to disk when they exceed `maxresultrows` or memory limits
- The `head` command can short-circuit pipeline evaluation for top-N use cases, dramatically reducing data processed
- Large `stats` operations with high cardinality grouping keys (e.g., by user_id) can exhaust memory — `sistats` and chunked aggregation are alternatives
Why this is asked: Memory management in SPL pipelines is a frequent source of production search failures.

**Q10: The demo uses exact string matching. In SPL, how do `regex`, `rex`, and `eval match()` differ, and when is each the right tool?**
What a good answer covers:
- `regex` filters events where the entire `_raw` field matches a pattern — used for coarse pre-filtering before field extraction
- `rex` extracts named capture groups from any field into new fields on the fly — the primary inline extraction tool
- `eval match(field, regex)` returns a boolean for conditional logic inside computed fields, not for filtering
- Overusing `rex` on `_raw` at search time instead of pre-extracting at index time is a common performance anti-pattern
Why this is asked: All three appear in production SPL but are frequently confused by candidates.

**Q11: `c002_spl_basics_demo.py`'s pipeline is linear. How would you use SPL subsearches and the `join` command for event correlation (e.g., matching payment errors to checkout orders), and what are their limitations?**
What a good answer covers:
- Subsearch: `index=orders level=ERROR [search index=orders status=declined | fields order_id]` — the inner search produces a filter applied to the outer
- Subsearches are limited to 10,000 results and 60 seconds by default; `join` has similar cardinality limits
- For high-volume correlation, `stats` self-join patterns or lookup-based correlation are more scalable alternatives
- True event correlation at scale is better done in a streaming layer (Kafka Streams, Flink) before ingestion
Why this is asked: Tests knowledge of SPL's correlation capabilities and their architectural limits.

### Level 4 — Architect

**Q12: `c002_spl_basics_demo.py` models searches as real-time point queries. How would you design a Splunk data model and pivot layer to support a self-service analytics platform where non-SPL users can build reports without writing search queries?**
What a good answer covers:
- Data Models define object hierarchies (root event, child event, transaction) with constrained field sets — they are the semantic layer on top of raw indexes
- Pivot UI generates SPL from data model definitions without users writing SPL; report acceleration materializes data model summaries to disk
- Connecting to the analytics track: data models function like a curated mart layer, similar to a dimensional model in a warehouse — the same normalization trade-offs apply
- Governance: data model definitions should be version-controlled and reviewed like schema changes in a relational system
Why this is asked: Tests whether the candidate can extend Splunk beyond power-user SPL toward a scalable analytics platform.

**Q13: If an organization needs both real-time alerting (sub-minute) and historical trend analysis (90-day rolling window) from the same log stream, how would you architect the SPL and index strategy, and where do Splunk's built-in capabilities require augmentation from other systems?**
What a good answer covers:
- Real-time saved searches with `rt` time windows provide sub-minute alerting but are resource-intensive and should be minimized
- Scheduled searches with 5-minute intervals and summary index writes balance freshness and cost for trend dashboards
- For true 90-day trend analytics, report acceleration over a data model or SmartStore-backed cold buckets is required
- Connecting to the streaming track: Kafka-based real-time alerting (Kafka Streams or Flink) can handle sub-second detection before Splunk, with Splunk receiving pre-aggregated results for dashboards
Why this is asked: Evaluates ability to select the right latency tier for each use case and know Splunk's boundaries.

---

## Dashboards and Alerting

### Level 1 — Starter

**Q1: In `c003_dashboards_alerts_demo.py`, the `dashboard_metrics` function computes total events, error count, and average latency. What SPL commands would produce these same metrics on a Splunk dashboard panel?**
What a good answer covers:
- `index=services | stats count as total_events, count(eval(level="ERROR")) as error_count, avg(latency_ms) as avg_latency_ms`
- Dashboard panels run as saved searches on a schedule (e.g., every 5 minutes) and cache results for display
- The Splunk Dashboard Studio or Classic Dashboard XML binds each panel to a saved search or inline SPL
Why this is asked: Verifies the candidate can translate demo logic directly into working SPL for a dashboard.

**Q2: The demo defines two thresholds: `LATENCY_THRESHOLD = 400` and `ERROR_THRESHOLD = 1`. How do you configure a Splunk alert to fire when these thresholds are breached, and what alert action types are available?**
What a good answer covers:
- Saved search with a condition: trigger when `error_count >= 1` OR `max(latency_ms) > 400` in the results
- Alert conditions can be: number of results, custom condition (SPL eval), rolling window comparisons
- Alert actions include: email, webhook (PagerDuty, Slack), run a script, add to triggered alerts list, send to a Splunk workflow
Why this is asked: Threshold-based alerting is the most common Splunk operational use case.

**Q3: `c003_dashboards_alerts_demo.py` runs `alert_checks` over all events at once. In Splunk, what is the difference between a scheduled alert and a real-time alert, and when is each appropriate?**
What a good answer covers:
- Scheduled alerts run on a cron interval (e.g., every 5 minutes over the last 5 minutes of data) — appropriate for most operational alerts
- Real-time alerts stream search results continuously and fire immediately — appropriate only for strict latency SLAs due to high resource cost
- For most production cases, a 1–5 minute scheduled alert is sufficient and far less resource-intensive than real-time
Why this is asked: Candidates often default to real-time alerts without understanding the resource trade-off.

**Q4: The demo's `dashboard_metrics` function calculates `avg_latency`. Why is average latency often a misleading metric for dashboards, and what alternatives does Splunk support?**
What a good answer covers:
- Averages mask outliers — a p99 latency spike causing user-facing errors may not move the average significantly if most requests are fast
- Splunk supports `perc95(latency_ms)` and `perc99(latency_ms)` via the `stats` command for percentile tracking
- Histogram panels using `bin` + `stats count by latency_bucket` show the full distribution
Why this is asked: Percentile vs. average is a fundamental observability concept that surfaces engineering maturity.

### Level 2 — Mid

**Q5: `c003_dashboards_alerts_demo.py` fires alerts based on instantaneous values. How would you implement a Splunk alert that only fires when a condition persists for at least 3 consecutive check intervals, to suppress transient spikes?**
What a good answer covers:
- Use a lookup or KV Store to track alert state across scheduled runs — increment a counter on each breach, reset on recovery
- Splunk's `collect` command can write intermediate state to a summary index that the next run checks before firing
- Alert suppression with `throttle` in the alert configuration prevents re-firing within a cooldown window, but doesn't track persistence count natively
Why this is asked: Transient spike suppression is a real production requirement that requires stateful alerting design.

**Q6: The demo uses a fixed `LATENCY_THRESHOLD`. How would you build a dynamic threshold alert in Splunk that fires when the current value deviates significantly from a historical baseline (e.g., last 7 days same hour)?**
What a good answer covers:
- Calculate the baseline with a subsearch or lookup: `[search index=services earliest=-7d@h latest=-0d@h | stats avg(latency_ms) as baseline, stdev(latency_ms) as stddev]`
- Alert fires when `current_value > baseline + 3*stddev` (3-sigma rule)
- The MLTK (Machine Learning Toolkit) `anomalydetection` command can automate baseline modeling for more sophisticated detection
Why this is asked: Dynamic thresholds are the step up from simple static alerts that production SRE teams need.

**Q7: `c003_dashboards_alerts_demo.py` uses a single `dashboard_metrics` function. How would you structure a Splunk dashboard with multiple panels that share a base search to avoid redundant index scans?**
What a good answer covers:
- Splunk's "post-processing searches" allow multiple panels to branch from one base saved search using `| search` filters on the shared result set
- Post-processing eliminates re-running the base SPL for each panel, reducing indexer load
- The trade-off: all panels are bound to the same time range and filter from the base search — panels needing different scopes must use separate searches
Why this is asked: Post-processing is a key dashboard optimization that reduces cost at scale.

**Q8: The demo triggers two independent alerts. In a production environment, how do you prevent alert fatigue when multiple correlated alerts fire simultaneously during an incident?**
What a good answer covers:
- Alert grouping and suppression: configure `throttle` to suppress re-firing for N minutes after the first trigger
- Use a correlation search (ES feature) or a parent alert that checks for co-occurring conditions before firing child alerts
- Route correlated alerts to an incident management tool (PagerDuty) with deduplication logic rather than sending raw Splunk alert emails
Why this is asked: Alert fatigue is a documented problem in operations; this tests the candidate's awareness of it.

### Level 3 — Senior

**Q9: `c003_dashboards_alerts_demo.py`'s `alert_checks` runs over all events in memory. How does Splunk Enterprise Security's correlation search framework differ from standard saved-search alerts, and when does the difference matter?**
What a good answer covers:
- ES correlation searches run against the Common Information Model (CIM) data model accelerations — they query pre-built summaries, not raw indexes, for speed
- ES produces "notable events" with risk scores rather than raw alerts — these feed into an investigation workflow with analyst assignment and status tracking
- Standard saved-search alerts are simpler and cheaper; ES correlation is appropriate for security/SIEM use cases requiring investigation workflows
Why this is asked: Distinguishes candidates with ES/SIEM exposure from those with only operational Splunk experience.

**Q10: The demo uses static Python functions. How would you design a Splunk monitoring architecture to detect when the alerting system itself is failing (e.g., scheduled searches not running, alert actions timing out)?**
What a good answer covers:
- Monitor the `_internal` index: `index=_internal sourcetype=scheduler` for `status=skipped` or `status=failed` events
- Create a watchdog alert on `index=_internal` that fires if the number of completed scheduled searches drops below expected
- Use Splunk's Health Report (Monitoring Console) to track scheduler skipped searches, indexer queue fill rates, and forwarder connectivity
Why this is asked: Self-monitoring of the observability platform is a senior-level operational concern.

**Q11: `c003_dashboards_alerts_demo.py` defines alerting in Python. How would you implement alert-as-code in Splunk (versioned, peer-reviewed, deployable), and what tooling supports this?**
What a good answer covers:
- Splunk objects (saved searches, alerts, dashboards) are stored as `.conf` files — these can be version-controlled in a Git repo and deployed via Splunk's REST API or `splunk btool`
- Tools like `pytest-splunk-addon` or Orca allow testing SPL correctness and alert logic in CI/CD pipelines
- Splunk Terraform provider (`splunk` provider) enables infrastructure-as-code for indexes, roles, and saved searches
Why this is asked: Treats Splunk configuration as software, which is essential for reliable, auditable production deployments.

### Level 4 — Architect

**Q12: `c003_dashboards_alerts_demo.py` computes metrics on the fly from raw events. How would you design a tiered observability architecture where Splunk dashboards and alerts are fed by pre-aggregated streams rather than raw log scans, and how does this connect to a streaming data platform?**
What a good answer covers:
- Pre-aggregate metrics in a streaming layer (Kafka Streams, Flink) before writing to Splunk via HEC — dashboard panels query summary indexes rather than raw events
- This decouples alerting latency from indexing lag and reduces Splunk compute cost for high-cardinality metrics
- Connecting to the streaming track: the streaming layer becomes the source of truth for real-time metrics; Splunk stores the enriched, aggregated events for historical analysis and compliance
- Trade-off: two systems increase operational complexity but enable sub-second alerting not possible with Splunk's 1-minute minimum scheduled search interval
Why this is asked: Tests architectural thinking about where computation belongs in a multi-tier observability stack.

**Q13: If dashboard adoption is low because query response times exceed 30 seconds on 30-day panels, walk through a full performance remediation plan for `c003_dashboards_alerts_demo.py`'s metrics at production scale.**
What a good answer covers:
- Instrument first: use `index=_internal sourcetype=scheduler` to identify which saved searches are slow and why (scan count, event count, dispatch time)
- Apply report acceleration on the underlying data model to pre-compute 30-day aggregations on a nightly schedule
- Replace full `stats` scans with `tstats` queries on indexed fields for panels that only need counts and sums
- Connecting to the data quality track: slow dashboards are often caused by unexpectedly high event volumes from a logging misconfiguration — add ingest volume monitoring as a leading indicator
Why this is asked: End-to-end performance remediation requires combining SPL knowledge, architecture, and data quality awareness.

---

## Log-Based Anomaly Detection

### Level 1 — Starter

**Q1: In `c004_log_anomaly_detection_demo.py`, the `detect_anomalies` function flags windows where requests drop below 60% of baseline or errors exceed 3x baseline. What SPL commands would you use to compute these same ratios from live Splunk data?**
What a good answer covers:
- `index=services | bucket _time span=5m | stats count as requests, count(eval(level="ERROR")) as errors by _time`
- Then: `| eval throughput_ratio=requests/100, error_ratio=errors/2 | where throughput_ratio < 0.6 OR error_ratio > 3`
- `timechart` could render the ratios over time; `where` filters for anomalous windows
Why this is asked: Verifies the candidate can lift the demo's Python logic directly into SPL.

**Q2: The demo uses fixed baselines (`BASELINE_REQUESTS = 100`, `BASELINE_ERRORS = 2`). What is the main weakness of static baselines for anomaly detection, and what is a simple alternative?**
What a good answer covers:
- Static baselines break during traffic growth, seasonal patterns (weekday vs. weekend), or after product launches
- A rolling average baseline: `| stats avg(requests) as baseline over the last N windows` adapts to drift
- Even a simple 7-day same-hour comparison is more robust than a hardcoded number
Why this is asked: Static vs. dynamic baselines is the foundational concept distinguishing basic from real anomaly detection.

**Q3: `c004_log_anomaly_detection_demo.py` detects two anomaly types: throughput drop and error spike. What additional signal types would you monitor in a production service, and why?**
What a good answer covers:
- Latency spike (p95/p99 degradation without volume change — indicates slow queries or dependency issues)
- Log volume drop per specific service (a silent crash with no errors, e.g., a service stops logging entirely)
- Cardinality explosion in a field (e.g., unique `order_id` values spike — indicates a fan-out bug or data leak)
Why this is asked: Shows whether the candidate thinks beyond the happy path of error and throughput signals.

**Q4: The demo processes 5-minute windows. In Splunk, how do you configure time bucketing for anomaly detection searches, and what trade-offs come with choosing bucket size?**
What a good answer covers:
- SPL `bucket _time span=5m` groups events into 5-minute windows for aggregation
- Smaller buckets increase detection sensitivity and reduce time-to-alert but increase false positive rate from statistical noise
- Larger buckets reduce noise but delay detection — for critical services, 1–5 minute buckets are typical; for trend analysis, hourly or daily buckets
Why this is asked: Bucket size is the primary tuning knob for detection sensitivity vs. false positive trade-off.

### Level 2 — Mid

**Q5: `c004_log_anomaly_detection_demo.py` applies the same thresholds to all services. How would you implement per-service baselines and thresholds in a Splunk search pipeline?**
What a good answer covers:
- Use a lookup table CSV (service, baseline_requests, baseline_errors) and join it to the aggregated results: `| lookup service_baselines service OUTPUT baseline_requests, baseline_errors`
- Then: `| eval throughput_anomaly=if(requests < baseline_requests*0.6, 1, 0)` per row
- The lookup can be updated automatically by a nightly baseline-recalculation search writing to a KV Store
Why this is asked: Per-entity thresholds are the standard pattern for production anomaly detection at scale.

**Q6: The demo flags anomalies as binary (present/absent). How would you implement severity scoring for anomalies in SPL so that a 50% drop is flagged differently from a 90% drop?**
What a good answer covers:
- Compute a deviation score: `| eval severity=round((baseline_requests - requests)/baseline_requests * 100, 1)`
- Bin the score into levels: `| eval severity_label=case(severity>=80, "CRITICAL", severity>=50, "HIGH", severity>=30, "MEDIUM", true(), "LOW")`
- Alert routing can use `severity_label` to direct critical anomalies to PagerDuty and medium ones to a Slack channel
Why this is asked: Severity scoring is a key step between binary detection and actionable alerting.

**Q7: `c004_log_anomaly_detection_demo.py` checks one metric at a time. How does multivariate anomaly detection differ, and what Splunk tools support it?**
What a good answer covers:
- Multivariate detection checks correlations between metrics — e.g., high latency + low throughput + high error rate together signal a different failure mode than any one alone
- Splunk MLTK's `anomalydetection` and `anomalousvalue` commands detect outliers across multiple fields simultaneously
- `cluster` command groups similar events, which can surface anomalous clusters that don't match normal patterns
Why this is asked: Tests awareness of Splunk's ML capabilities beyond simple threshold checks.

**Q8: The demo outputs anomaly records to a Python list. In Splunk, how would you store detected anomalies so they can be trended over time and queried retrospectively?**
What a good answer covers:
- Use the `collect` command to write anomaly events to a summary index: `| collect index=anomalies`
- Alternatively, use `outputlookup` to append to a KV Store for low-volume anomaly tracking
- The summary index approach allows SPL queries like `index=anomalies | timechart count by type` to trend anomaly frequency over weeks or months
Why this is asked: Persisting anomaly signals is essential for post-incident analysis and SLA reporting.

### Level 3 — Senior

**Q9: `c004_log_anomaly_detection_demo.py` uses hard-coded percentage thresholds. How does Splunk MLTK's `fit DensityFunction` or `fit IQR` approach differ, and what data characteristics make statistical models more appropriate than threshold rules?**
What a good answer covers:
- `fit DensityFunction` models the probability distribution of normal values and flags events outside a confidence interval — adapts automatically to the distribution shape
- IQR-based methods are distribution-agnostic and robust to outliers in the baseline period, suitable for metrics with heavy tails
- Statistical models are preferable when baseline values vary by time of day, day of week, or have long-term drift — threshold rules become unmaintainable in those cases
Why this is asked: Tests knowledge of when to graduate from rule-based to model-based anomaly detection.

**Q10: The demo operates on a 4-window dataset. How does the concept of seasonality affect anomaly detection in Splunk, and what techniques exist to account for it?**
What a good answer covers:
- Seasonality means expected values differ by time-of-day or day-of-week — a Monday morning traffic spike is normal but would fire on a Saturday
- Same-hour-of-day / same-day-of-week baselines: `earliest=-7d@h latest=-6d@h` subsearches create day-of-week-aware baselines
- Splunk MLTK's `StateSpaceForecast` algorithm models trend + seasonality components explicitly for time-series forecasting
Why this is asked: Seasonality handling is the most common failure mode of production anomaly detection systems.

**Q11: `c004_log_anomaly_detection_demo.py` detects anomalies but does not explain them. How would you build an automated root-cause analysis step in SPL that narrows down which service, endpoint, or user class is driving the anomaly?**
What a good answer covers:
- After detecting an anomaly window, drill down automatically: `| search _time=<anomaly_window> | stats count by service, endpoint | sort -count` to identify the top contributor
- Use the `anomalousvalue` command to identify which field values are disproportionately represented in the anomaly window vs. the baseline window
- For causal attribution, a subsearch compares error rates per dimension in the anomaly window vs. a prior normal window — the dimension with the largest lift is the candidate root cause
Why this is asked: Detection without attribution is operationally incomplete — root-cause automation is a senior-level capability.

### Level 4 — Architect

**Q12: `c004_log_anomaly_detection_demo.py` runs detection post-hoc over batched windows. How would you redesign this as a real-time streaming anomaly detection pipeline, and where does Splunk fit versus dedicated stream processing systems?**
What a good answer covers:
- Splunk's real-time searches are not true stream processing — they re-scan a sliding window every N seconds, introducing latency and compute cost
- A proper real-time detection pipeline uses Kafka Streams or Flink with stateful operators maintaining per-window running statistics, detecting anomalies in milliseconds
- Splunk's role in this architecture: receive the anomaly events emitted by the stream processor via HEC, store them for historical querying, and power dashboards — not do the detection itself
- Connecting to the streaming track: exactly-once semantics in the stream processor ensure anomaly events are not double-counted in Splunk's summary index
Why this is asked: Forces the candidate to define the right tool for the job and articulate Splunk's boundaries.

**Q13: The demo detects throughput drops that could indicate a silent service crash with no error logs. How would you design a cross-system health monitoring architecture that uses log signals from Splunk and infrastructure metrics from a time-series database to confirm or dismiss such anomalies?**
What a good answer covers:
- Log signal (Splunk): throughput drop detected in `index=services` → trigger enrichment lookup
- Infrastructure metric correlation: query Prometheus/Datadog for CPU, memory, and network metrics for the affected service during the anomaly window via a webhook alert action
- An automated enrichment script (Splunk Adaptive Response or SOAR integration) fetches correlated metrics and appends them to the notable event
- Connecting to the data quality track: a throughput drop may also indicate a logging pipeline failure (forwarder disconnected) rather than a service failure — the cross-system check disambiguates
Why this is asked: Cross-system correlation is the hallmark of mature observability architecture and requires integrating multiple data tracks.

---

## Splunk vs Elasticsearch

### Level 1 — Starter

**Q1: `c005_splunk_vs_elastic_demo.py` shows that Splunk uses Forwarders/HEC for ingestion while Elasticsearch uses Beats/Logstash. As a new engineer choosing a log analytics tool, what is the most important operational difference to understand about these two ingestion approaches?**
What a good answer covers:
- Splunk forwarders are purpose-built agents managed centrally via Deployment Server; Beats are lightweight open-source shippers with separate Logstash for transformation
- Splunk's ingestion pipeline is largely managed by the platform; Elasticsearch's pipeline requires more manual pipeline design (Logstash filters, ingest processors)
- Splunk's HEC is a simple HTTP API suitable for application-level log shipping; Elasticsearch has a comparable ingest API but schema mapping must be pre-configured
Why this is asked: Ingestion architecture is the first decision point when selecting a log platform.

**Q2: The comparison in `c005_splunk_vs_elastic_demo.py` notes that Splunk uses SPL while Elasticsearch uses DSL/Query APIs. For someone who knows SQL, which query language is easier to learn, and what are the trade-offs?**
What a good answer covers:
- SPL is pipeline-based and imperative — closer to Unix pipes than SQL; it has a gentle learning curve for filter+aggregate patterns but diverges from SQL for joins and subqueries
- Elasticsearch DSL is JSON-based and declarative — SQL-trained users often find it more familiar for structured queries but verbose for exploratory log analysis
- Elasticsearch supports an SQL compatibility layer (`_sql` API) that makes simple queries accessible; Splunk has no SQL mode
Why this is asked: Query language familiarity is a practical adoption concern that shapes team productivity.

**Q3: `c005_splunk_vs_elastic_demo.py` contrasts Splunk's hot/warm/cold buckets with Elasticsearch's indices/data streams. What does "schema-on-read" mean in the context of Splunk, and how does it differ from Elasticsearch's mapping-based "schema-on-write"?**
What a good answer covers:
- Splunk stores raw text (`_raw`) and defers field extraction until search time — you can define new fields retroactively without re-indexing
- Elasticsearch requires field mappings to be defined (or auto-detected) before indexing — changing a field type requires reindexing existing documents
- Schema-on-read is more flexible for exploratory log analysis; schema-on-write is more performant for known query patterns and strongly typed data
Why this is asked: This is the most architecturally significant difference between the two platforms.

**Q4: Based on `c005_splunk_vs_elastic_demo.py`'s use-case comparison, when would you recommend Elasticsearch over Splunk for a new log analytics project, and when would you choose Splunk?**
What a good answer covers:
- Choose Elasticsearch when: the team needs full-text search (product catalog, document search), has existing ELK/OpenSearch skills, or cost is a primary concern (open-source option)
- Choose Splunk when: the use case is SIEM/security operations, the team needs an all-in-one managed platform with minimal operational overhead, or compliance reporting is required
- Elasticsearch's open-source nature avoids Splunk's per-GB licensing cost but requires more operational investment
Why this is asked: Platform selection judgment is tested in senior interviews at organizations evaluating or migrating tooling.

### Level 2 — Mid

**Q5: `c005_splunk_vs_elastic_demo.py` shows both platforms support tiered storage. How does Splunk's SmartStore (S3-backed cold tier) compare to Elasticsearch's ILM (Index Lifecycle Management) with searchable snapshots, and what are the query latency implications?**
What a good answer covers:
- SmartStore caches recently accessed buckets locally and fetches cold data from S3 on demand — cold searches add S3 fetch latency
- Elasticsearch searchable snapshots allow querying frozen tier data directly from object storage with a local cache for repeated access
- Both solutions decouple compute from storage cost; Elasticsearch's tiered approach is more granular (hot/warm/cold/frozen) while Splunk's SmartStore primarily covers hot/cold
Why this is asked: Storage tiering directly affects the TCO argument when comparing the two platforms at scale.

**Q6: The demo notes Splunk's query model is "SPL search | filter | stats pipeline" while Elasticsearch uses "DSL/Query APIs with aggregations." For a data engineer building a log-based metrics pipeline, how does each platform's aggregation model affect the expressiveness of computed metrics?**
What a good answer covers:
- SPL's pipeline model makes multi-step transformations readable and composable — `stats`, `eval`, `where`, `timechart` chain naturally
- Elasticsearch's nested aggregations (bucket → metric → pipeline aggregations) are powerful but JSON-verbose; `derivative`, `moving_avg`, and `bucket_script` pipeline aggregations cover many SPL use cases
- SPL has richer built-in statistical functions (percentiles, anomaly detection) with simpler syntax; Elasticsearch's MLTK equivalent is Elastic ML, a separately licensed feature
Why this is asked: Aggregation expressiveness determines what kinds of metrics pipelines are feasible on each platform.

**Q7: `c005_splunk_vs_elastic_demo.py` lists SIEM as a primary Splunk use case. What specific capabilities make Splunk Enterprise Security more suitable for security operations than a standard Elasticsearch cluster, and what would be required to close that gap with Elasticsearch?**
What a good answer covers:
- Splunk ES provides out-of-the-box CIM normalization, correlation search framework, risk-based alerting, and investigation workflows (notable events, risk scores)
- Equivalent Elasticsearch setup requires: Elastic Security (licensed), custom pipelines for CIM-equivalent normalization, and significant SOAR integration work
- The operational burden of security-specific tuning is much lower in Splunk ES for teams without dedicated Elasticsearch security engineering resources
Why this is asked: SIEM is a dominant Splunk use case; knowing the competitive landscape is expected at mid-level.

**Q8: `c005_splunk_vs_elastic_demo.py` compares ingestion pipelines. How do the two platforms handle schema evolution when a new field is added to log events, and what are the operational risks of each approach?**
What a good answer covers:
- Splunk: new fields appear automatically at search time via key=value extraction — no migration needed; risk is that poorly named fields pollute the field namespace
- Elasticsearch: new fields trigger dynamic mapping if enabled (can cause mapping explosions from high-cardinality field names like UUIDs); explicit mappings require coordinated deployment
- Elasticsearch mapping conflicts (e.g., a field indexed as `integer` receiving `string` values) cause indexing failures; Splunk's equivalent is a silent extraction mismatch that returns no results
Why this is asked: Schema evolution handling is a critical operational concern in production log pipelines.

### Level 3 — Senior

**Q9: `c005_splunk_vs_elastic_demo.py` notes both platforms handle observability. How would you evaluate the two platforms for a use case requiring correlated log, metric, and trace analysis (full-stack observability), and what are the current gaps of each?**
What a good answer covers:
- Elasticsearch (via Elastic Observability): native APM with distributed tracing (OpenTelemetry), metrics via Elasticsearch time series, logs — all in one platform with correlation by trace ID
- Splunk Observability Cloud (formerly SignalFx): strong metrics and APM, but separate product from Splunk core — requires stitching log correlation manually via field-based joins
- Gap: neither platform natively handles all three signals at enterprise scale without significant licensing and configuration investment; OpenTelemetry Collector as a vendor-neutral pipeline is increasingly used to decouple signal collection from storage choice
Why this is asked: Full-stack observability is the evolving standard, and candidates should know the landscape.

**Q10: The demo's comparison uses static category labels. How do the licensing models of Splunk (per GB ingested) vs. Elasticsearch (per node/cluster or Elastic Cloud units) affect architecture decisions at scale, and what design patterns reduce cost for each?**
What a good answer covers:
- Splunk's per-GB model incentivizes reducing ingest volume: pre-aggregate in a streaming layer, drop debug logs at the forwarder, use `nullQueue` for high-volume noisy sources
- Elasticsearch's per-node model incentivizes right-sizing clusters: use frozen tier and searchable snapshots for cold data, tune shard counts to avoid over-provisioning
- Both platforms encourage summary index / rollup index patterns for long-term retention of aggregated metrics vs. raw events
Why this is asked: Cost architecture is a real concern that shapes ingest pipeline design at organizations with large log volumes.

**Q11: `c005_splunk_vs_elastic_demo.py` focuses on log analytics. How does the choice between Splunk and Elasticsearch interact with an organization's existing data platform (e.g., a Kafka-based streaming pipeline, a data warehouse), and what integration patterns minimize vendor lock-in?**
What a good answer covers:
- Both platforms can consume from Kafka (Splunk Kafka Connect add-on, Elasticsearch Kafka Connect or Logstash); Kafka as the central bus decouples log producers from the analytics store choice
- Using OpenTelemetry Collector as the shipping layer further decouples from both platforms — switch storage backends without changing application instrumentation
- Connecting to the streaming track: materializing pre-aggregated log metrics into a data warehouse (Snowflake, BigQuery) alongside Splunk/Elasticsearch enables long-term analytics without high per-GB log storage costs
Why this is asked: Vendor lock-in mitigation is an architect-level concern that requires cross-track thinking.

### Level 4 — Architect

**Q12: `c005_splunk_vs_elastic_demo.py` compares two platforms, but many organizations run both. How would you design a multi-platform observability architecture where Splunk handles security/compliance log retention and Elasticsearch handles application observability, without duplicating ingestion cost?**
What a good answer covers:
- Use a Kafka topic as the canonical log stream; deploy two consumer groups — one writing to Splunk HEC (security/compliance topics), one writing to Elasticsearch (application metrics/traces)
- Apply topic-level filtering to ensure compliance logs (authentication, privileged access) go only to Splunk; application debug logs go only to Elasticsearch
- Connecting to the streaming track: Kafka's consumer group model enables fan-out to multiple sinks with independent scaling and without duplicate ingest cost at the source
- Governance: data residency and retention policies differ between platforms — a central policy service (e.g., data contract registry) should enforce which events flow to each sink
Why this is asked: Multi-platform log routing is common at enterprise scale and requires streaming architecture knowledge.

**Q13: Given the trajectory of both platforms (Elastic moving upmarket into SIEM, Splunk moving into observability), how would you advise a CTO on a 5-year log analytics platform strategy that avoids being locked into either vendor's roadmap, while meeting current security, observability, and analytics requirements?**
What a good answer covers:
- Adopt OpenTelemetry as the universal instrumentation standard — it decouples signal generation from storage, enabling backend swaps without re-instrumenting applications
- Use a vendor-neutral streaming layer (Kafka or Apache Pulsar) as the log bus — storage backends become pluggable; migration is a consumer group configuration change
- Evaluate open-source alternatives (OpenSearch, ClickHouse for log analytics, Grafana Loki) for non-compliance workloads to reduce per-GB licensing exposure
- Connecting to the retrieval and analytics tracks: as log volumes grow, columnar storage (Parquet on S3 with Athena or BigQuery) becomes cost-competitive with both Splunk and Elasticsearch for historical analysis; the observability platform should be designed to export aggregated data to the warehouse rather than treating the log platform as the long-term analytics store
Why this is asked: Strategic platform thinking at the architect level requires connecting licensing, open standards, and cross-track data architecture.
\n---\n\n