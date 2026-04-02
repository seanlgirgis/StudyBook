# Story:
# Search uses an inverted index: word -> list of documents.
# This demo contrasts lookup vs search with AND/OR and simple ranking.

import re
from collections import defaultdict


DOCS = {
    1: "Cassandra spreads writes across nodes for availability.",
    2: "DynamoDB uses partition keys and sort keys for fast queries.",
    3: "Search engines build an inverted index to find documents by words.",
    4: "Indexes speed up lookup and search in large datasets.",
    5: "Partition keys can create hot partitions if traffic is skewed.",
}


def _tokenize(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def build_inverted_index(docs):
    index = defaultdict(set)
    for doc_id, text in docs.items():
        for token in _tokenize(text):
            index[token].add(doc_id)
    return index


def lookup(docs, doc_id):
    return docs.get(doc_id)


def search_single(index, term):
    return sorted(index.get(term, set()))


def search_and(index, terms):
    postings = [index.get(term, set()) for term in terms]
    if not postings:
        return []
    result = set.intersection(*postings) if postings else set()
    return sorted(result)


def search_or(index, terms):
    postings = [index.get(term, set()) for term in terms]
    result = set.union(*postings) if postings else set()
    return sorted(result)


def rank_by_term_frequency(docs, terms):
    scores = []
    for doc_id, text in docs.items():
        tokens = _tokenize(text)
        score = sum(tokens.count(term) for term in terms)
        if score > 0:
            scores.append((score, doc_id))
    scores.sort(reverse=True)
    return scores


def run_search_demo():
    index = build_inverted_index(DOCS)

    print("=" * 72)
    print("Scenario A: Exact lookup (id -> document)")
    doc = lookup(DOCS, 2)
    print("Lookup id=2:", doc)

    print("=" * 72)
    print("Inverted index sample (token -> docs)")
    for term in ["partition", "keys", "search", "index"]:
        print(f"{term}: {sorted(index.get(term, set()))}")

    print("=" * 72)
    print("Scenario B: Single-word search")
    term = "partition"
    print(f"Search '{term}':", search_single(index, term))

    print("=" * 72)
    print("Scenario C: Multi-word query")
    terms = ["partition", "keys"]
    print("AND:", search_and(index, terms))
    print("OR:", search_or(index, terms))

    print("=" * 72)
    print("Scenario D: Simple ranking")
    ranked = rank_by_term_frequency(DOCS, ["search", "index"])
    print("Query terms: search index")
    for score, doc_id in ranked:
        print(f"Doc {doc_id} score={score}: {DOCS[doc_id]}")


if __name__ == "__main__":
    run_search_demo()

# Takeaway:
# Lookup finds one record by key; search finds many by content and ranks them.
