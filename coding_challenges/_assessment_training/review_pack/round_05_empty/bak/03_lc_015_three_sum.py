# ============================================================================
# File: lc_015_three_sum.py
#
# LeetCode 15: 3Sum (Medium)
#
# PROBLEM STATEMENT:
# Given an integer array nums, return all the triplets 
# [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, 
# and nums[i] + nums[j] + nums[k] == 0.
#
# Notice that the solution set must not contain duplicate triplets.
# ============================================================================

from typing import List, Callable

# --- TEST CASES ---
# Format: {"kwargs": {...}, "expected": [...]}
three_sum_tests: List[dict] = [
    {
        "kwargs": {"nums": [-1, 0, 1, 2, -1, -4]},
        "expected": [[-1, -1, 2], [-1, 0, 1]]
    },
    {
        "kwargs": {"nums": [0, 1, 1]},
        "expected": []
    },
    {
        "kwargs": {"nums": [0, 0, 0]},
        "expected": [[0, 0, 0]]
    },
    {
        # Edge case: Multiple duplicates
        "kwargs": {"nums": [-2, 0, 0, 2, 2]},
        "expected": [[-2, 0, 2]]
    }
]

# --- TEST HARNESS ---
def test_harness(func: Callable, test_cases: List[dict]) -> None:
    """
    Test harness for LeetCode #15: 3Sum.
    Validates output arrays, accounting for any internal/external ordering.
    """
    print(f"--- Running Tests for: {func.__name__} ---")
    passed: int = 0
    
    def normalize_triplets(arr: List[List[int]]) -> List[List[int]]:
        """Sorts internal triplets and the outer list for safe comparison."""
        if arr is None:
            return None
        return sorted([sorted(triplet) for triplet in arr])
    
    for i, tc in enumerate(test_cases):
        kwargs = tc["kwargs"]
        expected: List[List[int]] = tc["expected"]
        
        try:
            # Execute the target function directly
            result = func(**kwargs)
            
            # Normalize both expected and actual results for comparison
            norm_result = normalize_triplets(result)
            norm_expected = normalize_triplets(expected)
            
            if result is None:
                print(f"Test {i+1}: FAILED | Got None, Expected {expected}")
            elif norm_result == norm_expected:
                # Formatting the output to stay readable if arrays are very large
                nums_display = str(kwargs['nums'])
                if len(nums_display) > 40:
                    nums_display = nums_display[:37] + "..."
                print(f"Test {i+1}: PASSED (nums={nums_display})")
                passed += 1
            else:
                print(f"Test {i+1}: FAILED | Got {result}, Expected {expected}")
                        
        except Exception as e:
            print(f"Test {i+1}: ERROR  | {type(e).__name__}: {e}")
            
    print(f"\nSummary: {passed}/{len(test_cases)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def threeSum(nums: List[int]) -> List[List[int]]:
    #sort the list
    nums.sort()
    out: List[List[int]] = []

    
    for i, num in enumerate(nums):
        if i > 0 and num == nums[i - 1]:
            continue

        l, r, target = i + 1, len(nums) - 1, -num
        
        while l < r:
            the_sum = nums[l] + nums[r]
            if the_sum > target:
                r -= 1
            elif the_sum < target:
                l += 1
            else:
                out.append([num, nums[l], nums[r]])
                l += 1
                r -= 1
                while l < r and nums[l] == nums[l-1]:
                    l += 1
                while l < r and nums[r] == nums[r+1]:
                    r -= 1
    return out
                
            
        
        


# Execute harness without __main__ block
test_harness(threeSum, three_sum_tests)
