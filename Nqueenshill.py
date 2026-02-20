import random

def print_board(state):
    n = len(state)
    for row in range(n):
        line = ""
        for col in range(n):
            if state[col] == row:
                line += "Q "
            else:
                line += ". "
        print(line)
    print()

# Cost function: number of attacking pairs
def compute_cost(state):
    attacks = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                attacks += 1
    return attacks

# Generate all neighbors by moving one queen in its column
def get_neighbors(state):
    neighbors = []
    n = len(state)
    for col in range(n):
        for row in range(n):
            if row != state[col]:
                new_state = list(state)
                new_state[col] = row
                neighbors.append(new_state)
    return neighbors

# Hill Climbing Algorithm
def hill_climbing(n, max_restarts=10):
    best_overall = None
    best_cost = float("inf")

    for restart in range(max_restarts):
        current = [random.randint(0, n - 1) for _ in range(n)]
        current_cost = compute_cost(current)

        while True:
            neighbors = get_neighbors(current)
            neighbor_costs = [compute_cost(neighbor) for neighbor in neighbors]
            min_cost = min(neighbor_costs)
            if min_cost >= current_cost:  # Local optimum
                break
            best_neighbor = neighbors[neighbor_costs.index(min_cost)]
            current, current_cost = best_neighbor, min_cost

        # Track the best solution across restarts
        if current_cost < best_cost:
            best_cost = current_cost
            best_overall = current

        # If a valid solution is found
        if best_cost == 0:
            break

    print("Final Board:")
    print_board(best_overall)
    print("Final Cost:", best_cost)
    if best_cost == 0:
        print("✅ Solution Found!")
    else:
        print("⚠ Local Optimum Reached.")

# Run the algorithm
n = 8  # You can change N here
hill_climbing(n)