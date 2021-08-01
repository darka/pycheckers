from enum import Enum, auto
from dataclasses import dataclass


class CheckerColor(Enum):
    RED = auto()
    WHITE = auto()


class CheckerLevel(Enum):
    MAN = auto()
    KING = auto()


@dataclass(frozen=True)
class CheckerPiece:
    color: CheckerColor
    level: CheckerLevel


def is_man(piece: CheckerPiece) -> bool:
    return piece.level == CheckerLevel.MAN


def is_king(piece: CheckerPiece) -> bool:
    return piece.level == CheckerLevel.KING


def is_white(piece: CheckerPiece) -> bool:
    return piece.color == CheckerColor.WHITE


def is_red(piece: CheckerPiece) -> bool:
    return piece.color == CheckerColor.RED
