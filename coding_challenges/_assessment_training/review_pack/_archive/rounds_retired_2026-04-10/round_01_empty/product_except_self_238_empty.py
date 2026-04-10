# LeetCode 238: Product of Array Except Self (Round 01 Empty)
from typing import Callable, List, Tuple

tests: List[Tuple[List[int], List[int]]] = [
    ([1, 2, 3, 4], [24, 12, 8, 6]),
    ([-1, 1, 0, -3, 3], [0, 0, 9, 0, 0]),
    ([0, 0], [0, 0]),
    ([5], [1]),
    ([2, 3], [3, 2]),
]

def harness(func: Callable[[List[int]], List[int]]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (nums, expected) in enumerate(tests, 1):
        try:
            result = func(nums.copy())
            if result == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                print(f"Test {i}: FAILED | expected={expected}, got={result}")
        except Exception as e:
            print(f"Test {i}: ERROR | {type(e).__name__}: {e}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.")

def productExceptSelf(nums: List[int]) -> List[int]:
    res = [1] * len(nums)
    postfix,prefix = 1,1
    for i in range(len(nums)):
        res[i] = prefix
        prefix *= nums[i]
    for i in range(len(nums)-1, -1 ,-1):
        res[i] *= postfix
        postfix *= nums[i]
    return res


harness(productExceptSelf)

