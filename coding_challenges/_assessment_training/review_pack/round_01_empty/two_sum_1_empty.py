# LeetCode 1: Two Sum (Round 01 Empty)
from typing import Callable, List, Tuple

tests: List[Tuple[List[int], int, List[int]]] = [
    ([2, 7, 11, 15], 9, [0, 1]),
    ([3, 2, 4], 6, [1, 2]),
    ([3, 3], 6, [0, 1]),
    ([0, 4, 3, 0], 0, [0, 3]),
    ([-1, -2, -3, -4, -5], -8, [2, 4]),
]

def harness(func: Callable[[List[int], int], List[int]]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (nums, target, expected) in enumerate(tests, 1):
        try:
            result = func(nums.copy(), target)
            if sorted(result) == sorted(expected):
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                print(f"Test {i}: FAILED | expected={expected}, got={result}")
        except Exception as e:
            print(f"Test {i}: ERROR | {type(e).__name__}: {e}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.")

def twoSum(nums: List[int], target: int) -> List[int]:
    seen: dict[int, int] = {}
    for i, num in enumerate(nums):
        if (target - num) in seen:
            return [seen[target-num], i]
        seen[num] = i
    return []

harness(twoSum)

