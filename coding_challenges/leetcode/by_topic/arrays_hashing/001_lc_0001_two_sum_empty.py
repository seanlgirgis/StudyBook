"""
id: lc_0001
title: Two Sum
source: leetcode
difficulty: easy
primary: arrays
tags: [arrays, hash-table]
leetcode_url: https://leetcode.com/problems/two-sum/
status: draft
last_updated: 2026-04-11
notes: 
- key idea: 
- time: 
- space: 
"""

# ============================================================================
# File: 001_lc_0001_two_sum_empty.py
# Problem 1: Two Sum (Easy)
# 
# PROBLEM STATEMENT:
# Given an array of integers nums and an integer target, return indices of the 
# two numbers such that they add up to target.
#
# You may assume that each input would have exactly one solution, and you 
# may not use the same element twice.
#
# You can return the answer in any order.
#
# EXAMPLES:
# Input: nums = [2,7,11,15], target = 9
# Output: [0,1]
# Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
#
# Input: nums = [3,2,4], target = 6
# Output: [1,2]
# ============================================================================

from typing import List, Tuple, Callable

# Test Cases: List[Tuple[nums, target, expected]]
# Note: Expected results are sorted to ensure comparison consistency
tests: List[Tuple[List[int], int, List[int]]] = [
    ([2, 7, 11, 15], 9, [0, 1]),           # Standard Example 1
    ([3, 2, 4], 6, [1, 2]),                # Standard Example 2
    ([3, 3], 6, [0, 1]),                   # Standard Example 3 (Duplicate values)
    ([1, 5, 5, 11], 10, [1, 2]),           # Mid-array duplicates
    ([-1, -2, -3, -4, -5], -8, [2, 4]),    # Negative numbers
    ([0, 4, 3, 0], 0, [0, 3]),             # Target zero with zeros
    ([-10, 7, 19, 15], 9, [0, 2]),         # Negative and positive mix
    ([1, 2, 3, 4, 5, 6], 11, [4, 5]),      # End of long array
    ([11, 15, 2, 7], 9, [2, 3]),           # Target at the end
    ([2, 5, 5, 11], 10, [1, 2]),           # Duplicate elements as the answer
    ([2, 4, 11, 3], 7, [1, 3]),            # Scattered indices
    ([1000000, 500, 1000000], 2000000, [0, 2]) # Large values
]

def harness(func: Callable) -> None:
    passed = 0
    failed = 0
    
    print(f"\n--- Testing: {func.__name__} ---")
    
    for i, (nums, target, expected) in enumerate(tests):
        # Deep copy the input to prevent user mutation
        nums_copy = list(nums)
        
        try:
            result = func(nums_copy, target)
            
            # Sort both to allow [0,1] vs [1,0] comparisons
            sorted_result = sorted(result) if result else None
            sorted_expected = sorted(expected)
            
            display_input = f"nums={nums}, target={target}"
            if len(display_input) > 60:
                display_input = display_input[:57] + "..."
            
            if sorted_result == sorted_expected:
                print(f"Test {i+1}: PASSED | {display_input}")
                passed += 1
            else:
                print(f"Test {i+1}: FAILED | {display_input}")
                print(f"   Expected: {expected}, Got: {result}")
                failed += 1
        except Exception as e:
            print(f"Test {i+1}: ERROR  | nums={nums}")
            print(f"   Exception: {e}")
            failed += 1
            
    print(f"\nResults: {passed} Passed, {failed} Failed\n")

# --- USER TO IMPLEMENT SOLUTION BELOW ---

def twoSum(nums: List[int], target: int) -> List[int]:
    """
    Finds two indices such that nums[i] + nums[j] == target.
    """
    seen = {}
    
    for i, num in enumerate(nums):
        if target - num in seen:
            return [seen[target - num], i]
        seen[num] = i
    return []


harness(twoSum)