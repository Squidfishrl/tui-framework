"""Area for the component when it's rendered"""

from __future__ import annotations

from typing import TYPE_CHECKING

from tui._area_box_model import BoxModel
from tui._coordinates import RestrictedCoordinates, Coordinates

if TYPE_CHECKING:
    from tui.styles.area import AreaInfo


class Area:
    """Area for the component when it's rendered
    Defines how the component looks in isolation (without parents)
    """
    def __init__(
            self,
            area_info: AreaInfo  # min, max rows
    ) -> None:
        self.model = BoxModel(info=area_info)
        self.char_area: list[list[str]] = [  # rows x columns
                [' ' for _ in range(self.columns)]
                for _ in range(self.rows)
            ]

        # used for easier char_area editing.
        self.area_ptr = RestrictedCoordinates(
                    _row=0,
                    _column=0,
                    _restriction=self.model.with_padding
                )

    def add_chars(self, string: str, column_preserve: bool = False) -> None:
        """Add a string starting from area_ptr. '\n' means row increment
        area_ptr is unaffected
        """

        initital_coords = Coordinates(
                    _row=self.area_ptr.row,
                    _column=self.area_ptr.column
                )

        if not self._verify_str(
                string=string,
                column_preserve=column_preserve
        ):
            raise IndexError("String is too large")

        for count, char in enumerate(string):
            if char == '\n':
                # if area_ptr is on the last row and the last char is a newline
                # area_ptr restriction would activate, hence the latter check
                if count >= len(string) - 1:
                    break

                self.area_ptr.row += 1
                if column_preserve:
                    self.area_ptr.column = initital_coords.column
                else:
                    self.area_ptr.column = (
                            self.area_ptr.restriction.top_left.column
                        )

                continue

            self.char_area[self.area_ptr.row][self.area_ptr.column] = char

            # Required to prevent RestrictedCoordinates exception
            if (self.area_ptr.column < self.area_ptr.restriction.bottom_right
                    .column):
                self.area_ptr.column += 1

        self.area_ptr.row = initital_coords.row
        self.area_ptr.column = initital_coords.column

    def _verify_str(self, string: str, column_preserve: bool) -> bool:
        """Verify that string can fit in char_area - used in add_chars"""
        row = self.area_ptr.row
        column = self.area_ptr.column

        for char in string:
            if char == '\n':
                row += 1
                if column_preserve:
                    column = self.area_ptr.column
                else:
                    column = self.area_ptr.restriction.top_left.column

                continue

            if (row >= self.area_ptr.restriction.rows or
                    column >= self.area_ptr.restriction.columns):
                return False

            column += 1

        return True

    def __str__(self):
        return "\n".join(
                ["".join(list(row)) for row in self.char_area]
            )

    @property
    def rows(self) -> int:
        """Get the rows in the area"""
        return self.model.info.rows

    @property
    def columns(self) -> int:
        """Get the columns in the area"""
        return self.model.info.columns

    @rows.setter
    def rows(self, rows: int) -> None:
        """Set the rows in the area"""
        raise NotImplementedError

    @columns.setter
    def columns(self, columns: int) -> None:
        """Set the columns in the area"""
        raise NotImplementedError
