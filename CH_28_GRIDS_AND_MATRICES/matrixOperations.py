from typing import *
import os, sys
# insert the project root so `import helper` works
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 3. Now you can import your helper module as if it were local:
from helper import helper

""" 28.8 MATRIX OPERATIONS
    Implement a Matrix class that can be initialized with a square grid of floating point numbers.
    It must have methods for transposition, clockwise rotation, anticlockwise rotation, horizontal reflection,
    and vertical reflection. All the methods should take zero parameters, modify the matrix in place,
    using only O(1) extra space and return nothing
"""

class Matrix:
    def __init__(self, grid: List[List[int]]):
        self.matrix: List[List[int]] = [row.copy() for row in grid]

    def show(self) -> List[List[int]]:
        return self.matrix


    def transpose(self) -> None:
        """
            In this method, we make the rows as columns and columns as rows.
            We achieve this by swapping elements under the main diagonal with elements above it
        """
        for r in range(len(self.matrix)):
            for c in range(r):
                self.matrix[r][c], self.matrix[c][r] = self.matrix[c][r], self.matrix[r][c]
    
    def reflect_horizontally(self) -> None:
        for row in range(len(self.matrix)):
            l = 0
            r = len(self.matrix[row]) - 1
            while l < r:
                self.matrix[row][l], self.matrix[row][r] = self.matrix[row][r], self.matrix[row][l]
                l += 1
                r -= 1
    def reflect_vertically(self) -> None:
        m: int = len(self.matrix)
        for i in range(m//2):
            self.matrix[i], self.matrix[m - i - 1] = self.matrix[m - i -1], self.matrix[i]
    
    """
        For rotation, we can do a trick, we can transpose and do reflection
        for clockwise rotation we can do transpose and followed by horizontal reflection of that result
        and for anti-clockwise rotation we can do transpose and followed by vertical reflection of that result
    """

    def rotate_clockwise(self) -> None:
        self.transpose()
        self.reflect_horizontally()

    def rotate_counterclockwise(self) -> None:
        self.transpose()
        self.reflect_vertically()

    def add(self, B: "Matrix") -> List[List[int]]:
        R: int = len(self.matrix)
        C: int = len(self.matrix[0])

        M: int = len(B.matrix)
        N: int = len(B.matrix[0])

        if R != M or C != N:
            print(f"Invalid operation, matrices must have same dimensions. A is ({R} X {C}), B is ({M} X {N})")
            return None
        
        res: List[List[int]] = [[0] * C for _ in range(R)]

        for i in range(R):
            for j in range(C):
                res[i][j] = (self.matrix[i][j] + B.matrix[i][j])

        return Matrix(res)

    def subtract(self, B: "Matrix") -> List[List[int]]:
        R: int = len(self.matrix)
        C: int = len(self.matrix[0])

        M: int = len(B.matrix)
        N: int = len(B.matrix[0])

        if R != M or C != N:
            print(f"Print invalid operation, row and column should be ({R} X {C})")
            return
        
        res: List[List[int]] = [[0] * C for _ in range(R)]

        for i in range(R):
            for j in range(C):
                res[i][j] = (self.matrix[i][j] - B.matrix[i][j])

        return Matrix(res)

    def dot_product(self, B: "Matrix") -> List[List[int]]:
        A = self.matrix
        R, C = len(A), len(A[0])
        M = len(B.show())
        N = len(B.show()[0])

        if C != M:
            raise ValueError(
                f"Cannot multiply: A is {R}×{C}, B is {M}×{N}"
            )

        # initialize R×N result with zeros
        res: List[List[int]] = [[0] * N for _ in range(R)]

        # triple loop: for each cell (i,j), sum over k
        for i in range(R):
            for j in range(N):
                total = 0
                # dot product of row A[i] and column B[:,j]
                for k in range(C):
                    total += A[i][k] * B.matrix[k][j]
                res[i][j] = total

        return Matrix(res)


helper.helper.newProblem("Leetcode 28.8 MATRIX OPERATIONS")
grid = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
]

mat = Matrix(grid)
print("Given matrix", mat.show())
helper.helper.newProblem("Transpose of matrix")
mat.transpose()
print("Transpose =", mat.show())

mat = Matrix(grid)
helper.helper.newProblem("Horizontal reflection of matrix")
mat.reflect_horizontally()
print("Horizontal reflection =", mat.show())

mat = Matrix(grid)
helper.helper.newProblem("Vertical reflection of matrix")
mat.reflect_vertically()
print("Vertical reflection =", mat.show())


mat = Matrix(grid)
helper.helper.newProblem("Clockwise rotation of matrix")
mat.rotate_clockwise()
print("Clockwise rotation =", mat.show())

mat = Matrix(grid)
helper.helper.newProblem("Counter clockwise rotation of matrix")
mat.rotate_counterclockwise()
print("Counterclockwise rotation =", mat.show())


gridA = [
    [7, 10],
    [8, 11],
    [9, 12]
]
gridB = [
    [1,  2],
    [4, 5],
    [7, 8],
]

A = Matrix(gridA)
B = Matrix(gridB)
C: Matrix = A.add(B)

helper.helper.newProblem("Matrix addition")
print("Matrix A =", A.show())
print("Matrix B =", B.show())
if C:
    print("A + B =", C.show())
else:
    print("Couldn't add two matrix")

gridA = [
    [7, 10],
    [8, 11],
    [9, 12]
]
gridB = [
    [1,  2],
    [4, 5],
    [7, 8],
]

A = Matrix(gridA)
B = Matrix(gridB)
C: Matrix = A.subtract(B)

helper.helper.newProblem("Matrix Subtraction")
print("Matrix A =", A.show())
print("Matrix B =", B.show())
if C:
    print("A - B =", C.show())
else:
    print("Couldn't add two matrix")

helper.helper.newProblem("Matrix multiplication")
gridC = [
    [1, 2],
    [4, 5],
    [7, 8]
]
gridD = [
    [1, 3, 5],
    [0, 2, 4],
]

C = Matrix(gridC)
D = Matrix(gridD)
print("Matrix C =", C.show())
print("Matrix D =", D.show())
product: Matrix = C.dot_product(D)
print("C * D =", product.show())
