# Sudoku Solver using Backtracking and Constraint Checking

N = 9  # Sudoku grid size (9x9)

# Function to print the Sudoku grid
def print_grid(grid):
    for i in range(N):
        for j in range(N):
            print(grid[i][j], end=" ")
        print()

# Check if placing num at grid[row][col] is valid
def is_safe(grid, row, col, num):
    # Row constraint
    if num in grid[row]:
        return False

    # Column constraint
    for i in range(N):
        if grid[i][col] == num:
            return False

    # 3x3 Subgrid constraint
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[start_row + i][start_col + j] == num:
                return False

    return True

# Find the next empty cell (returns tuple of row, col)
def find_empty_location(grid):
    for i in range(N):
        for j in range(N):
            if grid[i][j] == 0:
                return (i, j)
    return None

# Backtracking function to solve Sudoku
def solve_sudoku(grid):
    empty = find_empty_location(grid)
    if not empty:
        return True  # Puzzle solved

    row, col = empty

    for num in range(1, 10):  # Try numbers 1–9
        if is_safe(grid, row, col, num):
            grid[row][col] = num  # Assign value

            if solve_sudoku(grid):  # Recursive step
                return True

            # Backtrack
            grid[row][col] = 0

    return False

# -------- Main Program --------
if __name__ == "__main__":
    # Example Sudoku puzzle (0 = empty)
    sudoku_grid = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    print("Original Sudoku Puzzle:")
    print_grid(sudoku_grid)
    print("\nSolving...\n")

    if solve_sudoku(sudoku_grid):
        print("Solved Sudoku Grid:")
        print_grid(sudoku_grid)
    else:
        print("No solution exists.")