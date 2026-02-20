def ab(node, alpha, beta, is_max, tree):
    if node not in tree: 
        return node
    if is_max:
        val = float('-inf')
        for c in tree[node]:
            val = max(val, ab(c, alpha, beta, False, tree))
            alpha = max(alpha, val)
            if beta <= alpha: break
        return val
    else:
        val = float('inf')
        for c in tree[node]:
            val = min(val, ab(c, alpha, beta, True, tree))
            beta = min(beta, val)
            if beta <= alpha: break
        return val

tree = {
    'A': ['B','C'],
    'B': ['D','E'],
    'C': ['F','G'],
    'D': [2,3],
    'E': [5,9],
    'F': [0,1],
    'G': [7,5]
}

print("Optimal value:", ab('A', float('-inf'), float('inf'), True, tree))
