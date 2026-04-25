"""
id: cs_q2
title: CodeSignal - Vowel Word Transform
source: codesignal
difficulty: easy
primary: string
tags: [string, array, vowels, two-pointers]
leetcode_equivalent: Similar pattern to LC 917 (Reverse Only Letters)
status: draft
last_updated: 2026-04-24
notes:
- key idea: word[0] + word[1:-1][::-1] + word[-1] when both ends are vowels
- time: O(n * m)
- space: O(n)
"""

VOWELS = set("aeiouAEIOU")


def vowel_transform(words: list[str]) -> list[str]:
    vowels = VOWELS
    out = []
    for word in words:
        if len(word) < 2:
            out.append(word)
        elif word[0] in vowels and word[-1] in vowels:
            middle = word[1:-1]
            out.append(word[0] + middle[::-1] + word[-1])
        else:
            out.append(word)
    return out


print(vowel_transform(["apple"]))            # ["alppe"]
print(vowel_transform(["umbrella"]))         # ["ullerbma"]
print(vowel_transform(["hello"]))            # ["hello"]
print(vowel_transform(["apple", "hello"]))   # ["alppe", "hello"]


def _expected_word(word: str) -> str:
    vowels = set("aeiouAEIOU")
    if len(word) < 2:
        return word
    if word[0] in vowels and word[-1] in vowels:
        return word[0] + word[1:-1][::-1] + word[-1]
    return word


def test():
    # Short sanity checks
    assert vowel_transform(["apple"]) == ["alppe"], "apple"
    assert vowel_transform(["umbrella"]) == ["ullerbma"], "umbrella"
    assert vowel_transform(["hello"]) == ["hello"], "h not vowel"
    assert vowel_transform(["apple", "hello"]) == ["alppe", "hello"], "mixed list"
    assert vowel_transform(["OpenAI"]) == ["OAnepI"], "O/I vowels"
    assert vowel_transform([""]) == [""], "empty string"

    # Long mixed list (120 items)
    base_in = ["apple", "hello", "umbrella", "eve", "OpenAI", "sky", "a", "", "oi", "ende"]
    base_out = ["alppe", "hello", "ullerbma", "eve", "OAnepI", "sky", "a", "", "oi", "edne"]
    long_in = base_in * 12
    long_out = base_out * 12
    assert vowel_transform(long_in) == long_out, "long mixed list"

    # Long mostly-transformable list (105 items)
    mostly_vowel_in = ["audio", "idea", "oboe", "Eerie", "Aba", "uo", "eXe"] * 15
    mostly_vowel_out = ["aiduo", "ieda", "oobe", "Eiree", "Aba", "uo", "eXe"] * 15
    assert vowel_transform(mostly_vowel_in) == mostly_vowel_out, "long mostly-transformable"

    # Long mostly-non-transform list (120 items)
    mostly_non_in = ["hello", "world", "python", "sky", "try", "b", "z", "cat"] * 15
    assert vowel_transform(mostly_non_in) == mostly_non_in, "long mostly-non-transform"

    # Long generated list (1000 items)
    generated = []
    for i in range(250):
        generated.extend(["apple", "beta", "omega", "ufo", "x"])
    expected = [_expected_word(w) for w in generated]
    got = vowel_transform(generated)
    assert got == expected, "long generated list exact match"
    assert len(got) == len(generated), "length preserved"

    print("All Pass!")


test()
