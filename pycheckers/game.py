from collections import defaultdict
import math
import random
from pycheckers.ascii import ascii_symbol
from pycheckers.piece import (
    CheckerColor,
    CheckerLevel,
    CheckerPiece,
    is_white,
    is_red,
    is_king,
    is_man,
)
from pycheckers.square import capture_square, nearby_squares, out_of_bounds
from typing import List, Optional, Tuple


class CheckersException(Exception):
    pass


class BadMoveException(CheckersException):
    pass


RED_START_POS = [
    (0, 5),
    (2, 5),
    (4, 5),
    (6, 5),
    (1, 6),
    (3, 6),
    (5, 6),
    (7, 6),
    (0, 7),
    (2, 7),
    (4, 7),
    (6, 7),
]

WHITE_START_POS = [
    (1, 0),
    (3, 0),
    (5, 0),
    (7, 0),
    (0, 1),
    (2, 1),
    (4, 1),
    (6, 1),
    (1, 2),
    (3, 2),
    (5, 2),
    (7, 2),
]


class CheckersGame:
    def __init__(self, turn: CheckerColor = CheckerColor.RED):
        self.board = {}
        self.turn = turn

    def copy(self) -> "CheckersGame":
        new_game = CheckersGame(self.turn)
        new_game.board = self.board.copy()
        return new_game

    def is_over(self) -> bool:
        white_piece_found, red_piece_found = self._colors_on_board()
        return not white_piece_found or not red_piece_found

    def winner(self) -> Optional[CheckerColor]:
        white_piece_found, red_piece_found = self._colors_on_board()
        if white_piece_found and red_piece_found:
            return None
        elif white_piece_found:
            return CheckerColor.WHITE
        elif red_piece_found:
            return CheckerColor.RED

    def _colors_on_board(self) -> Tuple[CheckerColor, CheckerColor]:
        if not self.board:
            raise Exception("There are no pieces on the board.")
        white_piece_found = False
        red_piece_found = False
        for piece in self.board.values():
            if is_white(piece):
                white_piece_found = True
            if is_red(piece):
                red_piece_found = True
        return white_piece_found, red_piece_found

    @classmethod
    def with_board(
        cls, board: dict, turn: CheckerColor = CheckerColor.RED
    ) -> "CheckersGame":
        game = cls(turn)
        game.board = board
        return game

    def __str__(self):
        lines = []
        for y in range(8):
            symbols = [self._get_ascii_symbol((x, y)) for x in range(8)]
            line = " ".join(symbols)
            lines.append(line)
        return "\n".join(lines)

    def _get_ascii_symbol(self, pos: Tuple[int, int]) -> str:
        piece = self.board.get(pos)
        if not piece:
            return "."
        else:
            return ascii_symbol(piece)

    def move(self, start: Tuple[int, int], moves: List[Tuple[int, int]]) -> None:
        moves = [tuple(m) for m in moves]
        start = tuple(start)
        # Is there such a piece?
        if start not in self.board:
            raise BadMoveException(f"Square {start} is empty")

        piece = self.board[start]

        # Is the colour right?
        if piece.color != self.turn:
            raise BadMoveException("Wrong color turn")

        all_legal_moves = legal_moves(self)

        # Can this piece move at all?
        if start not in all_legal_moves:
            raise BadMoveException("Piece cannot move anywhere")

        # Is this move legal?
        for legal_move in all_legal_moves[start]:
            if moves == legal_move:
                break
        else:
            raise BadMoveException(f"Piece cannot move to ({moves})")

        # Move the piece
        prev_move = start
        for move in moves:
            if is_capture_move(prev_move, move):
                sq = capture_square(prev_move, move)
                del self.board[sq]
            prev_move = move

        final_pos = moves[-1]
        self.board[final_pos] = piece
        del self.board[start]

        # Upgrade piece if we reached the end of the board
        if is_man(piece):
            if is_red(piece) and final_pos[1] == 0:
                self.board[final_pos] = CheckerPiece(
                    CheckerColor.RED, CheckerLevel.KING
                )
            elif is_white(piece) and final_pos[1] == 7:
                self.board[final_pos] = CheckerPiece(
                    CheckerColor.WHITE, CheckerLevel.KING
                )

        self.next_turn()

    def next_turn(self) -> None:
        if self.turn == CheckerColor.WHITE:
            self.turn = CheckerColor.RED
        else:
            self.turn = CheckerColor.WHITE


def initial_setup_board() -> CheckersGame:
    return CheckersGame.with_board(
        {
            **{
                pos: CheckerPiece(CheckerColor.RED, CheckerLevel.MAN)
                for pos in RED_START_POS
            },
            **{
                pos: CheckerPiece(CheckerColor.WHITE, CheckerLevel.MAN)
                for pos in WHITE_START_POS
            },
        }
    )


def legal_moves(game: CheckersGame) -> dict:  # TODO: add a cache
    with_captures = defaultdict(list)
    without_captures = defaultdict(list)

    current_turn = game.turn

    for position, piece in game.board.items():
        if piece.color != current_turn:
            continue

        for sq in nearby_squares(piece, position):
            if out_of_bounds(sq):
                continue

            if not with_captures and is_empty(game, sq):
                without_captures[position].append([sq])
                continue

            # Check nearby squares if we can capture something
            capture_sq = get_capture_sq(game, piece, position, sq)
            if not capture_sq:
                continue

            # If we can capture something, recursively find all possible moves
            capture_paths = []
            _find_capture_paths(game, piece, [capture_sq], capture_paths)
            if capture_paths:
                with_captures[position].extend(capture_paths)
    if with_captures:
        return with_captures
    else:
        return without_captures


def _find_capture_paths(
    game: CheckersGame,
    piece: CheckerPiece,
    path: List[Tuple[int, int]],
    all_paths: List[List[Tuple[int, int]]],
):
    start = path[-1]

    end_of_path = True
    for sq in nearby_squares(piece, start):
        capture_sq = get_capture_sq(game, piece, start, sq)
        if not capture_sq:
            continue
        elif capture_sq in path:
            continue
        else:
            path_new = path + [capture_sq]
            _find_capture_paths(game, piece, path_new, all_paths)
            end_of_path = False

    # this tells us we recursed to the end of the capture path
    if end_of_path:
        all_paths.append(path)


def get_capture_sq(
    game: CheckersGame,
    piece: CheckerPiece,
    pos: Tuple[int, int],
    other_pos: Tuple[int, int],
) -> Optional[Tuple[int, int]]:
    if is_empty(game, other_pos):
        return None

    other_color = (
        CheckerColor.RED if piece.color == CheckerColor.WHITE else CheckerColor.WHITE
    )

    other_piece = game.board[other_pos]

    if other_piece.color is not other_color:
        return None

    x, y = pos
    x1, y1 = other_pos
    square_to_check = (x1 + (x1 - x), y1 + (y1 - y))

    if out_of_bounds(square_to_check):
        return None

    if not is_empty(game, square_to_check):
        return None

    return square_to_check


def is_empty(game: CheckersGame, pos: Tuple[int, int]) -> bool:
    return pos not in game.board


def is_capture_move(start: Tuple[int, int], end: Tuple[int, int]) -> bool:
    return abs(end[0] - start[0]) == 2


def random_move(game: CheckersGame) -> None:
    by_position = legal_moves(game)
    all_moves = []
    for position, moves in by_position.items():
        for path in moves:
            all_moves.append((position, path))
    m = random.choice(all_moves)
    game.move(m[0], m[1])
