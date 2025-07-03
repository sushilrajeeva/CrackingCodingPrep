from typing import *
import os, sys
# insert the project root so `import helper` works
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 3. Now you can import your helper module as if it were local:
from helper import helper

# 27.4 Palindromic sentence [PG-296]
"""
Given a string S, return wheather its letters form a palindrome ignoring puntuation, space, and casing.
Example:    S = "Bob wondered, 'Now, Bob?'"
Output:     true
"""

def palindromic_sentence(s: str) -> bool:

    n: int = len(s)
    l: int = 0
    r: int = n - 1

    while l < r:
        if not s[l].isalpha():
            l += 1
        elif not s[r].isalpha():
            r -= 1
        else:
            if s[l].lower() != s[r].lower(): return False
            l += 1
            r -= 1

    return True

helper.helper.newProblem("27.4 Palindromic sentence")
S = "Bob wondered, 'Now, Bob?'"
print("Given Sentence :", S, "is", "a" if palindromic_sentence(S) else "not a", "Palindrome")


# 27.5 of Reverse case match [PG-298]
"""
Given a string, S, where half of the etters are lowercase and half uppercase, 
return weather the word formed by the lowercase letters is the same as the reverse of the word formed by the uppercae letters.
(Assume that the length, n, is always even.)

Example:    S = "haDrRAHd"
Output:     true. Both spell 'hard' 

Example:    S = "haHrARDd"
Output:     false. The uppercase letters in reverse spell 'drah'. 
"""


def isLower(a: str) -> bool:
    return ord('a') <= ord(a) <= ord('z')
    
def isUpper(a: str) -> bool:
    return ord('A') <= ord(a) <= ord('Z')
    
def getLower(a: str) -> str:
    diff: int = ord(a) - ord('A')
    return chr(ord('a') + diff)

def isRev(s: str) -> bool:
    left: int = 0
    n: int = len(s)
    right: int = n - 1
    
    while left < n and right >= 0:
        if not isLower(s[left]):
            left += 1
        elif not isUpper(s[right]):
            right -= 1
        else:
            if s[left] != getLower(s[right]): return False
            left += 1
            right -= 1
            
    return True

helper.helper.newProblem("27.5 of Reverse case match")
S = "haDrRAHd"
print("Given string:", S," is reversible? :", isRev(S))

