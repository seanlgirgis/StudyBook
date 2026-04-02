# LC238 — Product of Array Except Self

## Why It Is Priority
- repeat count: 5
- bucket: Array
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: return array where each index is product of all elements except itself
- input shape: integer array `nums`
- output: array of same length
- constraints (inferred if needed): no division allowed; O(n) time, O(1) extra space (excluding output)

## Core Pattern
- prefix/suffix product decomposition
- compute left products and right products separately
- combine without using extra arrays (reuse output)

## Recognition Triggers
- "product except self"
- restriction: no division
- full array dependency except current index
- requirement for O(n) with constant extra space

## Correct Approach Outline
1. Initialize output array with 1s
2. Traverse left to right, storing prefix products
3. Traverse right to left, multiplying suffix products into output
4. Return output array

## Complexity
- time: O(n)
- space: O(1) extra (output not counted)
- why: two linear passes, no auxiliary arrays

## Common Failure Modes
- Using division (breaks zero handling and violates constraints)
- Forgetting to initialize output with 1
- Overwriting prefix before using it
- Mishandling zero values in input

## Implementation Checklist
- [ ] initialize output array with 1s
- [ ] maintain running prefix product
- [ ] maintain running suffix product
- [ ] multiply suffix into existing output values
- [ ] test cases with zeros (one zero, multiple zeros)

## What To Practice Next
- LC53 Maximum Subarray (prefix-like thinking)
- LC152 Maximum Product Subarray
- LC560 Subarray Sum Equals K

## Promotion Status
- status: enriched
- source: PracticeHistory
- notes: prefix/suffix decomposition pattern; avoids division

## Pattern Links
- Primary: Prefix/Suffix Products
- Related: Array Traversal