def expectiminimax(node, node_type, tree, probabilities=None):
    # Leaf node
    if isinstance(tree[node], int):
        return tree[node]
    # MAX node
    if node_type == 'max':
        return max(expectiminimax(child, tree['types'][child], tree, probabilities) for child in tree[node])
    # MIN node
    if node_type == 'min':
        return min(expectiminimax(child, tree['types'][child], tree, probabilities) for child in tree[node])
    # CHANCE node
    if node_type == 'chance':
        prob_list = probabilities[node]
        return sum(
            prob * expectiminimax(child, tree['types'][child], tree, probabilities)
            for child, prob in zip(tree[node], prob_list)
        )

# Example tree structure from the image:
# Root (MAX) --> Chance Node --> Leaf1, Leaf2
#                Hit Node    --> Leaf3, Leaf4

tree = {
    'Root': ['Chance', 'Hit'],
    'types': {'Root': 'max', 'Chance': 'chance', 'Hit': 'min', 'Leaf1': 'leaf', 'Leaf2': 'leaf', 'Leaf3': 'leaf', 'Leaf4': 'leaf'},
    'Chance': ['Leaf1', 'Leaf2'],
    'Hit': ['Leaf3', 'Leaf4'],
    'Leaf1': 5,
    'Leaf2': 12,
    'Leaf3': 15,
    'Leaf4': 8
}

# Probabilities for the chance node from the edge labels in the image
probabilities = {
    'Chance': [0.5, 0.5]  # Probability for Leaf1 and Leaf2
}

# Compute expected utility for both children of the root node
chance_utility = expectiminimax('Chance', tree['types']['Chance'], tree, probabilities)
hit_utility = expectiminimax('Hit', tree['types']['Hit'], tree, probabilities)

print(f"Expected utility of 'Chance' node: {chance_utility}")
print(f"Utility of 'Hit' node (MIN): {hit_utility}")

# Optimal decision at the root (MAX node)
if chance_utility > hit_utility:
    print("AI should choose the Chance node.")
else:
    print("AI should choose the Hit node.")

print("Randomness affects the choice because the Chance node utility is an average, not a fixed value.")
