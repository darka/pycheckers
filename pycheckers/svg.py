from main import CheckersGame

import xml.etree.ElementTree as ET


def render(game: CheckersGame, board_size: int) -> str:
    square_size = board_size / 8
    svg = ET.element('svg')
    for y in range(8):
        for x in range(8):
            piece = game.board.get((x, y))
            if piece is None:
                # draw empty square
                svg.SubElement('rect', 'square', {'width': square_size, 'height': square_size,})
            else:
                pass
                # draw piece
