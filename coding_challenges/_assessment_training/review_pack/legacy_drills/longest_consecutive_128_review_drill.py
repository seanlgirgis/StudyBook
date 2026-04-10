# LeetCode 128: Longest Consecutive Sequence (Review Drill)

from typing import Callable, List, Tuple


# --- TEST CASES ---
# Format: (nums_array, expected_length)
longest_consecutive_tests: List[Tuple[List[int], int]] = [
    ([100, 4, 200, 1, 3, 2], 4),                  # 1,2,3,4
    ([0, 3, 7, 2, 5, 8, 4, 6, 0, 1], 9),          # 0..8
    ([], 0),                                       # empty
    ([1], 1),                                      # single item
    ([1, 2, 0, 1], 3),                             # duplicates present
    ([-1, -2, -3, 10], 3),                         # negatives
    ([9, 1, 4, 7, 3, -1, 0, 5, 8, -1, 6], 7),     # -1..5 OR 3..9? longest is 7 (3..9)
    ([10, 30, 20], 1),                             # no adjacency
    ([5, 2, 99, 3, 4, 1, 100], 5),                 # 1..5
    ([-3, -2, -1, 0, 1, 2, 50], 6),                # -3..2
]


# --- TEST HARNESS ---
def test_harness(
    func: Callable[[List[int]], int],
    test_cases: List[Tuple[List[int], int]],
) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed: int = 0

    for i, (nums, expected) in enumerate(test_cases):
        try:
            result: int = func(nums.copy())
            if result == expected:
                print(f"Test {i + 1}: PASSED")
                passed += 1
            else:
                print(f"Test {i + 1}: FAILED")
                print(f"    Input:    {nums}")
                print(f"    Expected: {expected}")
                print(f"    Got:      {result}")
        except Exception as e:
            print(f"Test {i + 1}: ERROR | {type(e).__name__}: {e}")

    print(f"\nSummary: {passed}/{len(test_cases)} tests passed.")


# --- YOUR IMPLEMENTATION ---
def longestConsecutive(nums: List[int]) -> int:
    """
    Given an unsorted array of integers nums, return the length of the longest
    consecutive elements sequence.

    You must write an algorithm that runs in O(n) time.
    """
    my_nums = set(nums)
    max_seq = 0
    def seq_length (theSet, num):
        ret = 0 
        while num in theSet:
            ret+=1
            num+=1
        return ret
        
    for num in my_nums:
        if (num - 1) not in my_nums:    #start of a seq
            max_seq = max(max_seq, seq_length(my_nums, num))
    return max_seq


test_harness(longestConsecutive, longest_consecutive_tests)
