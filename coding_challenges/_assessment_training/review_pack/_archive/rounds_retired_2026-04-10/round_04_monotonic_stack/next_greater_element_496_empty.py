# LeetCode 496: Next Greater Element I (Monotonic Decreasing Stack)
#
# PROBLEM STATEMENT
# Given two arrays `nums1` and `nums2`, where all values in `nums1` exist in `nums2`,
# return an array such that for each value in `nums1`, you find the first greater
# value to its right in `nums2`; otherwise return -1.
#
# MONOTONIC PATTERN
# Use a monotonic decreasing stack of values while scanning nums2 left -> right.

from typing import Callable, List, Tuple

tests: List[Tuple[List[int], List[int], List[int]]] = [
    ([4, 1, 2], [1, 3, 4, 2], [-1, 3, -1]),
    ([2, 4], [1, 2, 3, 4], [3, -1]),
    ([1, 3, 5, 2, 4], [6, 5, 4, 3, 2, 1, 7], [7, 7, 7, 7, 7]),
    ([1], [1], [-1]),
]


def harness(func: Callable[[List[int], List[int]], List[int]]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (nums1, nums2, expected) in enumerate(tests, 1):
        try:
            got = func(nums1[:], nums2[:])
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                print(f"Test {i}: FAILED | expected={expected}, got={got}")
        except Exception as e:
            print(f"Test {i}: ERROR | {type(e).__name__}: {e}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.")


def nextGreaterElement(nums1: List[int], nums2: List[int]) -> List[int]:
    res = [-1] * len(nums1)
    hmap = {n: i for i, n in enumerate(nums1)}
    stack: List[int] = []      #monotonic decreasing stack 
    for i, num in enumerate(nums2): 
        while stack and nums2[stack[-1]] < num:
            popped_idx = stack.pop()
            if nums2[popped_idx] in hmap:
                res[hmap[nums2[popped_idx]]] = num
        stack.append(i)
    return res



harness(nextGreaterElement)
