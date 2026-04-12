"""
id: lc_0217
title: Contains Duplicate
source: leetcode
difficulty: easy
primary: hash-table
tags: [hash-table, arrays, sorting]
leetcode_url: https://leetcode.com/problems/contains-duplicate/
status: draft
last_updated: 2026-04-11
notes: 
- key idea: Use a hash set for O(1) average-time lookups to detect if an element has been seen before.
- time: O(n)
- space: O(n)
"""

# ============================================================================
# File: 217_lc_0217_contains_duplicate_empty.py
# Problem 217: Contains Duplicate (Easy)
# 
# PROBLEM STATEMENT:
# Given an integer array nums, return true if any value appears at least twice 
# in the array, and return false if every element is distinct.
#
# EXAMPLES:
# Input: nums = [1,2,3,1]
# Output: true
#
# Input: nums = [1,2,3,4]
# Output: false
#
# Input: nums = [1,1,1,3,3,4,3,2,4,2]
# Output: true
# ============================================================================

from typing import List, Tuple, Callable

# Test Cases: List[Tuple[nums, expected]]
tests: List[Tuple[List[int], bool]] = [
    ([1, 2, 3, 1], True),                # Standard Example 1: Duplicate at ends
    ([1, 2, 3, 4], False),               # Standard Example 2: All unique
    ([1, 1, 1, 3, 3, 4, 3, 2, 4, 2], True), # Standard Example 3: Multiple duplicates
    ([], False),                         # Edge Case: Empty array
    ([1], False),                        # Edge Case: Single element
    ([1, 1], True),                       # Edge Case: Two identical elements
    ([1, 2, 1], True),                   # Smallest case with non-adjacent duplicate
    ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], False), # Boundary: Long unique list
    ([-1, -2, -3, -1], True),            # Boundary: Negative numbers duplicate
    ([0, 0], True),                      # Boundary: Zeroes
    ([10**9, 10**9 - 1, 10**9], True),   # Large integers
    (list(range(1000)) + [999], True),   # Stress: Large array with one duplicate at end
]

def harness(func: Callable) -> None:
    passed = 0
    failed = 0
    
    print(f"\n--- Testing: {func.__name__} ---")
    
    for i, (nums, expected) in enumerate(tests):
        # Deep copy to prevent mutation
        nums_input = list(nums)
        
        try:
            result = func(nums_input)
            
            # Truncate visual display for long lists
            display_input = str(nums) if len(str(nums)) < 50 else f"{str(nums)[:47]}..."
            
            if result == expected:
                print(f"Test {i+1}: PASSED | Input: {display_input}")
                passed += 1
            else:
                print(f"Test {i+1}: FAILED | Input: {display_input}")
                print(f"   Expected: {expected}, Got: {result}")
                failed += 1
        except Exception as e:
            print(f"Test {i+1}: ERROR  | Input: {display_input}")
            print(f"   Exception: {e}")
            failed += 1
            
    print(f"\nResults: {passed} Passed, {failed} Failed\n")

# --- USER TO IMPLEMENT SOLUTION BELOW ---

def containsDuplicate(nums: List[int]) -> bool:
    """
    Checks if the array contains any duplicate values.
    """
    seen = set()
    for n in nums:
        if n in seen:
            return True
        seen.add(n)
    return False

harness(containsDuplicate)