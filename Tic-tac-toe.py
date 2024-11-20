import math

# Constants for representing the players and empty cells
EMPTY = "-"
PLAYER_X = "X"
PLAYER_O = "O"

# The game board
board = [EMPTY, EMPTY, EMPTY,
         EMPTY, EMPTY, EMPTY,
         EMPTY, EMPTY, EMPTY]

# Function to print the game board
def print_board(board):
    print("---------")
    for i in range(3):
        print("|", board[i*3], "|", board[i*3 + 1], "|", board[i*3 + 2], "|")
        print("---------")

# Function to check if a player has won
def check_winner(board):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]  # diagonals
    ]

    for combination in winning_combinations:
        if board[combination[0]] == board[combination[1]] == board[combination[2]] != EMPTY:
            return board[combination[0]]

    if EMPTY not in board:
        return "tie"

    return None

# Function to evaluate the game board
def evaluate(board):
    winner = check_winner(board)

    if winner == PLAYER_X:
        return 1
    elif winner == PLAYER_O:
        return -1
    else:
        return 0

# Minimax function with alpha-beta pruning
def minimax(board, depth, alpha, beta, maximizing_player):
    if check_winner(board) is not None or depth == 0:
        return evaluate(board)

    if maximizing_player:
        max_eval = -math.inf
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = PLAYER_X
                eval_score = minimax(board, depth - 1, alpha, beta, False)
                board[i] = EMPTY
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = PLAYER_O
                eval_score = minimax(board, depth - 1, alpha, beta, True)
                board[i] = EMPTY
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
        return min_eval

# Function to find the best move using minimax with alpha-beta pruning
def find_best_move(board):
    best_score = -math.inf
    best_move = None

    for i in range(9):
        if board[i] == EMPTY:
            board[i] = PLAYER_X
            move_score = minimax(board, 9, -math.inf, math.inf, False)
            board[i] = EMPTY

            if move_score > best_score:
                best_score = move_score
                best_move = i

    return best_move

# Main game loop
while True:
    print_board(board)
    winner = check_winner(board)

    if winner is not None:
        if winner == "tie":
            print("It's a tie!")
        else:
            print("Player", winner, "wins!")
        break

    if len([cell for cell in board if cell != EMPTY]) % 2 == 0:
        # Player O's turn
        while True:
            move = int(input("Enter O's move (0-8): "))
            if board[move] == EMPTY:
                board[move] = PLAYER_O
                break
            else:
                print("Invalid move! Try again.")
    else:
        # Player X's turn
        move = find_best_move(board)
        board[move] = PLAYER_X