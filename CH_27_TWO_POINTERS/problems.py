from typing import *
import os, sys
# insert the project root so `import helper` works
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 3. Now you can import your helper module as if it were local:
from helper import helper

""" 27.2 SMALLER PREFIXES
    Given an array of integers, arr, where the length n, is even, return whether the following condition holds for every k in the range 1 <= k <= n/2.
    "The sum of first k elements is smaller than the sum of the first 2k elements".
    If this condition is false for any k in the range, return false.
"""

def smaller_prefix(arr: List[int]) -> bool:
    slow: int = 0
    fast: int = 0
    n: int = len(arr)

    slow_total: int = 0
    fast_total: int = 0

    while fast < n:
        slow_total += arr[slow]
        fast_total += arr[fast] + arr[fast + 1]

        if slow_total >= fast_total:
            return False
        
        slow += 1
        fast += 2 

    return True

helper.helper.newProblem("27.2 SMALLER PREFIXES")
arr = [1, 2, 2, -1]
print("Given arr :", arr)
print("Is smaller prefix ?", "Yes" if smaller_prefix(arr) else "No")


""" 27.3 ARRAY INTERSECTION
    Given two sorted arrays of integers, arr1, and arr2.
    Return a new arr with the elements that appear in both sorted order, including duplicates present in both arrays

    Example : arr1 = [1, 2, 3] arr2 = [1, 3, 5]
    output: [1, 3]

    Example : arr1 = [1, 1, 1] arr2 = [1, 1]
    output: [1, 1]
"""

def common_elements(arr1: List[int], arr2: List[int]) -> List[int]:
    res: List[int] = []
    p1: int = 0
    p2: int = 0
    m: int = len(arr1)
    n: int = len(arr2)

    while p1 < m and p2 < n:
        if arr1[p1] == arr2[p2]:
            res.append(arr1[p1])
            p1 += 1
            p2 += 1
        elif arr1[p1] < arr2[p2]:
            p1 += 1
        else:
            p2 += 1
    return res

helper.helper.newProblem("27.3 ARRAY INTERSECTION")
arr1 = [1, 2, 3]
arr2 = [1, 3, 5]
print("Given arr1 :", arr1, "arr2 :", arr2)
print("Common elements in both arrays :", common_elements(arr1, arr2))


""" 27.6 MERGE TWO SORTED ARRAYS
    Given two sorted arrays of integers, arr1, and arr2.
    Return a new arrary that contains all the elements in arr1 and arr2 in sorted order, including duplicates

    Example : 1
    output: [1, 2, 3, 4, 4, 4, 5]

    Example : arr1 = [-1] arr2 = []
    output: [-1]
"""

def merge_two_sorted_arrays(arr1: List[int], arr2: List[int]) -> List[int]:
    p1: int = 0
    p2: int = 0

    m: int = len(arr1)
    n: int = len(arr2)

    res: List[int] = []

    while p1 < m and p2 < n:
        if arr1[p1] < arr2[p2]:
            res.append(arr1[p1])
            p1 += 1
        else:
            res.append(arr2[p2])
            p2 += 1

    while p1 < m:
        res.append(arr1[p1])
        p1 += 1
    
    while p2 < n:
        res.append(arr2[p2])
        p2 += 1

    return res

helper.helper.newProblem("27.6 MERGE TWO SORTED ARRAYS")
arr1 = [1, 3, 4, 5]
arr2 = [2, 4, 4]
print("Given arr1 :", arr1, "arr2 :", arr2)
print("Sorted Array :", merge_two_sorted_arrays(arr1, arr2))


""" 27.7 2 SUM
    Given a sorted array of integers, return wheather there are two distinct indices, i and j, such that arr[i] + arr[j] == 0.
    Do not use more than O(1) extra space.

    Example : arr = [-5, -2, -1, 1, 1, 10]
    output  : true (-1 + 1) = 0

    Example : arr = [-3, 0, 0, 1, 2]
    output  : true (0 - 0 = 0)

    Example : arr = [-5, -3, -1, 0, 2, 4, 6]
    output  : false
"""

