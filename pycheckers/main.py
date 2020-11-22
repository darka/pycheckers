import enum
from collections import defaultdict
from dataclasses import dataclass


class CheckerColor(enum.Enum):
    RED = enum.auto()
    BLACK = enum.auto()


class CheckerLevel(enum.Enum):
    MAN = enum.auto()
    KING = enum.auto()


@dataclass(frozen=True)
class CheckerPiece:
    color: CheckerColor
    level: CheckerLevel


def is_man(piece):
    return piece.level == CheckerLevel.MAN


def is_king(piece):
    return piece.level == CheckerLevel.KING


def is_black(piece):
    return piece.color == CheckerColor.BLACK


def is_red(piece):
    return piece.color == CheckerColor.RED


class CheckersException(Exception):
    pass


class BadMove(CheckersException):
    pass


class CheckersGame:
    def __init__(self):
        self.board = {}
        self.turn = CheckerColor.BLACK

    @classmethod
    def with_board(cls, board):
        game = cls()
        game.board = board
        return game

    # def move(self, color, x, y, x1, y1):
    #     if color != self.turn:
    #         raise BadMove('Wrong color turn')
        
    #     old_piece = CheckerPiece(color, x, y)
    #     if old_piece not in self.pieces:
    #         raise BadMove(f'No {color} piece not at: {x} {y}')
        
    #     if not (0 <= x1 < 8):
    #         raise Exception(f'{x1} is out of bounds')

    #     if not (0 <= y1 < 8):
    #         raise Exception(f'{y1} is out of bounds')

    #     self.next_turn()
    
    def next_turn(self):
        if self.turn == CheckerColor.BLACK:
            self.turn = CheckerColor.RED
        else:
            self.turn = CheckerColor.BLACK


def out_of_bounds(x, y):
    return x < 0 or x >= 8 or y < 0 or y >= 8


def man_legal_moves(game: CheckersGame):
    with_captures = defaultdict(list)
    without_captures = defaultdict(list)

    current_turn = game.turn

    for position, piece in game.board.items():
        if piece.color != current_turn:
            continue

        if is_king(piece):
            continue

        for sq in squares_to_consider_for_man(piece, *position):
            if out_of_bounds(*sq):
                continue
            if not with_captures and is_empty(game, *sq):
                without_captures[position].append([sq])
                continue
            else:
                capture_sq = get_capture_sq(game, piece, *position, *sq)
                if capture_sq:
                    capture_paths = []
                    _find_capture_paths(game, piece, [capture_sq],
                                        capture_paths)
                    with_captures[position].extend(capture_paths)
    if with_captures:
        return with_captures
    else:
        return without_captures


def _find_capture_paths(game, piece, path, all_paths):
    start = path[-1]

    end_of_path = True
    for sq in squares_to_consider_for_man(piece, *start):
        capture_sq = get_capture_sq(game, piece, *start, *sq)
        if not capture_sq:
            continue
        else:
            path_new = path + [capture_sq]
            _find_capture_paths(game, piece, path_new, all_paths)
            end_of_path = False

    # this tells us we recursed to the end of the capture path
    if end_of_path:
        all_paths.append(path)


def get_capture_sq(game, piece, x, y, x1, y1):
    if is_empty(game, x1, y1):
        return None

    other_color = CheckerColor.RED if piece.color == CheckerColor.BLACK else CheckerColor.BLACK

    other_piece = game.board[x1, y1]

    if other_piece.color != other_color:
        return None

    square_to_check = (x1+(x1-x), y1+(y1-y))

    if out_of_bounds(*square_to_check):
        return None

    if not is_empty(game, *square_to_check):
        return None

    return square_to_check


def is_empty(game, x, y):
    return (x, y) not in game.board


def man_y_direction(piece):
    if is_black(piece):
        return -1
    else:
        return 1


def squares_to_consider_for_man(piece, x, y):
    direction = man_y_direction(piece)
    return (x+1, y+1*direction), (x-1, y+1*direction)
