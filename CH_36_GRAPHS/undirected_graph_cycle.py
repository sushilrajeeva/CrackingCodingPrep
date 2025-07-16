from typing import *
from collections import *

from basic_graphs import print_graph

class Solution:
    
    def build_graph(self, V: int, edges: List[List[int]]) -> Dict[int, Set[int]]:
        graph: Dict[int, Set[int]] = {i: set() for i in range(V)}
        for edge in edges:
            graph[edge[0]].add(edge[1])
            graph[edge[1]].add(edge[0])
        return graph
        
    def bfs_detect(self, source: int, graph: Dict[int, Set[int]], visited: Set[int]) -> bool:
        visited.add(source)
        queue = deque([(source, -1)])
        
        while queue:
            node, parent = queue.popleft()
            
            for neighbor in graph[node]:
                if neighbor == parent:
                    continue
                if neighbor in visited:
                    return True
                visited.add(neighbor)
                queue.append((neighbor, node))
                
        return False

    def dfs_detect(self, source: int, parent: int, graph: Dict[int, Set[int]], visited: Set[int]) -> bool:
        visited.add(source)

        for neighbor in graph[source]:
            if neighbor == parent:
                continue
            if neighbor in visited:
                return True
            visited.add(neighbor)
            if self.dfs_detect(neighbor, source, graph, visited):
                return True
        return False
        
    
    def isCycle(self, V, edges):
		#Code here
        graph: Dict[int, Set[int]] = self.build_graph(V, edges)
        visited: Set[int] = set()
		
        for i in range(V):
            if i not in visited:
                if self.dfs_detect(i, -1, graph, visited): return True
                # if self.bfs_detect(i, graph, visited): return True 
        return False
    

if __name__ == "__main__":

    V: int = 4
    edges1: List[List[int]] = [
                                [0, 1], 
                                [0, 2], 
                                [1, 2],
                                [2, 3]
                            ]
    edges2: List[List[int]] = [
                                [0, 1],
                                [1, 2],
                                [2, 3]
                            ]
    
    sol = Solution()

    print("For given graph : ")
    print_graph(edges1)

    print("Is cycle present ?", sol.isCycle(V, edges1))