def two_sum(arr: List[int]) -> bool:
    l: int = 0
    n: int = len(arr)
    r: int = n - 1

    while l < r:
        if arr[r] < 0 or arr[l] > 0: return False
        total: int = arr[l] + arr[r]
        if total == 0: return True
        elif total < 0:
            l += 1
        else:
            r -= 1
    return False

helper.helper.newProblem("27.7 2 SUM")
arr = [-5, -2, -1, 1, 1, 10]
print("Given arr :", arr)
print("Has sum == 0 :", two_sum(arr))

""" 27.8 THREE WAY MERGE WITHOUT DUPLICATES
    Given three sorted arrays of integers, arr1, arr2, and arr3.
    Return a new arrary that contains all the elements in arr1, arr2 and arr3 in sorted order, without duplicates

    Example : arr1 = [2, 3, 3, 4, 5, 7] arr2 = [3, 3, 9] arr3 = [3, 3, 9]
    output: [2, 3, 4, 5, 7, 9]
"""

def merge_three_sorted(arr1: List[int], arr2: List[int], arr3: List[int]) -> List[int]:
    p1: int = 0
    p2: int = 0
    p3: int = 0

    x: int = len(arr1)
    y: int = len(arr2)
    z: int = len(arr3)

    res: List[int] = []

    while p1 < x and p2 < y and p3 < z:
        val = min(arr1[p1], arr2[p2], arr3[p3])
        if not res or res[-1] != val:
            res.append(val)
        
        if arr1[p1] == val:
            p1 += 1
        if arr2[p2] == val:
            p2 += 1
        if arr3[p3] == val:
            p3 += 1

    
    def merge_two(a, pa, lena, b, pb, lenb):
        nonlocal res

        while pa < lena and pb <lenb:
            v = min(a[pa], b[pb])
            if not res or res[-1] != v:
                res.append(v)
            
            if a[pa] == v:
                pa += 1
            if b[pb] == v:
                pb += 1
            
        while pa < lena:
            v = a[pa]
            pa += 1
            if not res or res[-1] != v:
                res.append(v)
        
        while pb < lenb:
            v = b[pb]
            pb += 1
            if not res or res[-1] != v:
                res.append(v)

    if p1 < x and p2 < y:
        merge_two(arr1, p1, x, arr2, p2, y)
    elif p1 < x and p3 < z:
        merge_two(arr1, p1, x, arr3, p3, z)
    elif p2 < y and p3 < z:
        merge_two(arr2, p2, y, arr3, p3, z)
    else:
        lst = None
        p = None
        pmax = None
        if p1 < x:
            lst = arr1
            p = p1
            pmax = x
        elif p2 < y:
            lst = arr2
            p = p2
            pmax = y
        else:
            lst = arr3
            p = p3
            pmax = z
        
        while p < pmax:
            if not res or res[-1] != lst[p]:
                res.append(lst[p])
            p += 1

    return res     


helper.helper.newProblem("27.8 3-WAY MERGE WITHOUT DUPLICATES")
arr1 = [2, 3, 3, 4, 5, 7]
arr2 = [3, 3, 9]
arr3 = [3, 3, 9]
print("Given arr1 :", arr1, "arr2 :", arr2, "and arr3 :", arr3)
print("Sorted Array :", merge_three_sorted(arr1, arr2, arr3))


""" 27.13 PARITY SORTING
    Given an array of integers, arr, modify it in place to put all even numbers before all odd numbers. The relative order between even numbers doesn't matter.
    Same for the odd numbers.

    Example : arr = [1, 2, 3, 4, 5]
    Output  : [4, 2, 3, 1, 5]
"""

def parity_sorting(arr: List[int]) -> List[int]:
    left: int = 0
    n: int = len(arr)
    right: int = n - 1

    while left < right:
        if arr[left] % 2 == 0:
            left += 1
        elif arr[right] % 2 == 1:
            right -= 1
        else:
            arr[left], arr[right] = arr[right], arr[left]
            left += 1
            right -= 1
    return arr


helper.helper.newProblem("27.13 PARITY SORTING")
arr = [1, 2, 3, 4, 5]
print("Given arr :", arr)
print("Parity sorted Array :", parity_sorting(arr))

