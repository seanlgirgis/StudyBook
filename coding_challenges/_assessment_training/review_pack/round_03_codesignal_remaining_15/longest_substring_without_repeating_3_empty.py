# LeetCode 3: Longest Substring Without Repeating Characters (Empty)
#
# PROBLEM STATEMENT
# Given a string `s`, return the length of the longest substring without repeating characters.
# A substring is contiguous.
#
# EXAMPLES
# 1) s = "abcabcbb" -> 3 ("abc")
# 2) s = "bbbbb" -> 1 ("b")
#
# WHAT TO IMPLEMENT
# Implement `lengthOfLongestSubstring(s)` in O(n) time (sliding window).
from typing import Callable, List, Tuple

tests: List[Tuple[str, int]] = [
    ("abcabcbb", 3),
    ("bbbbb", 1),
    ("pwwkew", 3),
    ("", 0),
    ("dvdf", 3),
    ("abba", 2),
    ("tmmzuxt", 5),
    ("au", 2),
    (" ", 1),
]

def harness(func: Callable[[str], int]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (s, expected) in enumerate(tests, 1):
        try:
            got = func(s)
            if got == expected: print(f"Test {i}: PASSED"); passed += 1
            else: print(f"Test {i}: FAILED | expected={expected}, got={got}")
        except Exception as e:
            print(f"Test {i}: ERROR | {type(e).__name__}: {e}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.")

def lengthOfLongestSubstring(s: str) -> int:
    if len(s) <= 1: return len(s)
    ret = 1
    seen = {s[0]}
    l = 0
    for r in range(1, len(s)):
        while s[r] in seen and l <= r:
            seen.remove(s[l])
            l+=1
        seen.add(s[r])
        ret = max(ret, r-l+1)
    return ret
    
harness(lengthOfLongestSubstring)

