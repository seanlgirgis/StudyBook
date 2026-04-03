"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 00-01 · Seed Lab Environment                                         ║
║  Creates Kafka topics and seeds deterministic events for all nuggets.        ║
║  IDEMPOTENT — safe to run multiple times.                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
1. Creates required Kafka topics
2. Seeds deterministic clickstream/order events
3. Provides reset script to clean lab state

USAGE
─────
    python 01_seed_lab.py          # Create topics + seed data
    python 01_seed_lab.py --reset   # Clean lab state only
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _spark_stream_connect import (
    create_kafka_topics, produce_kafka_messages,
    clean_lab, ensure_lab_dirs, LAB_DATA, TOPICS, KAFKA_BOOTSTRAP,
)


def generate_events(n: int = 200, seed: int = 42) -> list[bytes]:
    """Generate deterministic clickstream events as JSON bytes."""
    random.seed(seed)
    users = [f"user_{i:03d}" for i in range(1, 21)]
    pages = ["/home", "/products", "/product/1", "/product/2", "/cart", "/checkout", "/confirm"]
    event_types = ["page_view", "product_view", "add_to_cart", "checkout", "purchase"]
    devices = ["desktop", "mobile", "tablet"]

    base_time = datetime(2024, 1, 15, 10, 0, 0)
    events = []
    for i in range(n):
        ts = base_time + timedelta(seconds=i * 30 + random.randint(0, 10))
        event = {
            "event_id": f"evt_{i:05d}",
            "user_id": random.choice(users),
            "event_type": random.choices(event_types, weights=[0.4, 0.25, 0.15, 0.1, 0.1], k=1)[0],
            "page": random.choice(pages),
            "event_time": ts.isoformat(),
            "device": random.choice(devices),
            "amount": round(random.uniform(10, 500), 2) if random.random() > 0.7 else 0,
        }
        events.append(json.dumps(event).encode("utf-8"))
    return events


def main():
    parser = argparse.ArgumentParser(description="Seed Spark streaming lab environment.")
    parser.add_argument("--reset", action="store_true", help="Clean lab state only.")
    args = parser.parse_args()

    print("\n── Seed Lab Environment ──────────────────────────")

    if args.reset:
        print("\n  Resetting lab state...")
        clean_lab()
        print("  Lab state cleaned.")
        return

    ensure_lab_dirs()

    # 1. Create Kafka topics
    print("\n  Creating Kafka topics...")
    try:
        created = create_kafka_topics()
        if created > 0:
            print(f"    Created {created} topics")
        else:
            print("    All topics already exist")
    except Exception as e:
        print(f"    [!] Topic creation skipped: {e}")
        print("    (Kafka may not be running — nuggets will still work with file-based tests)")

    # 2. Seed events to lab_input topic
    print("\n  Seeding events to Kafka...")
    events = generate_events(200)
    try:
        produce_kafka_messages("lab_input", events)
        print(f"    Produced {len(events)} events to 'lab_input' topic")
    except Exception as e:
        print(f"    [!] Kafka produce failed: {e}")
        print("    Saving events to local file for file-based nuggets...")
        events_file = LAB_DATA / "seeded_events.jsonl"
        with open(events_file, "w") as f:
            for e in events:
                f.write(e.decode("utf-8") + "\n")
        print(f"    Saved {len(events)} events to {events_file}")

    # 3. Save seed data as JSON for offline nuggets
    print("\n  Saving seed data for offline tests...")
    events_file = LAB_DATA / "seeded_events.jsonl"
    if not events_file.exists():
        with open(events_file, "w") as f:
            for e in events:
                f.write(e.decode("utf-8") + "\n")
    print(f"    Seed data: {events_file} ({len(events)} events)")

    print("\n  Lab environment ready!")
    print(f"  Kafka: {KAFKA_BOOTSTRAP}")
    print(f"  Topics: {', '.join(TOPICS.keys())}")
    print()


if __name__ == "__main__":
    main()
