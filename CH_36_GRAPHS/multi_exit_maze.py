# Problem 36.14 MULTI-EXIT MAZE
"""
    A few friends are trapped on a maze represented by a grid of letters:
        - 'X' represents a wall.
        - 'O' represents an exit. There may be multiple exits.
        - '.' represents walkable space.

    Given the grid, maze, return a grid with the same dimensions. Each cell (r, c) should contain the minimum number of steps needed to go from position
    (r, c) in the maze to the closest exit. If (r, c) is a wall in the maze, return -1 at that position. It is guaranteed that every 
    walkable cell can reach an exit.

    Example:
        maze = [
                    ['.', '.', '.', 'X', '.', 'O'],
                    ['O', 'X', '.', 'X', '.', '.'],
                    ['.', '.', '.', 'X', '.', '.'],
                    ['X', 'O', 'X', '.', 'X', 'X']
                ]

        Output =    [
                        [1, 2, 3, -1, 1, 0],
                        [0, -1, 4, -1, 2, 1],
                        [1, 2, 3, -1, 3, 2],
                        [2, -1, 4, 5, 4, 3],
                        [-1, 0, -1, 6, -1, -1]
                    ]
"""

from typing import *
from collections import *
from basic_graphs import print_graph

class Solution:

    def is_valid_move(self, grid: List[List[str]], distances: List[List[int]], row: int, col: int) -> bool:
        return 0 <= row < len(grid) and 0 <= col < len(grid[0]) and grid[row][col] != "X" and distances[row][col] == -1

    def exit_distances(self, maze: List[List[str]]) -> List[List[int]]:
        m: int = len(maze)
        n: int = len(maze[0])
        distances: List[List[int]] = [[-1] * n for _ in range(m)]
        directions: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        queue = deque()

        for row in range(m):
            for col in range(n):
                if maze[row][col] == "O":
                    queue.append((row, col))
                    distances[row][col] = 0
        
        while queue:
            r, c = queue.popleft()

            for direction in directions:
                new_row: int = r + direction[0]
                new_col: int = c + direction[1]

                if self.is_valid_move(maze, distances, new_row, new_col):
                    distances[new_row][new_col] = distances[r][c] + 1
                    queue.append((new_row, new_col))

        return distances
    

if __name__ == "__main__":

    maze = [
                ['.', '.', '.', 'X', '.', 'O'],
                ['O', 'X', '.', 'X', '.', '.'],
                ['.', '.', '.', 'X', '.', '.'],
                ['.', 'X', '.', '.', '.', '.'],
                ['X', 'O', 'X', '.', 'X', 'X']
            ]
    
    sol = Solution()
    
    print("Given maze :")

    print_graph(maze)

    print("Distance matrix of each cell to nearest exit :")
    print_graph(sol.exit_distances(maze))


