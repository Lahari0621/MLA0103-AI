def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    
    # Mark the current node as visited
    visited.add(start)
    print(start, end=" ")

    # Recurse for all unvisited neighbors
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)


# ---------- Main Program ----------
if __name__ == "__main__":
    # Representing the graph as an adjacency list (dictionary)
    graph = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F'],
        'D': [],
        'E': ['F'],
        'F': []
    }

    start_node = 'A'
    print("Depth-First Search starting from node", start_node, ":")
    dfs(graph, start_node)
    