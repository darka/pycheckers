from pycheckers.piece import CheckerLevel, CheckerPiece, is_white


def capture_square(start: tuple[int, int], end: tuple[int, int]) -> tuple[int, int]:
    dx = end[0] - start[0]
    dx = dx / abs(dx)
    dy = end[1] - start[1]
    dy = dy / abs(dy)
    return (start[0] + dx, start[1] + dy)


def out_of_bounds(sq: tuple[int, int]) -> bool:
    x, y = sq
    return x < 0 or x >= 8 or y < 0 or y >= 8


def pos_to_square_number(pos):
    nx = pos[0] // 2 + 1
    ny = 4 * pos[1]
    return ny + nx


def square_number_to_pos(n):
    y = (n - 1) // 4
    x = (n - 1) % 4 * 2
    if y % 2 == 0:
        x += 1
    return (x, y)


def _man_y_direction(piece: CheckerPiece) -> int:
    assert piece.level == CheckerLevel.MAN
    if is_white(piece):
        return 1
    else:
        return -1


def nearby_squares(piece: CheckerPiece, pos: tuple[int, int]) -> list[tuple[int, int]]:
    x, y = pos
    if piece.level == CheckerLevel.KING:
        return [(x + 1, y + 1), (x - 1, y + 1), (x - 1, y - 1), (x + 1, y - 1)]
    else:
        direction = _man_y_direction(piece)
        return [(x + 1, y + 1 * direction), (x - 1, y + 1 * direction)]
