# LC003 — Longest Substring Without Repeating Characters

## Why It Is Priority
- repeat count: 4
- bucket: SlidingWindow
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: find the length of the longest substring without repeating characters
- input shape: string `s`
- output: integer representing maximum length
- constraints: 0 <= s.length <= 5 * 10^4, consists of English letters, digits, symbols, spaces

## Core Pattern
- sliding window / two pointers with hash map
- expand `right` pointer to include characters
- shrink `left` pointer when a duplicate character is encountered to maintain the "no repeat" invariant

## Recognition Triggers
- "longest substring"
- "without repeating characters"
- sequence optimization needing O(N) performance

## Correct Approach Outline
1. Initialize `char_index_map` to track the most recent index of each character
2. Initialize `left_pointer = 0` and `max_len = 0`
3. Iterate `right_pointer` over the string
4. If `s[right_pointer]` is in `char_index_map` AND its mapped index is >= `left_pointer`, update `left_pointer = char_index_map[s[right_pointer]] + 1`
5. Update `char_index_map[s[right_pointer]] = right_pointer`
6. Update `max_len = max(max_len, right_pointer - left_pointer + 1)`

## Complexity
- time: O(N)
- space: O(min(M, N)) (M is alphabet size, up to 128 for ASCII)
- why: `right_pointer` traverses once, hash map updates in O(1)

## Common Failure Modes
- Not verifying if the previously seen duplicate is actually inside the current window (`index >= left_pointer`)
- Shrinking `left_pointer` iteratively instead of jumping it directly to `duplicate_index + 1` (slower, but works)
- Mishandling empty strings

## Implementation Checklist
- [ ] check for empty string upfront (optional, loop handles it gracefully)
- [ ] ensure `left_pointer` only moves forward (`max(left, map[char] + 1)`)
- [ ] update character's index in map unconditionally
- [ ] compute length using inclusive formula `right - left + 1`

## What To Practice Next
- LC424 Longest Repeating Character Replacement
- LC076 Minimum Window Substring
- LC159 Longest Substring with At Most Two Distinct Characters

## Promotion Status
- status: enriched
- source: PracticeHistory
- notes: fundamental dynamic sliding window pattern

## Pattern Links
- Primary: Sliding Window
- Secondary: Hash Map
