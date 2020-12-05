from pycheckers.game import CheckersGame, is_red

import xml.etree.ElementTree as ET


def render(game: CheckersGame, board_size: int) -> str:
    square_size = board_size // 8
    svg = ET.Element("svg", board_attributes(board_size))
    for y in range(8):
        for x in range(8):
            piece = game.board.get((x, y))
            if piece is None:
                # draw empty square
                ET.SubElement(svg, "rect", square_attributes(x, y, square_size))
            else:
                ET.SubElement(svg, "rect", square_attributes(x, y, square_size))
                ET.SubElement(
                    svg,
                    "circle",
                    circle_attributes(x, y, square_size, piece_color(piece)),
                )
                # draw piece
    return ET.tostring(svg, encoding="unicode")


def board_attributes(size):
    return {"width": str(size), "height": str(size)}


def square_attributes(x, y, size):
    return {
        "width": str(size),
        "height": str(size),
        "x": str(x * size),
        "y": str(y * size),
        "style": "fill:yellow;stroke:black;stroke-width:3",
    }


def circle_attributes(x, y, size, color):
    cx = x * size + size // 2
    cy = y * size + size // 2
    r = round(0.4 * size)
    return {
        "cx": str(cx),
        "cy": str(cy),
        "r": str(r),
        "style": f"fill:{color};stroke:black;stroke-width:3",
    }


def piece_color(checkers_piece):
    if is_red(checkers_piece):
        return "red"
    else:
        return "black"
