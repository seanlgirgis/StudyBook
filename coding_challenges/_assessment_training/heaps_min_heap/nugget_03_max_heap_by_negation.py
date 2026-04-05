"""Nugget 03: Simulate max-heap using negation."""

from __future__ import annotations

import heapq


def main() -> None:
    nums = [5, 1, 9, 3]
    print(f"Original nums: {nums}")

    # Python has min-heap only, so store negatives.
    max_heap = [-x for x in nums]
    heapq.heapify(max_heap)
    print(f"Internal heap (negatives): {max_heap}")

    print("max values in descending order:")
    while max_heap:
        largest = -heapq.heappop(max_heap)
        print(largest, end=" ")
    print()


if __name__ == "__main__":
    main()
