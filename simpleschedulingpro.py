import random
import math
import matplotlib.pyplot as plt
import networkx as nx

# -------------------------------
# Problem setup
# -------------------------------

NUM_TASKS = 6
NUM_SLOTS = 3
SLOT_CAPACITY = 2  # each slot can handle 2 tasks at most

tasks = [f"Task{i+1}" for i in range(NUM_TASKS)]
slots = [f"Slot{j+1}" for j in range(NUM_SLOTS)]

# -------------------------------
# Cost function
# -------------------------------

def cost_function(schedule):
    """
    Penalizes slot overcapacity and unbalanced distribution.
    """
    slot_counts = {s: 0 for s in slots}
    for task, assigned_slot in schedule.items():
        slot_counts[assigned_slot] += 1

    # Penalty for exceeding capacity
    penalty = 0
    for slot, count in slot_counts.items():
        if count > SLOT_CAPACITY:
            penalty += (count - SLOT_CAPACITY) * 5  # heavy penalty

    # Encourage even distribution
    variance = sum((count - NUM_TASKS / NUM_SLOTS) ** 2 for count in slot_counts.values())
    return penalty + variance

# -------------------------------
# Generate random schedule
# -------------------------------

def random_schedule():
    return {task: random.choice(slots) for task in tasks}

# -------------------------------
# Get a neighbor solution
# -------------------------------

def neighbor(schedule):
    new_schedule = schedule.copy()
    # randomly reassign one task
    task_to_change = random.choice(tasks)
    new_slot = random.choice(slots)
    new_schedule[task_to_change] = new_slot
    return new_schedule

# -------------------------------
# Simulated Annealing algorithm
# -------------------------------

def simulated_annealing(initial_temp=100.0, cooling_rate=0.95, stop_temp=0.1, iterations_per_temp=100):
    current = random_schedule()
    current_cost = cost_function(current)
    best = current.copy()
    best_cost = current_cost
    temp = initial_temp
    history = []

    while temp > stop_temp:
        for _ in range(iterations_per_temp):
            new = neighbor(current)
            new_cost = cost_function(new)
            delta = new_cost - current_cost

            # Accept if better or with probability exp(-ΔE / T)
            if delta < 0 or random.random() < math.exp(-delta / temp):
                current, current_cost = new, new_cost
                if new_cost < best_cost:
                    best, best_cost = new.copy(), new_cost

            history.append(best_cost)

        temp *= cooling_rate  # cooling

    return best, best_cost, history

# -------------------------------
# Visualization
# -------------------------------

def visualize_schedule(schedule, title="Schedule Visualization"):
    G = nx.Graph()
    for task, slot in schedule.items():
        G.add_node(task, bipartite=0)
        G.add_node(slot, bipartite=1)
        G.add_edge(task, slot)

    plt.figure(figsize=(6, 4))
    # Properly merge task and slot positions
    pos = {**{t: (0, i) for i, t in enumerate(tasks)},
           **{s: (2, i) for i, s in enumerate(slots)}}
    nx.draw(G, pos, with_labels=True, node_size=1500, node_color="lightblue",
            font_weight="bold", width=1)
    plt.title(title)
    plt.show()

# -------------------------------
# Main program
# -------------------------------

def main():
    print("Simulated Annealing Task Scheduler\n")
    best_schedule, best_cost, history = simulated_annealing()

    print("✅ Best schedule found:")
    for t, s in best_schedule.items():
        print(f"  {t} → {s}")
    print(f"\nFinal Cost: {best_cost:.2f}")

    # Plot schedule
    visualize_schedule(best_schedule, title="Final Best Schedule")

    # Plot cost reduction over iterations
    plt.figure(figsize=(6, 4))
    plt.plot(history)
    plt.title("Cost Reduction Over Time")
    plt.xlabel("Iteration")
    plt.ylabel("Cost")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
