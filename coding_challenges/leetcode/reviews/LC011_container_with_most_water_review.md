# LC011 — Container With Most Water

## Why It Is Priority
- repeat count: {N}
- bucket: TwoPointers
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: find maximum water area formed by two vertical lines
- input shape: array `height` of non-negative integers
- output: maximum area as integer
- constraints (inferred if needed): area uses `min(height[l], height[r]) * (r - l)`

## Core Pattern
- Two pointers start at extremes to maximize initial width.
- Area is constrained by shorter wall, so move only the shorter side inward.
- Greedy elimination: discarded pairings cannot beat current width/height limit.

## Recognition Triggers
- Objective is max of pair-based formula using distance and min of two heights.
- Need best pair, not all pairs; O(n^2) enumeration is avoidable.
- Inputs are positional lines where inward movement changes width predictably.
- Problem structure suggests opposite-end pointers with monotonic shrink.

## Correct Approach Outline
1. Initialize two pointers at both ends of the array.
2. Compute area for current pair and update best answer.
3. Move pointer at shorter line inward (only this can improve min height).
4. Repeat until pointers meet.

## Complexity
- time: O(n)
- space: O(1)
- why: each pointer moves inward at most `n` steps total.

## Common Failure Modes
- {failure mode 1}
- {failure mode 2}
- {failure mode 3}
- {failure mode 4}

## Implementation Checklist
- [ ] compute area before pointer movement each iteration
- [ ] always move the shorter-side pointer
- [ ] handle equal heights consistently (move either side)
- [ ] track max area globally
- [ ] test minimal input size and monotonic height arrays

## What To Practice Next
- LC### {Related Problem 1}
- LC### {Related Problem 2}
- LC### {Related Problem 3}

## Promotion Status
- status: in-progress
- source: PracticeHistory
- notes: {draft lineage / decisions}


## Pattern Links
- Primary: Two pointers
