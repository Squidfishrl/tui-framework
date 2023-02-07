"""Structure to store the 2d coordinates"""

from __future__ import annotations

from dataclasses import dataclass


class CoordinateError(ValueError):
    """Raise when invalid coordinates are passed"""


@dataclass
class Coordinates:
    """Structure for containing mutable coordinates"""
    _row: int
    _column: int

    @property
    def row(self) -> int:
        """Get row coordinate"""
        return self._row

    @row.setter
    def row(self, row) -> None:
        """Set row coordinate"""
        self._row = row

    @property
    def column(self) -> int:
        """Get column coordinate"""
        return self._column

    @column.setter
    def column(self, column: int) -> None:
        """Set column coordinate"""
        self._column = column


@dataclass(init=False)
class RestrictedCoordinates(Coordinates):
    """Coordinates that can't go out of rectangular bounds"""
    _restriction: Rectangle

    def __init__(self, _row: int, _column: int, _restriction: Rectangle):
        self.restriction = _restriction
        self.row = _row
        self.column = _column

    def reset_coords(self) -> None:
        """Reset coordinates to the start of the rectangle"""
        self.row = self.restriction.top_left.row
        self.column = self.restriction.top_left.column

    @property
    def restriction(self) -> Rectangle:
        """Get the restrictive rectangle"""
        return self._restriction

    @restriction.setter
    def restriction(self, restriction: Rectangle) -> None:
        """Change the restrictive rectangle and reset coordinates"""
        self._restriction = restriction
        self.reset_coords()

    @Coordinates.row.setter
    def row(self, row) -> None:
        if (row > self.restriction.bottom_left.row or
                row < self.restriction.top_left.row):
            raise IndexError("Coordinate out of bounds")

        self._row = row

    @Coordinates.column.setter
    def column(self, column) -> None:
        if (column < self.restriction.top_left.column or
                column > self.restriction.bottom_right.column):
            raise IndexError("Coordinate out of bounds")

        self._column = column


class Rectangle:
    """Structure containing 4 Coordinates describing a rectangle"""
    def __init__(
            self,
            top_left: Coordinates,
            bottom_right: Coordinates
    ) -> None:

        self._top_left = top_left
        self._bottom_right = bottom_right
        self._top_right = Coordinates(
                _row=top_left.row,
                _column=bottom_right.column
            )
        self._bottom_left = Coordinates(
                _row=bottom_right.row,
                _column=top_left.column
            )

    def inner_rect(
            self,
            top_offset: int,
            bottom_offset: int,
            left_offset: int,
            right_offset: int
    ) -> Rectangle:
        """Create an inner rectangle. Used for area box model"""
        return Rectangle(
                top_left=Coordinates(
                        _row=self.top_left.row + top_offset,
                        _column=self.top_left.column + left_offset
                    ),
                bottom_right=Coordinates(
                        _row=self.bottom_right.row - bottom_offset,
                        _column=self.bottom_right.column - right_offset
                    )
            )

    @property
    def rows(self) -> int:
        """Get the amount of rows in the rectnangle"""
        return (self.bottom_left.row - self.top_left.row) + 1

    @property
    def columns(self) -> int:
        """Get the amount of columns in the rectangle"""
        return (self.top_right.column - self.top_left.column) + 1

    @property
    def top_left(self) -> Coordinates:
        """Return the top_left point coordinates"""
        return self._top_left

    @property
    def top_right(self) -> Coordinates:
        """Return the top_right point coordinates"""
        return self._top_right

    @property
    def bottom_left(self) -> Coordinates:
        """Return the bottom_left point coordinates"""
        return self._bottom_left

    @property
    def bottom_right(self) -> Coordinates:
        """Return the bottom_right point coordinates"""
        return self._bottom_right

    @top_left.setter
    def top_left(self, new_coords: Coordinates) -> None:
        """Set the top_left point coordinates"""
        if new_coords.column > self._top_right.column:
            raise CoordinateError("Invalid column coordinates")

        if new_coords.row > self._bottom_left.row:
            raise CoordinateError("Invalid row coordinates")

        self._top_left.column = new_coords.column
        self._top_left.row = new_coords.row

        self._top_right.row = new_coords.row
        self._bottom_left.column = new_coords.column

    @top_right.setter
    def top_right(self, new_coords: Coordinates) -> None:
        """Set the top_right point coordinates"""
        if new_coords.column < self._top_left.column:
            raise CoordinateError("Invalid column coordinates")

        if new_coords.row > self._bottom_right.row:
            raise CoordinateError("Invalid row coordinates")

        self._top_right.column = new_coords.column
        self._top_right.row = new_coords.row

        self._top_left.row = new_coords.row
        self._bottom_right.column = new_coords.column

    @bottom_left.setter
    def bottom_left(self, new_coords: Coordinates) -> None:
        """Set the bottom_left point coordinates"""
        if new_coords.column > self._bottom_right.column:
            raise CoordinateError("Invalid column coordinates")

        if new_coords.row < self._top_left.row:
            raise CoordinateError("Invalid row coordinates")

        self._bottom_left.column = new_coords.column
        self._bottom_left.row = new_coords.row

        self._top_left.column = new_coords.column
        self._bottom_right.row = new_coords.row

    @bottom_right.setter
    def bottom_right(self, new_coords: Coordinates) -> None:
        """Set the bottom_right point coordinates"""
        if new_coords.column < self._bottom_left.column:
            raise CoordinateError("Invalid column coordinates")

        if new_coords.row < self._top_right.row:
            raise CoordinateError("Invalid row coordinates")

        self._bottom_right.column = new_coords.column
        self._bottom_right.row = new_coords.row

        self._top_right.column = new_coords.column
        self._bottom_left.row = new_coords.row
