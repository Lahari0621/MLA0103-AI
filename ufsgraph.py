import heapq

def uniform_cost_search(graph, start, goal):
    queue, visited = [(0, start, [])], set()
    while queue:
        cost, node, path = heapq.heappop(queue)
        if node == goal:
            return path + [node], cost
        if node not in visited:
            visited.add(node)
            for neighbor, w in graph.get(node, []):
                heapq.heappush(queue, (cost + w, neighbor, path + [node]))
    return None, float('inf')

def dijkstra(graph, start, goal):
    queue, visited = [(0, start, [])], set()
    while queue:
        cost, node, path = heapq.heappop(queue)
        if node == goal:
            return path + [node], cost
        if node not in visited:
            visited.add(node)
            for neighbor, w in graph.get(node, []):
                heapq.heappush(queue, (cost + w, neighbor, path + [node]))
    return None, float('inf')

graph = {
    'C': [('A', 1)],
    'A': [('F', 4), ('B', 3)],
    'F': [('B', 2), ('G', 1)],
    'B': [('D', 2), ('E', 5), ('G', 7)],
    'D': [('G', 1)],
    'E': [('G', 2)],
    'G': []
}

ucs_path, ucs_cost = uniform_cost_search(graph, 'C', 'G')
dij_path, dij_cost = dijkstra(graph, 'C', 'G')

print(f"UCS: Path = {ucs_path}, Cost = {ucs_cost}")
print(f"Dijkstra: Path = {dij_path}, Cost = {dij_cost}")
