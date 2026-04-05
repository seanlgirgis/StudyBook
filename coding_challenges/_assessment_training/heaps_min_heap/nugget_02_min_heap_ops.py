"""Nugget 02: Core min-heap operations."""

from __future__ import annotations

import heapq


def main() -> None:
    heap: list[int] = []

    for x in [5, 2, 8, 1]:
        heapq.heappush(heap, x)
        print(f"push {x:>2} -> heap: {heap}")

    print()
    print("pop in sorted order (smallest first):")
    while heap:
        print(heapq.heappop(heap), end=" ")
    print()


if __name__ == "__main__":
    main()
