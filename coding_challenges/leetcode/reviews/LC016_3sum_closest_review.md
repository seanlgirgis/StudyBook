# LC016 — 3Sum Closest

## Why It Is Priority
- repeat count: 3
- bucket: Arrays/TwoPointers
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: find three integers in an array that sum closest to a given target
- input shape: integer array `nums`, integer `target`
- output: integer (the sum of the three integers)
- constraints: array length >= 3, unique closest sum guaranteed

## Core Pattern
- Sort + Two Pointers
- anchor one number, then use left and right pointers on the remaining segment to search for the closest sum
- track the minimum absolute difference

## Recognition Triggers
- "three integers", "closest sum"
- O(N^2) optimization over O(N^3) brute force required
- sequence order doesn't matter, allows sorting

## Correct Approach Outline
1. Sort the input array `nums`
2. Initialize `closest_sum = infinity`
3. Iterate `i` from `0` to `len(nums) - 2`
4. Set `left = i + 1` and `right = len(nums) - 1`
5. Loop while `left < right`: calculate `curr_sum = nums[i] + nums[left] + nums[right]`
6. Update `closest_sum` if absolute difference to target is better, adjust `left`/`right` based on `curr_sum < target` or `curr_sum > target`

## Complexity
- time: O(N^2)
- space: O(1) or O(log N) depending on sort implementation
- why: outer loop runs N times, inner two-pointer loop takes O(N) time per outer loop

## Common Failure Modes
- Returning the absolute difference instead of the actual closest sum
- Forgetting to sort the array before applying two-pointers
- Not breaking early when `curr_sum == target` (since diff is 0, it won't get better)

## Implementation Checklist
- [ ] `nums.sort()` as step 1
- [ ] `closest_sum` initialized correctly (e.g., `float('inf')` or sum of first 3 elements)
- [ ] update `closest_sum` by comparing `abs(curr_sum - target)` against `abs(closest_sum - target)`
- [ ] shift `left` rightward if `curr_sum < target`, else shift `right` leftward

## What To Practice Next
- LC015 3Sum
- LC259 3Sum Smaller
- LC011 Container With Most Water

## Promotion Status
- status: enriched
- source: PracticeHistory
- notes: direct application of 3Sum pattern with an optimization criteria

## Pattern Links
- Primary: Two Pointers
- Secondary: Arrays
