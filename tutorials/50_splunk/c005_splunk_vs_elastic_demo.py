# Story:
# Compare Splunk and Elasticsearch at a high level for log analytics.

COMPARISON = [
    {
        "category": "Ingestion",
        "splunk": "Forwarders/HEC send raw logs; indexing happens automatically.",
        "elastic": "Beats/Logstash ship data; pipelines enrich before indexing.",
    },
    {
        "category": "Indexing",
        "splunk": "Events go into indexes with metadata + raw text.",
        "elastic": "Documents indexed into shards with mappings.",
    },
    {
        "category": "Query",
        "splunk": "SPL search | filter | stats pipeline.",
        "elastic": "DSL/Query APIs with aggregations.",
    },
    {
        "category": "Storage",
        "splunk": "Hot/warm/cold buckets with time-based retention.",
        "elastic": "Indices/data streams with tiered storage.",
    },
    {
        "category": "Use Cases",
        "splunk": "Ops monitoring, SIEM, log analytics dashboards.",
        "elastic": "Search, observability, log analytics, APM.",
    },
]


def run_splunk_vs_elastic_demo():
    print("=" * 72)
    print("Scenario: Splunk vs Elasticsearch comparison")

    for row in COMPARISON:
        print(f"\n{row['category']}")
        print(f"  Splunk: {row['splunk']}")
        print(f"  Elastic: {row['elastic']}")

    print("\nSummary")
    print("- Splunk emphasizes SPL pipelines over indexed events.")
    print("- Elasticsearch uses document indices and DSL queries.")
    print("- Both support observability and log analytics.")


if __name__ == "__main__":
    run_splunk_vs_elastic_demo()

# Takeaway: Splunk and Elasticsearch solve similar problems with different models.
