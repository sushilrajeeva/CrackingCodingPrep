"""
  Given two lists of strings -"sentence" and "words" find the shortest substring such that "sentence" contains every word in "words"

  Example
  sentence = ['is', 'one', 'ok', 'you', 'the', 'frog', 'ok', 'one', 'the', 'you', 'is', 'not', 'frog']
  words = ['is', 'you', 'frog']

  answer = "you is not frog"

"""

from typing import *
from collections import *
class Solution:

  def getShortestSubstring(self, sentence: List[str], words: List[str]) -> str:

    if not words or not sentence:
      return ""

    m: int = len(sentence)
    n: int = len(words)

    if m < n: return ""

    word_map = defaultdict(int)
    for word in words:
      word_map[word] += 1

    s_map = defaultdict(int)

    required = len(word_map)
    formed = 0
    min_len = float("inf")
    res: str = ""
    l = 0

    for r, word in enumerate(sentence):
      s_map[word] += 1
      if word in word_map and word_map[word] == s_map[word]:
        formed += 1

      while l <= r and formed == required:
        cur_sen = " ".join(sentence[l : r+1])
        cur_len = len(cur_sen)
        if cur_len < min_len:
          min_len = cur_len
          res = cur_sen

        left_ele = sentence[l]
        s_map[left_ele] -= 1
        l += 1

        if left_ele in word_map and s_map[left_ele] < word_map[left_ele]:
          formed -= 1

    return res


if __name__ == "__main__":
  sentence = ['is', 'one', 'ok', 'you', 'the', 'frog', 'ok', 'one', 'the', 'you', 'is', 'not', 'frog']
  words = ['is', 'you', 'frog']

  sol = Solution()
  print("Given sentence :", sentence)
  print("Given words :", words)

  print("Res :", sol.getShortestSubstring(sentence, words))
        

