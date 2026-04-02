# BM25 Intuition - Story Map

## 1. Story (support search with noisy results)
A support agent searches for "xr15 refund policy." Many tickets mention "refund" and "policy" but only a few are about XR15. A long policy memo keeps showing up first even when a short XR15-specific ticket is more useful.

## 2. Core Concepts (street version)
- Not every matching word should count the same.
- Rare words should matter more.
- Repetition helps, but with diminishing returns.
- Long docs need normalization so they do not win by size.

## 3. Why simple term count is too naive
Counting matches treats "refund" the same as "xr15" and ignores document length.

## 4. What BM25 is really trying to fix
Balance three things: rarity, repetition (with limits), and document length.

## 5. Rare words vs common words
Common words are weak signals; rare words punch harder.

## 6. Repetition helps, but not forever
Repeating a term helps, but each extra repeat adds less than the last.

## 7. Why long docs need normalization
Long noisy docs mention many terms by accident. BM25 reduces that advantage.

## 8. What BM25 is great at
- Smarter keyword ranking
- Balancing relevance signals in real search

## 9. What BM25 is bad at
- Pure semantic matching
- Understanding intent beyond words

## 10. Final mental model
BM25 is a better bouncer: rare words get VIP access, repeats get smaller tips, long talkers do not cut the line.

## 11. Run Order
1. c095_bm25_demo.py
