"""Nugget 05: Common tricks and when to use negation."""

from __future__ import annotations

import heapq


def smallest_pair_sum(nums1: list[int], nums2: list[int]) -> tuple[int, int, int]:
    """Tiny example: pick one from each list with smallest sum."""
    heap: list[tuple[int, int, int]] = []  # (sum, a, b)
    for a in nums1:
        for b in nums2:
            heapq.heappush(heap, (a + b, a, b))
    return heapq.heappop(heap)


def main() -> None:
    print("When to use min-heap:")
    print("- You need repeated access to the smallest item.")
    print("- You want K smallest items.")
    print()
    print("When to use max behavior via negation:")
    print("- You need repeated access to the largest item.")
    print("- You want K largest items but only have Python min-heap.")
    print()

    nums = [4, 8, 2, 10]
    max_heap = []
    for x in nums:
        heapq.heappush(max_heap, -x)
    print(f"largest now (via negation): {-max_heap[0]}")

    best_sum, a, b = smallest_pair_sum([1, 7, 11], [2, 4, 6])
    print(f"smallest pair sum example -> sum={best_sum}, pair=({a}, {b})")


if __name__ == "__main__":
    main()
