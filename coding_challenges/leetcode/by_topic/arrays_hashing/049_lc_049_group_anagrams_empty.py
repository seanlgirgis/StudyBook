"""
id: lc_0049
title: Group Anagrams
source: leetcode
difficulty: medium
primary: hash-table
tags: [hash-table, strings, sorting]
leetcode_url: https://leetcode.com/problems/group-anagrams/
status: draft
last_updated: 2026-04-11
notes: 
- key idea: Use a hash map where the key is a sorted string or a character frequency tuple.
- time: O(n * k log k) or O(n * k) where n is number of strings and k is max string length.
- space: O(n * k) to store the grouped strings.
"""

# ============================================================================
# File: 049_lc_049_group_anagrams_empty.py
# Problem 49: Group Anagrams (Medium)
# 
# PROBLEM STATEMENT:
# Given an array of strings strs, group the anagrams together. You can return 
# the answer in any order.
#
# An Anagram is a word or phrase formed by rearranging the letters of a 
# different word or phrase, typically using all the original letters exactly once.
#
# EXAMPLES:
# Input: strs = ["eat","tea","tan","ate","nat","bat"]
# Output: [["bat"],["nat","tan"],["ate","eat","tea"]]
#
# Input: strs = [""]
# Output: [[""]]
#
# Input: strs = ["a"]
# Output: [["a"]]
# ============================================================================

from typing import List, Tuple, Callable
import copy

# Test Cases: List[Tuple[input_strs, expected_output]]
# Note: Harness handles nested list comparison by sorting groups
tests: List[Tuple[List[str], List[List[str]]]] = [
    (["eat", "tea", "tan", "ate", "nat", "bat"], [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]),
    ([""], [[""]]),
    (["a"], [["a"]]),
    (["abc", "bca", "cab", "xyz", "zyx"], [["abc", "bca", "cab"], ["xyz", "zyx"]]), # Multiple sets
    (["huh", "hhu", "uhh", "aaa"], [["huh", "hhu", "uhh"], ["aaa"]]),              # Frequency check
    (["stop", "pots", "tops", "opts", "post"], [["stop", "pots", "tops", "opts", "post"]]), # Five-way anagram
    (["apple", "apply"], [["apple"], ["apply"]]),                                 # Similar but different
    (["", "", ""], [["", "", ""]]),                                               # Multiple empty strings
    (["a", "b", "c"], [["a"], ["b"], ["c"]]),                                     # All unique
    (["no", "on", "not", "ton"], [["no", "on"], ["not", "ton"]]),                 # Subsets
    (["aaaaa", "aaaa", "aaa"], [["aaaaa"], ["aaaa"], ["aaa"]]),                   # Length differences
    (["ddddddddddg", "dgggggggggg"], [["ddddddddddg"], ["dgggggggggg"]]),         # Large frequency skew
]

def harness(func: Callable) -> None:
    passed = 0
    failed = 0
    
    print(f"\n--- Testing: {func.__name__} ---")
    
    for i, (strs, expected) in enumerate(tests):
        # Deep copy to prevent mutation
        strs_input = list(strs)
        
        try:
            result = func(strs_input)
            
            # Since order of groups and order within groups doesn't matter:
            # We sort the internal strings, then sort the list of lists.
            normalized_result = sorted([sorted(group) for group in result])
            normalized_expected = sorted([sorted(group) for group in expected])
            
            display_input = str(strs) if len(str(strs)) < 50 else f"{str(strs)[:47]}..."
            
            if normalized_result == normalized_expected:
                print(f"Test {i+1}: PASSED | Input: {display_input}")
                passed += 1
            else:
                print(f"Test {i+1}: FAILED | Input: {display_input}")
                print(f"   Expected: {expected}")
                print(f"   Got:      {result}")
                failed += 1
        except Exception as e:
            print(f"Test {i+1}: ERROR  | Input: {display_input}")
            print(f"   Exception: {e}")
            failed += 1
            
    print(f"\nResults: {passed} Passed, {failed} Failed\n")

# --- USER TO IMPLEMENT SOLUTION BELOW ---

def groupAnagrams(strs: List[str]) -> List[List[str]]:
    """
    Groups strings that are anagrams of each other.
    """
    # use a set of 26 intergers as hashes
    def make_me_tuple(s):
        h = [0] * 26
        for ch in s :
            h[ord(ch) - ord('a')] += 1 
        return tuple(h)
    groups = {}
    for s in strs:
        groups.setdefault(make_me_tuple(s), []).append(s)
    return groups.values()

harness(groupAnagrams)