# LC005 — Longest Palindromic Substring

## Why It Is Priority
- repeat count: 4
- bucket: TwoPointers
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: find the longest substring that is a palindrome
- input shape: string `s`
- output: string (the longest palindrome)
- constraints: 1 <= s.length <= 1000

## Core Pattern
- expand around center
- a palindrome mirrors around its center; centers can be one character (odd length) or two characters (even length)
- check all 2N - 1 possible centers expanding outward

## Recognition Triggers
- "longest palindromic substring"
- contiguous segments requiring symmetry
- input size up to 1000 hints O(N^2) is acceptable

## Correct Approach Outline
1. Define a helper function `expand(left, right)` that expands outwards while characters match and returns the valid length
2. Initialize `start = 0`, `max_len = 0`
3. Loop `i` from 0 to len(s) - 1
4. Find `len1 = expand(i, i)` (odd length palindromes)
5. Find `len2 = expand(i, i + 1)` (even length palindromes)
6. If `max(len1, len2) > max_len`, update `max_len` and compute new `start` index

## Complexity
- time: O(N^2)
- space: O(1)
- why: expanding from ~2N centers takes up to N steps each; no extra allocation until slicing the result

## Common Failure Modes
- Forgetting to check even-length centers (`i, i+1`)
- Out-of-bounds errors while expanding the pointers
- Incorrectly calculating the `start` substring index from the center and max length

## Implementation Checklist
- [ ] expand logic tightly bounds checks: `l >= 0 and r < n and s[l] == s[r]`
- [ ] return `r - l - 1` from expand helper (since pointers push past valid bounds before failing)
- [ ] update `start = i - (longest - 1) // 2` to safely handle both odd and even parity centers

## What To Practice Next
- LC647 Palindromic Substrings
- LC516 Longest Palindromic Subsequence

## Promotion Status
- status: enriched
- source: PracticeHistory
- notes: archetypal expand-around-center string algorithm

## Pattern Links
- Primary: Two Pointers
- Secondary: Strings
