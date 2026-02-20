import random

# ---------------- Parameters ----------------
NUM_CITIES = 5
NUM_ANTS = 10
ALPHA = 1.0        # pheromone influence
BETA = 5.0         # distance influence
EVAPORATION = 0.5  # pheromone evaporation rate
Q = 100            # pheromone deposit factor
ITERATIONS = 50

# ---------------- Distance Matrix ----------------
distance_matrix = [
    [0, 2, 9, 10, 7],
    [1, 0, 6, 4, 3],
    [15, 7, 0, 8, 3],
    [6, 3, 12, 0, 11],
    [9, 7, 5, 6, 0]
]

# ---------------- Initialization ----------------
num_cities = len(distance_matrix)
pheromone = [[1 for _ in range(num_cities)] for _ in range(num_cities)]

# Function to compute total tour length
def tour_length(tour):
    length = 0
    for i in range(len(tour) - 1):
        length += distance_matrix[tour[i]][tour[i + 1]]
    length += distance_matrix[tour[-1]][tour[0]]  # return to start
    return length

# Choose next city based on probability
def select_next_city(current_city, unvisited):
    total = 0.0
    probabilities = []
    for city in unvisited:
        pher = pheromone[current_city][city] ** ALPHA
        visibility = (1.0 / (distance_matrix[current_city][city] + 1e-10)) ** BETA
        score = pher * visibility
        probabilities.append((city, score))
        total += score

    # Normalize probabilities
    if total == 0:
        return random.choice(list(unvisited))
    probabilities = [(city, score / total) for city, score in probabilities]

    # Roulette wheel selection
    r = random.random()
    cumulative = 0.0
    for city, prob in probabilities:
        cumulative += prob
        if r <= cumulative:
            return city
    return probabilities[-1][0]

# ---------------- Ant Colony Optimization ----------------
def ant_colony_optimization():
    global pheromone
    best_tour = None
    best_length = float('inf')

    for iteration in range(ITERATIONS):
        all_tours = []

        for _ in range(NUM_ANTS):
            start = random.randint(0, num_cities - 1)
            tour = [start]
            unvisited = set(range(num_cities)) - {start}

            while unvisited:
                current_city = tour[-1]
                next_city = select_next_city(current_city, unvisited)
                tour.append(next_city)
                unvisited.remove(next_city)

            all_tours.append(tour)

        # Find best tour of this iteration
        for tour in all_tours:
            length = tour_length(tour)
            if length < best_length:
                best_length = length
                best_tour = tour

        # Evaporate pheromone
        for i in range(num_cities):
            for j in range(num_cities):
                pheromone[i][j] *= (1 - EVAPORATION)

        # Deposit pheromone
        for tour in all_tours:
            length = tour_length(tour)
            deposit = Q / length
            for i in range(len(tour) - 1):
                a, b = tour[i], tour[i + 1]
                pheromone[a][b] += deposit
                pheromone[b][a] += deposit
            a, b = tour[-1], tour[0]
            pheromone[a][b] += deposit
            pheromone[b][a] += deposit

        print(f"Iteration {iteration+1:02d} | Best Length So Far = {best_length}")

    return best_tour, best_length


# ---------------- Main ----------------
if __name__ == "__main__":
    best_path, best_cost = ant_colony_optimization()
    print("\nOptimal / Best Path Found:")
    print(" -> ".join(str(city) for city in best_path) + f" -> {best_path[0]}")
    print(f"Total Cost: {best_cost}")