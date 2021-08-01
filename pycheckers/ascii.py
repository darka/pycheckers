from pycheckers.piece import CheckerColor, CheckerLevel, CheckerPiece

ASCII_SYMBOLS = {
    CheckerColor.RED: {CheckerLevel.MAN: "m", CheckerLevel.KING: "k"},
    CheckerColor.WHITE: {CheckerLevel.MAN: "M", CheckerLevel.KING: "K"},
}


def ascii_symbol(piece: CheckerPiece) -> str:
    return ASCII_SYMBOLS[piece.color][piece.level]
