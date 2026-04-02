# LC010 — Regular Expression Matching

## Why It Is Priority
- repeat count: 3
- bucket: DP
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: implement regular expression matching with support for '.' (any single char) and '*' (zero or more of preceding element)
- input shape: string `s` (text), string `p` (pattern)
- output: boolean
- constraints: overlapping '*' are well-formed

## Core Pattern
- 2D dynamic programming (or memoized DFS)
- match the string and pattern recursively
- handle '*' by branching: either use the '*' to consume 0 of preceding char, or if current char matches, consume 1 of text char

## Recognition Triggers
- "regular expression", "wildcard matching"
- multiple valid ways to advance pointers (branching choices)
- checking sequence validity against structural rules

## Correct Approach Outline
1. Initialize a 2D DP table size `(len(s)+1) x (len(p)+1)` set to False
2. DP base case: `dp[0][0] = True` (empty string matches empty pattern)
3. Pre-fill row 0 for patterns that can match empty string (like `a*b*`)
4. Iterate `i` from 1 to `len(s)` and `j` from 1 to `len(p)`
5. If `p[j-1]` is a normal char or `.`, `dp[i][j] = dp[i-1][j-1]` AND characters match
6. If `p[j-1]` is `*`, `dp[i][j] = dp[i][j-2]` (match zero) OR (`dp[i-1][j]` AND text bound char matches preceding rule char)

## Complexity
- time: O(S * P)
- space: O(S * P)
- why: computing a 2D DP table of size S x P, each cell takes O(1) transitions

## Common Failure Modes
- Failing to initialize `dp[0][j]` for patterns that safely evaluate to empty (`a*`)
- Confusing the `*` character's indexing (it applies to `p[j-2]`)
- Array out-of-bounds indexing or offset mismatch between strings and DP table

## Implementation Checklist
- [ ] initialize DP grid correctly with boundary +1 dimensions
- [ ] `match(i, j)` helper or inline logic for: `s[i-1] == p[j-1] or p[j-1] == '.'`
- [ ] handle `*` 0-occurrence case first: `dp[i][j-2]`
- [ ] handle `*` 1+ occurrence case second, verifying preceding char matches current text char

## What To Practice Next
- LC044 Wildcard Matching
- LC072 Edit Distance

## Promotion Status
- status: enriched
- source: PracticeHistory
- notes: classic 2D DP sequence matching

## Pattern Links
- Primary: Dynamic Programming
- Secondary: Strings
