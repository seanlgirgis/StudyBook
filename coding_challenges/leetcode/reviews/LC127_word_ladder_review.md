# LC127 — Word Ladder

## Why It Is Priority
- repeat count: 4
- bucket: Graphs
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: find the shortest transformation sequence from beginWord to endWord
- input shape: beginWord, endWord, list of words `wordList`
- output: integer representing number of words in shortest path (0 if none)
- constraints (inferred if needed): transformation means changing exactly 1 letter

## Core Pattern
- BFS for unweighted shortest path
- state space generation by trying all 26 letters for each character position
- early exit when `endWord` is matched

## Recognition Triggers
- "shortest sequence", "minimum steps"
- changing states by small delta (1 letter)
- unweighted graph implicit in state transitions

## Correct Approach Outline
1. Drop `wordList` into a `word_set` for O(1) lookup. Early exit if `endWord` not in set
2. Initialize queue with `(beginWord, 1)` step count
3. While queue is not empty, pop `(word, steps)`
4. For each char index in `word`, try replacing it with 'a' through 'z'
5. If the new `next_word` equals `endWord`, return `steps + 1`
6. If `next_word` in `word_set`, remove it from `word_set` and add `(next_word, steps + 1)` to queue

## Complexity
- time: O(M^2 * N), where M is word length, N is vocab size
- space: O(M * N)
- why: Generating all 26*M variations per word takes O(M^2) with string slicing, doing it N times

## Common Failure Modes
- Building an explicit adjacency list of O(N^2), causing TLE
- Forgetting to remove visited words from the set, leading to cycles/exceeding time
- Returning the wrong step count (number of transformations vs number of words in path)

## Implementation Checklist
- [ ] Convert `wordList` to a set immediately
- [ ] Generate neighbors dynamically via 26 alphabet letters per position
- [ ] Remove `next_word` from `word_set` immediately when adding to queue
- [ ] Return step count starting at 1 for `beginWord`

## What To Practice Next
- LC433 Minimum Genetic Mutation (exact same problem, smaller alphabet)
- LC126 Word Ladder II (requires maintaining paths; much harder implementation)
- LC752 Open the Lock (similar implicit graph BFS)

## Promotion Status
- status: enriched
- source: PracticeHistory
- notes: archetype for implicit graph BFS shortest path

## Pattern Links
- Primary: Graphs (BFS shortest path)
- Secondary: Implicit graph