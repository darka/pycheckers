"""Interactive CLI for playing checkers."""

from __future__ import annotations

import re
from pycheckers.game import CheckersGame, initial_setup_board, legal_moves, BadMoveException
from pycheckers.piece import CheckerColor
from pycheckers.square import pos_to_square_number, square_number_to_pos
from pycheckers.minimax import minimax


def parse_move_notation(notation: str) -> list[int]:
    """
    Parse move notation like '11-15' or '11x15x22' into list of square numbers.

    Args:
        notation: Move string using square numbers (1-32)

    Returns:
        List of square numbers in the move path

    Raises:
        ValueError: If notation is invalid
    """
    notation = notation.strip()

    # Match moves like "11-15" or "11x15x22" (captures)
    if 'x' in notation:
        parts = notation.split('x')
    elif '-' in notation:
        parts = notation.split('-')
    else:
        raise ValueError("Invalid move notation. Use format like '11-15' or '11x15x22'")

    try:
        squares = [int(p.strip()) for p in parts]
    except ValueError:
        raise ValueError("Move must contain only numbers and '-' or 'x'")

    # Validate square numbers
    for sq in squares:
        if sq < 1 or sq > 32:
            raise ValueError(f"Invalid square number: {sq}. Must be between 1 and 32")

    return squares


def notation_to_move(notation: str) -> tuple[tuple[int, int], list[tuple[int, int]]]:
    """
    Convert move notation to game move format.

    Args:
        notation: Move string like '11-15'

    Returns:
        Tuple of (start_pos, [move_path])
    """
    squares = parse_move_notation(notation)

    if len(squares) < 2:
        raise ValueError("Move must have at least a start and end square")

    # Convert square numbers to positions
    start_pos = square_number_to_pos(squares[0])
    move_path = [square_number_to_pos(sq) for sq in squares[1:]]

    return start_pos, move_path


def display_board(game: CheckersGame) -> None:
    """Display the board with square numbers and pieces."""
    print("\n  +---+---+---+---+---+---+---+---+")

    for y in range(7, -1, -1):
        row = f"{y} |"
        for x in range(8):
            pos = (x, y)
            piece = game.board.get(pos)

            # Only dark squares have pieces in checkers
            if (x + y) % 2 == 1:
                if piece:
                    if piece.color == CheckerColor.WHITE:
                        symbol = ' W ' if piece.level.name == 'MAN' else ' WK'
                    else:
                        symbol = ' R ' if piece.level.name == 'MAN' else ' RK'
                else:
                    # Show square number
                    sq_num = pos_to_square_number(pos)
                    symbol = f'{sq_num:2d} ' if sq_num < 10 else f'{sq_num} '
            else:
                symbol = '###'

            row += symbol + "|"

        print(row)
        print("  +---+---+---+---+---+---+---+---+")

    print("    0   1   2   3   4   5   6   7\n")


def display_legal_moves(game: CheckersGame) -> None:
    """Display all legal moves for the current player."""
    moves = legal_moves(game)

    if not moves:
        print("No legal moves available!")
        return

    print(f"\nLegal moves for {game.turn.name}:")
    for pos, paths in moves.items():
        sq_num = pos_to_square_number(pos)
        for path in paths:
            path_squares = [pos_to_square_number(p) for p in path]
            separator = 'x' if len(path) > 1 or abs(path[0][0] - pos[0]) == 2 else '-'
            move_str = str(sq_num) + separator + separator.join(map(str, path_squares))
            print(f"  {move_str}")


def get_player_move(game: CheckersGame) -> tuple[tuple[int, int], list[tuple[int, int]]]:
    """Get a valid move from the player."""
    while True:
        try:
            notation = input(f"\n{game.turn.name}'s move (or 'help', 'moves', 'quit'): ").strip()

            if notation.lower() == 'quit':
                return None, None
            elif notation.lower() == 'help':
                print("\nHow to play:")
                print("  - Enter moves using square numbers (1-32)")
                print("  - Format: '11-15' for regular moves")
                print("  - Format: '11x15x22' for captures")
                print("  - Type 'moves' to see all legal moves")
                print("  - Type 'quit' to exit")
                continue
            elif notation.lower() == 'moves':
                display_legal_moves(game)
                continue

            start, path = notation_to_move(notation)
            return start, path

        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error: {e}")


