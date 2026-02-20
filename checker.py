import math
import copy

EMPTY = '.'
PLAYER_PIECE = 'P'
AI_PIECE = 'A'
BOARD_SIZE = 8

def create_board():
    board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    for row in range(3):
        for col in range(BOARD_SIZE):
            if (row + col) % 2 == 1:
                board[row][col] = AI_PIECE
    for row in range(5, 8):
        for col in range(BOARD_SIZE):
            if (row + col) % 2 == 1:
                board[row][col] = PLAYER_PIECE
    return board

def print_board(board):
    print("  " + " ".join(map(str, range(BOARD_SIZE))))
    for i in range(BOARD_SIZE):
        print(i, " ".join(board[i]))
    print()

def get_all_moves(board, piece):
    moves = []
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == piece:
                moves.extend(get_valid_moves(board, r, c, piece))
    return moves

def get_valid_moves(board, r, c, piece):
    moves = []
    directions = [(-1, -1), (-1, 1)] if piece == PLAYER_PIECE else [(1, -1), (1, 1)]
    for dr, dc in directions:
        new_r, new_c = r + dr, c + dc
        if 0 <= new_r < BOARD_SIZE and 0 <= new_c < BOARD_SIZE:
            if board[new_r][new_c] == EMPTY:
                moves.append(((r, c), (new_r, new_c)))
            elif board[new_r][new_c] != piece:
                jump_r, jump_c = new_r + dr, new_c + dc
                if 0 <= jump_r < BOARD_SIZE and 0 <= jump_c < BOARD_SIZE and board[jump_r][jump_c] == EMPTY:
                    moves.append(((r, c), (jump_r, jump_c)))
    return moves

def make_move(board, move):
    new_board = copy.deepcopy(board)
    (r1, c1), (r2, c2) = move
    piece = new_board[r1][c1]
    new_board[r1][c1] = EMPTY
    new_board[r2][c2] = piece

    if abs(r2 - r1) == 2:
        jumped_r = (r1 + r2) // 2
        jumped_c = (c1 + c2) // 2
        new_board[jumped_r][jumped_c] = EMPTY
    return new_board

def evaluate(board):
    player_score = sum(row.count(PLAYER_PIECE) for row in board)
    ai_score = sum(row.count(AI_PIECE) for row in board)
    return ai_score - player_score

def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or is_game_over(board):
        return evaluate(board), board

    if maximizing_player:
        max_eval = -math.inf
        best_move = None
        for move in get_all_moves(board, AI_PIECE):
            eval_val, _ = minimax(make_move(board, move), depth - 1, alpha, beta, False)
            if eval_val > max_eval:
                max_eval = eval_val
                best_move = move
            alpha = max(alpha, eval_val)
            if beta <= alpha:
                break
        return max_eval, make_move(board, best_move) if best_move else board

    else:
        min_eval = math.inf
        best_move = None
        for move in get_all_moves(board, PLAYER_PIECE):
            eval_val, _ = minimax(make_move(board, move), depth - 1, alpha, beta, True)
            if eval_val < min_eval:
                min_eval = eval_val
                best_move = move
            beta = min(beta, eval_val)
            if beta <= alpha:
                break
        return min_eval, make_move(board, best_move) if best_move else board

def is_game_over(board):
    return not get_all_moves(board, PLAYER_PIECE) or not get_all_moves(board, AI_PIECE)

def get_winner(board):
    player_pieces = sum(row.count(PLAYER_PIECE) for row in board)
    ai_pieces = sum(row.count(AI_PIECE) for row in board)
    if player_pieces > ai_pieces:
        return "Human Wins!"
    elif ai_pieces > player_pieces:
        return "AI Wins!"
    else:
        return "Draw!"

def play_game():
    board = create_board()
    print("Welcome to Checkers AI!")
    mode = input("Choose mode: 1) Human vs AI  2) AI vs AI : ")

    print_board(board)
    turn = 'PLAYER'

    while not is_game_over(board):
        if turn == 'PLAYER':
            if mode == '1':
                moves = get_all_moves(board, PLAYER_PIECE)
                if not moves:
                    break
                print("Your available moves:")
                for i, move in enumerate(moves):
                    print(f"{i}: {move}")
                choice = int(input("Choose your move: "))
                board = make_move(board, moves[choice])
            else:
                _, board = minimax(board, 3, -math.inf, math.inf, False)
            turn = 'AI'

        else:
            print("AI is thinking...")
            _, board = minimax(board, 3, -math.inf, math.inf, True)
            turn = 'PLAYER'

        print_board(board)

    print("Game Over! " + get_winner(board))

if __name__ == "__main__":
    play_game()
