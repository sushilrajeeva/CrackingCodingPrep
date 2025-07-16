"""
   Given an m x n 2D binary grid grid which represents a map of '1's (land) and '0's (water), return the number of islands.

    An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. 
    You may assume all four edges of the grid are all surrounded by water. 

    Inputs:
    grid1 = [
            ["1","1","1","1","0"],
            ["1","1","0","1","0"],
            ["1","1","0","0","0"],
            ["0","0","0","0","0"]
        ]

    output: 1

    grid2 = [
            ["1","1","0","0","0"],
            ["1","1","0","0","0"],
            ["0","0","1","0","0"],
            ["0","0","0","1","1"]
            ]
    
    Output: 3

"""

from typing import *
from basic_graphs import print_graph

class Solution:

    def isValidMove(self, grid: List[List[str]], row: int, col: int, visited: List[List[bool]]) -> bool:
        return 0 <= row < len(grid) and 0 <= col < len(grid[0]) and not visited[row][col] and grid[row][col] == "1"

    def numIslands(self, grid: List[List[str]]) -> int:
        count: int = 0
        m: int = len(grid)
        n: int = len(grid[0])
        visited: List[List[bool]] = [[False] * n for _ in range(m)]
        directions: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        def dfs(row: int, col: int) -> None:

            if not self.isValidMove(grid, row, col, visited):
                return

            visited[row][col] = True

            for direction in directions:
                new_row: int = row + direction[0]
                new_col: int = col + direction[1]
                dfs(new_row, new_col)

        for r in range(m):
            for c in range(n):
                if not visited[r][c] and grid[r][c] == "1":
                    count += 1
                    dfs(r, c)
                    

        return count
    

if __name__ == "__main__":

    grid1 = [
                ["1","1","1","1","0"],
                ["1","1","0","1","0"],
                ["1","1","0","0","0"],
                ["0","0","0","0","0"]
            ]
    
    grid2 = [
                ["1","1","0","0","0"],
                ["1","1","0","0","0"],
                ["0","0","1","0","0"],
                ["0","0","0","1","1"]
            ]
    
    sol = Solution()

    print("Give island matrix :")
    print_graph(grid1)

    print("Number of island =", sol.numIslands(grid1))

    print("Give island matrix :")
    print_graph(grid2)

    print("Number of island =", sol.numIslands(grid2))
    
    


        


        