from pycheckers.game import CheckersGame

import xml.etree.ElementTree as ET


def render(game: CheckersGame, board_size: int) -> str:
    square_size = board_size / 8
    svg = ET.Element('svg')
    for y in range(8):
        for x in range(8):
            piece = game.board.get((x, y))
            if piece is None:
                # draw empty square
                ET.SubElement(svg, 'rect', {'width': str(square_size),
                                            'height': str(square_size),
                                            'x': str(x*square_size),
                                            'y': str(y*square_size)})
            else:
                pass
                # draw piece
    return ET.dump(svg)
