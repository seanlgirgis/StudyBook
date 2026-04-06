# LeetCode 167: Two Sum II - Input Array Is Sorted (Dual Empty)
from typing import Callable, List, Tuple

# Format: (numbers, target, expected_1_based_indices)
tests: List[Tuple[List[int], int, List[int]]] = [
    ([2, 7, 11, 15], 9, [1, 2]),
    ([2, 3, 4], 6, [1, 3]),
    ([-1, 0], -1, [1, 2]),
    ([1, 2, 3, 4, 4, 9], 8, [4, 5]),
    ([-5, -4, -3, -2, -1], -8, [1, 3]),
]


def harness(
    func: Callable[[List[int], int], List[int]],
    name: str,
) -> None:
    print(f"--- Running Tests for: {name} ---")
    passed = 0
    for i, (numbers, target, expected) in enumerate(tests, 1):
        try:
            result = func(numbers.copy(), target)
            if result == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                print(f"Test {i}: FAILED | expected={expected}, got={result}")
        except Exception as e:
            print(f"Test {i}: ERROR | {type(e).__name__}: {e}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.")


def twoSumII_hash(nums: List[int], target: int) -> List[int]:
    """
    Return 1-based indices.
    Hash-map variant (empty for practice).
    """
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target - n] + 1, i + 1]
        seen[n] = i
    return []



def twoSumII_two_pointers(nums: List[int], target: int) -> List[int]:
    """
    Return 1-based indices.
    Two-pointer variant on sorted input (empty for practice).
    """
    l, r = 0, len(nums) - 1
    while l < r:
        if target == nums[l] + nums[r] :
            return [l+1 , r+1]
        elif target > (nums[l] + nums[r]):
            l += 1
        else:
            r -= 1
    return []


print("\n=== Two Sum II (Hash) ===")
harness(twoSumII_hash, "twoSumII_hash")

print("\n=== Two Sum II (Two Pointers) ===")
harness(twoSumII_two_pointers, "twoSumII_two_pointers")
