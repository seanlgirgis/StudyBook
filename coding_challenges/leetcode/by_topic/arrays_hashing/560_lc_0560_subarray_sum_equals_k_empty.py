"""
id: lc_0560
title: Subarray Sum Equals K
source: leetcode
difficulty: medium
primary: hash-table
tags: [hash-table, prefix-sum, arrays]
leetcode_url: https://leetcode.com/problems/subarray-sum-equals-k/
status: draft
last_updated: 2026-04-12
notes: 
- key idea: Use a hash map to store the frequency of prefix sums encountered so far.
- time: O(n)
- space: O(n)
"""

# ============================================================================
# File: 560_lc_0560_subarray_sum_equals_k_empty.py
# Problem 560: Subarray Sum Equals K (Medium)
# 
# PROBLEM STATEMENT:
# Given an array of integers nums and an integer k, return the total number 
# of subarrays whose sum equals to k.
#
# A subarray is a contiguous non-empty sequence of elements within an array.
#
# EXAMPLES:
# Input: nums = [1,1,1], k = 2
# Output: 2
#
# Input: nums = [1,2,3], k = 3
# Output: 2
# ============================================================================

from typing import List, Tuple, Callable

# Test Cases: List[Tuple[nums, k, expected]]
tests: List[Tuple[List[int], int, int]] = [
    ([1, 1, 1], 2, 2),                   # Standard Example 1
    ([1, 2, 3], 3, 2),                   # Standard Example 2 ([1,2] and [3])
    ([1], 0, 0),                         # Edge Case: Single element, no match
    ([1], 1, 1),                         # Edge Case: Single element, match
    ([0, 0, 0, 0, 0], 0, 15),            # Edge Case: All zeros (many subarrays)
    ([-1, -1, 1], 0, 1),                 # Boundary: Negative numbers canceling out
    ([1, -1, 1, -1, 1], 0, 6),           # Boundary: Alternating negatives
    ([1, 2, 1, 2, 1], 3, 4),             # Overlapping subarrays
    ([10, 2, -2, -20, 10], -10, 3),      # Large values and negative target
    ([1, 1, 1], 3, 1),                   # Total sum equals k
    ([3, 4, 7, 2, -3, 1, 4, 2], 7, 4),   # Complex sequence
    ([0, 5, -5, 0], 0, 6),               # Multiple zero-sum subarrays
]

def harness(func: Callable) -> None:
    passed = 0
    failed = 0
    
    print(f"\n--- Testing: {func.__name__} ---")
    
    for i, (nums, k, expected) in enumerate(tests):
        # Deep copy to prevent user mutation
        nums_copy = list(nums)
        
        try:
            result = func(nums_copy, k)
            
            display_input = f"nums={nums}, k={k}"
            if len(display_input) > 60:
                display_input = display_input[:57] + "..."
            
            if result == expected:
                print(f"Test {i+1}: PASSED | {display_input}")
                passed += 1
            else:
                print(f"Test {i+1}: FAILED | {display_input}")
                print(f"   Expected: {expected}, Got: {result}")
                failed += 1
        except Exception as e:
            print(f"Test {i+1}: ERROR  | {display_input}")
            print(f"   Exception: {e}")
            failed += 1
            
    print(f"\nResults: {passed} Passed, {failed} Failed\n")

# --- USER TO IMPLEMENT SOLUTION BELOW ---

def subarraySum(nums: List[int], k: int) -> int:
    # KEY INSIGHT:
    # sum(i..j) = prefix[j] - prefix[i-1]
    # We want that to equal k, so: prefix[i-1] = prefix[j] - k
    # As we build the running sum (prefix[j]), we ask:
    #   "how many times have we seen (running - k) before?"
    # Each occurrence = one subarray ending HERE that sums to k.

    # Seed with {0:1} — means "a prefix sum of 0 was seen once before we start"
    # This handles subarrays that start at index 0.
    seen = {0: 1}

    running = 0   # current prefix sum
    count = 0     # total subarrays found

    for num in nums:
        running += num                          # extend prefix sum to current index

        count += seen.get(running - k, 0)      # how many earlier prefixes make this subarray sum = k

        seen[running] = seen.get(running, 0) + 1   # record this prefix sum for future lookups

    return count

harness(subarraySum)