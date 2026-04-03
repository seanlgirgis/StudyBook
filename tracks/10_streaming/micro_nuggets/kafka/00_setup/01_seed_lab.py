"""
+==============================================================================+
|  NUGGET 00-01 . Seed Lab                                                     |
|  Create all lab topics and seed starter messages.                            |
+==============================================================================+

PURPOSE
-------
  - Create all topics used by the Kafka micro-nugget lane.
  - Seed realistic sample events into each topic.
  - Idempotent: safe to re-run (existing topics are not recreated).

TOPICS CREATED
--------------
  lab.raw.events      3 partitions  -- raw clickstream/IoT style events
  lab.clean.events    3 partitions  -- deduplicated clean events
  lab.agg.gold        1 partition   -- aggregated analytical output
  lab.reliability.test 2 partitions -- reliability pattern demos
  lab.dlq             1 partition   -- dead-letter queue
  lab.orders          4 partitions  -- keyed order events (key = user_id)
  lab.clickstream     3 partitions  -- web clickstream events
  lab.bronze          3 partitions  -- mini-capstone bronze layer
  lab.silver          3 partitions  -- mini-capstone silver layer
  lab.gold            1 partition   -- mini-capstone gold layer

TOPIC CONCEPTS
--------------
  Partition: an ordered, immutable sequence of records within a topic.
  Replication factor: how many broker copies exist. 1 = no redundancy (fine
    for local lab with single-broker Docker setup).
  Offset: position of a record within a partition (monotonically increasing).

USAGE
-----
    python 01_seed_lab.py

    Safe to re-run -- existing topics are skipped, existing messages remain.
"""
from __future__ import annotations

import json
import sys
import time
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _kafka_connect import BROKER, LAB_TOPICS, ensure_topics, require_broker

require_broker(BROKER)

print("\n-- Kafka Lab Seed --")
print(f"  Broker: {BROKER}")
print()

# -----------------------------------------------------------------------------
# 1. Create topics
# -----------------------------------------------------------------------------
print("  Creating topics (idempotent) ...")
from kafka import KafkaAdminClient, KafkaConsumer
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError

admin = KafkaAdminClient(bootstrap_servers=BROKER, request_timeout_ms=15_000)
existing = set(KafkaConsumer(bootstrap_servers=BROKER, consumer_timeout_ms=2_000).topics())

created = []
skipped = []
for name, cfg in LAB_TOPICS.items():
    if name in existing:
        skipped.append(name)
        continue
    try:
        admin.create_topics([
            NewTopic(
                name=name,
                num_partitions=cfg["num_partitions"],
                replication_factor=cfg["replication_factor"],
            )
        ])
        created.append(name)
    except TopicAlreadyExistsError:
        skipped.append(name)

admin.close()

for t in created:
    print(f"    [CREATED] {t}  ({LAB_TOPICS[t]['num_partitions']}p x {LAB_TOPICS[t]['replication_factor']}r)")
for t in skipped:
    print(f"    [EXISTS]  {t}")

print()

# -----------------------------------------------------------------------------
# 2. Seed messages
# -----------------------------------------------------------------------------
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=BROKER,
    acks="all",
    compression_type="gzip",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda k: k.encode("utf-8") if isinstance(k, str) else k,
    request_timeout_ms=15_000,
)


def send(topic: str, key: str | None, value: dict) -> None:
    producer.send(topic, key=key, value=value)


print("  Seeding starter messages ...")

# -- lab.raw.events: sensor / IoT-style events
users = ["alice", "bob", "carol", "dave", "eve"]
actions = ["page_view", "click", "purchase", "add_to_cart", "search"]
pages = ["/home", "/products", "/checkout", "/search", "/account"]
ts_base = int(time.time()) - 300  # start 5 min ago

raw_count = 0
for i in range(30):
    user = users[i % len(users)]
    event = {
        "event_id": str(uuid.uuid4()),
        "user_id": user,
        "action": actions[i % len(actions)],
        "page": pages[i % len(pages)],
        "ts": ts_base + i * 10,
        "session_id": f"sess_{user}_{(i // 5)}",
        "amount": round(9.99 + i * 2.5, 2) if actions[i % len(actions)] == "purchase" else None,
    }
    send("lab.raw.events", key=user, value=event)
    raw_count += 1

# -- lab.orders: keyed order events
for i in range(20):
    user = users[i % len(users)]
    order = {
        "order_id": f"ORD-{1000 + i}",
        "user_id": user,
        "product": f"PROD-{(i % 8) + 1}",
        "quantity": (i % 4) + 1,
        "price": round(14.99 + i * 3.0, 2),
        "status": "placed",
        "ts": ts_base + i * 15,
    }
    send("lab.orders", key=user, value=order)

# -- lab.clickstream: web clicks
for i in range(20):
    user = users[i % len(users)]
    click = {
        "event_id": str(uuid.uuid4()),
        "user_id": user,
        "url": f"https://shop.example.com{pages[i % len(pages)]}",
        "referrer": "https://google.com" if i % 3 == 0 else None,
        "ts": ts_base + i * 8,
        "device": "mobile" if i % 2 == 0 else "desktop",
    }
    send("lab.clickstream", key=user, value=click)

# -- lab.bronze: raw pipeline events for mini-capstone
for i in range(25):
    user = users[i % len(users)]
    event = {
        "event_id": str(uuid.uuid4()),
        "user_id": user,
        "event_type": actions[i % len(actions)],
        "payload": {"page": pages[i % len(pages)], "idx": i},
        "ingest_ts": ts_base + i * 12,
        "source": "web",
    }
    send("lab.bronze", key=user, value=event)

# -- lab.reliability.test: messages for reliability pattern demos
for i in range(10):
    msg = {
        "msg_id": str(uuid.uuid4()),
        "seq": i,
        "ts": ts_base + i * 5,
        "payload": f"test_payload_{i}",
    }
    send("lab.reliability.test", key=None, value=msg)

producer.flush()
producer.close()

print(f"    [OK] lab.raw.events     -- {raw_count} events seeded")
print(f"    [OK] lab.orders         -- 20 order events seeded")
print(f"    [OK] lab.clickstream    -- 20 click events seeded")
print(f"    [OK] lab.bronze         -- 25 pipeline events seeded")
print(f"    [OK] lab.reliability.test -- 10 test messages seeded")
print(f"    [OK] lab.dlq / lab.clean.events / lab.agg.gold / lab.silver / lab.gold")
print(f"         (created but not seeded -- populated by nuggets)")
print()
print("  Seed complete. Topics and starter data are ready.")
print("  View topics at http://localhost:8080 (Kafka UI)")
print()
