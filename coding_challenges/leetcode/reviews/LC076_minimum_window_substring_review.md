# LC076 — Minimum Window Substring

## Why It Is Priority
- repeat count: {N}
- bucket: Trees
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: find the shortest substring of `s` containing all characters of `t` with multiplicity
- input shape: strings `s` (search text) and `t` (required multiset)
- output: minimum valid window substring, or empty string if none exists
- constraints (inferred if needed): must track duplicate-required characters, not just presence

## Core Pattern
- {pattern point 1}
- {pattern point 2}
- {pattern point 3}

## Recognition Triggers
- {trigger 1}
- {trigger 2}
- {trigger 3}
- {trigger 4}

## Correct Approach Outline
1. Build frequency map `need` from `t`; maintain `window` counts plus `have/required`.
2. Expand right pointer, updating `window` and `have` when a needed count is satisfied.
3. While window is valid (`have == required`), update best answer and shrink left pointer.
4. On shrink, if a required count drops below target, decrement `have`; continue scan.

## Complexity
- time: O(|s| + |t|)
- space: O(|charset in t|)
- why: each pointer moves monotonically across `s`; maps store needed/window counts.

## Common Failure Modes
- {failure mode 1}
- {failure mode 2}
- {failure mode 3}
- {failure mode 4}

## Implementation Checklist
- [ ] initialize `need` from `t` including duplicate counts
- [ ] increase `have` only when `window[ch]` reaches `need[ch]`
- [ ] decrease `have` when shrinking breaks a required count
- [ ] track best window by `(length, left, right)` while valid
- [ ] test cases with repeated chars in `t` and no-valid-window scenario

## What To Practice Next
- LC### {Related Problem 1}
- LC### {Related Problem 2}
- LC### {Related Problem 3}

## Promotion Status
- status: in-progress
- source: PracticeHistory
- notes: {draft lineage / decisions}


## Pattern Links
- Primary: BFS/DFS grid
