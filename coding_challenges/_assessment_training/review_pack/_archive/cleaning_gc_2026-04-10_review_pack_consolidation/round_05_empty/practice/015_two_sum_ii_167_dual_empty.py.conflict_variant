# ============================================================================
# File: two_sum_ii_167_dual_empty.py
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
# not use the same element twice.
# 
# Your solution must use only constant extra space.
# ============================================================================

from typing import List, Tuple, Callable

# --- TEST CASES ---
# Format: (numbers, target, expected_1_based_indices)
tests: List[Tuple[List[int], int, List[int]]] = [
    ([2, 7, 11, 15], 9, [1, 2]),
    ([2, 3, 4], 6, [1, 3]),
    ([-1, 0], -1, [1, 2]),
    ([1, 2, 3, 4, 4, 9], 8, [4, 5]),
    ([-5, -4, -3, -2, -1], -8, [1, 3]),
]

# --- TEST HARNESS ---
def test_harness(func: Callable, test_cases: List[Tuple[List[int], int, List[int]]]) -> None:
    """
    Test harness for LeetCode #167: Two Sum II - Input Array Is Sorted.
    Validates output list against the expected 1-based index pair using tuple unpacking.
    """
    print(f"--- Running Tests for: {func.__name__} ---")
    passed: int = 0
    
    for i, (numbers, target, expected) in enumerate(test_cases):
        try:
            # Execute the target function directly
            result = func(numbers, target)
            
            if result is None:
                print(f"Test {i+1}: FAILED | Got None, Expected {expected}")
            elif result == expected:
                # Formatting the output to stay readable if arrays are very long
                nums_display = str(numbers)
                if len(nums_display) > 30:
                    nums_display = nums_display[:27] + "..."
                print(f"Test {i+1}: PASSED (numbers={nums_display}, target={target})")
                passed += 1
            else:
                nums_display = str(numbers)
                if len(nums_display) > 20:
                    nums_display = nums_display[:17] + "..."
                print(f"Test {i+1}: FAILED | Got {result}, Expected {expected} (numbers={nums_display}, target={target})")
                        
        except Exception as e:
            print(f"Test {i+1}: ERROR  | {type(e).__name__}: {e}")
            
    print(f"\nSummary: {passed}/{len(test_cases)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def twoSum(nums: List[int], target: int) -> List[int]:
    l, r = 0, len(nums) -1
    while l < r:
        if target == nums[l] + nums[r] :
            return [l+1, r + 1]
        elif target >  nums[l] + nums[r]:
            l += 1
        else:
            r -= 1
            
        

# Execute harness without __main__ block
test_harness(twoSum, tests)
