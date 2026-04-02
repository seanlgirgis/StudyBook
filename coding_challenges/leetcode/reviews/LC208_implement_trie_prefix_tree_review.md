# LC208 — Implement Trie (Prefix Tree)

## Why It Is Priority
- repeat count: 4
- bucket: Trees
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: design a Trie supporting insert, full-word search, and prefix checks
- input shape: sequence of lowercase string operations (`insert`, `search`, `startsWith`)
- output: boolean results for query operations
- constraints (inferred if needed): optimize by character path length, not number of stored words

## Core Pattern
- Prefix tree where each edge represents one character transition.
- Node stores child links and an end-of-word marker.
- Operations reduce to deterministic character-path traversal.

## Recognition Triggers
- Requires both full-word lookup and prefix lookup.
- Many string keys share common prefixes.
- Frequent insert/query operations over dictionary-like words.
- Need faster-than-linear-per-word-list checks by prefix depth.

## Correct Approach Outline
1. Represent each node with child map/array and an `is_end` flag.
2. `insert`: walk/create child nodes for each char, then mark end flag.
3. `search`: walk path; return true only if path exists and end flag is set.
4. `startsWith`: walk prefix path; return true if traversal succeeds.

## Complexity
- time: O(L) per operation (`insert`, `search`, `startsWith`)
- space: O(total characters inserted)
- why: each operation traverses at most one node per input character.

## Common Failure Modes
- treating path existence as full-word match without `is_end`
- marking every traversed node as word-end during insert
- applying full-word end check inside `startsWith`
- failing when one word is prefix of another (`app` vs `apple`)

## Implementation Checklist
- [ ] keep `is_end` separate from path existence
- [ ] create missing nodes only during `insert`
- [ ] fail fast when required child link is absent
- [ ] do not require `is_end` for `startsWith`
- [ ] test shared-prefix words (e.g., `app`, `apple`)

## What To Practice Next
- [LC211 Design Add and Search Words Data Structure](https://leetcode.com/problems/design-add-and-search-words-data-structure/)
- [LC212 Word Search II](https://leetcode.com/problems/word-search-ii/)
- [LC720 Longest Word in Dictionary](https://leetcode.com/problems/longest-word-in-dictionary/)

## Promotion Status
- status: in-progress
- source: PracticeHistory
- notes: priority pass filled for trie-recognition and operation semantics


## Pattern Links
- Primary: Trie
