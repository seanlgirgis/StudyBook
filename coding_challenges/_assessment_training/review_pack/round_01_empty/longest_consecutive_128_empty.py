# LeetCode 128: Longest Consecutive Sequence (Round 01 Empty)
from typing import Callable, List, Tuple

tests: List[Tuple[List[int], int]] = [
    ([100, 4, 200, 1, 3, 2], 4),
    ([0, 3, 7, 2, 5, 8, 4, 6, 0, 1], 9),
    ([], 0),
    ([1], 1),
    ([1, 2, 0, 1], 3),
]

def harness(func: Callable[[List[int]], int]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (nums, expected) in enumerate(tests, 1):
        try:
            result = func(nums.copy())
            if result == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                print(f"Test {i}: FAILED | expected={expected}, got={result}")
        except Exception as e:
            print(f"Test {i}: ERROR | {type(e).__name__}: {e}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.")

def longestConsecutive(nums: List[int]) -> int:

    my_nums = set(nums)
    def get_seq_length(n) -> int:
        ret = 0
        while n in my_nums:
            ret += 1
            n += 1
        return ret
            
    longest_cons = 0 
    for n in my_nums:
        if n - 1 not in my_nums:    # start of group
            longest_cons = max(longest_cons, get_seq_length(n))
    return longest_cons
harness(longestConsecutive)

