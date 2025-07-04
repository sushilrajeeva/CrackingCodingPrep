from typing import *
from collections import *
import os, sys
# insert the project root so `import helper` works
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 3. Now you can import your helper module as if it were local:
from helper import helper


# program to get number of nodes

v = 6
int_edges = [
    [0, 1], [1, 2], [4, 5], [2, 4], [1, 5], [1, 4], [2, 5]
]
str_edges = [["Alice","Bob"],["Bob","Carol"],["Alice","Diana"]]
mixed_edges = [["A","B"],["B","C"],["C","A"]]



helper.helper.newProblem("Get number of nodes")
def num_nodes(graph: List[List[int]]) -> int:
    return len(graph)

helper.helper.newProblem("Get number of edges")
def get_total_edges(graph: List[List[int]]) -> int:
    count: int = 0
    for node in range(len(graph)):
        count += len(graph[node])
    return count//2

helper.helper.newProblem("Get degree of a node in graph")
def get_degrees(graph: List[List[int]], node: int) -> int:
    return len(graph[node])

helper.helper.newProblem("Print neighbors")
def print_neighbors(graph: Union[List[List[Any]], Mapping[Any, Any]], node: Any) -> None:
    """Print the neighbors of a single node."""
    print(f"{node!r}:", end="")
    for neighbor in graph[node]:
        print(f" {neighbor!r}", end="")
    print()  # newline

def print_graph(graph: Union[List[List[Any]], Dict[Any, Any]]) -> None:
    """
    Print the entire graph adjacency list.
    Works for both list-of-lists (0…n-1 nodes) and dict-of-containers.
    """
    # Determine node ordering
    if isinstance(graph, Mapping):
        # For dicts, sort keys so it's deterministic
        nodes = sorted(graph.keys(), key=lambda x: str(x))
    else:
        # For lists, assume integer nodes 0..len(graph)-1
        nodes = range(len(graph))

    for node in nodes:
        print_neighbors(graph, node)
        
helper.helper.newProblem("Build adj list")
def build_adjacency_list(edge_list: List[List[int]]) -> List[List[int]]:
    graph: List[List[int]] = [[] for _ in range(v)]
    for node1, node2 in edge_list:
        graph[node1].append(node2)
        graph[node2].append(node1)
    return graph

# integer‐indexed graph
adj_int = build_adjacency_list(int_edges)
print("Integer‐indexed graph:")
print_graph(adj_int)

helper.helper.newProblem("Build adj list when vertices are strings")
def build_adjacency_list_str(edge_list: List[List[int]]) -> Dict[str, List[int]]:
    graph: Dict[str, List[int]] = defaultdict(list)
    for node1, node2 in edge_list:
        graph[node1].append(node2)
        graph[node2].append(node1)
    return graph

# string‐indexed graph with lists
adj_str = build_adjacency_list_str(str_edges)
print("\nString‐indexed graph (lists):")
print_graph(adj_str)

helper.helper.newProblem("Build adj list using set when there is frequent fetch operation")
def build_adjacency_set(edge_list: List[List[int]]) -> Dict[str, set[int]]:
    graph: Dict[str, set[int]] = defaultdict(set)
    for node1, node2 in edge_list:
        graph[node1].add(node2)
        graph[node2].add(node1)
    return graph

# string‐indexed graph with sets
adj_set = build_adjacency_set(mixed_edges)
print("\nString‐indexed graph (sets):")
print_graph(adj_set)

# Connectivity problem set

# 36.2 GRAPH PATH
"""
    Given the adjacnecy list of an undirected graph, graph, and two distinct nodes, node1 and node2, return a simple path from node1 to node2.
    A simple path does not repeat any nodes. Return an empty array if there is no path from node1 to node2.
    
    graph = [
                [1],                # Node 0
                [0, 2, 5, 4],       # Node 1
                [1, 4, 5],          # Node 2
                [],                 # Node 3
                [5, 2, 1],          # Node 4
                [1, 2, 4]           # Node 5
            ]

    node1 = 0 and node2 = 4 
    Output = [0, 1, 4] there are other valid outputs also like [0, 1, 2, 5, 4]

    node1 = 0 and node2 = 3
    output = [] there is no path to node 3
"""

graph = [
                [1],                # Node 0
                [0, 2, 5, 4],       # Node 1
                [1, 4, 5],          # Node 2
                [],                 # Node 3
                [5, 2, 1],          # Node 4
                [1, 2, 4]           # Node 5
]
node1 = 0
node2 = 4

def getPath(graph: List[List[int]], node1: int, node2: int) -> List[int]:
    path: List[int] = []
    v: int = len(graph)

    visited = [False] * v

    def visit(node: int) -> None:
        if visited[node]:
            return False
        visited[node] = True
        path.append(node)

        if node == node2: return True

        for neighbor in graph[node]:
            if visit(neighbor): return True

        path.pop()

        return False
        
    if visit(node1):
        return path
    return []

print("Get Path", getPath(graph, node1, node2))

def getAllPaths(graph: List[List[int]], node1: int, node2: int) -> List[List[int]]:
    path: List[int] = []
    result: List[List[int]] = []
    v: int = len(graph)
    visited = [False] * v

    def visit(node: int) -> None:
        if visited[node]:
            return
        
        visited[node] = True
        path.append(node)

        if node == node2:
            result.append(path.copy())
        else:
            for neighbor in graph[node]:
                visit(neighbor)
        path.pop()
        visited[node] = False

    visit(node1)
    return result
    

        

print("Get all paths", getAllPaths(graph, node1, node2))


# check if graph is a tree

"""
    Given non-empty adjacnece list of an undirected graph, graph, return wheather it is a tree. A graph is a tree if it is acyclic and connected
"""

