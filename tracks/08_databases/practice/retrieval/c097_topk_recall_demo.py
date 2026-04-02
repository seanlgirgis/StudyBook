# Story:
# Top-k gates candidates. Recall@k checks if the right docs survived.

import re


DOCS = {
    1: "xr15 refund denied escalation",
    2: "refund policy overview",
    3: "xr15 refund approved",
    4: "refund denied for xr15 after warranty expired",
    5: "chargeback dispute process",
    6: "xr15 return shipping label",
    7: "refund denied for xr99 headset",
    8: "xr15 refund denied appeal",
}

QUERY = "xr15 refund denied"
RELEVANT = {1, 4, 8}
K_VALUES = [1, 3, 5]


def _tokenize(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def overlap_score(query, doc):
    q = set(_tokenize(query))
    d = set(_tokenize(doc))
    return len(q & d)


def rank(scores):
    return sorted(scores.items(), key=lambda item: item[1], reverse=True)


def recall_at_k(top_k, relevant):
    hits = len(set(top_k) & relevant)
    return hits / len(relevant)


def run_topk_recall_demo():
    print("=" * 72)
    print("Query:", QUERY)

    print("=" * 72)
    print("Corpus:")
    for doc_id, text in DOCS.items():
        print(f"Doc {doc_id}: {text}")

    scores = {doc_id: overlap_score(QUERY, text) for doc_id, text in DOCS.items()}

    print("=" * 72)
    print("Full first-pass ranking:")
    ranked = rank(scores)
    for doc_id, score in ranked:
        print(f"Doc {doc_id} score={score}: {DOCS[doc_id]}")

    print("=" * 72)
    print("Relevant doc ids (ground truth):", sorted(RELEVANT))

    for k in K_VALUES:
        print("=" * 72)
        print(f"Top-k={k}")
        top_k = [doc_id for doc_id, _ in ranked[:k]]
        survived = sorted(set(top_k) & RELEVANT)
        missed = sorted(RELEVANT - set(top_k))
        recall = recall_at_k(top_k, RELEVANT)
        print("Top-k ids:", top_k)
        print(f"Recall@{k}: {recall:.2f}")
        print("Relevant survived:", survived)
        print("Relevant missed:", missed)

    print("=" * 72)
    print("Interpretation:")
    print("- Top-k is a gate: smaller k drops relevant docs faster.")
    print("- Recall@k rises as k grows, giving rerankers more to work with.")
    print("- Any relevant doc outside top-k is invisible to reranking.")


if __name__ == "__main__":
    run_topk_recall_demo()

# Takeaway:
# Top-k is a system design choice. Recall@k measures survival.
