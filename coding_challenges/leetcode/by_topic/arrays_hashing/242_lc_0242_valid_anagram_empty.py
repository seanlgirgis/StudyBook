"""
id: lc_0242
title: Valid Anagram
source: leetcode
difficulty: easy
primary: hash-table
tags: [hash-table, strings, sorting]
leetcode_url: https://leetcode.com/problems/valid-anagram/
status: draft
last_updated: 2026-04-11
notes: 
- key idea: Use a hash map (or fixed-size array) to count character frequencies and compare.
- time: O(n)
- space: O(1) if restricted to lowercase English alphabet, else O(k) for unique characters.
"""

# ============================================================================
# File: 242_lc_0242_valid_anagram_empty.py
# Problem 242: Valid Anagram (Easy)
# 
# PROBLEM STATEMENT:
# Given two strings s and t, return true if t is an anagram of s, and false 
# otherwise.
#
# An Anagram is a word or phrase formed by rearranging the letters of a 
# different word or phrase, typically using all the original letters exactly once.
#
# EXAMPLES:
# Input: s = "anagram", t = "nagaram"
# Output: true
#
# Input: s = "rat", t = "car"
# Output: false
# ============================================================================

from typing import List, Tuple, Callable

# Test Cases: List[Tuple[s, t, expected]]
tests: List[Tuple[str, str, bool]] = [
    ("anagram", "nagaram", True),        # Standard Example 1
    ("rat", "car", False),               # Standard Example 2
    ("a", "a", True),                    # Edge Case: Single character match
    ("a", "b", False),                   # Edge Case: Single character mismatch
    ("", "", True),                      # Edge Case: Empty strings
    ("ab", "a", False),                  # Boundary: Different lengths
    ("aabbcc", "abcabc", True),          # Multiple frequencies
    ("aaabbb", "ababab", True),          # Interleaved characters
    ("awesome", "asweome", True),        # Direct rearrangement
    ("apple", "aplee", False),           # Same letters, different counts
    ("bookkeeper", "keebokeerp", False),  # Long word with repeated letters
    ("a" * 1000 + "b", "b" + "a" * 1000, True), # Stress: Large matching strings
]

def harness(func: Callable) -> None:
    passed = 0
    failed = 0
    
    print(f"\n--- Testing: {func.__name__} ---")
    
    for i, (s, t, expected) in enumerate(tests):
        try:
            # Strings are immutable, no deep copy needed
            result = func(s, t)
            
            display_input = f"s='{s}', t='{t}'"
            if len(display_input) > 60:
                display_input = display_input[:57] + "..."
            
            if result == expected:
                print(f"Test {i+1}: PASSED | {display_input}")
                passed += 1
            else:
                print(f"Test {i+1}: FAILED | {display_input}")
                print(f"   Expected: {expected}, Got: {result}")
                failed += 1
        except Exception as e:
            print(f"Test {i+1}: ERROR  | s='{s}', t='{t}'")
            print(f"   Exception: {e}")
            failed += 1
            
    print(f"\nResults: {passed} Passed, {failed} Failed\n")

# --- USER TO IMPLEMENT SOLUTION BELOW ---

def isAnagram(s: str, t: str) -> bool:
    """
    Returns True if t is an anagram of s.
    """
    counts = [0] * 26
    for ch in s:
        counts[ord(ch) - ord('a')] += 1
    for ch in t:
        counts[ord(ch) - ord('a')] -= 1
    
    
    return not any(counts)

harness(isAnagram)