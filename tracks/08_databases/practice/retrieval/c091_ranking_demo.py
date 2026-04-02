# Story:
# Ranking orders matched documents by relevance.
# This demo compares no ranking vs simple scoring.

import math
import re
from collections import defaultdict


DOCS = {
    1: "Search ranking uses term frequency and rarity.",
    2: "Ranking puts the best search results first.",
    3: "Search engines rank results using many signals.",
    4: "Term frequency boosts a document when words repeat.",
    5: "Rarity makes a matching term more important.",
}


def _tokenize(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def build_inverted_index(docs):
    index = defaultdict(set)
    for doc_id, text in docs.items():
        for token in _tokenize(text):
            index[token].add(doc_id)
    return index


def candidate_docs(index, terms):
    postings = [index.get(term, set()) for term in terms]
    if not postings:
        return []
    return sorted(set.union(*postings))


def score_match_count(docs, terms):
    scores = {}
    for doc_id, text in docs.items():
        tokens = set(_tokenize(text))
        score = sum(1 for term in terms if term in tokens)
        if score:
            scores[doc_id] = score
    return scores


def score_term_frequency(docs, terms):
    scores = {}
    for doc_id, text in docs.items():
        tokens = _tokenize(text)
        score = sum(tokens.count(term) for term in terms)
        if score:
            scores[doc_id] = score
    return scores


def score_with_rarity(docs, terms):
    doc_freq = {term: 0 for term in terms}
    for text in docs.values():
        tokens = set(_tokenize(text))
        for term in terms:
            if term in tokens:
                doc_freq[term] += 1

    scores = {}
    for doc_id, text in docs.items():
        tokens = _tokenize(text)
        score = 0.0
        for term in terms:
            tf = tokens.count(term)
            if tf == 0:
                continue
            idf = math.log((len(docs) + 1) / (doc_freq[term] + 1)) + 1
            score += tf * idf
        if score:
            scores[doc_id] = round(score, 3)
    return scores


def _print_scores(label, scores):
    print(label)
    for doc_id, score in scores.items():
        print(f"  Doc {doc_id} score={score}: {DOCS[doc_id]}")


def _print_ranked(label, scores):
    print(label)
    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    for doc_id, score in ranked:
        print(f"  Doc {doc_id} score={score}: {DOCS[doc_id]}")


def run_ranking_demo():
    index = build_inverted_index(DOCS)
    terms = ["search", "ranking", "term"]

    print("=" * 72)
    print("Scenario A: Candidates only (no ranking)")
    candidates = candidate_docs(index, terms)
    print("Candidates:", candidates)

    print("=" * 72)
    print("Scenario B: Simple ranking (match count)")
    scores = score_match_count(DOCS, terms)
    _print_scores("Scores:", scores)
    _print_ranked("Ranked:", scores)

    print("=" * 72)
    print("Scenario C: Term frequency boost")
    scores = score_term_frequency(DOCS, terms)
    _print_scores("Scores:", scores)
    _print_ranked("Ranked:", scores)

    print("=" * 72)
    print("Scenario D: Rarity intuition (IDF-weighted)")
    scores = score_with_rarity(DOCS, terms)
    _print_scores("Scores:", scores)
    _print_ranked("Ranked:", scores)


if __name__ == "__main__":
    run_ranking_demo()

# Takeaway:
# Ranking turns matches into ordered, useful results.
