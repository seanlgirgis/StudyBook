# ============================================================================
# File: lc_001_two_sum.py
#
# LeetCode 1: Two Sum (Easy)
#
# PROBLEM STATEMENT:
# Given an array of integers nums and an integer target, return indices of the 
# two numbers such that they add up to target.
# 
# You may assume that each input would have exactly one solution, and you may 
# not use the same element twice.
# 
# You can return the answer in any order.
# ============================================================================

from typing import List

# --- TEST CASES ---
# Format: {"kwargs": {...}, "expected": [...]}
two_sum_tests: List[dict] = [
    {
        "kwargs": {"nums": [2, 7, 11, 15], "target": 9},
        "expected": [0, 1]
    },
    {
        "kwargs": {"nums": [3, 2, 4], "target": 6},
        "expected": [1, 2]
    },
    {
        "kwargs": {"nums": [3, 3], "target": 6},
        "expected": [0, 1]
    }
]

# --- TEST HARNESS ---
def test_harness(target_class: type, test_cases: List[dict]) -> None:
    """
    Test harness for LeetCode #1: Two Sum.
    Validates output indices, allowing for any return order.
    """
    print(f"--- Running Tests for: {target_class.__name__} ---")
    passed: int = 0
    obj = target_class()
    
    for i, tc in enumerate(test_cases):
        kwargs = tc["kwargs"]
        expected: List[int] = tc["expected"]
        
        try:
            # Execute the twoSum method
            result = obj.twoSum(**kwargs)
            
            # Validate results (sorting handles the "in any order" requirement safely)
            if result is None:
                print(f"Test {i+1}: FAILED | Got None, Expected {expected}")
            elif sorted(result) == sorted(expected):
                # Formatting the output to stay readable if arrays are very large
                nums_display = str(kwargs['nums'])
                if len(nums_display) > 30:
                    nums_display = nums_display[:27] + "..."
                print(f"Test {i+1}: PASSED (nums={nums_display}, target={kwargs['target']})")
                passed += 1
            else:
                print(f"Test {i+1}: FAILED | Got {result}, Expected {expected}")
                        
        except Exception as e:
            print(f"Test {i+1}: ERROR  | {type(e).__name__}: {e}")
            
    print(f"\nSummary: {passed}/{len(test_cases)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}
        for i, num in enumerate(nums):
            other = target - num
            if other in seen:
                return [seen[other], i]
            seen[num] = i
        return []
            

# Execute harness without __main__ block
test_harness(Solution, two_sum_tests)
