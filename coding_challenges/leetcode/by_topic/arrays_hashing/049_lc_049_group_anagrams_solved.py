"""
Group Anagrams - Optimization Explanation

Your solution:
    Nested loops comparing every string with every other string.
    Complexity: O(N^2 * K log K).
    For N=10,000 strings, this is extremely slow.

Optimized Approach (Hash Map):
    Instead of comparing strings to each other, we can map them to a COMMON KEY.
    If two strings are anagrams, they must sort to the same string.
    "eat" -> "aet"
    "tea" -> "aet"
    
    Algorithm:
    1. Create a hash map (dictionary).
    2. Iterate through each string ONE time.
    3. Sort the string to get the key.
    4. Append original string to the list at that key.
    
    Complexity: O(N * K log K). 
    We touch each string once, and sorting takes K log K.
    This is much faster than N^2.
"""

from typing import List
from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # Map: sorted_tuple -> list of anagrams
        anagram_map = defaultdict(list)
        
        for s in strs:
            # Create a immutable key: sorted characters
            # "eat" -> ('a', 'e', 't')
            key = tuple(sorted(s))
            anagram_map[key].append(s)
            
        return list(anagram_map.values())

# Test cases to run locally
if __name__ == "__main__":
    solution = Solution()
    
    # Test Case 1
    strs1 = ["eat", "tea", "tan", "ate", "nat", "bat"]
    print(f"Test Case 1: {strs1}")
    print(f"Output: {solution.groupAnagrams(strs1)}")
    
    # Test Case 2
    strs2 = [""]
    print(f"Test Case 2: {strs2}")
    print(f"Output: {solution.groupAnagrams(strs2)}")
