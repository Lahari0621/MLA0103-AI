# Minimax Algorithm Example

def minimax(depth, node_index, is_maximizing, values):
    """
    Recursive function to apply the minimax algorithm.

    depth: current depth in the game tree
    node_index: index of the current node
    is_maximizing: True if it's the maximizing player's turn, False for minimizing player
    values: list of leaf node values
    """
    # Base case: if we reach a leaf node
    if depth == 2:
        return values[node_index]
    
    # If it's the maximizing player's turn
    if is_maximizing:
        return max(
            minimax(depth + 1, node_index * 2, False, values),
            minimax(depth + 1, node_index * 2 + 1, False, values)
        )
    # If it's the minimizing player's turn
    else:
        return min(
            minimax(depth + 1, node_index * 2, True, values),
            minimax(depth + 1, node_index * 2 + 1, True, values)
        )

# ----------------------------------------------------------
# Leaf nodes (final states)
values = [3, 5, 2, 9]

# Depth of tree = 2 (Root -> Min -> Leaf)
optimal_value = minimax(0, 0, True, values)
print("The optimal value for the maximizing player is:", optimal_value)

# ----------------------------------------------------------
# Determine which move (L or R) the maximizing player should take
left_subtree = min(values[0], values[1])  # Min node under Left
right_subtree = min(values[2], values[3]) # Min node under Right

best_move = "Left" if max(left_subtree, right_subtree) == left_subtree else "Right"
print("The maximizing player should choose:", best_move)
