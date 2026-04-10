# ============================================================================
# File: lc_042_trapping_rain_water.py
#
# LeetCode 42: Trapping Rain Water (Hard)
#
# PROBLEM STATEMENT:
# Given n non-negative integers representing an elevation map where the width 
# of each bar is 1, compute how much water it can trap after raining.
#
# EXAMPLES:
# - height = [0,1,0,2,1,0,1,3,2,1,2,1] -> Expected: 6
# - height = [4,2,0,3,2,5]             -> Expected: 9
# ============================================================================

from typing import List, Callable

# --- TEST CASES ---
# Format: {"kwargs": {...}, "expected": ...}
trapping_rain_water_tests: List[dict] = [
    {
        "kwargs": {"height": [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]},
        "expected": 6
    },
    {
        "kwargs": {"height": [4, 2, 0, 3, 2, 5]},
        "expected": 9
    },
    {
        # Edge case: Empty array
        "kwargs": {"height": []},
        "expected": 0
    },
    {
        # Edge case: Single element
        "kwargs": {"height": [1]},
        "expected": 0
    },
    {
        # Edge case: No pits to trap water
        "kwargs": {"height": [1, 2, 3, 4, 5]},
        "expected": 0
    }
]

# --- TEST HARNESS ---
def test_harness(func: Callable, test_cases: List[dict]) -> None:
    """
    Test harness for LeetCode #42: Trapping Rain Water.
    Validates integer output against expected water trapped.
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
                height_display = str(kwargs['height'])
                if len(height_display) > 40:
                    height_display = height_display[:37] + "..."
                print(f"Test {i+1}: PASSED (height={height_display})")
                passed += 1
            else:
                height_display = str(kwargs['height'])
                if len(height_display) > 20:
                    height_display = height_display[:17] + "..."
                print(f"Test {i+1}: FAILED | Got {result}, Expected {expected} (height={height_display})")
                        
        except Exception as e:
            print(f"Test {i+1}: ERROR  | {type(e).__name__}: {e}")
            
    print(f"\nSummary: {passed}/{len(test_cases)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def trap(height: List[int]) -> int:
    # best to solve this issue using two pointer and max_barrier left and right
    if len(height) == 0 : return 0
    l, r = 0, len(height) - 1
    b_l = height[l]
    b_r = height[r]
    
    water = 0
    
    while l < r :
        if b_l <= b_r:
            l += 1
            b_l = max(b_l , height[l])
            if height[l] < b_l:
                water += b_l - height[l]
        else:
            r -= 1
            b_r = max(b_r , height[r])
            if height[r] < b_r:
                water += b_r - height[r]            

    return water


# Execute harness without __main__ block
test_harness(trap, trapping_rain_water_tests)
