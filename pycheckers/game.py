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


class BadMoveException(CheckersException):
    pass


RED_START_POS = [
    (1, 0), (3, 0), (5, 0), (7, 0),
    (0, 1), (2, 1), (4, 1), (6, 1),
    (1, 2), (3, 2), (5, 2), (7, 2),
]

BLACK_START_POS = [
    (0, 5), (2, 5), (4, 5), (6, 5),
    (1, 6), (3, 6), (5, 6), (7, 6),
    (0, 7), (2, 7), (4, 7), (6, 7),
]

ASCII_SYMBOLS = {
    CheckerColor.RED: {
        CheckerLevel.MAN: 'm',
        CheckerLevel.KING: 'k'
    },
    CheckerColor.BLACK: {
        CheckerLevel.MAN: 'M',
        CheckerLevel.KING: 'K'
    }
}

def initial_setup_board():
    return CheckersGame.with_board(
        {
            **{pos: CheckerPiece( CheckerColor.RED, CheckerLevel.MAN ) for pos in RED_START_POS},
            **{pos: CheckerPiece( CheckerColor.BLACK, CheckerLevel.MAN ) for pos in BLACK_START_POS},
        }
    )


def ascii_symbol(piece):
    return ASCII_SYMBOLS[piece.color][piece.level]


class CheckersGame:
    def __init__(self):
        self.board = {}
        self.turn = CheckerColor.BLACK

    @classmethod
    def with_board(cls, board):
        game = cls()
        game.board = board
        return game

    def __str__(self):
        lines = []
        for y in range(8):
            symbols = [self._get_ascii_symbol((x, y)) for x in range(8)]
            line = ' '.join(symbols)
            lines.append(line)
        return '\n'.join(lines)

    def _get_ascii_symbol(self, pos):
        piece = self.board.get(pos)
        if not piece:
            return '.'
        else:
            return ascii_symbol(piece)

    def move(self, start, moves):
        moves = [tuple(m) for m in moves]
        start = tuple(start)
        # Is there such a piece?
        if start not in self.board:
            raise BadMoveException(f'Square {start} is empty')

        piece = self.board[start]

        # Is the colour right?
        if piece.color != self.turn:
            raise BadMoveException('Wrong color turn')

        legal_moves = man_legal_moves(self)

        # Can this piece move at all?
        if start not in legal_moves:
            raise BadMoveException('Piece cannot move anywhere')
        
        # Is this move legal?
        for legal_move in legal_moves[start]:
            if moves == legal_move:
                break
        else:
            raise BadMoveException(f'Piece cannot move to ({moves})')

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

        self.next_turn()
    
    def next_turn(self):
        if self.turn == CheckerColor.BLACK:
            self.turn = CheckerColor.RED
        else:
            self.turn = CheckerColor.BLACK


def is_capture_move(start, end):
    return abs(end[0] - start[0]) == 2


def capture_square(start, end):
    dx = end[0] - start[0]
    dx = dx / abs(dx)
    dy = end[1] - start[1]
    dy = dy / abs(dy)
    return (start[0] + dx, start[1] + dy)


def out_of_bounds(sq):
    x, y = sq
    return x < 0 or x >= 8 or y < 0 or y >= 8


def man_legal_moves(game: CheckersGame):  # TODO: add a cache
    with_captures = defaultdict(list)
    without_captures = defaultdict(list)

    current_turn = game.turn

    for position, piece in game.board.items():
        if piece.color != current_turn:
            continue

        if is_king(piece):
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
    for sq in nearby_squares(piece, start):
        capture_sq = get_capture_sq(game, piece, start, sq)
        if not capture_sq:
            continue
        else:
            path_new = path + [capture_sq]
            _find_capture_paths(game, piece, path_new, all_paths)
            end_of_path = False

    # this tells us we recursed to the end of the capture path
    if end_of_path:
        all_paths.append(path)


def get_capture_sq(game, piece, pos, other_pos):
    if is_empty(game, other_pos):
        return None

    other_color = CheckerColor.RED if piece.color == CheckerColor.BLACK else CheckerColor.BLACK

    other_piece = game.board[other_pos]

    if other_piece.color != other_color:
        return None

    x, y = pos
    x1, y1 = other_pos
    square_to_check = (x1+(x1-x), y1+(y1-y))

    if out_of_bounds(square_to_check):
        return None

    if not is_empty(game, square_to_check):
        return None

    return square_to_check


def is_empty(game, pos):
    return pos not in game.board


def man_y_direction(piece):
    assert piece.level == CheckerLevel.MAN
    if is_black(piece):
        return -1
    else:
        return 1


def nearby_squares(piece, pos):
    x, y = pos
    if piece.level == CheckerLevel.KING:
        return (x+1, y+1), (x-1, y+1), (x-1, y-1), (x+1, y-1)
    else:
        direction = man_y_direction(piece)
        return (x+1, y+1*direction), (x-1, y+1*direction)

