"""
id: lc_0496
title: Next Greater Element I
source: leetcode
difficulty: easy
primary: stack
tags: [stack, hash-table, monotonic-stack, arrays]
leetcode_url: https://leetcode.com/problems/next-greater-element-i/
status: draft
last_updated: 2026-04-11
notes: 
- key idea: 
- time: 
- space: 
"""

# ============================================================================
# File: 496_lc_0496_next_greater_element_i_empty.py
# LC496: Next Greater Element I (Easy)
#
# PROBLEM STATEMENT:
# The next greater element of some element x in an array is the first greater 
# element that is to the right of x in the same array.
#
# You are given two distinct 0-indexed integer arrays nums1 and nums2, where 
# nums1 is a subset of nums2.
#
# For each 0 <= i < nums1.length, find the index j such that nums1[i] == nums2[j] 
# and determine the next greater element of nums2[j] in nums2. If there is no 
# next greater element, then the answer for this query is -1.
#
# Return an array ans of length nums1.length such that ans[i] is the next 
# greater element as described above.
#
# EXAMPLES:
# Input: nums1 = [4,1,2], nums2 = [1,3,4,2]
# Output: [-1,3,-1]
# Explanation: 4 in nums1 -> no greater in nums2. 1 in nums1 -> 3. 2 in nums1 -> none.
#
# Input: nums1 = [2,4], nums2 = [1,2,3,4]
# Output: [3,-1]
# ============================================================================

from typing import List, Tuple, Callable

# Test Cases: (nums1, nums2, expected_output)
tests: List[Tuple[List[int], List[int], List[int]]] = [
    ([4, 1, 2], [1, 3, 4, 2], [-1, 3, -1]),           # Example 1
    ([2, 4], [1, 2, 3, 4], [3, -1]),                 # Example 2
    ([1, 2, 3], [1, 2, 3, 4, 5], [2, 3, 4]),         # Strictly increasing
    ([5, 4, 3], [5, 4, 3, 2, 1], [-1, -1, -1]),      # Strictly decreasing
    ([1], [1], [-1]),                                # Single element
    ([1, 3, 5], [5, 4, 3, 2, 1], [-1, -1, -1]),      # Subset elements not in order
    ([7, 2, 4], [7, 2, 4, 6, 1, 9], [9, 4, 6]),      # Non-linear jumps
    ([1, 10], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [2, -1]), # Start and end elements
    ([10, 1], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [-1, 2]), # Reverse order subset
    ([4, 5, 2], [1, 4, 2, 5, 3], [5, -1, 5]),        # Jump over elements
]

def harness(func: Callable) -> None:
    passed = 0
    for i, (nums1, nums2, expected) in enumerate(tests):
        # Use slicing/copying to prevent mutation issues in the harness
        n1_copy = nums1[:]
        n2_copy = nums2[:]
        
        try:
            result = func(n1_copy, n2_copy)
            if result == expected:
                print(f"Test {i+1}: PASSED")
                passed += 1
            else:
                print(f"Test {i+1}: FAILED | Expected {expected}, got {result}")
        except Exception as e:
            print(f"Test {i+1}: ERROR  | {e}")
    
    print(f"\nResult: {passed}/{len(tests)} cases passed.")

# --- USER TO IMPLEMENT SOLUTION BELOW ---

def nextGreaterElement(nums1: List[int], nums2: List[int]) -> List[int]:
    """
    Finds the next greater element in nums2 for every element in nums1.
    """
    pass

harness(nextGreaterElement)