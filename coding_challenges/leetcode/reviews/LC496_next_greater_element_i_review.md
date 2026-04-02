# LC496 — Next Greater Element I

## Why It Is Priority
- repeat count: 3
- bucket: Stack
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: find next greater value for each element of `nums1` using order in `nums2`
- input shape: subset array `nums1` and reference array `nums2`
- output: array of next-greater values or `-1`
- constraints (inferred if needed): answer is value mapping, not distance/index

## Core Pattern
- Build `nextGreater[value]` map from `nums2` via monotonic decreasing stack.
- When current value is greater, pop smaller stack values and map them to current.
- Resolve `nums1` by direct hash lookups in precomputed map.

## Recognition Triggers
- Need next greater element to the right, but only for query subset.
- Output requires next greater value, unlike LC739 distance output.
- `nums2` order defines relationships; preprocessing then query is natural.
- Brute-force scan per query is O(m*n) and avoidable.

## Correct Approach Outline
1. Initialize empty stack and hash map for next-greater mapping.
2. Traverse `nums2`; while stack top is smaller, map popped value to current.
3. Push current value; leftover stack values map to `-1`.
4. Build result for `nums1` from mapping.

## Complexity
- time: O(n + m)
- space: O(n)
- why: each `nums2` value is pushed/popped once, plus O(m) lookups for `nums1`.

## Common Failure Modes
- storing indices when value-based map is required
- forgetting to assign `-1` for unresolved stack elements
- using non-strict compare and mishandling duplicate assumptions
- scanning `nums1` directly with stack instead of preprocessing `nums2`

## Implementation Checklist
- [ ] keep stack monotonic decreasing by value
- [ ] pop-then-map while current value is greater
- [ ] finalize unresolved values with `-1`
- [ ] query map for each `nums1` value
- [ ] test all-descending, all-ascending, and single-element cases

## What To Practice Next
- [LC503 Next Greater Element II](https://leetcode.com/problems/next-greater-element-ii/)
- [LC739 Daily Temperatures](https://leetcode.com/problems/daily-temperatures/)
- [LC901 Online Stock Span](https://leetcode.com/problems/online-stock-span/)

## Promotion Status
- status: in-progress
- source: PracticeHistory
- notes: promotion draft completed for stack-preprocess plus subset-query pattern


## Pattern Links
- Primary: Monotonic stack
