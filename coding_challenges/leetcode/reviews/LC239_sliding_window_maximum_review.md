# LC239 — Sliding Window Maximum

## Why It Is Priority
- repeat count: 4
- bucket: Stack
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: find the maximum element in every sliding window of size k
- input shape: array of integers `nums`, integer `k`
- output: array of maximums for each window
- constraints (inferred if needed): O(n) required, k <= len(nums)

## Core Pattern
- monotonic deque (decreasingly sorted indices)
- front of deque always holds the max for the current window
- drop elements from back if they are smaller than current element

## Recognition Triggers
- "sliding window" + "maximum" or "minimum"
- O(N*K) is too slow
- need to maintain an ordered set of useful candidates

## Correct Approach Outline
1. Initialize a `deque` to store indices, and a `result` list
2. Iterate `i` from 0 to n-1:
3. While deque is not empty and `deque[0] < i - k + 1`: popleft (remove out of bounds)
4. While deque is not empty and `nums[deque[-1]] <= nums[i]`: pop (remove useless)
5. Append `i` to deque
6. If `i >= k - 1`: append `nums[deque[0]]` to result

## Complexity
- time: O(N)
- space: O(K)
- why: each element is pushed and popped to the deque at most once

## Common Failure Modes
- Storing actual values instead of indices in the deque (makes it hard to check bounds)
- Dropping elements incorrectly from the back (using `<` instead of `<=`)
- Recording the maximum before the first full window is formed (`i < k - 1`)

## Implementation Checklist
- [ ] Deque stores indices, not values
- [ ] Clean up elements outside the window (`i - deque[0] >= k`)
- [ ] Maintain monotonic decreasing property (pop from back if `< nums[i]`)
- [ ] Wait until window size reaches `k` before appending to output

## What To Practice Next
- LC76 Minimum Window Substring (sliding window without deque)
- LC496 Next Greater Element I (monotonic stack basics)
- LC84 Largest Rectangle in Histogram (monotonic stack area)

## Promotion Status
- status: enriched
- source: PracticeHistory
- notes: classic monotonic deque pattern

## Pattern Links
- Primary: Monotonic deque
- Secondary: Two pointers
