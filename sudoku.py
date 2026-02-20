import pygame
import sys

pygame.init()

# --- Window setup ---
WIDTH, HEIGHT = 540, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Game")

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 50, 200)
RED = (200, 0, 0)
GRAY = (180, 180, 180)

# --- Font ---
FONT = pygame.font.Font(None, 50)
SMALL_FONT = pygame.font.Font(None, 35)

# --- Grid setup ---
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE

# Example Sudoku puzzle (0 = empty)
board = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]

selected = None

def draw_board():
    WIN.fill(WHITE)

    # Draw grid lines
    for i in range(GRID_SIZE + 1):
        line_width = 4 if i % 3 == 0 else 1
        pygame.draw.line(WIN, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), line_width)
        pygame.draw.line(WIN, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WIDTH), line_width)

    # Draw numbers
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            num = board[row][col]
            if num != 0:
                text = FONT.render(str(num), True, BLUE)
                WIN.blit(text, (col * CELL_SIZE + 20, row * CELL_SIZE + 10))

    # Draw bottom instruction
    msg = SMALL_FONT.render("Press R to reset | Click cell & type 1–9", True, RED)
    WIN.blit(msg, (10, WIDTH + 10))

    # Highlight selected cell
    if selected:
        row, col = selected
        pygame.draw.rect(WIN, RED, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)

    pygame.display.update()

def is_valid(num, pos):
    # Check row
    for i in range(GRID_SIZE):
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(GRID_SIZE):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    # Check 3x3 box
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False

    return True

def mouse_to_cell(pos):
    if pos[1] < WIDTH:
        x, y = pos
        return y // CELL_SIZE, x // CELL_SIZE
    return None

def reset_board():
    global board
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

# --- Game Loop ---
running = True
while running:
    draw_board()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            selected = mouse_to_cell(event.pos)

        if event.type == pygame.KEYDOWN:
            if selected:
                row, col = selected
                if event.key == pygame.K_1: num = 1
                elif event.key == pygame.K_2: num = 2
                elif event.key == pygame.K_3: num = 3
                elif event.key == pygame.K_4: num = 4
                elif event.key == pygame.K_5: num = 5
                elif event.key == pygame.K_6: num = 6
                elif event.key == pygame.K_7: num = 7
                elif event.key == pygame.K_8: num = 8
                elif event.key == pygame.K_9: num = 9
                elif event.key == pygame.K_0: num = 0
                else:
                    num = None

                if num is not None:
                    if num == 0 or is_valid(num, (row, col)):
                        board[row][col] = num

            if event.key == pygame.K_r:
                reset_board()
