# LeetCode 49: Group Anagrams (Round 01 Empty)
from typing import Callable, List, Tuple

tests: List[Tuple[List[str], int, List[int]]] = [
    (["eat", "tea", "tan", "ate", "nat", "bat"], 3, [1, 2, 3]),
    ([""], 1, [1]),
    (["a"], 1, [1]),
    (["ab", "ba", "abc", "cab", "bac", "foo"], 3, [1, 2, 3]),
]

def _is_valid_grouping(input_words: List[str], result: List[List[str]]) -> bool:
    if not isinstance(result, list) or any(not isinstance(g, list) for g in result):
        return False
    flattened = [w for g in result for w in g]
    if sorted(flattened) != sorted(input_words):
        return False
    for g in result:
        if not g:
            continue
        sig = sorted(g[0])
        for w in g[1:]:
            if sorted(w) != sig:
                return False
    return True

def harness(func: Callable[[List[str]], List[List[str]]]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (words, expected_count, expected_sizes) in enumerate(tests, 1):
        try:
            result = func(words.copy())
            sizes = sorted(len(g) for g in result) if isinstance(result, list) else []
            if _is_valid_grouping(words, result) and len(result) == expected_count and sizes == expected_sizes:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                print(f"Test {i}: FAILED | expected_count={expected_count}, expected_sizes={expected_sizes}, got={result}")
        except Exception as e:
            print(f"Test {i}: ERROR | {type(e).__name__}: {e}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.")

def groupAnagrams(strs: List[str]) -> List[List[str]]:
    def make_tuple_key(s: str) -> tuple[int, ...]:
        cnts = [0] * 26
        for ch in s :
            cnts[ord(ch) - ord('a')]+=1
        return tuple(cnts)
    out_map: dict[tuple[int, ...], list[str]] = {}
    for s in strs:
        tpl = make_tuple_key(s)
        out_map.setdefault(tpl, []).append(s)
    return list(out_map.values())
harness(groupAnagrams)

