import numpy as np
import random

# Define grid world parameters
rows, cols = 5, 5
obstacles = [(1, 1), (2, 3), (3, 2)]
start = (0, 0)
goal = (4, 4)
actions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
action_names = ['R', 'D', 'L', 'U']
step_penalty = -1
obstacle_penalty = -10
goal_reward = 20

# Hyperparams
alpha = 0.1          # Learning rate
gamma = 0.9          # Discount factor
epsilon = 0.2        # Exploration rate
episodes = 500       # Training episodes

# Initialize Q-table
Q = np.zeros((rows, cols, len(actions)))

def valid_state(state):
    r, c = state
    if 0 <= r < rows and 0 <= c < cols and state not in obstacles:
        return True
    return False

def get_next_state(current, action):
    next_r, next_c = current[0] + action[0], current[1] + action[1]
    next_state = (next_r, next_c)
    if not valid_state(next_state):
        return current  # Invalid move, stay in place
    return next_state

# Training loop
for episode in range(episodes):
    state = start
    while state != goal:
        r, c = state
        # Explore vs exploit
        if random.uniform(0, 1) < epsilon:
            a = random.randint(0, 3)
        else:
            a = np.argmax(Q[r, c])

        action = actions[a]
        next_state = get_next_state(state, action)
        nr, nc = next_state

        # Rewards
        if next_state == goal:
            reward = goal_reward
        elif next_state in obstacles:
            reward = obstacle_penalty
        else:
            reward = step_penalty

        # Q-Learning update
        Q[r, c, a] += alpha * (reward + gamma * np.max(Q[nr, nc]) - Q[r, c, a])

        state = next_state

# Print Q-table
print("Learned Q-table (shape:", Q.shape, "):")
print(Q)

# Find optimal path from start to goal
state = start
path = [state]
while state != goal:
    r, c = state
    a = np.argmax(Q[r, c])
    next_state = get_next_state(state, actions[a])
    if next_state == state or next_state in path:
        # Trapped or loop detected
        break
    path.append(next_state)
    state = next_state

print("Optimal path from start to goal:")
print(path)
