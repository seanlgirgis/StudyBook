# Story:
# Reranking uses a cheap first pass to get candidates, then a smarter second pass to reorder.

import re


DOCS = {
    1: "xr15 refund denied escalation",
    2: "refund policy overview",
    3: "xr15 refund approved",
    4: "refund rejected for xr15 after warranty expired",
    5: "chargeback dispute process",
    6: "xr15 return shipping label",
    7: "xr15 refund rejected appeal",
}

QUERY = "xr15 refund denied"
TOP_K = 3


def _tokenize(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def overlap_score(query, doc):
    q = set(_tokenize(query))
    d = set(_tokenize(doc))
    return len(q & d)


def reranker_score(doc):
    tokens = set(_tokenize(doc))
    score = 0.0
    if "xr15" in tokens:
        score += 2.0
    if "refund" in tokens:
        score += 1.0
    if "denied" in tokens:
        score += 2.5
    if "rejected" in tokens:
        score += 2.0
    if "refund" in tokens and ("denied" in tokens or "rejected" in tokens):
        score += 1.5
    if "warranty" in tokens:
        score += 1.0
    if "policy" in tokens:
        score -= 0.5
    return score


def rank(scores):
    return sorted(scores.items(), key=lambda item: item[1], reverse=True)


def run_reranking_demo():
    print("=" * 72)
    print("Query:", QUERY)

    print("=" * 72)
    print("Corpus:")
    for doc_id, text in DOCS.items():
        print(f"Doc {doc_id}: {text}")

    first_pass_scores = {doc_id: overlap_score(QUERY, text) for doc_id, text in DOCS.items()}

    print("=" * 72)
    print("First-pass scores (all docs):")
    for doc_id, score in first_pass_scores.items():
        print(f"Doc {doc_id} score={score}: {DOCS[doc_id]}")

    print("=" * 72)
    print("Scenario A: First-pass ranking")
    first_pass_ranked = rank(first_pass_scores)
    for doc_id, score in first_pass_ranked:
        print(f"Doc {doc_id} score={score}: {DOCS[doc_id]}")

    print("=" * 72)
    print("Scenario B: Top-k candidates")
    top_k = [doc_id for doc_id, _ in first_pass_ranked[:TOP_K]]
    print("Top-k:", top_k)

    print("=" * 72)
    print("Scenario C: Reranker scores (top-k only)")
    rerank_scores = {doc_id: reranker_score(DOCS[doc_id]) for doc_id in top_k}
    for doc_id, score in rerank_scores.items():
        print(f"Doc {doc_id} rerank={score:.2f}: {DOCS[doc_id]}")

    print("=" * 72)
    print("Scenario D: Reranked order")
    reranked = rank(rerank_scores)
    for doc_id, score in reranked:
        print(f"Doc {doc_id} rerank={score:.2f}: {DOCS[doc_id]}")

    print("=" * 72)
    print("Scenario E: Missed candidate outside top-k")
    missed_id = 7
    print(f"Doc {missed_id} first-pass score={first_pass_scores[missed_id]}: {DOCS[missed_id]}")
    print("This doc is relevant but was outside top-k, so reranker never saw it.")

    print("=" * 72)
    print("Interpretation:")
    print("- First pass is fast but imperfect: Doc 1 leads, but Doc 4 is the best match.")
    print("- Reranking improves order within top-k using a smarter intent score.")
    print("- Doc 7 was outside top-k, so reranker could not rescue it.")


if __name__ == "__main__":
    run_reranking_demo()

# Takeaway:
# Rerank only the top-k; what you miss in first pass is gone.
