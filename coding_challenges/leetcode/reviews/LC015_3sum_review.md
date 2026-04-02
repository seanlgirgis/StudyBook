# LC015 — 3Sum

## Why It Is Priority
- repeat count: {N}
- bucket: TwoPointers
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: find all unique triplets that sum to zero
- input shape: integer array `nums`
- output: list of unique triplets `[a, b, c]` with `a + b + c = 0`
- constraints (inferred if needed): must avoid duplicate triplets

## Core Pattern
- Sort first, then reduce 3Sum to repeated 2Sum with two pointers.
- Fix one anchor index and scan remaining range with `l/r` toward target complement.
- Skip duplicates at anchor and pointer moves to enforce unique triplets.

## Recognition Triggers
- Need all unique triplets meeting a sum condition.
- Duplicate handling is explicit and central to correctness.
- Cubic triple-loop is obvious baseline but too slow for typical constraints.
- Sorting would enable directional pointer moves based on sum sign.

## Correct Approach Outline
1. Sort array to enable two-pointer scanning and duplicate control.
2. Iterate anchor index `i`; skip duplicate anchors.
3. For each anchor, run two pointers `l/r` to find pairs summing to `-nums[i]`.
4. Record valid triplets and skip duplicate `l/r` values before continuing.

## Complexity
- time: O(n^2)
- space: O(1) extra (excluding output)
- why: sorting plus linear two-pointer sweep per anchor.

## Common Failure Modes
- {failure mode 1}
- {failure mode 2}
- {failure mode 3}
- {failure mode 4}

## Implementation Checklist
- [ ] sort input before scanning
- [ ] skip duplicate anchor values (`i > 0 and nums[i] == nums[i-1]`)
- [ ] after a match, advance `l/r` past duplicates
- [ ] move `l` or `r` based on current sum sign
- [ ] test all-zero array and no-solution cases

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
