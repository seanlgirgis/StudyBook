# Story:
# Metadata filtering removes invalid candidates before ranking.
# This demo shows why ranking alone can be wrong.

import re


DOCS = {
    1: {
        "text": "xr15 headset return form",
        "meta": {"product": "xr15", "region": "US", "status": "open"},
    },
    2: {
        "text": "refund xr15 headset policy",
        "meta": {"product": "xr15", "region": "EU", "status": "open"},
    },
    3: {
        "text": "refund request for xr99 headset",
        "meta": {"product": "xr99", "region": "US", "status": "open"},
    },
    4: {
        "text": "returning a broken audio device",
        "meta": {"product": "xr15", "region": "US", "status": "closed"},
    },
    5: {
        "text": "xr15 shipping delay update",
        "meta": {"product": "xr15", "region": "US", "status": "open"},
    },
    6: {
        "text": "account email change request",
        "meta": {"product": "account", "region": "US", "status": "open"},
    },
}

QUERY_TEXT = "refund xr15 headset"
FILTERS = {"product": "xr15", "region": "US", "status": "open"}


def _tokenize(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def keyword_overlap(query, doc):
    q = set(_tokenize(query))
    d = set(_tokenize(doc))
    return len(q & d)


def rank(scores):
    return sorted(scores.items(), key=lambda item: item[1], reverse=True)


def apply_filters(docs, filters):
    candidates = []
    for doc_id, doc in docs.items():
        if all(doc["meta"].get(key) == value for key, value in filters.items()):
            candidates.append(doc_id)
    return candidates


def run_metadata_filtering_demo():
    print("=" * 72)
    print("Query:", QUERY_TEXT)
    print("Filters:", FILTERS)

    print("=" * 72)
    print("Documents and metadata:")
    for doc_id, doc in DOCS.items():
        print(f"Doc {doc_id}: {doc['text']} | meta={doc['meta']}")

    scores = {doc_id: keyword_overlap(QUERY_TEXT, doc["text"]) for doc_id, doc in DOCS.items()}

    print("=" * 72)
    print("Scores before filtering:")
    for doc_id, score in scores.items():
        print(f"Doc {doc_id} score={score}: {DOCS[doc_id]['text']}")

    print("=" * 72)
    print("Scenario A: Ranking without filtering (can be wrong)")
    for doc_id, score in rank(scores):
        print(f"Doc {doc_id} score={score}: {DOCS[doc_id]['text']}")

    print("=" * 72)
    print("Scenario B: Filtered candidate set")
    candidates = apply_filters(DOCS, FILTERS)
    print("Candidates:", candidates)

    print("=" * 72)
    print("Scenario C: Ranking after filtering (correct context)")
    filtered_scores = {doc_id: scores[doc_id] for doc_id in candidates}
    for doc_id, score in rank(filtered_scores):
        print(f"Doc {doc_id} score={score}: {DOCS[doc_id]['text']}")

    print("=" * 72)
    print("Scenario D: Over-filtering risk")
    strict_filters = {"product": "xr15", "region": "US", "status": "pending"}
    strict_candidates = apply_filters(DOCS, strict_filters)
    print("Strict filters:", strict_filters)
    print("Candidates:", strict_candidates)

    print("=" * 72)
    print("Interpretation:")
    print("- Without filtering, Doc 2 ranks first but is invalid for region=US.")
    print("- Filtering removes invalid docs before ranking, so Doc 1 surfaces correctly.")
    print("- Over-filtering can drop all results even if good matches exist.")


if __name__ == "__main__":
    run_metadata_filtering_demo()

# Takeaway:
# Filter first by constraints, then rank what remains.
