from queue import Queue
import heapq

# ----------- Graph Representation -----------
graph = {
    'A': {'B': 2, 'C': 4},
    'B': {'D': 7, 'E': 3},
    'C': {'F': 4, 'G': 5},
    'D': {'H': 1},
    'E': {'H': 6},
    'F': {'G': 2, 'H': 5},
    'G': {'H': 3},
    'H': {}
}

# ----------- Heuristic Function -----------
# (Straight-line distance or estimated cost to goal)
heuristic = {
    'A': 10,
    'B': 8,
    'C': 7,
    'D': 4,
    'E': 5,
    'F': 3,
    'G': 2,
    'H': 0
}

# ----------- Beam Search Implementation -----------
def beam_search(start, goal, beam_width):
    print(f"\n--- Beam Search (Beam width = {beam_width}) ---")
    beam = [(heuristic[start], [start])]
    level = 0

    while beam:
        print(f"\nLevel {level}: Candidates -> {[path[-1] for (_, path) in beam]}")
        new_beam = []
        for _, path in beam:
            node = path[-1]
            if node == goal:
                print("Goal reached!")
                return path
            for neighbor, cost in graph[node].items():
                new_path = path + [neighbor]
                score = heuristic[neighbor]
                heapq.heappush(new_beam, (score, new_path))
        
        # Keep only k best nodes
        beam = heapq.nsmallest(beam_width, new_beam)
        level += 1

    print("Goal not found (beam too narrow).")
    return None

# ----------- Breadth-First Search (for comparison) -----------
def bfs(start, goal):
    print("\n--- Breadth-First Search ---")
    visited = set()
    queue = Queue()
    queue.put([start])

    while not queue.empty():
        path = queue.get()
        node = path[-1]

        if node == goal:
            return path

        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                new_path = path + [neighbor]
                queue.put(new_path)

    return None

# ----------- Main Function -----------
if __name__ == "__main__":
    start = 'A'
    goal = 'H'
    beam_width = 2  # you can change this to 1, 2, 3, etc.

    beam_result = beam_search(start, goal, beam_width)
    bfs_result = bfs(start, goal)

    print("\nBeam Search Path:", beam_result)
    print("BFS Path:", bfs_result)

    # ----------- Efficiency vs Completeness Discussion -----------
    print("\n--- Comparison ---")
    print("Beam Search:")
    print("- Faster, memory-efficient, but may miss optimal path if beam width is too small.")
    print("BFS:")
    print("- Guarantees the shortest path but explores all nodes (less efficient).")