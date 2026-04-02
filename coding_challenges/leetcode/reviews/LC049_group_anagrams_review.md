# LC049 — Group Anagrams

## Why It Is Priority
- repeat count: 3
- bucket: Hashing
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: group strings that are anagrams into buckets
- input shape: array of lowercase strings `strs`
- output: list of grouped anagram lists
- constraints (inferred if needed): grouping key must be identical for anagrams

## Core Pattern
- Build hash map from canonical signature to word list.
- Signature can be sorted string or fixed-size character count tuple.
- Append each word into bucket for its signature.

## Recognition Triggers
- Need partitioning by character multiset equivalence.
- Order of letters inside each word is irrelevant.
- Output asks for grouped lists, not pairwise checks.
- Frequent use of dictionary keyed by normalized representation.

## Correct Approach Outline
1. Initialize map `signature -> list`.
2. For each string, compute canonical signature.
3. Append string to its signature bucket.
4. Return all map values.

## Complexity
- time: O(n * k log k) with sorted-key approach
- space: O(n * k)
- why: each of `n` strings of length `k` contributes to key + storage.

## Common Failure Modes
- using set as key (loses character counts)
- mutable key structures causing hash-map errors
- forgetting empty-string handling in signature generation
- sorting each bucket post-hoc instead of keying correctly upfront

## Implementation Checklist
- [ ] choose deterministic signature format
- [ ] use map with list default initialization
- [ ] append word directly to signature bucket
- [ ] return grouped values without requiring order guarantees
- [ ] test duplicates, single-char words, and empty strings

## What To Practice Next
- [LC242 Valid Anagram](https://leetcode.com/problems/valid-anagram/)
- [LC438 Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/)
- [LC49 Group Anagrams (count-key variant revisit)](https://leetcode.com/problems/group-anagrams/)

## Promotion Status
- status: in-progress
- source: PracticeHistory
- notes: promotion draft completed for signature-hash grouping pattern


## Pattern Links
- Primary: Hash map lookup
