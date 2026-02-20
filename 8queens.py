import pygame
import sys

pygame.init()

# --- Constants ---
WIDTH, HEIGHT = 480, 480
CELL_SIZE = WIDTH // 8
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8-Queens Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)

font = pygame.font.Font(None, 40)

# --- Game Variables ---
board = [[0 for _ in range(8)] for _ in range(8)]  # 0 = empty, 1 = queen
selected = None

# --- Helper Functions ---
def draw_board():
    WIN.fill(WHITE)
    for row in range(8):
        for col in range(8):
            rect = pygame.Rect(col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(WIN, color, rect)
            if board[row][col] == 1:
                text = font.render("Q", True, RED)
                WIN.blit(text, (col*CELL_SIZE + 15, row*CELL_SIZE + 10))

def is_safe(row, col):
    # Check column
    for i in range(row):
        if board[i][col] == 1:
            return False
    # Check diagonal /
    i, j = row-1, col-1
    while i >= 0 and j >= 0:
        if board[i][j] == 1:
            return False
        i -= 1
        j -= 1
    # Check diagonal \
    i, j = row-1, col+1
    while i >= 0 and j < 8:
        if board[i][j] == 1:
            return False
        i -= 1
        j += 1
    return True

def count_queens():
    return sum(sum(row) for row in board)

# --- Main Loop ---
while True:
    draw_board()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Place or remove queen with mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            row, col = y // CELL_SIZE, x // CELL_SIZE
            if board[row][col] == 0:
                if is_safe(row, col):
                    board[row][col] = 1
            else:
                board[row][col] = 0

        # Reset board
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                board = [[0 for _ in range(8)] for _ in range(8)]
