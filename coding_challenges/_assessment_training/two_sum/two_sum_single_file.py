# LeetCode 1: Two Sum

from typing import Callable, List, Tuple

# --- PROBLEM STATEMENT ---
# Given an array of integers nums and an integer target, return indices of the
# two numbers such that they add up to target.
#
# You may assume that each input has exactly one solution, and you may not use
# the same element twice.
#
# You can return the answer in any order.
#
# Constraints:
# - 2 <= nums.length <= 10^4
# - -10^9 <= nums[i] <= 10^9
# - -10^9 <= target <= 10^9
# - Exactly one valid answer exists.

# --- TEST CASES ---
# Format: (nums_array, target, expected_indices)
two_sum_tests: List[Tuple[List[int], int, List[int]]] = [
    ([2, 7, 11, 15], 9, [0, 1]),               # 1. Standard LC Example 1
    ([3, 2, 4], 6, [1, 2]),                    # 2. Standard LC Example 2 (Unordered)
    ([3, 3], 6, [0, 1]),                       # 3. Standard LC Example 3 (Duplicate values)
    ([0, 4, 3, 0], 0, [0, 3]),                 # 4. Multiple zeros
    ([-1, -2, -3, -4, -5], -8, [2, 4]),        # 5. Negative numbers
    ([10, 20, 30, 40, 50], 90, [3, 4]),        # 6. Larger sequential numbers
    ([5, 75, 25], 100, [1, 2]),                # 7. Match at the end of the array
    ([-10, 7, 19, 15], 9, [0, 2]),             # 8. Negatives and positives crossing zero
    ([1, 5, 1, 5], 10, [1, 3]),                # 9. Multiple identical pairs (returns first valid)
    ([2, 1, 9, 4, 4, 56, 90, 3], 8, [3, 4])    # 10. Mid-array pair in larger set
]

# --- TEST HARNESS ---
def test_harness(func: Callable[[List[int], int], List[int]], test_cases: List[Tuple[List[int], int, List[int]]]) -> None:
    """
    Test harness for LeetCode #1: Two Sum.
    Validates O(n) Hash Map complement tracking.
    """
    print(f"--- Running Tests for: {func.__name__} ---")
    passed: int = 0

    for i, (nums, target, expected) in enumerate(test_cases):
        try:
            # Copy input to prevent accidental mutation during tests
            input_nums = nums.copy()

            # Strict typed execution
            result: List[int] = func(input_nums, target)

            # Since order doesn't technically matter for the answer, we sort for comparison
            if sorted(result) == sorted(expected):
                display_nums = f"{nums[:6]}..." if len(nums) > 6 else f"{nums}"
                print(f"Test {i+1}: PASSED (target={target}, nums={display_nums})")
                passed += 1
            else:
                display_nums = f"{nums[:6]}..." if len(nums) > 6 else f"{nums}"
                print(f"Test {i+1}: FAILED | target={target}, nums={display_nums}")
                print(f"    Expected: {expected}")
                print(f"    Got:      {result}")
        except Exception as e:
            display_nums = f"{nums[:6]}..." if len(nums) > 6 else f"{nums}"
            print(f"Test {i+1}: ERROR  | target={target}, nums={display_nums} | {type(e).__name__}: {e}")

    print(f"\nSummary: {passed}/{len(test_cases)} tests passed.")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def twoSum(nums: List[int], target: int) -> List[int]:
    """
    LC 1 — Two Sum

    PROBLEM:
    Given an array of integers `nums` and an integer `target`, return indices of the
    two numbers such that they add up to `target`. You may assume that each input would
    have exactly one solution, and you may not use the same element twice.

    HINT / APPROACH:
    1. Pattern: Hash Map (Complement Tracking).
    2. While the naive approach is nested loops O(n^2), we can do this in O(n) with a dictionary.
    3. Initialize an empty dictionary called `seen` to store `{value: index}`.
    4. Iterate through the array using `for i, n in enumerate(nums):`.
    5. The trick: Calculate the `complement = target - n`. (This is the number you need
       to find to reach the target).
    6. Check if the `complement` is already in your `seen` dictionary.
       - If it IS: You found your pair! Return `[seen[complement], i]`.
       - If it IS NOT: Add the current number and its index to the dictionary: `seen[n] = i`.

    Time:  O(n) — Single pass through the array. Dictionary lookups are O(1).
    Space: O(n) — The Hash Map could store up to n elements in the worst case.
    """
    seen = {}       #store seen and its id
    for i, n in enumerate(nums):
        if (target - n) in seen:
            return [seen[target - n] , i]
        seen[n] = i
    return []
            
# Execute harness without __main__ block
test_harness(twoSum, two_sum_tests)

