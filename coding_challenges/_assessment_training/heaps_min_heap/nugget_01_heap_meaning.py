"""Nugget 01: What is a heap?"""

from __future__ import annotations

import heapq


def main() -> None:
    print("Heap intuition:")
    print("- Heap is a data structure where the smallest element is always easy to access.")
    print("- In Python `heapq`, it is a MIN heap by default.")
    print()

    nums = [9, 3, 7, 1, 6]
    print(f"Start list: {nums}")

    heapq.heapify(nums)  # rearranges list into heap structure in-place
    print(f"After heapify: {nums}")
    print(f"Smallest (root): {nums[0]}")


if __name__ == "__main__":
    main()
