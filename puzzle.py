import heapq

# Goal state
GOAL_STATE = ((1, 2, 3),
              (4, 5, 6),
              (7, 8, 0))

# Possible moves: Up, Down, Left, Right
MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Manhattan distance heuristic
def manhattan_distance(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:
                target_x = (value - 1) // 3
                target_y = (value - 1) % 3
                distance += abs(target_x - i) + abs(target_y - j)
    return distance

# Generate neighbors
def get_neighbors(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                x, y = i, j
    neighbors = []
    for dx, dy in MOVES:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [list(row) for row in state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append(tuple(tuple(row) for row in new_state))
    return neighbors

# Solve puzzle using A* search
def solve_puzzle(start_state):
    start = tuple(tuple(row) for row in start_state)
    pq = [(manhattan_distance(start), 0, start)]
    visited = set()

    while pq:
        _, cost, state = heapq.heappop(pq)
        if state in visited:
            continue
        visited.add(state)
        if state == GOAL_STATE:
            return state
        for neighbor in get_neighbors(state):
            heapq.heappush(pq, (cost + 1 + manhattan_distance(neighbor), cost + 1, neighbor))
    return None

# Print the puzzle state
def print_state(state):
    for row in state:
        print(' '.join(str(x) if x != 0 else '_' for x in row))
    print()

# Take input from user
print("Enter the initial 8-puzzle state (0 for empty tile) row by row, numbers separated by spaces:")
start_state = [list(map(int, input(f"Row {i+1}: ").split())) for i in range(3)]

print("\nInitial State:")
print_state(start_state)

final_state = solve_puzzle(start_state)
if final_state:
    print("Final Solved State:")
    print_state(final_state)
else:
    print("No solution found.")
