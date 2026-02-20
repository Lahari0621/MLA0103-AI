initial_state = {
    'monkey': 'A',
    'box': 'B',
    'monkey_on_box': False,
    'has_banana': False
}

goal_state = {
    'has_banana': True
}

banana_position = 'C'  # Bananas are hanging at position C

def display_state(state):
    print(f"Monkey at: {state['monkey']}, Box at: {state['box']}, "
          f"On Box: {state['monkey_on_box']}, Has Banana: {state['has_banana']}")

def move(state, position):
    state['monkey'] = position
    print(f"Monkey moves to {position}")
    return state

def push_box(state, position):
    if state['monkey'] == state['box']:
        state['monkey'] = position
        state['box'] = position
        print(f"Monkey pushes the box to {position}")
    else:
        print("Monkey needs to be at the box to push it!")
    return state

def climb_box(state):
    if state['monkey'] == state['box']:
        state['monkey_on_box'] = True
        print("Monkey climbs on the box")
    else:
        print("Monkey must be at the box to climb it!")
    return state

def grab_banana(state):
    if state['monkey_on_box'] and state['box'] == banana_position:
        state['has_banana'] = True
        print("Monkey grabs the banana! 🍌")
    else:
        print("Monkey cannot reach the banana yet.")
    return state

# --- Simulation ---
print("Initial State:")
display_state(initial_state)
print("\nActions:")

# Step 1: Move to the box
move(initial_state, 'B')

# Step 2: Push box to bananas
push_box(initial_state, 'C')

# Step 3: Climb onto the box
climb_box(initial_state)

# Step 4: Grab the bananas
grab_banana(initial_state)

# --- Final State ---
print("\nFinal State:")
display_state(initial_state)

if initial_state['has_banana']:
    print("\n✅ Goal achieved! Monkey got the bananas!")
else:
    print("\n❌ Goal not achieved.")