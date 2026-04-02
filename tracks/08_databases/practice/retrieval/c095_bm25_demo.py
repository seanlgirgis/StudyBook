# Story:
# BM25 improves keyword ranking with rarity, saturation, and length normalization.
# This demo compares overlap, raw term frequency, and BM25-style scoring.

import math
import re


DOCS = {
    1: "xr15 refund policy",
    2: "refund refund refund refund headset return process",
    3: "xr15 headset battery replacement guide",
    4: "customer refund policy and return steps for all products including xr15 headset",
    5: "monthly policy update refund rules for all products and services",
    6: "xr15 refund request approved",
}

QUERY = "xr15 refund policy"

K1 = 1.5
B = 0.75


def _tokenize(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def term_frequencies(tokens):
    counts = {}
    for token in tokens:
        counts[token] = counts.get(token, 0) + 1
    return counts


def document_frequencies(docs_tokens, terms):
    df = {term: 0 for term in terms}
    for tokens in docs_tokens.values():
        token_set = set(tokens)
        for term in terms:
            if term in token_set:
                df[term] += 1
    return df


def bm25_score(tf, df, doc_len, avg_len, total_docs):
    score = 0.0
    for term, freq in tf.items():
        if freq == 0:
            continue
        idf = math.log((total_docs - df[term] + 0.5) / (df[term] + 0.5) + 1)
        denom = freq + K1 * (1 - B + B * (doc_len / avg_len))
        score += idf * ((freq * (K1 + 1)) / denom)
    return score


def rank(scores):
    return sorted(scores.items(), key=lambda item: item[1], reverse=True)


def run_bm25_demo():
    query_terms = _tokenize(QUERY)
    docs_tokens = {doc_id: _tokenize(text) for doc_id, text in DOCS.items()}
    docs_tf = {doc_id: term_frequencies(tokens) for doc_id, tokens in docs_tokens.items()}

    df = document_frequencies(docs_tokens, query_terms)
    doc_lengths = {doc_id: len(tokens) for doc_id, tokens in docs_tokens.items()}
    avg_len = sum(doc_lengths.values()) / len(doc_lengths)

    overlap_scores = {}
    tf_scores = {}
    bm25_scores = {}

    for doc_id, tokens in docs_tokens.items():
        tf = docs_tf[doc_id]
        overlap = sum(1 for term in query_terms if term in tf)
        tf_score = sum(tf.get(term, 0) for term in query_terms)
        bm25 = bm25_score({term: tf.get(term, 0) for term in query_terms}, df, doc_lengths[doc_id], avg_len, len(DOCS))
        overlap_scores[doc_id] = overlap
        tf_scores[doc_id] = tf_score
        bm25_scores[doc_id] = bm25

    print("=" * 72)
    print("Query:", QUERY)

    print("=" * 72)
    print("Corpus:")
    for doc_id, text in DOCS.items():
        print(f"Doc {doc_id}: {text}")

    print("=" * 72)
    print("Document frequencies (query terms):")
    for term in query_terms:
        print(f"{term}: df={df[term]}")

    print("=" * 72)
    print("Per-document scores:")
    for doc_id in DOCS:
        print(
            f"Doc {doc_id} len={doc_lengths[doc_id]} "
            f"overlap={overlap_scores[doc_id]} "
            f"tf={tf_scores[doc_id]} "
            f"bm25={bm25_scores[doc_id]:.3f} | {DOCS[doc_id]}"
        )

    print("=" * 72)
    print("Scenario A: Overlap ranking (too flat)")
    for doc_id, score in rank(overlap_scores):
        print(f"Doc {doc_id} overlap={score}: {DOCS[doc_id]}")

    print("=" * 72)
    print("Scenario B: Raw TF ranking (over-rewards repetition)")
    for doc_id, score in rank(tf_scores):
        print(f"Doc {doc_id} tf={score}: {DOCS[doc_id]}")

    print("=" * 72)
    print("Scenario C: BM25 ranking (rarity + saturation + length norm)")
    for doc_id, score in rank(bm25_scores):
        print(f"Doc {doc_id} bm25={score:.3f}: {DOCS[doc_id]}")

    print("=" * 72)
    print("Interpretation:")
    print("- Overlap ties Doc 1 and Doc 4 even though Doc 1 is cleaner and shorter.")
    print("- Raw TF over-rewards Doc 2 because it repeats 'refund' many times.")
    print("- BM25 boosts the rare term 'xr15' and normalizes length, so Doc 1 and Doc 6 rise.")
    print("- The final BM25 order is the most sensible balance of rarity, repetition, and length.")


if __name__ == "__main__":
    run_bm25_demo()

# Takeaway:
# Not every matching word should count the same. BM25 fixes that intuition.
