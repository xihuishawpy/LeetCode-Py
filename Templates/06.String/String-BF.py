def strStr(haystack: str, needle: str) -> int:
    i = 0
    j = 0
    len1 = len(haystack)
    len2 = len(needle)

    while i < len1 and j < len2:
        if haystack[i] == needle[j]:
            i += 1
            j += 1
        else:
            i -= j - 1
            j = 0

    return i-j if j == len2 else -1
        
print(strStr("abcdeabc", "bcd"))