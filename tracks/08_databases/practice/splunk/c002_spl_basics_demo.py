# Story:
# A Splunk user searches an index, filters events, and runs basic stats.

EVENTS = [
    {"index": "orders", "level": "INFO", "service": "checkout", "status": "created"},
    {"index": "orders", "level": "ERROR", "service": "payments", "status": "declined"},
    {"index": "orders", "level": "INFO", "service": "checkout", "status": "paid"},
    {"index": "orders", "level": "WARN", "service": "payments", "status": "retry"},
]


def search(events, **criteria):
    results = []
    for event in events:
        if all(event.get(k) == v for k, v in criteria.items()):
            results.append(event)
    return results


def stats_count_by(events, field):
    counts = {}
    for event in events:
        key = event.get(field, "(missing)")
        counts[key] = counts.get(key, 0) + 1
    return counts


def run_spl_basics_demo():
    print("=" * 72)
    print("Scenario: SPL basics")

    print("\nStep 1: Select index=orders")
    index_events = search(EVENTS, index="orders")
    for event in index_events:
        print(f"  {event}")

    print("\nStep 2: Filter level=ERROR")
    errors = search(index_events, level="ERROR")
    for event in errors:
        print(f"  {event}")

    print("\nStep 3: Stats count by service")
    counts = stats_count_by(index_events, "service")
    print(counts)

    print("\nSummary")
    print("- SPL starts with index selection.")
    print("- Filters narrow to events of interest.")
    print("- Stats summarize counts by a field.")


if __name__ == "__main__":
    run_spl_basics_demo()

# Takeaway: SPL chains search + filter + stats to explore logs.
