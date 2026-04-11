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
# LC020: Valid Parentheses (Easy)
#
# PROBLEM STATEMENT:
# Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', 
# determine if the input string is valid.
#
# An input string is valid if:
# 1. Open brackets must be closed by the same type of brackets.
# 2. Open brackets must be closed in the correct order.
# 3. Every close bracket has a corresponding open bracket of the same type.
#
# EXAMPLES:
# Input: s = "()" -> Output: true
# Input: s = "()[]{}" -> Output: true
# Input: s = "(]" -> Output: false
# ============================================================================

from typing import Callable, List, Tuple

# Test Cases: (input_string, expected_output)
tests: List[Tuple[str, bool]] = [
    ("()", True),                       # Example 1: Simple pair
    ("()[]{}", True),                   # Example 2: Multiple valid pairs
    ("(]", False),                      # Example 3: Mismatched types
    ("([])", True),                     # Nested valid brackets
    ("", True),                         # Edge Case: Empty string
    ("[", False),                       # Edge Case: Single opening
    ("]", False),                       # Edge Case: Single closing
    ("((((()))))", True),               # Deeply nested same type
    ("([)]", False),                    # Wrong order of closing
    ("((())", False),                   # Unbalanced: extra opening
    ("()))", False),                    # Unbalanced: extra closing
    ("{[()]}", True),                   # Complex nested valid
    ("{{{{", False),                    # Multiple same-type opening
    ("]]]]", False),                    # Multiple same-type closing
]

def harness(func: Callable) -> None:
    passed = 0
    for i, (s, expected) in enumerate(tests):
        # Strings are immutable, no deep copy needed
        try:
            result = func(s)
            if result == expected:
                print(f"Test {i+1}: PASSED | Input: '{s}'")
                passed += 1
            else:
                print(f"Test {i+1}: FAILED | Input: '{s}' | Expected: {expected}, Got: {result}")
        except Exception as e:
            print(f"Test {i+1}: ERROR  | Input: '{s}' | {type(e).__name__}: {e}")
    
    print(f"\nSummary: {passed}/{len(tests)} tests passed.")

# --- USER TO IMPLEMENT SOLUTION BELOW ---

def isValid(s: str) -> bool:
    """
    Determines if the input string of parentheses is valid using a stack-based approach.
    """
    lookup = {'}':'{' , ']':'[', ')':'('}
    stack= []
    
    

harness(isValid)