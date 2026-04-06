# LeetCode 33: Search in Rotated Sorted Array (Empty)
#
# PROBLEM STATEMENT
# Given a rotated sorted array `nums` (distinct values) and a target, return the target index
# if found, otherwise return -1. Required runtime is O(log n).
#
# EXAMPLES
# 1) nums=[4,5,6,7,0,1,2], target=0 -> 4
# 2) nums=[4,5,6,7,0,1,2], target=3 -> -1
#
# WHAT TO IMPLEMENT
# Implement `search(nums, target)` using binary search logic on sorted half.
from typing import Callable, List, Tuple

tests: List[Tuple[List[int], int, int]] = [
    ([4,5,6,7,0,1,2], 0, 4),
    ([4,5,6,7,0,1,2], 3, -1),
    ([1], 0, -1),
    ([1], 1, 0),
    ([3, 1], 1, 1),
    ([5, 1, 3], 5, 0),
    ([5, 1, 3], 3, 2),
]

def harness(func: Callable[[List[int], int], int]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (nums, target, expected) in enumerate(tests, 1):
        try:
            got = func(nums[:], target)
            if got == expected: print(f"Test {i}: PASSED"); passed += 1
            else: print(f"Test {i}: FAILED | expected={expected}, got={got}")
        except Exception as e:
            print(f"Test {i}: ERROR | {type(e).__name__}: {e}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.")

def search(nums: List[int], target: int) -> int:
    l, r = 0, len(nums)-1
    while l <= r:
        mid = l + (r-l)//2
        val = nums[mid]
        if val == target:
            return mid
        if nums[l] <= val:          #left portion is sorted    
            if target > val or target < nums[l]:
                l = mid + 1
            else:
                r = mid -1
        else:                       #right portion is sorted
            if target < val or target > nums[r]:              #target is on left-side of mid
                r = mid - 1
            else:
                l = mid + 1
    return -1

harness(search)

