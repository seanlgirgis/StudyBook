# LeetCode 347: Top K Frequent Elements

from typing import Callable, List, Tuple

# --- PROBLEM STATEMENT ---
# Given an integer array nums and an integer k, return the k most frequent elements.
# You may return the answer in any order.
#
# Constraints:
# - 1 <= nums.length <= 10^5
# - -10^4 <= nums[i] <= 10^4
# - k is in the range [1, number of unique elements in the array]
# - It is guaranteed that the answer is unique.

# --- TEST CASES ---
# Format: (nums_array, k, expected_elements_any_order)
top_k_tests: List[Tuple[List[int], int, List[int]]] = [
    ([1, 1, 1, 2, 2, 3], 2, [1, 2]),              # 1. Standard example
    ([1], 1, [1]),                                  # 2. Single element
    ([4, 4, 4, 6, 6, 2], 1, [4]),                  # 3. k=1
    ([5, 5, 6, 6, 7, 7, 7], 2, [7, 5]),            # 4. Distinct frequencies
    ([-1, -1, -2, -2, -2, 3], 2, [-2, -1]),        # 5. Negative numbers
    ([10, 10, 20, 20, 20, 30, 30, 30, 30], 2, [30, 20]), # 6. Larger skew
    ([1, 2, 3, 4, 4, 4, 5, 5], 3, [4, 5, 1]),      # 7. Multiple uniques, unique answer guaranteed
    ([9, 9, 8, 8, 8, 7, 7, 7, 7], 3, [7, 8, 9]),   # 8. Top 3 exact ordering irrelevant
    ([0, 0, 0, 1, 1, 2], 2, [0, 1]),               # 9. Includes zero
    ([100, 200, 100, 300, 200, 100], 2, [100, 200])# 10. Mixed values
]

# --- TEST HARNESS ---
def test_harness(func: Callable[[List[int], int], List[int]], test_cases: List[Tuple[List[int], int, List[int]]]) -> None:
    """
    Test harness for LeetCode #347: Top K Frequent Elements.
    Compares results as sets because output order is not important.
    """
    print(f"--- Running Tests for: {func.__name__} ---")
    passed: int = 0

    for i, (nums, k, expected) in enumerate(test_cases):
        try:
            input_nums = nums.copy()
            result: List[int] = func(input_nums, k)

            # Basic structural checks
            if not isinstance(result, list):
                raise TypeError(f"Result must be List[int], got {type(result).__name__}")
            if len(result) != k:
                raise ValueError(f"Result length must be {k}, got {len(result)}")

            # Compare as sets because order may vary
            if set(result) == set(expected):
                display_nums = f"{nums[:8]}..." if len(nums) > 8 else f"{nums}"
                print(f"Test {i+1}: PASSED (k={k}, nums={display_nums})")
                passed += 1
            else:
                display_nums = f"{nums[:8]}..." if len(nums) > 8 else f"{nums}"
                print(f"Test {i+1}: FAILED | k={k}, nums={display_nums}")
                print(f"    Expected set: {set(expected)}")
                print(f"    Got set:      {set(result)}")
        except Exception as e:
            display_nums = f"{nums[:8]}..." if len(nums) > 8 else f"{nums}"
            print(f"Test {i+1}: ERROR  | k={k}, nums={display_nums} | {type(e).__name__}: {e}")

    print(f"\nSummary: {passed}/{len(test_cases)} tests passed.")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
from collections import Counter
def topKFrequent(nums: List[int], k: int) -> List[int]:
    """
    LC 347 — Top K Frequent Elements

    PROBLEM:
    Return the k most frequent elements in nums.

    HINT / APPROACH:
    1. Count frequencies with a hash map/dictionary.
    2. Use one of:
       - bucket sort by frequency (O(n))
       - heap of size k (O(n log k))
    3. Return k elements with highest frequencies.

    Time target: better than O(n log n) full sort where possible.
    """
    # Note to codex .. I cheated the idea..    I need to train on it again and again
    # mainly it is a bucket sort
    # create as many buckets as there are elements + 1
    buckets = [[] for _ in range(len(nums) + 1) ]
    #get frequencies of numbers
    freq = Counter(nums)
    #Drop frequencies in buckets
    max_freq = 0
    res = []
    for num, count in freq.items():
        max_freq = max(count, max_freq)
        buckets[count].append(num)
    
    for i in range(max_freq, 0, -1):
        res.extend(buckets[i])
        if len(res) >= k: break
    return res[:k]


# Execute harness without __main__ block
test_harness(topKFrequent, top_k_tests)
