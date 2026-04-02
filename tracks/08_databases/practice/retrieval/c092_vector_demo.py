# Story:
# Vector retrieval finds items by meaning, not exact words.
# This demo uses hand-crafted vectors to show semantic similarity.

import math


DOCS = {
    1: {
        "text": "buy cheap laptop",
        "vector": [0.9, 0.7, 0.0, 0.0, 0.0],
    },
    2: {
        "text": "affordable notebook computer",
        "vector": [0.85, 0.75, 0.0, 0.0, 0.0],
    },
    3: {
        "text": "weather in texas",
        "vector": [0.0, 0.0, 0.95, 0.0, 0.0],
    },
    4: {
        "text": "database partition key",
        "vector": [0.0, 0.2, 0.0, 0.9, 0.0],
    },
    5: {
        "text": "movie soundtrack mood",
        "vector": [0.0, 0.0, 0.0, 0.0, 0.9],
    },
}

# Vector dimensions (intuition only):
# [shopping, computing, weather, databases, entertainment]


def _tokenize(text):
    return text.lower().split()


def keyword_overlap(query, doc):
    q = set(_tokenize(query))
    d = set(_tokenize(doc))
    return len(q & d)


def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def run_vector_demo():
    query_text = "budget laptop deal"
    query_vector = [0.88, 0.72, 0.0, 0.0, 0.0]

    print("=" * 72)
    print("Query:", query_text)
    print("Query vector:", query_vector)

    print("=" * 72)
    print("Documents and vectors:")
    for doc_id, doc in DOCS.items():
        print(f"Doc {doc_id}: {doc['text']} -> {doc['vector']}")

    print("=" * 72)
    print("Scenario A: Keyword overlap vs semantic similarity")
    for doc_id, doc in DOCS.items():
        overlap = keyword_overlap(query_text, doc["text"])
        sim = cosine_similarity(query_vector, doc["vector"])
        print(f"Doc {doc_id} overlap={overlap} similarity={sim:.3f} | {doc['text']}")

    print("=" * 72)
    print("Scenario B: Nearest neighbors (ranked)")
    scores = []
    for doc_id, doc in DOCS.items():
        sim = cosine_similarity(query_vector, doc["vector"])
        scores.append((sim, doc_id))
    scores.sort(reverse=True)
    for sim, doc_id in scores:
        print(f"Doc {doc_id} similarity={sim:.3f}: {DOCS[doc_id]['text']}")

    print("=" * 72)
    print("Scenario C: Unrelated docs score low")
    for doc_id in [3, 4]:
        sim = cosine_similarity(query_vector, DOCS[doc_id]["vector"])
        print(f"Doc {doc_id} similarity={sim:.3f}: {DOCS[doc_id]['text']}")


if __name__ == "__main__":
    run_vector_demo()

# Takeaway:
# Semantic neighbors can rank high even without exact word overlap.
