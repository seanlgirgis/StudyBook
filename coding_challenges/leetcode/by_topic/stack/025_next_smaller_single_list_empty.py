"""
id: lc_0000
title: Next Smaller Element
source: leetcode
difficulty: medium
primary: stack
tags: [stack, monotonic-stack, arrays]
leetcode_url: https://leetcode.com/problems/next-smaller-element/
status: draft
last_updated: 2026-04-11
notes: 
- key idea: 
- time: 
- space: 
"""

# ============================================================================
# File: 025_next_smaller_single_list_empty.py
#
# Pattern: Next Smaller Element (Single Array / List)
# (Foundation for monotonic stack problems)
#
# PROBLEM STATEMENT:
# Given an array `nums` of integers, find the Next Smaller Element for every 
# element in the array. 
#
# The Next Smaller Element of an element x is the first element to the right 
# of x that is strictly smaller than x. If no such element exists, output -1 
# for that element.
#
# Return an array containing the Next Smaller Element for each corresponding 
# element in the input array.
#
# EXAMPLES:
# 1) nums = [4, 8, 5, 2, 25] -> Expected: [2, 5, 2, -1, -1]
# 2) nums = [13, 7, 6, 12] -> Expected: [7, 6, -1, -1]
# 3) nums = [1, 2, 3, 4] -> Expected: [-1, -1, -1, -1]
# ============================================================================

from typing import Callable, List, Tuple
import copy

# --- TEST CASES ---
# Format: (nums, expected_list)
tests: List[Tuple[List[int], List[int]]] = [
    ([4, 8, 5, 2, 25], [2, 5, 2, -1, -1]),                   # Standard Example 1
    ([13, 7, 6, 12], [7, 6, -1, -1]),                        # Standard Example 2
    ([1, 2, 3, 4], [-1, -1, -1, -1]),                       # Boundary: Strictly increasing
    ([4, 3, 2, 1], [3, 2, 1, -1]),                          # Boundary: Strictly decreasing
    ([], []),                                               # Edge Case: Empty list
    ([5], [-1]),                                            # Edge Case: Single element
    ([2, 2, 2, 2], [-1, -1, -1, -1]),                       # Boundary: All identical elements
    ([3, 1, 2, 4], [1, -1, -1, -1]),                        # Mixed values
    ([10, 3, 12, 4, 2, 9, 13, 8], [3, 2, 4, 2, -1, 8, 8, -1]), # Complex: Multiple valleys
    ([5, 2, -10, -11], [2, -10, -11, -1]),                  # Negative numbers
    ([1, 10, 1, 10, 1], [-1, 1, -1, 1, -1]),                # Oscillating values
    ([100, 50, 100, 40], [50, 40, 40, -1]),                 # Repetitive jumps
]

def harness(func: Callable) -> None:
    passed = 0
    for i, (nums, expected) in enumerate(tests):
        # Deep copy to protect the test suite from in-place mutations
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

# --- USER TO IMPLEMENT SOLUTION BELOW ---

def nextSmallerElement(nums: List[int]) -> List[int]:
    # Solution has to involve mono increasing stack .. means evict larger  items from stack as smaller ones arrive
    n = len(nums)
    out = [-1] * n
    stack = []                              # store (index, val)
    for i, val in enumerate(nums):
        #evict first
        while stack and stack[-1][1] > val:
            idx, _ = stack.pop()
            out[idx] = val
        stack.append((i, val))
    return out

harness(nextSmallerElement)