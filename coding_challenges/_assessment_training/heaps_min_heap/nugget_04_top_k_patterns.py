"""Nugget 04: Top-K patterns with heaps."""

from __future__ import annotations

import heapq


def top_k_largest(nums: list[int], k: int) -> list[int]:
    """Keep a min-heap of size k."""
    heap: list[int] = []
    for x in nums:
        if len(heap) < k:
            heapq.heappush(heap, x)
        elif x > heap[0]:
            heapq.heapreplace(heap, x)
    return sorted(heap, reverse=True)


def k_smallest(nums: list[int], k: int) -> list[int]:
    heap = nums[:]
    heapq.heapify(heap)
    return [heapq.heappop(heap) for _ in range(min(k, len(heap)))]


def main() -> None:
    nums = [10, 3, 5, 12, 7, 1, 15, 9]
    k = 3
    print(f"nums={nums}, k={k}")
    print(f"top {k} largest: {top_k_largest(nums, k)}")
    print(f"{k} smallest:    {k_smallest(nums, k)}")


if __name__ == "__main__":
    main()
