from pycheckers.svg import render
from pycheckers.game import CheckersGame

def test_render_basic():
    game = CheckersGame()
    svg_string = render(game, 400)
    assert svg_string.startswith("<svg")
