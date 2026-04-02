# LC042 - Trapping Rain Water

## Why It Is Priority
- repeat count: 5
- bucket: TwoPointers
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: compute total trapped rain water across all bars
- input shape: array of non-negative bar heights
- output: total accumulated trapped water as an integer
- constraints (inferred if needed): linear-time approach preferred over nested scans

## Core Pattern
- two pointers
- running left_max / right_max
- local water level determined by smaller boundary

## Recognition Triggers
- elevation bars / heights
- trapped volume between boundaries
- need total accumulation, not just max area
- brute force suggests left/right max scans

## Correct Approach Outline
1. Initialize two pointers at both ends and track `left_max` and `right_max`.
2. Compare current boundary heights and move the pointer on the smaller side.
3. Update that side max first, then add trapped water using `max - current_height`.
4. Continue until pointers cross, accumulating the total.

## Complexity
- time: O(n)
- space: O(1)
- why: each index is processed once with constant extra state.

## Common Failure Modes
- confusing with Container With Most Water
- moving the wrong pointer
- updating water before boundary max
- off-by-one around ends

## Implementation Checklist
- [ ] move the pointer on the smaller boundary side
- [ ] update boundary max before adding water at that index
- [ ] avoid double-processing when pointers meet
- [ ] validate behavior on monotonic increasing/decreasing arrays
- [ ] validate behavior on small arrays (length < 3)

## What To Practice Next
- LC011 Container With Most Water
- LC084 Largest Rectangle in Histogram
- LC739 Daily Temperatures

## Promotion Status
- status: in-progress
- source: PracticeHistory
- notes: first promotion draft from pooled index


## Pattern Links
- Primary: Two pointers
- Secondary: Monotonic stack
