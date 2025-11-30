import pytest
from pycheckers.play import parse_move_notation, notation_to_move, display_board, display_legal_moves
from pycheckers.game import CheckersGame, initial_setup_board
from pycheckers.piece import CheckerPiece, CheckerColor, CheckerLevel
from pycheckers.square import pos_to_square_number, square_number_to_pos
from io import StringIO
import sys


# Tests for parse_move_notation function

def test_simple_move():
    """Test parsing a simple move with dash."""
    result = parse_move_notation("11-15")
    assert result == [11, 15]


def test_capture_move():
    """Test parsing a capture move with x."""
    result = parse_move_notation("11x15")
    assert result == [11, 15]


def test_multiple_captures():
    """Test parsing multiple captures."""
    result = parse_move_notation("11x15x22")
    assert result == [11, 15, 22]


def test_long_capture_chain():
    """Test parsing a long chain of captures."""
    result = parse_move_notation("1x8x15x22x29")
    assert result == [1, 8, 15, 22, 29]


def test_move_with_whitespace():
    """Test that whitespace is properly stripped."""
    result = parse_move_notation("  11-15  ")
    assert result == [11, 15]


def test_move_with_spaces_between():
    """Test move with spaces around separator."""
    result = parse_move_notation("11 - 15")
    assert result == [11, 15]


def test_all_valid_squares():
    """Test that all valid square numbers (1-32) are accepted."""
    result = parse_move_notation("1-32")
    assert result == [1, 32]


def test_invalid_no_separator():
    """Test that missing separator raises ValueError."""
    with pytest.raises(ValueError, match="Invalid move notation"):
        parse_move_notation("1115")


def test_invalid_square_too_low():
    """Test that square number below 1 raises ValueError."""
    with pytest.raises(ValueError, match="Invalid square number"):
        parse_move_notation("0-15")


def test_invalid_square_too_high():
    """Test that square number above 32 raises ValueError."""
    with pytest.raises(ValueError, match="Invalid square number"):
        parse_move_notation("11-33")


def test_invalid_non_numeric():
    """Test that non-numeric input raises ValueError."""
    with pytest.raises(ValueError, match="Move must contain only numbers"):
        parse_move_notation("a-b")


def test_invalid_empty_string():
    """Test that empty string raises ValueError."""
    with pytest.raises(ValueError, match="Invalid move notation"):
        parse_move_notation("")


def test_invalid_partial_move():
    """Test that partial move (only one number) raises ValueError."""
    with pytest.raises(ValueError, match="Invalid move notation"):
        parse_move_notation("11")


def test_mixed_separators_not_allowed():
    """Test that mixing separators raises ValueError."""
    # Should split by 'x', treating '-22' as a single part which will fail to parse as int
    with pytest.raises(ValueError, match="Move must contain only numbers"):
        parse_move_notation("11x15-22")


# Tests for notation_to_move function

def test_simple_move_conversion():
    """Test converting a simple move notation."""
    start, path = notation_to_move("11-15")
    assert start == square_number_to_pos(11)
    assert path == [square_number_to_pos(15)]


def test_capture_move_conversion():
    """Test converting a capture move."""
    start, path = notation_to_move("11x15")
    assert start == square_number_to_pos(11)
    assert path == [square_number_to_pos(15)]


def test_multiple_captures_conversion():
    """Test converting multiple captures."""
    start, path = notation_to_move("11x15x22")
    assert start == square_number_to_pos(11)
    assert path == [square_number_to_pos(15), square_number_to_pos(22)]


def test_long_path_conversion():
    """Test converting a long capture chain."""
    start, path = notation_to_move("1x8x15x22")
    assert start == square_number_to_pos(1)
    assert path == [
        square_number_to_pos(8),
        square_number_to_pos(15),
        square_number_to_pos(22),
    ]


def test_invalid_single_square():
    """Test that single square raises ValueError."""
    with pytest.raises(ValueError):
        # First will fail in parse_move_notation
        notation_to_move("11")


def test_invalid_notation_propagates():
    """Test that invalid notation from parse_move_notation propagates."""
    with pytest.raises(ValueError):
        notation_to_move("invalid")


# Tests for display_board function

