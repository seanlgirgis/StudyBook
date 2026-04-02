# LC136 — Single Number

## Why It Is Priority
- repeat count: 3
- bucket: BitManipulation
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: find the unique element in an array where every other element appears exactly twice
- input shape: array of integers `nums`
- output: integer (the unique element)
- constraints (inferred if needed): O(1) extra space, O(N) time required

## Core Pattern
- bitwise XOR accumulation
- `X ^ X = 0` (duplicates cancel out)
- `X ^ 0 = X` (single number remains)

## Recognition Triggers
- "every element appears twice except for one"
- strict requirements for O(n) time and O(1) space
- finding a uniquely unpaired element

## Correct Approach Outline
1. Initialize `result = 0`
2. Iterate `num` through `nums`
3. XOR `result` with `num` (`result ^= num`)
4. Return `result`

## Complexity
- time: O(N)
- space: O(1)
- why: single pass, single scalar for bitwise accumulation

## Common Failure Modes
- Using a Hash Map/Set (violates O(1) space constraint, though functionally works)
- Sorting the array first (violates O(N) time limit, makes it O(N log N))
- Overcomplicating parity checks of bits instead of leveraging the XOR operator directly

## Implementation Checklist
- [ ] initialize accumulator to 0 (neutral element for XOR)
- [ ] use `^=` operator correctly
- [ ] edge case: array with single element works natively
- [ ] handle negative numbers (Python handles negative bitwise operations safely here)

## What To Practice Next
- LC268 Missing Number (similar XOR exact-pair cancellation pattern)
- LC137 Single Number II (every element appears three times; requires modulus bit counting)
- LC260 Single Number III (two unique numbers; requires finding differing bit post-XOR)

## Promotion Status
- status: enriched
- source: PracticeHistory
- notes: archetype for duplicate cancellation via XOR

## Pattern Links
- Primary: Bit manipulation (XOR)
