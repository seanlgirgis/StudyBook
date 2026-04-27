# Algorithms & Data Structures: The "Cheat Sheet"

## 1. Arrays & Hashing
**Key Insight:** Accessing an array by index is `O(1)`. Searching is `O(N)`. We use Hash Maps (Dictionaries) to make searching `O(1)`.

### Patterns
*   **Frequency Map (`Counter`):** Count how many times items appear.
    *   *Used in:* Valid Anagram, Top K Frequent.
    *   *Code:* `count = collections.Counter(nums)`
*   **Hash Map for Lookup:** Store `{value: index}` to find complements instantly.
    *   *Used in:* Two Sum.
    *   *Concept:* `target - current_val` in `map`?
*   **Sorting as a Key:** Anagrams have the same sorted characters.
    *   *Used in:* Group Anagrams.
    *   *Key:* `tuple(sorted(s))`

---

## 2. Two Pointers
**Key Insight:** For **Sorted Arrays** or filtering tasks, use two indices (`left`, `right`) to scan the data in `O(N)` instead of nested loops `O(N^2)`.

### Patterns
*   **Convergence:** Start at ends, move towards middle.
    *   *Used in:* Valid Palindrome, Two Sum II (Sorted), Container With Most Water.
    *   *Logic:*
        *   Sum too small? `left += 1` (Increase sum).
        *   Sum too big? `right -= 1` (Decrease sum).
*   **Iterator Pair:** Start both at 0, move one faster/slower (not covered yet, but used in linked lists).

### tricky Cases
*   **3Sum:** Fix one number (`i`), then run Two Sum II on the rest. **Critical:** Skip duplicates to result unique triplets.

---

## 3. Sliding Window
**Key Insight:** When looking for a "Subarray" or "Substring" that satisfies a condition, expand `right` to include data, and shrink `left` when the condition breaks.

### Patterns
*   **Variable Window:**
    *   *Used in:* Longest Substring Without Repeating Characters.
    *   *Logic:*
        *   `seen` map stores `{char: index}`.
        *   If `s[right]` is in `seen`, jump `left` to `seen[s[right]] + 1`.
        *   Updates `max_len` at every step.
*   **Fixed Window:** (e.g. Max sum of subarray of size K) - We maintain a running sum.

---

## 4. Stack (LIFO)
**Key Insight:** Last In, First Out. Great for matching pairs (nested structures) or tracking "previous" state.

### Patterns
*   **Matching Parentheses:**
    *   *Used in:* Valid Parentheses.
    *   *Logic:* Push openers `(`, pop and match closers `)`. Stack must be empty at end.
