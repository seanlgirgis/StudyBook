# LC242 — Valid Anagram

## Why It Is Priority
- repeat count: 3
- bucket: Hashing
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: determine whether two strings are anagrams
- input shape: strings `s` and `t`
- output: boolean validity result
- constraints (inferred if needed): same characters with same frequencies required

## Core Pattern
- Count character frequencies and compare count profiles.
- Increment counts from one string and decrement for the other.
- Valid anagram requires all net counts to end at zero.

## Recognition Triggers
- Need equality of character multiset, not order.
- Same-length check quickly eliminates impossible pairs.
- Frequency matching is central; sorting is optional fallback.
- Boolean output on two strings suggests counting map pattern.

## Correct Approach Outline
1. If lengths differ, return `false`.
2. Build frequency map from `s`.
3. Traverse `t`, decrementing counts and failing on missing/negative entries.
4. Return `true` if all counts balance to zero.

## Complexity
- time: O(n)
- space: O(k)
- why: single pass frequency updates over alphabet/key set size `k`.

## Common Failure Modes
- skipping early length check and doing unnecessary work
- using set equality (ignores character multiplicity)
- allowing counts to go negative without failing
- mishandling unicode/charset assumptions when using fixed arrays

## Implementation Checklist
- [ ] fail fast when lengths differ
- [ ] use map/array keyed by character
- [ ] decrement counts for second string and validate availability
- [ ] confirm all counts are zero at end
- [ ] test repeated chars, empty strings, and one-char mismatch

## What To Practice Next
- [LC049 Group Anagrams](https://leetcode.com/problems/group-anagrams/)
- [LC438 Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/)
- [LC383 Ransom Note](https://leetcode.com/problems/ransom-note/)

## Promotion Status
- status: in-progress
- source: PracticeHistory
- notes: promotion draft completed for frequency-map anagram recognition


## Pattern Links
- Primary: Hash map lookup
