N = 8  # Chessboard size (8x8)

def print_solution(board):
    """Display the chessboard with queens placed safely."""
    for row in board:
        print(" ".join("Q" if x == 1 else "." for x in row))
    print("\n")

def is_safe(board, row, col):
    """Check if a queen can be safely placed at board[row][col]."""

    # Check this column on upper rows
    for i in range(row):
        if board[i][col] == 1:
            return False

    # Check upper left diagonal
    for i, j in zip(range(row-1, -1, -1), range(col-1, -1, -1)):
        if board[i][j] == 1:
            return False

    # Check upper right diagonal
    for i, j in zip(range(row-1, -1, -1), range(col+1, N)):
        if board[i][j] == 1:
            return False

    return True

def solve_nqueens(board, row):
    """Use backtracking to solve the N Queens problem."""
    # Base case: If all queens are placed
    if row >= N:
        print_solution(board)
        return True

    success = False
    for col in range(N):
        if is_safe(board, row, col):
            board[row][col] = 1  # Place the queen
            success = solve_nqueens(board, row + 1) or success
            board[row][col] = 0  # Backtrack (remove the queen)

    return success

def solve():
    """Initialize board and trigger solver."""
    board = [[0] * N for _ in range(N)]
    if not solve_nqueens(board, 0):
        print("No solution exists.")
    else:
        print("All possible solutions found.")
solve()