def test_display_empty_board(capsys):
    """Test displaying an empty board."""
    game = CheckersGame.with_board({}, turn=CheckerColor.RED)
    display_board(game)

    captured = capsys.readouterr()
    output = captured.out

    # Check that board is displayed
    assert "+---+---+---+---+---+---+---+---+" in output
    # Check that square numbers are shown
    assert " 1 " in output
    assert "32 " in output


def test_display_initial_board(capsys):
    """Test displaying the initial game board."""
    game = initial_setup_board()
    display_board(game)

    captured = capsys.readouterr()
    output = captured.out

    # Check for white pieces
    assert " W " in output
    # Check for red pieces
    assert " R " in output
    # Check board structure
    assert "+---+---+---+---+---+---+---+---+" in output


def test_display_board_with_kings(capsys):
    """Test displaying board with king pieces."""
    # Place pieces on dark squares: (x+y) % 2 == 1
    game = CheckersGame.with_board(
        {
            (0, 7): CheckerPiece(CheckerColor.WHITE, CheckerLevel.KING),
            (1, 0): CheckerPiece(CheckerColor.RED, CheckerLevel.KING),
        },
        turn=CheckerColor.RED,
    )
    display_board(game)

    captured = capsys.readouterr()
    output = captured.out

    # Check for king pieces
    assert " WK" in output
    assert " RK" in output


def test_display_board_shows_coordinates(capsys):
    """Test that board displays coordinate labels."""
    game = initial_setup_board()
    display_board(game)

    captured = capsys.readouterr()
    output = captured.out

    # Check for x-axis coordinates
    assert "0   1   2   3   4   5   6   7" in output
    # Check for y-axis coordinates (should have rows 0-7)
    for i in range(8):
        assert f"{i} |" in output


# Tests for display_legal_moves function

def test_display_moves_for_initial_position(capsys):
    """Test displaying legal moves from initial position."""
    game = initial_setup_board()
    display_legal_moves(game)

    captured = capsys.readouterr()
    output = captured.out

    # Red moves first, so should show RED moves
    assert "Legal moves for RED:" in output
    # Should contain some move notation
    assert "-" in output


def test_display_no_legal_moves(capsys):
    """Test displaying when no legal moves are available."""
    # Create a board with no legal moves (e.g., only opponent pieces)
    game = CheckersGame.with_board(
        {(1, 0): CheckerPiece(CheckerColor.WHITE, CheckerLevel.MAN)},
        turn=CheckerColor.RED,
    )
    display_legal_moves(game)

    captured = capsys.readouterr()
    output = captured.out

    assert "No legal moves available!" in output


def test_display_capture_moves(capsys):
    """Test displaying capture moves with 'x' notation."""
    # Set up a position with a capture available
    # Red at (1,4) can capture White at (2,3) by jumping to (3,2)
    game = CheckersGame.with_board(
        {
            (1, 4): CheckerPiece(CheckerColor.RED, CheckerLevel.MAN),
            (2, 3): CheckerPiece(CheckerColor.WHITE, CheckerLevel.MAN),
        },
        turn=CheckerColor.RED,
    )
    display_legal_moves(game)

    captured = capsys.readouterr()
    output = captured.out

    # Should show capture notation with 'x'
    assert "x" in output


def test_display_simple_moves(capsys):
    """Test displaying simple moves with '-' notation."""
    game = CheckersGame.with_board(
        {(2, 2): CheckerPiece(CheckerColor.RED, CheckerLevel.MAN)},
        turn=CheckerColor.RED,
    )
    display_legal_moves(game)

    captured = capsys.readouterr()
    output = captured.out

    # Should show move notation with '-'
    assert "-" in output
    assert "Legal moves for RED:" in output


# Integration tests for square number conversions used in play.py

def test_round_trip_conversion():
    """Test that square number conversion is reversible."""
    for sq_num in range(1, 33):
        pos = square_number_to_pos(sq_num)
        converted_back = pos_to_square_number(pos)
        assert converted_back == sq_num


def test_notation_move_integration():
    """Test full integration of notation parsing and position conversion."""
    # Test a known move: square 11 is at position (2, 2) in Red's starting position
    start, path = notation_to_move("11-15")

    # Verify the conversion makes sense
    assert isinstance(start, tuple)
    assert len(start) == 2
    assert isinstance(path, list)
    assert len(path) == 1
    assert isinstance(path[0], tuple)
    assert len(path[0]) == 2
