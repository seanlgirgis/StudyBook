"""
id: lc_0128
title: Longest Consecutive Sequence
source: leetcode
difficulty: medium
primary: hash-table
tags: [hash-table, arrays, union-find]
leetcode_url: https://leetcode.com/problems/longest-consecutive-sequence/
status: draft
last_updated: 2026-04-11
notes: 
- key idea: Use a HashSet for O(1) lookups. Only start counting a sequence if (num - 1) is not in the set.
- time: O(n)
- space: O(n)
"""

# ============================================================================
# File: 128_lc_128_longest_consecutive_sequence_empty.py
# Problem 128: Longest Consecutive Sequence (Medium)
# 
# PROBLEM STATEMENT:
# Given an unsorted array of integers nums, return the length of the longest 
# consecutive elements sequence.
#
# You must write an algorithm that runs in O(n) time.
#
# EXAMPLES:
# Input: nums = [100,4,200,1,3,2]
# Output: 4
# Explanation: The longest consecutive elements sequence is [1, 2, 3, 4]. 
# Therefore its length is 4.
#
# Input: nums = [0,3,7,2,5,8,4,6,0,1]
# Output: 9
# ============================================================================

from typing import List, Tuple, Callable

# Test Cases: List[Tuple[nums, expected]]
tests: List[Tuple[List[int], int]] = [
    ([100, 4, 200, 1, 3, 2], 4),        # Standard Example 1
    ([0, 3, 7, 2, 5, 8, 4, 6, 0, 1], 9), # Standard Example 2 (with duplicates)
    ([], 0),                             # Edge Case: Empty input
    ([1], 1),                            # Edge Case: Single element
    ([5, 5, 5, 5], 1),                   # Edge Case: All identical
    ([10, 9, 8, 7, 6, 5], 6),            # Boundary: Strictly decreasing
    ([1, 2, 3, 4, 5, 6], 6),             # Boundary: Strictly increasing
    ([-1, -2, -3, 0, 1], 5),             # Boundary: Negatives across zero
    ([1, 10, 2, 20, 3, 30], 3),          # Scattered: Multiple sequences
    ([1, 2, 0, 1], 3),                   # Duplicate values within sequence
    ([100, 101, 102, 5, 4, 3, 2, 1], 5), # Two sequences, return longest
    ([2147483647, -2147483648], 1),      # Large gap (integer limits)
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

def longestConsecutive(nums: List[int]) -> int:
    """
    Finds the length of the longest consecutive sequence in O(n) time.
    """
    nums = set(nums)
    longest = 0
    def seq_len(num):
        ret = 0
        while num in nums:
            ret +=1
            num += 1
        return ret
        
    for num in nums:
        if num - 1 not in nums:
            longest = max(longest, seq_len(num))
    return longest

harness(longestConsecutive)