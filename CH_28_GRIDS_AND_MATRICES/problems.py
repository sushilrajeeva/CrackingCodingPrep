from typing import *
import os, sys
# insert the project root so `import helper` works
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 3. Now you can import your helper module as if it were local:
from helper import helper

""" Leetcode 498. Diagonal Traversal

    Given an m x n matrix mat, return an array of all the elements of the array in a diagonal order.

    Example 1: 
    Input: mat = [[1,2,3],[4,5,6],[7,8,9]]
    Output: [1,2,4,7,5,3,6,8,9]

    Example 2: 
    Input: mat = [[1,2],[3,4]]
    Output: [1,2,3,4]
"""


def isValid(grid: List[List[int]], row: int, col: int) -> bool:
        return 0 <= row < len(grid) and 0 <= col < len(grid[0])

# TC => general : O(MXN) since we visit all the cells in the matrix
# SC => O(1)

def findDiagonalOrder(mat: List[List[int]]) -> List[int]:

    up: bool = True
    rows: int = len(mat)
    cols: int = len(mat[0])
    # total diagonals = rows + cols - 1
    itrs = rows + cols - 1

    up_dir = (-1, 1)
    down_dir = (1, -1)

    res: List[int] = []
    
    for itr in range(itrs):
        # pick starting point and direction
        nr, nc = 0, 0
        if up:
            if itr < rows:
                nr, nc = itr, 0
            else:
                nr, nc = rows - 1, itr - rows + 1
            dr, dc = up_dir
            
        else:
            if itr < cols:
                nr, nc = 0, itr
            else:
                nr, nc = itr - cols + 1, cols - 1
            dr, dc = down_dir

        # walk this diagonal until we leave the matrix
        while isValid(mat, nr, nc):
            res.append(mat[nr][nc])
            nr += dr
            nc += dc
        up = not up

    return res

helper.helper.newProblem("Leetcode 498. Diagonal Traversal")
mat = [[1,2,3],[4,5,6],[7,8,9]]
print("Given matrix", mat)
print("Diagonal Traversal Output =", findDiagonalOrder(mat))

""" 36. Valid Sudoku

    Determine if a 9 x 9 Sudoku board is valid. Only the filled cells need to be validated according to the following rules:

        - Each row must contain the digits 1-9 without repetition.
        - Each column must contain the digits 1-9 without repetition.
        - Each of the nine 3 x 3 sub-boxes of the grid must contain the digits 1-9 without repetition.
    
    Note:

        - A Sudoku board (partially filled) could be valid but is not necessarily solvable.
        - Only the filled cells need to be validated according to the mentioned rules.

    Example 1:
    Input: board = 
        [["5","3",".",".","7",".",".",".","."]
        ,["6",".",".","1","9","5",".",".","."]
        ,[".","9","8",".",".",".",".","6","."]
        ,["8",".",".",".","6",".",".",".","3"]
        ,["4",".",".","8",".","3",".",".","1"]
        ,["7",".",".",".","2",".",".",".","6"]
        ,[".","6",".",".",".",".","2","8","."]
        ,[".",".",".","4","1","9",".",".","5"]
        ,[".",".",".",".","8",".",".","7","9"]]
    Output: true

    Example 2:
    Input: board = 
        [["8","3",".",".","7",".",".",".","."]
        ,["6",".",".","1","9","5",".",".","."]
        ,[".","9","8",".",".",".",".","6","."]
        ,["8",".",".",".","6",".",".",".","3"]
        ,["4",".",".","8",".","3",".",".","1"]
        ,["7",".",".",".","2",".",".",".","6"]
        ,[".","6",".",".",".",".","2","8","."]
        ,[".",".",".","4","1","9",".",".","5"]
        ,[".",".",".",".","8",".",".","7","9"]]
    Output: false
    Explanation: Same as Example 1, except with the 5 in the top left corner being modified to 8. Since there are two 8's in the top left 3x3 sub-box, it is invalid.

"""
def valid_rows( board: List[List[int]]) -> bool:
    rows: int = len(board)
    cols: int = len(board[0])

    for row in range(rows):
        seen = set()
        for col in range(cols):
            if board[row][col] in seen:
                return False
            if board[row][col] != ".":
                seen.add(board[row][col])
    return True

def valid_cols( board: List[List[int]]) -> bool:
    rows: int = len(board)
    cols: int = len(board[0])

    for col in range(cols):
        seen = set()
        for row in range(rows):
            if board[row][col] in seen:
                return False
            if board[row][col] != ".":
                seen.add(board[row][col])
    return True

def valid_subgrid(board: List[List[int]], row: int, col: int) -> bool:
    seen = set()
    for r in range(row, row + 3):
        for c in range(col, col + 3):
            if board[r][c] in seen:
                return False
            if board[r][c] != ".":
                seen.add(board[r][c])
    return True

def valid_subgrids(board: List[List[int]]) -> bool:
    for row in range(3):
        for col in range(3):
            if not valid_subgrid(board, row * 3, col * 3):
                return False
    return True

def isValidSudoku(board: List[List[str]]) -> bool:
    return (
        valid_rows(board) and
        valid_cols(board) and
        valid_subgrids(board)
        )

