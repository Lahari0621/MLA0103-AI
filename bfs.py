from collections import deque

def bfs(graph, start):
    visited = []
    queue = deque([start])

    while queue:
        node = queue.popleft()
        if node not in visited:
            print(node, end=" ")
            visited.append(node)
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    queue.append(neighbor)

# ---- MAIN PROGRAM ----
graph = {}

n = int(input("Enter the number of levels in the graph: "))

print("\nEnter each node and its neighbors.")
print("Example: For node A with neighbors B and C, enter: A B C")
print("          For node 1 with neighbors 2 and 3, enter: 1 2 3\n")

for _ in range(n):
    data = input("Enter node and its neighbors: ").split()
    node = data[0]
    # Convert to int if possible
    try:
        node = int(node)
    except ValueError:
        pass

    neighbors = []
    for val in data[1:]:
        try:
            neighbors.append(int(val))
        except ValueError:
            neighbors.append(val)

    graph[node] = neighbors

# Display the graph
print("\nGraph (Adjacency List):")
for node, neighbors in graph.items():
    print(f"{node} -> {neighbors}")

# BFS Traversal
start = input("\nEnter the starting node: ")
try:
    start = int(start)
except ValueError:
    pass

if start not in graph:
    print("\nInvalid starting node!")
else:
    print(f"\nBreadth-First Search traversal starting from node {start}:")
    bfs(graph, start)
