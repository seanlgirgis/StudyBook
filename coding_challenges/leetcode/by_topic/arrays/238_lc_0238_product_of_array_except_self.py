"""
id: lc_0238
title: Product of Array Except Self
source: leetcode
difficulty: medium
primary: arrays
tags: [arrays, prefix-sum, suffix-sum]
leetcode_url: https://leetcode.com/problems/product-of-array-except-self/
status: draft
last_updated: 2026-04-10
notes: 
- key idea: 
- time: 
- space: 
"""

# ============================================================================
# File: 238_lc_0238_product_of_array_except_self.py
# LC238: Product of Array Except Self (Medium)
#
# PROBLEM STATEMENT:
# Given an integer array nums, return an array answer such that answer[i] is 
# equal to the product of all the elements of nums except nums[i].
# 
# The product of any prefix or suffix of nums is guaranteed to fit in a 
# 32-bit integer.
# 
# You must write an algorithm that runs in O(n) time and without using the 
# division operation.
#
# EXAMPLES:
# Example 1:
# Input: nums = [1,2,3,4]
# Output: [24,12,8,6]
#
# Example 2:
# Input: nums = [-1,1,0,-3,3]
# Output: [0,0,9,0,0]
# ============================================================================

from typing import List, Callable, Tuple

# Test cases: (input_list, expected_output)
tests: List[Tuple[List[int], List[int]]] = [
    ([1, 2, 3, 4], [24, 12, 8, 6]),                # Example 1
    ([-1, 1, 0, -3, 3], [0, 0, 9, 0, 0]),          # Example 2 (Single zero)
    ([0, 0], [0, 0]),                              # Edge Case: Multiple zeros
    ([1, 5], [5, 1]),                              # Edge Case: Length 2
    ([1, 1, 1], [1, 1, 1]),                        # Boundary: All ones
    ([4, 3, 2, 1, 2], [12, 16, 24, 48, 24]),       # Complex pattern
    ([10, 20], [20, 10]),                          # Simple swap
    ([0, 4, 0], [0, 0, 0]),                        # Boundary: Two zeros interspersed
    ([-2, -1, -3, -4], [-12, -24, -8, -6]),       # Negative values
    ([1, -1], [-1, 1]),                            # Negative and positive
    ([2, 3, 5, 0], [0, 0, 0, 30]),                 # Zero at the end
    ([0, 2, 3, 5], [30, 0, 0, 0]),                 # Zero at the start
]

def harness(func: Callable) -> None:
    passed = 0
    for i, (nums, expected) in enumerate(tests):
        # Deep copy input to prevent mutation issues during test run
        nums_input = nums[:]
        try:
            result = func(nums_input)
            if result == expected:
                print(f"Test {i+1}: PASSED")
                passed += 1
            else:
                print(f"Test {i+1}: FAILED")
                print(f"   Input:    {nums}")
                print(f"   Expected: {expected}")
                print(f"   Actual:   {result}")
        except Exception as e:
            print(f"Test {i+1}: ERROR")
            print(f"   Input: {nums}")
            print(f"   {type(e).__name__}: {e}")
    
    print(f"\nSummary: {passed}/{len(tests)} tests passed.")

# --- USER TO IMPLEMENT SOLUTION BELOW ---

def productExceptSelf(nums: List[int]) -> List[int]:
    """
    O(n) time and O(1) extra space (excluding output array).
    Do not use the division operator.
    """
    # prefix  = running product of elements to the LEFT of current index
    # postfix = running product of elements to the RIGHT of current index
    # n       = length shortcut for readability
    prefix, postfix, n = 1, 1, len(nums)

    # out[i] will eventually hold:
    # (product of all values left of i) * (product of all values right of i)
    out = [1] * n

    # PASS 1 (left -> right):
    # Store left-side product at each index.
    #
    # Example nums = [1,2,3,4]
    # i=0 -> out[0] = 1              (nothing on left)
    # i=1 -> out[1] = 1              (left product = 1)
    # i=2 -> out[2] = 1*2 = 2
    # i=3 -> out[3] = 1*2*3 = 6
    for i in range(n):
        out[i] = prefix
        prefix *= nums[i]

    # PASS 2 (right -> left):
    # Multiply each out[j] by right-side product.
    #
    # Continuing example:
    # j=3 -> out[3] *= 1      => 6
    # j=2 -> out[2] *= 4      => 8
    # j=1 -> out[1] *= 12     => 12
    # j=0 -> out[0] *= 24     => 24
    #
    # Final out = [24,12,8,6]
    for j in range(n - 1, -1, -1):
        out[j] *= postfix
        postfix *= nums[j]

    # We never used division, and we used only constant extra variables
    # (prefix, postfix, n), besides the required output array.
    return out
        
harness(productExceptSelf)
