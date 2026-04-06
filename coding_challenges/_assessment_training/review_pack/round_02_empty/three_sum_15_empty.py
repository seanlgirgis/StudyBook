# LeetCode 15: 3Sum (Round 02 Empty)
from typing import Callable, List, Tuple

tests: List[Tuple[List[int], List[List[int]]]] = [
    ([-1, 0, 1, 2, -1, -4], [[-1, -1, 2], [-1, 0, 1]]),
    ([0, 1, 1], []),
    ([0, 0, 0], [[0, 0, 0]]),
    ([-2, 0, 0, 2, 2], [[-2, 0, 2]]),
    ([-5, 1, 2, 2, 3, 3, 4], [[-5, 1, 4], [-5, 2, 3]]),  # duplicate-pair trap
    ([], []),
]


def _normalize(triples: List[List[int]]) -> List[List[int]]:
    return sorted([sorted(t) for t in triples])


def harness(func: Callable[[List[int]], List[List[int]]]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (nums, expected) in enumerate(tests, 1):
        try:
            result = func(nums.copy())
            if _normalize(result) == _normalize(expected):
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                print(f"Test {i}: FAILED")
                print(f"    expected={_normalize(expected)}")
                print(f"    got={_normalize(result)}")
        except Exception as e:
            print(f"Test {i}: ERROR | {type(e).__name__}: {e}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.")


def threeSum(nums: List[int]) -> List[List[int]]:

    nums.sort()
    #return all possibilties that can make up target
    # we return list of values not indexes
    def two_sums(nos: List[int], target)-> List[List[int]]:
        if len(nos) < 2 : return []
        res: list[list[int]] = []
        l, r = 0, len(nos) - 1
        while l < r:
            if target == nos[l] + nos[r] :
                if res:
                    col0 = [row[0] for row in res] 
                    if  nos[l] in col0:
                        l+=1
                        continue
                res.append([nos[l] , nos[r]])
                l += 1
            elif target > (nos[l] + nos[r]):
                l += 1
            else:
                r -= 1
        return res
    ret: list[list[int]] = []
    for i, n in enumerate(nums):
        #we do not calculate for duplicate numbers
        if i > 0 and n == nums[i-1]:
            continue
        lsts = two_sums(nums[i+1:], -n)
        if lsts:
            for lst in lsts:
                alist = [n]
                alist.extend(lst)
                ret.append(alist)
    return ret
    
 


harness(threeSum)
