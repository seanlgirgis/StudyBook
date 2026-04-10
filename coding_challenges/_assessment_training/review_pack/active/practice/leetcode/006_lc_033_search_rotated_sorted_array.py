# ============================================================================
# File: search_in_rotated_sorted_array_033_empty.py
#
# LeetCode 33: Search in Rotated Sorted Array (Medium)
#
# PROBLEM STATEMENT:
# There is an integer array nums sorted in ascending order (with distinct values).
# Prior to being passed to your function, nums is possibly rotated at an unknown 
# pivot index k (1 <= k < nums.length) such that the resulting array is 
# [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]] (0-indexed).
#
# For example, [0,1,2,4,5,6,7] might be rotated at pivot index 3 and become [4,5,6,7,0,1,2].
#
# Given the array nums after the possible rotation and an integer target, return 
# the index of target if it is in nums, or -1 if it is not in nums.
#
# You must write an algorithm with O(log n) runtime complexity.
#
# EXAMPLES:
# 1) nums = [4,5,6,7,0,1,2], target = 0 -> Expected: 4
# 2) nums = [4,5,6,7,0,1,2], target = 3 -> Expected: -1
# 3) nums = [1], target = 0 -> Expected: -1
# ============================================================================

from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (nums, target, expected_index)
tests: List[Tuple[List[int], int, int]] = [
    ([4, 5, 6, 7, 0, 1, 2], 0, 4),             # Standard Example 1
    ([4, 5, 6, 7, 0, 1, 2], 3, -1),            # Standard Example 2
    ([1], 0, -1),                              # Standard Example 3
    ([1], 1, 0),                               # Edge Case: Single element (Found)
    ([3, 1], 1, 1),                            # Boundary: Two elements, rotated, target right
    ([3, 1], 3, 0),                            # Boundary: Two elements, rotated, target left
    ([5, 1, 3], 5, 0),                         # Boundary: Three elements, target at start
    ([5, 1, 3], 1, 1),                         # Boundary: Three elements, target at pivot
    ([1, 2, 3, 4, 5, 6], 4, 3),                # Boundary: Not rotated at all
    ([6, 7, 8, 1, 2, 3, 4, 5], 7, 1),          # Boundary: Target is on the left sorted portion
    ([4, 5, 6, 7, 8, 1, 2, 3], 2, 6),          # Boundary: Target is on the right sorted portion
    ([5, 6, 7, 8, 9, 10, 1, 2, 3], 10, 5),     # Boundary: Target is the maximum element
    ([5, 6, 7, 8, 9, 10, 1, 2, 3], 1, 6),      # Boundary: Target is the minimum element
    ([7, 8, 9, 1, 2, 3, 4, 5, 6], 6, 8),       # Tricky: Target at far right after rotation
    ([7, 8, 9, 1, 2, 3, 4, 5, 6], 7, 0),       # Tricky: Target at far left after rotation
    ([30, 40, 50, 5, 10, 20], 25, -1),         # Tricky: Missing target between partitions
]

# --- TEST HARNESS ---
def harness(func: Callable[[List[int], int], int]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (nums, target, expected) in enumerate(tests, 1):
        try:
            # Pass a copy to prevent accidental mutation by the user's function
            got = func(nums.copy(), target)

            if not isinstance(got, int):
                raise AssertionError(f"Output must be int. got={type(got).__name__}")
            if got < -1 or got >= len(nums):
                raise AssertionError(f"Output index out of valid range [-1, {len(nums) - 1}]. got={got}")
            if got != -1 and nums[got] != target:
                raise AssertionError(f"Returned index does not point to target. nums[{got}]={nums[got]}, target={target}")
            
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                nums_disp = str(nums) if len(nums) <= 10 else f"[{str(nums[:9])[1:-1]}, ...]"
                print(f"Test {i}: FAILED | expected={expected}, got={got} | target={target}, nums={nums_disp}")
        except Exception as e:
            nums_disp = str(nums) if len(nums) <= 10 else f"[{str(nums[:9])[1:-1]}, ...]"
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | target={target}, nums={nums_disp}")
            
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def search(nums: List[int], target: int) -> int:
    if len(nums) == 0:
        return -1

    l, r = 0, len(nums) - 1
    while l <= r:
        mid = l + (r - l) // 2
        n_at_mid = nums[mid]    

        if target == n_at_mid:
            return mid

        # Which side is sorted 
        if nums[l] <= n_at_mid:        # left side is sorted
            if nums[l] <= target < n_at_mid:
                r = mid - 1
            else:
                l = mid + 1
        else:                          #right side is sorted
            if nums[r] >= target > n_at_mid:
                l = mid + 1
            else:
                r = mid - 1
    return -1


# Execute harness without __main__ block
harness(search)
