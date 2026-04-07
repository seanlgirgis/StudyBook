# ============================================================================
# File: lc_033_search_rotated_sorted_array.py
#
# LeetCode 33: Search in Rotated Sorted Array (Medium)
#
# PROBLEM STATEMENT:
# There is an integer array nums sorted in ascending order (with distinct values).
#
# Prior to being passed to your function, nums is possibly rotated at an 
# unknown pivot index k (1 <= k < nums.length) such that the resulting array 
# is [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]] (0-indexed).
# For example, [0,1,2,4,5,6,7] might be rotated at pivot index 3 and 
# become [4,5,6,7,0,1,2].
#
# Given the array nums after the possible rotation and an integer target, 
# return the index of target if it is in nums, or -1 if it is not in nums.
#
# You must write an algorithm with O(log n) runtime complexity.
# ============================================================================

from typing import List, Callable

# --- TEST CASES ---
# Format: {"kwargs": {...}, "expected": ...}
search_rotated_tests: List[dict] = [
    {
        "kwargs": {"nums": [4, 5, 6, 7, 0, 1, 2], "target": 0},
        "expected": 4
    },
    {
        "kwargs": {"nums": [4, 5, 6, 7, 0, 1, 2], "target": 3},
        "expected": -1
    },
    {
        "kwargs": {"nums": [1], "target": 0},
        "expected": -1
    },
    {
        # Edge case: Array is not actually rotated
        "kwargs": {"nums": [1, 2, 3, 4, 5], "target": 4},
        "expected": 3
    },
    {
        # Edge case: Target at the boundaries
        "kwargs": {"nums": [5, 1, 3], "target": 5},
        "expected": 0
    }
]

# --- TEST HARNESS ---
def test_harness(func: Callable, test_cases: List[dict]) -> None:
    """
    Test harness for LeetCode #33: Search in Rotated Sorted Array.
    Validates integer output against expected indices.
    """
    print(f"--- Running Tests for: {func.__name__} ---")
    passed: int = 0
    
    for i, tc in enumerate(test_cases):
        kwargs = tc["kwargs"]
        expected: int = tc["expected"]
        
        try:
            # Execute the target function directly
            result = func(**kwargs)
            
            if result is None:
                print(f"Test {i+1}: FAILED | Got None, Expected {expected}")
            elif result == expected:
                # Formatting the output to stay readable if arrays are very long
                nums_display = str(kwargs['nums'])
                if len(nums_display) > 30:
                    nums_display = nums_display[:27] + "..."
                print(f"Test {i+1}: PASSED (nums={nums_display}, target={kwargs['target']})")
                passed += 1
            else:
                nums_display = str(kwargs['nums'])
                if len(nums_display) > 20:
                    nums_display = nums_display[:17] + "..."
                print(f"Test {i+1}: FAILED | Got {result}, Expected {expected} (nums={nums_display}, target={kwargs['target']})")
                        
        except Exception as e:
            print(f"Test {i+1}: ERROR  | {type(e).__name__}: {e}")
            
    print(f"\nSummary: {passed}/{len(test_cases)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def search(nums: List[int], target: int) -> int:
    # Two pointer implementation
    l, r = 0, len(nums) -1
    while l <= r:
        mid = l + (r-l)//2
        n_at_mid = nums[mid]
        if n_at_mid == target:
            return mid
        #Because it is rotated.. we need to know which side is sorted
        if nums[l] <= n_at_mid:   #left side is sorted
            if nums[l] <= target < n_at_mid:       #target is within sorted left side
                r = mid -1
            else:
                l = mid + 1
        else:                     #right side is sorted
            if n_at_mid < target <= nums[r]:      #target is with sorted right side
                l = mid + 1
            else:
                r = mid - 1
    #if not found; return -1
    return -1


# Execute harness without __main__ block
test_harness(search, search_rotated_tests)
