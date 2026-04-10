# ============================================================================
# File: 028_lc_739_daily_temperatures_empty.py
#
# LeetCode 739: Daily Temperatures (Medium)
#
# PROBLEM STATEMENT:
# Given an array of integers temperatures represents the daily temperatures, 
# return an array answer such that answer[i] is the number of days you have 
# to wait after the ith day to get a warmer temperature. 
# 
# If there is no future day for which this is possible, keep answer[i] == 0 instead.
#
# EXAMPLES:
# 1) temperatures = [73,74,75,71,69,72,76,73] -> Expected: [1,1,4,2,1,1,0,0]
# 2) temperatures = [30,40,50,60] -> Expected: [1,1,1,0]
# 3) temperatures = [30,60,90] -> Expected: [1,1,0]
# ============================================================================

from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (temperatures, expected_days_to_wait)
tests: List[Tuple[List[int], List[int]]] = [
    ([73, 74, 75, 71, 69, 72, 76, 73], [1, 1, 4, 2, 1, 1, 0, 0]), # Standard Example 1
    ([30, 40, 50, 60], [1, 1, 1, 0]),                             # Standard Example 2 (Strictly increasing)
    ([30, 60, 90], [1, 1, 0]),                                    # Standard Example 3
    ([90, 80, 70, 60], [0, 0, 0, 0]),                             # Boundary: Strictly decreasing
    ([50, 50, 50, 50], [0, 0, 0, 0]),                             # Boundary: All identical temperatures
    ([30], [0]),                                                  # Edge Case: Single element
    ([30, 31, 31, 32], [1, 2, 1, 0]),                             # Plateau then a jump
    ([89, 62, 70, 58, 47, 47, 46, 76, 100, 70], [8, 1, 5, 4, 3, 2, 1, 1, 0, 0]), # Complex: Deep valleys, late spike
    ([100, 99, 98, 97, 96, 95, 94, 93, 92, 101], [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]), # Large monotonic stack buildup
    ([34, 80, 80, 34, 34, 80, 80, 34, 80, 34], [1, 0, 0, 2, 1, 0, 0, 1, 0, 0]),   # Repeating pattern
]

# --- TEST HARNESS ---
def harness(func: Callable[[List[int]], List[int]]) -> None:
    """
    Test harness for LeetCode #739: Daily Temperatures.
    """
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (temperatures, expected) in enumerate(tests, 1):
        try:
            # Pass a copy to prevent accidental mutation by the user's function
            got = func(temperatures.copy())
            
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                temps_disp = str(temperatures) if len(temperatures) <= 10 else f"[{str(temperatures[:9])[1:-1]}, ...]"
                print(f"Test {i}: FAILED | expected={expected}, got={got} | temperatures={temps_disp}")
        except Exception as e:
            temps_disp = str(temperatures) if len(temperatures) <= 10 else f"[{str(temperatures[:9])[1:-1]}, ...]"
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | temperatures={temps_disp}")
            
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def dailyTemperatures(temps: List[int]) -> List[int]:
    out = [0] * len(temps)
    stack = []      # if cur is > top .. pop and calculat.. It stores indexes
    
    for i, temp in enumerate(temps):
        while stack and temp > temps[stack[-1]]:
            idx = stack.pop()
            out[idx] = i - idx
            
        stack.append(i)
    return out
        
    


# Execute harness without __main__ block
harness(dailyTemperatures)