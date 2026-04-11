"""
id: lc_0020
title: Valid Parentheses
source: leetcode
difficulty: easy
primary: stack
tags: [stack, string]
leetcode_url: https://leetcode.com/problems/valid-parentheses/
status: draft
last_updated: 2026-04-11
notes:
- key idea:
- time:
- space:
"""

# ============================================================================
# File: 020_lc_0020_valid_parentheses.py
# Problem 20: Valid Parentheses (Easy)
#
# Problem Statement:
# Given a string s containing just the characters '(', ')', '{', '}', '[' and
# ']', determine if the input string is valid.
#
# An input string is valid if:
#   1. Open brackets must be closed by the same type of brackets.
#   2. Open brackets must be closed in the correct order.
#   3. Every close bracket has a corresponding open bracket of the same type.
#
# Constraints:
# - 1 <= s.length <= 10^4
# - s consists of parentheses only '()[]{}'
#
# Examples:
# Example 1:
# Input: s = "()"
# Output: True
#
# Example 2:
# Input: s = "()[]{}"
# Output: True
#
# Example 3:
# Input: s = "(]"
# Output: False
# ============================================================================

from typing import Callable, List, Tuple

# Test Suite: (Input, Expected Output)
tests: List[Tuple[str, bool]] = [
    ("()",         True),    # Example 1: Simple pair
    ("()[]{}",     True),    # Example 2: Multiple valid pairs
    ("(]",         False),   # Example 3: Mismatched types
    ("([])",       True),    # Nested valid brackets
    ("",           True),    # Edge Case: Empty string
    ("[",          False),   # Edge Case: Single opening
    ("]",          False),   # Edge Case: Single closing
    ("((((()))))", True),    # Deeply nested same type
    ("([)]",       False),   # Wrong order of closing
    ("((())",      False),   # Unbalanced: extra opening
    ("()))",       False),   # Unbalanced: extra closing
    ("{[()]}",     True),    # Complex nested valid
    ("{{{{",       False),   # Multiple same-type opening
    ("]]]]",       False),   # Multiple same-type closing
]

def harness(func: Callable) -> None:
    passed = 0
    failed = 0

    print(f"--- Running Tests for: {func.__name__} ---")

    for i, (s, expected) in enumerate(tests):
        try:
            actual = func(s)
            if actual == expected:
                status = "PASSED"
                passed += 1
            else:
                status = f"FAILED (Expected {expected}, got {actual})"
                failed += 1
        except Exception as e:
            status = f"ERROR ({type(e).__name__}: {e})"
            failed += 1

        display_input = f"'{s}'" if len(s) < 50 else f"'{s[:47]}...'"
        print(f"Test {i+1:02d}: {status} | Input: {display_input}")

    print(f"\n--- Result: {passed} Passed, {failed} Failed ---")

# --- USER TO IMPLEMENT SOLUTION BELOW ---

def isValid(s: str) -> bool:
    lookup = {'}': '{', ']': '[', ')': '('}
    stack = []

    for ch in s:
        if ch in lookup:
            if stack and stack[-1] == lookup[ch]:
                stack.pop()
                continue
            else:
                return False

        stack.append(ch)

    return not stack


harness(isValid)
