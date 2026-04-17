"""
id: lc_0139
title: Word Break
source: leetcode
difficulty: medium
primary: dynamic programming
tags: [string, hash-table, dynamic-programming, trie, memoization]
leetcode_url: https://leetcode.com/problems/word-break/
status: draft
last_updated: 2026-04-17
notes: 
- key idea: 
- time: 
- space: 
"""

# ============================================================================
# File: 139_lc_0139_word_break_empty.py
# LC 139: Word Break (Medium)
# 
# PROBLEM STATEMENT:
# Given a string s and a dictionary of strings wordDict, return true if s can 
# be segmented into a space-separated sequence of one or more dictionary words.
# 
# Note that the same word in the dictionary may be reused multiple times in 
# the segmentation.
# 
# EXAMPLES:
# Example 1:
# Input: s = "leetcode", wordDict = ["leet", "code"]
# Output: true
# Explanation: Return true because "leetcode" can be segmented as "leet code".
# 
# Example 2:
# Input: s = "applepenapple", wordDict = ["apple", "pen"]
# Output: true
# Explanation: Return true because "applepenapple" can be segmented as "apple pen apple".
# 
# Example 3:
# Input: s = "catsandog", wordDict = ["cats", "dog", "sand", "and", "cat"]
# Output: false
# ============================================================================

from typing import List, Callable, Tuple

# Test cases: (s, wordDict, expected_output, description)
tests: List[Tuple[str, List[str], bool, str]] = [
    ("leetcode", ["leet", "code"], True, "Example 1: Basic split"),
    ("applepenapple", ["apple", "pen"], True, "Example 2: Reusing words"),
    ("catsandog", ["cats", "dog", "sand", "and", "cat"], False, "Example 3: Impossible segmentation"),
    ("a", ["a"], True, "Edge Case: Single character match"),
    ("a", ["b"], False, "Edge Case: Single character mismatch"),
    ("aaaaaaa", ["aaaa", "aaa"], True, "Overlap: Multiple ways to partition"),
    ("goalspecial", ["go", "goal", "goals", "special"], True, "Prefix overlap: goal vs goals"),
    ("bb", ["a", "b", "bbb", "bbbb"], True, "Short match in long dict"),
    ("", ["apple"], False, "Edge Case: Empty string (usually False per constraints)"),
    ("ab", ["a", "b"], True, "Multiple single characters"),
    ("bccdbacdb", ["bc", "cd", "db", "ac"], False, "Complex sequence (odd length with only 2-char tokens)"),
    ("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab", 
     ["a","aa","aaa","aaaa","aaaaa","aaaaaa","aaaaaaa","aaaaaaaa","aaaaaaaaa","aaaaaaaaaa"], 
     False, "Stress Test: TLE Prevention (Exponential recursion check)")
]

def harness(func: Callable) -> None:
    print(f"\n--- Running Harness for: {func.__name__} ---")
    passed = 0
    for i, (s, word_dict, expected, desc) in enumerate(tests):
        # Deep copy for safety, though strings/bools are immutable, the list isn't
        dict_copy = word_dict[:]
        
        try:
            result = func(s, dict_copy)
            if result == expected:
                print(f"Test {i+1}: PASSED | {desc}")
                passed += 1
            else:
                print(f"Test {i+1}: FAILED | {desc}")
                print(f"   Input: s='{s}', dict={word_dict}")
                print(f"   Expected: {expected}, Got: {result}")
        except Exception as e:
            print(f"Test {i+1}: ERROR  | {desc}")
            print(f"   Exception: {e}")
            
    print(f"\nSummary: {passed}/{len(tests)} cases passed.")

# --- USER TO IMPLEMENT SOLUTION BELOW ---

def word_break(s: str, wordDict: List[str]) -> bool:
    if s == "": return False
    word_set = set(wordDict)
    dp = [False] * (len(s) + 1)
    dp[0] = True                    # empty prefix is segmentable
    for r in range(1, len(s) + 1):
        for l in range(r):
            if dp[l] and s[l:r] in word_set:
                dp[r] = True
                break               # segment ending at r found
    return dp[len(s)]

harness(word_break)
