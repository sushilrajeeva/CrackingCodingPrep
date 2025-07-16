# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
from typing import *
from collections import *
'''
Paramenters:
    * an array of currency conversion rates. 
        E.g. ['USD', 'GBP', 0.77] 
        which means 1 USD is equal to 0.77 GBP
    * a list of queries containing a 'from' currency and a 'to' currency
Question:
    Given the above parameters, find the conversion rate that maps to the 'from' currency 
    to the 'to' currency for every single query
Example: 
Rates:   [['USD', 'JPY', 100],['JPY', 'CHN', 20],['CHN', 'THAI', 200]]
queries: [['USD', 'CHN'], ['JPY', 'THAI'], ['USD', 'AUD']]
Output:  [1000.0,  4000.0, -1.0] 
'''
Rates =   [['USD', 'JPY', 100],['JPY', 'CHN', 20],['CHN', 'THAI', 200]]
queries = [['USD', 'CHN'], ['JPY', 'THAI'], ['USD', 'AUD']]

"""
    are the rates always one direction like a->b but not (a->b and b->a) = no
    are currency positive ? yes
    can conversion be floats? yes
    if no relation found between source and dest currency -> -1.0
    1 usd -> chn ?
    1 usd -> 100 jpy
                1 jpy - 20 chn
    1 usd ->      100 jpy -> 2000 chn
    
    Algo : build graph
        TC: O(V)
        SC: O(V)
        for each cur, dest, rate in rates:
            graph[cur].append((dest, rate))
            graph[dest].append((cur, 1.0/rate))
        return graph
    
    TC: O(V+E)
    SC: O(V)
    Algo : dfs for visiting all relationship
        def dfs(s, d, r, visited):
            if s == d: return r
            explore all neighbors of graph[s]:
                cur, rate = neighbor
                if cur in visited:
                    continue
                else:
                    res = 0
                    if cur not in graph: res = -1.0
                    else:
                        res =  dfs(cur, t, rate * r)
            return res
     
    TC: O(N(v+e))
    sc: O(N) + O(V)
    overall : for each query
                create visited array, call dfs 
            
        
"""

class Solution:
    
    def build_currency_graph(self, rates: List[Tuple[str, str, float]]) -> Dict[str, List[Tuple[str, int]]]:
        graph: List[Tuple[str, int]] = defaultdict(list)
        
        for currency1, currency2, rate in rates:
            graph[currency1].append((currency2, rate))
            graph[currency2].append((currency1, (1.0/rate)))
        return graph
        
    def converted_currency_values(self, rates: List[Tuple[str, str, float]], queries: List[Tuple[str, str]]) -> List[float]:
        
        graph: List[Tuple[str, int]] = self.build_currency_graph(rates)
        
        results: List[float] = []
        
        def dfs(source: str, destination: str, value: float, visited: Set[str]) -> float:
            if source == destination:
                return value
            
            visited.add(source)
            
            for currency, rate in graph[source]:
                if currency in visited:
                    continue
                res = dfs(currency, destination, value * rate, visited)
                if res != -1.0:
                    return res
            return -1.0
        
        for src, dest in queries:
            if src not in graph or dest not in graph:
                results.append(-1.0)
            else:
                visited = set()
                result = dfs(src, dest, 1.0, visited)
                results.append(result)
        return results
        
        
# Example usage:
if __name__ == "__main__":
    rates = [
        ["USD", "JPY", 100.0],
        ["JPY", "CHN", 20.0],
        ["CHN", "THAI", 200.0]
    ]
    queries = [
        ["USD", "CHN"],
        ["JPY", "THAI"],
        ["USD", "AUD"]
    ]

    sol = Solution()
    output = sol.converted_currency_values(rates, queries)
    print(output)
    

