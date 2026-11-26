"""2-player Tic-Tac-Toe for the terminal."""

WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
    (0, 4, 8), (2, 4, 6),             # diagonals
]


def new_board():
    """Return a fresh board holding the labels '1'..'9'."""
    return [str(i) for i in range(1, 10)]


def display_board(board):
    """Print the 3x3 board."""
    print()
    for row in range(3):
        a, b, c = board[row * 3: row * 3 + 3]
        print(f" {a} | {b} | {c} ")
        if row < 2:
            print("---+---+---")
    print()


def get_move(board, player):
    """Ask the current player for a valid, free position (1-9). Returns a 0-based index."""
    while True:
        try:
            raw = input(f"Player {player}, choose a position (1-9): ").strip()
        except EOFError:
            print("\nInput closed. Exiting game.")
            raise SystemExit
        if not raw.isdigit() or not 1 <= int(raw) <= 9:
            print("Invalid input. Please enter a number from 1 to 9.")
            continue
        index = int(raw) - 1
        if board[index] in ("X", "O"):
            print("Spot taken, try again")
            continue
        return index


def check_winner(board):
    """Return 'X' or 'O' if someone has three in a row, otherwise None."""
    for a, b, c in WIN_LINES:
        if board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_draw(board):
    """True if every spot is taken."""
    return all(spot in ("X", "O") for spot in board)


def play_game():
    """Run a single game from start to finish."""
    board = new_board()
    player = "X"  # Player 1 = X, Player 2 = O
    display_board(board)

    while True:
        board[get_move(board, player)] = player
        display_board(board)

        if check_winner(board):
            number = 1 if player == "X" else 2
            print(f"Player {number} ({player}) wins!")
            return
        if is_draw(board):
            print("It's a draw!")
            return

        player = "O" if player == "X" else "X"


def ask_play_again():
    """Ask until the user answers Yes or No. Returns True for Yes."""
    while True:
        try:
            answer = input("Do you want to play again? Yes/No: ").strip().lower()
        except EOFError:
            return False
        if answer in ("yes", "y"):
            return True
        if answer in ("no", "n"):
            return False
        print("Please type Yes or No.")


def main():
    print("=== Tic-Tac-Toe ===")
    print("Player 1 is X, Player 2 is O.")
    while True:
        play_game()
        if not ask_play_again():
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()