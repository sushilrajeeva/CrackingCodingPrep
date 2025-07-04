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

# 27.6 Merge Sort
"""
Given two sorted arrays of integers, arr1 and arr2, return a new array that contains all the elements in arr1 and arr2 in sorted order, 
including duplicates.

Example:    arr1 = [1, 3, 4, 5], arr2 = [2, 4, 4]
Output:     [1, 2, 3, 4, 4, 4, 5]

Example:    arr1 = [-1], arr2 = []
Output:     [-1]

"""

helper.helper.newProblem("27.6 Merge Sort")
arr1 = [1, 3, 4, 5]
arr2 = [2, 4, 4]

def merge(arr1: List[int], arr2: List[int]) -> List[int]:
    result = []

    n1: int = len(arr1)
    n2: int = len(arr2)

    p1: int = 0
    p2: int = 0

    while p1 < n1 and p2 < n2:
        if arr1[p1] <= arr2[p2]:
            result.append(arr1[p1])
            p1 += 1
        else:
            result.append(arr2[p2])
            p2 += 1
    
    while p1 < n1:
        result.append(arr1[p1])
        p1 += 1
    
    while p2 < n2:
        result.append(arr2[p2])
        p2 += 1

    return result

print("Given arr1:", arr1, "arr2:", arr2, "And their merged arr =", merge(arr1, arr2))

# 27.7 2-SUM
"""
Given a sorted array of integers, return wheather there are two distinct indices, i and j, such that arr[i] + arr[j] = 0.
Do not use more than O(1) extra space.

Example:    arr = [-5, -2, -1, 1, 1, 10]
Output:     true. -1 + 1 = 0

Example:    arr = [-3, 0, 0, 1, 2]
Output:     true. 0 + 0 = 0

Example:    arr = [-5, -3, -1, 0, 2, 4, 6]
Output:     false.

"""

helper.helper.newProblem("27.7 2-SUM")
arr = [-5, -2, -1, 1, 1, 10]

def two_sum(arr: List[int]) -> bool:
    n: int = len(arr)
    l: int = 0
    r: int = n - 1

    while l < r:
        if arr[l] + arr[r] < 0:
            l += 1
        elif arr[l] + arr[r] == 0: return True
        else: r-=1

    return False

print("Given arr:", arr, "has a 2-SUM ->", two_sum(arr))


# 27.10 Missing numbers in range
"""
Given a sorted array of integers, arr, and two values indicating a range, [low, high], with low <= high, 
return a new array with all the numbers in the range that do not appear in arr.

Example:    arr = [6, 9, 12, 15, 18], low = 9, high = 13
Output:     [10, 11, 13]

Example:    arr = [], low = 9, high = 9
Output:     [9]

Example:    arr = [6, 7, 8, 9], low = 7, high = 8
Output:     []

"""

helper.helper.newProblem("27.10 Missing numbers in range")
arr = [6, 9, 12, 15, 18]
low = 9
high = 13

def missing_numbers(arr1: List[int], low: int, high: int) -> List[int]:
    result: List[int] = []

    arr2: List[int] = list(range(low, high + 1))

    n1: int = len(arr1)
    n2: int = len(arr2)

    p1: int = 0
    p2: int = 0

    while p1 < n1 and p2 < n2:
        if arr1[p1] == arr2[p2]:
            p1 += 1
            p2 += 1
        elif arr1[p1] < arr2[p2]:
            p1 += 1
        else:
            result.append(arr2[p2])
            p2 += 1

    while p2 < n2:
        result.append(arr2[p2])
        p2 += 1

    return result

print("arr =", arr, "range = [", low, ",", high, "]")
print("Missing numbers:", missing_numbers(arr, low, high))


# 27.11 Interval Intersection
"""
You are given two lists of closed intervals, firstList and secondList,
 where firstList[i] = [starti, endi] and secondList[j] = [startj, endj]. Each list of intervals is pairwise disjoint and in sorted order.

Return the intersection of these two interval lists.

A closed interval [a, b] (with a <= b) denotes the set of real numbers x with a <= x <= b.

The intersection of two closed intervals is a set of real numbers that are either empty or represented as a closed interval. 
For example, the intersection of [1, 3] and [2, 4] is [2, 3].

Example:    firstList = [[0,2],[5,10],[13,23],[24,25]], secondList = [[1,5],[8,12],[15,24],[25,26]]
Output:     [[1,2],[5,5],[8,10],[15,23],[24,24],[25,25]]

Example:    firstList = [[1,3],[5,9]], secondList = []
Output:     []

"""

