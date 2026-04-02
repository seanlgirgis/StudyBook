# Story:
# One pipeline, many storage patterns: each stage exists for a reason.

import math
from collections import defaultdict


RAW_EVENTS = [
    {
        "event_id": "e1",
        "customer_id": 101,
        "customer_name": "Ava",
        "city": "Austin",
        "product": "laptop",
        "amount": 1200,
        "message": "need a lightweight laptop for travel",
    },
    {
        "event_id": "e2",
        "customer_id": 102,
        "customer_name": "Ben",
        "city": "Boston",
        "product": "headphones",
        "amount": 200,
        "message": "looking for noise canceling headphones",
    },
    {
        "event_id": "e3",
        "customer_id": 101,
        "customer_name": "Ava",
        "city": "Austin",
        "product": "laptop",
        "amount": 900,
        "message": "budget laptop recommendation",
    },
]


def _separator(title):
    print("=" * 72)
    print(title)


def ingest_events(events):
    return list(events)


def normalize_to_relational(events):
    customers = {}
    orders = []
    for event in events:
        customers[event["customer_id"]] = {
            "customer_id": event["customer_id"],
            "name": event["customer_name"],
            "city": event["city"],
        }
        orders.append(
            {
                "order_id": event["event_id"],
                "customer_id": event["customer_id"],
                "product": event["product"],
                "amount": event["amount"],
                "message": event["message"],
            }
        )
    return {"customers": list(customers.values()), "orders": orders}


def cache_hot_lookup(store, cache):
    key = 101
    if key in cache:
        return cache[key], "hit"
    customer = next(c for c in store["customers"] if c["customer_id"] == key)
    cache[key] = customer
    return customer, "miss"


def analytics_summary(store):
    totals = defaultdict(int)
    for order in store["orders"]:
        totals[order["customer_id"]] += order["amount"]
    return [{"customer_id": k, "total_spend": v} for k, v in sorted(totals.items())]


def build_search_index(store):
    index = defaultdict(set)
    for order in store["orders"]:
        for token in order["message"].lower().split():
            index[token].add(order["order_id"])
    return index


def _cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def vector_retrieval(store):
    # Tiny mock vectors: [laptop, audio, budget]
    vectors = {
        "e1": [1.0, 0.0, 0.2],
        "e2": [0.0, 1.0, 0.0],
        "e3": [1.0, 0.0, 1.0],
    }
    query = {"text": "budget laptop", "vector": [1.0, 0.0, 1.0]}
    scores = []
    for order in store["orders"]:
        sim = _cosine_similarity(query["vector"], vectors[order["order_id"]])
        scores.append((sim, order["order_id"], order["message"]))
    scores.sort(reverse=True)
    return query, scores


def queue_and_worker(store):
    queue = []
    for order in store["orders"]:
        queue.append(
            {
                "job_id": f"job-{order['order_id']}",
                "task": "notify_fulfillment",
                "payload": {"order_id": order["order_id"], "product": order["product"]},
            }
        )
    results = []
    for job in queue:
        results.append({"job_id": job["job_id"], "status": "done"})
    return queue, results


def run_pipeline():
    _separator("Raw input (ingest)")
    ingested = ingest_events(RAW_EVENTS)
    for row in ingested:
        print(row)

    _separator("Relational store (normalized tables)")
    store = normalize_to_relational(ingested)
    print("customers:", store["customers"])
    print("orders:", store["orders"])

    _separator("Cache lookup (hot customer)")
    cache = {}
    customer, status = cache_hot_lookup(store, cache)
    print(f"cache {status} ->", customer)
    customer, status = cache_hot_lookup(store, cache)
    print(f"cache {status} ->", customer)

    _separator("Analytics summary (total spend per customer)")
    summary = analytics_summary(store)
    for row in summary:
        print(row)

    _separator("Search index (keyword -> order ids)")
    index = build_search_index(store)
    for term in ["laptop", "budget", "noise"]:
        print(f"{term}: {sorted(index.get(term, set()))}")

    _separator("Vector-style retrieval (semantic similarity)")
    query, scored = vector_retrieval(store)
    print("query:", query["text"], "| vector:", query["vector"])
    for sim, order_id, message in scored:
        print(f"{order_id} similarity={sim:.3f} | {message}")

    _separator("Queue + worker processing")
    queue, results = queue_and_worker(store)
    print("queue:", queue)
    print("worker results:", results)

    _separator("System view")
    print("- Ingest: raw events arriving from apps or logs.")
    print("- Relational store: normalized truth for customers and orders.")
    print("- Cache: hot customer lookup to avoid repeated DB hits.")
    print("- Analytics: aggregate totals for reporting.")
    print("- Search index: keyword lookup for support queries.")
    print("- Vector retrieval: semantic search by meaning.")
    print("- Queue/worker: async tasks like fulfillment notifications.")


if __name__ == "__main__":
    run_pipeline()

# Takeaway:
# Polyglot systems connect to serve different access patterns.
