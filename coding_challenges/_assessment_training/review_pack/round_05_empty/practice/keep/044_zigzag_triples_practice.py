# ============================================================================
# File: 044_zigzag_triples_practice.py
#
# Practice: Zigzag Triples
# ============================================================================
#
# PROBLEM:
# A triple (a, b, c) is zigzag if:
# - a < b > c   (peak)
# OR
# - a > b < c   (valley)
#
# Given an array numbers, return an array of length len(numbers) - 2 where:
# - result[i] = 1 if (numbers[i], numbers[i+1], numbers[i+2]) is zigzag
# - result[i] = 0 otherwise
#
# EXAMPLE:
# numbers = [1, 2, 1, 3, 4]
# triples:
# (1,2,1) -> zigzag -> 1
# (2,1,3) -> zigzag -> 1
# (1,3,4) -> not zigzag -> 0
# result = [1, 1, 0]

from typing import Callable, List, Tuple


# Format: (numbers, expected)
tests: List[Tuple[List[int], List[int]]] = [
    ([1, 2, 1, 3, 4], [1, 1, 0]),
    ([1, 2, 3, 4], [0, 0]),
    ([4, 3, 4, 3, 4], [1, 1, 1]),
    ([5, 5, 5], [0]),                 # equal values are not zigzag
    ([10, 1, 10], [1]),
    ([1, 10, 10], [0]),
    ([], []),
    ([7], []),
    ([7, 8], []),
]


def harness(func: Callable[[List[int]], List[int]]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (numbers, expected) in enumerate(tests, 1):
        try:
            got = func(numbers[:])
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                print(f"Test {i}: FAILED | expected={expected}, got={got}, numbers={numbers}")
        except Exception as e:
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


def zigzag_triples(numbers: List[int]) -> List[int]:
    result: List[int] = []
    for i in range(len(numbers) - 2):
        a, b, c = numbers[i], numbers[i + 1], numbers[i + 2]
        if (a < b > c) or (a > b < c):
            result.append(1)
        else:
            result.append(0)
    return result


harness(zigzag_triples)

