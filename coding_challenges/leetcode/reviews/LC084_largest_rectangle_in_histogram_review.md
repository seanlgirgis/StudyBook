# LC084 - Largest Rectangle in Histogram

## Why It Is Priority
- repeat count: 4
- bucket: Stack
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: find maximum rectangle area under histogram bars
- input shape: array of bar heights
- output: maximum rectangular area as an integer
- constraints (inferred if needed): brute-force boundary expansion is too slow

## Core Pattern
- monotonic increasing stack
- defer area calculation until a shorter bar appears
- width determined by previous smaller and next smaller boundaries

## Recognition Triggers
- histogram / bar heights
- largest rectangle or max area under bars
- need nearest smaller boundary on both sides
- brute force width expansion is too slow

## Correct Approach Outline
1. Maintain a monotonic increasing stack of indices.
2. For each bar, pop while current height is smaller than top height.
3. On each pop, compute area using popped height and width from new stack top to current index.
4. Add sentinel processing at end to flush remaining bars.

## Complexity
- time: O(n)
- space: O(n)
- why: each index is pushed and popped at most once.

## Common Failure Modes
- forgetting sentinel flush at the end
- computing width incorrectly after pop
- storing heights instead of indices
- misunderstanding what the stack represents

## Implementation Checklist
- [ ] stack stores indices, not heights
- [ ] compute width as `i - left_smaller_index - 1` after pop
- [ ] handle empty-stack case when computing width
- [ ] flush stack at end via sentinel index/height
- [ ] test equal-height bars and strictly increasing input

## What To Practice Next
- LC085 Maximal Rectangle
- LC739 Daily Temperatures
- LC042 Trapping Rain Water

## Promotion Status
- status: in-progress
- source: PracticeHistory
- notes: third promotion draft from pooled index


## Pattern Links
- Primary: Monotonic stack
