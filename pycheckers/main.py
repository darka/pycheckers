from pycheckers.game import *
from pycheckers.svg import render


def main():
    game = CheckersGame.with_board(
        {
            (2, 7): CheckerPiece(CheckerColor.BLACK, CheckerLevel.MAN),
            (3, 6): CheckerPiece(CheckerColor.BLACK, CheckerLevel.KING),
            (0, 1): CheckerPiece(CheckerColor.RED, CheckerLevel.MAN),
            (1, 0): CheckerPiece(CheckerColor.RED, CheckerLevel.MAN),
            (3, 2): CheckerPiece(CheckerColor.RED, CheckerLevel.KING),
        }
    )
    print(game)
    print(render(game, 64))


if __name__ == "__main__":
    main()
