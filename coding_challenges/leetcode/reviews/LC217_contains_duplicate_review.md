# LC217 — Contains Duplicate

## Why It Is Priority
- repeat count: 3
- bucket: Hashing
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: determine whether any value appears at least twice
- input shape: integer array `nums`
- output: boolean indicating duplicate existence
- constraints (inferred if needed): optimize beyond pairwise comparison

## Core Pattern
- Track seen values in a hash set during one pass.
- If current value already exists in set, duplicate is confirmed.
- Early return on first repeat for minimal work.

## Recognition Triggers
- Ask is existence of any duplicate, not count or index list.
- Brute-force compare-all-pairs is obvious but inefficient.
- Order is irrelevant; membership check dominates.
- Boolean output suggests early-exit scan.

## Correct Approach Outline
1. Initialize an empty hash set `seen`.
2. Iterate each number in `nums`.
3. If number is already in `seen`, return `true`; otherwise add it.
4. Return `false` after full scan if no repeat found.

## Complexity
- time: O(n)
- space: O(n)
- why: each element does O(1) average set lookup and insert once.

## Common Failure Modes
- using list membership checks and degrading to O(n^2)
- sorting in-place when mutation side effects are undesirable
- forgetting early return after detecting first duplicate
- mishandling empty/single-element arrays

## Implementation Checklist
- [ ] initialize empty set before scan
- [ ] check membership before adding current value
- [ ] return immediately on duplicate hit
- [ ] return false only after full traversal
- [ ] test empty, single, all-unique, and all-same cases

## What To Practice Next
- [LC219 Contains Duplicate II](https://leetcode.com/problems/contains-duplicate-ii/)
- [LC220 Contains Duplicate III](https://leetcode.com/problems/contains-duplicate-iii/)
- [LC001 Two Sum](https://leetcode.com/problems/two-sum/)

## Promotion Status
- status: in-progress
- source: PracticeHistory
- notes: promotion draft completed for hash-set duplicate detection baseline


## Pattern Links
- Primary: Hash map lookup
