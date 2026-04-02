# LC001 — Two Sum

## Why It Is Priority
- repeat count: 4
- bucket: Hashing
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: find two distinct indices whose values sum to `target`
- input shape: integer array `nums` and integer `target`
- output: index pair `[i, j]` for the valid two-sum match
- constraints (inferred if needed): exactly one solution; cannot reuse same index

## Core Pattern
- Single-pass hash map for complement lookup.
- At each value `x`, check whether `target - x` was seen earlier.
- Store value-to-index after check to avoid reusing same element.

## Recognition Triggers
- Need pair of indices matching a target sum.
- Brute-force O(n^2) pair scan is the obvious baseline to beat.
- Output asks for indices, not sorted values or count.
- Exactly-one-solution style wording suggests direct lookup approach.

## Correct Approach Outline
1. Initialize an empty hash map from value to index.
2. Iterate `nums` once; compute `complement = target - nums[i]`.
3. If complement is already in map, return `[map[complement], i]`.
4. Otherwise store current value/index and continue.

## Complexity
- time: O(n)
- space: O(n)
- why: each element is processed once with O(1) average map lookup/insert.

## Common Failure Modes
- inserting before complement check and pairing index with itself
- mishandling duplicates like `[3,3]` for target `6`
- returning values instead of required indices
- using two-pointer without preserving original indices context

## Implementation Checklist
- [ ] check complement before inserting current value
- [ ] store value -> index mapping (not index -> value)
- [ ] return original indices, not sorted values
- [ ] ensure same index is never reused
- [ ] test duplicate-value case (e.g., `[3,3]`, target `6`)

## What To Practice Next
- [LC167 Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)
- [LC1 Two Sum (variant revisit)](https://leetcode.com/problems/two-sum/)
- [LC560 Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/)

## Promotion Status
- status: in-progress
- source: PracticeHistory
- notes: priority pass filled for pattern recognition + interview recall


## Pattern Links
- Primary: Hash map lookup
