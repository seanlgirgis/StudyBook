# Story:
# A lakehouse table keeps snapshots. Time travel reads older snapshots safely.

SNAPSHOTS = {
    1: [
        {"order_id": "o100", "amount": 120.5},
        {"order_id": "o101", "amount": 85.0},
    ],
    2: [
        {"order_id": "o100", "amount": 120.5},
        {"order_id": "o101", "amount": 90.0},
        {"order_id": "o102", "amount": 42.0},
    ],
}


def read_snapshot(version):
    return SNAPSHOTS.get(version, [])


def run_time_travel_demo():
    print("=" * 72)
    print("Scenario: time travel queries")

    print("\nCurrent snapshot (v2)")
    current = read_snapshot(2)
    for row in current:
        print(f"  {row}")

    print("\nTime travel to snapshot v1")
    past = read_snapshot(1)
    for row in past:
        print(f"  {row}")

    print("\nSummary")
    print("- Snapshots capture table versions over time.")
    print("- Time travel reads older snapshots without changing current data.")


if __name__ == "__main__":
    run_time_travel_demo()

# Takeaway: Snapshot-based queries retrieve past table states safely.
