"""
id: lc_0496
title: Next Greater Element I
source: leetcode
difficulty: easy
primary: stack
tags: [stack, monotonic-stack, arrays]
leetcode_url: https://leetcode.com/problems/next-greater-element-i/
status: draft
last_updated: 2026-04-11
notes: 
- key idea: 
- time: 
- space: 
"""

# ============================================================================
# File: 024_next_greater_single_list_empty.py
#
# Pattern: Next Greater Element (Single Array / List)
# (Foundation for LeetCode 496, 503, 739)
#
# PROBLEM STATEMENT:
# Given an array `nums` of integers, find the Next Greater Element for every 
# element in the array. 
#
# The Next Greater Element of an element x is the first element to the right 
# of x that is strictly greater than x. If no such element exists, output -1 
# for that element.
#
# Return an array containing the Next Greater Element for each corresponding 
# element in the input array.
#
# EXAMPLES:
# 1) nums = [4, 5, 2, 25] -> Expected: [5, 25, 25, -1]
# 2) nums = [13, 7, 6, 12] -> Expected: [-1, 12, 12, -1]
# 3) nums = [1, 2, 3, 4] -> Expected: [2, 3, 4, -1]
# ============================================================================

from typing import Callable, List, Tuple
import copy

# --- TEST CASES ---
# Format: (nums, expected_list)
tests: List[Tuple[List[int], List[int]]] = [
    ([4, 5, 2, 25], [5, 25, 25, -1]),                 # Standard Example 1
    ([13, 7, 6, 12], [-1, 12, 12, -1]),               # Standard Example 2
    ([1, 2, 3, 4], [2, 3, 4, -1]),                    # Boundary: Strictly increasing
    ([4, 3, 2, 1], [-1, -1, -1, -1]),                 # Boundary: Strictly decreasing
    ([], []),                                         # Edge Case: Empty list
    ([5], [-1]),                                      # Edge Case: Single element
    ([2, 2, 2, 2], [-1, -1, -1, -1]),                 # Boundary: All identical elements
    ([3, 1, 2, 4], [4, 2, 4, -1]),                    # Mixed values
    ([10, 3, 12, 4, 2, 9, 13, 8], [12, 12, 13, 9, 9, 13, -1, -1]), # Complex: Multiple peaks
    ([-5, -2, -10, -1], [-2, -1, -1, -1]),            # Negative numbers
    ([1, 5, 2, 7, 3, 8], [5, 7, 7, 8, 8, -1]),        # Alternating heights
    ([100, 1, 1, 1, 101], [101, 101, 101, 101, -1]),  # Distant greater element
    
    ([4, 5, 2, 25], [5, 25, 25, -1]),                        # Standard Example 1
    ([13, 7, 6, 12], [-1, 12, 12, -1]),                      # Standard Example 2
    ([1, 2, 3, 4], [2, 3, 4, -1]),                           # Boundary: Strictly increasing
    ([4, 3, 2, 1], [-1, -1, -1, -1]),                        # Boundary: Strictly decreasing
    ([], []),                                                # Edge Case: Empty list
    ([5], [-1]),                                             # Edge Case: Single element
    ([2, 2, 2, 2], [-1, -1, -1, -1]),                        # Boundary: All identical elements
    ([3, 1, 2, 4], [4, 2, 4, -1]),                           # Mixed values
    ([10, 3, 12, 4, 2, 9, 13, 8], [12, 12, 13, 9, 9, 13, -1, -1]), # Complex array with multiple peaks
    ([-5, -2, -10, -1], [-2, -1, -1, -1]),                   # Negative numbers
]

def harness(func: Callable) -> None:
    passed = 0
    for i, (nums, expected) in enumerate(tests):
        # Prevent mutation of test data
        input_copy = copy.deepcopy(nums)
        try:
            result = func(input_copy)
            if result == expected:
                print(f"Test {i+1}: PASSED")
                passed += 1
            else:
                input_disp = str(nums) if len(str(nums)) < 50 else str(nums)[:47] + "..."
                print(f"Test {i+1}: FAILED | Input: {input_disp} | Expected: {expected}, Got: {result}")
        except Exception as e:
            print(f"Test {i+1}: ERROR  | Input: {nums} | Exception: {e}")
    
    print(f"\nSummary: {passed}/{len(tests)} tests passed.")

    
#Next greater element requires a mono decreasing stack
#Mono decreasing stack requires evicting smaller items before inserting    
def nextGreaterElement(nums: List[int]) -> List[int]:
    n = len(nums)
    out = [-1] * n
    stack = []                        # self decreasing stack evict smaller items from stack before adding 
    for i, val in enumerate(nums):
        while stack and stack[-1][1] < val:
            idx, _ = stack.pop()
            out[idx] = val
        stack.append((i, val))
    return out

harness(nextGreaterElement)