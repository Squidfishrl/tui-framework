"""Test that src/_coordinates.py works correctly"""
import pytest

from tui._coordinates import (
        Coordinates,
        Rectangle,
        CoordinateError,
        RestrictedCoordinates
    )


@pytest.fixture
def three_by_two_rectangle() -> Rectangle:
    """Return a 3 wide 2 tall rectangle at 0,0"""
    rect = Rectangle(
            top_left=Coordinates(0, 0),
            bottom_right=Coordinates(_column=3, _row=2)
        )

    return rect


def test_coordinates_init():
    """Test that coordinates are initialised correctly"""
    coord = Coordinates(_row=1, _column=5)
    assert (coord.row == 1 and coord.column == 5)


def test_rectangle_init(three_by_two_rectangle: Rectangle):
    """Test that a rectangle is initialised correctly"""
    assert (
            three_by_two_rectangle.top_left == Coordinates(_row=0, _column=0)
            and
            three_by_two_rectangle.top_right == Coordinates(_row=0, _column=3)
            and
            three_by_two_rectangle.bottom_left == Coordinates(_row=2,
                                                              _column=0)
            and
            three_by_two_rectangle.bottom_right == Coordinates(_row=2,
                                                               _column=3)
        )


def test_init_rectangle_with_one_row():
    """Test that a rectangle with one row can be initialised correctly"""
    rect = Rectangle(
            top_left=Coordinates(0, 0),
            bottom_right=Coordinates(_column=3, _row=0)
        )

    assert (
            rect.top_left == Coordinates(_row=0, _column=0)
            and
            rect.top_right == Coordinates(_row=0, _column=3)
            and
            rect.bottom_left == Coordinates(_row=0, _column=0)
            and
            rect.bottom_right == Coordinates(_row=0, _column=3)
        )


def test_rectangle_rows():
    """Test that a rectangle returns the correct amount of rows"""
    rect = Rectangle(
            top_left=Coordinates(0, 0),
            bottom_right=Coordinates(_column=3, _row=3)
        )

    assert rect.rows == 4


def test_rectangle_columns():
    """Test that a rectangle returns the correct amount of columns"""
    rect = Rectangle(
            top_left=Coordinates(0, 0),
            bottom_right=Coordinates(_column=3, _row=3)
        )

    assert rect.columns == 4


def test_rectangle_move_top_left_point(three_by_two_rectangle: Rectangle):
    """Test that a rectangle remains correct after moving its top left point"""
    three_by_two_rectangle.top_left = Coordinates(_row=1, _column=2)
    assert (
            three_by_two_rectangle.top_left == Coordinates(_row=1, _column=2)
            and
            three_by_two_rectangle.top_right == Coordinates(_row=1, _column=3)
            and
            three_by_two_rectangle.bottom_left == Coordinates(_row=2,
                                                              _column=2)
            and
            three_by_two_rectangle.bottom_right == Coordinates(_row=2,
                                                               _column=3)
        )


def test_rectangle_move_top_right_point(three_by_two_rectangle: Rectangle):
    """Test that a rectangle is correct after moving its top right point"""
    three_by_two_rectangle.top_right = Coordinates(_row=1, _column=2)
    assert (
            three_by_two_rectangle.top_left == Coordinates(_row=1, _column=0)
            and
            three_by_two_rectangle.top_right == Coordinates(_row=1, _column=2)
            and
            three_by_two_rectangle.bottom_left == Coordinates(_row=2,
                                                              _column=0)
            and
            three_by_two_rectangle.bottom_right == Coordinates(_row=2,
                                                               _column=2)
        )


def test_rectangle_move_bottom_left_point(three_by_two_rectangle: Rectangle):
    """Test that a rectangle is correct after moving its bottom left point"""
    three_by_two_rectangle.bottom_left = Coordinates(_row=1, _column=2)
    assert (
            three_by_two_rectangle.top_left == Coordinates(_row=0, _column=2)
            and
            three_by_two_rectangle.top_right == Coordinates(_row=0, _column=3)
            and
            three_by_two_rectangle.bottom_left == Coordinates(_row=1,
                                                              _column=2)
            and
            three_by_two_rectangle.bottom_right == Coordinates(_row=1,
                                                               _column=3)
        )


def test_rectangle_move_bottom_right_point(three_by_two_rectangle: Rectangle):
    """Test that a rectangle is correct after moving its bottom right point"""
    three_by_two_rectangle.bottom_right = Coordinates(_row=1, _column=2)
    assert (
            three_by_two_rectangle.top_left == Coordinates(_row=0, _column=0)
            and
            three_by_two_rectangle.top_right == Coordinates(_row=0, _column=2)
            and
            three_by_two_rectangle.bottom_left == Coordinates(_row=1,
                                                              _column=0)
            and
            three_by_two_rectangle.bottom_right == Coordinates(_row=1,
                                                               _column=2)
        )


def test_rectangle_move_two_points(three_by_two_rectangle: Rectangle):
    """Test that a rectangle is correct after moving its top left and bottom
    right point"""
    three_by_two_rectangle.bottom_right = Coordinates(_row=4, _column=5)
    three_by_two_rectangle.top_left = Coordinates(_row=1, _column=2)
    assert (
            three_by_two_rectangle.top_left == Coordinates(_row=1, _column=2)
            and
            three_by_two_rectangle.top_right == Coordinates(_row=1, _column=5)
            and
            three_by_two_rectangle.bottom_left == Coordinates(_row=4,
                                                              _column=2)
            and
            three_by_two_rectangle.bottom_right == Coordinates(_row=4,
                                                               _column=5)
        )


def test_move_point_to_invalid_coordinate(three_by_two_rectangle: Rectangle):
    """Test that CoordinateError exception is thrown when moving a point to
    invalid coordinates"""
    with pytest.raises(CoordinateError):
        three_by_two_rectangle.top_left = Coordinates(10, 10)


def test_restricted_coordinates_init(three_by_two_rectangle: Rectangle):
    """Test that RestrictedCoordinates are initialised correctly"""
    rcoords = RestrictedCoordinates(
            _row=0,
            _column=0,
            _restriction=three_by_two_rectangle
        )

    assert (
            rcoords.row == 0 and
            rcoords.column == 0 and
            rcoords.restriction == three_by_two_rectangle
        )


def test_restricted_coordinates_init_error(three_by_two_rectangle: Rectangle):
    """Test that RestrictedCoordinates are initialised correctly"""
    with pytest.raises(IndexError):
        _ = RestrictedCoordinates(
                _row=4,
                _column=0,
                _restriction=three_by_two_rectangle
            )
