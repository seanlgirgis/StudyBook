# ============================================================================
# File: 016_lc_198_house_robber_empty.py
#
# LeetCode 198: House Robber (Medium)
#
# PROBLEM STATEMENT:
# You are a professional robber planning to rob houses along a street. Each 
# house has a certain amount of money stashed, the only constraint stopping you 
# from robbing each of them is that adjacent houses have security systems 
# connected and it will automatically contact the police if two adjacent houses 
# were broken into on the same night.
#
# Given an integer array nums representing the amount of money of each house, 
# return the maximum amount of money you can rob tonight without alerting the police.
#
# EXAMPLES:
# 1) nums = [1,2,3,1] -> Expected: 4
#    Explanation: Rob house 1 (money = 1) and then rob house 3 (money = 3).
#    Total amount you can rob = 1 + 3 = 4.
# 2) nums = [2,7,9,3,1] -> Expected: 12
#    Explanation: Rob house 1 (money = 2), rob house 3 (money = 9) and rob house 5 (money = 1).
#    Total amount you can rob = 2 + 9 + 1 = 12.
# ============================================================================

from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (nums, expected_max_money)
tests: List[Tuple[List[int], int]] = [
    ([1, 2, 3, 1], 4),                                # Standard Example 1
    ([2, 7, 9, 3, 1], 12),                            # Standard Example 2
    ([], 0),                                          # Edge Case: No houses
    ([5], 5),                                         # Edge Case: Single house
    ([2, 3], 3),                                      # Edge Case: Two houses (max of the two)
    ([2, 1, 1, 2], 4),                                # Boundary: Robbing the first and last (gap of 2)
    ([10, 0, 0, 10], 20),                             # Boundary: Zeros in between forcing a jump
    ([5, 5, 5, 5, 5], 15),                            # Boundary: Identical amounts, odd length (rob 1st, 3rd, 5th)
    ([5, 5, 5, 5], 10),                               # Boundary: Identical amounts, even length
    ([100, 1, 1, 100], 200),                          # Boundary: Huge values separated by tiny values
    ([0, 0, 0, 0], 0),                                # Boundary: All zeros
    ([1, 3, 1, 3, 100], 103),                         # Boundary: Complex pattern, optimal path shifts
]

# --- TEST HARNESS ---
def harness(func: Callable[[List[int]], int]) -> None:
    """
    Test harness for LeetCode #198: House Robber.
    """
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (nums, expected) in enumerate(tests, 1):
        try:
            # Pass a copy to prevent accidental mutation by the user's function
            got = func(nums.copy())
            
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                nums_disp = str(nums) if len(nums) <= 10 else f"[{str(nums[:9])[1:-1]}, ...]"
                print(f"Test {i}: FAILED | expected={expected}, got={got} | nums={nums_disp}")
        except Exception as e:
            nums_disp = str(nums) if len(nums) <= 10 else f"[{str(nums[:9])[1:-1]}, ...]"
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | nums={nums_disp}")
            
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def rob(nums: List[int]) -> int:
    if len(nums) == 0 : return 0
    if len(nums) <= 2 : return max(nums)
    prev = max(nums[1], nums[0])
    prevprev = nums[0]
    
    for i in range(2, len(nums)):
        prev, prevprev = max(prev , prevprev+ nums[i]), prev
    return prev


# Execute harness without __main__ block
harness(rob)