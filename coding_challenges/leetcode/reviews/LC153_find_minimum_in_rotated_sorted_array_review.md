# LC153 — Find Minimum in Rotated Sorted Array

## Why It Is Priority
- repeat count: 3
- bucket: BinarySearch
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: find the minimum value in a rotated sorted array
- input shape: rotated sorted array `nums` with distinct integers
- output: minimum element value
- constraints (inferred if needed): must run in O(log n)

## Core Pattern
- Binary search on rotation boundary rather than direct target.
- Compare `nums[mid]` with `nums[r]` to decide which side contains minimum.
- Keep interval that is guaranteed to include pivot/minimum.

## Recognition Triggers
- Array is sorted but rotated, and asks for minimum.
- Distinct values remove ambiguity in half-selection.
- Linear scan is obvious baseline but too slow for prompt.
- No target search; objective is structural boundary detection.

## Correct Approach Outline
1. Initialize `l = 0`, `r = len(nums) - 1`.
2. While `l < r`, compute `mid`.
3. If `nums[mid] > nums[r]`, minimum is right of `mid`; set `l = mid + 1`; else set `r = mid`.
4. Return `nums[l]` when pointers converge.

## Complexity
- time: O(log n)
- space: O(1)
- why: each comparison removes roughly half the remaining range.

## Common Failure Modes
- using `r = mid - 1` and skipping possible minimum at `mid`
- mixing target-search template with min-search logic
- incorrect loop condition (`l <= r`) causing boundary bugs
- failing on already sorted non-rotated arrays

## Implementation Checklist
- [ ] use `while l < r` for convergence to single index
- [ ] compare against right bound value for partition decision
- [ ] keep `mid` in range when updating `r = mid`
- [ ] return value at converged index
- [ ] test unrotated, single-element, and two-element cases

## What To Practice Next
- [LC033 Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/)
- [LC081 Search in Rotated Sorted Array II](https://leetcode.com/problems/search-in-rotated-sorted-array-ii/)
- [LC154 Find Minimum in Rotated Sorted Array II](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array-ii/)

## Promotion Status
- status: in-progress
- source: PracticeHistory
- notes: promotion draft completed for rotated-array boundary binary search


## Pattern Links
- Primary: Binary search variants
