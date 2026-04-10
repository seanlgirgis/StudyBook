# ============================================================================
# File: 934_deque_rotate_warmup.py
#
# Warmup: Circular Scan with deque.rotate
#
# PROBLEM:
# Given list nums and integer k, return the sequence of first elements seen
# while repeatedly:
# 1) reading deque front
# 2) rotating left by 1
#
# Do this exactly k times.
#
# This is a warmup to build intuition for circular scanning with deque.
# ============================================================================

from collections import deque
from typing import Callable, List, Tuple

tests: List[Tuple[List[int], int, List[int]]] = [
    ([10, 20, 30], 5, [10, 20, 30, 10, 20]),
    ([1], 4, [1, 1, 1, 1]),
    ([4, 5], 6, [4, 5, 4, 5, 4, 5]),
    ([], 0, []),                          # Edge: empty input + zero reads
    ([], 5, []),                          # Edge: empty input + positive k
    ([9, 8, 7], 0, []),                   # Edge: k = 0
    ([-3, -2, -1], 4, [-3, -2, -1, -3]), # Edge: negative values
    ([42, 42, 42], 7, [42, 42, 42, 42, 42, 42, 42]), # All equal
    ([0, 1, 0, 1], 8, [0, 1, 0, 1, 0, 1, 0, 1]),     # Alternating pattern
    ([1, 2, 3, 4], 10, [1, 2, 3, 4, 1, 2, 3, 4, 1, 2]), # k > len(nums)
]


def harness(func: Callable[[List[int], int], List[int]]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (nums, k, expected) in enumerate(tests, 1):
        try:
            got = func(nums.copy(), k)
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                print(f"Test {i}: FAILED | expected={expected}, got={got}")
        except Exception as e:
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")

def circularRead(nums: List[int], k: int) -> List[int]:
    """
    TODO:
    Implement with deque and rotate(-1).
    
    """
    n = len(nums)
    if n == 0 or k == 0: return []
    ret = []
    for i in range(k):
        ret.append( nums[i%n])
    return ret


harness(circularRead)

def circularRead_deque(nums: List[int], k: int) -> List[int]:
    """
    TODO:
    Implement with deque and rotate(-1).
    
    """
    if not nums or k == 0:
        return []

    ret: List[int] = []
    ring = deque(nums)
    for _ in range(k):
        ret.append(ring[0])
        ring.rotate(-1)
    return ret


harness(circularRead_deque)
