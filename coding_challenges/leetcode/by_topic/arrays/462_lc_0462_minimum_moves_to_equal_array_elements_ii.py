"""
id: lc_0462
title: Minimum Moves to Equal Array Elements II
source: leetcode
difficulty: medium
primary: arrays
tags: [arrays, math, sorting, median]
leetcode_url: https://leetcode.com/problems/minimum-moves-to-equal-array-elements-ii/
status: draft
last_updated: 2026-04-11
notes:
- key idea: 
- time: 
- space: 
"""

# ============================================================================
# File: 462_lc_0462_minimum_moves_to_equal_array_elements_ii.py
# LeetCode 462: Minimum Moves to Equal Array Elements II (Medium)
# 
# PROBLEM STATEMENT:
# Given an integer array nums of size n, return the minimum number of moves 
# required to make all array elements equal.
# In one move, you can increment or decrement an element of the array by 1.
# Test cases are designed so that the answer will fit in a 32-bit integer.
#
# EXAMPLES:
# Input: nums = [1,2,3]
# Output: 2
# Explanation: Only two moves are needed (remember each move increments or 
# decrements one element): [1,2,3]  =>  [2,2,3]  =>  [2,2,2]
#
# Input: nums = [1,10,2,9]
# Output: 16
# ============================================================================

from typing import List, Callable, Tuple
import copy

# Test cases: (nums, expected_output)
tests: List[Tuple[List[int], int]] = [
    ([1, 2, 3], 2),                     # Example 1: Standard small odd array
    ([1, 10, 2, 9], 16),                # Example 2: Standard small even array
    ([1], 0),                           # Edge Case: Single element
    ([1, 1], 0),                        # Edge Case: Already equal
    ([1, 1, 1, 1], 0),                  # Edge Case: All identical
    ([0, 0, 100], 100),                 # Boundary: Large difference with zeroes
    ([-10, -5, 0, 5, 10], 30),          # Symmetric around 0: |-10|+|-5|+|0|+|5|+|10| = 30
    ([1, 5, 10, 15, 20], 29),           # Median 10: 9+5+0+5+10 = 29
    ([20, 15, 10, 5, 1], 29),           # Same multiset as above (order doesn't matter)
    ([1, 2, 10, 11], 18),               # Pattern: Bimodal distribution
    ([1, 1, 1, 1000], 999),             # Stress: Single outlier
    ([7, 4, 3, 9, 1, 8, 5, 2, 6], 20),  # Random: Unsorted sequence
]

def harness(func: Callable) -> None:
    print(f"Testing function: {func.__name__}")
    passed = 0
    for i, (nums_in, expected) in enumerate(tests):
        # Deep copy to prevent mutation issues
        nums_copy = list(nums_in)
        try:
            result = func(nums_copy)
            if result == expected:
                print(f"Test {i+1}: PASSED")
                passed += 1
            else:
                input_str = str(nums_in) if len(nums_in) < 15 else f"{nums_in[:5]}...{nums_in[-5:]}"
                print(f"Test {i+1}: FAILED | Input: {input_str} | Expected: {expected} | Got: {result}")
        except Exception as e:
            print(f"Test {i+1}: ERROR | {type(e).__name__}: {e}")
    
    print(f"\nSummary: {passed}/{len(tests)} tests passed.")

# --- USER TO IMPLEMENT SOLUTION BELOW ---

def minMoves2(heights: List[int]) -> int:
    """
    Calculates the minimum moves to make all elements in nums equal.
    Target value is the median of the array.
    """
    heights.sort()
    median = heights[len(heights) //2 ]
    return sum(abs(x - median) for x in heights)
    

harness(minMoves2)