helper.helper.newProblem("27.11 Interval Intersection")
firstList = [[0,2],[5,10],[13,23],[24,25]]
secondList = [[1,5],[8,12],[15,24],[25,26]]

def intersection(interval1: List[int], interval2: List[int]) -> List[int]:
    overlap_start: int = max(interval1[0], interval2[0])
    overlap_end: int = min(interval1[1], interval2[1])
    return [overlap_start, overlap_end]

def intervalIntersection(firstList: List[List[int]], secondList: List[List[int]]) -> List[List[int]]:

    p1: int = 0
    p2: int = 0

    n1: int = len(firstList)
    n2: int = len(secondList)

    result: List[List[int]] = []

    while p1 < n1 and p2 < n2:
        interval1: List[int] = firstList[p1]
        interval2: List[int] = secondList[p2]

        if interval1[1] < interval2[0]:
            p1 += 1
        elif interval2[1] < interval1[0]:
            p2 += 1
        else:
            result.append(intersection(interval1, interval2))
            if interval1[1] < interval2[1]:
                p1 += 1
            else:
                p2 += 1
                
    return result


print("firstList = ", firstList)
print("secondList =", secondList)
print("Intersections:", intervalIntersection(firstList, secondList))

# 27.13 Parity Sorting
"""
Given an integer array nums, move all the even integers at the beginning of the array followed by all the odd integers.

Return any array that satisfies this condition.

Example:        nums = [3, 1, 2, 4]
Output:         [2,4,3,1]
Explanation:    The outputs [4, 2, 3, 1], [2, 4, 1, 3], and [4, 2, 1, 3] would also be accepted.

Example:        nums = [0]
Output:         [0]

"""

helper.helper.newProblem("27.13 Parity Sorting")

def sortArrayByParity(nums: List[int]) -> List[int]:

    n: int = len(nums)
    l: int = 0
    r: int = n -1

    while l < r:
        if nums[l] % 2 == 0:
            l += 1
        elif nums[r] % 2 == 1:
            r -= 1
        else:
            nums[l], nums[r] = nums[r], nums[l]
            l += 1
            r -= 1
    
    return nums

nums = [3, 1, 2, 4]
print("input = ", nums)
print("Parity Sorted:", sortArrayByParity(nums))

# Seeker and wrier pointer
"""
In-place modification problems can get tricky when we need to read the element from left to right and write from left to right

For problmes like this, we use fast and slow pointers, except that each one has a specific role.

    - Fast pointer is the seeker, looking for the next element to write
    - Slow pointer is the writer, staying at the position where the next element needs to be written.

We can update these pointers accounting to the following recipe.

Recipe 1: Seeker and Writer

def seeker_writer_recipe(arr):
    seeker, writer = 0, 0
    while seeker < len(arr):
        if we need to keep arr[seeker]:
            arr[writer] = arr[seeker]
            writer += 1
            seeker += 1
        else:
            seeker += 1
"""

# 27.14 In-place duplicate removal
"""
Given a sorted array of integers, arr, remove duplicates in place while preserving the order,
and return the number of unique elements. It doesn't matter what remains in arr beyond the unique elements.

Example:        arr = [1, 2, 2, 3, 3, 3, 5]
Output:         4
Explanation:    arr = [1, 2, 3, 5, 0, 0, 0]. The last 3 values could be anything; [1, 2, 3, 5, 1, 2, 3] would also be valid.

Example:        nums = [0]
Output:         [0]

"""

helper.helper.newProblem("27.14 In-place Duplicate Removal")

def remove_duplicates(arr: List[int]) -> int:
    seeker: int = 0
    writer: int = 0
    n: int = len(arr)

    while seeker < n:
        must_keep = seeker == 0 or arr[seeker] != arr[seeker - 1]
        if must_keep:
            arr[writer] = arr[seeker]
            writer += 1
        seeker += 1

    return writer

arr = [1, 2, 2, 3, 3, 3, 5]

print("Given input:", arr)
print("number of unique elements:", remove_duplicates(arr))
print("After removing duplicates:", arr)

