# ============================================================================
# File: group_anagrams_049_empty.py
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
# 1) strs = ["eat","tea","tan","ate","nat","bat"] 
#    Expected: [["bat"],["nat","tan"],["ate","eat","tea"]]
# 2) strs = [""] -> Expected: [[""]]
# 3) strs = ["a"] -> Expected: [["a"]]
# ============================================================================

from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (strs, expected_groups)
tests: List[Tuple[List[str], List[List[str]]]] = [
    (["eat", "tea", "tan", "ate", "nat", "bat"], [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]), # Standard Example 1
    ([""], [[""]]),                                      # Standard Example 2
    (["a"], [["a"]]),                                    # Standard Example 3
    (["", "b", ""], [["", ""], ["b"]]),                  # Edge Case: Multiple empty strings
    (["a", "a", "a"], [["a", "a", "a"]]),                # Edge Case: Identical strings
    (["ab", "ba", "abc", "cba", "bca", "a"], [["a"], ["ab", "ba"], ["abc", "bca", "cba"]]), # Mixed lengths
    (["ddddddddddg", "dgggggggggg"], [["ddddddddddg"], ["dgggggggggg"]]), # Boundary: Same chars, different frequencies
    (["cab", "tin", "pew", "duh", "may", "ill", "buy", "bar", "max", "doc"], 
     [["cab"], ["tin"], ["pew"], ["duh"], ["may"], ["ill"], ["buy"], ["bar"], ["max"], ["doc"]]) # Boundary: All unique (no anagrams)
]

# --- TEST HARNESS ---
def harness(func: Callable[[List[str]], List[List[str]]]) -> None:
    """
    Test harness for LeetCode #49: Group Anagrams.
    Normalizes the output to gracefully handle unsorted inner lists and 
    unsorted outer lists since order does not matter for the final result.
    """
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    
    def normalize(groups: List[List[str]]) -> List[Tuple[str, ...]]:
        """Normalizes the list of lists into a sorted list of sorted tuples for safe comparison."""
        if not groups:
            return []
        return sorted([tuple(sorted(g)) for g in groups])

    for i, (strs, expected) in enumerate(tests, 1):
        try:
            # Pass a copy to prevent accidental mutation by the user's function
            got = func(strs.copy())
            
            # Normalize both actual and expected outputs for order-agnostic comparison
            norm_expected = normalize(expected)
            norm_got = normalize(got)
            
            if norm_got == norm_expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                strs_disp = str(strs) if len(strs) <= 10 else f"[{str(strs[:9])[1:-1]}, ...]"
                print(f"Test {i}: FAILED | expected={norm_expected}, got={norm_got} | strs={strs_disp}")
        except Exception as e:
            strs_disp = str(strs) if len(strs) <= 10 else f"[{str(strs[:9])[1:-1]}, ...]"
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | strs={strs_disp}")
            
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")

# --- USER TO IMPLEMENT SOLUTION BELOW ---
def groupAnagrams(strs: List[str]) -> List[List[str]]:
    
    def tuple_me(s):
        lst = [0] * 26
        for ch in s:
            lst[ord(ch) - ord('a')] += 1
        return tuple(lst)
    
    groupings = {}
    
    for s in strs:
        tpl = tuple_me(s)
        groupings.setdefault(tpl, []).append(s)
        
    return list(groupings.values())
        
        
        


# Execute harness without __main__ block
harness(groupAnagrams)
