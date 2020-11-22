import pytest
import sys
print(sys.path)
from pycheckers import *


@pytest.fixture
def board():
    return [[None]*8 for _ in range(8)]


def test_squares_to_consider_for_man(board):
    piece = CheckerPiece(CheckerColor.RED, CheckerLevel.MAN)
    assert squares_to_consider_for_man(board, piece, 1, 0) == ((2, 1), (0, 1))
