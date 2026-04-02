# Ranking — Story Map

## 1. Story (librarian ordering books by relevance)
You ask a librarian for books on "distributed systems." They pull a stack, then sort the best ones to the top.

## 2. Core Concepts (street version)
- Search finds candidates.
- Ranking decides the order.
- Higher score means more relevant.

## 3. Why ranking is needed after search
Matching alone returns too many results. Ranking puts the most useful first.

## 4. What a score is
A number that estimates how relevant a document is to the query.

## 5. Simple signals (term frequency, match count)
More matched terms or repeated terms push a doc higher.

## 6. Better signals (rarity / importance intuition)
Rare terms matter more than common terms, so they should carry extra weight.

## 7. Trade-offs (simple vs complex ranking)
Simple ranking is fast and explainable. Complex ranking can be smarter but harder to tune.

## 8. Final mental model
Search brings the pile. Ranking puts the best on top.

## 9. Run Order
1. c091_ranking_demo.py
