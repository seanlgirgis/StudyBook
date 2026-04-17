"""
id: lc_0091
title: Decode Ways
source: leetcode
difficulty: medium
primary: dynamic-programming
tags: [dynamic-programming, string, memoization]
leetcode_url: https://leetcode.com/problems/decode-ways/
status: draft
last_updated: 2026-04-16
notes: 
- key idea: 
- time: 
- space: 
"""

# ============================================================================
# File: 091_lc_0091_decode_ways.py
# LeetCode 91: Decode Ways (Medium)
#
# PROBLEM STATEMENT:
# A message containing letters from A-Z can be encoded into numbers using the 
# following mapping:
# 'A' -> "1", 'B' -> "2", ..., 'Z' -> "26"
#
# To decode an encoded message, all the digits must be grouped then mapped back 
# into letters using the reverse of the mapping above (there may be multiple ways).
# For example, "11106" can be mapped into:
# - "AAJF" with the grouping (1 1 10 6)
# - "KJF" with the grouping (11 10 6)
# Note that the grouping (1 11 06) is invalid because "06" cannot be mapped 
# into 'F' since "6" is different from "06".
#
# Given a string s containing only digits, return the number of ways to decode it.
#
# EXAMPLES:
# Example 1:
# Input: s = "12"
# Output: 2
# Explanation: "12" could be decoded as "AB" (1 2) or "L" (12).
#
# Example 2:
# Input: s = "226"
# Output: 3
# Explanation: "226" could be decoded as "BZ" (2 26), "VF" (22 6), or "BBF" (2 2 6).
#
# Example 3:
# Input: s = "06"
# Output: 0
# Explanation: "06" cannot be mapped to "F" because of the leading zero.
# ============================================================================

from typing import List, Callable, Tuple
import copy

# Test cases: (s, expected_output, description)
tests: List[Tuple[str, int, str]] = [
    ("12", 2, "Standard Example 1"),
    ("226", 3, "Standard Example 2"),
    ("06", 0, "Standard Example 3: Leading zero"),
    ("0", 0, "Edge Case: Single zero"),
    ("10", 1, "Edge Case: Valid 10"),
    ("27", 1, "Boundary: Above 26 (single digit only)"),
    ("2101", 1, "Complex: Zero in middle"),
    ("11111", 8, "Stress: Multiple overlapping combinations"),
    ("100", 0, "Edge Case: Double zero invalid"),
    ("30", 0, "Edge Case: Zero after high digit"),
    ("1212", 5, "Stress: Multiple ways"),
    ("1", 1, "Edge Case: Single valid digit"),
]

def harness(func: Callable) -> None:
    print(f"\n--- Running Harness for: {func.__name__} ---")
    passed = 0
    for i, (s_input, expected, desc) in enumerate(tests):
        try:
            # Strings are immutable in Python, so copy() is not strictly needed but 
            # good for consistency with the harness pattern.
            result = func(s_input)
            if result == expected:
                print(f"CASE {i+1} PASSED: {desc}")
                passed += 1
            else:
                print(f"CASE {i+1} FAILED: {desc}")
                print(f"  Input:    '{s_input}'")
                print(f"  Expected: {expected}")
                print(f"  Actual:   {result}")
        except Exception as e:
            print(f"CASE {i+1} ERROR: {desc}")
            print(f"  Exception: {type(e).__name__}: {e}")

    print(f"\nRESULT: {passed}/{len(tests)} cases passed.")

# --- USER TO IMPLEMENT SOLUTION BELOW ---

def numDecodings(s: str) -> int:
    """
    Returns the number of ways to decode the digit string.
    """
    pass

harness(numDecodings)