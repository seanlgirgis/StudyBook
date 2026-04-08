# ============================================================================
# File: 028_lc_739_daily_temperatures.py
#
# LeetCode 739: Daily Temperatures (Medium)
#
# PROBLEM STATEMENT:
# Given an array of integers temperatures represents the daily temperatures,
# return an array answer such that answer[i] is the number of days you have to
# wait after the i-th day to get a warmer temperature.
# If there is no future day for which this is possible, keep answer[i] == 0.
#
# EXAMPLES:
# 1) temperatures = [73,74,75,71,69,72,76,73] -> [1,1,4,2,1,1,0,0]
# 2) temperatures = [30,40,50,60]             -> [1,1,1,0]
# ============================================================================

from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (temperatures, expected_wait_days)
tests: List[Tuple[List[int], List[int]]] = [
    ([73, 74, 75, 71, 69, 72, 76, 73], [1, 1, 4, 2, 1, 1, 0, 0]),  # Standard
    ([30, 40, 50, 60], [1, 1, 1, 0]),                              # Strictly increasing
    ([30, 60, 90], [1, 1, 0]),                                     # Increasing short
    ([90, 80, 70, 60], [0, 0, 0, 0]),                              # Strictly decreasing
    ([70], [0]),                                                    # Single day
    ([], []),                                                       # Empty list
    ([70, 70, 70], [0, 0, 0]),                                     # All equal
    ([70, 71, 70, 71, 70], [1, 0, 1, 0, 0]),                       # Zig-zag
    ([65, 66, 65, 64, 68], [1, 3, 2, 1, 0]),                       # Dip then peak
    ([100, 99, 100], [0, 1, 0]),                                   # Same max returns 0 for first
]


# --- TEST HARNESS ---
def harness(func: Callable[[List[int]], List[int]]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (temperatures, expected) in enumerate(tests, 1):
        try:
            result = func(temperatures.copy())
            if result == expected:
                temps_display = (
                    str(temperatures)
                    if len(temperatures) <= 10
                    else f"[{str(temperatures[:9])[1:-1]}, ...]"
                )
                print(f"Test {i}: PASSED (temperatures={temps_display})")
                passed += 1
            else:
                temps_display = (
                    str(temperatures)
                    if len(temperatures) <= 10
                    else f"[{str(temperatures[:9])[1:-1]}, ...]"
                )
                print(
                    f"Test {i}: FAILED | expected={expected}, got={result} "
                    f"| temperatures={temps_display}"
                )
        except Exception as e:
            temps_display = (
                str(temperatures)
                if len(temperatures) <= 10
                else f"[{str(temperatures[:9])[1:-1]}, ...]"
            )
            print(
                f"Test {i}: ERROR  | {type(e).__name__}: {e} "
                f"| temperatures={temps_display}"
            )

    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def dailyTemperatures(temperatures: List[int]) -> List[int]:
    pass



# Execute harness without __main__ block
harness(dailyTemperatures)
