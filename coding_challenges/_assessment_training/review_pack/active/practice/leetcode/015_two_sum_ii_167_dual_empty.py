# ============================================================================
# File: 015_two_sum_ii_167_dual_empty.py
#
# LeetCode 167: Two Sum II - Input Array Is Sorted (Medium)
#
# PROBLEM STATEMENT:
# Given a 1-indexed array of integers numbers that is already sorted in 
# non-decreasing order, find two numbers such that they add up to a specific 
# target number. Let these two numbers be numbers[index1] and numbers[index2] 
# where 1 <= index1 < index2 <= numbers.length.
#
# Return the indices of the two numbers, index1 and index2, added by one as 
# an integer array [index1, index2] of length 2.
#
# The tests are generated such that there is exactly one solution. You may 
# not use the same element twice. Your solution must use only constant extra space.
#
# EXAMPLES:
# 1) numbers = [2,7,11,15], target = 9 -> Expected: [1,2]
#    Explanation: The sum of 2 and 7 is 9. Therefore, index1 = 1, index2 = 2.
# 2) numbers = [2,3,4], target = 6 -> Expected: [1,3]
# 3) numbers = [-1,0], target = -1 -> Expected: [1,2]
# ============================================================================

from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (numbers, target, expected_1_indexed_indices)
tests: List[Tuple[List[int], int, List[int]]] = [
    ([2, 7, 11, 15], 9, [1, 2]),                   # Standard Example 1
    ([2, 3, 4], 6, [1, 3]),                        # Standard Example 2
    ([-1, 0], -1, [1, 2]),                         # Standard Example 3 (Negative numbers)
    ([0, 0], 0, [1, 2]),                           # Edge Case: Zeros
    ([1, 2, 3, 4, 4, 9, 56, 90], 8, [4, 5]),       # Duplicate numbers as the answer
    ([-10, -8, -2, 1, 5], -9, [1, 4]),             # Mixed negatives and positives
    ([5, 10], 15, [1, 2]),                         # Boundary: Minimum length of 2
    ([-5, -4, -3, -2, -1], -8, [1, 3]),            # Boundary: All negative numbers
    (list(range(1, 10001)), 19999, [9999, 10000]), # Boundary: Very large array, answer at the very end
    ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 11, [1, 10]) # Boundary: Answer at the exact extremes (two pointers optimal)
]

# --- TEST HARNESS ---
def harness(func: Callable[[List[int], int], List[int]]) -> None:
    """
    Test harness for LeetCode #167: Two Sum II - Input Array Is Sorted.
    """
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (numbers, target, expected) in enumerate(tests, 1):
        try:
            # Pass a copy to prevent accidental mutation by the user's function
            got = func(numbers.copy(), target)
            
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                nums_disp = str(numbers) if len(numbers) <= 10 else f"[{str(numbers[:9])[1:-1]}, ...]"
                print(f"Test {i}: FAILED | expected={expected}, got={got} | target={target}, numbers={nums_disp}")
        except Exception as e:
            nums_disp = str(numbers) if len(numbers) <= 10 else f"[{str(numbers[:9])[1:-1]}, ...]"
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | target={target}, numbers={nums_disp}")
            
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def twoSum(nums: List[int], target: int) -> List[int]:
    l , r = 0, len(nums) -1
    
    while l < r:
        if target == nums[l] + nums[r]:
            return [l+1, r+1]
        elif target > nums[l] + nums[r]:
            l += 1
        else:
            r -= 1
    return []   #according to specs impossible to happen


# Execute harness without __main__ block
harness(twoSum)