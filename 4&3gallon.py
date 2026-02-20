from collections import deque
def water_jug_problem():
    jugA, jugB = 4, 3
    visited = set()
    queue = deque([(0, 0, [])])

    while queue:
        a, b, path = queue.popleft()
        if (a, b) in visited:
            continue
        visited.add((a, b))
        path = path + [(a, b)]
        if a == 2:
            print("Steps to get exactly 2 gallons in the 4-gallon jug:\n")
            for step in path:
                print(f"Jug A: {step[0]} gallons, Jug B: {step[1]} gallons")
            return

        next_states = []
        next_states.append((jugA, b))
        next_states.append((a, jugB))
        next_states.append((0, b))
        next_states.append((a, 0))
        pour = min(a, jugB - b)\
        next_states.append((a - pour, b + pour))
        pour = min(b, jugA - a)
        next_states.append((a + pour, b - pour))

        # Add next states to queue
        for state in next_states:
            if state not in visited:
                queue.append((state[0], state[1], path))

    print("No solution found.")

water_jug_problem()