helper.helper.newProblem("Leetcode 36. Valid Sudoku")
board1 = [
             ["5","3",".",".","7",".",".",".","."]
            ,["6",".",".","1","9","5",".",".","."]
            ,[".","9","8",".",".",".",".","6","."]
            ,["8",".",".",".","6",".",".",".","3"]
            ,["4",".",".","8",".","3",".",".","1"]
            ,["7",".",".",".","2",".",".",".","6"]
            ,[".","6",".",".",".",".","2","8","."]
            ,[".",".",".","4","1","9",".",".","5"]
            ,[".",".",".",".","8",".",".","7","9"]
        ]

board2 = [
             ["8","3",".",".","7",".",".",".","."]
            ,["6",".",".","1","9","5",".",".","."]
            ,[".","9","8",".",".",".",".","6","."]
            ,["8",".",".",".","6",".",".",".","3"]
            ,["4",".",".","8",".","3",".",".","1"]
            ,["7",".",".",".","2",".",".",".","6"]
            ,[".","6",".",".",".",".","2","8","."]
            ,[".",".",".","4","1","9",".",".","5"]
            ,[".",".",".",".","8",".",".","7","9"]
        ]
print("Given matrix", board1)
print("Diagonal Traversal Output =", isValidSudoku(board1))


""" Problem 28.6 SUBGRID MAXIMUMS

    Given a rectangular RXC grid of integers, grid, with R > 0 and C > 0, return a new grid with the same dimensions where each cell [r, c]
    contains the maximum in the subgrid with [r, c] in the top-left corner and [R-1, C-1] in the bottom-right corner

    Example 1: grid = [
                        [1, 5, 3],
                        [4, -1, 0],
                        [2, 0, 2]
                    ]

                output = [
                            [5, 5, 3],
                            [4, 2, 2],
                            [2, 2, 2]
                        ]
"""

def subgrid_maximums(grid: List[List[int]]) -> List[List[int]]:
    m: int = len(grid)
    n: int = len(grid[0])

    res: List[List[int]] = [row.copy() for row in grid]

    for r in range(m-1, -1, -1):
        for c in range(n-1, -1, -1):
            if r + 1 < m:
                res[r][c] = max(res[r][c], res[r+1][c])
            if c + 1 < m:
                res[r][c] = max(res[r][c], res[r][c+1])
    return res

grid = [
        [1, 5, 3],
        [4, -1, 0],
        [2, 0, 2]
        ]

helper.helper.newProblem("Problem 28.6 SUBGRID MAXIMUMS")
print("Given matrix", grid)
print("Subgrid maxiums =", subgrid_maximums(grid))


""" Problem 28.7 SUBGRID SUM

    Given a rectangular RXC grid of integers, grid, with R > 0 and C > 0, return a new grid with the same dimensions where each cell [r, c]
    contains the sum of all elements in the subgrid with [r, c] in the top-left corner and [R-1, C-1] in the bottom-right corner

    Example 1: grid = [
                        [-1, 2, 3],
                        [4, 0, 0],
                        [-2, 0, 9]
                    ]

                output = [
                            [15, 14, 12],
                            [11, 9, 9],
                            [7, 9, 9]
                        ]
"""

def subgrid_sums(grid: List[List[int]]) -> List[List[int]]:
    m: int = len(grid)
    n: int = len(grid[0])

    res: List[List[int]] = [row.copy() for row in grid]

    for r in range(m - 1, -1, -1):
        for c in range(n - 1, -1, -1):
            if r + 1 < m:
                res[r][c] += res[r + 1][c]
            if c + 1 < n:
                res[r][c] += res[r][c + 1]
            if r + 1 < m and c + 1 < n:
                res[r][c] -= res[r + 1][c + 1]
    
    return res

grid = [
            [-1, 2, 3],
            [4, 0, 0],
            [-2, 0, 9]
        ]


helper.helper.newProblem("Problem 28.7 SUBGRID SUMS")
print("Given matrix", grid)
print("Subgrid sums =", subgrid_sums(grid))



""" Leetcode 54. Spiral Matrix

    Given an m x n matrix, return all elements of the matrix in spiral order.

    Example 1: matrix = [
                        [1,2,3],
                        [4,5,6],
                        [7,8,9]
                    ]

    Output: [1,2,3,6,9,8,7,4,5]

    Example 2: matrix = [
                            [1,2,3,4],
                            [5,6,7,8],
                            [9,10,11,12]
                        ]
    Output: [1,2,3,4,8,12,11,10,9,5,6,7]

"""

def spiral_order(matrix: List[List[int]]) -> List[int]:
    if not matrix or not matrix[0]:
        return []
    
    m: int = len(matrix)
    n: int = len(matrix[0])

    top: int = 0
    bottom: int = m - 1

    left: int = 0
    right: int = n - 1

    res: List[int] = []

    while top <= bottom and left <= right:

        # 1) Traverse from left → right along the top row
        for col in range(left, right + 1):
            res.append(matrix[top][col])
        top += 1 # moving down the boundry

        # 2) Traverse from top → bottom along the right column
        for row in range(top, bottom + 1):
            res.append(matrix[row][right])
        right -= 1

        # 3) If there’s still a bottom row, traverse right → left
        if left <= right:
            for col in range(right, left - 1, -1):
                res.append(matrix[bottom][col])
            bottom -= 1

        # 4) If there’s still a left column, traverse bottom → top (if it still exist)
        if top <= bottom:
            for row in range(bottom, top - 1, -1):
                res.append(matrix[row][left])
            left += 1

    return res
            


helper.helper.newProblem("Leetcode 54. Spiral Matrix")
mat = [[1,2,3],[4,5,6],[7,8,9]]
print("Given matrix", mat)
print("Spiral order of the matrix =", spiral_order(mat))