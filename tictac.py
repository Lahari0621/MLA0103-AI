import pygame
import sys
import math

pygame.init()

# --- Constants ---
WIDTH, HEIGHT = 300, 350  # Extra height for messages
CELL_SIZE = WIDTH // 3
LINE_WIDTH = 5
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe Player vs AI")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)

# --- Game Variables ---
board = [["" for _ in range(3)] for _ in range(3)]
player = "X"  # Human
ai = "O"      # AI
current_player = player
game_over = False
winner = None

# --- Functions ---
def draw_board():
    WIN.fill(WHITE)
    # Draw grid
    for i in range(1, 3):
        pygame.draw.line(WIN, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), LINE_WIDTH)
        pygame.draw.line(WIN, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WIDTH), LINE_WIDTH)

    # Draw X and O
    font = pygame.font.Font(None, 100)
    for row in range(3):
        for col in range(3):
            if board[row][col] != "":
                text = font.render(board[row][col], True, BLACK)
                WIN.blit(text, (col * CELL_SIZE + 30, row * CELL_SIZE + 10))

def show_message(message):
    font = pygame.font.Font(None, 35)
    text = font.render(message, True, RED)
    WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, WIDTH + 10))

def check_winner(player_symbol):
    # Rows and columns
    for i in range(3):
        if all(board[i][j] == player_symbol for j in range(3)):
            return True
        if all(board[j][i] == player_symbol for j in range(3)):
            return True
    # Diagonals
    if all(board[i][i] == player_symbol for i in range(3)):
        return True
    if all(board[i][2 - i] == player_symbol for i in range(3)):
        return True
    return False

def check_winner_state(board_state, player_symbol):
    # Same as check_winner but for a given board (used in minimax)
    for i in range(3):
        if all(board_state[i][j] == player_symbol for j in range(3)):
            return True
        if all(board_state[j][i] == player_symbol for j in range(3)):
            return True
    if all(board_state[i][i] == player_symbol for i in range(3)):
        return True
    if all(board_state[i][2 - i] == player_symbol for i in range(3)):
        return True
    return False

def is_full():
    return all(all(cell != "" for cell in row) for row in board)

def minimax(board_state, depth, is_maximizing):
    if check_winner_state(board_state, ai):
        return 1
    if check_winner_state(board_state, player):
        return -1
    if all(all(cell != "" for cell in row) for row in board_state):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board_state[i][j] == "":
                    board_state[i][j] = ai
                    score = minimax(board_state, depth + 1, False)
                    board_state[i][j] = ""
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board_state[i][j] == "":
                    board_state[i][j] = player
                    score = minimax(board_state, depth + 1, True)
                    board_state[i][j] = ""
                    best_score = min(score, best_score)
        return best_score

def ai_move():
    best_score = -math.inf
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                board[i][j] = ai
                score = minimax(board, 0, False)
                board[i][j] = ""
                if score > best_score:
                    best_score = score
                    move = (i, j)
    if move:
        board[move[0]][move[1]] = ai

def restart_game():
    global board, current_player, game_over, winner
    board = [["" for _ in range(3)] for _ in range(3)]
    current_player = player
    game_over = False
    winner = None

# --- Main Loop ---
while True:
    draw_board()
    if game_over:
        if winner:
            show_message(f"{winner} wins! Press R to restart")
        else:
            show_message("It's a draw! Press R to restart")

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not game_over:
            if current_player == player:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if y < WIDTH:  # Click only inside board
                        row, col = y // CELL_SIZE, x // CELL_SIZE
                        if board[row][col] == "":
                            board[row][col] = player
                            if check_winner(player):
                                winner = "Player"
                                game_over = True
                            elif is_full():
                                game_over = True
                            else:
                                current_player = ai
            else:  # AI turn
                pygame.time.delay(300)
                ai_move()
                if check_winner(ai):
                    winner = "AI"
                    game_over = True
                elif is_full():
                    game_over = True
                else:
                    current_player = player
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                restart_game()
