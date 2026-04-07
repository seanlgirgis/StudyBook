# ============================================================================
# File: lc_198_house_robber.py
#
# LeetCode 198: House Robber (Medium)
#
# PROBLEM STATEMENT:
# You are given an integer array `nums` where each element represents the amount of
# money in a house along a street. Adjacent houses have connected alarms, so you
# cannot rob two adjacent houses on the same night.
#
# Return the maximum amount of money you can rob without alerting the police.
#
# EXAMPLES:
# 1) nums = [1, 2, 3, 1] -> Expected: 4
#    Explanation: Rob house 1 (money = 1) and then rob house 3 (money = 3).
#
# 2) nums = [2, 7, 9, 3, 1] -> Expected: 12
#    Explanation: Rob house 1 (money = 2), rob house 3 (money = 9) and rob house 5 (money = 1).
# ============================================================================

from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (nums, expected_max_money)
tests: List[Tuple[List[int], int]] = [
    ([1, 2, 3, 1], 4),
    ([2, 7, 9, 3, 1], 12),
    ([2, 1, 1, 2], 4),
    ([], 0),                  # Edge case: No houses
    ([5], 5),                 # Edge case: Single house
    ([2, 3], 3),              # Edge case: Two houses
    ([2, 1, 1, 2, 10], 13),   # Boundary: Optimal to jump over two adjacent '1's
    ([100, 1, 1, 100], 200),  # Boundary: High value edges
    ([0, 0, 0, 0], 0),        # Boundary: All zeros
]

# --- TEST HARNESS ---
def test_harness(func: Callable[[List[int]], int]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (nums, expected) in enumerate(tests, 1):
        try:
            # Pass a copy of nums to prevent accidental mutation by the function
            got = func(nums[:])
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                nums_display = str(nums) if len(nums) <= 10 else f"[{str(nums[:9])[1:-1]}, ...]"
                print(f"Test {i}: FAILED | expected={expected}, got={got} | nums={nums_display}")
        except Exception as e:
            nums_display = str(nums) if len(nums) <= 10 else f"[{str(nums[:9])[1:-1]}, ...]"
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | nums={nums_display}")
            
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def rob(nums: List[int]) -> int:
    if len(nums) <= 2:
        return max(nums) if nums else 0

    # we have more than two houses
    prev_theft = nums[0]
    max_theft = max(nums[1], prev_theft)
    
    for i in range(2, len(nums)):
        prev_theft, max_theft = max_theft, max(prev_theft + nums[i], max_theft)
    
    return max_theft
    


# Execute harness without __main__ block
test_harness(rob)
