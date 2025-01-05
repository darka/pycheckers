import math
from pycheckers.game import CheckersGame, legal_moves
from pycheckers.piece import CheckerColor, is_white, is_red, is_king


def board_value(game: CheckersGame) -> int:
    if game.is_over():
        if game.winner() == CheckerColor.WHITE:
            return 100
        elif game.winner() == CheckerColor.RED:
            return -100
        else:
            return 0

    ret = 0
    for piece in game.board.values():
        if is_white(piece):
            if is_king(piece):
                ret += 5
            else:
                ret += 1
        elif is_red(piece):
            if is_king(piece):
                ret -= 5
            else:
                ret -= 1
    return ret


def minimax(
    game: CheckersGame, depth: int, maximising_player: bool
) -> tuple[int, tuple[int, int] | None, list[tuple[int, int]] | None]:
    return _minimax_internal(game, depth, maximising_player, depth)


def _minimax_internal(
    game: CheckersGame, depth: int, maximising_player: bool, max_depth: int
) -> tuple[int, tuple[int, int] | None, list[tuple[int, int]] | None]:
    if depth == 0 or game.is_over():
        return board_value(game), None, None

    best_pos = None
    best_path = None

    if maximising_player:
        best_value = -math.inf

        moves = legal_moves(game)

        for pos, paths in moves.items():
            for path in paths:
                new_game = game.copy()
                new_game.move(pos, path)
                value, _, _ = _minimax_internal(new_game, depth - 1, False, max_depth)
                if depth == max_depth:
                    print(value, pos, path)
                if value > best_value:
                    best_value = value
                    best_pos = pos
                    best_path = path
    else:
        best_value = math.inf

        moves = legal_moves(game)

        for pos, paths in moves.items():
            for path in paths:
                new_game = game.copy()
                new_game.move(pos, path)
                value, _, _ = _minimax_internal(new_game, depth - 1, True, max_depth)
                if depth == max_depth:
                    print(value, pos, path)
                if value < best_value:
                    best_value = value
                    best_pos = pos
                    best_path = path
    if depth == max_depth:
        print(f"Picked move: {best_value}, {best_pos}, {best_path}")
    return best_value, best_pos, best_path
