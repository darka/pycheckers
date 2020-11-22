import enum
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
    return piece.level == CheckerColor.RED


class CheckersException(Exception):
    pass


class BadMove(CheckersException):
    pass


class CheckersGame:
    def __init__(self):
        self.board = [[None]*8 for _ in range(8)]
        self.pieces = set()
        self.turn = CheckerColor.BLACK

    def move(self, color, x, y, x1, y1):
        if color != self.turn:
            raise BadMove('Wrong color turn')
        
        old_piece = CheckerPiece(color, x, y)
        if old_piece not in self.pieces:
            raise BadMove(f'No {color} piece not at: {x} {y}')
        
        if not (0 <= x1 < 8):
            raise Exception(f'{x1} is out of bounds')

        if not (0 <= y1 < 8):
            raise Exception(f'{y1} is out of bounds')

        self.next_turn()
    
    def next_turn(self):
        if self.turn == CheckerColor.BLACK:
            self.turn = CheckerColor.RED
        else:
            self.turn = CheckerColor.BLACK


def empty_square(board, x, y):
    if not board[y][x]:
        return True
    return False


def out_of_bounds(board, x, y):
    if (0 <= x < 8) and (0 <= y < 8):
        return False

    return True


def man_legal_moves(board, piece, x, y):
    direction = man_y_direction(piece)
    
    possible_moves = (x+1, y+1*direction), (x-1, y+1*direction)

    moves = []

    for move in possible_moves:
        if out_of_bounds(board, *move):
            continue


def man_can_capture(board, piece, x, y, x1, y1):
    direction = man_y_direction(piece)
    
    if not board[y1][x1]:
        raise Exception(f'Nothing on the board at ({x1},{y1})')

    other_color = CheckerColor.RED if piece.color == CheckerColor.BLACK else CheckerColor.BLACK

    if board[y1][x1].color != other_color:
        return False

    square_to_check = (x1+(x1-x), y+1*direction)

    if out_of_bounds(board, *square_to_check):
        return False

    if board[square_to_check[1]][square_to_check[0]]:
        return False
    
    return True


def man_y_direction(piece):
    if is_black(piece):
        return -1
    else:
        return 1


def squares_to_consider_for_man(board, piece, x, y):
    direction = man_y_direction(piece)
    return (x+1, y+1*direction), (x-1, y+1*direction)

# def main():


if __name__ == '__main__':
    main()
