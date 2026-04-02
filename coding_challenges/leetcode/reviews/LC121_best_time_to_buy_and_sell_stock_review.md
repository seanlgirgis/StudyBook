# LC121 — Best Time to Buy and Sell Stock

## Why It Is Priority
- repeat count: 5
- bucket: DP
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: find the maximum profit from one buy and one sell (buy before sell)
- input shape: array of stock prices indexed by day
- output: integer — max profit (0 if no profit possible)
- constraints (inferred if needed): prices are non-negative; exactly one buy-before-sell transaction allowed at most

## Core Pattern
- greedy / state tracking — one-pass scan
- track running minimum price seen so far (`min_price`)
- at each step compute `price - min_price` and update `max_profit`

## Recognition Triggers
- "one transaction only" or "buy then sell" language
- maximize a difference where left index < right index
- no need to remember the full history, only the running min
- O(n) is clearly achievable

## Correct Approach Outline
1. Initialize `min_price = inf`, `max_profit = 0`
2. Iterate through each price
3. Update `min_price = min(min_price, price)`
4. Update `max_profit = max(max_profit, price - min_price)`

## Complexity
- time: O(n)
- space: O(1)
- why: single pass, two scalar variables only

## Common Failure Modes
- Trying to use DP table or nested loops — unnecessary for single transaction
- Using future prices implicitly by not maintaining the invariant: `min_price` must come from days at or before current index
- Forgetting to return 0 when prices are strictly decreasing
- Confusing this with LC122 (multiple transactions) and adding prices greedily

## Implementation Checklist
- [ ] `min_price` initialized to `inf` (not `prices[0]`) to unify loop logic
- [ ] `max_profit` updated using `price - min_price`, not `price - prices[0]`
- [ ] Update `min_price` BEFORE computing profit in same iteration
- [ ] Return `max_profit` (0 is the floor — never go negative)
- [ ] Edge case: single element array → profit = 0

## What To Practice Next
- LC122 Best Time to Buy and Sell Stock II (multiple transactions — greedy on diffs)
- LC123 Best Time to Buy and Sell Stock III (at most 2 transactions — DP)
- LC53 Maximum Subarray (same Kadane-style intuition)

## Promotion Status
- status: enriched
- source: PracticeHistory
- notes: greedy state-tracking baseline; covers the "running min" pattern family

## Pattern Links
- Primary: Greedy / State Tracking
- Secondary: DP (state-compression view)
