import pytest
from pycheckers.game import *


def test_squares_to_consider_for_man():
    piece = CheckerPiece(CheckerColor.RED, CheckerLevel.MAN)
    assert nearby_squares(piece, (1, 0)) == [(2, 1), (0, 1)]


def test_out_of_bounds():
    assert not out_of_bounds((0, 0))
    assert not out_of_bounds((0, 2))
    assert not out_of_bounds((5, 1))
    assert not out_of_bounds((7, 7))
    assert out_of_bounds((-1, 0))
    assert out_of_bounds((0, -1))
    assert out_of_bounds((8, 0))
    assert out_of_bounds((0, 8))


def test_legal_move_black_basic():
    game = CheckersGame.with_board(
        {(2, 7): CheckerPiece(CheckerColor.BLACK, CheckerLevel.MAN)}
    )

    assert man_legal_moves(game) == {
        (2, 7): [
            [(3, 6)],
            [(1, 6)],
        ]
    }


def test_legal_move_black_corner():
    game = CheckersGame.with_board(
        {(0, 7): CheckerPiece(CheckerColor.BLACK, CheckerLevel.MAN)}
    )

    assert man_legal_moves(game) == {
        (0, 7): [
            [(1, 6)],
        ]
    }


def test_legal_move_black_capture():
    game = CheckersGame.with_board(
        {
            (2, 7): CheckerPiece(CheckerColor.BLACK, CheckerLevel.MAN),
            (3, 6): CheckerPiece(CheckerColor.RED, CheckerLevel.MAN),
        }
    )

    assert man_legal_moves(game) == {(2, 7): [[(4, 5)]]}


def test_legal_move_black_multi_capture():
    game = CheckersGame.with_board(
        {
            (2, 7): CheckerPiece(CheckerColor.BLACK, CheckerLevel.MAN),
            (3, 6): CheckerPiece(CheckerColor.RED, CheckerLevel.MAN),
            (3, 4): CheckerPiece(CheckerColor.RED, CheckerLevel.MAN),
        }
    )

    assert man_legal_moves(game) == {(2, 7): [[(4, 5), (2, 3)]]}


def test_legal_move_black_multi_capture_different_paths():
    game = CheckersGame.with_board(
        {
            (2, 7): CheckerPiece(CheckerColor.BLACK, CheckerLevel.MAN),
            (3, 6): CheckerPiece(CheckerColor.RED, CheckerLevel.MAN),
            (3, 4): CheckerPiece(CheckerColor.RED, CheckerLevel.MAN),
            (5, 4): CheckerPiece(CheckerColor.RED, CheckerLevel.MAN),
        }
    )

    assert man_legal_moves(game) == {
        (2, 7): [
            [(4, 5), (6, 3)],
            [(4, 5), (2, 3)],
        ]
    }


def test_str_board():
    game = CheckersGame.with_board(
        {
            (2, 7): CheckerPiece(CheckerColor.BLACK, CheckerLevel.MAN),
            (3, 6): CheckerPiece(CheckerColor.BLACK, CheckerLevel.KING),
            (0, 1): CheckerPiece(CheckerColor.RED, CheckerLevel.MAN),
            (1, 0): CheckerPiece(CheckerColor.RED, CheckerLevel.MAN),
            (3, 2): CheckerPiece(CheckerColor.RED, CheckerLevel.KING),
        }
    )
    assert (
        str(game)
        == """\
. m . . . . . .
m . . . . . . .
. . . k . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . K . . . .
. . M . . . . ."""
    )


def test_illegal_moves():
    game = CheckersGame.with_board(
        {
            (2, 7): CheckerPiece(CheckerColor.BLACK, CheckerLevel.MAN),
            (3, 6): CheckerPiece(CheckerColor.RED, CheckerLevel.MAN),
        }
    )

    with pytest.raises(BadMoveException):
        game.move((0, 1), [(1, 2)])

    with pytest.raises(BadMoveException):
        game.move((2, 7), [(3, 8)])

    with pytest.raises(BadMoveException):
        game.move((2, 7), [(3, 6)])

    with pytest.raises(BadMoveException):
        game.move((2, 7), [(0, 0)])


def test_legal_move():
    game = CheckersGame.with_board(
        {
            (2, 7): CheckerPiece(CheckerColor.BLACK, CheckerLevel.MAN),
        }
    )

    game.move((2, 7), [(3, 6)])

    assert game.board[3, 6] == CheckerPiece(CheckerColor.BLACK, CheckerLevel.MAN)


def test_legal_move_as_list():
    game = CheckersGame.with_board(
        {
            (2, 7): CheckerPiece(CheckerColor.BLACK, CheckerLevel.MAN),
        }
    )

    game.move((2, 7), [[3, 6]])

    assert game.board[3, 6] == CheckerPiece(CheckerColor.BLACK, CheckerLevel.MAN)


def test_pos_to_square_number():
    assert pos_to_square_number((1, 0)) == 1
    assert pos_to_square_number((7, 0)) == 4
    assert pos_to_square_number((0, 1)) == 5
    assert pos_to_square_number((6, 1)) == 8
    assert pos_to_square_number((6, 5)) == 24
    assert pos_to_square_number((7, 6)) == 28
    assert pos_to_square_number((6, 7)) == 32


def test_square_number_to_pos():
    assert square_number_to_pos(1) == (1, 0)
    assert square_number_to_pos(4) == (7, 0)
    assert square_number_to_pos(5) == (0, 1)
    assert square_number_to_pos(28) == (7, 6)
    assert square_number_to_pos(29) == (0, 7)
    assert square_number_to_pos(32) == (6, 7)


if __name__ == "__main__":
    pytest.main(["-vv"])
