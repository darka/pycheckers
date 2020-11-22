import pytest
from pycheckers import *


def test_squares_to_consider_for_man():
    piece = CheckerPiece(CheckerColor.RED, CheckerLevel.MAN)
    assert squares_to_consider_for_man(piece, 1, 0) == ((2, 1), (0, 1))


def test_out_of_bounds():
    assert not out_of_bounds(0, 0)
    assert not out_of_bounds(0, 2)
    assert not out_of_bounds(5, 1)
    assert not out_of_bounds(7, 7)
    assert out_of_bounds(-1, 0)
    assert out_of_bounds(0, -1)
    assert out_of_bounds(8, 0)
    assert out_of_bounds(0, 8)


def test_legal_move_black_basic():
    game = CheckersGame.with_board({
        (2, 7): CheckerPiece(CheckerColor.BLACK, CheckerLevel.MAN)
    })

    assert man_legal_moves(game) == {
        (2, 7): [
            [(3, 6)],
            [(1, 6)],
        ]
    }


def test_legal_move_black_corner():
    game = CheckersGame.with_board({
        (0, 7): CheckerPiece(CheckerColor.BLACK, CheckerLevel.MAN)
    })

    assert man_legal_moves(game) == {
        (0, 7): [
            [(1, 6)],
        ]
    }



if __name__ == '__main__':
    pytest.main()
