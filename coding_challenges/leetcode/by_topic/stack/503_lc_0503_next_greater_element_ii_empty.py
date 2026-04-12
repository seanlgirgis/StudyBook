"""
id: lc_0503
title: Next Greater Element II
source: leetcode
difficulty: medium
primary: stack
tags: [stack, monotonic-stack, arrays, circular-array]
leetcode_url: https://leetcode.com/problems/next-greater-element-ii/
status: draft
last_updated: 2026-04-11
notes: 
- key idea: Use a monotonic stack and simulate a circular array by iterating through the array twice (using i % n).
- time: O(n)
- space: O(n)
"""

# ============================================================================
# File: 503_lc_0503_next_greater_element_ii_empty.py
#
# LeetCode 503: Next Greater Element II
# Difficulty: Medium
#
# PROBLEM STATEMENT:
# Given a circular integer array `nums` (i.e., the next element of 
# `nums[nums.length - 1]` is `nums[0]`), return the next greater number for 
# every element in `nums`.
#
# The next greater number of an element x is the first greater number to its 
# traversing-order next in the array, which means you could search circularly 
# to find its next greater number. If it doesn't exist, return -1 for this 
# number.
#
# EXAMPLES:
# 1) nums = [1, 2, 1] -> Expected: [2, -1, 2]
#    Explanation: The first 1's next greater is 2; 
#    2's next greater doesn't exist; 
#    The last 1's next greater is 2 (circularly).
#
# 2) nums = [1, 2, 3, 4, 3] -> Expected: [2, 3, 4, -1, 4]
# ============================================================================

from typing import Callable, List, Tuple
import copy

# --- TEST CASES ---
# Format: (nums, expected_output)
tests: List[Tuple[List[int], List[int]]] = [
    ([1, 2, 1], [2, -1, 2]),                             # Example 1
    ([1, 2, 3, 4, 3], [2, 3, 4, -1, 4]),                 # Example 2
    ([5, 4, 3, 2, 1], [-1, 5, 5, 5, 5]),                 # Boundary: Strictly decreasing
    ([1, 2, 3, 4, 5], [2, 3, 4, 5, -1]),                 # Boundary: Strictly increasing
    ([1, 1, 1, 1], [-1, -1, -1, -1]),                    # Boundary: All identical
    ([1], [-1]),                                         # Edge Case: Single element
    ([], []),                                            # Edge Case: Empty list
    ([10, 2, 10, 2], [-1, 10, -1, 10]),                  # Complex: Alternating peaks
    ([-1, -2, -3], [-1, -1, -1]),                        # Negative numbers
    ([3, 8, 4, 1, 2], [8, -1, 8, 2, 3]),                 # Random distribution
    ([2, 3, 1], [3, -1, 2]),                             # Small circular wrap
    ([1, 5, 2, 4, 3], [5, -1, 4, 5, 5]),                 # Multiple jumps over the end
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

# --- USER TO IMPLEMENT SOLUTION BELOW ---
from collections import deque
def nextGreaterElements(nums: List[int]) -> List[int]:
    
    n = len(nums)
    out = [-1] * n
    stack = []
    # uise mono increasing stack evict smaller numbers as bigger one comes in
    for j in range(2 * n):
        i = j % n
        val = nums[i]
        while stack and stack[-1][1] < val:
            idx, _ = stack.pop()
            out[idx] = val
        stack.append((i, val))
    return out
        
        
            
        
    
    
    

harness(nextGreaterElements)