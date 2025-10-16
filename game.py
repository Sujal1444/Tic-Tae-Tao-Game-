import tkinter as tk
from tkinter import messagebox

# Board: 3x3 list
board = [""] * 9

# Winning positions
wins = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)]

# Add an AI delay (milliseconds) and a flag to prevent clicks during AI turn
ai_delay_ms = 500
ai_thinking = False

def check_winner(b):
    for (i, j, k) in wins:
        if b[i] and b[i] == b[j] == b[k]:
            return b[i]
    if "" not in b: return "Draw"
    return None


def minimax(b, is_maximizing):
    result = check_winner(b)
    if result == "X": return -1
    if result == "O": return 1
    if result == "Draw": return 0

    if is_maximizing:  # AI 'O'
        best = -999
        for i in range(9):
            if b[i] == "":
                b[i] = "O"
                score = minimax(b, False)
                b[i] = ""
                best = max(best, score)
        return best
    else:  # Human 'X'
        best = 999
        for i in range(9):
            if b[i] == "":
                b[i] = "X"
                score = minimax(b, True)
                b[i] = ""
                best = min(best, score)
        return best


def best_move():
    best_score = -999
    move = None
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            score = minimax(board, False)
            board[i] = ""
            if score > best_score:
                best_score = score
                move = i
    return move

def click(i):
    global ai_thinking
    if ai_thinking:
        return
    if board[i] == "" and check_winner(board) is None:
        board[i] = "X"
        buttons[i].config(text="X", state="disabled")

        result = check_winner(board)
        if result:
            game_over(result)
            return

        # Prevent further clicks and schedule AI move after a delay
        ai_thinking = True
        root.after(ai_delay_ms, ai_turn)

def ai_turn():
    global ai_thinking
    ai = best_move()
    if ai is not None and board[ai] == "":
        board[ai] = "O"
        buttons[ai].config(text="O", state="disabled")

    result = check_winner(board)
    if result:
        ai_thinking = False
        game_over(result)
        return

    # Re-enable clicking for remaining empty cells
    ai_thinking = False

def reset_game():
    global ai_thinking
    ai_thinking = False
    # Clear the board state
    for i in range(9):
        board[i] = ""
    # Reset the UI buttons
    for btn in buttons:
        btn.config(text="", state="normal")

def game_over(result):
    if result == "Draw":
        msg = "It's a Draw!"
    else:
        msg = f"{result} wins!"
    play_again = messagebox.askyesno("Game Over", f"{msg}\n\nPlay again?")
    if play_again:
        reset_game()
    else:
        
        root.destroy()



root = tk.Tk()
root.title("Tic Tac Toe with Minimax AI")

buttons = []
for i in range(9):
    b = tk.Button(root, text="", font=("Arial", 24), width=5, height=2,
                  command=lambda i=i: click(i))
    b.grid(row=i // 3, column=i % 3)
    buttons.append(b)

root.mainloop()