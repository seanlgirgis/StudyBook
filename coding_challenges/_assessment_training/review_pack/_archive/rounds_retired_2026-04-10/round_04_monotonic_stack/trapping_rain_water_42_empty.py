# LeetCode 42: Trapping Rain Water (Monotonic Decreasing Stack Variant)
#
# PROBLEM STATEMENT
# Given non-negative heights where width of each bar is 1, compute how much water
# can be trapped after raining.
#
# MONOTONIC PATTERN
# A monotonic decreasing stack of indices can identify bounded valleys and fill area.

from typing import Callable, List, Tuple

tests: List[Tuple[List[int], int]] = [
    ([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6),
    ([4, 2, 0, 3, 2, 5], 9),
    ([1, 0, 1], 1),
    ([3, 3, 3], 0),
    ([], 0),
]


def harness(func: Callable[[List[int]], int]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (height, expected) in enumerate(tests, 1):
        try:
            got = func(height[:])
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                print(f"Test {i}: FAILED | expected={expected}, got={got}")
        except Exception as e:
            print(f"Test {i}: ERROR | {type(e).__name__}: {e}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.")


def trap(height: List[int]) -> int:
    trapped = 0
    # Stack stores indices of bars.
    # We keep bar heights in monotonic decreasing order from bottom -> top of stack.
    # When current bar is taller than stack top, we found a right boundary for a valley.
    stack: List[int] = []

    for i, h in enumerate(height):
        # Resolve every valley where current bar can serve as the right wall.
        while stack and height[stack[-1]] < h:
            # Valley floor index (the "bottom" bar).
            bottom_idx = stack.pop()

            # No left boundary available to trap water.
            if not stack:
                break

            # Left boundary is now the new top of stack.
            left_idx = stack[-1]
            # Width is the distance between boundaries minus the boundaries themselves.
            width = i - left_idx - 1
            # Water level is limited by the shorter boundary.
            # Subtract valley floor height to get actual water height above this bottom.
            bounded_height = min(height[left_idx], h) - height[bottom_idx]

            if bounded_height > 0:
                # Add area of this trapped segment.
                trapped += width * bounded_height

        # Push current bar as a candidate boundary for future valleys.
        stack.append(i)

    return trapped
harness(trap)


def trap2(height: List[int]) -> int:
    water = [0] * len(height)
    max_left = [0] * len(height)
    max_right = [0] * len(height)
    for i in range(1, len(height)):
        max_left[i] = max(height[i-1], max_left[i-1])
    for i in range(len(height)-2, -1, -1):
        max_right[i] = max(height[i+1], max_right[i+1])
    for i in range(len(height)):
        val = min(max_left[i], max_right[i]) - height[i]
        water[i] = val if val > 0 else 0
    return sum(water)
        

harness(trap2)


def trap3(height: List[int]) -> int:
    # Same DP idea as trap2, but avoid the extra per-index water array.
    max_left = [0] * len(height)
    max_right = [0] * len(height)

    for i in range(1, len(height)):
        max_left[i] = max(height[i - 1], max_left[i - 1])

    for i in range(len(height) - 2, -1, -1):
        max_right[i] = max(height[i + 1], max_right[i + 1])

    total = 0
    for i in range(len(height)):
        bounded_height = min(max_left[i], max_right[i]) - height[i]
        if bounded_height > 0:
            total += bounded_height

    return total


harness(trap3)

def trap4(height: List[int]) -> int:
    if not height:
        return 0

    l, r = 0, len(height) - 1
    left_max, right_max = height[l], height[r]
    total = 0
    
    while l < r:
        if left_max < right_max:
            l += 1
            if left_max > height[l]:
                total += left_max - height[l]
            left_max = max(left_max, height[l])
        else:
            r -= 1
            if right_max > height[r]:
                total += right_max - height[r]
            right_max = max(right_max, height[r])
    return total

harness(trap4)
            
