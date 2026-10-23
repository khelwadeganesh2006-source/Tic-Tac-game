
import tkinter as tk
from tkinter import messagebox

# -------------------- GAME SETTINGS --------------------


HUMAN = "X"
AI = "O"
EMPTY = ""

BG_COLOR = "#101827"
CARD_COLOR = "#1E293B"
CELL_COLOR = "#334155"
X_COLOR = "#38BDF8"
O_COLOR = "#FBBF24"
TEXT_COLOR = "#F8FAFC"

board = [EMPTY] * 9
game_over = False
ai_thinking = False
ai_job = None


# -------------------- GAME LOGIC --------------------

def get_winner(state):
    winning_lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]

    for a, b, c in winning_lines:
        if state[a] and state[a] == state[b] == state[c]:
            return state[a]

    if EMPTY not in state:
        return "Draw"

    return None


def minimax(state, depth, is_maximizing, alpha, beta):
    result = get_winner(state)

    if result == AI:
        return 10 - depth

    if result == HUMAN:
        return depth - 10

    if result == "Draw":
        return 0

    if is_maximizing:
        best_score = float("-inf")

        for i in range(9):
            if state[i] == EMPTY:
                state[i] = AI
                score = minimax(
                    state, depth + 1, False, alpha, beta
                )
                state[i] = EMPTY

                best_score = max(best_score, score)
                alpha = max(alpha, best_score)

                if beta <= alpha:
                    break

        return best_score

    else:
        best_score = float("inf")

        for i in range(9):
            if state[i] == EMPTY:
                state[i] = HUMAN
                score = minimax(
                    state, depth + 1, True, alpha, beta
                )
                state[i] = EMPTY

                best_score = min(best_score, score)
                beta = min(beta, best_score)

                if beta <= alpha:
                    break

        return best_score


def find_best_move():
    best_score = float("-inf")
    best_move = None


    for i in range(9):
        if board[i] == EMPTY:
            board[i] = AI

            score = minimax(
                board, 0, False,
                float("-inf"), float("inf")
            )

            board[i] = EMPTY

            if score > best_score:
                best_score = score
                best_move = i

    return best_move


# -------------------- USER INTERFACE --------------------

root = tk.Tk()
root.title("Tic-Tac-Toe AI")
root.geometry("430x570")
root.resizable(False, False)
root.configure(bg=BG_COLOR)

title = tk.Label(
    root,
    text="TIC-TAC-TOE AI",
    font=("Arial", 23, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
title.pack(pady=(22, 5))

subtitle = tk.Label(
    root,
    text="Human (X)  vs  AI (O)",
    font=("Arial", 12),
    bg=BG_COLOR,
    fg="#CBD5E1"
)
subtitle.pack(pady=3)

status_label = tk.Label(
    root,
    text="Your turn! Select a square.",
    font=("Arial", 12, "bold"),
    bg=BG_COLOR,
    fg=X_COLOR
)
status_label.pack(pady=14)

board_frame = tk.Frame(root, bg=CARD_COLOR, padx=8, pady=8)
board_frame.pack(pady=5)

buttons = []

def update_board():
    for i, button in enumerate(buttons):
        button.config(
            text=board[i],
            fg=(
                X_COLOR if board[i] == HUMAN
                else O_COLOR if board[i] == AI
                else TEXT_COLOR
            ),
            bg=CELL_COLOR if board[i] == EMPTY else CARD_COLOR,
            state=(
                "normal"
                if board[i] == EMPTY
                and not game_over
                and not ai_thinking
                else "disabled"
            )
        )


def finish_game(result):
    global game_over

    game_over = True

    if result == HUMAN:
        status_label.config(
            text="Congratulations! You Win!",
            fg="#4ADE80"
        )
        messagebox.showinfo("Game Over", "You won! Great job!")

    elif result == AI:
        status_label.config(
            text="AI Wins! Better luck next time.",
            fg=O_COLOR
        )
        messagebox.showinfo(
            "Game Over",
            "AI wins! Try again."
        )

    else:
        status_label.config(
            text="It's a Draw!",
            fg=TEXT_COLOR
        )
        messagebox.showinfo(
            "Game Over",
            "It's a draw! Well played."
        )

    update_board()


def check_game():
    result = get_winner(board)

    if result is not None:
        finish_game(result)
        return True

    return False


def ai_move():
    global ai_thinking, ai_job

    ai_job = None

    if game_over:
        ai_thinking = False
        return

    move = find_best_move()

    if move is not None:
        board[move] = AI

    ai_thinking = False
    update_board()

    if not check_game():
        status_label.config(
            text="Your turn! Select a square.",
            fg=X_COLOR
        )
        update_board()


def on_cell_click(index):
    global ai_thinking, ai_job

    if game_over or ai_thinking or board[index] != EMPTY:
        return

    # Human player makes a move
    board[index] = HUMAN
    update_board()

    if check_game():
        return

    # AI calculates its next move
    ai_thinking = True
    status_label.config(
        text="AI is thinking...",
        fg=O_COLOR
    )
    update_board()

    ai_job = root.after(250, ai_move)


for i in range(9):
    button = tk.Button(
        board_frame,
        text="",
        font=("Arial", 28, "bold"),
        width=4,
        height=2,
        bg=CELL_COLOR,
        fg=TEXT_COLOR,
        activebackground="#475569",
        relief="flat",
        cursor="hand2",
        command=lambda index=i: on_cell_click(index)
    )

    button.grid(
        row=i // 3,
        column=i % 3,
        padx=5,
        pady=5
    )

    buttons.append(button)


# -------------------- RESET GAME --------------------

def reset_game():
    global board, game_over, ai_thinking, ai_job

    if ai_job is not None:
        root.after_cancel(ai_job)
        ai_job = None

    board = [EMPTY] * 9
    game_over = False
    ai_thinking = False

    status_label.config(
        text="Your turn! Select a square.",
        fg=X_COLOR
    )

    update_board()


reset_button = tk.Button(
    root,
    text="New Game",
    font=("Arial", 12, "bold"),
    bg="#2563EB",
    fg="white",
    activebackground="#1D4ED8",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    padx=30,
    pady=10,
    command=reset_game
)
reset_button.pack(pady=20)

footer = tk.Label(
    root,
    text="Powered by Minimax + Alpha-Beta Pruning",
    font=("Arial", 9),
    bg=BG_COLOR,
    fg="#94A3B8"
)
footer.pack(side="bottom", pady=12)

update_board()
root.mainloop()
