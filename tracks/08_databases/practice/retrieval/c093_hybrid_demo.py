# Story:
# Hybrid retrieval blends exact word match with semantic similarity.
# This demo shows why the combination is stronger than either alone.

import math
import re


DOCS = {
    1: {
        "text": "xr15 headset refund form",
        "vector": [0.4, 0.9, 0.2, 0.0, 0.0],
    },
    2: {
        "text": "returning a broken audio device",
        "vector": [0.85, 0.4, 0.9, 0.0, 0.0],
    },
    3: {
        "text": "refund policy for accessories",
        "vector": [0.9, 0.0, 0.0, 0.0, 0.0],
    },
    4: {
        "text": "shipping delay status update",
        "vector": [0.0, 0.0, 0.0, 0.9, 0.0],
    },
    5: {
        "text": "update your account email",
        "vector": [0.0, 0.0, 0.0, 0.0, 0.9],
    },
    6: {
        "text": "xr15 battery replacement guide",
        "vector": [0.05, 0.85, 0.05, 0.0, 0.0],
    },
}

# Vector dimensions (intuition only):
# [refunds, product, damage, shipping, account]

QUERY_TEXT = "refund xr15 headset"
QUERY_VECTOR = [0.9, 0.7, 0.8, 0.0, 0.0]

KEYWORD_WEIGHT = 0.3
VECTOR_WEIGHT = 0.7


def _tokenize(text):
    return re.findall(r"[a-z0-9]+", text.lower())


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


def rank(scores):
    return sorted(scores.items(), key=lambda item: item[1], reverse=True)


def run_hybrid_demo():
    print("=" * 72)
    print("Query:", QUERY_TEXT)
    print("Query vector:", QUERY_VECTOR)

    print("=" * 72)
    print("Documents and vectors:")
    for doc_id, doc in DOCS.items():
        print(f"Doc {doc_id}: {doc['text']} -> {doc['vector']}")

    overlaps = {doc_id: keyword_overlap(QUERY_TEXT, doc["text"]) for doc_id, doc in DOCS.items()}
    max_overlap = max(overlaps.values()) or 1

    keyword_scores = {}
    vector_scores = {}
    hybrid_scores = {}

    for doc_id, doc in DOCS.items():
        overlap = overlaps[doc_id]
        keyword_scores[doc_id] = overlap
        vector_scores[doc_id] = cosine_similarity(QUERY_VECTOR, doc["vector"])
        keyword_norm = overlap / max_overlap
        hybrid_scores[doc_id] = (KEYWORD_WEIGHT * keyword_norm) + (
            VECTOR_WEIGHT * vector_scores[doc_id]
        )

    print("=" * 72)
    print("Per-document scores:")
    for doc_id, doc in DOCS.items():
        print(
            f"Doc {doc_id} keyword={keyword_scores[doc_id]} "
            f"vector={vector_scores[doc_id]:.3f} "
            f"hybrid={hybrid_scores[doc_id]:.3f} | {doc['text']}"
        )

    print("=" * 72)
    print("Scenario A: Keyword-only ranking (exact words)")
    for doc_id, score in rank(keyword_scores):
        print(f"Doc {doc_id} keyword={score}: {DOCS[doc_id]['text']}")

    print("=" * 72)
    print("Scenario B: Vector-only ranking (meaning)")
    for doc_id, score in rank(vector_scores):
        print(f"Doc {doc_id} vector={score:.3f}: {DOCS[doc_id]['text']}")

    print("=" * 72)
    print("Scenario C: Hybrid ranking (best practical blend)")
    for doc_id, score in rank(hybrid_scores):
        print(f"Doc {doc_id} hybrid={score:.3f}: {DOCS[doc_id]['text']}")

    print("=" * 72)
    print("Scenario D: Unrelated docs stay low")
    for doc_id in [4, 5]:
        print(
            f"Doc {doc_id} keyword={keyword_scores[doc_id]} "
            f"vector={vector_scores[doc_id]:.3f} "
            f"hybrid={hybrid_scores[doc_id]:.3f} | {DOCS[doc_id]['text']}"
        )

    print("=" * 72)
    print("Interpretation:")
    print("- Keyword-only puts Doc 1 first because it matches 'xr15' and 'refund'.")
    print("- Vector-only puts Doc 2 first because it is a semantic match with no exact overlap.")
    print("- Hybrid keeps Doc 1 on top, boosts Doc 2 above generic policy, and leaves unrelated docs low.")


if __name__ == "__main__":
    run_hybrid_demo()

# Takeaway:
# Exact words and meaning are both useful signals. Hybrid blends them.
