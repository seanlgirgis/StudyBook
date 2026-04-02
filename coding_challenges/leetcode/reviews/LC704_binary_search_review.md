# LC704 — Binary Search

## Why It Is Priority
- repeat count: 3
- bucket: BinarySearch
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: find target index in a sorted array, or return `-1` if missing
- input shape: sorted integer array `nums` and integer `target`
- output: target index or `-1`
- constraints (inferred if needed): logarithmic-time solution expected

## Core Pattern
- Maintain search interval `[l, r]` over sorted space.
- Use `mid` to discard half of remaining candidates each step.
- Preserve invariant that target, if present, stays inside kept half.

## Recognition Triggers
- Input is sorted and asks for fast lookup.
- Prompt explicitly or implicitly targets O(log n).
- Need exact index, not frequency or nearest value.
- One-dimensional monotonic search space is clear.

## Correct Approach Outline
1. Initialize `l = 0`, `r = len(nums) - 1`.
2. While `l <= r`, compute `mid`.
3. Return `mid` if `nums[mid] == target`; otherwise move `l` or `r` by comparison.
4. If loop ends, return `-1`.

## Complexity
- time: O(log n)
- space: O(1)
- why: each iteration halves the candidate range.

## Common Failure Modes
- using `while l < r` and missing final candidate check
- updating bounds incorrectly and causing infinite loops
- off-by-one errors when moving `l = mid + 1` or `r = mid - 1`
- returning value instead of required index

## Implementation Checklist
- [ ] keep loop condition consistent with inclusive bounds
- [ ] compute `mid` each iteration after bounds update
- [ ] compare `nums[mid]` before pruning half
- [ ] return `-1` only after loop exhaustion
- [ ] test single element, absent target, and boundary indices

## What To Practice Next
- [LC074 Search a 2D Matrix](https://leetcode.com/problems/search-a-2d-matrix/)
- [LC033 Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/)
- [LC153 Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/)

## Promotion Status
- status: in-progress
- source: PracticeHistory
- notes: promotion draft completed for baseline binary-search invariant handling


## Pattern Links
- Primary: Binary search variants
