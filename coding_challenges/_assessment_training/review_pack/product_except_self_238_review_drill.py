# LeetCode 238: Product of Array Except Self (Review Drill)

from typing import Callable, List, Tuple


# --- TEST CASES ---
# Format: (nums_array, expected_output_array)
product_except_self_tests: List[Tuple[List[int], List[int]]] = [
    ([1, 2, 3, 4], [24, 12, 8, 6]),
    ([-1, 1, 0, -3, 3], [0, 0, 9, 0, 0]),
    ([0, 0], [0, 0]),
    ([5], [1]),
    ([2, 3], [3, 2]),
    ([10, 3, 5, 6, 2], [180, 600, 360, 300, 900]),
    ([-1, -2, -3, -4], [-24, -12, -8, -6]),
    ([0, 4, 5], [20, 0, 0]),
]


# --- TEST HARNESS ---
def test_harness(
    func: Callable[[List[int]], List[int]],
    test_cases: List[Tuple[List[int], List[int]]],
) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed: int = 0

    for i, (nums, expected) in enumerate(test_cases):
        try:
            result: List[int] = func(nums.copy())
            if result == expected:
                print(f"Test {i + 1}: PASSED")
                passed += 1
            else:
                print(f"Test {i + 1}: FAILED")
                print(f"    Input:    {nums}")
                print(f"    Expected: {expected}")
                print(f"    Got:      {result}")
        except Exception as e:
            print(f"Test {i + 1}: ERROR | {type(e).__name__}: {e}")

    print(f"\nSummary: {passed}/{len(test_cases)} tests passed.")


# --- YOUR IMPLEMENTATION ---
def productExceptSelf(nums: List[int]) -> List[int]:
    """
    Given an integer array nums, return an array answer such that answer[i]
    is equal to the product of all the elements of nums except nums[i].

    Constraints (LeetCode style):
    - Solve without using division
    - Aim for O(n) time
    """
    ret = [1] * len(nums)
    prefix , postfix = 1,1
    for i in range(1, len(nums)):
        prefix *= nums[i-1]
        ret[i] = prefix 
    for i in range(len(nums) -1 , -1, -1):
        ret[i] *= postfix
        postfix *= nums[i]
    return ret


test_harness(productExceptSelf, product_except_self_tests)
