# This Seek and Write can also be called Fast and slow pointers

"""
    In-place modification problems can get tricky when we need to read the elements from left to right and write from left to right

    For problems like this, we can use fast and slow (seek and write) pointers, except that each one has a specific role

        - The fast pointer is the seeker, looking for the next element to write.
        - The slow pointer is the writer, staying at the position where the next elements needs to be written.

        Algo
        Seeker_writer(arr):
            seeker, writer = 0, 0
            while seeker < len(arr):
                if we need to keep arr[seeker]:
                    arr[writer] = arr[seeker]
                    advance both writer and seekr
                else:
                    advance only seeker
"""

from typing import *
import os, sys
# insert the project root so `import helper` works
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 3. Now you can import your helper module as if it were local:
from helper import helper


""" 27.14 IN-PLACE DUPLICATE REMOVEAL
    Given a sorted array of integers, arr, remove duplicates in place while preserving the order, and return the number of unique elements.
    It doesn't matter what remains in arr beyond the unique elements.
    
    Example : arr = [1, 2, 2, 3, 3, 3, 5]
    Output  : [1, 2, 3, 5, 0, 0, 0] or [1, 2, 3, 5, 1, 2, 3] the last values could be anything we are only concenred about the first k valid values
"""

def remove_duplicates(arr: List[int]) -> List[int]:
    fast: int = 0
    slow: int = 0
    n: int = len(arr)

    while fast < n:
        flag: bool = (fast == 0) or (arr[fast] != arr[fast - 1])
        if flag:
            arr[slow] = arr[fast]
            slow += 1
        fast += 1
    return arr

helper.helper.newProblem("27.14 IN-PLACE DUPLICATE REMOVEAL")
arr = [1, 2, 2, 3, 3, 3, 5]
print("Given arr :", arr)
print("Array after removing duplicates in place :", remove_duplicates(arr))