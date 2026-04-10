# ============================================================================
# File: lc_049_group_anagrams.py
#
# LeetCode 49: Group Anagrams (Medium)
#
# PROBLEM STATEMENT:
# Given an array of strings strs, group the anagrams together. You can return 
# the answer in any order.
# 
# An Anagram is a word or phrase formed by rearranging the letters of a 
# different word or phrase, typically using all the original letters exactly once.
#
# EXAMPLES:
# - strs = ["eat","tea","tan","ate","nat","bat"] 
#   -> Expected: [["bat"],["nat","tan"],["ate","eat","tea"]]
# - strs = [""]  -> Expected: [[""]]
# - strs = ["a"] -> Expected: [["a"]]
# ============================================================================

from typing import List, Callable, Tuple

# --- TEST CASES ---
# Format: {"kwargs": {...}, "expected": ...}
group_anagrams_tests: List[dict] = [
    {
        "kwargs": {"strs": ["eat", "tea", "tan", "ate", "nat", "bat"]},
        "expected": [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]
    },
    {
        "kwargs": {"strs": [""]},
        "expected": [[""]]
    },
    {
        "kwargs": {"strs": ["a"]},
        "expected": [["a"]]
    }
]

# --- TEST HARNESS ---
def test_harness(func: Callable, test_cases: List[dict]) -> None:
    """
    Test harness for LeetCode #49: Group Anagrams.
    Validates grouped lists of strings, accounting for any internal/external ordering.
    """
    print(f"--- Running Tests for: {func.__name__} ---")
    passed: int = 0
    
    def normalize_groups(groups: List[List[str]]) -> List[List[str]]:
        """Sorts inner groups and the outer list for safe comparison."""
        if groups is None:
            return None
        return sorted([sorted(group) for group in groups])
    
    for i, tc in enumerate(test_cases):
        kwargs = tc["kwargs"]
        expected: List[List[str]] = tc["expected"]
        
        try:
            # Execute the target function directly
            result = func(**kwargs)
            
            # Normalize both expected and actual results for comparison
            norm_result = normalize_groups(result)
            norm_expected = normalize_groups(expected)
            
            if result is None:
                print(f"Test {i+1}: FAILED | Got None, Expected {expected}")
            elif norm_result == norm_expected:
                # Formatting the output to stay readable if arrays are very large
                strs_display = str(kwargs['strs'])
                if len(strs_display) > 40:
                    strs_display = strs_display[:37] + "..."
                print(f"Test {i+1}: PASSED (strs={strs_display})")
                passed += 1
            else:
                print(f"Test {i+1}: FAILED | Got {result}, Expected {expected}")
                        
        except Exception as e:
            print(f"Test {i+1}: ERROR  | {type(e).__name__}: {e}")
            
    print(f"\nSummary: {passed}/{len(test_cases)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def groupAnagrams(strs: List[str]) -> List[List[str]]:
    #To find anagrams and to group them for strictly lowercase strings. 
    #I would rely on a tuple of 26 integers as keys
    def make_me_akey(s: str) -> Tuple[int, ...]:
        lst = [0] * 26
        for ch in s:
            lst[ord(ch) - ord('a')] += 1
        return tuple(lst)
    hmap: dict[Tuple[int, ...], List[str]] = {}
    for s in strs:
        key = make_me_akey(s)
        hmap.setdefault(key, []).append(s)
    return list(hmap.values())
# Execute harness without __main__ block
test_harness(groupAnagrams, group_anagrams_tests)
