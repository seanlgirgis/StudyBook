# ============================================================================
# File: longest_substring_without_repeating_003_empty.py
#
# LeetCode 3: Longest Substring Without Repeating Characters (Medium)
#
# PROBLEM STATEMENT:
# Given a string s, find the length of the longest substring without repeating characters.
#
# EXAMPLES:
# 1) s = "abcabcbb" -> Expected: 3
#    Explanation: The answer is "abc", with the length of 3.
# 2) s = "bbbbb" -> Expected: 1
#    Explanation: The answer is "b", with the length of 1.
# 3) s = "pwwkew" -> Expected: 3
#    Explanation: The answer is "wke", with the length of 3.
#    Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.
# ============================================================================

from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (s, expected_length)
tests: List[Tuple[str, int]] = [
    ("abcabcbb", 3),                         # Standard Example 1
    ("bbbbb", 1),                            # Standard Example 2
    ("pwwkew", 3),                           # Standard Example 3
    ("", 0),                                 # Edge case: Empty string
    (" ", 1),                                # Edge case: Single space
    ("au", 2),                               # Edge case: Two distinct characters
    ("dvdf", 3),                             # Boundary: Requires sliding window to jump correctly
    ("tmmzuxt", 5),                          # Boundary: Duplicate jump logic check
    ("abcdefghijklmnopqrstuvwxyz", 26),      # Boundary: All unique characters
    ("aab", 2),                              # Boundary: Duplicate at start
    ("baa", 2),                              # Boundary: Duplicate at end
    ("abba", 2),                             # Tricky: Left pointer must not move backward
    ("anviaj", 5),                           # Tricky: Non-adjacent repeat
    ("😀😃😄😁😆😅😂🤣😊😇", 10),           # Unicode unique characters
    ("0123456789!@#$%^&*()", 20),            # Boundary: Non-alphabet characters
]

# --- TEST HARNESS ---
def harness(func: Callable[[str], int]) -> None:
    """
    Test harness for LeetCode #3: Longest Substring Without Repeating Characters.
    """
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0

    def oracle_longest_unique_substring_len(text: str) -> int:
        """Brute-force oracle used only by harness to validate expected values."""
        best = 0
        n = len(text)
        for i in range(n):
            seen = set()
            for j in range(i, n):
                if text[j] in seen:
                    break
                seen.add(text[j])
                best = max(best, j - i + 1)
        return best
    
    for i, (s, expected) in enumerate(tests, 1):
        try:
            got = func(s)

            if not isinstance(got, int):
                raise AssertionError(f"Output must be int. got={type(got).__name__}")
            if got < 0 or got > len(s):
                raise AssertionError(f"Output out of valid range [0, {len(s)}]. got={got}")

            oracle = oracle_longest_unique_substring_len(s)
            if expected != oracle:
                raise AssertionError(f"Bad test expectation: expected={expected}, oracle={oracle}")
            
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                s_disp = f"'{s}'" if len(s) <= 15 else f"'{s[:12]}...'"
                print(f"Test {i}: FAILED | expected={expected}, got={got} | s={s_disp}")
        except Exception as e:
            s_disp = f"'{s}'" if len(s) <= 15 else f"'{s[:12]}...'"
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | s={s_disp}")
            
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def lengthOfLongestSubstring(s: str) -> int:
    if len(s) <= 1:
        return len(s)

    seen = set()
    l, max_len = 0, 0

    for r, ch in enumerate(s):
        while ch in seen:
            seen.remove(s[l])
            l += 1

        seen.add(ch)
        max_len = max(max_len, r - l + 1)

    return max_len


# Execute harness without __main__ block
harness(lengthOfLongestSubstring)
