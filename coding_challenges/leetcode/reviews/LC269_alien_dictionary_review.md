# LC269 — Alien Dictionary

## Why It Is Priority
- repeat count: 3
- bucket: Graphs
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: deduce alien character ordering from sorted word list
- input shape: array of strings `words`
- output: string of characters in correct order (or "" if impossible)
- constraints (inferred if needed): words are sorted lexicographically

## Core Pattern
- topological sort on characters
- build graph by comparing adjacent words to find first differing character
- detect cycles and handle prefix edge cases (e.g., "abc" before "ab" is invalid)

## Recognition Triggers
- "sorted lexicographically", "custom alphabet definition"
- deriving global ordering from pairwise rules
- string comparisons hinting at directed edges between characters

## Correct Approach Outline
1. Initialize `adj` map and `in_degree` map for all unique characters
2. Iterate through adjacent pairs of words `w1`, `w2`
3. If `w1` starts with `w2` and `len(w1) > len(w2)`: return "" (invalid)
4. Find first differing char `c1`, `c2`, add edge `c1 -> c2`, increment `in_degree[c2]`, then break
5. Perform Kahn's BFS topo sort
6. Return joined result if `len(result) == len(in_degree)`, else ""

## Complexity
- time: O(C), where C is total chars across all words
- space: O(1) or O(U), where U is unique chars (at most 26)
- why: graph building compares each char at most once; alphabet size is fixed

## Common Failure Modes
- Forgetting to initialize the graph with ALL unique characters (isolated nodes vanish)
- Missing the prefix edge case (e.g., `["abc", "ab"]` must return "")
- Processing characters beyond the first difference in two words

## Implementation Checklist
- [ ] Initialize `in_degree` to 0 for every character in the input
- [ ] Ensure valid topological sort cycle detection (`len(result) == items`)
- [ ] Break the loop immediately after finding the first differing character
- [ ] Check for prefix invalidity explicitly

## What To Practice Next
- LC210 Course Schedule II (standard topological sort)
- LC332 Reconstruct Itinerary (Eulerian path topo sort)

## Promotion Status
- status: enriched
- source: PracticeHistory
- notes: topological sort applied to string differences

## Pattern Links
- Primary: Graphs (topological sort)
- Secondary: String ordering constraints