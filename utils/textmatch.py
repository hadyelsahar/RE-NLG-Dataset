"""
https://github.com/laurentluce/python-algorithms
"""

def string_matching_rabin_karp(text='', pattern='', hash_base=256):
    """Returns positions where pattern is found in text.
    worst case: O(nm)
    O(n+m) if the number of valid matches is small and the pattern is large.
    Performance: ord() is slow so we shouldn't use it here
    Example: text = 'ababbababa', pattern = 'aba'
             string_matching_rabin_karp(text, pattern) returns [0, 5, 7]
    @param text text to search inside
    @param pattern string to search for
    @param hash_base base to calculate the hash value
    @return list containing offsets (shifts) where pattern is found inside text
    """

    n = len(text)
    m = len(pattern)
    offsets = []
    htext = hash_value(text[:m], hash_base)
    hpattern = hash_value(pattern, hash_base)
    for i in range(n-m+1):
        if htext == hpattern:
            if text[i:i+m] == pattern:
                offsets.append(i)
        if i < n-m:
            htext = (hash_base *
                     (htext -
                      (ord(text[i]) *
                       (hash_base ** (m-1))))) + ord(text[i+m])

    return offsets


def hash_value(s, base):
    """Calculate the hash value of a string using base.
    Example: 'abc' = 97 x base^2 + 98 x base^1 + 99 x base^0
    @param s string to compute hash value for
    @param base base to use to compute hash value
    @return hash value
    """
    v = 0
    p = len(s)-1
    for i in range(p+1):
        v += ord(s[i]) * (base ** p)
        p -= 1

    return v