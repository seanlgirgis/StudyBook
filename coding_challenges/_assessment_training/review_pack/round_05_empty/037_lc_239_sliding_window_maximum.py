# ============================================================================
# File: 037_lc_239_sliding_window_maximum.py
#
# LeetCode 239: Sliding Window Maximum
# ============================================================================

from collections import deque
from typing import Callable, List, Tuple


tests: List[Tuple[List[int], int, List[int]]] = [
    ([1, 3, -1, -3, 5, 3, 6, 7], 3, [3, 3, 5, 5, 6, 7]),
    ([1], 1, [1]),
    ([9, 8, 7, 6], 2, [9, 8, 7]),
    ([4, 4, 4, 4], 2, [4, 4, 4]),
    ([1, -1], 1, [1, -1]),
    ([7, 2, 4], 2, [7, 4]),
]


def harness(func: Callable[[List[int], int], List[int]]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (nums, k, expected) in enumerate(tests, 1):
        try:
            got = func(nums[:], k)
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                print(f"Test {i}: FAILED | expected={expected}, got={got} | nums={nums}, k={k}")
        except Exception as e:
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | nums={nums}, k={k}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


def maxSlidingWindow(nums: List[int], k: int) -> List[int]:
    # Sean style:
    # Deque stores indices in decreasing value order.
    # Front always points to the max of current window.
    if not nums or k == 0:
        return []

    dq: deque[int] = deque()
    out: List[int] = []

    for i, n in enumerate(nums):
        # Remove indices out of this window's left boundary.
        while dq and dq[0] <= i - k:
            dq.popleft()

        # Remove weaker candidates from back.
        while dq and nums[dq[-1]] <= n:
            dq.pop()

        dq.append(i)

        # Start recording once first full window is formed.
        if i >= k - 1:
            out.append(nums[dq[0]])

    return out


harness(maxSlidingWindow)

