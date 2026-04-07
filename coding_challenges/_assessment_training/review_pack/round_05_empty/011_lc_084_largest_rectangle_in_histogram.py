# ============================================================================
# File: lc_084_largest_rectangle_in_histogram.py
#
# LeetCode 84: Largest Rectangle in Histogram (Hard)
#
# PROBLEM STATEMENT:
# Given an array of integers heights representing the histogram's bar height 
# where the width of each bar is 1, return the area of the largest rectangle 
# in the histogram.
#
# EXAMPLES:
# - heights = [2,1,5,6,2,3] -> Expected: 10
#   Explanation: The largest rectangle is shown in the vertical bars 5 and 6, 
#   which has an area = 2 * 5 = 10.
#
# - heights = [2,4] -> Expected: 4
# ============================================================================

from typing import List, Callable

# --- TEST CASES ---
# Format: {"kwargs": {...}, "expected": ...}
largest_rectangle_tests: List[dict] = [
    {
        # Standard Example 1
        "kwargs": {"heights": [2, 1, 5, 6, 2, 3]},
        "expected": 10
    },
    {
        # Standard Example 2
        "kwargs": {"heights": [2, 4]},
        "expected": 4
    },
    {
        # Edge case: Single bar
        "kwargs": {"heights": [5]},
        "expected": 5
    },
    {
        # Boundary: Flat histogram (all same heights)
        "kwargs": {"heights": [2, 2, 2, 2, 2]},
        "expected": 10
    },
    {
        # Boundary: Strictly increasing
        "kwargs": {"heights": [1, 2, 3, 4, 5]},
        "expected": 9
    },
    {
        # Boundary: Strictly decreasing
        "kwargs": {"heights": [5, 4, 3, 2, 1]},
        "expected": 9
    },
    {
        # Edge case: Histogram split by a zero
        "kwargs": {"heights": [2, 1, 2, 0, 3, 2, 2, 3]},
        "expected": 6
    }
]

# --- TEST HARNESS ---
def test_harness(func: Callable, test_cases: List[dict]) -> None:
    """
    Test harness for LeetCode #84: Largest Rectangle in Histogram.
    Validates integer output against expected maximum area.
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
                heights_display = str(kwargs['heights'])
                if len(heights_display) > 40:
                    heights_display = heights_display[:37] + "..."
                print(f"Test {i+1}: PASSED (heights={heights_display})")
                passed += 1
            else:
                heights_display = str(kwargs['heights'])
                if len(heights_display) > 20:
                    heights_display = heights_display[:17] + "..."
                print(f"Test {i+1}: FAILED | Got {result}, Expected {expected} (heights={heights_display})")
                        
        except Exception as e:
            print(f"Test {i+1}: ERROR  | {type(e).__name__}: {e}")
            
    print(f"\nSummary: {passed}/{len(test_cases)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def largestRectangleArea(heights: List[int]) -> int:
    pass


# Execute harness without __main__ block
test_harness(largestRectangleArea, largest_rectangle_tests)