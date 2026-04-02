# Top-k and Recall@k - Story Map

## 1. Story (support search gate)
A support agent searches for "xr15 refund denied" and only keeps the top results to save time. The best tickets are there, but one important case falls just below the cutoff.

## 2. Core Concepts (street version)
- Top-k is a gate: only the first k results survive.
- Smaller k is cheaper but riskier.
- Larger k is safer but more expensive.
- Recall@k asks: did the relevant docs make it through?

## 3. What top-k means
Keep only the top k candidates from the first-pass ranking.

## 4. Why top-k is a tradeoff
Lower k saves cost; higher k protects recall and future reranking.

## 5. What recall@k means
The fraction of relevant docs that survived the top-k gate.

## 6. Why reranking depends on recall@k
Rerankers can only fix order inside top-k. Missed docs are gone.

## 7. Small k vs large k
Small k risks dropping a relevant doc. Larger k preserves it for later stages.

## 8. What recall@k is great at
- Measuring candidate survival
- Comparing retrieval stages

## 9. What recall@k is bad at
- Judging ranking quality inside top-k
- Capturing user satisfaction by itself

## 10. Final mental model
Top-k is the gate. Recall@k tells you how many right answers made it inside.

## 11. Run Order
1. c097_topk_recall_demo.py
