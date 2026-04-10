# ============================================================================
# File: trapping_rain_water_042_empty.py
#
# LeetCode 42: Trapping Rain Water (Hard)
#
# PROBLEM STATEMENT:
# Given n non-negative integers representing an elevation map where the width 
# of each bar is 1, compute how much water it can trap after raining.
#
# EXAMPLES:
# 1) height = [0,1,0,2,1,0,1,3,2,1,2,1] -> Expected: 6
#    Explanation: The above elevation map (black section) is represented by array 
#    [0,1,0,2,1,0,1,3,2,1,2,1]. In this case, 6 units of rain water (blue section) 
#    are being trapped.
# 2) height = [4,2,0,3,2,5] -> Expected: 9
# ============================================================================

from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (height, expected_water)
tests: List[Tuple[List[int], int]] = [
    ([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6), # Standard Example 1
    ([4, 2, 0, 3, 2, 5], 9),                   # Standard Example 2
    ([], 0),                                   # Edge Case: Empty map
    ([5], 0),                                  # Edge Case: Single bar
    ([2, 2], 0),                               # Edge Case: Two bars
    ([3, 3, 3, 3], 0),                         # Boundary: Flat surface (no trapping)
    ([1, 2, 3, 4, 5], 0),                      # Boundary: Strictly increasing (no trapping)
    ([5, 4, 3, 2, 1], 0),                      # Boundary: Strictly decreasing (no trapping)
    ([1, 2, 3, 2, 1], 0),                      # Boundary: Pyramid shape (no trapping)
    ([3, 2, 1, 2, 3], 4),                      # Boundary: V-shape (traps in middle)
    ([5, 0, 5, 0, 5], 10),                     # Boundary: Alternating high/low
    ([4, 2, 3], 1),                            # Boundary: Small standard trap
]

# --- TEST HARNESS ---
def harness(func: Callable[[List[int]], int]) -> None:
    """
    Test harness for LeetCode #42: Trapping Rain Water.
    """
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    
    for i, (height, expected) in enumerate(tests, 1):
        try:
            # Pass a copy to prevent accidental mutation by the user's function
            got = func(height.copy())
            
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                height_disp = str(height) if len(height) <= 12 else f"[{str(height[:11])[1:-1]}, ...]"
                print(f"Test {i}: FAILED | expected={expected}, got={got} | height={height_disp}")
        except Exception as e:
            height_disp = str(height) if len(height) <= 12 else f"[{str(height[:11])[1:-1]}, ...]"
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | height={height_disp}")
            
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def trap(height: List[int]) -> int:
    if len(height) == 0 : return 0
    water = 0
    l, r = 0, len(height) -1
    
    bar_l, bar_r = height[l], height[r]
    
    while l < r:
        if bar_l < bar_r:
            l += 1
            if height[l] < bar_l:
                water += bar_l - height[l]
            bar_l = max(bar_l , height[l])
        else:
            r -= 1
            if height[r] < bar_r:
                water += bar_r - height[r]
            bar_r = max(bar_r , height[r])
         
    return water

# Execute harness without __main__ block
harness(trap)