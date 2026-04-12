"""
id: lc_0347
title: Top K Frequent Elements
source: leetcode
difficulty: medium
primary: hash-table
tags: [hash-table, heap, bucket-sort, counting]
leetcode_url: https://leetcode.com/problems/top-k-frequent-elements/
status: draft
last_updated: 2026-04-11
notes: 
- key idea: Use a hash map for frequencies, then either a Min-Heap of size k or Bucket Sort (array of lists) for O(n).
- time: O(n) with bucket sort or O(n log k) with heap.
- space: O(n) to store frequencies and buckets.
"""

# ============================================================================
# File: 347_lc_0347_top_k_frequent_elements_empty.py
# Problem 347: Top K Frequent Elements (Medium)
# 
# PROBLEM STATEMENT:
# Given an integer array nums and an integer k, return the k most frequent 
# elements. You may return the answer in any order.
#
# EXAMPLES:
# Input: nums = [1,1,1,2,2,3], k = 2
# Output: [1,2]
#
# Input: nums = [1], k = 1
# Output: [1]
#
# Constraints:
# - k is in the range [1, the number of unique elements in the array].
# - It is guaranteed that the answer is unique.
# ============================================================================

from typing import List, Tuple, Callable

# Test Cases: List[Tuple[nums, k, expected]]
tests: List[Tuple[List[int], int, List[int]]] = [
    ([1, 1, 1, 2, 2, 3], 2, [1, 2]),       # Standard Example 1
    ([1], 1, [1]),                        # Standard Example 2
    ([1, 2], 2, [1, 2]),                  # Boundary: k equals number of unique elements
    ([4, 1, -1, 2, -1, 2, 3], 2, [-1, 2]), # Negative numbers and scattered frequencies
    ([1, 1, 2, 2, 3, 3, 4, 4, 4, 4], 1, [4]), # Clear winner
    ([1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 5, 6], 3, [3, 2, 1]), # Clear top-3: freq 4,3,2
    ([1, 1, 1, 1, 1], 1, [1]),            # All identical
    ([10, 20, 20, 30, 30, 30], 2, [30, 20]),     # Clear top-2: freq 3,2,1
    ([5, 5, 5, 2, 2, 1], 3, [5, 2, 1]),   # k is total unique
    ([1, 2, 1, 2, 3, 1], 2, [1, 2]),      # Out of order frequencies
    ([0, 0, 0, 1, 1, 2], 2, [0, 1]),      # Including zero
    ([100, 200, 100, 200, 300, 100], 1, [100]), # Sparse large values
]

def harness(func: Callable) -> None:
    passed = 0
    failed = 0
    
    print(f"\n--- Testing: {func.__name__} ---")
    
    for i, (nums, k, expected) in enumerate(tests):
        # Deep copy the list to prevent mutation
        nums_copy = list(nums)
        
        try:
            result = func(nums_copy, k)
            
            # Since order doesn't matter, sort both for comparison
            sorted_result = sorted(result) if result is not None else None
            sorted_expected = sorted(expected)
            
            display_input = f"nums={nums}, k={k}"
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
            print(f"Test {i+1}: ERROR  | nums={nums}, k={k}")
            print(f"   Exception: {e}")
            failed += 1
            
    print(f"\nResults: {passed} Passed, {failed} Failed\n")

# --- USER TO IMPLEMENT SOLUTION BELOW ---
from collections import Counter
import heapq

# Approach 1: Min-Heap of size k — O(n log k)
# Keep a heap of the k most frequent seen so far.
# pushpop evicts the smallest freq when heap is full,
# so only the top-k freqs survive.
def topKFrequent(nums: List[int], k: int) -> List[int]:
    heap = []
    counts = Counter(nums)
    for n, freq in counts.items():
        if len(heap) < k:
            heapq.heappush(heap, (freq, n))
        else:
            heapq.heappushpop(heap, (freq, n))
    return [val for _, val in heap]


# Approach 2: Bucket Sort — O(n)
# Frequency can never exceed len(nums), so use freq as the index.
# buckets[f] holds all numbers that appear exactly f times.
# Walk from high freq down, collect until we have k elements.
def topKFrequentBucket(nums: List[int], k: int) -> List[int]:
    counts = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, freq in counts.items():
        buckets[freq].append(num)
    out = []
    for freq in range(len(buckets) - 1, 0, -1):
        for num in buckets[freq]:
            out.append(num)
            if len(out) == k:
                return out


harness(topKFrequent)
harness(topKFrequentBucket)