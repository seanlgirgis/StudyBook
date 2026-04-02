# LC033 — Search in Rotated Sorted Array

## Why It Is Priority
- repeat count: {N}
- bucket: BinarySearch
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: locate target index in rotated sorted array with distinct values
- input shape: rotated sorted integer array `nums` and integer `target`
- output: index of `target`, or `-1` if absent
- constraints (inferred if needed): must run in logarithmic time

## Core Pattern
- Modified binary search using sorted-half detection each iteration.
- At `mid`, identify which side is normally sorted via boundary comparison.
- Keep only the half that can still contain target; discard the other.

## Recognition Triggers
- Array is sorted but rotated, with requirement for logarithmic search time.
- Standard binary search fails because global order is broken at pivot.
- Values are distinct, making half-order checks unambiguous.
- Prompt asks for index lookup in near-sorted structure, signaling binary-search variant.

## Correct Approach Outline
1. Run binary search with pointers `l` and `r`.
2. Compute `mid`; if `nums[mid] == target`, return `mid`.
3. Determine which half is sorted (`nums[l] <= nums[mid]` or right half sorted).
4. Keep target-containing half and discard the other; continue until exhausted.

## Complexity
- time: O(log n)
- space: O(1)
- why: each step halves the search interval.

## Common Failure Modes
- {failure mode 1}
- {failure mode 2}
- {failure mode 3}
- {failure mode 4}

## Implementation Checklist
- [ ] detect sorted half correctly each iteration
- [ ] compare target against sorted-half bounds inclusively
- [ ] update `l/r` to avoid infinite loops
- [ ] return immediately on exact mid match
- [ ] test unrotated array, single element, and missing target

## What To Practice Next
- LC### {Related Problem 1}
- LC### {Related Problem 2}
- LC### {Related Problem 3}

## Promotion Status
- status: in-progress
- source: PracticeHistory
- notes: {draft lineage / decisions}


## Pattern Links
- Primary: Binary search variants
