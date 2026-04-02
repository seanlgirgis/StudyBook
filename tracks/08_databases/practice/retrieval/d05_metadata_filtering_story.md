# Metadata Filtering - Story Map

## 1. Story (support desk triage)
A support agent searches for "refund xr15 headset" but only for US open tickets. The best text match might be an EU policy or a closed case. Those are wrong for this request.

## 2. Core Concepts (street version)
- Retrieval finds matches by text or meaning.
- Filters enforce constraints like product, region, and status.
- Filter first, then rank what remains.

## 3. What metadata filtering is
Using structured fields (metadata) to remove invalid candidates before ranking.

## 4. Why retrieval alone is not enough
The top match can still be wrong if it violates business rules or context.

## 5. What filters represent (product, region, status, time, etc.)
Metadata is the hard truth: product line, geography, lifecycle status, time window, permissions.

## 6. Filter -> then rank flow
1. Apply filters to shrink the candidate set.
2. Rank only the valid documents.

## 7. What metadata filtering is great at
- Enforcing business rules
- Keeping results in the right context

## 8. What metadata filtering is bad at
- Capturing nuance in free-text meaning
- Replacing ranking (it only removes)

## 9. Final mental model
Filters are the bouncer. Ranking is the DJ. You cannot rank what should not enter.

## 10. Run Order
1. c094_metadata_filtering_demo.py
