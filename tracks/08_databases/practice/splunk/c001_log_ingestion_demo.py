# Story:
# Raw logs are ingested, parsed into fields, and indexed for search.

RAW_LOGS = [
    "2026-03-27T12:00:01Z level=INFO service=checkout msg=order_created order_id=o100",
    "2026-03-27T12:00:05Z level=ERROR service=payments msg=card_declined order_id=o101",
    "2026-03-27T12:00:09Z level=INFO service=checkout msg=order_paid order_id=o100",
]


def parse_log(line):
    parts = line.split(" ")
    record = {"_raw": line, "timestamp": parts[0]}
    for token in parts[1:]:
        if "=" in token:
            key, value = token.split("=", 1)
            record[key] = value
    return record


def index_events(records, index_name):
    indexed = []
    for record in records:
        record["index"] = index_name
        indexed.append(record)
    return indexed


def search(indexed, **criteria):
    results = []
    for record in indexed:
        if all(record.get(k) == v for k, v in criteria.items()):
            results.append(record)
    return results


def run_splunk_ingest_demo():
    print("=" * 72)
    print("Scenario: log ingestion and indexing concepts")

    print("\nIngest raw logs")
    for line in RAW_LOGS:
        print(f"  {line}")

    parsed = [parse_log(line) for line in RAW_LOGS]
    indexed = index_events(parsed, "orders")

    print("\nParsed + indexed events")
    for event in indexed:
        print(f"  {event}")

    print("\nSearch: index=orders level=ERROR")
    results = search(indexed, index="orders", level="ERROR")
    for event in results:
        print(f"  {event}")

    print("\nSummary")
    print("- Ingestion takes raw logs into the system.")
    print("- Parsing extracts fields for search.")
    print("- Indexing assigns events to an index for fast queries.")


if __name__ == "__main__":
    run_splunk_ingest_demo()

# Takeaway: Splunk ingests raw logs, parses fields, and indexes events for search.
