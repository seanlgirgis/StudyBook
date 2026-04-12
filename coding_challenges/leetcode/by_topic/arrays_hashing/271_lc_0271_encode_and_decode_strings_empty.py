"""
id: lc_0271
title: Encode and Decode Strings
source: leetcode
difficulty: medium
primary: hash-table
tags: [strings, design, encoding]
leetcode_url: https://leetcode.com/problems/encode-and-decode-strings/
status: draft
last_updated: 2026-04-11
notes: 
- key idea: Use a length-prefix followed by a delimiter (e.g., "length#string") to handle strings containing any character.
- time: O(n) for both encode and decode.
- space: O(n) to store the encoded string.
"""

# ============================================================================
# File: 271_lc_0271_encode_and_decode_strings_empty.py
# Problem 271: Encode and Decode Strings (Medium)
# 
# PROBLEM STATEMENT:
# Design an algorithm to encode a list of strings to a string. The encoded 
# string is then sent over the network and is decoded back to the original 
# list of strings.
#
# Machine 1 (sender) has the function:
# string encode(vector<string> strs) { ... return encoded_string; }
#
# Machine 2 (receiver) has the function:
# vector<string> decode(string s) { ... return strs; }
#
# Constraints:
# - strs[i] contains any possible characters out of 256 valid ASCII characters.
# - Your algorithm should be as efficient as possible.
# ============================================================================

from typing import List, Tuple, Callable
import copy

# Test Cases: List of string lists to be encoded and then decoded
tests: List[List[str]] = [
    ["hello", "world"],                  # Standard Example 1
    [""],                                # Edge Case: Single empty string
    ["", ""],                            # Edge Case: Multiple empty strings
    ["#", "##", "###"],                  # Boundary: Strings containing the delimiter
    ["10#apple", "5#pear"],              # Boundary: Strings looking like the encoding pattern
    ["!@#$%^&*()_+", "{}[]|\\", ":;\"'<>,.?/"], # Complex: Special characters
    ["a" * 10, "b" * 20, "c" * 5],       # Stress: Different lengths
    ["long_string" * 100],               # Stress: Very long string
    [" ", "  ", "   "],                  # Boundary: Whitespace only
    ["0", "123", "456789"],              # Boundary: Numeric strings
    [],                                  # Edge Case: Empty list
    ["Character with \n newline", "Tab\tincluded"], # Non-printable/Control characters
]

def harness(encode_func: Callable, decode_func: Callable) -> None:
    passed = 0
    failed = 0
    
    print(f"\n--- Testing: {encode_func.__name__} & {decode_func.__name__} ---")
    
    for i, original_strs in enumerate(tests):
        # Deep copy to prevent mutation (though strings are immutable)
        strs_input = list(original_strs)
        
        try:
            encoded = encode_func(strs_input)
            decoded = decode_func(encoded)
            
            display_input = str(original_strs) if len(str(original_strs)) < 50 else f"{str(original_strs)[:47]}..."
            
            if decoded == original_strs:
                print(f"Test {i+1}: PASSED | Input: {display_input}")
                passed += 1
            else:
                print(f"Test {i+1}: FAILED | Input: {display_input}")
                print(f"   Encoded: {repr(encoded)}")
                print(f"   Expected: {original_strs}")
                print(f"   Got:      {decoded}")
                failed += 1
        except Exception as e:
            print(f"Test {i+1}: ERROR  | Input: {display_input}")
            print(f"   Exception: {e}")
            failed += 1
            
    print(f"\nResults: {passed} Passed, {failed} Failed\n")

# --- USER TO IMPLEMENT SOLUTION BELOW ---

def encode(strs: List[str]) -> str:
    if not strs:
        return "|"
    header = ",".join(str(len(s)) for s in strs)
    body = "".join(strs)
    return header + "|" + body

def decode(s: str) -> List[str]:
    if s == "|": return []
    header, body = s.split("|", 1)
    cnts = [int(x) for x in header.split(",")]
    start = end = 0
    out = []
    for length in cnts:
        end += length
        out.append(body[start:end])
        start += length
    return out


# Running the harness with both functions
harness(encode, decode)