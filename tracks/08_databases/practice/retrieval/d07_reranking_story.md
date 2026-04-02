# Reranking - Story Map

## 1. Story (support search triage)
A support agent searches for "xr15 refund denied" and gets a quick list. The best ticket is in the list but not first. A smarter second pass fixes the order.

## 2. Core Concepts (street version)
- First-pass retrieval is fast and broad.
- Reranking is slower but smarter.
- Only the top-k candidates get the expensive score.

## 3. What first-pass retrieval does
Use a cheap score to grab plausible candidates quickly.

## 4. Why first-pass ranking can still be wrong
Cheap scores miss nuance, so the top result can be a weaker match.

## 5. What reranking is
A second pass that reorders the top-k using a more accurate signal.

## 6. Why reranking is done only on top-k
Expensive scoring is too slow to run on the full corpus.

## 7. Filter / retrieve / rerank flow
Filter by rules -> retrieve top-k -> rerank those candidates.

## 8. What reranking is great at
- Fixing ordering mistakes
- Adding smarter intent signals on a small set

## 9. What reranking is bad at
- Recovering documents that never made top-k
- Replacing good first-pass recall

## 10. Final mental model
First pass is a net. Reranker is a judge. The judge only sees what the net caught.

## 11. Run Order
1. c096_reranking_demo.py
