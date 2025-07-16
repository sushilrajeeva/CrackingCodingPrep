"""
    You are given an m x n grid where each cell can have one of three values:

    0 representing an empty cell,
    1 representing a fresh orange, or
    2 representing a rotten orange.
    Every minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten.

    Return the minimum number of minutes that must elapse until no cell has a fresh orange. If this is impossible, return -1.

    Examples:

        Input: grid = [[2,1,1],[1,1,0],[0,1,1]]
        Output: 4

        Input: grid = [[2,1,1],[0,1,1],[1,0,1]]
        Output: -1
        Explanation: The orange in the bottom left corner (row 2, column 0) is never rotten, because rotting only happens 4-directionally.

        Input: grid = [[0,2]]
        Output: 0
        Explanation: Since there are already no fresh oranges at minute 0, the answer is just 0.

    Constraints:

        m == grid.length
        n == grid[i].length
        1 <= m, n <= 10
        grid[i][j] is 0, 1, or 2.

"""
from typing import *

from collections import *
class Solution:

    def isValidMove(self, grid: List[List[int]], row, col) -> bool:
        return 0 <= row < len(grid) and 0 <= col < len(grid[0]) and grid[row][col] == 1

    def orangesRotting(self, grid: List[List[int]]) -> int:
        directions: List[Tuple[int, int]] = [(1,0),(0,1),(-1,0),(0,-1)]
        max_time: int = 0
        m: int = len(grid)
        n: int = len(grid[0])
        queue = deque([])
        fresh_count: int = 0

        # create a queue of rotten oranges
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 2:
                    queue.append((i, j, 0))
                elif grid[i][j] == 1:
                    fresh_count += 1

        while len(queue) > 0:
            row, col, time = queue.popleft()
            max_time = max(max_time, time)

            for _row, _col in directions:
                r = row + _row
                c = col + _col
                if self.isValidMove(grid, r, c):
                    queue.append((r, c, time + 1))
                    grid[r][c] = 2
                    fresh_count -= 1
        
        if fresh_count > 0:
            return -1
        
        return max_time
    

if __name__ == "__main__":
     
    grid: List[List[int]] = [
                                [2,1,1],
                                [1,1,0],
                                [0,1,1]
                            ]
    
    solution = Solution()

    result: int = solution.orangesRotting(grid)

    print("Max time to rotten oranges is: ", result)
     
    
