# LeetCode 49: Group Anagrams (Blank Practice)

from typing import Callable, List, Tuple


# Format: (input_words, expected_group_count, expected_group_sizes_sorted)
group_anagrams_tests: List[Tuple[List[str], int, List[int]]] = [
    (["eat", "tea", "tan", "ate", "nat", "bat"], 3, [1, 2, 3]),
    ([""], 1, [1]),
    (["a"], 1, [1]),
    (["ab", "ba", "abc", "cab", "bac", "foo"], 3, [1, 2, 3]),
    (["listen", "silent", "enlist", "google", "gogole"], 2, [2, 3]),
    (["aa", "aa", "aa"], 1, [3]),
    (["abc", "def", "ghi"], 3, [1, 1, 1]),
    (["bob", "obb", "bbo", "cat", "act", "tac"], 2, [3, 3]),
]


def _is_valid_grouping(input_words: List[str], result: List[List[str]]) -> Tuple[bool, str]:
    if not isinstance(result, list):
        return False, f"Result must be List[List[str]], got {type(result).__name__}"
    if any(not isinstance(g, list) for g in result):
        return False, "Each group must be a list of strings"
    if any(any(not isinstance(w, str) for w in g) for g in result):
        return False, "All grouped elements must be strings"

    flattened: List[str] = [w for g in result for w in g]
    if sorted(flattened) != sorted(input_words):
        return False, "Grouped output does not contain exactly the input words"

    for g in result:
        if not g:
            continue
        signature = sorted(g[0])
        for w in g[1:]:
            if sorted(w) != signature:
                return False, f"Invalid group {g}: not all words are anagrams"

    return True, "ok"


def test_harness(
    func: Callable[[List[str]], List[List[str]]],
    test_cases: List[Tuple[List[str], int, List[int]]],
) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed: int = 0

    for i, (words, expected_groups, expected_sizes) in enumerate(test_cases):
        try:
            result = func(words.copy())
            valid, reason = _is_valid_grouping(words, result)
            if not valid:
                print(f"Test {i + 1}: FAILED")
                print(f"    Reason: {reason}")
                print(f"    Got:    {result}")
                continue

            sizes = sorted(len(g) for g in result)
            if len(result) == expected_groups and sizes == expected_sizes:
                print(f"Test {i + 1}: PASSED")
                passed += 1
            else:
                print(f"Test {i + 1}: FAILED")
                print(f"    Expected group count: {expected_groups}")
                print(f"    Got group count:      {len(result)}")
                print(f"    Expected sizes:       {expected_sizes}")
                print(f"    Got sizes:            {sizes}")
        except Exception as e:
            print(f"Test {i + 1}: ERROR | {type(e).__name__}: {e}")

    print(f"\nSummary: {passed}/{len(test_cases)} tests passed.")

from typing import Tuple, List
def groupAnagrams(strs: List[str]) -> List[List[str]]:
    def makeMeTuple(s):
        counts = [0] *26
        for ch in s:
            counts[ord(ch)-ord('a')] +=1
        return tuple(counts)
    dict = {}
    for s in strs:
        dict.setdefault(makeMeTuple(s), []).append(s)
    return list(dict.values())
        


test_harness(groupAnagrams, group_anagrams_tests)
