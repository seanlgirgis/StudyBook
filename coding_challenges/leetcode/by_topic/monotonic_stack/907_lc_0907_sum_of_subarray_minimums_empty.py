"""
id: lc_0907
title: Sum of Subarray Minimums
source: leetcode
difficulty: medium
primary: stack
tags: [stack, monotonic-stack, arrays, dynamic-programming]
leetcode_url: https://leetcode.com/problems/sum-of-subarray-minimums/
status: draft
last_updated: 2026-04-12
notes:
- key idea: For each element arr[i], find the distance to the Previous Less Element (PLE)
            and Next Less Element (NLE). The number of subarrays where arr[i] is the
            minimum is left * right where left = i - PLE and right = NLE - i.
- time: O(n)
- space: O(n)
- duplicate handling: use strict < for PLE and <= for NLE (or vice versa) to avoid
  double-counting subarrays when equal elements exist.
"""

# ============================================================================
# File: 907_lc_0907_sum_of_subarray_minimums_empty.py
# Problem 907: Sum of Subarray Minimums (Medium)
#
# PROBLEM STATEMENT:
# Given an array of integers arr, find the sum of min(b), where b ranges over
# every (contiguous) subarray of arr. Since the answer may be large, return
# the answer modulo 10^9 + 7.
#
# EXAMPLES:
# Input: arr = [3,1,2,4]
# Output: 17
# Explanation:
# Subarrays are [3],[1],[2],[4],[3,1],[1,2],[2,4],[3,1,2],[1,2,4],[3,1,2,4].
# Minimums are  3,  1,  2,  4,  1,   1,   2,   1,   1,    1.
# Sum is 17.
#
# Input: arr = [11,81,94,43]
# Output: 444
# ============================================================================

from typing import List, Tuple, Callable

MOD = 10**9 + 7

# Test Cases: List[Tuple[arr, expected]]
tests: List[Tuple[List[int], int]] = [
    ([3, 1, 2, 4], 17),                   # Standard Example 1
    ([11, 81, 94, 43], 429),              # Standard Example 2
    ([1], 1),                             # Edge Case: Single element
    ([1, 1], 3),                          # Edge Case: Identical elements
    ([71, 55, 82, 55], 593),              # Complex: Repeating minimums
    ([1, 2, 3], 10),                      # Boundary: Strictly increasing
    ([3, 2, 1], 10),                      # Boundary: Strictly decreasing
    ([1, 2, 1], 7),                       # V-shape
    ([2, 1, 2], 8),                       # Peak-shape
    ([10, 10, 10], 60),                   # Multiple identical elements
    ([100, 200, 300, 400], 2000),         # Increasing large numbers
    ([10, 1, 10, 1], 28),                 # Alternating values
]

def harness(func: Callable) -> None:
    passed = 0
    failed = 0

    print(f"\n--- Testing: {func.__name__} ---")

    for i, (arr, expected) in enumerate(tests):
        arr_copy = list(arr)
        try:
            result = func(arr_copy)
            display = str(arr) if len(str(arr)) < 55 else str(arr)[:52] + "..."
            if result == expected:
                print(f"Test {i+1:02d}: PASSED | {display}")
                passed += 1
            else:
                print(f"Test {i+1:02d}: FAILED | {display}")
                print(f"   Expected: {expected}, Got: {result}")
                failed += 1
        except Exception as e:
            print(f"Test {i+1:02d}: ERROR  | {arr}")
            print(f"   Exception: {e}")
            failed += 1

    print(f"\n--- Result: {passed} Passed, {failed} Failed ---\n")

# --- USER TO IMPLEMENT SOLUTION BELOW ---

def sumSubarrayMins(arr: List[int]) -> int:
    n = len(arr)

    # PLE[i] = nearest index to the LEFT with value strictly less than arr[i]
    # sentinel: -1 (nothing smaller, subarray can start all the way to index 0)
    ple = [-1] * n
    stack = []
    for i in range(n):
        while stack and arr[stack[-1]] >= arr[i]:
            stack.pop()
        ple[i] = stack[-1] if stack else -1
        stack.append(i)

    # NLE[i] = nearest index to the RIGHT with value less than OR EQUAL to arr[i]
    # sentinel: n (nothing smaller, subarray can end all the way to index n-1)
    # NOTE: using <= here (not <) to avoid double-counting duplicate minimums
    nle = [n] * n
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and arr[stack[-1]] > arr[i]:
            stack.pop()
        nle[i] = stack[-1] if stack else n
        stack.append(i)

    # For each element: count subarrays where it is the minimum
    # left  = i - ple[i]  → how many start positions
    # right = nle[i] - i  → how many end positions
    total = 0
    for i in range(n):
        left  = i - ple[i]
        right = nle[i] - i
        total += arr[i] * left * right

    return total % MOD

harness(sumSubarrayMins)