def play_human_vs_human():
    """Play a game of human vs human."""
    game = initial_setup_board()

    print("\n" + "=" * 50)
    print("CHECKERS - Human vs Human")
    print("=" * 50)
    print("\nW = White pieces, R = Red pieces")
    print("WK/RK = Kings")
    print("Numbers show available squares")

    while not game.is_over():
        display_board(game)

        start, path = get_player_move(game)

        if start is None:  # quit
            print("\nGame ended by player.")
            return

        try:
            game.move(start, path)
        except BadMoveException as e:
            print(f"Illegal move: {e}")
            print("Try again or type 'moves' to see legal moves.")

    # Game over
    display_board(game)
    winner = game.winner()
    print(f"\n{'=' * 50}")
    print(f"GAME OVER - {winner.name} WINS!")
    print(f"{'=' * 50}\n")


def play_human_vs_ai():
    """Play a game of human vs AI."""
    print("\n" + "=" * 50)
    print("CHECKERS - Human vs AI")
    print("=" * 50)

    # Choose color
    while True:
        color_choice = input("\nPlay as (R)ed or (W)hite? ").strip().upper()
        if color_choice in ['R', 'W']:
            break
        print("Please enter 'R' or 'W'")

    human_color = CheckerColor.RED if color_choice == 'R' else CheckerColor.WHITE
    ai_color = CheckerColor.WHITE if human_color == CheckerColor.RED else CheckerColor.RED

    # Choose difficulty
    print("\nDifficulty levels:")
    print("  1 - Easy (depth 1)")
    print("  2 - Medium (depth 3)")
    print("  3 - Hard (depth 5)")

    while True:
        try:
            difficulty = int(input("Choose difficulty (1-3): ").strip())
            if difficulty in [1, 2, 3]:
                break
            print("Please enter 1, 2, or 3")
        except ValueError:
            print("Please enter a number")

    depths = {1: 1, 2: 3, 3: 5}
    ai_depth = depths[difficulty]

    print(f"\nYou are {human_color.name}, AI is {ai_color.name}")
    print("W = White pieces, R = Red pieces")
    print("WK/RK = Kings")

    game = initial_setup_board()

    while not game.is_over():
        display_board(game)

        if game.turn == human_color:
            # Human turn
            start, path = get_player_move(game)

            if start is None:  # quit
                print("\nGame ended by player.")
                return

            try:
                game.move(start, path)
            except BadMoveException as e:
                print(f"Illegal move: {e}")
                print("Try again or type 'moves' to see legal moves.")
        else:
            # AI turn
            print(f"\n{ai_color.name} (AI) is thinking...")

            # Determine if AI is maximizing or minimizing
            maximizing = (ai_color == CheckerColor.WHITE)

            _, best_pos, best_path = minimax(game, ai_depth, maximizing)

            if best_pos is None:
                print("AI has no legal moves!")
                break

            # Display AI's move
            sq_num = pos_to_square_number(best_pos)
            path_squares = [pos_to_square_number(p) for p in best_path]
            separator = 'x' if len(best_path) > 1 or abs(best_path[0][0] - best_pos[0]) == 2 else '-'
            move_str = str(sq_num) + separator + separator.join(map(str, path_squares))
            print(f"{ai_color.name} plays: {move_str}")

            game.move(best_pos, best_path)

    # Game over
    display_board(game)
    winner = game.winner()
    print(f"\n{'=' * 50}")
    if winner == human_color:
        print(f"GAME OVER - YOU WIN!")
    else:
        print(f"GAME OVER - AI WINS!")
    print(f"{'=' * 50}\n")


def main():
    """Main entry point for interactive checkers."""
    while True:
        print("\n" + "=" * 50)
        print("CHECKERS")
        print("=" * 50)
        print("\n1. Human vs Human")
        print("2. Human vs AI")
        print("3. Quit")

        choice = input("\nChoose game mode (1-3): ").strip()

        if choice == '1':
            play_human_vs_human()
        elif choice == '2':
            play_human_vs_ai()
        elif choice == '3':
            print("\nThanks for playing!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
