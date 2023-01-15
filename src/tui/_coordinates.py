"""Structure to store the 2d coordinates"""

from dataclasses import dataclass


class CoordinateError(ValueError):
    """Raise when invalid coordinates are passed"""


@dataclass
class Coordinates:
    """Structure for containing mutable coordinates"""
    row: int
    column: int


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
                row=top_left.row, 
                column=bottom_right.column
            )
        self._bottom_left= Coordinates(
                row=bottom_right.row,
                column=top_left.column
            )

    @property
    def top_left(self) -> Coordinates:
        return self._top_left

    @property
    def top_right(self) -> Coordinates:
        return self._top_right

    @property
    def bottom_left(self) -> Coordinates:
        return self._bottom_left

    @property
    def bottom_right(self) -> Coordinates:
        return self._bottom_right

    @top_left.setter
    def top_left(self, new_coords: Coordinates) -> None: 
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
        if new_coords.column < self._bottom_left.column:
            raise CoordinateError("Invalid column coordinates") 

        if new_coords.row < self._top_right.row:
            raise CoordinateError("Invalid row coordinates") 

        self._bottom_right.column = new_coords.column
        self._bottom_right.row = new_coords.row

        self._top_right.column = new_coords.column
        self._bottom_left.row = new_coords.row


