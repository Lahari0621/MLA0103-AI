# Knight's Tour using Backtracking

N = 8  # size of chessboard (8x8)

def print_solution(board):
    for row in board:
        print(' '.join(str(cell).rjust(2, ' ') for cell in row))
    print()

# Check if (x, y) is a valid move
def is_safe(x, y, board):
    return 0 <= x < N and 0 <= y < N and board[x][y] == -1

# Recursive utility to solve Knight's Tour
def solve_knight_tour(x, y, movei, board, x_move, y_move):
    # Base case: if all squares are visited
    if movei == N * N:
        return True

    # Try all possible moves from current coordinate (x, y)
    for k in range(8):
        next_x = x + x_move[k]
        next_y = y + y_move[k]
        if is_safe(next_x, next_y, board):
            board[next_x][next_y] = movei
            if solve_knight_tour(next_x, next_y, movei + 1, board, x_move, y_move):
                return True
            # Backtrack
            board[next_x][next_y] = -1
    return False

def knight_tour():
    # Initialize board
    board = [[-1 for _ in range(N)] for _ in range(N)]

    # Moves for the knight
    x_move = [2, 1, -1, -2, -2, -1, 1, 2]
    y_move = [1, 2, 2, 1, -1, -2, -2, -1]

    # Start position
    board[0][0] = 0

    # Start solving from (0, 0)
    if not solve_knight_tour(0, 0, 1, board, x_move, y_move):
        print("No solution exists.")
    else:
        print("Knight's Tour Solution Path:")
        print_solution(board)

# Run the program
knight_tour()