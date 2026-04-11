"""
id: lc_0152
title: Maximum Product Subarray
source: leetcode
difficulty: medium
primary: arrays
tags: [arrays, dynamic-programming]
leetcode_url: https://leetcode.com/problems/maximum-product-subarray/
status: draft
last_updated: 2026-04-10
notes: 
- key idea: 
- time: 
- space: 
"""

# ============================================================================
# File: 152_lc_152_maximum_product_subarray.py
# Problem 152: Maximum Product Subarray (Medium)
# 
# Problem Statement:
# Given an integer array nums, find a subarray that has the largest product, 
# and return the product.
#
# Constraints:
# - The test cases are generated so that the answer will fit in a 32-bit integer.
# - 1 <= nums.length <= 2 * 10^4
# - -10 <= nums[i] <= 10
#
# Examples:
# Example 1:
# Input: nums = [2,3,-2,4]
# Output: 6
# Explanation: [2,3] has the largest product 6.
#
# Example 2:
# Input: nums = [-2,0,-1]
# Output: 0
# Explanation: The result cannot be 2, because [-2,-1] is not a subarray.
# ============================================================================

from typing import List, Tuple, Callable

# Test Suite: (Input, Expected Output)
tests: List[Tuple[List[int], int]] = [
    ([2, 3, -2, 4], 6),                # Example 1: Basic positive path
    ([-2, 0, -1], 0),                  # Example 2: Zero interruption
    ([0], 0),                          # Edge Case: Single zero
    ([-2], -2),                        # Edge Case: Single negative
    ([5], 5),                          # Edge Case: Single positive
    ([-2, 3, -4], 24),                 # Negative: Two negatives cancel out
    ([-2, -3, -4], 12),                # Negative: Odd number of negatives
    ([2, -5, 3, 1, -4, 0, -2], 120),   # Complex: Multiple sign flips and a zero
    ([0, 0, 0], 0),                    # Boundary: All zeros
    ([-1, -1, -1, -1], 1),             # Boundary: Alternating products
    ([1, 2, 3, 4], 24),                # Strictly Increasing
    ([-1, 0, -2, 0], 0),               # Disjoint zeros
    ([10, -1, 10], 10),                # Small negative bridge
]

def harness(func: Callable) -> None:
    passed = 0
    failed = 0
    
    print(f"--- Running Tests for: {func.__name__} ---")
    
    for i, (nums_in, expected) in enumerate(tests):
        # Create a deep copy to prevent mutation issues
        nums_copy = list(nums_in)
        
        try:
            actual = func(nums_copy)
            if actual == expected:
                status = "PASSED"
                passed += 1
            else:
                status = f"FAILED (Expected {expected}, got {actual})"
                failed += 1
        except Exception as e:
            status = f"ERROR ({type(e).__name__}: {e})"
            failed += 1
        
        # Truncate long inputs for cleaner output
        display_input = str(nums_in) if len(str(nums_in)) < 50 else f"{str(nums_in)[:47]}..."
        print(f"Test {i+1:02d}: {status} | Input: {display_input}")
        
    print(f"\n--- Result: {passed} Passed, {failed} Failed ---")

# --- USER TO IMPLEMENT SOLUTION BELOW ---

def maxProduct(nums: List[int]) -> int:
    """
    Finds the subarray with the largest product.
    """
    # Base case:
    # The problem guarantees len(nums) >= 1, so we can safely initialize from nums[0].
    #
    # We track three things while scanning left -> right:
    # 1) cur_max: maximum product of a subarray that MUST end at current index.
    # 2) cur_min: minimum product of a subarray that MUST end at current index.
    # 3) best: global maximum product seen anywhere so far.
    #
    # Why both cur_max and cur_min?
    # Because multiplying by a negative number flips signs:
    # - a large negative (cur_min) * negative can become the new large positive.
    cur_max = nums[0]
    cur_min = nums[0]
    best = nums[0]

    # Start from index 1 because index 0 already seeded the running values.
    for x in nums[1:]:
        # Candidates for "subarray ending at current index":
        # A) start fresh at current element alone: x
        # B) extend previous max product subarray: cur_max * x
        # C) extend previous min product subarray: cur_min * x
        #
        # We need previous cur_max and cur_min together, so compute candidates first.
        cand1 = x
        cand2 = cur_max * x
        cand3 = cur_min * x

        # New max/min ending at this index.
        cur_max = max(cand1, cand2, cand3)
        cur_min = min(cand1, cand2, cand3)

        # Update global best if this index gives a better product.
        best = max(best, cur_max, cur_min)

    return best

harness(maxProduct)
