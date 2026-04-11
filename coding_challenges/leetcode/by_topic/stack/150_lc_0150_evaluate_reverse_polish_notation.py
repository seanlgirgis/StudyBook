"""
id: lc_0150
title: Evaluate Reverse Polish Notation
source: leetcode
difficulty: medium
primary: stack
tags: [stack, array, math]
leetcode_url: https://leetcode.com/problems/evaluate-reverse-polish-notation/
status: draft
last_updated: 2026-04-11
notes:
- key idea: 
- time: 
- space: 
"""

# ============================================================================
# File: 150_lc_0150_evaluate_reverse_polish_notation.py
# 150. Evaluate Reverse Polish Notation (Medium)
# 
# PROBLEM STATEMENT:
# You are given an array of strings tokens that represents an arithmetic 
# expression in a Reverse Polish Notation.
#
# Evaluate the expression. Return an integer that represents the value of 
# the expression.
#
# Note that:
# - The valid operators are '+', '-', '*', and '/'.
# - Each operand may be an integer or another expression.
# - The division between two integers always truncates toward zero.
# - There will not be any division by zero.
# - The input represents a valid arithmetic expression in reverse polish notation.
# - The answer and all the intermediate calculations can be represented in a 
#   32-bit integer.
#
# EXAMPLES:
# Example 1:
# Input: tokens = ["2","1","+","3","*"]
# Output: 9
# Explanation: ((2 + 1) * 3) = 9
#
# Example 2:
# Input: tokens = ["4","13","5","/","+"]
# Output: 6
# Explanation: (4 + (13 / 5)) = 6
# ============================================================================

from typing import List, Callable, Tuple
import copy

# Test Cases: (tokens, expected_output)
tests: List[Tuple[List[str], int]] = [
    (["2", "1", "+", "3", "*"], 9),                          # Example 1: Simple add and mult
    (["4", "13", "5", "/", "+"], 6),                         # Example 2: Truncated division
    (["10","6","9","3","+","-11","*","/","*","17","+","5","+"], 22), # Example 3: Complex nested
    (["18"], 18),                                            # Edge: Single element
    (["-1", "1", "+"], 0),                                   # Case: Result is zero
    (["10", "3", "-"], 7),                                   # Case: Basic subtraction
    (["4", "-2", "/"], -2),                                  # Case: Negative result division
    (["1", "2", "+", "3", "4", "+", "*"], 21),               # Case: Parallel operations (1+2)*(3+4)
    (["-128", "128", "*"], -16384),                          # Case: Large negative product
    (["0", "3", "/"], 0),                                    # Case: Zero as numerator
    (["10", "6", "-"], 4),                                   # Case: Positive subtraction result
    (["3", "-4", "+"], -1),                                  # Case: Addition with negative
]

def harness(func: Callable) -> None:
    print(f"Testing: {func.__name__}")
    passed = 0
    for i, (tokens, expected) in enumerate(tests):
        # Deep copy to prevent mutation during test
        arg_copy = copy.deepcopy(tokens)
        try:
            result = func(arg_copy)
            if result == expected:
                status = "PASS"
                passed += 1
            else:
                status = f"FAIL (Expected {expected}, got {result})"
        except Exception as e:
            status = f"ERROR ({type(e).__name__}: {e})"
        
        # Format input display for long arrays
        display_input = str(tokens) if len(tokens) < 8 else f"{str(tokens[:5])[:-1]}...{str(tokens[-2:])[1:]}"
        print(f"Test {i+1:02d}: {status} | Input: {display_input}")
    
    print(f"\nResult: {passed}/{len(tests)} cases passed.")

# --- USER TO IMPLEMENT SOLUTION BELOW ---

def evalRPN(tokens: List[str]) -> int:
    """
    Evaluates the value of an arithmetic expression in Reverse Polish Notation.
    Truncates division toward zero: int(a / b) in Python handles this correctly.
    """
    pass

harness(evalRPN)