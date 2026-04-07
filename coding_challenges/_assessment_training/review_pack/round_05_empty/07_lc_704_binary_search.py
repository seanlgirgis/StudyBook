# ============================================================================
# File: 07_lc_704_binary_search.py
#
# LeetCode 704: Binary Search (Easy)
#
# PROBLEM STATEMENT:
# Given an array of integers nums which is sorted in ascending order, and an
# integer target, write a function to search target in nums.
#
# If target exists, then return its index. Otherwise, return -1.
# You must write an algorithm with O(log n) runtime complexity.
# ============================================================================

from typing import List, Callable

# --- TEST CASES ---
# Format: {"kwargs": {...}, "expected": ...}
binary_search_tests: List[dict] = [
    {"kwargs": {"nums": [-1, 0, 3, 5, 9, 12], "target": 9}, "expected": 4},
    {"kwargs": {"nums": [-1, 0, 3, 5, 9, 12], "target": 2}, "expected": -1},
    {"kwargs": {"nums": [1], "target": 1}, "expected": 0},
    {"kwargs": {"nums": [1], "target": 0}, "expected": -1},
    {"kwargs": {"nums": [2, 4, 6, 8, 10], "target": 2}, "expected": 0},
    {"kwargs": {"nums": [2, 4, 6, 8, 10], "target": 10}, "expected": 4},
]


# --- TEST HARNESS ---
def test_harness(func: Callable, test_cases: List[dict]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed: int = 0

    for i, tc in enumerate(test_cases):
        kwargs = tc["kwargs"]
        expected: int = tc["expected"]

        try:
            result = func(**kwargs)

            if result == expected:
                nums_display = str(kwargs["nums"])
                if len(nums_display) > 30:
                    nums_display = nums_display[:27] + "..."
                print(
                    f"Test {i + 1}: PASSED (nums={nums_display}, target={kwargs['target']})"
                )
                passed += 1
            else:
                print(
                    f"Test {i + 1}: FAILED | Got {result}, Expected {expected} "
                    f"(nums={kwargs['nums']}, target={kwargs['target']})"
                )

        except Exception as e:
            print(f"Test {i + 1}: ERROR  | {type(e).__name__}: {e}")

    print(f"\nSummary: {passed}/{len(test_cases)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def search(nums: List[int], target: int) -> int:
    l, r = 0, len(nums) - 1
    while l <= r:
        mid = l + (r - l) // 2
        n_at_mid = nums[mid]
        if n_at_mid == target:
            return mid
        if target < n_at_mid:            # val is on the left side.. search left
            r = mid - 1
        else:                            # val is on the right side.. search right
            l = mid + 1
    return -1


# Execute harness without __main__ block
test_harness(search, binary_search_tests)
