from pycheckers.game import CheckersGame, is_red

import xml.etree.ElementTree as ET


def render(game: CheckersGame, board_size: int) -> str:
    square_size = board_size // 8
    svg = ET.Element("svg", board_attributes(board_size))
    for y in range(8):
        for x in range(8):
            piece = game.board.get((x, y))

            # draw empty square
            ET.SubElement(svg, "rect", square_attributes(x, y, square_size))
            if piece is None:
                continue

            # draw piece
            ET.SubElement(
                svg,
                "circle",
                circle_attributes(x, y, square_size, piece_color(piece)),
            )

    return ET.tostring(svg, encoding="unicode")


def board_attributes(size):
    return {"width": str(size), "height": str(size)}


def square_attributes(x, y, size):
    return {
        "width": str(size),
        "height": str(size),
        "x": str(x * size),
        "y": str(y * size),
        "class": "board-square",
        "id": f"board-square-{x}-{y}",
    }


def circle_attributes(x, y, size, color):
    cx = x * size + size // 2
    cy = y * size + size // 2
    r = round(0.4 * size)
    return {"cx": str(cx), "cy": str(cy), "r": str(r), "class": f"checker-{color}"}


def piece_color(checkers_piece):
    if is_red(checkers_piece):
        return "red"
    else:
        return "black"
