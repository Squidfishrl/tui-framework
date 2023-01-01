"""Area for the component when it's rendered"""

from __future__ import annotations

import copy
from typing import TYPE_CHECKING

from tui._coordinates import Coordinates

if TYPE_CHECKING:
    from tui.style import AreaInfo


class Area:
    """Area for the component when it's rendered
    Defines how the component looks in isolation (without parents)
    """
    def __init__(
            self,
            area_info: AreaInfo  # min, max rows
    ) -> None:
        self._rows: int = area_info.min_rows
        self._columns: int = area_info.min_columns
        self.char_area: list[list[str]] = [  # rows x columns 
                [' ' for _ in range(self._columns)]
                for _ in range(self._rows)
            ]

        # is True where char_area is being occupied 
        self.occupied_area: list[list[bool]] = [  # rows x columns 
                [False for _ in range(self._columns)]
                for _ in range(self._rows)
            ]

        # used for easier char_area editing.
        self.area_ptr: Coordinates = Coordinates(0, 0)

    def add_chars(self, str: str, column_preserve: bool = False) -> None:
        """Add a string starting from area_ptr. '\n' means row increment
        area_ptr is unaffected
        """

        if not self._verify_str(str=str, column_preserve=column_preserve):
            raise IndexError("String is too large")

        # make sure area_ptr isn't mutated
        temp_ptr = copy.deepcopy(self.area_ptr)
        # TODO: verify that str is enough to fit in char_area

        for char in str:
            if char == '\n':
                temp_ptr.row += 1
                if column_preserve:
                    temp_ptr.column = self.area_ptr.column
                else:
                    temp_ptr.column = 0

                continue

            self.char_area[temp_ptr.row][temp_ptr.column] = char
            self.occupied_area[temp_ptr.row][temp_ptr.column] = True
            temp_ptr.column += 1

    def _verify_str(self, str: str, column_preserve: bool) -> bool:
        """Verify that string can fit in char_area - used in add_chars"""
        row = self.area_ptr.row
        column = self.area_ptr.column

        for char in str:
            if char == '\n':
                row += 1
                if column_preserve:
                    column = self.area_ptr.column
                else:
                    column = 0

                continue
 
            if row >= self.rows or column >= self.columns:
                return False

            column += 1

        return True

    def __str__(self):
        return "\n".join(["".join([char for char in row]) for row in self.char_area])

    @property
    def rows(self) -> int:
        """Get the rows in the area"""
        return self._rows

    @property
    def columns(self) -> int:
        """Get the columns in the area"""
        return self._columns

    @rows.setter
    def rows(self, rows: int) -> None:
        """Set the rows in the area"""
        if rows < 0:
            raise ValueError("Rows cannot be negative")

        self._rows = rows
        # TODO: resize char_area

    @columns.setter
    def columns(self, columns: int) -> None:
        """Set the columns in the area"""
        if columns < 0:
            raise ValueError("Columns cannot be negative")

        self._columns = columns
        # TODO: resize char_area
